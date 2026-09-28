import subprocess

with open('generate_standalone_html.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

# Let's inspect all function declarations in py_code JS template
import re
func_matches = list(re.finditer(r'function\s+([a-zA-Z0-9_]+)\s*\(', py_code))
print(f"Found {len(func_matches)} JS function declarations in generate_standalone_html.py:")
for m in func_matches:
    print(" -", m.group(1))

# Let's check which function is unclosed in script_3.js
with open('scratch/script_3.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

js_func_matches = list(re.finditer(r'function\s+([a-zA-Z0-9_]+)\s*\(', js_code))
for i in range(len(js_func_matches)):
    start_pos = js_func_matches[i].start()
    end_pos = js_func_matches[i+1].start() if i+1 < len(js_func_matches) else len(js_code)
    sub = js_code[:end_pos]
    # append closing brace
    with open('scratch/test_sub.js', 'w', encoding='utf-8') as tf:
        tf.write(sub + '\n}')
    res = subprocess.run(['node', '--check', 'scratch/test_sub.js'], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Function #{i} '{js_func_matches[i].group(1)}' at JS char {start_pos} parses cleanly when closed!")
    else:
        # Check if without extra brace it parses
        with open('scratch/test_sub2.js', 'w', encoding='utf-8') as tf:
            tf.write(sub)
        res2 = subprocess.run(['node', '--check', 'scratch/test_sub2.js'], capture_output=True, text=True)
        if res2.returncode == 0:
            print(f"--> Syntax error occurs IN OR AFTER function #{i} '{js_func_matches[i].group(1)}'")
