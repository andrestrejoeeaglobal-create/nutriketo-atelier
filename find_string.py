import os

target = "02 al 08 de Agosto"
workspace = r"c:\Users\andre\OneDrive\Escritorio\nutriketo"

found = []
for root, dirs, files in os.walk(workspace):
    if ".pytest_cache" in root or "__pycache__" in root or ".git" in root:
        continue
    for file in files:
        filepath = os.path.join(root, file)
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if target in content:
                    found.append((filepath, content.count(target)))
        except Exception as e:
            pass

print("SEARCH RESULTS FOR '02 al 08 de Agosto':")
for path, count in found:
    print(f"- {path} ({count} occurrences)")
