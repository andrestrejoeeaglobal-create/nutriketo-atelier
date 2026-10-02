# -*- coding: utf-8 -*-
"""
Script maestro para compilar la Semana 41 completa:
- semana_41_master.json
- expediente_completo_semana_41.md
- Sincronización en brain artifacts
"""

import os
import sys
import json
import shutil

sys.path.insert(0, os.path.abspath('.'))

from scratch.s41_data import get_semana_41_data
from scratch.s41_markdown_builder import generate_s41_markdown

def main():
    print("Compilando Semana 41...")
    data = get_semana_41_data()
    
    # 1. Guardar semana_41_master.json
    json_path = 'semana_41_master.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Generado {json_path} con éxito.")
    
    # 2. Generar expediente_completo_semana_41.md
    md_content = generate_s41_markdown(data)
    md_path = 'expediente_completo_semana_41.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Generado {md_path} con éxito ({len(md_content)} caracteres).")
    
    # 3. Copiar a la carpeta de artefactos
    art_dir = r"C:\Users\andre\.gemini\antigravity\brain\77a3e1ca-fab2-4f79-b956-c9dd52a8791d"
    if os.path.exists(art_dir):
        art_path = os.path.join(art_dir, 'expediente_completo_semana_41.md')
        with open(art_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Copiado artefacto a {art_path}")

if __name__ == '__main__':
    main()
