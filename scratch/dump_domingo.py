# -*- coding: utf-8 -*-
import json

d = json.load(open("semana_40_master.json", encoding="utf-8"))
for day in d["days"]:
    if day["day"] == "Domingo":
        print(f"\n==================== {day['day']} ====================")
        for m in day["meals"]:
            print(f"\n--- {m['meal_type']} ---")
            for course in ["starter", "main", "side"]:
                c = m[course]
                ings = [f"{i['name']} ({i['amount']}{i['unit']})" for i in c.get("ingredients", [])]
                print(f"[{course.upper()}] {c.get('title')} | Tech: {c.get('technique')}")
                print(f"  Ings: {', '.join(ings)}")
