import json

with open('semana_40_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

for day in master['days']:
    for meal in day['meals']:
        for c in ['starter', 'main', 'side']:
            course = meal.get(c)
            if course and isinstance(course, dict):
                for ing in course.get('ingredients', []):
                    name = ing.get('name', '')
                    nl = name.lower()
                    if any(k in nl for k in ['caldo claro', 'caldo de ', 'caldo concentrado', 'fondo claro', 'infusi']):
                        amt = ing.get('amount')
                        u = ing.get('unit')
                        d = day['day']
                        m = meal['meal_type']
                        print(f"{d} {m} ({c}): {name} -> {amt} {u}")
