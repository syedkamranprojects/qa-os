"""Build the injectable page helper: qaos_helpers.js -> qaos_helpers.min.js (no comments, no blank lines).

    python plugins/qa-os/runtime/build_helper.py

Why: the recorder injects the helper through the browser MCP's execute_script. Comments made the text long and
backticks/escapes in comments broke template-string injection. The build keeps the code byte-for-byte except:
  * block comments (/* ... */) are removed,
  * lines that start with // (after indentation) are removed (code lines containing '//' inside strings, such as
    xpaths, are kept because they do not start with //),
  * blank lines are removed.
It refuses to build if the source contains a backtick or a NUL byte, and checks the result with `node --check`
when node is available.

Injection (recording-protocol): read qaos_helpers.min.js and pass its text as the FIRST ARGUMENT of execute_script:
    script: "localStorage.qaos_src = arguments[0]; eval(arguments[0]); return qaos.watch();"
    args:   ["<contents of qaos_helpers.min.js>"]
Passing the code as an argument means no quoting or escaping inside the script text.
"""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, 'qaos_helpers.js'), os.path.join(HERE, 'qaos_helpers.min.js')

src = open(SRC, encoding='utf-8').read()
if '`' in src or '\x00' in src:
    sys.exit('refused: qaos_helpers.js contains a backtick or a NUL byte')
code = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
lines = [l.rstrip() for l in code.splitlines()]
lines = [l for l in lines if l.strip() and not l.lstrip().startswith('//')]
out = '\n'.join(lines) + '\n'
open(OUT, 'w', encoding='utf-8', newline='\n').write(out)
if shutil.which('node'):
    r = subprocess.run(['node', '--check', OUT], capture_output=True, text=True)
    if r.returncode:
        sys.exit('built file failed node --check:\n' + r.stderr)
print(f'{OUT}: {len(out)} chars (source {len(src)})')
