import json
import re
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from generate_standalone_html import build_typed_recipe_for_dish
from app.services.keto_architect import KetoAIArchitect

def normalize_shopping_item(iname: str, category: str, unit: str, base_qty: float):
    name_clean = re.sub(r'^[^\w\s]+\s*', '', iname.lower().strip())
    clean_unit = unit.strip()
    scaled_qty = base_qty
    
    # 1. Formula 33Plus & 34Plus
    if "33plus" in name_clean:
        return ("Fórmula Biotecnológica Nootrópica 33Plus®", "💊 SUPLEMENTACIÓN CELULAR / BIOTECNOLOGÍA", "33plus_formula", "g", scaled_qty)
    if "34plus" in name_clean:
        return ("Fórmula Biotecnológica Reparadora 34Plus®", "💊 SUPLEMENTACIÓN CELULAR / BIOTECNOLOGÍA", "34plus_formula", "g", scaled_qty)
        
    # 2. Aguacate Hass
    if "aguacate" in name_clean or "guacamole" in name_clean:
        if clean_unit.lower() in ["g", "grams"]:
            qty_piezas = scaled_qty / 150.0
            return ("Aguacate Hass fresco", "🥑 Grasas Saludables y Frutos", "aguacate_hass", "piezas", qty_piezas)
        return ("Aguacate Hass fresco", "🥑 Grasas Saludables y Frutos", "aguacate_hass", "piezas", scaled_qty)
        
    # 3. Mantequilla / Ghee
    if "mantequilla" in name_clean or "ghee" in name_clean:
        return ("Mantequilla de pastoreo / Ghee", "🥑 Grasas Saludables y Frutos", "mantequilla_pastoreo", "g", scaled_qty)

    # 4. Pechuga de pavo vs Tocino de pavo
    if "tocino de pavo" in name_clean:
        return ("Tocino de pavo artesanal crujiente", "🥩 Proteínas Principales Seleccionadas", "tocino_pavo", "piezas", scaled_qty)
    if "pavo" in name_clean:
        if clean_unit.lower() in ["piezas", "pieza"]:
            return ("Pechuga de pavo artesanal", "🥩 Proteínas Principales Seleccionadas", "pechuga_pavo", "g", scaled_qty * 150.0)
        return ("Pechuga de pavo artesanal", "🥩 Proteínas Principales Seleccionadas", "pechuga_pavo", "g", scaled_qty)

    # 5. Machaca Artesanal
    if "machaca" in name_clean:
        return ("Carne seca machaca artesanal de res", "🥩 Proteínas Principales Seleccionadas", "machaca_artesanal", "g", scaled_qty)

    # 6. Pechuga de pollo
    if "pollo" in name_clean:
        return ("Pechuga de pollo orgánica", "🥩 Proteínas Principales Seleccionadas", "pechuga_pollo", "g", scaled_qty)

    # 7. Sal de mar
    if "sal" in name_clean:
        return ("Sal de mar mineral en escamas", "🧂 Condimentos y Sal Mineral", "sal_marina", "g", scaled_qty)

    # 8. Jugo de limón
    if "limón" in name_clean or "limon" in name_clean:
        return ("Jugo de limón fresco recién exprimido", "🍋 Cítricos y Ácidos Naturales", "jugo_limon", "ml", scaled_qty)

    # 9. Sésamo / Ajonjolí
    if "sésamo" in name_clean or "sesamo" in name_clean or "ajonjolí" in name_clean:
        return ("Semillas de sésamo tostadas", "🌰 Semillas y Nueces", "semillas_sesamo", "g", scaled_qty)

    # 10. Fruits
    if any(k in name_clean for k in ["granada", "arilos de granada"]):
        return ("Arilos de Granada fresca de la granja", "🍓 Frutas Keto y Cosecha Viva", "granada_fresca", "g", scaled_qty)
    if any(k in name_clean for k in ["higo", "higos"]):
        return ("Higos frescos vivos de la granja", "🍓 Frutas Keto y Cosecha Viva", "higos_frescos", "g", scaled_qty)
    if any(k in name_clean for k in ["pitaya", "pitahaya"]):
        return ("Pitaya fresca de la granja", "🍓 Frutas Keto y Cosecha Viva", "pitaya_fresca", "g", scaled_qty)
    if any(k in name_clean for k in ["frambuesa", "frambuesas"]):
        return ("Frambuesas frescas orgánicas", "🍓 Frutas Keto y Cosecha Viva", "frambuesas_frescas", "g", scaled_qty)
    if any(k in name_clean for k in ["arándano", "arandano", "arándanos", "arandanos"]):
        return ("Arándanos frescos orgánicos", "🍓 Frutas Keto y Cosecha Viva", "arandanos_frescos", "g", scaled_qty)
    if any(k in name_clean for k in ["fresa", "fresas"]):
        return ("Fresas frescas de la granja", "🍓 Frutas Keto y Cosecha Viva", "fresas_frescas", "g", scaled_qty)
    if any(k in name_clean for k in ["mora", "moras"]):
        return ("Moras frescas de la granja", "🍓 Frutas Keto y Cosecha Viva", "moras_frescas", "g", scaled_qty)

    # 11. Vegetables
    if "espárrago" in name_clean or "esparrago" in name_clean:
        return ("Espárragos verdes frescos de la granja", "🥦 Hortalizas y Vegetales Córtex", "esparragos_verdes", "g", scaled_qty)
    if "calabacita" in name_clean or "zucchini" in name_clean:
        return ("Calabacitas tiernas de la granja", "🥦 Hortalizas y Vegetales Córtex", "calabacitas_tiernas", "g", scaled_qty)
    if "lechuga" in name_clean:
        return ("Hojas de lechuga orejona viva", "🥬 Hojas Verdes y Envolturas", "lechuga_orejona_viva", "g", scaled_qty)
    if "pepino" in name_clean:
        return ("Pepino blanco fresco de la granja", "🥦 Hortalizas y Vegetales Córtex", "pepino_blanco", "g", scaled_qty)
    if "apio" in name_clean:
        return ("Apio fresco de la granja", "🥦 Hortalizas y Vegetales Córtex", "apio_fresco", "g", scaled_qty)
    if "hinojo" in name_clean:
        return ("Hinojo fresco de la granja", "🥦 Hortalizas y Vegetales Córtex", "hinojo_fresco", "g", scaled_qty)
    if "arúgula" in name_clean or "arugula" in name_clean:
        return ("Hojas de arúgula fresca", "🥬 Hojas Verdes y Envolturas", "arugula_fresca", "g", scaled_qty)
    if "espinaca" in name_clean or "espinacas" in name_clean:
        return ("Espinacas baby frescas de la granja", "🥬 Hojas Verdes y Envolturas", "espinacas_baby", "g", scaled_qty)
    if "nopal" in name_clean or "nopales" in name_clean:
        return ("Nopales tiernos limpios de la granja", "🥦 Hortalizas y Vegetales Córtex", "nopales_tiernos", "g", scaled_qty)
    if "chayote" in name_clean or "chayotes" in name_clean:
        return ("Chayotes tiernos de la granja", "🥦 Hortalizas y Vegetales Córtex", "chayote_tierno", "g", scaled_qty)
    if "ejote" in name_clean or "ejotes" in name_clean:
        return ("Ejotes verdes frescos de la granja", "🥦 Hortalizas y Vegetales Córtex", "ejotes_frescos", "g", scaled_qty)

    # 12. Proteins
    if "sirloin" in name_clean:
        return ("Carne molida / Filete de Sirloin magro", "🥩 Proteínas Principales Seleccionadas", "carne_sirloin", "g", scaled_qty)
    if "ribeye" in name_clean:
        return ("Corte de Ribeye de res premium", "🥩 Proteínas Principales Seleccionadas", "ribeye_res", "g", scaled_qty)
    if "salmón" in name_clean or "salmon" in name_clean:
        return ("Filete de Salmón fresco con piel", "🥩 Proteínas Principales Seleccionadas", "filete_salmon", "g", scaled_qty)
    if "atún" in name_clean or "atun" in name_clean:
        return ("Medallón de Atún fresco", "🥩 Proteínas Principales Seleccionadas", "atun_fresco", "g", scaled_qty)
    if "pescado" in name_clean:
        return ("Filete de Pescado blanco fresco", "🥩 Proteínas Principales Seleccionadas", "pescado_blanco", "g", scaled_qty)
    if "huachinango" in name_clean:
        return ("Filete de Huachinango fresco", "🥩 Proteínas Principales Seleccionadas", "huachinango_fresco", "g", scaled_qty)

    return (iname.strip(), category, name_clean, unit, scaled_qty)


architect = KetoAIArchitect()
s40_plan = architect.build_semana_40_plan(diners_count=6)
s40 = s40_plan.model_dump()

diners = 6

lines = []
lines.append("# 📄 Expediente Técnico Canónico Semanal — Semana 40")
lines.append("**Semana 40 (27 de Septiembre al 03 de Octubre de 2026)**  ")
lines.append("**Ecosistema:** NutriKeto Atelier T.I.L.O.® — Arquitectura Bioquímica SSOT V36.6 REV3  ")
lines.append(f"**Comensales Activos:** {diners} Personas  ")
lines.append("")
lines.append("---")
lines.append("")

lines.append("## 1. Menú Sintético Semanal (Visión Ejecutiva)")
lines.append("| Día | Desayuno (Huevo Orgánico & Nootrópico) | Comida (3 Tiempos Atwater) | Cena (Digestión Ligera & 34Plus®) |")
lines.append("|---|---|---|---|")

for day in s40.get("days", []):
    d_name = f"**{day['day']} {day['date_str']}**"
    des = day['meals'][0]['main_dish_name'] if len(day['meals']) > 0 else ""
    com = day['meals'][1]['main_dish_name'] if len(day['meals']) > 1 else ""
    cen = day['meals'][2]['main_dish_name'] if len(day['meals']) > 2 else ""
    lines.append(f"| {d_name} | {des} | {com} | {cen} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## 2. Recetario Canónico Día por Día")
lines.append("")

shopping_map = {}

for day in s40.get('days', []):
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
                    
                    c_name, c_cat, c_key, c_unit, calc_qty = normalize_shopping_item(iname, grp['category'], unit, total_qty)
                    map_key = c_key
                    if map_key not in shopping_map:
                        shopping_map[map_key] = {'name': c_name, 'total_qty': 0.0, 'unit': c_unit, 'category': c_cat}
                    shopping_map[map_key]['total_qty'] += calc_qty

            lines.append('')
            lines.append('**Procedimiento Paso a Paso:**')
            for step in recipe.get('steps', []):
                lines.append(f"{step}")
            lines.append('')

lines.append('---')
lines.append('')
lines.append('## 3. Lista de Compras Consolidada')
lines.append('**Total Insumos Requeridos para 6 Comensales durante 7 Días Completos (Semana 40):**')
lines.append('')
lines.append('| Insumo | Cantidad Total (6 Comensales) | Unidad | Categoría |')
lines.append('|---|---|---|---|')

for k in sorted(shopping_map.keys(), key=lambda x: (shopping_map[x]['category'], shopping_map[x]['name'])):
    item = shopping_map[k]
    lines.append(f"| **{item['name']}** | {item['total_qty']:g} | {item['unit']} | {item['category']} |")

output_text = '\n'.join(lines)

with open('expediente_completo_semana_40.md', 'w', encoding='utf-8') as out_f:
    out_f.write(output_text)

art_dir = r'C:\Users\andre\.gemini\antigravity\brain\99ee14ae-61ae-4f7d-85f3-3786e9a90a04'
art_path = os.path.join(art_dir, 'expediente_completo_semana_40.md')
with open(art_path, 'w', encoding='utf-8') as art_f:
    art_f.write(output_text)

print(f"Expediente Semana 40 generado exitosamente en {art_path}. Total de líneas: {len(lines)}")
