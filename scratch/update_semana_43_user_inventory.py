# -*- coding: utf-8 -*-
import json
from app.services.menu_hard_gate_auditor import assert_zero_violations, DEFAULT_PANTRY_STOCK, DEFAULT_FARM_HARVEST

MASTER_43 = "semana_43_master.json"
MASTER_42 = "semana_42_master.json"

with open(MASTER_43, "r", encoding="utf-8") as f:
    w43 = json.load(f)

with open(MASTER_42, "r", encoding="utf-8") as f:
    w42 = json.load(f)

def set_course(meal, role, title, note, technique, coct, steps, ingredients):
    dish = meal.get(role, {})
    dish["title"] = title
    dish["note"] = note
    if technique:
        dish["technique"] = technique
    if coct:
        dish["coct_reasoning"] = coct
    if steps:
        dish["steps"] = steps
    dish["ingredients"] = ingredients
    meal[role] = dish
    if f"{role}_recipe" in meal and isinstance(meal[f"{role}_recipe"], dict):
        meal[f"{role}_recipe"].update(dish)
    if role == "starter":
        meal["starter_name"] = title
    elif role == "main":
        meal["main_dish_name"] = title
    elif role == "side":
        meal["side_dish_name"] = title

days = w43["days"]

# 1. Domingo Cena Main: Espárragos + Semillas Mixtas -> Cebollas Asadas de Alacena Gratinadas al Horno con Queso Ricotta, Queso Parmesano, Romero de la Granja y Nuez Pecana
set_course(
    days[0]["meals"][2],
    "main",
    "Cebollas Asadas de Alacena Gratinadas al Horno con Queso Ricotta, Queso Parmesano, Romero de la Granja y Nuez Pecana",
    "Plato fuerte nocturno vegetariano y circadiano que aprovecha las Cebollas de Alacena, el Queso Ricotta (1,920 g en stock) y el Queso Parmesano (100 g en stock), perfumados con Romero y Nuez pecana recién recolectados de la Granja El Herami ($0 compra).",
    "Asado al horno a 190°C con gratinado lácteo de Ricotta, Parmesano y Romero",
    {
        "thermodynamics": "Asado a 190°C durante 18 minutos para caramelizar lentamente las capas internas de la cebolla sin quemar los azúcares estructurales, fundiendo la cubierta de ricotta y parmesano.",
        "flavor_and_aromatics": "Dulzura suave de la cebolla asada contrastada con el umami salino del Parmesano, las notas balsámicas de pino del romero de la granja y la nuez pecana tostada.",
        "textural_architecture": "Capas tiernas y sedosas de cebolla asada bajo un gratinado cremoso de queso ricotta y el toque crujiente de la nuez pecana.",
        "critical_control_points": "Cortar las cebollas en mitades transversales uniformes; pincelar con aceite de oliva VEVO antes de hornear y añadir la nuez pecana en los últimos 3 minutos."
    },
    [
        "1. Acondicionamiento y Corte en Mitades: Pelar las cebollas blancas de alacena y cortarlas transversalmente en mitades firmes conservando la raíz basal para mantener unidas las capas.",
        "2. Asado Aromático al Romero: Disponer las mitades de cebolla en bandeja de horno, bañar con aceite de oliva extra virgen, sal de mar y las hojas de romero de la granja; hornear a 190°C durante 14 minutos hasta que estén tiernas.",
        "3. Gratinado de Ricotta, Parmesano y Nuez Pecana: Cubrir las cebollas asadas con copos de queso ricotta y queso parmesano rallado; incorporar la nuez pecana troceada de la granja, gratinar 4 minutos adicionales, coronar con cilantro picado y servir caliente."
    ],
    [
        {"name": "Cebolla", "amount": 2.0, "unit": "piezas", "per_guest": 0.3333, "category": "🥬 Verduras, Hortalizas y Frescos"},
        {"name": "Queso ricotta", "amount": 300.0, "unit": "g", "per_guest": 50.0, "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)"},
        {"name": "Queso parmesano", "amount": 90.0, "unit": "g", "per_guest": 15.0, "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)"},
        {"name": "Nuez pecana", "amount": 90.0, "unit": "g", "per_guest": 15.0, "category": "🥑 Grasas, Aceites y Semillas"},
        {"name": "Romero", "amount": 12.0, "unit": "g", "per_guest": 2.0, "category": "🥬 Verduras, Hortalizas y Frescos"},
        {"name": "Cilantro", "amount": 48.0, "unit": "g", "per_guest": 8.0, "category": "🥬 Verduras, Hortalizas y Frescos"},
        {"name": "Aceite de oliva", "amount": 48.0, "unit": "ml", "per_guest": 8.0, "category": "🥑 Grasas, Aceites y Semillas"},
        {"name": "Sal de mar", "amount": 6.0, "unit": "g", "per_guest": 1.0, "category": "🌶️ Chiles, Condimentos e Infusiones"}
    ]
)

# 2. Lunes Desayuno Main: Morrón -> Jitomate de Alacena, Cebolla y Romero de la Granja
set_course(
    days[1]["meals"][0],
    "main",
    "Frittata Rústica de Huevos al Sartén con Jitomate de Alacena, Cebolla, Romero de la Granja y Queso Philadelphia Cremoso",
    "3 huevos enteros por comensal cuajados lentamente al sartén en mantequilla y aceite VEVO con dados de jitomate y cebolla de alacena, perfumados con romero de la Granja El Herami y medallones de queso Philadelphia.",
    "open_skillet_frittata",
    {
        "thermodynamics": "Salteado previo de cebolla y jitomate a 140°C con romero para evaporar agua vegetativa antes de verter el huevo batido y cuajar a 120°C.",
        "flavor_and_aromatics": "Aroma balsámico de romero de la granja y dulzor de cebolla pochada fundidos con la acidez suave del jitomate y la untuosidad láctea del queso Philadelphia.",
        "textural_architecture": "Estructura esponjosa y firme de frittata con vetas cremosas de queso crema fundente.",
        "critical_control_points": "Evaporar el exceso de jugo del jitomate en sartén antes de incorporar los huevos para evitar sinéresis."
    },
    [
        "1. Sofrito Aromático de Alacena y Granja: Picar finamente la cebolla y el jitomate de alacena; saltear en sartén de hierro con la mitad de la mantequilla y las hojitas de romero de la granja durante 3 minutos.",
        "2. Emulsión de Huevos y Cuajado Lento: Batir los 18 huevos con sal de mar; incorporar el resto de la mantequilla al sartén, verter el huevo y cocinar a fuego bajo tapado durante 5 minutos.",
        "3. Coronación Cremosa de Philadelphia: Distribuir dados de queso Philadelphia en la superficie, rociar el aceite de oliva extra virgen en crudo y reposar 1 minuto tapado hasta fundir suavemente."
    ],
    [
        {"category": "🥩 Carnes, Pescados y Proteínas", "name": "Huevo", "per_guest": 3, "amount": 18, "unit": "piezas"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Jitomate", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cebolla", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Romero", "per_guest": 2.0, "amount": 12.0, "unit": "g"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Queso Philadelphia", "per_guest": 35, "amount": 210, "unit": "g"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Mantequilla", "per_guest": 14, "amount": 84, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 6, "amount": 36, "unit": "ml"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6, "unit": "g"}
    ]
)

# 3. Lunes Cena Main: Lechuga 2.0 -> 1.0 piezas
days[1]["meals"][2]["main"]["ingredients"] = [
    {"category": "🥩 Carnes, Pescados y Proteínas", "name": "Atún en agua", "per_guest": 115, "amount": 690, "unit": "g"},
    {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aguacate", "per_guest": 0.5, "amount": 3.0, "unit": "piezas"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Lechuga", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cilantro", "per_guest": 10, "amount": 60, "unit": "g"},
    {"category": "🥑 Grasas, Aceites y Semillas", "name": "Mayonesa", "per_guest": 15, "amount": 90, "unit": "g"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Limones", "per_guest": 12, "amount": 72, "unit": "g"},
    {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6, "unit": "g"}
]

# 4. Martes Desayuno Starter: Frambuesas -> Fresas y Zarzamoras
set_course(
    days[2]["meals"][0],
    "starter",
    "Tazón de Fresas y Zarzamoras con Semillas de Chía y Nuez Pecana de la Granja",
    "Entrada matutina antioxidante de bajo índice glucémico con fresas, zarzamoras, chía orgánica y nuez pecana recién cosechada de la Granja El Herami.",
    "raw_assembly",
    days[2]["meals"][0]["starter"].get("coct_reasoning"),
    [
        "1. Selección en Frío: Higienizar y escurrir las fresas y zarzamoras manteniendo la cadena de frío (4°C); cortar las fresas en cuartos uniformes.",
        "2. Troceado de Nuez Pecana de la Granja: Cascar y trocear las mitades de nuez pecana de la granja para liberar sus aceites esenciales.",
        "3. Montaje Activo: Servir las bayas en cuencos fríos, coronar con la nuez pecana y espolvorear las semillas de chía orgánicas al momento de despachar."
    ],
    [
        {"category": "🍓 Frutas de Bajo Índice Glucémico", "name": "Fresas", "per_guest": 15, "amount": 90, "unit": "g"},
        {"category": "🍓 Frutas de Bajo Índice Glucémico", "name": "Zarzamora", "per_guest": 10, "amount": 60, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Semillas de chía orgánicas", "per_guest": 8, "amount": 48, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Nuez pecana", "per_guest": 15, "amount": 90, "unit": "g"}
    ]
)

# 5. Martes Comida Main: Jitomate 2.0 piezas, Cebolla 1.0 piezas
days[2]["meals"][1]["main"]["ingredients"] = [
    {"category": "🥩 Carnes, Pescados y Proteínas", "name": "Sardinas", "per_guest": 140, "amount": 840, "unit": "g"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Jitomate", "per_guest": 0.3333, "amount": 2.0, "unit": "piezas"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cebolla", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
    {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Mantequilla", "per_guest": 12, "amount": 72, "unit": "g"},
    {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 6, "amount": 36, "unit": "ml"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cilantro", "per_guest": 8, "amount": 48, "unit": "g"},
    {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Pimienta negra", "per_guest": 0.5, "amount": 3.0, "unit": "g"},
    {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1.5, "amount": 9.0, "unit": "g"}
]

# 6. Martes Cena Starter: Lechuga 2.0 -> 1.0 piezas
days[2]["meals"][2]["starter"]["ingredients"] = [
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Lechuga", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cilantro", "per_guest": 8, "amount": 48.0, "unit": "g"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Limones", "per_guest": 10, "amount": 60.0, "unit": "g"},
    {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 6, "amount": 36.0, "unit": "ml"},
    {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6.0, "unit": "g"}
]

# 7. Miércoles Desayuno Main: Morrón -> Anillo de Cebolla Blanca de Alacena con Mantequilla, Cilantro de la Granja y Queso Ricotta
set_course(
    days[3]["meals"][0],
    "main",
    "Huevos al Sartén en Anillo de Cebolla Blanca de Alacena con Mantequilla, Cilantro de la Granja y Queso Ricotta",
    "3 huevos enteros por comensal cocinados a baja temperatura dentro de aros gruesos de cebolla blanca de alacena dorados en mantequilla y coronados con queso ricotta de alacena y cilantro de la Granja El Herami.",
    "ring_pan_sear",
    {
        "thermodynamics": "Sellado de los aros gruesos de cebolla a 135°C en mantequilla para caramelizar su perímetro y contener la clara líquida mientras coagula suavemente a 65°C.",
        "flavor_and_aromatics": "Dulzor natural de los aros de cebolla dorados en mantequilla de pastoreo con la frescura herbácea del cilantro de la granja y la suavidad láctea de la ricotta.",
        "textural_architecture": "Borde tierno-crujiente de cebolla asada, clara sedosa, yema cremosa y copos tibios de queso ricotta.",
        "critical_control_points": "Cortar aros exteriores de cebolla de 1.5 cm de grosor para contener perfectamente los huevos al cascarlos."
    },
    [
        "1. Corte de Aros Estructurales de Cebolla: Pelar la cebolla blanca de alacena y cortar rodajas transversales de 1.5 cm de espesor separando los anillos exteriores más amplios.",
        "2. Dorado en Mantequilla y Encapsulado: Fundir la mantequilla en sartén amplia, dorar los anillos de cebolla 2 minutos por lado y cascar los huevos en su interior.",
        "3. Coronación de Ricotta y Cilantro de la Granja: Sazonar con sal de mar, distribuir el queso ricotta y el cilantro picado de la granja alrededor de las yemas, tapar 2 minutos a fuego mínimo y terminar con aceite de oliva VEVO."
    ],
    [
        {"category": "🥩 Carnes, Pescados y Proteínas", "name": "Huevo", "per_guest": 3, "amount": 18, "unit": "piezas"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cebolla", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Queso ricotta", "per_guest": 30, "amount": 180, "unit": "g"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cilantro", "per_guest": 6, "amount": 36, "unit": "g"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Mantequilla", "per_guest": 14, "amount": 84, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 5, "amount": 30, "unit": "ml"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6, "unit": "g"}
    ]
)

# 8. Miércoles Desayuno Side: Gelatina de Frambuesa -> Gelatina Artesanal de Jamaica de la Granja (4°C) con Fórmula Nootrópica 33Plus®
set_course(
    days[3]["meals"][0],
    "side",
    "Gelatina Artesanal de Jamaica de la Granja (4°C) con Fórmula Nootrópica 33Plus®",
    "Gelatina matutina de colágeno estructurado con infusión rubí de Jamaica y Agua purificada de la Granja El Herami ($0 compra), enriquecida a ≤45°C con MultiSinergix® (33Plus®).",
    "digestive_gelatin",
    {
        "thermodynamics": "Infusión de cálices de Jamaica de la granja a 85°C, hidratación bloom de grenetina en frío y descenso térmico a ≤45°C antes de integrar 33Plus®; gelificación a 4°C.",
        "flavor_and_aromatics": "Acidez floral brillante de las antocianinas de la jamaica de la granja en equilibrio con el perfil botánico de la Fórmula 33Plus®.",
        "textural_architecture": "Gel coloidal rubí traslúcido, firme y refrescante.",
        "critical_control_points": "Colar los cálices de jamaica y verificar temperatura ≤45°C antes de disolver MultiSinergix®."
    },
    [
        "1. Infusión Rubí de Jamaica de la Granja: Infusionar la jamaica cosechada en la Granja El Herami en 420 ml de agua purificada caliente durante 5 minutos y colar.",
        "2. Hidratación Bloom de Grenetina: Hidratar los 42 g de grenetina en los 300 ml restantes de agua purificada fría durante 8 minutos y disolver en la infusión tibia de jamaica.",
        "3. Integración Nootrópica y Cuajado a 4°C: Atemperar a 42°C, incorporar los 30 g de MultiSinergix® (33Plus®), verter en copas de cristal y refrigerar a 4°C por mínimo 3 horas."
    ],
    [
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Jamaica", "per_guest": 5, "amount": 30, "unit": "g"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Grenetina", "per_guest": 7, "amount": 42, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "MultiSinergix®", "per_guest": 5, "amount": 30, "unit": "g"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Agua purificada", "per_guest": 120, "amount": 720, "unit": "ml"}
    ]
)

# 9. Miércoles Comida Side: Cebolla 2.0 -> 1.0 piezas
days[3]["meals"][1]["side"]["ingredients"] = [
    {"name": "Cebolla", "amount": 1.0, "unit": "piezas", "per_guest": 0.1667, "category": "🥬 Verduras, Hortalizas y Frescos"},
    {"name": "Cilantro", "amount": 48.0, "unit": "g", "per_guest": 8.0, "category": "🥬 Verduras, Hortalizas y Frescos"},
    {"name": "Aceite de oliva", "amount": 36.0, "unit": "ml", "per_guest": 6.0, "category": "🥑 Grasas, Aceites y Semillas"},
    {"name": "Limones", "amount": 60.0, "unit": "g", "per_guest": 10.0, "category": "🥬 Verduras, Hortalizas y Frescos"},
    {"name": "Orégano", "amount": 3.0, "unit": "g", "per_guest": 0.5, "category": "🌶️ Chiles, Condimentos e Infusiones"},
    {"name": "Sal de mar", "amount": 6.0, "unit": "g", "per_guest": 1.0, "category": "🌶️ Chiles, Condimentos e Infusiones"}
]

# 10. Miércoles Cena Main: Semillas y nueces mixtas -> Nuez pecana de la Granja
set_course(
    days[3]["meals"][2],
    "main",
    "Medallones de Filete de Atún Sellados en Costra de Nuez Pecana de la Granja con Limón Real y Nopales de la Granja",
    "Filete de atún sellado al sartén en costra aromática de Nuez pecana recién cosechada de la Granja El Herami, montado sobre nopales tiernos de la granja al limón y aceite VEVO.",
    "pan_seared_tataki",
    days[3]["meals"][2]["main"].get("coct_reasoning"),
    [
        "1. Costra de Nuez Pecana de la Granja: Picar finamente la nuez pecana de la granja con sal de mar y presionar sobre los bordes de los medallones de filete de atún.",
        "2. Salteado de Nopales de la Granja: Saltear los nopales en bastones con la mitad de la mantequilla y jugo de limón real hasta que estén tiernos y brillantes.",
        "3. Sellado Rápido de los Medallones: Sellar los medallones de atún en sartén caliente con la mantequilla restante durante 90 segundos por cara, montar sobre los nopales y bañar con aceite de oliva VEVO."
    ],
    [
        {"category": "🥩 Carnes, Pescados y Proteínas", "name": "Filete de atún", "per_guest": 115, "amount": 690.0, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Nuez pecana", "per_guest": 6.0, "amount": 36.0, "unit": "g"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Nopales", "per_guest": 80, "amount": 480.0, "unit": "g"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Mantequilla", "per_guest": 10, "amount": 60.0, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 8, "amount": 48.0, "unit": "ml"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Limones", "per_guest": 12, "amount": 72.0, "unit": "g"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6.0, "unit": "g"}
    ]
)

# 11. Jueves Comida Main: Pechuga de pollo (0g en alacena) -> Pollo entero de Alacena (1 pieza en stock!) + Romero de la Granja
set_course(
    days[4]["meals"][1],
    "main",
    "Supremas de Pollo Entero de Alacena al Horno con Romero de la Granja, Queso Ricotta y Acelgas de la Granja en Emulsión VEVO",
    "Aprovecha al 100% el Pollo entero disponible en Alacena (1 pieza, $0 compra), horneado en su jugo con Romero y Acelgas de la Granja El Herami y gratinado suave de Queso Ricotta de Alacena.",
    "stuffed_supreme_bake",
    {
        "thermodynamics": "Horneado del pollo entero porcionado a 185°C con mantequilla y romero de la granja hasta alcanzar 74°C internos, integrando al final el queso ricotta y las acelgas salteadas.",
        "flavor_and_aromatics": "Jugos naturales del pollo entero de alacena perfumados con los aceites esenciales del romero de la granja y la suavidad láctea de la ricotta.",
        "textural_architecture": "Carne de ave jugosa y tierna con guarnición integrada cremosa de acelgas y queso ricotta.",
        "critical_control_points": "Bañar las piezas con los jugos de cocción y mantequilla de romero a mitad del horneado para máxima jugosidad."
    },
    [
        "1. Porcionado y Adobo al Romero de la Granja: Porcionar el pollo entero de alacena en piezas nobles (supremas, muslos y contramuslos), secar y frotar con sal de mar, mantequilla y romero picado de la granja.",
        "2. Horneado Jugoso: Hornear a 185°C durante 28 minutos bañando con sus propios jugos hasta alcanzar 74°C en el núcleo.",
        "3. Integración de Acelgas y Ricotta: En los últimos 5 minutos, disponer alrededor las acelgas de la granja salteadas y copos de queso ricotta de alacena; terminar en mesa con emulsión de aceite de oliva VEVO."
    ],
    [
        {"category": "🥩 Carnes, Pescados y Proteínas", "name": "Pollo entero", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Queso ricotta", "per_guest": 40, "amount": 240.0, "unit": "g"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Acelgas", "per_guest": 60, "amount": 360.0, "unit": "g"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Romero", "per_guest": 2, "amount": 12.0, "unit": "g"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Mantequilla", "per_guest": 10, "amount": 60.0, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 8, "amount": 48.0, "unit": "ml"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6.0, "unit": "g"}
    ]
)

# 12. Jueves Comida Side: Morrón -> Cebolla Blanca de Alacena Rostizada al Romero de la Granja con Aceite de Oliva VEVO
set_course(
    days[4]["meals"][1],
    "side",
    "Cebolla Blanca de Alacena Rostizada al Romero de la Granja con Aceite de Oliva VEVO",
    "Gajos tiernos de cebolla blanca de alacena rostizados al sartén de hierro con hojas de romero de la Granja El Herami y aceite de oliva extra virgen.",
    "pan_roast_strips",
    {
        "thermodynamics": "Rostizado lento en sartén de hierro a 150°C para suavizar las fibras de la cebolla sin quemar los compuestos volátiles del romero.",
        "flavor_and_aromatics": "Notas dulces de cebolla caramelizada entrelazadas con el perfume herbal del romero de la granja.",
        "textural_architecture": "Gajos carnosos y brillantes con bordes ligeramente dorados.",
        "critical_control_points": "Mantener fuego medio para lograr traslucidez uniforme antes de añadir el aceite de oliva VEVO al cierre."
    },
    [
        "1. Corte en Gajos: Pelar y cortar la cebolla blanca de alacena en gajos longitudinales uniformes.",
        "2. Rostizado al Romero de la Granja: Rostizar los gajos en sartén caliente con las hojitas de romero de la granja durante 5 minutos volteando con pinzas.",
        "3. Emulsión de Cierre: Retirar del fuego, bañar con el aceite de oliva extra virgen y sazonar con sal de mar."
    ],
    [
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cebolla", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Romero", "per_guest": 2.0, "amount": 12.0, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 6, "amount": 36.0, "unit": "ml"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6.0, "unit": "g"}
    ]
)

# 13. Jueves Cena Starter: Jitomate 3.0 -> 1.0 piezas
days[4]["meals"][2]["starter"]["ingredients"] = [
    {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Jitomate", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
    {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 6, "amount": 36, "unit": "ml"},
    {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Orégano", "per_guest": 0.5, "amount": 3.0, "unit": "g"},
    {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6, "unit": "g"},
    {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Agua purificada", "per_guest": 80, "amount": 480, "unit": "ml"}
]

# 14. Jueves Cena Main: Timbal de Queso Cottage (480 g <= 500 g en Alacena!) y Yogur Griego (240 g) con Aguacate Hass, Cilantro y Nuez Pecana de la Granja
set_course(
    days[4]["meals"][2],
    "main",
    "Timbal de Queso Cottage Cremoso y Yogur Griego de Alacena con Aguacate Hass, Cilantro y Nuez Pecana de la Granja",
    "Plato fuerte nocturno ligero y circadiano elaborado con el stock exacto de Queso Cottage (480 g de 500 g en Alacena, $0 compra) y Yogur Griego (3,880 g en Alacena), coronado con Aguacate Hass, Cilantro y Nuez pecana de la Granja El Herami.",
    "chilled_timbale_mold",
    {
        "thermodynamics": "Ensamblaje en frío (6°C–8°C) integrando el queso cottage con yogur griego de alacena para formar una estructura cremosa que sostiene el aguacate y la nuez pecana.",
        "flavor_and_aromatics": "Cremosidad láctea suave del queso cottage y yogur griego realzada por el cilantro de la granja, el aceite VEVO y la nuez pecana tostada.",
        "textural_architecture": "Contraste entre las perlas cremosas del cottage, la untuosidad del aguacate Hass y la crocancia de la nuez pecana.",
        "critical_control_points": "Drenar ligeramente el suero del queso cottage e integrar con el yogur griego justo antes de moldear en aro de acero."
    },
    [
        "1. Emulsión Láctea de Alacena: En un bol frío, integrar los 480 g de queso cottage y 240 g de yogur griego de alacena con el cilantro picado de la granja y sal de mar.",
        "2. Moldeado del Timbal con Aguacate: En aros de emplatar individuales, formar la base de aguacate Hass en dados y cubrir con la mezcla cremosa de queso cottage y yogur griego.",
        "3. Coronación de Nuez Pecana de la Granja: Desmoldar con cuidado, coronar con la nuez pecana troceada de la granja y bañar con aceite de oliva extra virgen."
    ],
    [
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Queso cottage", "per_guest": 80, "amount": 480, "unit": "g"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Yogur griego", "per_guest": 40, "amount": 240, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aguacate", "per_guest": 0.5, "amount": 3.0, "unit": "piezas"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Nuez pecana", "per_guest": 15, "amount": 90, "unit": "g"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cilantro", "per_guest": 8, "amount": 48, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 8, "amount": 48, "unit": "ml"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6, "unit": "g"}
    ]
)

# 15. Viernes Desayuno Starter: Frambuesas -> Zarzamoras con Semillas de Chía, Canela y Nuez Pecana de la Granja
set_course(
    days[5]["meals"][0],
    "starter",
    "Tazón de Zarzamoras con Semillas de Chía, Canela y Nuez Pecana de la Granja",
    "Zarzamoras de bajo índice glucémico servidas en frío con chía orgánica, canela de alacena y nuez pecana de la Granja El Herami.",
    "raw_assembly",
    days[5]["meals"][0]["starter"].get("coct_reasoning"),
    [
        "1. Acondicionamiento en Frío: Seleccionar y secar suavemente las zarzamoras a 4°C.",
        "2. Troceado de Nuez Pecana de la Granja: Partir las nueces pecana de la granja en mitades.",
        "3. Servicio con Chía y Canela: Disponer en cuencos fríos con las semillas de chía orgánicas y un toque aromático de canela molida de alacena."
    ],
    [
        {"category": "🍓 Frutas de Bajo Índice Glucémico", "name": "Zarzamora", "per_guest": 30, "amount": 180, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Semillas de chía orgánicas", "per_guest": 8, "amount": 48, "unit": "g"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Canela molida", "per_guest": 0.5, "amount": 3.0, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Nuez pecana", "per_guest": 15, "amount": 90, "unit": "g"}
    ]
)

# 15b. Viernes Desayuno Main: Omelette Francés Baveuse relleno de Queso Ricotta de Alacena (para no exceder los 500 g de Queso cottage!)
set_course(
    days[5]["meals"][0],
    "main",
    "Omelette Francés Baveuse de 3 Huevos Relleno de Queso Ricotta Cremoso de Alacena y Cilantro de la Granja",
    "3 huevos enteros por comensal batidos y emulsionados en mantequilla de pastoreo con corazón fundente de Queso Ricotta de Alacena (1,920 g en stock) y cilantro de la Granja El Herami.",
    "french_baveuse_omelette",
    {
        "thermodynamics": "Coagulación controlada de proteínas de huevo a 125°C en mantequilla espumosa conservando el centro húmedo baveuse a 64°C al envolver el queso ricotta.",
        "flavor_and_aromatics": "Notas lácteas dulces de mantequilla y queso ricotta de alacena realzadas por los aceites esenciales del cilantro de la granja.",
        "textural_architecture": "Exterior liso y sedoso sin dorado excesivo con interior cremoso de queso ricotta tibio.",
        "critical_control_points": "Retirar del fuego cuando la superficie aún luzca húmeda y enrollar en tercios."
    },
    [
        "1. Emulsión de Huevos: Batir los 18 huevos con sal de mar hasta integrar claras y yemas sin incorporar espuma excesiva.",
        "2. Cocción Baveuse en Mantequilla: Fundir la mantequilla en sartén antiadherente a fuego medio-bajo, verter el huevo y remover continuamente con espátula hasta obtener cuajada cremosa.",
        "3. Relleno de Ricotta y Enrollado: Disponer en el centro el queso ricotta de alacena y el cilantro picado de la granja, doblar en tres pliegues y abrillantar con aceite de oliva VEVO."
    ],
    [
        {"category": "🥩 Carnes, Pescados y Proteínas", "name": "Huevo", "per_guest": 3, "amount": 18.0, "unit": "piezas"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Queso ricotta", "per_guest": 80, "amount": 480.0, "unit": "g"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cilantro", "per_guest": 6, "amount": 36.0, "unit": "g"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Mantequilla", "per_guest": 15, "amount": 90.0, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 5, "amount": 30.0, "unit": "ml"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6.0, "unit": "g"}
    ]
)

# 16. Viernes Comida Main: Morrón -> Cebolla Blanca de Alacena y Romero de la Granja
set_course(
    days[5]["meals"][1],
    "main",
    "Juliana de Flat Steak de Res Salteada al Wok con Cebolla Blanca de Alacena, Romero de la Granja y Aceite VEVO",
    "Tiras jugosas de Flat Steak de res salteadas a fuego vivo en wok con plumas de cebolla blanca de alacena, romero aromático de la Granja El Herami, mantequilla y aceite VEVO.",
    "high_heat_wok_saute",
    {
        "thermodynamics": "Salteado relámpago al wok a 180°C durante 3 minutos para lograr reacción de Maillard externa en las tiras de Flat Steak conservando su centro jugoso.",
        "flavor_and_aromatics": "Notas cárnicas intensas de res al wok perfumadas con romero de la granja, pimienta negra y dulzor de cebolla blanca salteada.",
        "textural_architecture": "Juliana de res tierna acompañada de plumas de cebolla al dente con glaseado brillante de mantequilla y aceite de oliva.",
        "critical_control_points": "Sellar la carne en una sola tanda sin saturar el wok antes de incorporar la cebolla y el romero."
    },
    [
        "1. Corte en Juliana y Plumas: Cortar el Flat Steak en tiras contra la fibra y la cebolla blanca de alacena en plumas gruesas.",
        "2. Salteado al Wok con Romero de la Granja: Calentar el wok a fuego alto, fundir la mantequilla y sellar las tiras de res con las hojitas de romero de la granja durante 2 minutos.",
        "3. Integración de Cebolla y Emulsión VEVO: Añadir las plumas de cebolla, saltear 90 segundos adicionales, sazonar con sal de mar y pimienta negra, y terminar fuera del fuego con aceite de oliva VEVO."
    ],
    [
        {"category": "🥩 Carnes, Pescados y Proteínas", "name": "Flat steak", "per_guest": 150, "amount": 900, "unit": "g"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cebolla", "per_guest": 0.1667, "amount": 1.0, "unit": "piezas"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Romero", "per_guest": 2.0, "amount": 12.0, "unit": "g"},
        {"category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "name": "Mantequilla", "per_guest": 14, "amount": 84, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 8, "amount": 48, "unit": "ml"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1.5, "amount": 9.0, "unit": "g"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Pimienta negra", "per_guest": 0.5, "amount": 3.0, "unit": "g"}
    ]
)

# 17. Viernes Cena Main: Rollitos de Pechuga de Pollo (sin Lechuga para dejar exactamente 3.0 piezas de Lechuga en la semana)
set_course(
    days[5]["meals"][2],
    "main",
    "Rollitos de Pechuga de Pollo al Vapor con Alcaparras, Aceitunas Manzanilla, Cilantro de la Granja, Limón Real y Aceite VEVO",
    "Roulades suaves de pechuga de pollo cocidos al vapor con alcaparras y aceitunas manzanilla de alacena, bañados en emulsión de limón real, cilantro de la Granja El Herami y aceite de oliva VEVO.",
    "steam_roulade",
    {
        "thermodynamics": "Cocción al vapor húmedo a 85°C durante 14 minutos hasta alcanzar 74°C internos sin resecar las fibras magras de la pechuga de pollo.",
        "flavor_and_aromatics": "Contraste mediterráneo entre la salinidad de las alcaparras y aceitunas manzanilla de alacena con el perfume cítrico del limón real y cilantro de la granja.",
        "textural_architecture": "Medallones de pollo tiernos y jugosos con relleno firme de aceitunas y alcaparras bañados en emulsión brillante de aceite VEVO.",
        "critical_control_points": "Enrollar con firmeza las láminas de pechuga y emulsionar en frío el jugo de limón con el aceite de oliva VEVO antes de bañar los medallones."
    },
    [
        "1. Formado de los Rollitos Mediterráneos: Extender las láminas de pechuga de pollo, rellenar con alcaparras, aceitunas manzanilla fileteadas de alacena y cilantro picado de la granja, y enrollar firmemente.",
        "2. Cocción Suave al Vapor: Cocinar al vapor a 85°C durante 14 minutos hasta alcanzar 74°C internos conservando toda su jugosidad.",
        "3. Emulsión Cítrica de Cierre: Cortar en medallones sesgados y bañar con la emulsión de jugo de limón real de la granja, aceite de oliva extra virgen y sal de mar."
    ],
    [
        {"category": "🥩 Carnes, Pescados y Proteínas", "name": "Pechuga de pollo", "per_guest": 150, "amount": 900, "unit": "g"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Alcaparras", "per_guest": 10, "amount": 60, "unit": "g"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Aceitunas manzanilla", "per_guest": 15, "amount": 90, "unit": "g"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Cilantro", "per_guest": 10, "amount": 60, "unit": "g"},
        {"category": "🥑 Grasas, Aceites y Semillas", "name": "Aceite de oliva", "per_guest": 8, "amount": 48, "unit": "ml"},
        {"category": "🥬 Verduras, Hortalizas y Frescos", "name": "Limones", "per_guest": 12, "amount": 72, "unit": "g"},
        {"category": "🌶️ Chiles, Condimentos e Infusiones", "name": "Sal de mar", "per_guest": 1, "amount": 6, "unit": "g"}
    ]
)

# 18. Sábado Cena Main: Semillas y nueces mixtas -> Nuez pecana de la Granja
set_course(
    days[6]["meals"][2],
    "main",
    "Carpaccio Templado de Ejotes Tiernos al Vapor con Queso Ricotta, Mantequilla de Pastoreo y Nuez Pecana Tostada de la Granja",
    "Aprovecha los 500 g de Ejotes y el Queso Ricotta en Alacena, coronados con Nuez pecana recién cosechada de la Granja El Herami ($0 compra).",
    "Cocción al vapor corto y salteado tibio en emulsión de mantequilla y aceite VEVO",
    days[6]["meals"][2]["main"].get("coct_reasoning"),
    [
        "1. Cocción al Vapor Al Dente: Cocer los ejotes de alacena al vapor durante 4 minutos hasta lograr un verde brillante y textura crujiente.",
        "2. Salteado Templado en Mantequilla: Pasar los ejotes por sartén tibia con mantequilla de pastoreo y sal de mar durante 60 segundos.",
        "3. Montaje con Ricotta y Nuez Pecana de la Granja: Disponer en plato extendido tipo carpaccio, distribuir copos de queso ricotta de alacena, coronar con la nuez pecana tostada de la granja y rociar aceite de oliva VEVO."
    ],
    [
        {"name": "Ejotes", "amount": 480.0, "unit": "g", "per_guest": 80.0, "category": "🥬 Verduras, Hortalizas y Frescos"},
        {"name": "Queso ricotta", "amount": 300.0, "unit": "g", "per_guest": 50.0, "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)"},
        {"name": "Nuez pecana", "amount": 90.0, "unit": "g", "per_guest": 15.0, "category": "🥑 Grasas, Aceites y Semillas"},
        {"name": "Mantequilla", "amount": 72.0, "unit": "g", "per_guest": 12.0, "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)"},
        {"name": "Aceite de oliva", "amount": 48.0, "unit": "ml", "per_guest": 8.0, "category": "🥑 Grasas, Aceites y Semillas"},
        {"name": "Sal de mar", "amount": 6.0, "unit": "g", "per_guest": 1.0, "category": "🌶️ Chiles, Condimentos e Infusiones"}
    ]
)

# Sync top-level inventory metadata in semana_43_master.json
w43["selected_harvest"] = DEFAULT_FARM_HARVEST
w43["deleted_farm_items"] = [
    "Zarzamoras", "Frambuesas", "Fresas", "Menta", "Arándanos",
    "Epazote", "Calabacitas", "Coliflor", "Espinacas", "Ejotes",
    "Espárragos", "Arúgula", "Brócoli"
]
w43["deleted_pantry_items"] = [
    "Elote", "Higos", "Nogada", "Zanahoria", "Agua mineral"
]

report = assert_zero_violations(
    w43,
    pantry_stock=DEFAULT_PANTRY_STOCK,
    farm_harvest=DEFAULT_FARM_HARVEST,
    prev_week_data=w42
)

with open(MASTER_43, "w", encoding="utf-8") as f:
    json.dump(w43, f, ensure_ascii=False, indent=2)

print("ZERO VIOLATIONS PASSED:", report["passed"])
print("FARM ITEMS:", len(report["bom_summary"]["farm_harvest_items"]))
for item in report["bom_summary"]["farm_harvest_items"]:
    print("  [GRANJA]", item)
print("PANTRY COVERED ITEMS:", len(report["bom_summary"]["pantry_covered_items"]))
for item in report["bom_summary"]["pantry_covered_items"]:
    print("  [ALACENA 100%]", item)
print("MARKET PURCHASES:", len(report["bom_summary"]["market_purchases"]))
for item in report["bom_summary"]["market_purchases"]:
    print("  [SUPERMERCADO]", item)
