import sys, json, os
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')
from generate_standalone_html import build_typed_recipe_for_dish

s = json.load(open('semana_39_master.json', 'r', encoding='utf-8'))

bad_count = 0
for d in s['days']:
    print(f"\n==================== {d['day']} {d['date_str']} ====================")
    for m in d['meals']:
        courses = [
            ("Starter", m.get('starter_name'), 'starter'),
            ("Main", m.get('main_dish_name'), 'main'),
            ("Side", m.get('side_dish_name'), 'side')
        ]
        for ctype, dname, crole in courses:
            if not dname: continue
            recipe = build_typed_recipe_for_dish(dname, course_type=crole)
            tech = recipe.get('cooking_technique')
            steps = " ".join(recipe.get('steps', []))
            items = [it.get('name') for g in recipe.get('ingredient_groups', []) for it in g.get('items', [])]
            
            # Check for bad patterns
            is_bad = False
            reasons = []
            if "sellar la proteína" in steps.lower() or "180°c" in steps.lower() or "licor/fondo" in steps.lower():
                if any(k in dname.lower() for k in ["aguacate", "pepino", "pitaya", "ceviche", "bastones", "ensalada", "salpicón", "higos"]):
                    is_bad = True
                    reasons.append("180C searing applied to raw/cold/ceviche dish!")
            
            if any("seleccionado" in str(it).lower() for it in items):
                is_bad = True
                reasons.append(f"Generic composite item 'seleccionado' in items: {items}")
                
            status = "❌ FAIL" if is_bad else "✅ OK"
            if is_bad: bad_count += 1
            print(f"{status} [{ctype}] '{dname}' -> Technique: {tech}")
            if is_bad:
                for r in reasons:
                    print(f"   ⚠️ REASON: {r}")
                print(f"   Items: {items}")
                print(f"   Step 1: {recipe.get('steps', [''])[0]}")

print(f"\nTOTAL BAD DISHES: {bad_count}")
