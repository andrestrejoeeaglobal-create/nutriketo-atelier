import re
import math
import pytest
from app.services.inventory_master import consolidate_market_bom

BIOLOGICAL_SPECIES_TOKENS = {
    "pavo", "pollo", "res", "cerdo", "atun", "atún", "salmon", "salmón",
    "robalo", "róbalo", "huachinango", "pato", "conejo", "vaca", "cordero"
}

THERMAL_FORBIDDEN_TOKENS = [
    r"\bcaliente\b", r"\bfr[ií][oa]\b", r"\btibi[oa]\b", r"\bhielo\b", r"\batemperad[oa]\b"
]

UNRESOLVED_LIQUID_PATTERNS = [
    r"^caldo\s+", r"^fondo\s+", r"^infusi[oó]n\s+"
]

def get_species_token(name: str):
    nl = name.lower()
    for s in BIOLOGICAL_SPECIES_TOKENS:
        if re.search(r'\b' + s + r'\b', nl):
            return s
    return None

def test_no_thermal_tokens_in_commercial_bom():
    # Load semana 40 ingredients
    import json
    with open('semana_40_master.json', 'r', encoding='utf-8') as f:
        master = json.load(f)

    all_ings = []
    for day in master.get('days', []):
        for meal in day.get('meals', []):
            for c in ['starter', 'main', 'side']:
                course = meal.get(c)
                if course and isinstance(course, dict):
                    all_ings.extend(course.get('ingredients', []))

    bom_res = consolidate_market_bom(all_ings)
    bom_items = bom_res.get("commercial_bom", bom_res) if isinstance(bom_res, dict) else bom_res

    for item in bom_items:
        name = item.get("name", "").lower()
        for p in THERMAL_FORBIDDEN_TOKENS:
            assert not re.search(p, name), f"Insumo comercial '{name}' contiene adjetivo térmico prohibido ({p})"

def test_no_unresolved_liquids_in_commercial_bom():
    import json
    with open('semana_40_master.json', 'r', encoding='utf-8') as f:
        master = json.load(f)

    all_ings = []
    for day in master.get('days', []):
        for meal in day.get('meals', []):
            for c in ['starter', 'main', 'side']:
                course = meal.get(c)
                if course and isinstance(course, dict):
                    all_ings.extend(course.get('ingredients', []))

    bom_res = consolidate_market_bom(all_ings)
    bom_items = bom_res.get("commercial_bom", bom_res) if isinstance(bom_res, dict) else bom_res

    for item in bom_items:
        name = item.get("name", "").lower()
        unit = item.get("unit", "").lower()
        if unit in ["ml", "l", "litros"]:
            for p in UNRESOLVED_LIQUID_PATTERNS:
                assert not re.search(p, name), f"Líquido no resuelto '{name}' en compras de mercado. Debe desglosarse a insumo en seco o retazo."

def test_herbs_sold_by_weight():
    import json
    with open('semana_40_master.json', 'r', encoding='utf-8') as f:
        master = json.load(f)

    all_ings = []
    for day in master.get('days', []):
        for meal in day.get('meals', []):
            for c in ['starter', 'main', 'side']:
                course = meal.get(c)
                if course and isinstance(course, dict):
                    all_ings.extend(course.get('ingredients', []))

    bom_res = consolidate_market_bom(all_ings)
    bom_items = bom_res.get("commercial_bom", bom_res) if isinstance(bom_res, dict) else bom_res

    for item in bom_items:
        name = item.get("name", "").lower()
        unit = item.get("unit", "").lower()
        if any(h in name for h in ["zacate", "tomillo", "romero", "eneldo", "oregano", "orégano", "menta", "toronjil", "manzanilla", "jamaica"]):
            assert unit in ["g", "kg", "gramos"], f"Hierba/Aromático '{name}' cotizado en unidad prohibida '{unit}'. Debe ser por peso (g)."

def test_biochemical_categorization_integrity():
    import json
    with open('semana_40_master.json', 'r', encoding='utf-8') as f:
        master = json.load(f)

    all_ings = []
    for day in master.get('days', []):
        for meal in day.get('meals', []):
            for c in ['starter', 'main', 'side']:
                course = meal.get(c)
                if course and isinstance(course, dict):
                    all_ings.extend(course.get('ingredients', []))

    bom_res = consolidate_market_bom(all_ings)
    bom_items = bom_res.get("commercial_bom", bom_res) if isinstance(bom_res, dict) else bom_res

    for item in bom_items:
        name = item.get("name", "").lower()
        cat = item.get("category", "")
        if "grenetina" in name or "colágeno" in name or "colageno" in name:
            assert "Lácteo" not in cat and "Lacteo" not in cat and "Grasas" not in cat, f"Grenetina mal clasificada en '{cat}'"
            assert "Bases Hidrocoloides" in cat or "Suplementación" in cat, f"Grenetina debe estar en Bases Hidrocoloides / Suplementación, no en '{cat}'"
        if "ajo" in name and "ajonjol" not in name:
            assert "Especias" in cat or "Aromáticos" in cat or "Condimentos" in cat, f"Ajo debe estar en Especias/Aromáticos, no en '{cat}'"

def test_semantic_no_fuzzy_duplicates():
    import json
    with open('semana_40_master.json', 'r', encoding='utf-8') as f:
        master = json.load(f)

    all_ings = []
    for day in master.get('days', []):
        for meal in day.get('meals', []):
            for c in ['starter', 'main', 'side']:
                course = meal.get(c)
                if course and isinstance(course, dict):
                    all_ings.extend(course.get('ingredients', []))

    bom_res = consolidate_market_bom(all_ings)
    bom_items = bom_res.get("commercial_bom", bom_res) if isinstance(bom_res, dict) else bom_res
    names = [it.get("name") for it in bom_items]

    # Check distinctness
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            n1 = names[i]
            n2 = names[j]
            s1 = get_species_token(n1)
            s2 = get_species_token(n2)

            # SALVAGUARDA A: Si tienen especies biológicas distintas (ej. pavo vs pollo), son inmunes a duplicidad
            if s1 and s2 and s1 != s2:
                continue

            # Si comparten la misma especie o ninguna, verificar que no sean variaciones poéticas
            t1 = set(n1.lower().split())
            t2 = set(n2.lower().split())
            common = t1.intersection(t2)
            if len(common) >= 2 and (t1.issubset(t2) or t2.issubset(t1)):
                pytest.fail(f"Posible duplicado difuso no colapsado en compras: '{n1}' vs '{n2}'")
