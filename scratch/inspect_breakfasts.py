import sys, os, json
sys.path.insert(0, os.path.abspath('.'))

sys.stdout.reconfigure(encoding='utf-8')
import generate_standalone_html as gsh
from app.services.keto_architect import KetoAIArchitect

s40 = KetoAIArchitect().build_semana_40_plan(6).model_dump()

print("=== CHECKING CANONICAL RECIPE CATALOG FOR BREAKFAST DISHES ===")
for d in s40['days']:
    b_name = d['meals'][0]['main_dish_name']
    recipe = gsh.build_typed_recipe_for_dish(b_name, 'main')
    print(f"\n--- {d['day'].upper()}: {b_name} ---")
    print(f"Technique: {recipe.get('cooking_technique')}")
    print(f"Sensory: {recipe.get('sensory_description')}")
    print("Ingredient Groups:")
    for grp in recipe.get('ingredient_groups', []):
        print(f"  * {grp['category']}:")
        for item in grp.get('items', []):
            print(f"    - {item.get('name')}: {item.get('base_qty_per_person')} {item.get('unit')}/persona")
    print("Steps:")
    for step in recipe.get('steps', []):
        print(f"  - {step}")
