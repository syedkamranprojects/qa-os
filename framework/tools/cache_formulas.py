"""Give date-formula cells a cached value, the way Excel stores them.

  python framework/tools/cache_formulas.py <workbook.xlsx> [--date YYYY-MM-DD]

Why: openpyxl writes a formula such as =TEXT(NOW(),"YYYY-MM-DD") with an EMPTY cached value (<v></v>). The legacy engine's row check
(ExcelReader.isRowValid) reads the cached value; with none, Apache POI throws, the exception is only printed and the whole screen
is skipped while the run can still look green (verification review v3, 2026-10-01). Excel itself saves a cached result, so the sample
workbooks work. This tool patches the sheet XML: <c r="F2"><f>..</f><v></v></c> -> <c r="F2" t="str"><f>..</f><v>2026-10-01</v></c>.
The formula stays live: the engine computes today's value when it fills the field; the cached text only has to be non-empty and well formed.
Handles formulas TEXT(NOW()|TODAY(),"YYYY-MM-DD") and the SO-number form CONCATENATE("Automation_",TEXT(NOW(),"DD-MM-YYYY")).
Run it as the last step after every workbook write (an openpyxl save drops the cached values again).
"""
import argparse
import datetime
import os
import re
import shutil
import sys
import zipfile

CELL = re.compile(r'<c r="(?P<ref>[A-Z]+\d+)"(?P<attrs>[^>]*)><f>(?P<f>.*?)</f><v\s*/?>(?:</v>)?</c>', re.S)


def cached(formula, day):
    f = formula.replace('&quot;', '"')
    m = re.fullmatch(r'TEXT\((?:NOW|TODAY)\(\),"(?P<fmt>[^"]+)"\)', f)
    if m:
        return fmt(day, m.group('fmt'))
    m = re.fullmatch(r'CONCATENATE\("(?P<pre>[^"]*)",TEXT\((?:NOW|TODAY)\(\),"(?P<fmt>[^"]+)"\)\)', f)
    if m:
        return m.group('pre') + fmt(day, m.group('fmt'))
    return None


def fmt(day, f):
    return f.upper().replace('YYYY', f'{day.year:04d}').replace('MM', f'{day.month:02d}').replace('DD', f'{day.day:02d}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('xlsx')
    ap.add_argument('--date', help='YYYY-MM-DD, default today')
    a = ap.parse_args()
    day = datetime.date.fromisoformat(a.date) if a.date else datetime.date.today()
    tmp = a.xlsx + '.tmp'
    patched, left = [], []
    with zipfile.ZipFile(a.xlsx) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith('xl/worksheets/sheet') and item.filename.endswith('.xml'):
                x = data.decode('utf-8')

                def sub(m):
                    v = cached(m.group('f'), day)
                    if v is None:
                        left.append((item.filename, m.group('ref'), m.group('f')))
                        return m.group(0)
                    patched.append((item.filename, m.group('ref'), v))
                    attrs = re.sub(r'\st="[^"]*"', '', m.group('attrs'))
                    return f'<c r="{m.group("ref")}"{attrs} t="str"><f>{m.group("f")}</f><v>{v}</v></c>'
                data = CELL.sub(sub, x).encode('utf-8')
            zout.writestr(item, data)
    shutil.move(tmp, a.xlsx)
    for f, ref, v in patched:
        print(f'cached {os.path.basename(f)}!{ref} = {v}')
    for f, ref, fo in left:
        print(f'WARNING {os.path.basename(f)}!{ref}: formula {fo} not recognised, cached value still empty')
    print(f'{len(patched)} cell(s) patched, {len(left)} left')
    sys.exit(1 if left else 0)


if __name__ == '__main__':
    main()
