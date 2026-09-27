import sys, json

sys.stdout.reconfigure(encoding='utf-8')
with open('semana_40_master.json', 'r', encoding='utf-8') as f:
    s40_master = json.load(f)

print("Semana 40 Master Keys:", list(s40_master.keys()))
if 'summary' in s40_master:
    print("Summary:", s40_master['summary'])

# Calculate actual daily average net carbs from s40_master days:
daily_carbs = []
for d in s40_master.get('days', []):
    day_carbs = sum(m.get('net_carbs_g', 0) for m in d.get('meals', []))
    daily_carbs.append(day_carbs)

print("Daily net carbs per day (S40):", daily_carbs)
avg_net_carbs = sum(daily_carbs) / len(daily_carbs) if daily_carbs else 0
print(f"Average Daily Net Carbs: {avg_net_carbs:.2f} g / día")
