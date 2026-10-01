"""Build the S&D menu catalog from a saved smm_pr_opg_optiongroups (+ apo) query result.

Input : JSON file {result:[{id,pid,lvl,seq,typ,descr,opt,haschild,opt_desc,opt_path,opt_angular,opt_param,is_layout}]}
        produced by the snd-schema MCP query documented in snd_domain_knowledge.md.
Output: snd_menu_tree.json   nested tree
        snd_menu_flat.json   one record per menu leaf/node with full path, option id and route
        snd_menu_outline.md  indented outline for humans / grep
Usage : python snd_menu_build.py <query-result.json>
"""
import json, os, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge')
rows = json.load(open(sys.argv[1], encoding='utf-8'))['result']

by_id = collections.defaultdict(list)          # ids are not guaranteed unique across duplicates
for r in rows:
    by_id[r['id']].append(r)
children = collections.defaultdict(list)
for r in rows:
    children[r['pid']].append(r)
key = lambda r: (int(r['seq']) if str(r['seq'] or '').isdigit() else 9999, r['descr'] or '')

def node(r, path, seen):
    p = path + [r['descr'] or r['id']]
    n = {'group_id': r['id'], 'title': r['descr'], 'level': r['lvl'], 'type': r['typ'],
         'option_id': r['opt'], 'route': r['opt_angular'] or r['opt_path'], 'page_param': r['opt_param'],
         'is_layout': r['is_layout'], 'path': ' > '.join(p)}
    kids = [c for c in sorted(children.get(r['id'], []), key=key) if c['id'] not in seen and c is not r]
    n['children'] = [node(c, p, seen | {r['id']}) for c in kids]
    return n

roots = [r for r in sorted(children.get(None, []), key=key)]
tree = [node(r, [], {r['id']}) for r in roots]

flat, seen_ids = [], set()
def walk(n, depth, out):
    seen_ids.add(n['group_id'])
    flat.append({k: v for k, v in n.items() if k != 'children'})
    out.append('  ' * depth + f"- {n['title']}" + (f"  `{n['option_id']}`" if n['option_id'] else '')
               + (f"  → {n['route']}" if n['route'] else ''))
    for c in n['children']:
        walk(c, depth + 1, out)
outline = []
for n in tree:
    walk(n, 0, outline)

orphans = [r for r in rows if r['id'] not in seen_ids]
leaves = [f for f in flat if f['option_id']]
json.dump(tree, open(os.path.join(HERE, 'snd_menu_tree.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
json.dump(flat, open(os.path.join(HERE, 'snd_menu_flat.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
with open(os.path.join(HERE, 'snd_menu_outline.md'), 'w', encoding='utf-8') as f:
    f.write('# S&D menu outline\n\nFrom `smm_pr_opg_optiongroups` + `smm_pr_apo_appoption` (db ng_astrone). '
            '`option_id` = screen option, `→` = route (Angular path or legacy page).\n'
            'This is the **configured** menu; what a user sees depends on role (`smm_pr_rop_roleoption`).\n\n')
    f.write('\n'.join(outline))
    if orphans:
        f.write(f'\n\n## Not reachable from a root ({len(orphans)})\n\n')
        f.write('\n'.join(f"- {r['descr']} (`{r['id']}`, parent `{r['pid']}`)" for r in orphans))
print(f'rows={len(rows)} roots={len(tree)} nodes={len(flat)} with_option={len(leaves)} orphans={len(orphans)}')
