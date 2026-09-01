"""
Atelier T.I.L.O.® — Validador de Cumplimiento Gastronómico y Gobernanza Clínica (V23.1.0 SSOT)
Garantiza el cumplimiento estricto de la Directiva Sistémica Vinculante y la Cobertura Bidireccional de Entidades.
"""

import re
import unicodedata
from typing import Tuple, List
from app.schemas import TypedRecipeSchema, CulinaryTechniqueEnum

FORBIDDEN_KEYWORDS = [
    "cerdo", "puerco", "tocino de cerdo", "jamon de cerdo", "manteca", "chicharron",
    "chile", "serrano", "jalapeño", "habanero", "chipotle", "cayena", "paprika picante",
    "trigo", "maiz", "arroz", "harina refinada", "azucar"
]

STOPWORDS_CULINARIAS = {
    "de", "la", "el", "los", "las", "con", "y", "en", "al", "a", "del", "para", "por", "un", "una",
    "preparación", "estilo", "artesanal", "fresco", "fresca", "frescos", "frescas", "granja", "herami",
    "revueltos", "revuelto", "asados", "asado", "salteada", "salteado", "gratinados", "gratinadas", "gratinado",
    "pochados", "pochado", "al", "vapor", "rostizado", "rostizada", "horneados", "horneadas", "horneado",
    "sellados", "sellado", "marinado", "marinada", "crujiente", "dorado", "dorada", "casero", "casera",
    "viva", "vivos", "puro", "pura", "ligero", "ligera", "ligeros", "ligeras", "tiernos", "tiernas", "tierna", "tierno",
    "coctel", "cóctel", "omelette", "especial", "tazón", "tazon", "bowl", "ensalada", "ensaladas", "crema", "cremas", "sopa", "sopas",
    "consomé", "consome", "mousse", "waffle", "waffles", "pancakes", "crepa", "crepas", "muffins", "muffin", "platillo",
    "gelatina", "gelatinas", "infusión", "infusion", "infusiones", "té", "te", "bebida", "bebidas", "caldo", "caldos", "puchero",
    "brochetas", "brocheta", "zoodles", "bastones", "bastón", "baston", "frittata", "tartar", "carpaccio", "ceviche", "chilorio",
    "barbacoa", "parrillada", "mix", "tradicional", "nocturna", "nocturno", "relajante", "digestiva", "digestivo", "extra", "virgen",
    "maduro", "madura", "maduros", "maduras", "estrellados", "estrellado", "carbón", "carbon", "sartén", "sarten", "plancha",
    "horno", "parrilla", "rellenas", "rellenos", "relleno", "rellena", "salsa", "salsas", "especias", "especia", "fría", "fria",
    "verde", "verdes", "tabasqueñas", "tabasqueña", "claro", "clara", "rallado", "rallada", "baby", "vinagreta", "pastoreo",
    "seleccionado", "seleccionada", "seleccionados", "seleccionadas", "molida", "molido", "troceado", "troceada",
    "benedictinos", "sobre", "nube", "holandesa", "aderezo", "sin", "crotones", "abanico", "salpicón", "salpicon", "costra",
    "ranchera", "orgánico", "orgánica", "orgánicos", "orgánicas", "fileteadas", "fileteada", "fileteados", "cremosa", "desmenuzada",
    "keto", "cetogénica", "cetogénico"
}

PROCESS_ADJECTIVES = {
    "salteada", "salteado", "salteados", "gratinados", "gratinadas", "gratinado",
    "pochados", "pochado", "asados", "asado", "rostizado", "rostizada", "horneados", "horneadas",
    "horneado", "crujiente", "dorado", "dorada", "sellado", "sellados"
}

# Mapeo de equivalencias lematizadas para ingredientes españoles comunes
INGREDIENT_ALIASES = {
    "nueces": ["nuez", "nueces", "pecana", "pecanas", "castilla"],
    "nuez": ["nuez", "nueces", "pecana", "pecanas", "castilla"],
    "limón": ["limón", "limon", "limones"],
    "limon": ["limón", "limon", "limones"],
    "espárragos": ["espárrago", "esparrago", "espárragos", "esparragos"],
    "esparragos": ["espárrago", "esparrago", "espárragos", "esparragos"],
    "pitahaya": ["pitahaya", "pitaya"],
    "pitaya": ["pitahaya", "pitaya"],
    "calabacitas": ["calabacita", "calabacitas", "calabaza", "zucchini"],
    "calabacita": ["calabacita", "calabacitas", "calabaza", "zucchini"],
    "zucchini": ["calabacita", "calabacitas", "calabaza", "zucchini"],
    "rostizado": ["rostizado", "rostizada", "rostizar", "hornear", "horno", "horneado", "horneada"],
    "rostizada": ["rostizado", "rostizada", "rostizar", "hornear", "horno", "horneado", "horneada"],
    "moras": ["mora", "moras", "frambuesa", "frambuesas", "fruta", "frutas"],
    "mora": ["mora", "moras", "frambuesa", "frambuesas", "fruta", "frutas"],
    "frambuesa": ["frambuesa", "frambuesas", "mora", "moras"],
    "frambuesas": ["frambuesa", "frambuesas", "mora", "moras"],
    "arándanos": ["arándano", "arandano", "arándanos", "arandanos"],
    "arandanos": ["arándano", "arandano", "arándanos", "arandanos"],
    "jengibre": ["jengibre"],
    "toronjil": ["toronjil"],
    "manzanilla": ["manzanilla"],
    "alcaparras": ["alcaparra", "alcaparras"],
    "cognac": ["cognac", "coñac", "licor"],
    "eneldo": ["eneldo"],
    "salvia": ["salvia"],
    "hinojo": ["hinojo"],
    "sésamo": ["sésamo", "sesamo", "ajonjolí", "ajonjoli"],
    "sesamo": ["sésamo", "sesamo", "ajonjolí", "ajonjoli"],
    "cheddar": ["cheddar", "queso"],
    "gouda": ["gouda", "queso"],
    "panela": ["panela", "queso"],
    "manchego": ["manchego", "queso"],
    "chayotes": ["chayote", "chayotes"],
    "chayote": ["chayote", "chayotes"],
    "aguacate": ["aguacate", "hass"],
    "atún": ["atún", "atun"],
    "atun": ["atún", "atun"]
}

def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').lower()

def get_word_root(word: str) -> str:
    w = strip_accents(word)
    if w.endswith("es") and len(w) > 4:
        w = w[:-2]
    elif w.endswith("s") and len(w) > 3:
        w = w[:-1]
    return w[:3] if len(w) >= 4 else w

def validate_entity_coverage(recipe: TypedRecipeSchema) -> Tuple[bool, str]:
    """
    Valida que los sustantivos clave del título existan en el BOM y en los Pasos,
    y que los adjetivos de proceso culinario estén documentados en los pasos técnicos.
    """
    title_text = (recipe.title or recipe.name or "").lower()
    words = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]+\b', title_text)
    
    # 1. Extraer sustantivos e ingredientes principales
    core_entities = [w for w in words if w.lower() not in STOPWORDS_CULINARIAS and len(w) > 2]
    # 2. Extraer adjetivos de proceso requeridos en steps
    process_reqs = [w for w in words if w.lower() in PROCESS_ADJECTIVES]

    # Consolidar texto de ingredientes y pasos
    ingredient_items = []
    if recipe.ingredient_groups:
        for g in recipe.ingredient_groups:
            items = g.get("items", []) if isinstance(g, dict) else getattr(g, "items", [])
            if items:
                for item in items:
                    name = item.get("name") if isinstance(item, dict) else getattr(item, "name", str(item))
                    ingredient_items.append(name)
    if hasattr(recipe, "ingredients") and recipe.ingredients:
        items = recipe.ingredients.get("items", []) if isinstance(recipe.ingredients, dict) else getattr(recipe, "ingredients", [])
        if items:
            for item in items:
                name = item.get("name") if isinstance(item, dict) else getattr(item, "name", str(item))
                ingredient_items.append(name)

    all_ingredients_text = strip_accents(" ".join(ingredient_items))
    
    steps_list = []
    if recipe.steps:
        for s in recipe.steps:
            steps_list.append(s.action_description if hasattr(s, "action_description") else str(s))
    all_steps_text = strip_accents(" ".join(steps_list))

    missing_in_bom = []
    missing_in_steps = []

    for entity in core_entities:
        ent_clean = strip_accents(entity)
        root = get_word_root(entity)
        aliases = INGREDIENT_ALIASES.get(entity.lower(), [entity.lower(), ent_clean, root])

        # Comprobar en BOM
        found_in_bom = any(strip_accents(alias) in all_ingredients_text for alias in aliases)
        if not found_in_bom:
            missing_in_bom.append(entity)

        # Comprobar en Steps
        found_in_steps = any(strip_accents(alias) in all_steps_text for alias in aliases)
        if not found_in_steps:
            missing_in_steps.append(entity)

    if missing_in_bom:
        return False, f"El BOM omite ingredientes clave del título: {missing_in_bom}"
    if missing_in_steps:
        return False, f"La preparación en steps omite técnicas o ingredientes del título: {missing_in_steps}"

    # Validar que adjetivos de proceso estén documentados en steps
    for proc in process_reqs:
        root_proc = get_word_root(proc)
        if root_proc not in all_steps_text:
            return False, f"Los pasos omiten la técnica procesal indicada en el título: '{proc}'"

    return True, "OK"

def validate_bom_usage_in_steps(recipe: TypedRecipeSchema) -> Tuple[bool, str]:
    """
    Verifica que cada ingrediente declarado en el BOM (salvo sazonadores menores)
    sea manipulado explícitamente dentro del texto de los pasos de preparación.
    """
    steps_list = []
    if recipe.steps:
        for s in recipe.steps:
            steps_list.append(s.action_description if hasattr(s, "action_description") else str(s))
    steps_text = strip_accents(" ".join(steps_list))

    unused_items = []
    ingredient_items = []
    if recipe.ingredient_groups:
        for g in recipe.ingredient_groups:
            items = g.get("items", []) if isinstance(g, dict) else getattr(g, "items", [])
            if items:
                for item in items:
                    ingredient_items.append(item)
    if hasattr(recipe, "ingredients") and recipe.ingredients:
        items = recipe.ingredients.get("items", []) if isinstance(recipe.ingredients, dict) else getattr(recipe, "ingredients", [])
        if items:
            for item in items:
                ingredient_items.append(item)

    generic_words = {"de", "la", "el", "los", "las", "con", "y", "en", "al", "a", "del", "para", "por", "un", "una", "fresco", "fresca", "frescos", "frescas", "granja", "herami", "orgánico", "orgánica", "orgánicos", "orgánicas", "troceado", "troceada", "picado", "picada", "molido", "molida", "sal", "pimienta"}

    for item in ingredient_items:
        iname = (item.get("name") if isinstance(item, dict) else getattr(item, "name", str(item))).lower()
        unit = (item.get("unit") if isinstance(item, dict) else getattr(item, "unit", "")).lower()
        if unit in ["pizcas", "pizca", "al gusto"]:
            continue

        item_words = [w for w in re.findall(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]+', iname) if w.lower() not in generic_words and len(w) > 2]
        
        # Comprobar si al menos una palabra clave del ingrediente está en los pasos
        found_in_steps = False
        for w in item_words:
            w_clean = strip_accents(w)
            root = get_word_root(w)
            aliases = INGREDIENT_ALIASES.get(w.lower(), [w.lower(), w_clean, root])
            if any(strip_accents(alias) in steps_text for alias in aliases):
                found_in_steps = True
                break

        if not found_in_steps and item_words:
            unused_items.append(iname)

    if len(unused_items) > 1:
        return False, f"Ingredientes del BOM huérfanos sin procesar en los pasos: {unused_items}"

    return True, "OK"

def validate_recipe_compliance(recipe: TypedRecipeSchema, forbidden_harvest: list = None) -> Tuple[bool, str]:
    """
    Valida la receta generada contra la Directiva Sistémica Vinculante, Gobernanza Agronómica
    y Cobertura Bidireccional de Entidades.
    Retorna (True, "OK") si cumple con todos los criterios o (False, motivo) si debe ser rechazada.
    """
    if not recipe or not (recipe.title or recipe.name):
        return False, "La receta está vacía o no tiene título."

    title_lower = (recipe.title or recipe.name or "").lower().strip()
    
    # 1. REGLA DE GOBERNANZA AGRONÓMICA: Rechazo de Insumos de Cosecha Agotados / Prohibidos
    if forbidden_harvest:
        for bad_h in forbidden_harvest:
            clean_bad = bad_h.lower().replace("fresca", "").replace("frescos", "").replace("tiernos", "").replace("tiernas", "").strip()
            if len(clean_bad) >= 3:
                if clean_bad in title_lower:
                    return False, f"Insumo de cosecha prohibido/agotado en título: '{bad_h}'."
                if recipe.ingredient_groups:
                    for g in recipe.ingredient_groups:
                        if g.items:
                            for item in g.items:
                                iname = (item.name if hasattr(item, "name") else str(item)).lower()
                                if clean_bad in iname:
                                    return False, f"Insumo de cosecha prohibido/agotado en ingrediente: '{iname}' contiene '{bad_h}'."

    # 2. REGLA DE ERRADICACIÓN DE INGREDIENTE MONOLÍTICO E INGREDIENTES PROHIBIDOS CLINICOS
    ingredient_items = []
    if recipe.ingredient_groups:
        for g in recipe.ingredient_groups:
            items = g.get("items", []) if isinstance(g, dict) else getattr(g, "items", [])
            if items:
                for item in items:
                    name = item.get("name") if isinstance(item, dict) else getattr(item, "name", str(item))
                    ingredient_items.append(name)
    if hasattr(recipe, "ingredients") and recipe.ingredients:
        items = recipe.ingredients.get("items", []) if isinstance(recipe.ingredients, dict) else getattr(recipe, "ingredients", [])
        if items:
            for item in items:
                name = item.get("name") if isinstance(item, dict) else getattr(item, "name", str(item))
                ingredient_items.append(name)

    total_items = len(ingredient_items)
    for item_name in ingredient_items:
        item_name_lower = item_name.lower().strip()
        is_exact = item_name_lower == title_lower
        is_monolithic = len(title_lower.split()) >= 3 and title_lower in item_name_lower
        if is_exact or is_monolithic:
            return False, f"Ingrediente monolítico prohibido: '{item_name}' replica el título del plato."
        for bad in FORBIDDEN_KEYWORDS:
            if bad in item_name_lower:
                return False, f"Ingrediente prohibido según directiva clínica: '{item_name}' contiene '{bad}'."

    if total_items < 2:
        return False, "La receta debe contener al menos 2 ingredientes atómicos desglosados."

    # 3. REGLA DE COHERENCIA TÉRMICA POR TÉCNICA CULINARIA
    steps_list = []
    if recipe.steps:
        for s in recipe.steps:
            steps_list.append(s.action_description if hasattr(s, "action_description") else str(s))
    steps_combined = " ".join(steps_list).lower()
    
    if recipe.cooking_technique == CulinaryTechniqueEnum.RAW_ASSEMBLY:
        forbidden_thermal = ["cocinar a fuego", "hervir", "sellar", "sartén caliente", "fuego medio", "fuego alto"]
        for kw in forbidden_thermal:
            if kw in steps_combined:
                return False, f"Incoherencia térmica en raw_assembly: término prohibido '{kw}'."

    # 4. REGLA DE COBERTURA BIDIRECCIONAL DE ENTIDADES Y BÚSQUEDA LÉXICA
    cov_ok, cov_msg = validate_entity_coverage(recipe)
    if not cov_ok:
        return False, cov_msg

    # 5. REGLA DE USO EFECTIVO DE BOM EN PASOS DE COCINA
    bom_ok, bom_msg = validate_bom_usage_in_steps(recipe)
    if not bom_ok:
        return False, bom_msg

    # 6. REGLA DE PROHIBICIÓN DE PASOS GENÉRICOS VAGOS
    generic_patterns = [
        "preparar e higienizar insumos",
        "cocinar a fuego medio controlando la temperatura",
        "servir de inmediato en plato amplio"
    ]
    matches = sum(1 for p in generic_patterns if p in steps_combined)
    if matches >= 2:
        return False, "Secuencia de pasos detectada como plantilla genérica vaga."

    return True, "OK"
