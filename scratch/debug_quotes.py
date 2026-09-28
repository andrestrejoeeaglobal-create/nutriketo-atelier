with open('scratch/script_3.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
in_str = None
in_str_line = 0

for line_no, line in enumerate(lines, 1):
    i = 0
    while i < len(line):
        c = line[i]
        if in_str:
            if in_str == '`' and c == '`':
                in_str = None
            elif in_str != '`' and c == in_str and (i == 0 or line[i-1] != '\\'):
                in_str = None
        else:
            if c in ['"', "'", '`']:
                in_str = c
                in_str_line = line_no
        i += 1
    if in_str == "'":
        print(f"Line {line_no} ended while in single quote string (started line {in_str_line})")
