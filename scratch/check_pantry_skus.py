import re

raw_table = """
| **1** | Mantequilla | 1 | 290 | g |
| **2** | Mostaza | 3 | 50 | g |
| **3** | Queso cottage | 3 | 960 | g |
| **4** | Yogur griego | 3 | 960 | g |
| **5** | Queso Philadelphia | 4 | 180 | g |
| **6** | Crema ácida | 1 | 960 | g |
| **7** | Mayonesa | 1 | 1000 | g |
| **8** | Queso manchego | 1 | 1200 | g |
| **9** | Queso de cabra | 1 | 500 | g |
| **10** | Salsa BBQ | 1 | 550 | g |
| **11** | Leche de coco | 1 | 960 | ml |
| **12** | Leche evaporada | 1 | 960 | ml |
| **13** | Leche | 1 | 960 | ml |
| **14** | Salsa cátsup | 2 | 1300 | g |
| **15** | Queso mozzarella | 1 | 105 | g |
| **16** | Nogada | 1 | 960 | ml |
| **17** | Agua mineral | 6 | 1500 | ml |
| **18** | Agua mineral | 1 | 355 | ml |
| **19** | Botella de agua | 120 | 355 | ml |
| **20** | Queso parmesano | 1 | 100 | g |
| **21** | Flat steak | 1 | 940 | g |
| **22** | Flat steak | 1 | 945 | g |
| **23** | Lomo de salmón | 1 | 1385 | g |
| **24** | Carne molida | 1 | 1680 | g |
| **25** | Fajitas de mojarra | 1 | 907 | g |
| **26** | Filete de atún | 1 | 700 | g |
| **27** | Jitomate | 9 | — | piezas |
| **28** | Morrón | 7 | — | piezas |
| **29** | Pechuga de pollo | 3 | — | piezas |
| **30** | Zanahoria | 7 | — | piezas |
| **31** | Flor de calabaza | 1 | — | manojo |
| **32** | Calabaza | 6 | — | piezas |
| **33** | Cebolla | 9 | — | piezas |
| **34** | Lechuga | 3 | — | piezas |
| **35** | Ejotes | — | 500 | g |
| **36** | Tomate | — | 400 | g |
| **37** | Elote | 2 | — | piezas |
| **38** | Aguacate | 13 | — | piezas |
| **39** | Zarzamora | 1 | 500 | g |
| **40** | Champiñón | 1 | 1000 | g |
| **41** | Pulpa de arándano | 4 | 960 | g |
| **42** | Pistaches | 1 | 100 | g |
| **43** | Nuez de la India | 1 | 100 | g |
| **44** | Cacahuate enchilado | 1 | 1200 | g |
| **45** | Semillas y nueces mixtas | 1 | 960 | g |
| **46** | Granola | 1 | 100 | g |
| **47** | Té chai | 1 | 70 | g |
| **48** | Hierbas finas | 1 | 25 | g |
| **49** | Harina de trigo | 1 | 1500 | g |
| **50** | Harina para hot cakes | 1 | 500 | g |
| **51** | Cebolla en polvo | 1 | 50 | g |
| **52** | Sal con ajo | 1 | 100 | g |
| **53** | Canela molida | 3 | 250 | g |
| **54** | Alcaparras | 2 | 100 | g |
| **55** | Extracto de vainilla | 2 | 200 | ml |
| **56** | Microdyn | 2 | 100 | ml |
| **57** | Cerezas | 1 | 260 | g |
| **58** | Tajín | 2 | 100 | g |
| **59** | Miguelito | 1 | 100 | g |
| **60** | Chamoy | 1 | 300 | ml |
| **61** | Bicarbonato de sodio | 1 | 227 | g |
| **62** | Achiote | 1 | 110 | g |
| **63** | Polvo para hornear | 1 | 100 | g |
| **64** | Aceitunas manzanilla | 1 | 175 | g |
| **65** | Chocolate para cobertura | 1 | 165 | g |
| **66** | Concentrado de caldo de pollo en polvo | 1 | 250 | g |
| **67** | Café colombiano | 1 | 100 | g |
| **68** | Vinagre balsámico | 2 | 100 | ml |
| **69** | Jugo Maggi | 1 | 200 | ml |
| **70** | Salsa inglesa | 1 | 200 | ml |
| **71** | Salsa de soya | 1 | 250 | ml |
| **72** | Vinagre de vino tinto | 1 | 250 | ml |
| **73** | Aceite de oliva | 1 | 400 | ml |
| **74** | Flor de Jamaica molida en polvo | 1 | 200 | g |
| **75** | Almendras fileteadas | 1 | 200 | g |
| **76** | Hojas de laurel | 1 | 20 | g |
| **77** | Orégano delgado | 1 | 50 | g |
| **78** | Orégano grueso | 1 | 100 | g |
| **79** | Tomillo | 1 | 20 | g |
| **80** | Pimienta negra | 1 | 50 | g |
| **81** | Comino | 1 | 50 | g |
| **82** | Clavo de olor | 1 | 50 | g |
| **83** | Pimienta molida | 1 | 20 | g |
| **84** | Ajonjolí | 1 | 50 | g |
| **85** | Manzanilla | 1 | 50 | g |
| **86** | Cúrcuma | 1 | 100 | g |
| **87** | Sal marina de grano | 1 | 2000 | g |
| **88** | Sal fina | 1 | 1000 | g |
| **89** | Manteca de cerdo | 1 | 500 | g |
| **90** | Aceite de coco | 1 | 500 | g |
| **91** | Tang | 8 | 13 | g |
| **92** | Atún en agua | 7 | 100 | g |
| **93** | Sardina en salsa de tomate | 4 | 425 | g |
| **94** | Rajas de jalapeño | 2 | 157 | g |
| **95** | Harina Power Cakes | 1 | 1000 | g |
| **96** | Hojuelas de avena | 1 | 100 | g |
| **97** | Maíz palomero | 1 | 100 | g |
| **98** | Lentejas | 1 | 100 | g |
| **99** | Quinoa | 1 | 100 | g |
| **100** | Chile güero | 1 | 840 | g |
| **101** | Palomitas para microondas | 6 | 100 | g |
| **102** | Grenetina | 4 | 28 | g |
| **103** | Saborizante para arroz | 4 | 12 | g |
| **104** | Huevo | — | 105 | piezas |
| **105** | MultiSinergix® | 1 | 300 | g |
| **106** | AminoSinergix® | 1 | 200 | g |
"""

with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

pantry_match = re.search(r"window\.PANTRY_STOCK_INVENTORY\s*=\s*(\{[\s\S]*?\n\s*\});", text)
html_pantry = pantry_match.group(1) if pantry_match else ""

lines = [l.strip() for l in raw_table.strip().split('\n') if l.strip().startswith('|')]
print(f"Table items count: {len(lines)}")
missing = []
for line in lines:
    parts = [p.strip().replace('**', '') for p in line.split('|')[1:-1]]
    num = int(parts[0])
    name = parts[1]
    sku_pattern = f'"item_num":\\s*{num}|"item_num": {num}|item_num: {num}'
    if not re.search(sku_pattern, html_pantry):
        missing.append((num, name))

print(f"Missing SKUs in PANTRY_STOCK_INVENTORY: {len(missing)}")
if missing:
    print("Missing:", missing)
else:
    print("All 106 SKUs are present in PANTRY_STOCK_INVENTORY!")
