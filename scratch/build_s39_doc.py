import json
import re
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
import unicodedata
from generate_standalone_html import build_typed_recipe_for_dish

with open('semana_39_master.json', 'r', encoding='utf-8') as f:
    s39 = json.load(f)

diners = s39.get('diners_count', 6)

lines = []
lines.append('# 📑 Expediente Técnico Canónico y Recetario Completo — Semana 39')
lines.append('**Período:** 20 al 26 de Septiembre de 2026  ')
lines.append('**Comensales Fijos:** 6 Personas  ')
lines.append('**Estándar de Gobernanza:** SSOT V36.6 (Atelier T.I.L.O.®)  ')
lines.append('**Estado:** 100% Zero-Mockup / Zero-Template / Recetas Heurísticas Reales  ')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## 📋 Índice del Documento')
lines.append('1. [Resumen Ejecutivo de la Semana 39](#1-resumen-ejecutivo-de-la-semana-39)')
lines.append('2. [Recetario Canónico Día por Día (21 Fichas Técnicas de Ensamblaje)](#2-recetario-canónico-día-por-día)')
lines.append('3. [Lista de Compras Consolidada (BOM 3D Granular)](#3-lista-de-compras-consolidada)')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## 1. Resumen Ejecutivo de la Semana 39')
lines.append('El presente expediente establece la matriz oficial de menús, recetario de precisión culinaria y lista de insumos calculada dinámicamente para los 6 comensales durante la Semana 39.')
lines.append('')
lines.append('| Día | Desayuno | Comida | Cena |')
lines.append('|---|---|---|---|')

for day in s39.get('days', []):
    d_name = f"{day['day']} {day['date_str']}"
    m_des = next((m for m in day['meals'] if m['meal_type'] == 'Desayuno'), {})
    m_com = next((m for m in day['meals'] if m['meal_type'] == 'Comida'), {})
    m_cen = next((m for m in day['meals'] if m['meal_type'] == 'Cena'), {})
    lines.append(f"| **{d_name}** | {m_des.get('main_dish_name', '')} | {m_com.get('main_dish_name', '')} | {m_cen.get('main_dish_name', '')} |")

lines.append('')
lines.append('---')
lines.append('')
lines.append('## 2. Recetario Canónico Día por Día')
lines.append('')

shopping_map = {}

for day in s39.get('days', []):
    lines.append(f"### 📅 {day['day'].upper()} {day['date_str'].upper()}")
    lines.append('')
    for meal in day.get('meals', []):
        mtype = meal.get('meal_type', 'Servicio')
        fat = meal.get('fat_g', 0)
        prot = meal.get('protein_g', 0)
        nc = meal.get('net_carbs_g', 0)
        kcal = fat * 9 + prot * 4 + nc * 4
        lines.append(f"#### 🍽️ Servicio: {mtype.upper()} ({kcal:.0f} kcal Atwater Target)")
        lines.append(f"**Macros 3 Tiempos:** Grasa: `{fat}g` | Proteína: `{prot}g` | Carbs Netos: `{nc}g`  ")
        lines.append('')

        courses = [
            ("🥗 ENTRADA", meal.get('starter_name'), 'starter'),
            ("🥩 PLATILLO PRINCIPAL", meal.get('main_dish_name') or meal.get('dish_name'), 'main'),
            ("🌿 ACOMPAÑAMIENTO / BEBIDA", meal.get('side_dish_name'), 'side')
        ]

        for badge, d_name, course_type in courses:
            if not d_name: continue
            recipe = build_typed_recipe_for_dish(d_name, course_type=course_type)
            lines.append(f"##### {badge}: {recipe['title']}")
            lines.append(f"- **Técnica Culinaria:** `{recipe.get('cooking_technique', 'saute_and_sear')}`")
            lines.append(f"- **Nota Organoléptica:** *\"{recipe.get('sensory_description', '')}\"* ")
            lines.append('')
            lines.append('**Ingredientes (Escalado Fijo para 6 Comensales):**')
            for grp in recipe.get('ingredient_groups', []):
                lines.append(f"- *{grp['category']}*")
                for item in grp.get('items', []):
                    iname = item.get('name') or item.get('item_name')
                    base_qty = float(item.get('base_qty_per_person', 1.0))
                    total_qty = base_qty * diners
                    unit = item.get('unit', 'g')
                    lines.append(f"  - {iname}: **{total_qty:g} {unit}** ({base_qty:g} {unit}/persona)")
                    
                    # Accumulate for consolidated shopping list
                    s_key = iname.lower().strip()
                    if s_key not in shopping_map:
                        shopping_map[s_key] = {'name': iname, 'total_qty': 0.0, 'unit': unit, 'category': grp['category']}
                    shopping_map[s_key]['total_qty'] += total_qty

            lines.append('')
            lines.append('**Procedimiento Paso a Paso:**')
            for step in recipe.get('steps', []):
                lines.append(f"{step}")
            lines.append('')

lines.append('---')
lines.append('')
lines.append('## 3. Lista de Compras Consolidada')
lines.append('**Total Insumos Requeridos para 6 Comensales durante 7 Días Completos (Semana 39):**')
lines.append('')
lines.append('| Insumo | Cantidad Total (6 Comensales) | Unidad | Categoría |')
lines.append('|---|---|---|---|')

for k in sorted(shopping_map.keys()):
    item = shopping_map[k]
    lines.append(f"| **{item['name']}** | {item['total_qty']:g} | {item['unit']} | {item['category']} |")

output_text = '\n'.join(lines)

# Write to workspace file
with open('expediente_completo_semana_39.md', 'w', encoding='utf-8') as out_f:
    out_f.write(output_text)

# Write to artifact directory as well
art_dir = r'C:\Users\andre\.gemini\antigravity\brain\99ee14ae-61ae-4f7d-85f3-3786e9a90a04'
art_path = os.path.join(art_dir, 'expediente_completo_semana_39.md')
with open(art_path, 'w', encoding='utf-8') as art_f:
    art_f.write(output_text)

print(f"Expediente generado exitosamente en {art_path}. Total de líneas: {len(lines)}")
