# -*- coding: utf-8 -*-
"""
Reconstruye la Sección 2 (Recetario Día por Día) de expediente_completo_semana_40.md
usando los datos reales y normalizados de semana_40_master.json con CoCT completo.
"""

import json
import re
import os

MASTER_PATH = r"C:\Users\andre\OneDrive\Escritorio\Archivos de prueba\nutriketo\semana_40_master.json"
MD_LOCAL = r"C:\Users\andre\OneDrive\Escritorio\Archivos de prueba\nutriketo\expediente_completo_semana_40.md"
MD_ARTIFACT = r"C:\Users\andre\.gemini\antigravity\brain\77a3e1ca-fab2-4f79-b956-c9dd52a8791d\expediente_completo_semana_40.md"

def build_section_2():
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        master = json.load(f)

    lines = ["## 2. Recetario Técnico y Gastronómico Día por Día\n"]

    day_dates = {
        "Domingo": "27 DE SEPTIEMBRE DE 2026",
        "Lunes": "28 DE SEPTIEMBRE DE 2026",
        "Martes": "29 DE SEPTIEMBRE DE 2026",
        "Miércoles": "30 DE SEPTIEMBRE DE 2026",
        "Jueves": "01 DE OCTUBRE DE 2026",
        "Viernes": "02 DE OCTUBRE DE 2026",
        "Sábado": "03 DE OCTUBRE DE 2026"
    }

    for day in master["days"]:
        dname = day["day"]
        date_str = day_dates.get(dname, "")
        lines.append(f"### 📅 {dname.upper()} {date_str}\n")

        for meal in day["meals"]:
            mtype = meal["meal_type"].upper()
            cals = meal.get("calories", 0)
            fat = meal.get("fat_g", 0)
            prot = meal.get("protein_g", 0)
            carbs = meal.get("net_carbs_g", 0)

            lines.append(f"#### 🍽️ Servicio: {mtype} ({cals} kcal Atwater Target)")
            lines.append(f"**Macros 3 Tiempos:** Grasa: `{fat}g` | Proteína: `{prot}g` | Carbs Netos: `{carbs}g`  \n")

            course_meta = [
                ("starter", "🥗 ENTRADA", "starter_name"),
                ("main", "🥩 PLATILLO PRINCIPAL", "main_dish_name"),
                ("side", "🌿 ACOMPAÑAMIENTO / INFUSIÓN / GELATINA", "side_dish_name")
            ]

            for ckey, clabel, cname_key in course_meta:
                cdata = meal.get(ckey, {})
                title = cdata.get("title") or meal.get(cname_key)
                tech = cdata.get("technique", "raw_assembly")
                note = cdata.get("note", "")
                coct = cdata.get("coct_reasoning", {})
                ings = cdata.get("ingredients", [])
                steps = cdata.get("steps", [])

                lines.append(f"##### {clabel}: {title}")
                lines.append(f"- **Técnica Culinaria:** `{tech}`")
                if note:
                    lines.append(f"- **Nota Organoléptica y Bioquímica:** *\"{note}\"*  ")

                if coct:
                    lines.append("- **Razonamiento Culinario CoCT (Física del Bocado):**")
                    if "thermodynamics" in coct:
                        lines.append(f"  - *Termodinámica:* {coct['thermodynamics']}")
                    if "flavor_and_aromatics" in coct:
                        lines.append(f"  - *Construcción de Sabor:* {coct['flavor_and_aromatics']}")
                    if "textural_architecture" in coct:
                        lines.append(f"  - *Arquitectura de Textura:* {coct['textural_architecture']}")
                    if "critical_control_points" in coct:
                        lines.append(f"  - *Puntos Críticos de Control:* {coct['critical_control_points']}")

                lines.append("\n**Ingredientes (Escalado Fijo para 6 Comensales):**")
                for ing in ings:
                    cat = ing.get("category", "Materia Prima")
                    iname = ing.get("name", "")
                    amt = ing.get("amount", 0)
                    unit = ing.get("unit", "")
                    pp = ing.get("per_guest", round(amt/6, 1))
                    lines.append(f"- *{cat}*: {iname}: **{amt} {unit}** ({pp} {unit}/persona)")

                lines.append("\n**Procedimiento de Autor (Pasos Deducidos por CoCT):**")
                for s in steps:
                    # Formato ordenado con negrita en título de paso si tiene ':'
                    if ":" in s and re.match(r'^[0-9]+\.\s+', s):
                        parts = s.split(":", 1)
                        step_title = parts[0].strip()
                        step_body = parts[1].strip()
                        lines.append(f"{step_title}: {step_body}")
                    else:
                        lines.append(f"{s}")
                lines.append("\n---\n")

    return "\n".join(lines)

def update_dossiers():
    sec2_text = build_section_2()

    for path in [MD_LOCAL, MD_ARTIFACT]:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Reemplazar Sección 2 manteniendo Sección 1, 3 y 4 intactas
        pattern = r"(## 2\. Recetario Técnico y Gastronómico Día por Día\n.*?\n)(?=## 3\. Lista de Compras Consolidada \(BOM 3D\))"
        new_content = re.sub(pattern, sec2_text + "\n", content, flags=re.DOTALL)

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Dossier successfully updated: {path}")

if __name__ == "__main__":
    update_dossiers()
