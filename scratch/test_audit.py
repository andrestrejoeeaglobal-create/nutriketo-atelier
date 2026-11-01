import re
import unicodedata

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

# Extract areInsumosEquivalent from generate_standalone_html.py or check in python
with open('generate_standalone_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect what items in Week 41 and Week 42 BOM exist and how they match against pantry
import json
with open('semana_41_master.json', 'r', encoding='utf-8') as f:
    s41 = json.load(f)

print("Week 41 loaded successfully")
