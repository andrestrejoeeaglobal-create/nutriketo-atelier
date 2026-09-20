import json
s = json.load(open('semana_39_master.json', 'r', encoding='utf-8'))
for d in s['days']:
    print(f"=== {d['day']} {d['date_str']} ===")
    for m in d['meals']:
        print(f"  {m['meal_type']}:")
        print(f"    Starter: {m.get('starter_name')}")
        print(f"    Main:    {m.get('main_dish_name')}")
        print(f"    Side:    {m.get('side_dish_name')}")
