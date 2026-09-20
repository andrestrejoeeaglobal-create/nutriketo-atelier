import json
import re
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from generate_standalone_html import build_typed_recipe_for_dish

def normalize_shopping_item(iname: str, category: str):
    name_clean = re.sub(r'^[^\w\s]+\s*', '', iname.lower().strip())
    
    if any(k in name_clean for k in ["granada", "arilos de granada"]):
        return ("Arilos de Granada fresca de la granja", "🍓 Frutas Keto y Cosecha Viva", "granada_fresca")
    if any(k in name_clean for k in ["higo", "higos"]):
        return ("Higos frescos vivos de la granja", "🍓 Frutas Keto y Cosecha Viva", "higos_frescos")
    if any(k in name_clean for k in ["pitaya", "pitahaya"]):
        return ("Pitaya fresca de la granja", "🍓 Frutas Keto y Cosecha Viva", "pitaya_fresca")
    if any(k in name_clean for k in ["frambuesa", "frambuesas"]):
        return ("Frambuesas frescas orgánicas", "🍓 Frutas Keto y Cosecha Viva", "frambuesas_frescas")
    if any(k in name_clean for k in ["arándano", "arandano", "arándanos", "arandanos"]):
        return ("Arándanos frescos orgánicos", "🍓 Frutas Keto y Cosecha Viva", "arandanos_frescos")
    if any(k in name_clean for k in ["fresa", "fresas"]):
        return ("Fresas frescas de la granja", "🍓 Frutas Keto y Cosecha Viva", "fresas_frescas")
    if any(k in name_clean for k in ["mora", "moras"]):
        return ("Moras frescas de la granja", "🍓 Frutas Keto y Cosecha Viva", "moras_frescas")
    if "espárrago" in name_clean or "esparrago" in name_clean:
        return ("Espárragos verdes frescos de la granja", "🥦 Hortalizas y Vegetales Córtex", "esparragos_verdes")
    if "calabacita" in name_clean or "zucchini" in name_clean:
        return ("Calabacitas tiernas de la granja", "🥦 Hortalizas y Vegetales Córtex", "calabacitas_tiernas")
    if "aguacate" in name_clean or "guacamole" in name_clean:
        return ("Aguacate Hass fresco", "🥑 Grasas Saludables y Frutos", "aguacate_hass")
    if "lechuga" in name_clean:
        return ("Hojas de lechuga orejona viva", "🥬 Hojas Verdes y Envolturas", "lechuga_orejona_viva")
    if "pepino" in name_clean:
        return ("Pepino blanco fresco de la granja", "🥦 Hortalizas y Vegetales Córtex", "pepino_blanco")
    if "apio" in name_clean:
        return ("Apio fresco de la granja", "🥦 Hortalizas y Vegetales Córtex", "apio_fresco")
    if "hinojo" in name_clean:
        return ("Hinojo fresco de la granja", "🥦 Hortalizas y Vegetales Córtex", "hinojo_fresco")
    if "arúgula" in name_clean or "arugula" in name_clean:
        return ("Hojas de arúgula fresca", "🥬 Hojas Verdes y Envolturas", "arugula_fresca")
    if "espinaca" in name_clean or "espinacas" in name_clean:
        return ("Espinacas baby frescas de la granja", "🥬 Hojas Verdes y Envolturas", "espinacas_baby")
    if "nopal" in name_clean or "nopales" in name_clean:
        return ("Nopales tiernos limpios de la granja", "🥦 Hortalizas y Vegetales Córtex", "nopales_tiernos")
    if "chayote" in name_clean or "chayotes" in name_clean:
        return ("Chayotes tiernos de la granja", "🥦 Hortalizas y Vegetales Córtex", "chayote_tierno")
    if "ejote" in name_clean or "ejotes" in name_clean:
        return ("Ejotes verdes frescos de la granja", "🥦 Hortalizas y Vegetales Córtex", "ejotes_frescos")
    if "sirloin" in name_clean:
        return ("Carne molida / Filete de Sirloin magro", "🥩 Proteínas Principales Seleccionadas", "carne_sirloin")
    if "ribeye" in name_clean:
        return ("Corte de Ribeye de res premium", "🥩 Proteínas Principales Seleccionadas", "ribeye_res")
    if "salmón" in name_clean or "salmon" in name_clean:
        return ("Filete de Salmón fresco con piel", "🥩 Proteínas Principales Seleccionadas", "filete_salmon")
    if "pescado blanco" in name_clean or "robalo" in name_clean:
        return ("Filete de Pescado Blanco (Robalo)", "🥩 Proteínas Principales Seleccionadas", "pescado_blanco")
    if "huachinango" in name_clean:
        return ("Filete de Huachinango fresco", "🥩 Proteínas Principales Seleccionadas", "huachinango_fresco")
    if "atún" in name_clean or "atun" in name_clean:
        return ("Lomo de Atún fresco corte sashimi", "🥩 Proteínas Principales Seleccionadas", "lomo_atun")
    if "pavo" in name_clean:
        return ("Pechuga de pavo artesanal", "🥩 Proteínas Principales Seleccionadas", "pechuga_pavo")
    if "pollo" in name_clean:
        return ("Pechuga de pollo orgánica", "🥩 Proteínas Principales Seleccionadas", "pechuga_pollo")
    if "claras de huevo" in name_clean:
        return ("Claras de huevo frescas orgánicas", "🥚 Huevo y Derivados", "claras_huevo")
    if "huevos" in name_clean or "huevo" in name_clean:
        return ("Huevos orgánicos de libre pastoreo", "🥚 Huevo y Derivados", "huevos_organicos")
    if "mantequilla" in name_clean or "ghee" in name_clean:
        return ("Mantequilla de pastoreo / Ghee", "🥑 Grasas Saludables y Frutos", "mantequilla_pastoreo")
    if "aceite de oliva" in name_clean or "vevo" in name_clean:
        return ("Aceite de oliva extra virgen (VEVO)", "🥑 Grasas Saludables y Frutos", "aceite_vevo")
    if "limón" in name_clean or "limon" in name_clean:
        return ("Jugo de limón fresco recién exprimido", "🍋 Cítricos y Ácidos Naturales", "jugo_limon")
    if "sal" in name_clean:
        return ("Sal de mar mineral en escamas", "🧂 Condimentos y Sal Mineral", "sal_marina")
    if "pimienta" in name_clean:
        return ("Pimienta negra en grano / molida", "🧂 Condimentos y Sal Mineral", "pimienta_negra")
    if "chía" in name_clean or "chia" in name_clean:
        return ("Semillas de chía orgánicas", "🌰 Semillas y Nueces", "semillas_chia")
    if "almendras" in name_clean:
        return ("Almendras fileteadas tostadas", "🌰 Semillas y Nueces", "almendras_fileteadas")
    if "nuez pecana" in name_clean:
        return ("Nuez pecana troceada", "🌰 Semillas y Nueces", "nuez_pecana")
    if "nuez de castilla" in name_clean:
        return ("Nuez de Castilla troceada", "🌰 Semillas y Nueces", "nuez_castilla")
    if "girasol" in name_clean:
        return ("Semillas de girasol tostadas", "🌰 Semillas y Nueces", "semillas_girasol")
    if "sésamo" in name_clean or "ajonjolí" in name_clean:
        return ("Semillas de sésamo tostadas", "🌰 Semillas y Nueces", "semillas_sesamo")

    clean_disp = re.sub(r'^[^\w\s]+\s*', '', iname).strip()
    clean_disp = re.sub(r'\s+seleccionado[as]?', '', clean_disp, flags=re.IGNORECASE)
    clean_key = re.sub(r'\W+', '_', clean_disp.lower()).strip('_')
    return (clean_disp, category, clean_key)


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
                    
                    # Accumulate for consolidated shopping list with canonical normalization
                    c_name, c_cat, c_key = normalize_shopping_item(iname, grp['category'])
                    if c_key not in shopping_map:
                        shopping_map[c_key] = {'name': c_name, 'total_qty': 0.0, 'unit': unit, 'category': c_cat}
                    shopping_map[c_key]['total_qty'] += total_qty

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

for k in sorted(shopping_map.keys(), key=lambda x: (shopping_map[x]['category'], shopping_map[x]['name'])):
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
