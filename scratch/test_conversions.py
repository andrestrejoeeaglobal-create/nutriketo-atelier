import re

def get_piece_gram_weight(name):
    n = name.lower()
    if 'morron' in n or 'pimiento' in n: return 160
    if 'pechuga' in n or 'pollo' in n: return 500
    if 'calabacita' in n or 'calabaza' in n: return 180
    if 'flor de calabaza' in n: return 180
    if 'lechuga' in n: return 380
    if 'jitomate' in n or 'tomate saladet' in n: return 120
    if 'cebolla' in n: return 160
    if 'aguacate' in n: return 180
    return 100

# 1. Pimientos morrones
demand_morron = 726 # grams
pantry_morron_pieces = 7
pantry_morron_grams = pantry_morron_pieces * get_piece_gram_weight("Pimientos morrones dulces")
net_morron = max(0, demand_morron - pantry_morron_grams)
print(f"Morron: demand {demand_morron}g, stock {pantry_morron_pieces} pzas ({pantry_morron_grams}g) -> Net: {net_morron}g (Fully covered: {net_morron == 0})")

# 2. Flor de calabaza
demand_flor = 152 # grams
pantry_flor_manojo = 1
pantry_flor_grams = pantry_flor_manojo * get_piece_gram_weight("Flor de calabaza")
net_flor = max(0, demand_flor - pantry_flor_grams)
print(f"Flor de calabaza: demand {demand_flor}g, stock {pantry_flor_manojo} manojo ({pantry_flor_grams}g) -> Net: {net_flor}g (Fully covered: {net_flor == 0})")

# 3. Lechuga Sweet
demand_lechuga = 1100 # grams (1.1 kg)
pantry_lechuga_pieces = 3
pantry_lechuga_grams = pantry_lechuga_pieces * get_piece_gram_weight("Lechuga Sweet")
net_lechuga = max(0, demand_lechuga - pantry_lechuga_grams)
print(f"Lechuga: demand {demand_lechuga}g, stock {pantry_lechuga_pieces} pzas ({pantry_lechuga_grams}g) -> Net: {net_lechuga}g (Fully covered: {net_lechuga == 0})")

# 4. Pechuga de pollo
demand_pollo = 1900 # grams (1.9 kg)
pantry_pollo_pieces = 3
pantry_pollo_grams = pantry_pollo_pieces * get_piece_gram_weight("Pechuga de pollo")
net_pollo = max(0, demand_pollo - pantry_pollo_grams)
print(f"Pechuga pollo: demand {demand_pollo}g, stock {pantry_pollo_pieces} pzas ({pantry_pollo_grams}g) -> Net: {net_pollo}g")

# 5. Agua mineral
unit_str = "6 botellas de 1500 ml"
pkg_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(kg|kilo|kilos|g|gramos?|l|lt|litros?|ml)', unit_str, re.I)
print("Agua mineral pkg_match:", pkg_match.groups() if pkg_match else None)
if pkg_match:
    pkg_size = float(pkg_match.group(1).replace(',', '.'))
    print(f"6 botellas * {pkg_size} ml = {6 * pkg_size} ml")
