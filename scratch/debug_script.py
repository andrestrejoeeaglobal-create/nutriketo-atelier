with open('scratch/script_3.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
stack = []
in_str = None

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
            elif c == '{':
                stack.append(('{', line_no, i+1))
            elif c == '}':
                if stack and stack[-1][0] == '{':
                    stack.pop()
                else:
                    print(f"Unmatched '}}' at line {line_no}:{i+1}")
            elif c == '(':
                stack.append(('(', line_no, i+1))
            elif c == ')':
                if stack and stack[-1][0] == '(':
                    stack.pop()
                else:
                    print(f"Unmatched ')' at line {line_no}:{i+1}")
        i += 1

print(f"Final stack length: {len(stack)}")
print(f"In string: {in_str}")
for item in stack:
    print(f"  Unclosed {item[0]} at line {item[1]}:{item[2]}")
