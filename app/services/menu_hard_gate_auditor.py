"""
Motor Universal de Auditoría Hard-Gate (V16.0 — Arquitectura Herami / Atelier T.I.L.O.®)
=========================================================================================
Valida determinísticamente cualquier plan semanal (`week_data`) inspeccionando directamente
los `ingredients[]`, `steps[]`, `title`, `note` y `technique` de las 63 recetas (21 servicios x 3 tiempos)
contra las 8 Reglas Duras Canónicas [R1]–[R8] y reconciliando matemáticamente el BOM Tridimensional.
"""

import json
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple


def _strip_accents(text: str) -> str:
    if not text:
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFD", str(text))
        if unicodedata.category(c) != "Mn"
    ).lower().strip()


# ---------------------------------------------------------------------------
# INVENTARIO CANÓNICO BASE (ALACENA Y GRANJA EL HERAMI)
# ---------------------------------------------------------------------------
DEFAULT_FARM_HARVEST: List[str] = [
    "Nopales",
    "Cilantro",
    "Limones",
    "Nuez pecana",
    "Acelgas",
    "Romero",
    "Agua purificada",
    "Jamaica",
]


DEFAULT_PANTRY_STOCK: Dict[str, Tuple[float, str]] = {
    "Huevo": (206.0, "piezas"),
    "Pollo entero": (1.0, "piezas"),
    "Pechuga de pollo": (0.0, "g"),
    "Pechuga de pavo": (1000.0, "g"),
    "Flat steak": (2200.0, "g"),
    "Carne molida": (1360.0, "g"),
    "Lomo de salmón": (1250.0, "g"),
    "Fajitas de mojarra": (2000.0, "g"),
    "Filete de atún": (0.0, "g"),
    "Atún en agua": (700.0, "g"),
    "Sardinas": (1700.0, "g"),
    "Queso cottage": (500.0, "g"),
    "Yogur griego": (5680.0, "g"),
    "Queso ricotta": (3840.0, "g"),
    "Queso manchego": (1000.0, "g"),
    "Queso Philadelphia": (720.0, "g"),
    "Queso de cabra": (0.0, "g"),
    "Queso mozzarella": (105.0, "g"),
    "Queso parmesano": (100.0, "g"),
    "Crema ácida": (960.0, "g"),
    "Mayonesa": (1000.0, "g"),
    "Leche de coco": (960.0, "ml"),
    "Mantequilla": (1370.0, "g"),
    "Aceite de coco": (2000.0, "g"),
    "Fresas": (0.0, "g"),
    "Zarzamora": (340.0, "g"),
    "Frambuesas": (340.0, "g"),
    "Champiñón": (0.0, "g"),
    "Lechuga": (3.0, "piezas"),
    "Jitomate": (7.0, "piezas"),
    "Morrón": (0.0, "piezas"),
    "Cebolla": (8.0, "piezas"),
    "Flor de calabaza": (0.0, "manojo"),
    "Calabaza": (0.0, "piezas"),
    "Espinacas": (0.0, "g"),
    "Espárragos": (907.0, "g"),
    "Germinado": (500.0, "g"),
    "Ejotes": (500.0, "g"),
    "Tomate": (400.0, "g"),
    "Aguacate": (1.0, "piezas"),
    "Semillas y nueces mixtas": (0.0, "g"),
    "Almendras fileteadas": (0.0, "g"),
    "Pistaches": (100.0, "g"),
    "Nuez de la India": (907.0, "g"),
    "Ajonjolí": (0.0, "g"),
    "Aceite de oliva": (400.0, "ml"),
    "Alcaparras": (200.0, "g"),
    "Aceitunas manzanilla": (175.0, "g"),
    "Sal de mar": (3000.0, "g"),
    "Sal con ajo": (100.0, "g"),
    "Cebolla en polvo": (50.0, "g"),
    "Orégano": (150.0, "g"),
    "Pimienta negra": (70.0, "g"),
    "Canela molida": (750.0, "g"),
    "Cúrcuma": (100.0, "g"),
    "Comino": (50.0, "g"),
    "Clavo de olor": (50.0, "g"),
    "Hojas de laurel": (20.0, "g"),
    "Hierbas finas": (25.0, "g"),
    "Tomillo": (20.0, "g"),
    "Manzanilla": (50.0, "g"),
    "Té chai": (70.0, "g"),
    "Flor de Jamaica molida en polvo": (200.0, "g"),
    "Botella de agua": (150.0, "botellas (355 ml)"),
    "Grenetina": (112.0, "g"),
    "MultiSinergix®": (300.0, "g"),
    "AminoSinergix®": (200.0, "g"),
    "Mostaza": (150.0, "g"),
    "Extracto de vainilla": (400.0, "ml"),
    "Microdyn": (200.0, "ml"),
    "Tajín": (200.0, "g"),
    "Bicarbonato de sodio": (227.0, "g"),
    "Achiote": (110.0, "g"),
    "Polvo para hornear": (100.0, "g"),
    "Salsa inglesa": (200.0, "ml"),
    "Salsa de soya": (250.0, "ml"),
    "Vinagre de vino tinto": (250.0, "ml"),
    "Rajas de jalapeño": (314.0, "g"),
    "Chile güero": (840.0, "g"),
}

# Insumos de cocina libre (0 costo mercado; se preparan internamente) o de compra neta planificada en Mercado
FREE_KITCHEN_STAPLES = {
    "agua purificada",
    "fondo claro de pollo",
    "fondo de res",
    "fondo oscuro de res",
    "caldo claro de pollo",
    "caldo de pollo",
    "caldo de res",
    "caldo concentrado y fondo de res casero",
    "caldo de huesos",
}

KNOWN_MARKET_PURCHASE_ITEMS = {
    "semillas de chia organicas",
    "huevo",
    "pechuga de pollo",
    "flat steak",
    "carne molida",
    "lomo de salmon",
    "fajitas de mojarra",
    "filete de atun",
    "fresas",
    "zarzamora",
    "aguacate",
    "cebolla",
    "jitomate",
    "brocoli",
    "coliflor",
    "calabacitas",
    "calabaza",
    "esparragos",
    "espinacas",
    "champinon",
    "morron",
    "pepino",
    "mantequilla",
    "aceite de oliva",
    "manzanilla",
    "grenetina",
    "multisinergix",
    "aminosinergix",
    "33plus",
    "34plus",
}


FORBIDDEN_INGREDIENT_TOKENS = [
    "cerdo", "puerco", "tocino de cerdo", "jamon de cerdo", "manteca de cerdo", "chicharron",
    "azucar", "miel", "jarabe", "sacarosa", "maltitol", "eritritol", "estevia", "stevia",
    "higo", "durazno", "platano", "mango",
    "frijol", "arroz", "maiz", "trigo", "harina de trigo", "avena", "quinoa", "papa", "lenteja", "garbanzo",
    "chile", "chipotle", "chile serrano", "jalapeno", "habanero", "paprika picante",
    "cafe", "cafe colombiano", "espresso", " descafeinado",
    "concentrado de caldo", "caldo de pollo en polvo",
]

WEEKDAY_NAMES_REGEX = re.compile(
    r"\b(lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo)\b",
    re.IGNORECASE,
)

# Banco Canónico de 4 Ciclos (4 x 21 = 84 Arquetipos Maestros: 28 de Huevo + 56 de Comida/Cena)
CYCLE_ARCHETYPE_BANK: Dict[str, Dict[str, List[str]]] = {
    "A": {  # Semanas 41, 45, 49, 53, 57...
        "breakfast": [
            "huevo_revuelto_mantequilla",
            "huevo_pochado_esparragos",
            "huevo_horno_portobello",
            "huevo_sarten_hierbas",
            "huevo_cocotte_crema",
            "huevo_estrellado_aguacate",
            "huevo_revuelto_flor_calabaza",
        ],
        "lunch_dinner": [
            "salmon_plancha_limon",
            "pollo_limon_finas_hierbas",
            "res_medallones_sirloin",
            "robalo_vapor_hierbas",
            "res_machaca_sarten",
            "pavo_fajitas_salteadas",
            "atun_sellado_costra",
            "mojarra_horno_epazote",
            "res_arrachera_brasas",
            "pollo_rollo_espinaca",
            "salmon_mantequilla_eneldo",
            "pavo_albondigas_caldo",
            "res_ribeye_romero",
            "portobello_gratinado_cabra",
        ],
    },
    "B": {  # Semanas 42, 46, 50, 54, 58...
        "breakfast": [
            "huevo_pochado_aguacate",
            "huevo_tortilla_espanola_keto",
            "huevo_revuelto_salmon",
            "huevo_cazuela_espinaca",
            "huevo_omelette_champinon",
            "huevo_frittata_mediterranea",
            "huevo_revuelto_ejotes",
        ],
        "lunch_dinner": [
            "res_hamburguesa_arrachera",
            "mojarra_fajitas_sarten",
            "pollo_suprema_mostaza",
            "salmon_glaseado_limon",
            "res_cortadillo_sirloin",
            "pavo_medallones_salvia",
            "atun_ensalada_nicoise",
            "sardina_escabeche_tibio",
            "res_bife_plancha",
            "pollo_fajitas_morron",
            "salmon_papillote_hierbas",
            "mojarra_vapor_cilantro",
            "res_albondigas_tomate",
            "cottage_tazon_proteico",
        ],
    },
    "C": {  # Semanas 43, 47, 51, 55, 59...
        "breakfast": [
            "frittata",
            "tamagoyaki",
            "anillo",
            "cilbir",
            "estrellados",
            "cazuela",
            "omelette",
        ],
        "lunch_dinner": [
            "fajitas",
            "albondigas",
            "hamburguesa",
            "carpaccio",
            "timbal",
            "salpicon",
            "barquitas",
            "piezas_pollo_horno",
            "papillote",
            "rollitos",
            "medallones",
            "juliana_wok",
            "corte_parrilla",
            "portobello_relleno",
            "salmon_costra",
            "lomos_horno",
        ],
    },
    "D": {  # Semanas 44, 48, 52, 56, 60...
        "breakfast": [
            "huevo_shakshuka_verde",
            "huevo_benedictino_holandesa",
            "huevo_souffle_gratinado",
            "huevo_al_plato_philadelphia_ricotta",
            "huevo_nube_montado",
            "huevo_roulade_ricotta",
            "huevo_crepa_rellena_acelgas",
        ],
        "lunch_dinner": [
            "salmon_glaseado_mostaza_sarten",
            "pavo_medallones_mantequilla_ajo",
            "res_tagliata_romero",
            "mojarra_veracruzana_sarten",
            "res_kofta_tzatziki",
            "champinon_fondue_manchego_ricotta",
            "sardina_pipian_nuez_india",
            "mojarra_meuniere_limon",
            "res_pastel_horno_manchego",
            "atun_croquetas_ricotta_sarten",
            "salmon_veloute_ricotta_romero",
            "pollo_cacciatora_cazadora",
            "res_involtini_braseado",
            "quenelles_ricotta_cottage_espejo_yogur",
        ],
    },
}

# Diccionario de raíces de arquetipos culinarios [R3] y [R10]
ARCHETYPE_PATTERNS: List[Tuple[str, List[str]]] = [
    # --- Arquetipos Específicos Ciclo D (Semana 44, 48, 52, 56, 60+) ---
    ("huevo_shakshuka_verde", ["shakshuka verde"]),
    ("huevo_benedictino_holandesa", ["estilo benedictino", "benedictino sobre nopal", "benedictinos sobre"]),
    ("huevo_souffle_gratinado", ["souffle dorado de huevos", "souffle de huevos"]),
    ("huevo_al_plato_philadelphia_ricotta", ["huevos al plato", "oeufs sur le plat"]),
    ("huevo_nube_montado", ["huevos nube al horno", "huevos en nube"]),
    ("huevo_roulade_ricotta", ["roulade de huevo", "roulade relleno de huevo"]),
    ("huevo_crepa_rellena_acelgas", ["crepas sin harina de huevo", "crepa gruesa de huevo"]),
    ("salmon_glaseado_mostaza_sarten", ["lomo de salmon glaseado a la mostaza", "salmon glaseado a la mostaza"]),
    ("pavo_medallones_mantequilla_ajo", ["medallones de pechuga de pavo dorados", "medallones de pechuga de pavo"]),
    ("res_tagliata_romero", ["tagliata de flat steak", "tagliata de top sirloin"]),
    ("mojarra_veracruzana_sarten", ["a la veracruzana cetogenica", "mojarra salteadas a la veracruzana"]),
    ("res_kofta_tzatziki", ["koftas arabes", "koftas de carne molida"]),
    ("champinon_fondue_manchego_ricotta", ["en fondue cremoso de queso manchego", "cazuela de champinones salteados al ajillo"]),
    ("sardina_pipian_nuez_india", ["enpipianados cetogenicos en salsa espesa de nuez de la india", "sardina enpipianados"]),
    ("mojarra_meuniere_limon", ["mojarra blanca a la meuniere", "a la meuniere"]),
    ("res_pastel_horno_manchego", ["pastel de carne", "pastel horno de carne molida"]),
    ("atun_croquetas_ricotta_sarten", ["croquetas doradas de lomo de atun", "croquetas doradas de atun"]),
    ("salmon_veloute_ricotta_romero", ["salmon al horno en salsa cremosa de queso ricotta", "salsa cremosa de queso ricotta"]),
    ("pollo_cacciatora_cazadora", ["braseadas a la cazadora", "pollo entero de alacena braseado a la cazadora"]),
    ("res_involtini_braseado", ["rollos involtini de flat steak", "involtini de flat steak"]),
    ("quenelles_ricotta_cottage_espejo_yogur", ["quenelles templadas de queso ricotta", "espejo de yogur griego"]),
    # --- Arquetipos Ciclo C (Semana 43, 47, 51, 55, 59+) y Base ---
    ("fajitas", ["fajita", "fajitas"]),
    ("tamagoyaki", ["tamagoyaki", "rollo tamagoyaki"]),
    ("omelette", ["omelette"]),
    ("frittata", ["frittata"]),
    ("cazuela", ["cazuela", "cocotte", "shakshuka"]),
    ("anillo", ["en anillo", "anillo de"]),
    ("cilbir", ["cilbir", "çılbır", "turcos pochados"]),
    ("estrellados", ["estrellado", "estrellados", "sunny"]),
    ("albondigas", ["albondiga", "albondigas"]),
    ("hamburguesa", ["hamburguesa", "hamburguesas"]),
    ("carpaccio", ["carpaccio"]),
    ("timbal", ["timbal"]),
    ("salpicon", ["salpicon"]),
    ("barquitas", ["barquita", "barquitas", "barcas"]),
    ("piezas_pollo_horno", ["piezas de pollo entero", "suprema", "supremas"]),
    ("papillote", ["papillote"]),
    ("rollitos", ["rollito", "rollitos", "roulade"]),
    ("medallones", ["medallon", "medallones", "tataki"]),
    ("juliana_wok", ["juliana", "wok"]),
    ("corte_parrilla", ["corte de", "a la parrilla"]),
    ("portobello_relleno", ["portobello al horno", "champinones portobello al horno"]),
    ("salmon_costra", ["lomo de salmon", "costra de pistaches"]),
    ("lomos_horno", ["lomos de sardina", "sardina del pacifico"]),
]

# Vegetales secundarios/base monitoreados para [R4] (intra-servicio e intra-día)
VEGETABLE_FAMILIES: Dict[str, List[str]] = {
    "flor_de_calabaza": ["flor de calabaza"],
    "esparragos": ["esparrago", "esparragos"],
    "brocoli": ["brocoli"],
    "coliflor": ["coliflor"],
    "ejotes": ["ejote", "ejotes"],
    "calabacitas": ["calabacita", "calabacitas", "zucchini", "zoodles"],
    "chayote": ["chayote", "chayotes"],
    "nopales": ["nopal", "nopales"],
    "acelgas": ["acelga", "acelgas"],
    "espinacas": ["espinaca", "espinacas"],
    "arugula": ["arugula"],
    "morron": ["morron", "pimiento"],
    "lechuga": ["lechuga"],
    "champinon": ["champinon", "portobello"],
    "pepino": ["pepino", "pepinos"],
}

FRUIT_FAMILIES: Dict[str, List[str]] = {
    "fresas": ["fresa", "fresas"],
    "zarzamora": ["zarzamora", "zarzamoras"],
    "frambuesas": ["frambuesa", "frambuesas"],
    "arandanos": ["arandano", "arandanos"],
    "granada": ["granada", "arilos de granada"],
    "pitaya": ["pitaya", "pitahaya"],
}


def extract_dish_archetype(dish: Dict[str, Any]) -> str:
    title_norm = _strip_accents(dish.get("title") or dish.get("name") or "")
    tech_norm = _strip_accents(dish.get("technique") or dish.get("cooking_technique") or "")
    for arch_key, patterns in ARCHETYPE_PATTERNS:
        for pat in patterns:
            if _strip_accents(pat) in title_norm:
                return arch_key
    return tech_norm or title_norm[:24]


def extract_veg_and_fruit_families(dish: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    vegs = set()
    fruits = set()
    for ing in dish.get("ingredients", []):
        ing_norm = _strip_accents(ing.get("name", ""))
        for v_key, tokens in VEGETABLE_FAMILIES.items():
            if any(tok in ing_norm for tok in tokens):
                vegs.add(v_key)
        for f_key, tokens in FRUIT_FAMILIES.items():
            if any(tok in ing_norm for tok in tokens):
                fruits.add(f_key)
    return sorted(vegs), sorted(fruits)


def classify_main_protein(main_dish: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inspecciona `main_dish['ingredients']` para determinar la proteína principal real,
    su familia biológica y si es circadiana (apta para cena).
    """
    ing_names = [
        _strip_accents(i.get("name", ""))
        for i in main_dish.get("ingredients", [])
        if not any(b in _strip_accents(i.get("name", "")) for b in ("fondo claro", "caldo concentrado", "caldo de"))
    ]
    joined = " | ".join(ing_names)

    if "flat steak" in joined or (re.search(r"\bres\b", joined) and "molida" not in joined):
        return {"key": "flat_steak", "family": "res", "circadian_dinner_ok": False, "is_dense": True}
    if "carne molida" in joined:
        return {"key": "carne_molida", "family": "res", "circadian_dinner_ok": False, "is_dense": True}
    if "salmon" in joined:
        return {"key": "salmon", "family": "pescado_azul", "circadian_dinner_ok": False, "is_dense": True}
    if "sardina" in joined:
        return {"key": "sardinas", "family": "pescado_azul", "circadian_dinner_ok": False, "is_dense": True}
    if "pechuga de pollo" in joined or re.search(r"\bpollo\b", joined):
        return {"key": "pechuga_pollo", "family": "pollo", "circadian_dinner_ok": True, "is_dense": False}
    if re.search(r"\bpavo\b", joined):
        return {"key": "pavo", "family": "pavo", "circadian_dinner_ok": True, "is_dense": False}
    if "mojarra" in joined or "robalo" in joined or "huachinango" in joined or "pescado blanco" in joined:
        return {"key": "mojarra", "family": "pescado_blanco", "circadian_dinner_ok": True, "is_dense": False}
    if "atun en agua" in joined:
        return {"key": "atun_agua", "family": "atun", "circadian_dinner_ok": True, "is_dense": False}
    if "filete de atun" in joined or re.search(r"\batun\b", joined):
        return {"key": "filete_atun", "family": "atun", "circadian_dinner_ok": True, "is_dense": False}
    if "champinon" in joined or "portobello" in joined:
        return {"key": "champinon", "family": "fungica", "circadian_dinner_ok": True, "is_dense": False}
    if "queso cottage" in joined:
        return {"key": "queso_cottage", "family": "lactea_ligera", "circadian_dinner_ok": True, "is_dense": False}
    if "huevo" in joined:
        return {"key": "huevo", "family": "huevo", "circadian_dinner_ok": True, "is_dense": False}

    return {"key": "otra", "family": "otra", "circadian_dinner_ok": True, "is_dense": False}


def is_main_dish_metabolically_dense(main_dish: Dict[str, Any]) -> bool:
    """
    Determina si un plato fuerte es DENSO según sus ingredientes reales:
    - Contiene carne de res (`flat steak`, `carne molida`), pescado azul (`salmón`, `sardinas`),
      o quesos/cremas densas (`queso manchego`, `queso de cabra`, `queso philadelphia`,
      `queso ricotta`, `crema ácida`, `aguacate`).
    """
    for ing in main_dish.get("ingredients", []):
        nm = _strip_accents(ing.get("name", ""))
        if re.search(r"\bres\b", nm) or any(
            k in nm
            for k in [
                "flat steak", "carne molida", "sirloin", "ribeye", "arrachera",
                "salmon", "sardina",
                "queso manchego", "queso de cabra", "queso philadelphia", "queso ricotta",
                "crema acida", "aguacate", "mayonesa"
            ]
        ):
            return True
    return False


def has_heavy_lipid_or_dairy_in_side_or_starter(dish: Dict[str, Any], include_butter: bool = False) -> List[str]:
    """
    Inspecciona `dish['ingredients']` en Entrada o Acompañamiento para detectar
    ingredientes prohibidos cuando el plato fuerte es DENSO ([R2]).
    """
    heavy_found = []
    tokens = [
        "queso", "crema acida", "yogur", "mayonesa", "aguacate",
        "tocino", "manteca"
    ]
    if include_butter:
        tokens.append("mantequilla")
    for ing in dish.get("ingredients", []):
        nm = _strip_accents(ing.get("name", ""))
        if any(k in nm for k in tokens):
            heavy_found.append(ing.get("name", nm))
    return heavy_found


def is_super_dense_beef_dish(main_dish: Dict[str, Any]) -> bool:
    """
    Detecta cortes densos de res a la parrilla o de carne molida con queso/crema/guacamole
    (ej. Corte de Flat Steak a la Parrilla con Mantequilla, Albóndigas en Salsa Cremosa,
    Hamburguesa con Queso Manchego y Guacamole).
    Para estos platos, la Entrada debe ser obligatoriamente Ensalada Verde Fresca (no consomé/crema)
    y ni Entrada ni Guarnición pueden llevar mantequilla ni lácteos ([R2] Regla 2.3).
    """
    title_norm = _strip_accents(main_dish.get("title", ""))
    ings_norm = [_strip_accents(i.get("name", "")) for i in main_dish.get("ingredients", [])]
    joined = " | ".join(ings_norm)
    if "carne molida" in joined or "corte de flat steak" in title_norm or "hamburguesa" in title_norm or "albondiga" in title_norm:
        return True
    return False



def validate_no_fruit_dairy_mix(dish: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """
    [R4.6] validateNoFruitDairyMix:
    Prohíbe mezclar cualquier fruta (fresas, zarzamoras, frambuesas, etc.) con lácteos
    (yogur griego, queso cottage, queso ricotta, crema, queso, leche) en el mismo plato.
    """
    _, fruits_found = extract_veg_and_fruit_families(dish)
    dairy_found: List[str] = []
    for ing in dish.get("ingredients", []):
        nm = _strip_accents(ing.get("name", ""))
        if any(k in nm for k in ["yogur", "cottage", "ricotta", "queso", "crema acida", "leche de vaca"]):
            dairy_found.append(ing.get("name", nm))
    return fruits_found, dairy_found


_JACCARD_CANON_ING_TOKENS: List[Tuple[str, List[str]]] = [
    ("calabacitas", ["calabacita", "zucchini", "zoodles"]),
    ("coliflor", ["coliflor"]),
    ("brocoli", ["brocoli"]),
    ("esparragos", ["esparrago"]),
    ("espinacas", ["espinaca"]),
    ("acelgas", ["acelga"]),
    ("nopales", ["nopal"]),
    ("ejotes", ["ejote"]),
    ("pepino", ["pepino"]),
    ("lechuga", ["lechuga"]),
    ("champinon", ["champinon", "portobello"]),
    ("morron", ["morron", "pimiento"]),
    ("chayote", ["chayote"]),
    ("arugula", ["arugula"]),
    ("apio", ["apio"]),
    ("rabano", ["rabano"]),
    ("jitomate", ["jitomate"]),
    ("tomate", ["tomate verde", "tomate"]),
    ("cebolla", ["cebolla", "cebollin", "puerro"]),
    ("aguacate", ["aguacate"]),
    ("queso_ricotta", ["ricotta"]),
    ("queso_manchego", ["manchego"]),
    ("queso_philadelphia", ["philadelphia"]),
    ("queso_cottage", ["cottage"]),
    ("queso_gouda", ["gouda"]),
    ("queso_panela", ["panela"]),
    ("queso_parmesano", ["parmesano"]),
    ("queso_mozzarella", ["mozzarella"]),
    ("queso_cabra", ["queso de cabra"]),
    ("yogur_griego", ["yogur", "yoghurt"]),
    ("crema_acida", ["crema acida"]),
    ("mayonesa", ["mayonesa"]),
    ("mantequilla", ["mantequilla"]),
    ("leche_coco", ["leche de coco"]),
    ("aceite_coco", ["aceite de coco"]),
    ("nuez_india", ["nuez de la india"]),
    ("nuez_pecana", ["nuez pecana", "nueces pecanas", "nuez de castilla"]),
    ("almendras", ["almendra"]),
    ("pistaches", ["pistache"]),
    ("ajonjoli", ["ajonjoli", "sesamo"]),
    ("aceitunas", ["aceituna"]),
    ("alcaparras", ["alcaparra"]),
    ("mostaza", ["mostaza"]),
    ("germinado", ["germinado"]),
    ("cilantro", ["cilantro"]),
    ("romero", ["romero"]),
    ("tomillo", ["tomillo"]),
    ("oregano", ["oregano"]),
    ("laurel", ["laurel"]),
    ("comino", ["comino"]),
    ("eneldo", ["eneldo"]),
    ("epazote", ["epazote"]),
    ("hierbas_finas", ["hierbas finas", "finas hierbas"]),
]


def compute_dish_structural_dna(dish: Dict[str, Any]) -> Tuple[str, str, str, str]:
    """
    [R10-DNA] Calcula la Huella Física Inmutable de 4 Dimensiones:
    `(proteina_base, metodo_termico, morfologia, familia_salsa_o_cama)`
    inspeccionando `ingredients[]`, `technique`, `title` y `steps[]` (sin confiar en `archetype_id`).
    """
    t = _strip_accents(dish.get("title") or dish.get("name") or "")
    tech = _strip_accents(dish.get("technique") or dish.get("cooking_technique") or "")
    steps_txt = " ".join(_strip_accents(s) for s in (dish.get("steps") or []))
    ings_txt = " ".join(_strip_accents(i.get("name") or "") for i in (dish.get("ingredients") or []))
    full = f"{t} {tech} {ings_txt} {steps_txt}"

    # --- 9 Reglas Físicas Canónicas Anti-Camuflaje ---
    # 1. Huevo + (Acelgas o Espinacas) + cocción al horno / cazuela / florentina
    if "huevo" in ings_txt and ("acelga" in ings_txt or "espinaca" in ings_txt) and any(
        w in f"{t} {tech}" for w in ("horno", "hornead", "cazuela", "florentina", "cocotte")
    ):
        return ("huevo", "horno", "cama_hoja_verde", "cazuela_florentina")
    # 2. Salmón + costra (Nuez / Pistaches / Ajonjolí / Almendra adherida)
    if "salmon" in ings_txt and "costra" in f"{t} {tech} {steps_txt}":
        return ("salmon", "sellado_horno", "costra", "semilla_nuez")
    # 3. Atún + costra o medallón sellado / tataki
    if "atun" in ings_txt and any(w in f"{t} {tech}" for w in ("costra", "medallon", "tataki")):
        return ("atun", "sellado", "costra_tataki", "semilla_nuez")
    # 4. Champiñón + relleno / portobello / gratinado al horno con queso
    if ("champinon" in ings_txt or "portobello" in f"{t} {ings_txt}") and (
        "portobello" in t or "relleno" in t or ("horno" in f"{t} {tech}" and ("ricotta" in ings_txt or "gratinad" in t or "queso" in ings_txt))
    ):
        return ("champinon", "horno", "relleno_gratinado", "queso")
    # 5. Corte de Res (Flat steak / Ribeye / Arrachera) + parrilla / brasas / bife + Mantequilla
    if any(k in ings_txt for k in ("flat steak", "ribeye", "arrachera", "sirloin")) and "molida" not in ings_txt:
        if any(w in f"{t} {tech}" for w in ("parrilla", "brasas", "bife", "corte")) and "mantequilla" in ings_txt and "involtini" not in t:
            return ("res_corte", "parrilla", "mantequilla_hierbas", "corte_bife")
    # 6. Sardinas + horno + Tomate/Jitomate
    if "sardina" in ings_txt and any(w in f"{t} {tech}" for w in ("horno", "hornead")) and ("tomate" in ings_txt or "jitomate" in ings_txt):
        return ("sardina", "horno", "tomate", "lomos_enteros")
    # 7. Queso cottage + Yogur griego + timbal / molde frío
    if "cottage" in ings_txt and "yogur" in ings_txt and ("timbal" in f"{t} {tech}" or "molde" in t):
        return ("lacteo_frio", "ensamblaje", "timbal", "cottage_yogur")
    # 8. Huevo + revuelto / baveuse al sartén (no omelette)
    if "huevo" in ings_txt and ("revuelto" in f"{t} {tech}" or ("baveuse" in f"{t} {tech}" and "omelette" not in t)):
        return ("huevo", "sarten", "revuelto", "cremoso_vegetal")
    # 9. Mojarra + grill/plancha/sartén + ajo + cilantro + limón (mojo)
    if "mojarra" in ings_txt and ("ajo" in full and "cilantro" in full) and any(
        w in f"{t} {tech}" for w in ("grill", "mojo", "plancha")
    ) and not any(w in full for w in ("veracruzana", "meuniere", "aceituna", "alcaparra")):
        return ("mojarra", "plancha", "ajo_cilantro_limon", "mojo")

    # --- Extracción General Determinista de 4 Dimensiones ---
    prot = classify_main_protein(dish)["key"]
    if prot == "otra":
        vegs, fruits = extract_veg_and_fruit_families(dish)
        if vegs:
            prot = f"veg_{vegs[0]}"
        elif fruits:
            prot = f"fruit_{fruits[0]}"
        elif "caldo" in full or "fondo" in full:
            prot = "caldo_base"

    # Dimensión 2: Método Térmico
    t_tech = f"{t} {tech}"
    if any(w in t_tech for w in ("pochad", "escalfad", "poach")):
        metodo = "pochado"
    elif any(w in t_tech for w in ("horno", "hornead", "rostizad", "gratinad", "bake", "roast", "souffle")):
        metodo = "horno"
    elif any(w in t_tech for w in ("vapor", "papillote", "steam")):
        metodo = "vapor_papillote"
    elif any(w in t_tech for w in ("brasead", "cazadora", "cacciatora", "braise", "involtini")):
        metodo = "braseado"
    elif any(w in t_tech for w in ("parrilla", "plancha", "grill", "brasas")):
        metodo = "parrilla_plancha"
    elif "wok" in t_tech:
        metodo = "wok"
    elif any(w in t_tech for w in ("crema", "veloute", "cappuccino", "gazpacho", "emulsified")):
        metodo = "licuado_emulsion"
    elif any(w in t_tech for w in ("consome", "caldo", "sopa", "potaje", "potage", "broth")):
        metodo = "caldo_hervido"
    elif any(w in t_tech for w in ("sarten", "saltead", "dorad", "meuniere", "sellad", "skillet", "sear", "pan")):
        metodo = "sarten"
    else:
        metodo = "frio_ensamblaje"

    # Dimensión 3: Morfología Culinaria
    morf = "estandar"
    for m_key, m_tokens in [
        ("shakshuka", ["shakshuka"]),
        ("benedictino", ["benedictin"]),
        ("souffle", ["souffle"]),
        ("oeufs_plat", ["al plato", "sur le plat"]),
        ("nube_orsini", ["nube", "orsini"]),
        ("roulade", ["roulade"]),
        ("crepa", ["crepa", "crepe"]),
        ("tamagoyaki", ["tamagoyaki"]),
        ("omelette", ["omelette"]),
        ("frittata", ["frittata"]),
        ("anillo", ["anillo"]),
        ("cilbir", ["cilbir"]),
        ("estrellados", ["estrellad"]),
        ("glaseado", ["glasead", "glaze"]),
        ("tagliata", ["tagliata"]),
        ("veracruzana", ["veracruzana"]),
        ("kofta", ["kofta"]),
        ("fondue_cazuela", ["fondue"]),
        ("pipian", ["enpipianad", "pipian"]),
        ("meuniere", ["meuniere"]),
        ("pastel_carne", ["pastel de carne", "meatloaf"]),
        ("croquetas", ["croqueta"]),
        ("veloute_horno", ["salsa cremosa de queso ricotta"]),
        ("cacciatora", ["cazadora", "cacciatora"]),
        ("involtini", ["involtini"]),
        ("quenelles", ["quenelle"]),
        ("albondigas", ["albondiga"]),
        ("hamburguesa", ["hamburguesa"]),
        ("barquitas", ["barquita", "tostada", "taco"]),
        ("salpicon", ["salpicon"]),
        ("juliana_wok", ["juliana"]),
        ("tartar_brunoise", ["tartar", "brunoise"]),
        ("carpaccio", ["carpaccio", "abanico"]),
        ("potaje_trozos", ["potaje", "floretes de coliflor enteros"]),
        ("crema_veloute", ["crema", "veloute", "cappuccino"]),
        ("consome_caldo", ["consome", "caldo", "sopa"]),
        ("ensalada", ["ensalada"]),
        ("bastones", ["bastones"]),
    ]:
        if any(tok in t_tech for tok in m_tokens):
            morf = m_key
            break

    # Dimensión 4: Familia de Salsa o Cama
    cama_tokens = []
    for c_key, c_pats in _JACCARD_CANON_ING_TOKENS:
        if any(p in ings_txt for p in c_pats):
            cama_tokens.append(c_key)
    familia_cama = "+".join(sorted(cama_tokens)[:4]) if cama_tokens else "natural"
    return (prot, metodo, morf, familia_cama)


def compute_dish_jaccard_features(dish: Dict[str, Any]) -> Set[str]:
    """
    [R10-DNA] Extrae el conjunto de características físico-culinarias de un platillo:
    Ingredientes canónicos significativos (excluyendo comodines universales de aderezo/salmuera)
    + tokens del ADN estructural (`metodo_termico` y `morfologia`).
    """
    ings_txt = " | ".join(_strip_accents(i.get("name") or "") for i in (dish.get("ingredients") or []))
    features: Set[str] = set()
    for c_key, c_pats in _JACCARD_CANON_ING_TOKENS:
        if any(p in ings_txt for p in c_pats):
            features.add(f"ing:{c_key}")
    dna = compute_dish_structural_dna(dish)
    features.add(f"metodo:{dna[1]}")
    features.add(f"morfo:{dna[2]}")
    return features


def compute_dish_jaccard_similarity(dish_a: Dict[str, Any], dish_b: Dict[str, Any]) -> float:
    """
    Calcula el índice de similitud de Jaccard [0.0, 1.0] entre dos platillos.
    """
    fa = compute_dish_jaccard_features(dish_a)
    fb = compute_dish_jaccard_features(dish_b)
    if not fa or not fb:
        return 0.0
    union_len = len(fa | fb)
    if union_len == 0:
        return 0.0
    return len(fa & fb) / float(union_len)


def extract_structural_signature(dish: Dict[str, Any]) -> Optional[str]:
    """
    [R10] Wrapper de compatibilidad hacia atrás que retorna la firma si el platillo
    cae en cualquiera de las 9 huellas físicas canónicas de S41-S43 o cremas/caldos repetidos.
    """
    dna = compute_dish_structural_dna(dish)
    t = _strip_accents(dish.get("title") or "")
    ings = " ".join(_strip_accents(i.get("name") or "") for i in dish.get("ingredients", []))
    full = f"{t} {ings}"

    if dna[:3] == ("salmon", "sellado_horno", "costra"):
        return "sig_salmon_costra"
    if dna[:3] == ("champinon", "horno", "relleno_gratinado"):
        return "sig_portobello_relleno_horno"
    if dna[:3] == ("sardina", "horno", "tomate"):
        return "sig_sardina_horno"
    if dna[:3] == ("atun", "sellado", "costra_tataki"):
        return "sig_atun_costra_medallon"
    if dna[:3] == ("res_corte", "parrilla", "mantequilla_hierbas"):
        return "sig_res_parrilla_mantequilla"
    if dna[:3] == ("lacteo_frio", "ensamblaje", "timbal"):
        return "sig_timbal_cottage_yogur"
    if dna[:3] == ("huevo", "horno", "cama_hoja_verde"):
        return "sig_huevo_horno_hojas_verdes"
    if dna[:3] == ("huevo", "sarten", "revuelto"):
        return "sig_huevo_revuelto"
    if dna[:3] == ("mojarra", "plancha", "ajo_cilantro_limon"):
        return "sig_mojarra_ajo_cilantro"
    if "coliflor" in full and ("crema" in t or "veloute" in t):
        return "sig_starter_crema_coliflor"
    if "calabacita" in full and ("juliana" in t or ("caldo" in t and "laurel" in full and "cilantro" in full)):
        return "sig_starter_caldo_calabacitas_laurel"
    return None



def compute_repeat_weight_modifier(
    dish_title: str,
    feedback_ledger: Optional[List[Dict[str, Any]]] = None,
) -> float:
    """
    [R11] Calcula el multiplicador de peso de repetición según el historial en MEAL_FEEDBACK_LEDGER:
      - 1 estrella -> 0.20x (bloqueo / penalización severa)
      - 2 estrellas -> 0.45x
      - 3 estrellas -> 0.75x
      - 4 estrellas -> 1.00x
      - 5 estrellas -> 1.15x (o 1.35x si además tuvo digestión ligera)
      - Digestión pesada -> 0.50x (bloqueo de repetición en la misma estructura)
    """
    if not feedback_ledger or not dish_title:
        return 1.0
    norm_target = _strip_accents(dish_title)
    is_target_reformulated = norm_target.startswith("version digestiva ligera al vapor")
    modifier = 1.0
    for entry in feedback_ledger:
        if not isinstance(entry, dict):
            continue
        entry_dish = _strip_accents(
            str(
                entry.get("main_dish_title")
                or entry.get("dish_name")
                or entry.get("dish")
                or entry.get("dish_title")
                or entry.get("title")
                or ""
            )
        )
        if not entry_dish:
            continue
        is_entry_reformulated = entry_dish.startswith("version digestiva ligera al vapor")
        if is_target_reformulated and not is_entry_reformulated:
            continue
        if entry_dish not in norm_target and norm_target not in entry_dish:
            continue
        rating = int(entry.get("rating_stars", entry.get("rating", entry.get("stars", 4))) or 4)
        digestion = _strip_accents(str(entry.get("digestion_tolerance") or entry.get("digestion") or "ligera"))
        if rating <= 1:
            modifier = min(modifier, 0.20)
        elif rating == 2:
            modifier = min(modifier, 0.45)
        elif rating == 3:
            modifier = min(modifier, 0.75)
        elif rating >= 5:
            modifier = max(modifier, 1.35 if ("ligera" in digestion or "optima" in digestion) else 1.15)
        if "pesada" in digestion:
            modifier = min(modifier, 0.50)
    return round(modifier, 2)


# ---------------------------------------------------------------------------
# AUDITOR UNIVERSAL DE LAS REGLAS DURAS [R1] - [R11]
# ---------------------------------------------------------------------------
def audit_week_plan(
    week_data: Dict[str, Any],
    pantry_stock: Optional[Dict[str, Tuple[float, str]]] = None,
    farm_harvest: Optional[List[str]] = None,
    enforce_pantry_overdraft: bool = True,
    prev_week_data: Optional[Dict[str, Any]] = None,
    feedback_ledger: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Ejecuta la auditoría forense completa [R1]–[R11] sobre `week_data`.
    Si se proporciona `prev_week_data` (Semana W-1 en modo Read-Only), valida también:
      - [R9] Continuidad de frontera Sábado(W-1) -> Domingo(W).
      - [R10] Anti-clonación inter-semanal (cero repetición de plato o combo el mismo día de la semana)
              y unicidad de las 7 guarniciones de comida dentro de la Semana W.
      - [R11] Filtro de MEAL_FEEDBACK_LEDGER (`compute_repeat_weight_modifier`).
    Devuelve un diccionario con `passed` (bool), `violations` (List[str]), y `bom_summary`.
    """
    violations: List[str] = []
    pantry = pantry_stock if pantry_stock is not None else DEFAULT_PANTRY_STOCK
    harvest = farm_harvest if farm_harvest is not None else DEFAULT_FARM_HARVEST

    harvest_norm_set = set()
    for h in harvest:
        hn = _strip_accents(h)
        harvest_norm_set.add(hn)
        harvest_norm_set.add(re.sub(r"\s*\bfresc[oa]s?\b", "", hn).strip())

    pantry_norm_map: Dict[str, Tuple[str, float, str]] = {
        _strip_accents(k): (k, float(v[0]), v[1]) for k, v in pantry.items()
    }

    days = week_data.get("days", [])
    if len(days) != 7:
        violations.append(f"[R1] La semana debe contener exactamente 7 días (encontrados: {len(days)}).")

    weekly_fat_g = 0.0
    weekly_prot_g = 0.0
    weekly_carbs_g = 0.0

    breakfast_archetypes: Dict[str, str] = {}
    lunch_dinner_archetypes: Dict[str, str] = {}
    seen_main_techniques: Dict[str, str] = {}
    seen_main_titles: Dict[str, str] = {}
    seen_lunch_side_titles: Dict[str, str] = {}
    seen_lunch_dinner_starter_titles: Dict[str, str] = {}

    lunch_proteins_by_day: List[Tuple[str, str]] = []
    dinner_proteins_by_day: List[Tuple[str, str]] = []
    lunch_dinner_protein_counts: Dict[str, int] = {}
    weekly_breakfast_gelatinas_count = 0
    weekly_veg_family_counts: Dict[str, int] = {}
    seen_lunch_side_vegs: Dict[str, str] = {}

    bom_totals: Dict[str, Dict[str, Any]] = {}

    for d_idx, day in enumerate(days):
        day_name = day.get("day", f"Día {d_idx + 1}")
        meals = day.get("meals", [])
        if len(meals) != 3:
            violations.append(f"[R1] {day_name}: Debe tener exactamente 3 servicios (encontrados: {len(meals)}).")
            continue

        day_fat = 0.0
        day_prot = 0.0
        day_carbs = 0.0

        day_veg_to_meals: Dict[str, List[str]] = {}
        day_avocado_locations: List[str] = []
        day_lunch_prot_key: Optional[str] = None
        day_dinner_prot_key: Optional[str] = None

        for m_idx, meal in enumerate(meals):
            m_type = meal.get("meal_type", f"Servicio {m_idx + 1}")
            loc_label = f"{day_name} - {m_type}"

            fat_g = float(meal.get("fat_g", 0.0))
            prot_g = float(meal.get("protein_g", 0.0))
            carbs_g = float(meal.get("net_carbs_g", 0.0))

            # [R1] Tope estricto <= 5.0g Carbs Netos por servicio
            if carbs_g > 5.0 or carbs_g <= 0.0:
                violations.append(
                    f"[R1] {loc_label}: net_carbs_g={carbs_g}g viola el umbral estricto (0 < net_carbs <= 5.0g)."
                )

            day_fat += fat_g
            day_prot += prot_g
            day_carbs += carbs_g

            starter = meal.get("starter") or {}
            main = meal.get("main") or {}
            side = meal.get("side") or {}

            # [R7/SPLIT-BRAIN] Prohibición absoluta de desincronización entre nombres de cabecera y objetos de receta
            if "starter_name" in meal and meal.get("starter_name") != starter.get("title"):
                violations.append(
                    f"[R7/SPLIT-BRAIN] {loc_label}: starter_name ('{meal.get('starter_name')}') != starter.title ('{starter.get('title')}')."
                )
            if "main_dish_name" in meal and meal.get("main_dish_name") != main.get("title"):
                violations.append(
                    f"[R7/SPLIT-BRAIN] {loc_label}: main_dish_name ('{meal.get('main_dish_name')}') != main.title ('{main.get('title')}')."
                )
            if "side_dish_name" in meal and meal.get("side_dish_name") != side.get("title"):
                violations.append(
                    f"[R7/SPLIT-BRAIN] {loc_label}: side_dish_name ('{meal.get('side_dish_name')}') != side.title ('{side.get('title')}')."
                )

            for c_role, dish in [("starter", starter), ("main", main), ("side", side)]:
                c_label = f"{loc_label} ({c_role}: '{dish.get('title', '')}')"
                ings = dish.get("ingredients", [])
                steps = dish.get("steps", [])
                if not ings:
                    violations.append(f"[R1] {c_label}: No contiene lista de ingredients[].")
                if not steps:
                    violations.append(f"[R1] {c_label}: No contiene pasos de preparación steps[].")

                # Verificar ingredientes prohibidos en ingredients[] y título
                title_and_ings_text = _strip_accents(dish.get("title", "")) + " " + " ".join(
                    _strip_accents(i.get("name", "")) for i in ings
                )
                for forbidden in FORBIDDEN_INGREDIENT_TOKENS:
                    if _strip_accents(forbidden) in title_and_ings_text:
                        violations.append(
                            f"[R1/R3.4] {c_label}: Detectado insumo prohibido o picante irritante '{forbidden}'."
                        )

                # [R4.6] validateNoFruitDairyMix: prohibido mezclar fruta con lácteos en el mismo plato
                fr_mix, dairy_mix = validate_no_fruit_dairy_mix(dish)
                if fr_mix and dairy_mix:
                    violations.append(
                        f"[R4.6] {c_label}: Violación a validateNoFruitDairyMix — prohibido mezclar fruta ({fr_mix}) con lácteos ({dairy_mix}) en el mismo plato."
                    )

                # [R6] Cero diuréticos en Cena (prohibido usar Flor de Jamaica en la noche)
                if _strip_accents(m_type) == "cena" and "jamaica" in title_and_ings_text:
                    violations.append(
                        f"[R6] {c_label}: Prohibido usar diuréticos ('jamaica') en infusiones o platos de Cena."
                    )

                # [R5] Conteo diario de Aguacate en los 9 tiempos del día
                for ing in ings:
                    ing_nm_norm = _strip_accents(ing.get("name", ""))
                    if "aguacate" in ing_nm_norm:
                        day_avocado_locations.append(c_label)

                    # Acumular BOM
                    raw_name = ing.get("name", "").strip()
                    unit = ing.get("unit", "g").strip()
                    amt = float(ing.get("amount", round(float(ing.get("per_guest", 0.0)) * 6, 2)))
                    b_key = _strip_accents(raw_name)
                    if b_key not in bom_totals:
                        bom_totals[b_key] = {
                            "name": raw_name,
                            "unit": unit,
                            "total": 0.0,
                            "category": ing.get("category", ""),
                        }
                    bom_totals[b_key]["total"] = round(bom_totals[b_key]["total"] + amt, 2)

                # [R7] Cero menciones a días de la semana en notas organolépticas
                note_text = str(dish.get("note", "")) + " " + json.dumps(dish.get("coct_reasoning", {}), ensure_ascii=False)
                m_day = WEEKDAY_NAMES_REGEX.search(note_text)
                if m_day:
                    violations.append(
                        f"[R7] {c_label}: La nota organoléptica menciona un día de la semana ('{m_day.group(0)}')."
                    )

                # [R7] Coherencia bidireccional title <-> ingredients[]
                _check_title_ingredient_coherence(c_label, dish, violations)

            # [R2] Balance de Carga Metabólica (enforceMetabolicLoadBalance)
            m_type_norm = _strip_accents(m_type)
            if m_type_norm in ("comida", "cena") and is_main_dish_metabolically_dense(main):
                super_dense_beef = is_super_dense_beef_dish(main)
                heavy_st = has_heavy_lipid_or_dairy_in_side_or_starter(starter, include_butter=super_dense_beef)
                heavy_sd = has_heavy_lipid_or_dairy_in_side_or_starter(side, include_butter=super_dense_beef)
                if heavy_st:
                    violations.append(
                        f"[R2] {loc_label}: Plato principal DENSO ('{main.get('title')}') con Entrada pesada ({heavy_st})."
                    )
                if heavy_sd:
                    violations.append(
                        f"[R2] {loc_label}: Plato principal DENSO ('{main.get('title')}') con Acompañamiento pesado ({heavy_sd})."
                    )
                if super_dense_beef and "ensalada" not in _strip_accents(starter.get("title", "")):
                    violations.append(
                        f"[R2] {loc_label}: Corte denso de res ('{main.get('title')}') exige obligatoriamente Ensalada Verde en la Entrada (encontrado: '{starter.get('title')}')."
                    )

            # [R3] Unicidad de Arquetipo Culinario y Técnica en Plato Principal
            arch = extract_dish_archetype(main)
            tech = _strip_accents(main.get("technique") or "")
            m_title_norm = _strip_accents(main.get("title") or "")

            if m_title_norm in seen_main_titles:
                violations.append(
                    f"[R3] {loc_label}: Plato principal repetido ('{main.get('title')}') ya usado en {seen_main_titles[m_title_norm]}."
                )
            else:
                seen_main_titles[m_title_norm] = loc_label

            if tech in seen_main_techniques:
                violations.append(
                    f"[R3] {loc_label}: Técnica culinaria '{tech}' repetida (ya usada en {seen_main_techniques[tech]})."
                )
            else:
                seen_main_techniques[tech] = loc_label

            if m_type_norm == "desayuno":
                if arch in breakfast_archetypes:
                    violations.append(
                        f"[R3] {loc_label}: Arquetipo matutino '{arch}' repetido en la semana (ya usado en {breakfast_archetypes[arch]})."
                    )
                else:
                    breakfast_archetypes[arch] = loc_label
            else:
                if arch in lunch_dinner_archetypes:
                    violations.append(
                        f"[R3] {loc_label}: Arquetipo culinario '{arch}' repetido en comidas/cenas (ya usado en {lunch_dinner_archetypes[arch]})."
                    )
                else:
                    lunch_dinner_archetypes[arch] = loc_label

                st_title_norm = _strip_accents(starter.get("title") or "")
                if st_title_norm in seen_lunch_dinner_starter_titles:
                    violations.append(
                        f"[R3] {loc_label}: Entrada de comida/cena repetida en la semana ('{starter.get('title')}') ya usada en {seen_lunch_dinner_starter_titles[st_title_norm]}."
                    )
                else:
                    seen_lunch_dinner_starter_titles[st_title_norm] = loc_label

            # [R4] Cero repetición de vegetal o fruta intra-servicio e intra-día
            st_vegs, st_fruits = extract_veg_and_fruit_families(starter)
            mn_vegs, mn_fruits = extract_veg_and_fruit_families(main)
            sd_vegs, sd_fruits = extract_veg_and_fruit_families(side)

            # Intra-servicio: ningún vegetal ni fruta se repite en 2 tiempos del mismo servicio
            for v in set(st_vegs + mn_vegs + sd_vegs):
                count_in_meal = (1 if v in st_vegs else 0) + (1 if v in mn_vegs else 0) + (1 if v in sd_vegs else 0)
                if count_in_meal > 1:
                    violations.append(
                        f"[R4] {loc_label}: El vegetal '{v}' se repite en múltiples tiempos del mismo servicio."
                    )
                day_veg_to_meals.setdefault(v, []).append(m_type)
                weekly_veg_family_counts[v] = weekly_veg_family_counts.get(v, 0) + count_in_meal

            for fr in set(st_fruits + mn_fruits + sd_fruits):
                count_fr = (1 if fr in st_fruits else 0) + (1 if fr in mn_fruits else 0) + (1 if fr in sd_fruits else 0)
                if count_fr > 1:
                    violations.append(
                        f"[R4] {loc_label}: La fruta '{fr}' se repite en Entrada y Acompañamiento/Gelatina del mismo servicio."
                    )

            # Reglas específicas por tipo de servicio (Desayuno / Comida / Cena)
            if m_type_norm == "desayuno":
                # Exigencia de Nuez pecana de la granja y Semillas de chía en las 7 entradas de desayuno
                starter_ings_norm = {_strip_accents(i.get("name", "")): i for i in starter.get("ingredients", [])}
                if not any("nuez pecana" in k for k in starter_ings_norm):
                    violations.append(
                        f"[R8] {loc_label}: La entrada del desayuno debe incluir obligatoriamente 'Nuez pecana de la granja'."
                    )
                if not any("chia" in k for k in starter_ings_norm):
                    violations.append(
                        f"[R8] {loc_label}: La entrada del desayuno debe incluir obligatoriamente 'Semillas de chía orgánicas'."
                    )

                # 3 huevos enteros por comensal y MultiSinergix en acompañamiento
                main_ings_norm = {_strip_accents(i.get("name", "")): i for i in main.get("ingredients", [])}
                if "huevo" not in main_ings_norm or float(main_ings_norm["huevo"].get("per_guest", 0)) != 3.0:
                    violations.append(
                        f"[R5] {loc_label}: El plato fuerte de desayuno debe contener exactamente 3 huevos enteros por comensal."
                    )
                side_ings_norm = {_strip_accents(i.get("name", "")): i for i in side.get("ingredients", [])}
                if not any("multisinergix" in k or "33plus" in k for k in side_ings_norm):
                    violations.append(
                        f"[R8] {loc_label}: El acompañamiento matutino debe incluir MultiSinergix® (33Plus®)."
                    )
                if any("grenetina" in k for k in side_ings_norm) and "gelatina" in _strip_accents(side.get("title", "")):
                    weekly_breakfast_gelatinas_count += 1
            else:
                prot_info = classify_main_protein(main)
                p_key = prot_info["key"]
                lunch_dinner_protein_counts[p_key] = lunch_dinner_protein_counts.get(p_key, 0) + 1

                if m_type_norm == "comida":
                    day_lunch_prot_key = p_key
                    lunch_proteins_by_day.append((day_name, p_key))
                    side_title_norm = _strip_accents(side.get("title") or "")
                    if side_title_norm in seen_lunch_side_titles:
                        violations.append(
                            f"[R10] {loc_label}: Guarnición de comida repetida en la misma semana ('{side.get('title')}') ya usada en {seen_lunch_side_titles[side_title_norm]}."
                        )
                    else:
                        seen_lunch_side_titles[side_title_norm] = loc_label

                    # [R4-SIDE] Diversidad estricta de las 7 guarniciones de Comida (7/7 vegetales principales distintos)
                    w_lbl_check = _strip_accents(week_data.get("week_name") or week_data.get("week_label") or "")
                    if "semana 44" in w_lbl_check:
                        primary_side_veg = sd_vegs[0] if sd_vegs else ""
                        if not primary_side_veg:
                            violations.append(
                                f"[R4-SIDE] {loc_label}: La guarnición de comida ('{side.get('title')}') no contiene un vegetal principal reconocible."
                            )
                        elif primary_side_veg in seen_lunch_side_vegs:
                            violations.append(
                                f"[R4-SIDE] {loc_label}: El vegetal de guarnición de comida '{primary_side_veg}' ('{side.get('title')}') se repite en la misma semana (ya usado en {seen_lunch_side_vegs[primary_side_veg]}). Se exigen 7/7 vegetales distintos."
                            )
                        else:
                            seen_lunch_side_vegs[primary_side_veg] = loc_label
                elif m_type_norm == "cena":
                    day_dinner_prot_key = p_key
                    dinner_proteins_by_day.append((day_name, p_key))
                    if not prot_info["circadian_dinner_ok"]:
                        violations.append(
                            f"[R6] {loc_label}: Proteína '{p_key}' ({prot_info['family']}) prohibida en Cena por Regla Circadiana."
                        )
                    side_ings_norm = {_strip_accents(i.get("name", "")): i for i in side.get("ingredients", [])}
                    if not any("aminosinergix" in k or "34plus" in k for k in side_ings_norm):
                        violations.append(
                            f"[R8] {loc_label}: El acompañamiento nocturno debe incluir AminoSinergix® (34Plus®)."
                        )

            # [R11] Verificación contra MEAL_FEEDBACK_LEDGER (si aplica)
            if feedback_ledger:
                for c_role, dish in [("starter", starter), ("main", main), ("side", side)]:
                    d_title = dish.get("title", "")
                    mod = compute_repeat_weight_modifier(d_title, feedback_ledger)
                    if mod <= 0.50:
                        violations.append(
                            f"[R11] {loc_label} ({c_role}: '{d_title}'): Platillo penalizado en MEAL_FEEDBACK_LEDGER (modifier={mod}x <= 0.50x por baja calificación o digestión pesada)."
                        )

        # [R4] Intra-día: ningún vegetal secundario/base puede repetirse en dos servicios del mismo día
        for v_key, used_meals in day_veg_to_meals.items():
            if len(used_meals) > 1:
                violations.append(
                    f"[R4] {day_name}: El vegetal '{v_key}' se repite en múltiples servicios del mismo día ({', '.join(used_meals)})."
                )

        # [R5] Unicidad estricta de Aguacate (<= 1 vez por día en los 9 tiempos)
        if len(day_avocado_locations) > 1:
            violations.append(
                f"[R5] {day_name}: Aguacate aparece {len(day_avocado_locations)} veces en el mismo día ({'; '.join(day_avocado_locations)}). Máximo permitido: 1."
            )

        # [R6] Comida y Cena del mismo día no pueden repetir proteína
        if day_lunch_prot_key and day_dinner_prot_key and day_lunch_prot_key == day_dinner_prot_key:
            violations.append(
                f"[R6] {day_name}: Misma proteína principal ('{day_lunch_prot_key}') repetida en Comida y Cena del mismo día."
            )

        # [R1] Proporción energética cetogénica diaria (Grasa 70-78%, Proteína 20-25%, Carbs <= 5%)
        day_kcal = (day_fat * 9.0) + (day_prot * 4.0) + (day_carbs * 4.0)
        if day_kcal > 0:
            f_pct = (day_fat * 9.0 / day_kcal) * 100.0
            p_pct = (day_prot * 4.0 / day_kcal) * 100.0
            c_pct = (day_carbs * 4.0 / day_kcal) * 100.0
            if not (70.0 <= f_pct <= 78.0):
                violations.append(
                    f"[R1] {day_name}: Grasa diaria fuera de banda cetogénica ({f_pct:.1f}%, requerido 70-78%)."
                )
            if not (20.0 <= p_pct <= 25.0):
                violations.append(
                    f"[R1] {day_name}: Proteína diaria fuera de banda cetogénica ({p_pct:.1f}%, requerido 20-25%)."
                )
            if c_pct > 5.0:
                violations.append(
                    f"[R1] {day_name}: Carbohidratos netos diarios fuera de banda ({c_pct:.1f}%, requerido <= 5.0%)."
                )

        weekly_fat_g += day_fat
        weekly_prot_g += day_prot
        weekly_carbs_g += day_carbs

    # [R8] Exigencia de mínimo 5 Gelatinas de Grenetina con 33Plus® por semana en acompañamiento matutino
    if weekly_breakfast_gelatinas_count < 5:
        violations.append(
            f"[R8] El acompañamiento matutino debe incluir mínimo 5 Gelatinas Artesanales de Grenetina con 33Plus® (4°C) por semana (encontradas: {weekly_breakfast_gelatinas_count})."
        )

    # [R4] Tope estricto semanal de Acelgas (<= 2 veces) y Nopales (<= 2 veces)
    if weekly_veg_family_counts.get("acelgas", 0) > 2:
        violations.append(
            f"[R4] Acelgas aparece {weekly_veg_family_counts['acelgas']} veces en la semana (máximo permitido: 2)."
        )
    if weekly_veg_family_counts.get("nopales", 0) > 2:
        violations.append(
            f"[R4] Nopales aparece {weekly_veg_family_counts['nopales']} veces en la semana (máximo permitido: 2)."
        )

    # [R6] Cero repetición de proteína en cenas consecutivas y comidas consecutivas
    for i in range(len(dinner_proteins_by_day) - 1):
        d1, p1 = dinner_proteins_by_day[i]
        d2, p2 = dinner_proteins_by_day[i + 1]
        if p1 == p2:
            violations.append(
                f"[R6] Cenas consecutivas ({d1} y {d2}) repiten la misma proteína principal ('{p1}')."
            )
    for i in range(len(lunch_proteins_by_day) - 1):
        d1, p1 = lunch_proteins_by_day[i]
        d2, p2 = lunch_proteins_by_day[i + 1]
        if p1 == p2:
            violations.append(
                f"[R6] Comidas consecutivas ({d1} y {d2}) repiten el mismo corte proteico ('{p1}')."
            )

    # [R6] Máximo 2 apariciones de cualquier proteína en las 14 comidas/cenas
    for p_key, cnt in lunch_dinner_protein_counts.items():
        if cnt > 2:
            violations.append(
                f"[R6] La proteína '{p_key}' aparece {cnt} veces en las 14 comidas/cenas (máximo permitido: 2)."
            )

    w_label_norm = _strip_accents(week_data.get("week_name") or week_data.get("week_label") or "")
    is_week_44_plus = "semana 43" not in w_label_norm
    is_strict_s44 = "semana 44" in w_label_norm

    # [R9] y [R10] Validaciones Inter-Semanales Hacia Adelante (contra prev_week_data en modo Read-Only)
    if prev_week_data and isinstance(prev_week_data, dict):
        prev_days = prev_week_data.get("days", [])
        if len(prev_days) == 7 and len(days) == 7:
            # [R9] Continuidad de Frontera Sábado(W-1) -> Domingo(W)
            prev_sat_meals = prev_days[6].get("meals", [])
            curr_sun_meals = days[0].get("meals", [])
            if len(prev_sat_meals) == 3 and len(curr_sun_meals) == 3:
                _, prev_b_fruits = extract_veg_and_fruit_families(prev_sat_meals[0].get("starter") or {})
                _, curr_b_fruits = extract_veg_and_fruit_families(curr_sun_meals[0].get("starter") or {})
                shared_b_fruits = set(prev_b_fruits) & set(curr_b_fruits)
                if shared_b_fruits:
                    violations.append(
                        f"[R9] Frontera Sábado(W-1)->Domingo(W) (Desayuno): Repite la misma fruta en entrada ('{', '.join(sorted(shared_b_fruits))}')."
                    )
                prev_b_arch = extract_dish_archetype(prev_sat_meals[0].get("main") or {})
                curr_b_arch = extract_dish_archetype(curr_sun_meals[0].get("main") or {})
                if prev_b_arch == curr_b_arch:
                    violations.append(
                        f"[R9] Frontera Sábado(W-1)->Domingo(W) (Desayuno): Repite el mismo arquetipo matutino ('{curr_b_arch}')."
                    )
                for m_idx, m_label in [(1, "Comida"), (2, "Cena")]:
                    pm_main = prev_sat_meals[m_idx].get("main") or {}
                    cm_main = curr_sun_meals[m_idx].get("main") or {}
                    pp = classify_main_protein(pm_main)
                    cp = classify_main_protein(cm_main)
                    if pp["family"] == cp["family"] or pp["key"] == cp["key"]:
                        violations.append(
                            f"[R9] Frontera Sábado(W-1)->Domingo(W) ({m_label}): Repite la misma proteína/familia proteica en días consecutivos ('{pp['family']}/{pp['key']}' -> '{cp['family']}/{cp['key']}')."
                        )
                    p_arch = extract_dish_archetype(pm_main)
                    c_arch = extract_dish_archetype(cm_main)
                    if p_arch == c_arch:
                        violations.append(
                            f"[R9] Frontera Sábado(W-1)->Domingo(W) ({m_label}): Repite el mismo arquetipo culinario ('{c_arch}')."
                        )

            # [R10] Anti-Clonación Inter-Semanal Global (Disjunción 7x7 contra toda la Semana W-1)
            prev_all_main_titles: Dict[str, str] = {}
            prev_all_main_archs: Dict[str, str] = {}
            prev_all_starter_titles: Dict[str, str] = {}
            for pd_idx in range(7):
                pd_label = prev_days[pd_idx].get("day", f"Día {pd_idx + 1}")
                for pm_idx, pm_label in [(0, "Desayuno"), (1, "Comida"), (2, "Cena")]:
                    p_meals_list = prev_days[pd_idx].get("meals", [])
                    if len(p_meals_list) == 3:
                        pm_obj = p_meals_list[pm_idx]
                        pm_m = pm_obj.get("main") or {}
                        pm_t = _strip_accents(pm_m.get("title") or "")
                        pm_a = extract_dish_archetype(pm_m)
                        pm_s = _strip_accents((pm_obj.get("starter") or {}).get("title") or "")
                        if pm_t:
                            prev_all_main_titles[pm_t] = f"{pd_label} {pm_label}"
                        if pm_a:
                            prev_all_main_archs[pm_a] = f"{pd_label} {pm_label}"
                        if pm_s:
                            prev_all_starter_titles[pm_s] = f"{pd_label} {pm_label}"

            for d_idx in range(7):
                p_meals = prev_days[d_idx].get("meals", [])
                c_meals = days[d_idx].get("meals", [])
                d_label = days[d_idx].get("day", f"Día {d_idx + 1}")
                if len(p_meals) == 3 and len(c_meals) == 3:
                    for m_idx, m_label in [(0, "Desayuno"), (1, "Comida"), (2, "Cena")]:
                        pm = p_meals[m_idx]
                        cm = c_meals[m_idx]
                        pm_main = pm.get("main") or {}
                        cm_main = cm.get("main") or {}
                        pm_title = _strip_accents(pm_main.get("title") or "")
                        cm_title = _strip_accents(cm_main.get("title") or "")
                        pm_arch = extract_dish_archetype(pm_main)
                        cm_arch = extract_dish_archetype(cm_main)
                        pm_st = _strip_accents((pm.get("starter") or {}).get("title") or "")
                        cm_st = _strip_accents((cm.get("starter") or {}).get("title") or "")
                        pm_sd = _strip_accents((pm.get("side") or {}).get("title") or "")
                        cm_sd = _strip_accents((cm.get("side") or {}).get("title") or "")
                        same_main_title = bool(pm_title and pm_title == cm_title)
                        same_arch_on_same_weekday = bool(
                            pm_arch and pm_arch == cm_arch and (is_week_44_plus or pm_st == cm_st or pm_sd == cm_sd)
                        )
                        if same_main_title or same_arch_on_same_weekday:
                            violations.append(
                                f"[R10] Anti-Clonación Inter-Semanal ({d_label} - {m_label}): Repite el mismo plato fuerte o arquetipo ('{cm_main.get('title')}') en el mismo día de la semana que en la semana inmediata anterior."
                            )
                        if pm_st and pm_sd and pm_st == cm_st and pm_sd == cm_sd:
                            violations.append(
                                f"[R10] Anti-Clonación Inter-Semanal ({d_label} - {m_label}): Repite el misma combinación Entrada+Guarnición en el mismo día de la semana que en la semana inmediata anterior."
                            )
                        # Chequeo Global 7x7 contra permutación de días de la semana anterior
                        if cm_title in prev_all_main_titles:
                            violations.append(
                                f"[R10] Permutación Inter-Semanal Prohibida ({d_label} - {m_label}): El plato fuerte '{cm_main.get('title')}' ya se sirvió en {prev_all_main_titles[cm_title]} de la semana anterior."
                            )
                        if is_week_44_plus and cm_arch in prev_all_main_archs:
                            violations.append(
                                f"[R10] Permutación de Arquetipo Prohibida ({d_label} - {m_label}): El arquetipo '{cm_arch}' ya se usó en {prev_all_main_archs[cm_arch]} de la semana anterior."
                            )
                        if cm_st in prev_all_starter_titles:
                            violations.append(
                                f"[R10] Permutación de Entrada Prohibida ({d_label} - {m_label}): La entrada '{(cm.get('starter') or {}).get('title')}' ya se sirvió en {prev_all_starter_titles[cm_st]} de la semana anterior."
                            )

    # [R10-DNA] Bloqueo por Huella Física Inmutable (`compute_dish_structural_dna`) y Similitud de Jaccard (< 0.60)
    # en Ventana Móvil de 4 Semanas ([W-3, W-2, W-1, W])
    if is_strict_s44 and len(days) == 7:
        root_dir = Path(__file__).resolve().parents[2]
        rolling_prev_weeks: List[Tuple[str, Dict[str, Any]]] = []
        for w_num in (41, 42, 43):
            w_path = root_dir / f"semana_{w_num}_master.json"
            if w_path.exists():
                try:
                    rolling_prev_weeks.append((f"S{w_num}", json.loads(w_path.read_text(encoding="utf-8"))))
                except Exception:
                    pass

        for d_idx in range(7):
            d_label = days[d_idx].get("day", f"Día {d_idx + 1}")
            c_meals = days[d_idx].get("meals", [])
            if len(c_meals) == 3:
                for m_idx, m_label in [(0, "Desayuno"), (1, "Comida"), (2, "Cena")]:
                    cm = c_meals[m_idx]
                    c_main = cm.get("main") or {}
                    c_starter = cm.get("starter") or {}
                    sig_main = extract_structural_signature(c_main)
                    if sig_main:
                        violations.append(
                            f"[R10-DNA] Huella Estructural Repetida de S41-S43 ({d_label} - {m_label}): '{c_main.get('title')}' colisiona con huella '{sig_main}'."
                        )
                    sig_starter = extract_structural_signature(c_starter)
                    if sig_starter:
                        violations.append(
                            f"[R10-DNA] Huella Estructural de Entrada Repetida de S41-S43 ({d_label} - {m_label}): '{c_starter.get('title')}' colisiona con huella '{sig_starter}'."
                        )

                    dna_main_c = compute_dish_structural_dna(c_main)
                    dna_st_c = compute_dish_structural_dna(c_starter)

                    for w_tag, pw_data in rolling_prev_weeks:
                        for pd_obj in pw_data.get("days", []):
                            pd_name = pd_obj.get("day", "")
                            for pm_idx, pm_obj in enumerate(pd_obj.get("meals", [])):
                                pm_type = pm_obj.get("meal_type", "")
                                p_main = pm_obj.get("main") or {}
                                dna_main_p = compute_dish_structural_dna(p_main)
                                if dna_main_c == dna_main_p:
                                    violations.append(
                                        f"[R10-DNA] Colisión de ADN Estructural {dna_main_c} en {d_label} {m_label} ('{c_main.get('title')}') contra {w_tag} {pd_name} {pm_type} ('{p_main.get('title')}')."
                                    )
                                elif dna_main_c[0] == dna_main_p[0]:
                                    jac_m = compute_dish_jaccard_similarity(c_main, p_main)
                                    if jac_m >= 0.60:
                                        violations.append(
                                            f"[R10-DNA] Violación de Compuerta Jaccard (J={jac_m:.2f} >= 0.60) en {d_label} {m_label} ('{c_main.get('title')}') contra {w_tag} {pd_name} {pm_type} ('{p_main.get('title')}')."
                                        )

                                if m_idx in (1, 2) and pm_idx in (1, 2):
                                    p_st = pm_obj.get("starter") or {}
                                    dna_st_p = compute_dish_structural_dna(p_st)
                                    if dna_st_c[0] == dna_st_p[0] and dna_st_c[2] != "ensalada":
                                        if dna_st_c == dna_st_p:
                                            violations.append(
                                                f"[R10-DNA] Colisión de ADN Estructural de Entrada {dna_st_c} en {d_label} {m_label} ('{c_starter.get('title')}') contra {w_tag} {pd_name} {pm_type} ('{p_st.get('title')}')."
                                            )
                                        else:
                                            jac_s = compute_dish_jaccard_similarity(c_starter, p_st)
                                            if jac_s >= 0.60:
                                                violations.append(
                                                    f"[R10-DNA] Violación de Compuerta Jaccard en Entrada (J={jac_s:.2f} >= 0.60) en {d_label} {m_label} ('{c_starter.get('title')}') contra {w_tag} {pd_name} {pm_type} ('{p_st.get('title')}')."
                                                )

    # [R12] Compuerta de Invariante Estricta de 126 Huevos Semanales (7 desayunos x 18 huevos; 0 en comida/cena)
    total_weekly_eggs = bom_totals.get("huevo", {}).get("total", 0.0)
    if is_strict_s44 and abs(total_weekly_eggs - 126.0) > 0.01:
        violations.append(
            f"[R12] Invariante semanal de Huevo violada: total={total_weekly_eggs} piezas (debe ser exactamente 126 piezas = 7 desayunos x 18 huevos, con 0 huevos en comidas y cenas)."
        )


    # [R8] Reconciliación matemática exacta del BOM (incluyendo las 4 tomas diarias de Sinergix®)
    # En recetas están incluidas Toma 2 (210g MultiSinergix®) y Toma 3 (210g AminoSinergix®).
    # Sumamos Toma 1 (07:00 = 210g MultiSinergix®) y Toma 4 (22:30 = 210g AminoSinergix®) para el BOM total (420g + 420g).
    for s_key, s_display in [("multisinergix", "MultiSinergix®"), ("aminosinergix", "AminoSinergix®")]:
        matched_bom_key = next((k for k in bom_totals if s_key in k), None)
        if matched_bom_key:
            recipe_qty = bom_totals[matched_bom_key]["total"]
            if abs(recipe_qty - 210.0) > 0.5:
                violations.append(
                    f"[R8] {s_display}: La suma en recetas de los 7 días es {recipe_qty}g (debe ser exactamente 210g = 5g x 6 comensales x 7 días)."
                )
            bom_totals[matched_bom_key]["total_with_protocol_4_tomas"] = round(recipe_qty + 210.0, 2)
        else:
            violations.append(f"[R8] No se encontró {s_display} en los ingredientes de las recetas de la semana.")

    bom_reconciliation = {
        "farm_harvest_items": [],
        "pantry_covered_items": [],
        "market_purchases": [],
    }

    STRICT_NO_OVERDRAFT_S44_PLUS = {
        "flat steak", "carne molida", "lomo de salmon", "fajitas de mojarra",
        "pechuga de pavo", "huevo", "queso ricotta", "queso manchego",
        "yogur griego", "mantequilla", "aceite de coco", "nuez de la india",
        "frambuesas", "zarzamora", "esparragos", "germinado",
    }

    for b_key, info in sorted(bom_totals.items()):
        total_req = info.get("total_with_protocol_4_tomas", info["total"])
        raw_name = info["name"]
        unit = info["unit"]

        if b_key in harvest_norm_set or b_key in FREE_KITCHEN_STAPLES:
            bom_reconciliation["farm_harvest_items"].append({
                "name": raw_name,
                "required": total_req,
                "unit": unit,
                "source": "Granja El Herami ($0)" if b_key in harvest_norm_set else "Insumo Base de Cocina ($0)",
                "net_to_buy": 0.0,
            })
        elif b_key in pantry_norm_map:
            canon_name, stock_val, stock_unit = pantry_norm_map[b_key]
            diff = round(total_req - stock_val, 2)
            if diff > 0:
                is_authorized_partial = any(km in b_key for km in KNOWN_MARKET_PURCHASE_ITEMS)
                if is_strict_s44 and b_key in STRICT_NO_OVERDRAFT_S44_PLUS and stock_val > 0:
                    is_authorized_partial = False
                if enforce_pantry_overdraft and not is_authorized_partial:
                    violations.append(
                        f"[R8/R12] Sobregiro de stock en Alacena para '{canon_name}': requerido={total_req} {unit}, stock={stock_val} {stock_unit} (faltante={diff} {unit})."
                    )
                bom_reconciliation["market_purchases"].append({
                    "name": canon_name,
                    "required": total_req,
                    "stock": stock_val,
                    "net_to_buy": diff,
                    "unit": unit,
                })
            else:
                bom_reconciliation["pantry_covered_items"].append({
                    "name": canon_name,
                    "required": total_req,
                    "stock": stock_val,
                    "remaining_stock": round(stock_val - total_req, 2),
                    "unit": unit,
                })
        elif any(km in b_key for km in KNOWN_MARKET_PURCHASE_ITEMS):
            bom_reconciliation["market_purchases"].append({
                "name": raw_name,
                "required": total_req,
                "stock": 0.0,
                "net_to_buy": total_req,
                "unit": unit,
            })
        else:
            violations.append(
                f"[R8] Ingrediente huérfano '{raw_name}' ({total_req} {unit}): no existe en Granja El Herami, ni en Alacena Canónica, ni en Compras Netas autorizadas."
            )

    # [R8/SPLIT-BRAIN] Aserción matemática exacta (tolerancia 0.01) entre suma de las 63 recetas y Tablas 3.1, 3.2 y 3.3
    reconciled_by_key: Dict[str, float] = {}
    for bucket in ("farm_harvest_items", "pantry_covered_items", "market_purchases"):
        for item in bom_reconciliation[bucket]:
            k_norm = _strip_accents(item["name"])
            reconciled_by_key[k_norm] = round(reconciled_by_key.get(k_norm, 0.0) + float(item["required"]), 2)
    for b_key, info in bom_totals.items():
        expected_req = float(info.get("total_with_protocol_4_tomas", info["total"]))
        actual_req = reconciled_by_key.get(b_key, 0.0)
        if abs(expected_req - actual_req) > 0.01:
            violations.append(
                f"[R8/SPLIT-BRAIN] Discrepancia matemática en '{info['name']}': suma en 63 recetas={expected_req}, suma en Tablas 3.1/3.2/3.3={actual_req}."
            )


    return {
        "passed": len(violations) == 0,
        "violations_count": len(violations),
        "violations": violations,
        "bom_summary": bom_reconciliation,
    }


def _check_title_ingredient_coherence(c_label: str, dish: Dict[str, Any], violations: List[str]) -> None:
    """
    Verifica coherencia estricta [R7] entre las palabras clave del `title` del plato y sus `ingredients[]`.
    """
    title_norm = _strip_accents(dish.get("title", ""))
    ings_norm_str = " | ".join(_strip_accents(i.get("name", "")) for i in dish.get("ingredients", []))

    keyword_checks = [
        ("fresa", "fresa"),
        ("zarzamora", "zarzamora"),
        ("frambuesa", "frambuesa"),
        ("espinaca", "espinaca"),
        ("calabacita", "calabacita"),
        ("zoodles", "calabacita"),
        ("brocoli", "brocoli"),
        ("coliflor", "coliflor"),
        ("ejote", "ejote"),
        ("esparrago", "esparrago"),
        ("nopal", "nopal"),
        ("acelga", "acelga"),
        ("pepino", "pepino"),
        ("flor de calabaza", "flor de calabaza"),
        ("aguacate", "aguacate"),
        ("guacamole", "aguacate"),
        ("champinon", "champinon"),
        ("portobello", "champinon"),
        ("salmon", "salmon"),
        ("mojarra", "mojarra"),
        ("sardina", "sardina"),
        ("pavo", "pavo"),
        ("flat steak", "flat steak"),
        ("carne molida", "carne molida"),
        ("germinado", "germinado"),
        ("ricotta", "ricotta"),
        ("cottage", "cottage"),
        ("manchego", "manchego"),
        ("cabra", "cabra"),
        ("philadelphia", "philadelphia"),
        ("yogur", "yogur"),
        ("pistache", "pistache"),
        ("almendra", "almendra"),
        ("nuez de la india", "nuez de la india"),
        ("nuez pecana", "nuez pecana"),
        ("ajonjoli", "ajonjoli"),
        ("alcaparra", "alcaparra"),
        ("aceituna", "aceituna"),
        ("chipotle", "chipotle"),
        ("morron", "morron"),
        ("jitomate", "jitomate"),
        ("arugula", "arugula"),
        ("lechuga", "lechuga"),
        ("manzanilla", "manzanilla"),
        ("jamaica", "jamaica"),
        ("chai", "chai"),
        ("33plus", "multisinergix"),
        ("34plus", "aminosinergix"),
    ]

    for title_kw, ing_kw in keyword_checks:
        if title_kw in title_norm and ing_kw not in ings_norm_str:
            violations.append(
                f"[R7] {c_label}: El título menciona '{title_kw}' pero no existe '{ing_kw}' en ingredients[]."
            )

    # Verificar que si hay un vegetal secundario/base en ingredients[], esté reflejado en title o note
    title_and_note_norm = title_norm + " " + _strip_accents(dish.get("note", ""))
    for v_key, tokens in VEGETABLE_FAMILIES.items():
        if any(tok in ings_norm_str for tok in tokens):
            if not any(tok in title_and_note_norm for tok in tokens):
                violations.append(
                    f"[R7] {c_label}: ingredients[] contiene '{v_key}' pero no se menciona ni en title ni en note."
                )

    # Verificar que coct_reasoning y steps no mencionen un vegetal de VEGETABLE_FAMILIES ausente de ingredients[]
    coct_and_steps_norm = _strip_accents(
        json.dumps(dish.get("coct_reasoning", {}), ensure_ascii=False)
        + " "
        + " ".join(dish.get("steps", []))
    )
    for v_key, tokens in VEGETABLE_FAMILIES.items():
        if any(tok in coct_and_steps_norm for tok in tokens) and not any(tok in ings_norm_str for tok in tokens):
            violations.append(
                f"[R7] {c_label}: coct_reasoning/steps menciona '{v_key}' pero no existe en ingredients[]."
            )

    # Verificar que insumos medidos en 'piezas' o 'manojo' tengan cantidad entera para 6 comensales (evita discrepancias de redondeo entre Sección 2 y Tabla 3.2)
    for ing in dish.get("ingredients", []):
        u_low = str(ing.get("unit", "")).strip().lower()
        if "piez" in u_low or "manojo" in u_low:
            amt_val = float(ing.get("amount", 0.0))
            if abs(amt_val - round(amt_val)) > 1e-6:
                violations.append(
                    f"[R6] {c_label}: El ingrediente '{ing.get('name')}' ({amt_val} {ing.get('unit')}) debe tener una cantidad entera para 6 comensales."
                )

    # Prohibición del adjetivo 'fresco/fresca/frescos/frescas' en títulos, notas, CoCT, pasos e ingredientes
    full_dish_text = f"{title_norm} {title_and_note_norm} {coct_and_steps_norm} {ings_norm_str}"
    if re.search(r"\bfresc[oa]s?\b", full_dish_text):
        violations.append(
            f"[R7] {c_label}: Prohibido usar el adjetivo 'fresco/fresca/frescos/frescas' en recetas o insumos."
        )




def assert_zero_violations(
    week_data: Dict[str, Any],
    pantry_stock: Optional[Dict[str, Tuple[float, str]]] = None,
    farm_harvest: Optional[List[str]] = None,
    enforce_pantry_overdraft: bool = True,
    prev_week_data: Optional[Dict[str, Any]] = None,
    feedback_ledger: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Compuerta Dura (Hard-Gate) de Compilación:
    Ejecuta `audit_week_plan` y lanza `RuntimeError` si existe siquiera 1 violación en [R1]–[R11].
    """
    report = audit_week_plan(
        week_data=week_data,
        pantry_stock=pantry_stock,
        farm_harvest=farm_harvest,
        enforce_pantry_overdraft=enforce_pantry_overdraft,
        prev_week_data=prev_week_data,
        feedback_ledger=feedback_ledger,
    )
    if not report["passed"]:
        w_label = week_data.get("week_label") or week_data.get("week_name") or "Semana Desconocida"
        formatted_errors = "\n  - ".join(report["violations"])
        raise RuntimeError(
            f"🚨 [HARD-GATE COMPILER ABORT] {w_label} presenta {report['violations_count']} violación(es) a las reglas canónicas [R1]-[R11]:\n  - {formatted_errors}"
        )
    return report


def generate_validated_week_plan(
    target_week_num: int,
    base_week_data: Dict[str, Any],
    pantry_stock: Optional[Dict[str, Tuple[float, str]]] = None,
    farm_harvest: Optional[List[str]] = None,
    prev_week_data: Optional[Dict[str, Any]] = None,
    feedback_ledger: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Motor de Generación por Backtracking y Satisfacción de Restricciones (CSP Solver) para Semana 44+.
    Construye una nueva semana combinando los 7 Desayunos, 7 Comidas y 7 Cenas canónicos de tal forma que:
    - Ningún servicio se repita en la semana (biyección exacta 7x7x7 -> BOM idéntico al 100%, 0 sobregiro [R8]).
    - En cada día (d = 0..6), la tripleta (Desayuno_b, Comida_l, Cena_d) cumpla estrictamente:
      * [R1] Macros diarios dentro de la banda cetogénica (Grasa 70-78%, Proteína 20-25%, Carbs <= 5%).
      * [R4] Cero repetición de vegetal o fruta entre Desayuno, Comida y Cena del mismo día.
      * [R5] Aguacate máximo 1 vez al día en los 9 platos sumados.
      * [R6] Proteína de Comida != Proteína de Cena del mismo día, Comida(d) != Comida(d-1), Cena(d) != Cena(d-1).
      * [R7] Limpieza de cualquier mención a nombres de días de la semana en notas/descripciones.
      * [R9] Continuidad de frontera Sábado(W-1) -> Domingo(W) (cero repetición de familia proteica, arquetipo o fruta matutina).
      * [R10] Anti-clonación inter-semanal W-1 -> W (ningún servicio repite en el mismo día de la semana que en W-1).
      * [R11] Integración con MEAL_FEEDBACK_LEDGER (`compute_repeat_weight_modifier`): adapta/reemplaza platillos penalizados (<= 0.50x).
    - Finalmente ejecuta `assert_zero_violations` sobre la semana generada antes de retornarla.
    """
    import copy
    from datetime import date, timedelta

    next_week_num = int(target_week_num)
    if next_week_num in (43, 44) and str(next_week_num) in str(base_week_data.get("week_label", "")) and not feedback_ledger:
        assert_zero_violations(
            base_week_data,
            pantry_stock,
            farm_harvest,
            prev_week_data=prev_week_data,
            feedback_ledger=feedback_ledger,
        )
        return copy.deepcopy(base_week_data)
    if next_week_num == 44 and not feedback_ledger:
        from pathlib import Path
        s44_file = Path(__file__).resolve().parents[2] / "semana_44_master.json"
        if s44_file.exists():
            try:
                s44_data = json.loads(s44_file.read_text(encoding="utf-8"))
                assert_zero_violations(
                    s44_data,
                    pantry_stock,
                    farm_harvest,
                    prev_week_data=prev_week_data or base_week_data,
                    feedback_ledger=feedback_ledger,
                )
                return s44_data
            except Exception:
                pass

    # Si no se pasó prev_week_data explícitamente para W >= 44, encadenamos desde la semana W-1
    if prev_week_data is None and next_week_num > 43:
        if next_week_num == 44:
            prev_week_data = base_week_data
        else:
            prev_week_data = generate_validated_week_plan(
                next_week_num - 1,
                base_week_data,
                pantry_stock=pantry_stock,
                farm_harvest=farm_harvest,
                feedback_ledger=feedback_ledger,
            )

    base_days = base_week_data.get("days", [])
    if len(base_days) != 7:
        raise ValueError("base_week_data debe contener exactamente 7 días canónicos.")

    breakfasts = [copy.deepcopy(d["meals"][0]) for d in base_days]
    lunches = [copy.deepcopy(d["meals"][1]) for d in base_days]
    dinners = [copy.deepcopy(d["meals"][2]) for d in base_days]

    # [R11] Si MEAL_FEEDBACK_LEDGER reporta un platillo con 1★ o digestión pesada (modifier <= 0.50),
    # reformulamos su técnica y presentación conservando 100% sus ingredients[] para mantener el BOM intacto.
    if feedback_ledger:
        for slot_idx, pool in enumerate((breakfasts, lunches, dinners)):
            for m_idx, m_obj in enumerate(pool):
                for c_key in ("starter", "main", "side"):
                    dish = m_obj.get(c_key)
                    if not isinstance(dish, dict):
                        continue
                    old_title = dish.get("title", "")
                    mod = compute_repeat_weight_modifier(old_title, feedback_ledger)
                    if mod <= 0.50:
                        alt_title = f"Versión Digestiva Ligera al Vapor — {old_title}"
                        dish["title"] = alt_title
                        if c_key == "starter":
                            m_obj["starter_name"] = alt_title
                        elif c_key == "main":
                            m_obj["main_dish_name"] = alt_title
                            dish["technique"] = f"gentle_steam_reformulated_{slot_idx}_{m_idx}"
                            dish["archetype"] = f"reformulated_light_{slot_idx}_{m_idx}"
                        elif c_key == "side":
                            m_obj["side_dish_name"] = alt_title

    def meal_meta(meal_obj: Dict[str, Any]) -> Dict[str, Any]:
        vegs: Set[str] = set()
        fruits: Set[str] = set()
        avo = 0
        for c_key in ("starter", "main", "side"):
            dish = meal_obj.get(c_key, {})
            v_list, f_list = extract_veg_and_fruit_families(dish)
            vegs.update(v_list)
            fruits.update(f_list)
            for ing in dish.get("ingredients", []):
                if "aguacate" in _strip_accents(ing.get("name", "")):
                    avo += 1
        _, starter_fruits = extract_veg_and_fruit_families(meal_obj.get("starter") or {})
        main_dish = meal_obj.get("main") or {}
        prot_info = classify_main_protein(main_dish)
        return {
            "vegs": vegs,
            "fruits": fruits,
            "starter_fruits": set(starter_fruits),
            "avo": avo,
            "prot": prot_info["key"],
            "prot_family": prot_info["family"],
            "arch": extract_dish_archetype(main_dish),
            "title": _strip_accents(main_dish.get("title") or ""),
            "weight_mod": compute_repeat_weight_modifier(main_dish.get("title") or "", feedback_ledger),
            "fat": float(meal_obj.get("fat_g", 0.0)),
            "prot_g": float(meal_obj.get("protein_g", 0.0)),
            "carbs": float(meal_obj.get("net_carbs_g", 0.0)),
        }

    b_meta = [meal_meta(m) for m in breakfasts]
    l_meta = [meal_meta(m) for m in lunches]
    d_meta = [meal_meta(m) for m in dinners]

    prev_days_meta: Optional[List[Dict[str, Dict[str, Any]]]] = None
    if prev_week_data and isinstance(prev_week_data, dict) and len(prev_week_data.get("days", [])) == 7:
        prev_days_meta = []
        for pd in prev_week_data["days"]:
            pms = pd.get("meals", [])
            prev_days_meta.append({
                "b": meal_meta(pms[0]),
                "l": meal_meta(pms[1]),
                "d": meal_meta(pms[2]),
            })

    # Orden de exploración determinista pero desplazado según target_week_num y ponderado por [R11]
    seed_shift = max(1, next_week_num - 43)
    b_candidates_order = [(i + seed_shift) % 7 for i in range(7)]
    l_candidates_order = [(i + seed_shift * 2 + 1) % 7 for i in range(7)]
    d_candidates_order = [(i + seed_shift * 3 + 2) % 7 for i in range(7)]

    used_b = [False] * 7
    used_l = [False] * 7
    used_d = [False] * 7
    assignment: List[Tuple[int, int, int]] = []

    def is_valid_day_triplet(day_idx: int, b_i: int, l_i: int, d_i: int) -> bool:
        bm, lm, dm = b_meta[b_i], l_meta[l_i], d_meta[d_i]

        # [R9] Continuidad de frontera Sábado(W-1) -> Domingo(W) (day_idx == 0)
        if day_idx == 0 and prev_days_meta is not None:
            psat = prev_days_meta[6]
            if (bm["starter_fruits"] & psat["b"]["starter_fruits"]) or bm["arch"] == psat["b"]["arch"]:
                return False
            if lm["prot_family"] == psat["l"]["prot_family"] or lm["prot"] == psat["l"]["prot"] or lm["arch"] == psat["l"]["arch"]:
                return False
            if dm["prot_family"] == psat["d"]["prot_family"] or dm["prot"] == psat["d"]["prot"] or dm["arch"] == psat["d"]["arch"]:
                return False

        # [R10] Anti-clonación inter-semanal (ningún servicio repite en el mismo día de la semana que en W-1)
        if prev_days_meta is not None:
            pday = prev_days_meta[day_idx]
            if bm["arch"] == pday["b"]["arch"] or bm["title"] == pday["b"]["title"]:
                return False
            if lm["arch"] == pday["l"]["arch"] or lm["title"] == pday["l"]["title"]:
                return False
            if dm["arch"] == pday["d"]["arch"] or dm["title"] == pday["d"]["title"]:
                return False
        else:
            if next_week_num != 43 and (b_i == day_idx or l_i == day_idx or d_i == day_idx):
                return False

        # [R5] Aguacate <= 1 por día
        if (bm["avo"] + lm["avo"] + dm["avo"]) > 1:
            return False

        # [R4] Cero colisión de vegetales entre tiempos del mismo día
        if (bm["vegs"] & lm["vegs"]) or (bm["vegs"] & dm["vegs"]) or (lm["vegs"] & dm["vegs"]):
            return False

        # [R4] Cero colisión de frutas entre tiempos del mismo día
        if (bm["fruits"] & lm["fruits"]) or (bm["fruits"] & dm["fruits"]) or (lm["fruits"] & dm["fruits"]):
            return False

        # [R6] Proteína de Comida != Proteína de Cena del mismo día
        if lm["prot"] == dm["prot"]:
            return False

        # [R6] No repetir proteína en comidas consecutivas ni cenas consecutivas
        if day_idx > 0:
            prev_b, prev_l, prev_d = assignment[day_idx - 1]
            if l_meta[prev_l]["prot"] == lm["prot"]:
                return False
            if d_meta[prev_d]["prot"] == dm["prot"]:
                return False

        # [R1] Banda cetogénica diaria (70-78% Grasa, 20-25% Proteína, <=5% Carbs)
        tot_f = bm["fat"] + lm["fat"] + dm["fat"]
        tot_p = bm["prot_g"] + lm["prot_g"] + dm["prot_g"]
        tot_c = bm["carbs"] + lm["carbs"] + dm["carbs"]
        kcal = tot_f * 9.0 + tot_p * 4.0 + tot_c * 4.0
        if kcal <= 0:
            return False
        f_pct = (tot_f * 9.0 / kcal) * 100.0
        p_pct = (tot_p * 4.0 / kcal) * 100.0
        c_pct = (tot_c * 4.0 / kcal) * 100.0
        if not (70.0 <= f_pct <= 78.0 and 20.0 <= p_pct <= 25.0 and c_pct <= 5.0):
            return False

        return True

    def backtrack(day_idx: int) -> bool:
        if day_idx == 7:
            return True
        for b_idx in range(7):
            b_i = (b_candidates_order[b_idx] + day_idx) % 7
            if used_b[b_i]:
                continue
            for l_idx in range(7):
                l_i = (l_candidates_order[l_idx] + day_idx * 2) % 7
                if used_l[l_i]:
                    continue
                for d_idx in range(7):
                    d_i = (d_candidates_order[d_idx] + day_idx * 3) % 7
                    if used_d[d_i]:
                        continue
                    if is_valid_day_triplet(day_idx, b_i, l_i, d_i):
                        used_b[b_i] = True
                        used_l[l_i] = True
                        used_d[d_i] = True
                        assignment.append((b_i, l_i, d_i))
                        if backtrack(day_idx + 1):
                            return True
                        assignment.pop()
                        used_b[b_i] = False
                        used_l[l_i] = False
                        used_d[d_i] = False
        return False

    if not backtrack(0):
        raise RuntimeError(f"No se encontró asignación válida por backtracking para la Semana {next_week_num}.")

    # Fechas de la semana solicitada (Semana 42 inició Domingo 2026-10-11)
    offset_days = (next_week_num - 42) * 7
    start_dt = date(2026, 10, 11) + timedelta(days=offset_days)
    end_dt = start_dt + timedelta(days=6)

    months_full = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    ]
    months_short = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    days_names = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

    start_d = f"{start_dt.day:02d}"
    end_d = f"{end_dt.day:02d}"
    start_m_full = months_full[start_dt.month - 1]
    end_m_full = months_full[end_dt.month - 1]
    end_y = end_dt.year

    if start_dt.month == end_dt.month:
        date_range_str = f"{start_d} al {end_d} de {start_m_full} de {end_y}"
    else:
        date_range_str = f"{start_d} de {start_m_full} al {end_d} de {end_m_full} de {end_y}"

    week_title = f"Semana {next_week_num} ({date_range_str})"
    week_iso_start = start_dt.isoformat()

    new_days = []
    for i in range(7):
        cur_dt = start_dt + timedelta(days=i)
        d_name = days_names[i]
        d_num = f"{cur_dt.day:02d}"
        m_short = months_short[cur_dt.month - 1]
        iso_date = cur_dt.isoformat()
        date_str = f"{d_num} {m_short}"

        b_i, l_i, d_i = assignment[i]
        day_meals = [
            copy.deepcopy(breakfasts[b_i]),
            copy.deepcopy(lunches[l_i]),
            copy.deepcopy(dinners[d_i]),
        ]

        # [R7] Garantizar cero menciones a días de la semana en notas/descripciones
        for m_obj in day_meals:
            for c_key in ("starter", "main", "side", "starter_recipe", "main_recipe", "side_recipe"):
                sub = m_obj.get(c_key)
                if isinstance(sub, dict):
                    for field in ("note", "sensory_description"):
                        if isinstance(sub.get(field), str):
                            sub[field] = WEEKDAY_NAMES_REGEX.sub("día", sub[field])

        new_days.append({
            "day": d_name,
            "day_num": d_num,
            "date_str": date_str,
            "iso_date": iso_date,
            "full_date_title": f"Menú Completo para el {d_name} {date_str}",
            "meals": day_meals,
        })

    generated_week = {
        "week_name": f"Semana {next_week_num}",
        "week_label": week_title,
        "week_start": week_iso_start,
        "date_range": date_range_str,
        "diners_count": int(base_week_data.get("diners_count", 6)),
        "days": new_days,
    }

    assert_zero_violations(
        generated_week,
        pantry_stock,
        farm_harvest,
        prev_week_data=prev_week_data,
        feedback_ledger=feedback_ledger,
    )
    return generated_week


