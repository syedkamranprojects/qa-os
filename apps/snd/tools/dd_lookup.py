"""Search the S&D table catalog (snd_tables.json) without loading it all into context.

  python dd_lookup.py substitution          # tables/columns whose name or description matches
  python dd_lookup.py -t SND_PR_PRS_SUBSTITUTION_MAP   # full column list of one table
  python dd_lookup.py -r SND_PR_CHH_CHANEL_HIERARCHY   # tables with an FK referencing it
  python dd_lookup.py -s "Outlet Code"      # screen caption -> table.column (Mapping sheets)
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge')
T = json.load(open(os.path.join(HERE, 'snd_tables.json'), encoding='utf-8'))['tables']

def show_table(name):
    e = T.get(name.upper())
    if not e:
        sys.exit(f'no table {name}')
    print(f'{name.upper()}  [{e["module"]}]  {e["description"] or ""}')
    print(f'  PK: {", ".join(e["primary_key"]) or "-"}   sheet: {e["source_sheet"]}')
    for c in e['columns']:
        flags = ('PK ' if c['pk'] else '') + (f'FK->{c["references"] or "?"}' if c['fk'] else '')
        print(f'  {c["name"]:<34} {c["type"] or "":<15} {flags:<40} {c["description"] or ""}')

args = sys.argv[1:]
if not args:
    sys.exit(__doc__)
if args[0] == '-t':
    show_table(args[1])
elif args[0] == '-r':
    target = args[1].upper()
    for t, e in T.items():
        cols = [c['name'] for c in e['columns'] if c['references'] == target]
        if cols:
            print(f'{t}: {", ".join(cols)}')
elif args[0] == '-s':
    m = json.load(open(os.path.join(HERE, 'snd_screen_field_map.json'), encoding='utf-8'))['screens']
    rx = re.compile(args[1], re.I)
    for screen, rows in m.items():
        for r in rows:
            if rx.search(r['caption']):
                print(f'{screen} / {r["screen_tab"]} / {r["caption"]} -> {r["table"]}.{r["column"]} ({r["type"]})')
else:
    rx = re.compile(' '.join(args), re.I)
    for t, e in T.items():
        if rx.search(t) or rx.search(e['description'] or ''):
            print(f'TABLE  {t}  [{e["module"]}]  {e["description"] or ""}')
    for t, e in T.items():
        for c in e['columns']:
            if rx.search(c['name']) or rx.search(c['description'] or ''):
                print(f'COLUMN {t}.{c["name"]}  {c["description"] or ""}')
