import json

with open("semana_41_master.json", "r", encoding="utf-8") as f:
    d = json.load(f)

meals = d['days'][0]['meals']
print("meals type:", type(meals))
if isinstance(meals, list):
    print("meals len:", len(meals))
    print("meal 0 keys:", list(meals[0].keys()))
    print("meal 0 name/type:", meals[0].get("meal_name"), meals[0].get("meal_type"))
