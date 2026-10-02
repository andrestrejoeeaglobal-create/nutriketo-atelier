import json
import re
import math

with open('semana_40_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

# Extract all ingredients
all_ings = []
for day in master.get('days', []):
    for meal in day.get('meals', []):
        for c in ['starter', 'main', 'side']:
            course = meal.get(c)
            if course and isinstance(course, dict):
                all_ings.extend(course.get('ingredients', []))

RAW_PIECE_YIELD_GRAMS = {
    "aguacate_hass_fresco": 150.0,
    "limon_fresco": 30.0,
    "champiñon_portobello": 100.0,
    "lechuga_orejona_cogollo": 9.0  # 9 hojas grandes por cogollo
}

PREP_PATTERNS = [
    r"\s+en\s+l[aá]minas(\s+finas)?",
    r"\s+en\s+cubos(\s+de\s+\d+\s*mm|\s+medianos|\s+finos)?",
    r"\s+en\s+guacamole",
    r"\s+en\s+rodajas",
    r"\s+en\s+abanico",
    r"\s+(finamente\s+)?desmenuzad[oa]s?",
    r"\s+(finamente\s+)?trocead[oa]s?",
    r"\s+(finamente\s+)?rallad[oa]s?(\s+fino)?",
    r"\s+(finamente\s+)?picad[oa]s?(\s+fin[oa])?",
    r"\s+filetead[oa]s?",
    r"\s+tostad[oa]s?(\s+sin\s+sal)?",
    r"\s+crujiente",
    r"\s+asad[oa]s?",
    r"\s+rostizad[oa]s?",
    r"\s+sellad[oa]s?",
    r"\s+blanquead[oa]s?",
    r"\s+al\s+horno",
    r"\s+a\s+la\s+parrilla",
    r"\s+al\s+sart[eé]n",
    r"\s+al\s+vapor",
    r"\s+reci[eé]n\s+exprimido",
    r"\s+en\s+su\s+punto",
    r"\s+en\s+pieza",
    r"\s+en\s+tiras",
    r"\s+en\s+medallones",
    r"\s+en\s+floretes",
    r"\s+en\s+mitades",
    r"\s+en\s+bastones",
    r"\s+para\s+hidrataci[oó]n",
    r"\s+caliente",
    r"\s+tibi[oa]",
    r"\s+fr[ií][oa]",
    r"\s+para\s+infusi[oó]n",
    r"\s+limpia\s+\(sin\s+c[aá]liz\s+amargo\)",
    r"\s+de\s+alta\s+pureza",
    r"\s+\(supremas\)",
    r"\s+deshuesad[oa]",
    r"\s+sin\s+almid[oó]n",
    r"\s+de\s+la\s+granja",
    r"\s+del\s+huerto",
    r"\s+de\s+libre\s+pastoreo",
    r"\s+\(ceboll[ií]n,\s+perejil\s+franc[eé]s\s+y\s+perifollo\)",
    r"\s+\(perejil,\s+tomillo\s+y\s+or[eé]gano\)",
]

def resolve_to_canonical_sku(name: str):
    clean = name.strip()
    for p in PREP_PATTERNS:
        clean = re.sub(p, "", clean, flags=re.IGNORECASE)
    clean = re.sub(r'\s+', ' ', clean).strip()

    nl = clean.lower()

    # Biological and physical identity maps
    if "aguacate" in nl:
        return "Aguacate Hass fresco", "Verduras y Hortalizas Frescas"
    if "jitomate" in nl:
        return "Jitomate bola fresco", "Verduras y Hortalizas Frescas"
    if "lechuga orejona" in nl:
        return "Lechuga orejona viva (cogollo)", "Verduras y Hortalizas Frescas"
    if "apio" in nl:
        return "Apio tierno", "Verduras y Hortalizas Frescas"
    if "calabacita" in nl or "zucchini" in nl or "zoodles" in nl:
        return "Calabacitas verdes tiernas", "Verduras y Hortalizas Frescas"
    if "ejote" in nl:
        return "Ejotes verdes tiernos", "Verduras y Hortalizas Frescas"
    if "espárrago" in nl or "esparrago" in nl:
        return "Espárragos verdes frescos", "Verduras y Hortalizas Frescas"
    if "espinaca" in nl and "baby" in nl:
        return "Espinacas baby tiernas", "Verduras y Hortalizas Frescas"
    if "espinaca" in nl:
        return "Espinacas frescas", "Verduras y Hortalizas Frescas"
    if "arúgula" in nl or "arugula" in nl:
        if "espinaca" in nl:
            return "Arúgula y espinaca baby mixta", "Verduras y Hortalizas Frescas"
        return "Arúgula fresca", "Verduras y Hortalizas Frescas"
    if "coliflor" in nl:
        return "Coliflor fresca", "Verduras y Hortalizas Frescas"
    if "chayote" in nl:
        return "Chayotes tiernos pelados", "Verduras y Hortalizas Frescas"
    if "flor de calabaza" in nl:
        return "Flor de calabaza limpia", "Verduras y Hortalizas Frescas"
    if "nopal" in nl:
        return "Nopales tiernos", "Verduras y Hortalizas Frescas"
    if "pepino" in nl:
        return "Pepino fresco", "Verduras y Hortalizas Frescas"
    if "portobello" in nl or "champiñ" in nl or "champin" in nl:
        return "Champiñones Portobello frescos", "Verduras y Hortalizas Frescas"
    if "hinojo" in nl:
        if "bulbo" in nl:
            return "Bulbo de hinojo fresco", "Verduras y Hortalizas Frescas"
        return "Semillas y hojas de hinojo fresco", "Especias, Hierbas y Aromáticos"

    # Aromatics, Herbs, Spices
    if "ajo" in nl and "ajonjol" not in nl:
        return "Ajo fresco", "Especias, Hierbas y Aromáticos"
    if "tomillo" in nl:
        return "Tomillo fresco", "Especias, Hierbas y Aromáticos"
    if "romero" in nl:
        return "Romero fresco", "Especias, Hierbas y Aromáticos"
    if "eneldo" in nl:
        return "Eneldo fresco", "Especias, Hierbas y Aromáticos"
    if "epazote" in nl:
        return "Epazote fresco", "Especias, Hierbas y Aromáticos"
    if "orégano" in nl or "oregano" in nl:
        return "Orégano silvestre seco", "Especias, Hierbas y Aromáticos"
    if "menta" in nl:
        return "Hojas de menta fresca", "Especias, Hierbas y Aromáticos"
    if "toronjil" in nl:
        return "Hojas de toronjil fresco", "Especias, Hierbas y Aromáticos"
    if "cilantro" in nl:
        return "Cilantro fresco", "Especias, Hierbas y Aromáticos"
    if "cebollín" in nl or "cebollin" in nl:
        return "Cebollín fresco", "Especias, Hierbas y Aromáticos"
    if "finas hierbas" in nl:
        return "Finas hierbas frescas", "Especias, Hierbas y Aromáticos"
    if "curry" in nl:
        return "Curry aromático suave en polvo", "Especias, Hierbas y Aromáticos"
    if "cúrcuma" in nl or "curcuma" in nl:
        return "Cúrcuma orgánica en polvo", "Especias, Hierbas y Aromáticos"
    if "manzanilla" in nl:
        return "Flores de manzanilla deshidratadas", "Especias, Hierbas y Aromáticos"
    if "zacate" in nl or "lemongrass" in nl:
        return "Zacate limón deshidratado", "Especias, Hierbas y Aromáticos"
    if "sal de mar" in nl or "sal mineral" in nl:
        return "Sal de mar mineral de Colima", "Especias, Hierbas y Aromáticos"
    if "jamaica" in nl:
        return "Flores de jamaica orgánica deshidratada", "Especias, Hierbas y Aromáticos"

    # Citrus and acids
    if "limón" in nl or "limon" in nl:
        return "Limones frescos", "Cítricos y Ácidos Naturales"
    if "vinagre" in nl:
        return "Vinagre de manzana orgánico", "Cítricos y Ácidos Naturales"

    # Keto Fruits
    if "mora" in nl and "zarzamora" not in nl:
        return "Moras frescas", "Frutas Cetogénicas"
    if "frambuesa" in nl:
        return "Frambuesas frescas orgánicas", "Frutas Cetogénicas"
    if "arándano" in nl or "arandano" in nl:
        return "Arándanos frescos", "Frutas Cetogénicas"
    if "fresa" in nl:
        return "Fresas frescas", "Frutas Cetogénicas"
    if "zarzamora" in nl:
        return "Zarzamoras frescas", "Frutas Cetogénicas"
    if "pitaya" in nl or "pitahaya" in nl:
        return "Pitaya fresca", "Frutas Cetogénicas"
    if "granada" in nl or "arilos" in nl:
        return "Arilos de granada fresca", "Frutas Cetogénicas"

    # Proteins
    if "huevo" in nl and "claras" not in nl and "yemas" not in nl:
        return "Huevos orgánicos de libre pastoreo", "Huevos y Ovoproductos"
    if "arrachera" in nl:
        return "Arrachera de res magra limpia", "Carnes, Aves y Pescados"
    if "machaca" in nl:
        return "Carne seca machaca artesanal de res", "Carnes, Aves y Pescados"
    if "sirloin" in nl:
        return "Medallones de Sirloin de res magro", "Carnes, Aves y Pescados"
    if "pechuga de pavo" in nl or ("pavo" in nl and "tocino" not in nl):
        return "Pechuga de pavo artesanal", "Carnes, Aves y Pescados"
    if "pechuga de pollo" in nl or ("pollo" in nl and "hueso" not in nl and "retazo" not in nl):
        return "Pechuga de pollo orgánica", "Carnes, Aves y Pescados"
    if "tocino de pavo" in nl:
        return "Tocino de pavo artesanal", "Carnes, Aves y Pescados"
    if any(k in nl for k in ["robalo", "róbalo"]) or "pescado blanco" in nl:
        return "Filete de robalo salvaje fresco de captura", "Carnes, Aves y Pescados"
    if "huachinango" in nl:
        return "Filetes de huachinango fresco con piel", "Carnes, Aves y Pescados"
    if "salmón" in nl or "salmon" in nl:
        return "Lomo de salmón fresco calidad sashimi", "Carnes, Aves y Pescados"
    if "atún" in nl or "atun" in nl:
        return "Medallones de atún fresco calidad sashimi", "Carnes, Aves y Pescados"

    # Dairy and healthy fats
    if "mantequilla clarificada" in nl or "ghee" in nl:
        return "Mantequilla clarificada (Ghee)", "Lácteos y Grasas Saludables"
    if "mantequilla" in nl:
        return "Mantequilla de pastoreo artesanal", "Lácteos y Grasas Saludables"
    if "aceite de oliva" in nl or "vevo" in nl:
        return "Aceite de oliva extra virgen (VEVO)", "Lácteos y Grasas Saludables"
    if "aceite" in nl and ("ajonjol" in nl or "sésamo" in nl or "sesamo" in nl):
        return "Aceite de ajonjolí tostado", "Lácteos y Grasas Saludables"
    if "crema entera" in nl or "crema de rancho" in nl:
        return "Crema entera de rancho sin pasteurizar ultra", "Lácteos y Quesos (Sin Gluten / Keto)"
    if "parmesano" in nl:
        return "Queso Parmesano artesanal", "Lácteos y Quesos (Sin Gluten / Keto)"
    if "gouda" in nl:
        return "Queso Gouda artesanal", "Lácteos y Quesos (Sin Gluten / Keto)"
    if "panela" in nl:
        return "Queso Panela artesanal", "Lácteos y Quesos (Sin Gluten / Keto)"
    if "queso crema" in nl:
        return "Queso crema suave artesanal", "Lácteos y Quesos (Sin Gluten / Keto)"
    if "queso de cabra" in nl or "cabra" in nl:
        return "Queso de cabra artesanal", "Lácteos y Quesos (Sin Gluten / Keto)"

    # Nuts & Seeds
    if "almendra" in nl:
        return "Almendras fileteadas tostadas", "Semillas y Frutos Secos"
    if "sésamo" in nl or "sesamo" in nl or "ajonjolí" in nl or "ajonjoli" in nl:
        return "Semillas de sésamo (ajonjolí)", "Semillas y Frutos Secos"
    if "chía" in nl or "chia" in nl:
        return "Semillas de chía orgánicas", "Semillas y Frutos Secos"
    if "girasol" in nl:
        return "Semillas de girasol sin sal", "Semillas y Frutos Secos"
    if "coco" in nl:
        return "Coco deshidratado sin azúcar", "Semillas y Frutos Secos"
    if "pecana" in nl:
        return "Nuez pecana", "Semillas y Frutos Secos"
    if "castilla" in nl:
        return "Nueces de Castilla", "Semillas y Frutos Secos"

    # Hydrocolloids & Supplements
    if "grenetina" in nl or "colágeno" in nl or "colageno" in nl:
        return "Grenetina natural pura (colágeno hidrolizado)", "Bases Hidrocoloides y Suplementación Celular"
    if "33plus" in nl:
        return "Fórmula Biotecnológica Nootrópica 33Plus®", "Suplementación T.I.L.O."
    if "34plus" in nl:
        return "Fórmula Biotecnológica Reparadora 34Plus®", "Suplementación T.I.L.O."

    return clean, "Abarrotes y Varios"

print("Classifier defined successfully")
