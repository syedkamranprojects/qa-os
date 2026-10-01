"""Profile legacy Regress case-data workbooks (framework/casedata-samples/*.xlsx).

Reports: control-column usage and value vocab, header conventions, value formats (dates, codes),
PK linking parent -> child sheets, and writes a JSON profile for bulk-data-factory.

  python framework/tools/analyse_casedata.py [--screens screens.json] > report.txt
  (screens.json: optional [{"psc_screenid","psc_screenname"}] from CTA_CONFIG_ASSERTION to check sheet names)
"""
import collections, datetime as dt, glob, json, os, re, sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = os.path.join(HERE, '..', 'casedata-samples')
CONTROL = ['PK', 'PK_DESC', 'STPONERR', 'CASE_TYPE', 'EXPECTED_INPUT', 'EXPECTED_MESSAGE', 'CHECK_VALIDATION', 'EVENT_ID', 'SWIPE']

screens = None
if '--screens' in sys.argv:
    screens = {s['psc_screenname'].strip().lower(): s['psc_screenid'] for s in json.load(open(sys.argv[sys.argv.index('--screens') + 1], encoding='utf-8'))}


def kind(v):
    if v is None or v == '':
        return 'empty'
    if isinstance(v, (dt.datetime, dt.date)):
        return 'excel-date'
    if isinstance(v, bool):
        return 'bool'
    if isinstance(v, (int, float)):
        return 'number'
    s = str(v)
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', s): return 'text-date yyyy-mm-dd'
    if re.fullmatch(r'\d{2}[-/]\d{2}[-/]\d{4}', s): return 'text-date dd-mm-yyyy'
    if re.fullmatch(r'\d{1,2}-[A-Za-z]{3}-\d{2,4}', s): return 'text-date dd-Mon-yy'
    if re.fullmatch(r'\d+', s): return 'digits'
    if re.fullmatch(r'[A-Z0-9_-]+', s): return 'code'
    if ' - ' in s or re.match(r'^\S+-\S', s): return 'code-desc'
    return 'text'


profile = {}
ctl_values = collections.defaultdict(collections.Counter)
ctl_presence = collections.Counter()
header_style = collections.Counter()
field_kinds = collections.defaultdict(collections.Counter)
per_field_ctl = collections.Counter()
sheet_counts = {}
pk_links = collections.Counter()
unmatched_sheets = collections.Counter()
total_sheets = 0

for f in sorted(glob.glob(os.path.join(SAMPLES, '*.xlsx'))):
    if os.path.basename(f).startswith('~$'):
        continue
    wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
    name = os.path.basename(f)
    sheets = {}
    for ws in wb.worksheets:
        rows = [r for r in ws.iter_rows(values_only=True)]
        if not rows:
            continue
        hdr = [str(h).strip() if h is not None else None for h in rows[0]]
        data = [r for r in rows[1:] if any(c not in (None, '') for c in r)]
        total_sheets += 1
        if screens is not None and ws.title.strip().lower() not in screens:
            unmatched_sheets[ws.title] += 1
        cols = {}
        for i, h in enumerate(hdr):
            if not h:
                continue
            up = h.upper()
            base = re.sub(r'#\d+$', '', up)
            if base in CONTROL:
                ctl_presence[base] += 1
                for r in data:
                    if i < len(r) and r[i] not in (None, ''):
                        ctl_values[base][str(r[i])[:60]] += 1
            elif any(up.endswith('_' + c) for c in ('CASE_TYPE', 'EXPECTED_MESSAGE', 'EXPECTED_INPUT')):
                per_field_ctl[re.sub(r'^.*?_(CASE_TYPE|EXPECTED_MESSAGE|EXPECTED_INPUT)$', r'\1', up)] += 1
            else:
                header_style['lower_snake' if re.fullmatch(r'[a-z0-9_.]+', h) else
                             'UPPER_SNAKE' if re.fullmatch(r'[A-Z0-9_.#]+', h) else
                             'repo_' if h.lower().startswith('repo_') else 'caption/other'] += 1
                for r in data:
                    if i < len(r):
                        field_kinds[h.lower()][kind(r[i])] += 1
            cols[h] = [r[i] if i < len(r) else None for r in data]
        pks = [str(v) for v in cols.get('PK', []) if v not in (None, '')]
        sheets[ws.title] = {'headers': [h for h in hdr if h], 'rows': len(data), 'pks': pks[:50]}
    # PK linking: a child sheet whose PKs are all found in another sheet
    for a, sa in sheets.items():
        for b, sb in sheets.items():
            if a != b and sb['pks'] and sa['pks'] and set(sb['pks']) <= set(sa['pks']) and len(set(sa['pks'])) > 1:
                pk_links[(name, a, b)] += 1
    profile[name] = sheets
    sheet_counts[name] = (len(sheets), sum(s['rows'] for s in sheets.values()))

print('# Case-data samples profile\n')
for n, (s, r) in sheet_counts.items():
    print(f'- {n}: {s} sheets, {r} data rows')
print(f'\n## Control columns (sheets using them, of {total_sheets})')
for c in CONTROL:
    top = ', '.join(f'{v!r}×{n}' for v, n in ctl_values[c].most_common(8))
    print(f'- {c}: {ctl_presence[c]} sheets; values: {top}')
print(f'- per-field variants (<col>_CASE_TYPE etc.): {dict(per_field_ctl)}')
print('\n## Field header style:', dict(header_style))
kinds_total = collections.Counter()
for h, k in field_kinds.items():
    kinds_total.update(k)
print('## Field value kinds (all cells):', dict(kinds_total.most_common()))
dates = collections.Counter({k: v for k, v in kinds_total.items() if 'date' in k})
print('## Date formats:', dict(dates))
samples = [(h, k.most_common(1)[0]) for h, k in field_kinds.items() if any('code-desc' == x for x in k)]
print('## Fields holding "code - description" values (first 15):', [h for h, _ in samples[:15]])
print(f'\n## PK parent -> child links (first 25 of {len(pk_links)})')
for (n, a, b) in list(pk_links)[:25]:
    print(f'- {n}: {a} -> {b}')
if screens is not None:
    print(f'\n## Sheets not matching any psc_screenname ({len(unmatched_sheets)}):', list(unmatched_sheets)[:40])
json.dump(profile, open(os.path.join(HERE, '..', 'casedata_profile.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
