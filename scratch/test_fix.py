import subprocess

with open('scratch/script_3.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Append closing braces/parens one by one to see how many are missing
appendages = ["}", "});", "};", "}", "})", "}", "};"]
for i in range(1, 10):
    for suffix in ["\n" + "}\n" * i, "\n" + "});\n" * i, "\n" + "}\n" * i + "});\n"]:
        test_code = code + suffix
        with open('scratch/test_fix.js', 'w', encoding='utf-8') as tf:
            tf.write(test_code)
        res = subprocess.run(['node', '--check', 'scratch/test_fix.js'], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"SUCCESSFULLY FIXED BY APPENDING: {repr(suffix)}")
            break
    else:
        continue
    break
else:
    print("Could not fix by simple appendage, searching deeper...")
