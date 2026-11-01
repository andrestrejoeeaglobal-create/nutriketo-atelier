import json
import re
import unicodedata

def strip_accents(s):
    if not s: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()

# Load week 41 ingredients
with open("semana_41_master.json", "r", encoding="utf-8") as f:
    s41 = json.load(f)

week_ingredients = {}
days_data = s41.get("days", [])
for day_val in days_data:
    meals = day_val.get("meals", [])
    for meal in meals:
        for course in ["starter", "main_dish", "dessert", "side_dish", "side", "drink", "main"]:
            c_data = meal.get(course, {})
            if isinstance(c_data, dict):
                for ing in c_data.get("ingredients", []):
                    if isinstance(ing, dict) and "name" in ing:
                        name = ing["name"]
                        if name not in week_ingredients:
                            week_ingredients[name] = ing

print(f"Total Unique Week 41 Recipe Ingredients: {len(week_ingredients)}")

# Also load week 42 if available
try:
    with open("semana_42_master.json", "r", encoding="utf-8") as f:
        s42 = json.load(f)
    for day_val in s42.get("days", []):
        meals = day_val.get("meals", [])
        for meal in meals:
            for course in ["starter", "main_dish", "dessert", "side_dish", "side", "drink", "main"]:
                c_data = meal.get(course, {})
                if isinstance(c_data, dict):
                    for ing in c_data.get("ingredients", []):
                        if isinstance(ing, dict) and "name" in ing:
                            name = ing["name"]
                            if name not in week_ingredients:
                                week_ingredients[name] = ing
    print(f"Total Unique W41+W42 Recipe Ingredients: {len(week_ingredients)}")
except Exception as e:
    print("W42 not loaded:", e)

# 106 physical inventory items
pantry_106 = [
    "Mantequilla", "Mostaza", "Queso cottage", "Yogur griego", "Queso Philadelphia",
    "Crema ácida", "Mayonesa", "Queso manchego", "Queso de cabra", "Salsa BBQ",
    "Leche de coco", "Leche evaporada", "Leche", "Salsa cátsup", "Queso mozzarella",
    "Nogada", "Agua mineral", "Botella de agua", "Queso parmesano",
    "Flat steak", "Lomo de salmón", "Carne molida", "Fajitas de mojarra", "Filete de atún",
    "Jitomate", "Morrón", "Pechuga de pollo", "Zanahoria", "Flor de calabaza",
    "Calabaza", "Cebolla", "Lechuga", "Ejotes", "Tomate", "Elote", "Aguacate",
    "Zarzamora", "Champiñón", "Pulpa de arándano", "Pistaches", "Nuez de la India",
    "Cacahuate enchilado", "Semillas y nueces mixtas", "Granola", "Té chai",
    "Hierbas finas", "Harina de trigo", "Harina para hot cakes", "Cebolla en polvo",
    "Sal con ajo", "Canela molida", "Alcaparras", "Extracto de vainilla", "Microdyn",
    "Cerezas", "Tajín", "Miguelito", "Chamoy", "Bicarbonato de sodio", "Achiote",
    "Polvo para hornear", "Aceitunas manzanilla", "Chocolate para cobertura",
    "Concentrado de caldo de pollo en polvo", "Café colombiano", "Vinagre balsámico",
    "Jugo Maggi", "Salsa inglesa", "Salsa de soya", "Vinagre de vino tinto",
    "Aceite de oliva", "Flor de Jamaica molida en polvo", "Almendras fileteadas",
    "Hojas de laurel", "Orégano delgado", "Orégano grueso", "Tomillo",
    "Pimienta negra", "Comino", "Clavo de olor", "Pimienta molida", "Ajonjolí",
    "Manzanilla", "Cúrcuma", "Sal marina de grano", "Sal fina", "Manteca de cerdo",
    "Aceite de coco", "Tang", "Atún en agua", "Sardina en salsa de tomate",
    "Rajas de jalapeño", "Harina Power Cakes", "Hojuelas de avena", "Maíz palomero",
    "Lentejas", "Quinoa", "Chile güero", "Palomitas para microondas", "Grenetina",
    "Saborizante para arroz", "Huevo", "MultiSinergix", "AminoSinergix"
]

with open("scratch/all_recipe_ingredients.txt", "w", encoding="utf-8") as f:
    for name in sorted(week_ingredients.keys()):
        ing = week_ingredients[name]
        f.write(f"{name} | unit: {ing.get('unit')} | cat: {ing.get('category')}\n")

print("Wrote scratch/all_recipe_ingredients.txt")
