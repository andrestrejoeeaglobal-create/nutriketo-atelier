import os

workspace = r"c:\Users\andre\OneDrive\Escritorio\nutriketo"

for root, dirs, files in os.walk(workspace):
    for f in files:
        if "index.html" in f:
            full = os.path.join(root, f)
            size = os.path.getsize(full)
            print(f"Found: {full} (Size: {size} bytes)")
            with open(full, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                if "02 al 08 de Agosto" in content:
                    print("  --> HAS OLD STRING '02 al 08 de Agosto'")
                else:
                    print("  --> DOES NOT HAVE OLD STRING")
