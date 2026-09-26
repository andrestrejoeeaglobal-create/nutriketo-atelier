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
    "mar", "hass", "negra", "blanco", "blanca", "dulces", "dulce", "flor", "bisglicinato", "magnesio",
    "castilla", "arilos", "botánicas", "botanicas", "silvestre", "supremo", "frescos", "viva", "vivos",
    "de", "la", "el", "los", "las", "con", "y", "en", "al", "a", "del", "para", "por", "un", "una",
    "preparación", "estilo", "artesanal", "fresco", "fresca", "frescos", "frescas", "granja", "herami",
    "revueltos", "revuelto", "asados", "asado", "salteada", "salteado", "gratinados", "gratinadas", "gratinado",
    "pochados", "pochado", "al", "vapor", "rostizado", "rostizada", "horneados", "horneadas", "horneado",
    "sellados", "sellado", "marinado", "marinada", "crujiente", "dorado", "dorada", "casero", "casera",
    "viva", "vivos", "puro", "pura", "ligero", "ligera", "ligeros", "ligeras", "tiernos", "tiernas", "tierna", "tierno",
    "coctel", "cóctel", "omelette", "especial", "tazón", "tazon", "bowl", "ensalada", "ensaladas", "crema", "cremas", "sopa", "sopas",
    "consomé", "consome", "mousse", "waffle", "waffles", "pancakes", "crepa", "crepas", "muffins", "muffin", "platillo",
    "gelatina", "gelatinas", "infusión", "infusion", "infusiones", "té", "te", "bebida", "bebidas", "caldo", "caldos", "puchero",
    "tisana", "tisanas", "elixir", "elixires", "smoothie", "smoothies", "helado", "helada", "helados", "heladas",
    "brochetas", "brocheta", "zoodles", "bastones", "bastón", "baston", "frittata", "tartar", "carpaccio", "ceviche", "chilorio",
    "barbacoa", "parrillada", "mix", "tradicional", "nocturna", "nocturno", "relajante", "digestiva", "digestivo", "extra", "virgen",
    "maduro", "madura", "maduros", "maduras", "estrellados", "estrellado", "carbón", "carbon", "sartén", "sarten", "plancha",
    "horno", "parrilla", "rellenas", "rellenos", "relleno", "rellena", "salsa", "salsas", "especias", "especia", "fría", "fria",
    "verde", "verdes", "tabasqueñas", "tabasqueña", "claro", "clara", "rallado", "rallada", "baby", "vinagreta", "pastoreo",
    "seleccionado", "seleccionada", "seleccionados", "seleccionadas", "molida", "molido", "troceado", "troceada",
    "benedictinos", "sobre", "nube", "holandesa", "aderezo", "sin", "crotones", "abanico", "salpicón", "salpicon", "costra",
    "ranchera", "orgánico", "orgánica", "orgánicos", "orgánicas", "fileteadas", "fileteada", "fileteados", "cremosa", "cremoso", "nootrópico", "nootropico", "reparador", "reparadora", "desmenuzada",
    "keto", "cetogénica", "cetogénico", "marina", "mineral", "salados", "deshuesadas", "mediterránea", "mediterranea", "envuelto",
    "tacos", "punta", "puntas", "medallones", "medallón", "medallon", "ribeye", "sirloin", "filete", "cortes", "corte",
    "mantequilla", "tomillo", "romero", "aceite", "oliva", "jitomate", "bola", "harina", "almendras", "almendra", "hierbas", "vinagre", "manzana",
    "turcos", "cilbir", "enchiladas", "jamaica", "canela", "espinacas", "césar", "cesar", "mayonesa", "italiana", "campo", "picante",
    "secas", "alfredo", "caliente", "lechuga", "crujientes", "carne", "pechuga", "pollo", "queso", "pavo", "yogur", "griego",
    "panela", "cabra", "brócoli", "brocoli", "guacamole", "nuez", "pecana", "semillas", "girasol", "ajo", "cilantro", "coco", "calabacitas", "calabacita",
    "rústico", "rústica", "rustico", "rustica", "gourmet", "suave", "suaves", "jugo", "jugos", "real", "mignon", "reducción", "reduccion", "encostrado", "encostrada", "cama", "azahar",
    "huachinango", "róbalo", "robalo", "fajitas", "ceto", "espejo", "comal", "finas", "vegetales", "vegetal", "mct", "comino", "morada"
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
    "limón": ["limón", "limon", "limones", "jugo de limón", "jugo de limon"],
    "limon": ["limón", "limon", "limones", "jugo de limón", "jugo de limon"],
    "parmesano": ["parmesano", "queso parmesano"],
    "pimientos": ["pimiento", "pimientos", "pimiento morrón", "pimientos morrones"],
    "pimiento": ["pimiento", "pimientos", "pimiento morrón", "pimientos morrones"],
    "cebolla": ["cebolla", "cebollas", "cebolla blanca", "cebolla morada"],
    "cebollas": ["cebolla", "cebollas", "cebolla blanca", "cebolla morada"],
    "espárragos": ["espárrago", "esparrago", "espárragos", "esparragos"],
    "esparragos": ["espárrago", "esparrago", "espárragos", "esparragos"],
    "pitahaya": ["pitahaya", "pitaya"],
    "pitaya": ["pitahaya", "pitaya"],
    "calabacitas": ["calabacita", "calabacitas", "calabaza", "zucchini"],
    "calabacita": ["calabacita", "calabacitas", "calabaza", "zucchini"],
    "zucchini": ["calabacita", "calabacitas", "calabaza", "zucchini"],
    "rostizado": ["rostizado", "rostizada", "rostizar", "hornear", "horno", "horneado", "horneada", "asar", "asado", "asadas", "plancha", "comal", "tratamientotermico", "alta temperatura"],
    "rostizada": ["rostizado", "rostizada", "rostizar", "hornear", "horno", "horneado", "horneada", "asar", "asado", "asadas", "plancha", "comal", "tratamientotermico", "alta temperatura"],
    "pochados": ["pochados", "pochado", "pochar", "huevo", "huevos", "benedictinos", "claras"],
    "pochado": ["pochados", "pochado", "pochar", "huevo", "huevos", "benedictinos", "claras"],
    "crujiente": ["crujiente", "crujientes", "dorado", "dorada", "tostado", "tostadas", "sellar", "sellado", "tocino", "alta temperatura"],
    "moras": ["mora", "moras", "frambuesa", "frambuesas", "fruta", "frutas", "frutos rojos"],
    "mora": ["mora", "moras", "frambuesa", "frambuesas", "fruta", "frutas", "frutos rojos"],
    "frambuesa": ["frambuesa", "frambuesas", "mora", "moras", "frutos rojos"],
    "frambuesas": ["frambuesa", "frambuesas", "mora", "moras", "frutos rojos"],
    "arándanos": ["arándano", "arandano", "arándanos", "arandanos", "frutos rojos"],
    "arandanos": ["arándano", "arandano", "arándanos", "arandanos", "frutos rojos"],
    "durazno": ["durazno", "fruta"],
    "coco": ["coco", "coco rallado"],
    "jengibre": ["jengibre", "raíz", "raiz", "especias"],
    "cúrcuma": ["cúrcuma", "curcuma", "especias"],
    "curcuma": ["cúrcuma", "curcuma", "especias"],
    "matcha": ["matcha", "té", "te"],
    "33plus": ["33plus", "33 plus", "suplementación", "fórmula"],
    "34plus": ["34plus", "34 plus", "suplementación", "fórmula"],
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
    "aguacate": ["aguacate", "hass", "guacamole"],
    "atún": ["atún", "atun", "pescado"],
    "atun": ["atún", "atun", "pescado"],
    "machaca": ["machaca", "pavo desmenuzado"],
    "salmón": ["salmón", "salmon", "pescado"],
    "salmon": ["salmón", "salmon", "pescado"],
    "pescado": ["pescado", "pescado blanco", "salmón", "atún"],
    "res": ["res", "filete", "sirloin", "ribeye", "costilla", "carne molida", "carne", "punta", "mignon"],
    "shakshuka": ["shakshuka", "huevos", "jitomate"],
    "huevos": ["huevos", "huevo"],
    "brócoli": ["brócoli", "brocoli"],
    "brocoli": ["brócoli", "brocoli"],
    "berenjena": ["berenjena", "berenjenas"],
    "berenjenas": ["berenjena", "berenjenas"],
    "mostaza": ["mostaza", "mostaza antigua"],
    "pistaches": ["pistache", "pistaches", "pistacho", "pistachos"],
    "pistache": ["pistache", "pistaches", "pistacho", "pistachos"],
    "lomo": ["lomo", "pechuga", "pavo", "res", "filete"]
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
        proc_aliases = INGREDIENT_ALIASES.get(proc.lower(), [proc.lower(), root_proc])
        if not any(strip_accents(alias) in all_steps_text for alias in proc_aliases):
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

def validate_recipe_compliance(recipe: TypedRecipeSchema, forbidden_harvest: list = None, meal_type: str = None, course_role: str = None) -> Tuple[bool, str]:
    """
    Valida la receta generada contra la Directiva Sistémica Vinculante, Gobernanza Agronómica,
    Gobernanza Circadiana y Cobertura Bidireccional de Entidades.
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

    # 7. CANDADO 2 SSOT V28.0.0: ASERCIONES NEGATIVAS ESTRICTAS ANTI-ABSURDOS
    step1_text = (recipe.steps[0].action_description if hasattr(recipe.steps[0], "action_description") else str(recipe.steps[0])).lower() if recipe.steps else ""
    
    # 7.1. Prohibición de higienizar o atemperar insumos ya cocinados en Paso 1
    clean_verbs = ["higienizar", "lavar", "desinfectar", "atemperar"]
    forbidden_cooked_states = ["pochado", "pochados", "crujiente", "dorado", "dorada", "gratinado", "gratinada", "salteado", "salteada", "horneado", "horneada"]
    if any(v in step1_text for v in clean_verbs):
        for state in forbidden_cooked_states:
            if re.search(r'\b' + state + r'\b', step1_text):
                return False, f"Aberración procedimental SSOT V28.0.0: El Paso 1 intenta higienizar/atemperar insumos ya cocinados ('{state}')."

    # 7.2. Prohibición de 'o vegetales' en caldos o consomés cárnicos puros
    is_pure_meat_broth = ("consomé" in title_lower or "consome" in title_lower or "caldo" in title_lower) and not any(v in title_lower for v in ["nopales", "hortalizas", "verduras", "chayote"])
    if is_pure_meat_broth:
        if "o vegetales" in steps_combined or "cortes proteicos o vegetales" in steps_combined:
            return False, "Aberración procedimental SSOT V28.0.0: Mención de 'o vegetales' en consomé de res pura sin vegetales en BOM."

    # 7.3. Prohibición de 'semillas', 'desvenar' o 'ahuecar pulpa' en proteínas animales
    has_explicit_seeds = any(s in title_lower for s in ["semilla", "semillas", "sesamo", "sésamo", "chia", "chía", "girasol"])
    meat_words = ["pollo", "pechuga", "res", "sirloin", "ribeye", "filete", "pescado", "salmón", "salmon", "pavo", "atún", "atun"]
    is_meat_main = any(re.search(r'\b' + m + r'\b', title_lower) for m in meat_words) and not any(v in title_lower for v in ["pimientos", "pimiento", "champiñones", "portobello", "calabacitas", "zucchini"])
    
    if is_meat_main:
        for bad_seed in ["desvenar", "ahuecar pulpa"]:
            if re.search(r'\b' + bad_seed + r'\b', steps_combined):
                return False, f"Aberración anatómica SSOT V28.0.0: Mención de '{bad_seed}' en una preparación de proteína animal."
        if not has_explicit_seeds:
            if re.search(r'\bsemillas\b', steps_combined):
                return False, "Aberración anatómica SSOT V28.0.0: Mención de 'semillas' en una preparación de proteína animal sin semillas en BOM."

    # 7.4. SSOT V30.0.0: Prohibición de 'membranas albugíneas' fuera de Granada y Cítricos (rutáceas)
    if "albugíneas" in steps_combined or "albugineas" in steps_combined:
        if not any(c in title_lower for c in ["granada", "arilos", "limón", "limon", "naranja", "toronja", "mandarina"]):
            return False, "Aberración botánica SSOT V30.0.0: Mención de 'membranas albugíneas' en frutos que no son granada ni cítricos (rutáceas)."

    # 7.5. SSOT V29.0.0: Prohibición de 'colágeno' / 'tuétano' en Caldos Vegetales
    if is_pure_meat_broth is False and ("consomé" in title_lower or "caldo" in title_lower):
        if "nopales" in title_lower or "hortalizas" in title_lower:
            for bad_meat_word in ["colágeno", "colageno", "tuétano", "tuetano", "coq10"]:
                if bad_meat_word in steps_combined or bad_meat_word in (recipe.sensory_description or "").lower():
                    return False, f"Aberración bioquímica SSOT V29.0.0: Mención de '{bad_meat_word}' en un caldo vegetal puro."

    # 7.6. SSOT V29.0.0: Prohibición de discordancias gramaticales ('sazonada' con sustantivos masculinos)
    masculine_dishes = ["pepino", "apio", "aguacate", "zucchini", "ceviche", "tartar", "salpicón", "salpicon"]
    if any(m in title_lower for m in masculine_dishes) and not ("ensalada" in title_lower):
        if "sazonada" in steps_combined:
            return False, "Aberración morfosintáctica SSOT V29.0.0: Uso de participio femenino 'sazonada' para insumos o platillos masculinos."

    # 7.7. SSOT V31.0.0: Prohibición de Pollo Crudo en Ensaladas / Seguridad Alimentaria
    if ("pollo" in title_lower or "pechuga" in title_lower) and ("ensalada" in title_lower or "césar" in title_lower or "cesar" in title_lower):
        if not any(cook_word in steps_combined for cook_word in ["sellar", "dorar", "cocinar", "asar", "hornear"]):
            return False, "Riesgo Sanitario SSOT V31.0.0: Servir pollo crudo marinado en ensalada sin paso térmico de cocción."

    # 7.8. SSOT V31.0.0: Prohibición de Artefacto Tipográfico 'GB'
    if "GB " in steps_combined or "GB " in str(recipe.ingredient_groups):
        return False, "Artefacto de texto SSOT V31.0.0: Presencia del prefijo roto 'GB' en la receta."

    # 7.9. SSOT V31.0.0: Prohibición de 'pedúnculo' en Pitahaya
    if "pitahaya" in title_lower or "pitaya" in title_lower:
        if "pedúnculo" in steps_combined or "pedunculo" in steps_combined:
            return False, "Aberración botánica SSOT V31.0.0: Mención de 'pedúnculo' en la pitahaya."

    # 7.10. SSOT V31.1.0: Prohibición de 'desgranar' en frutos que no sean granada
    if "desgranar" in steps_combined:
        if not ("granada" in title_lower or "arilos" in title_lower):
            return False, "Aberración botánica SSOT V31.1.0: Mención de 'desgranar' en frutos que no son granada."

    # 7.11. SSOT V31.2.0: Prohibición de insumo fantasma mantequilla en Ensalada César
    if "césar" in title_lower or "cesar" in title_lower:
        if "mantequilla" in steps_combined:
            return False, "Insumo fantasma SSOT V31.2.0: Mención de 'mantequilla' en Ensalada César sin declarar en BOM."

    # 7.13. SSOT V35.0.0: Prohibición de cocción cárnica en bebidas / elixires
    is_beverage = any(re.search(r'\b' + b + r'\b', title_lower) for b in ["té", "te", "infusión", "infusion", "elixir", "smoothie", "tisana"]) or recipe.cooking_technique in [CulinaryTechniqueEnum.STEEP_BEVERAGE, "functional_elixir"]
    if is_beverage:
        forbidden_meat_steps = ["sellar", "maillard", "tabla de corte", "secar con papel", "fuego alto", "trinchar", "rallar queso"]
        for bad_step in forbidden_meat_steps:
            if bad_step in steps_combined:
                return False, f"Aberración procedimental SSOT V35.0.0: Mención de '{bad_step}' en una bebida o elixir."

    # 7.14. SSOT V35.0.0: Regla termodinámica (servicio de bebidas heladas/frías)
    is_cold_beverage = any(c in title_lower for c in ["helado", "helada", "frío", "fría", "macerado", "macerada"]) and is_beverage
    if is_cold_beverage:
        if "65°c" in steps_combined or "bien caliente" in steps_combined or "taza de cerámica" in steps_combined:
            return False, "Aberración termodinámica SSOT V35.0.0: Servicio a 65°C en bebida helada o fría."

    # 7.15. SSOT V36.1.0: Candado de Oro - Paridad 1:1, Bom Limpio y Protección Térmica
    has_33_title = "33plus" in title_lower or "33 plus" in title_lower
    has_34_title = "34plus" in title_lower or "34 plus" in title_lower

    bom_items = []
    for group in (recipe.ingredient_groups or []):
        items = group.items if hasattr(group, 'items') else (group.get('items', []) if isinstance(group, dict) else [])
        for item in items:
            item_name = item.name if hasattr(item, 'name') else (item.get('name', '') if isinstance(item, dict) else str(item))
            item_lower = item_name.lower()
            bom_items.append(item_lower)
            if "/" in item_lower and not ("/" in title_lower):
                return False, f"RECETA RECHAZADA SSOT V36.1.0: Ítem en BOM '{item_name}' contiene barra disyuntiva '/'."
            if any(umb in item_lower for umb in ["hierbas botánicas de la granja", "especias bioactivas", "insumos mixtos"]):
                return False, f"RECETA RECHAZADA SSOT V36.1.0: Ítem en BOM '{item_name}' es un nombre paraguas genérico."

    steps_text = " ".join(recipe.steps).lower() if recipe.steps else ""

    if has_33_title:
        if not any("33plus" in item or "33 plus" in item for item in bom_items):
            return False, f"RECETA RECHAZADA SSOT V36.1.0: '{recipe.title}' promete 33Plus pero no existe en el BOM."
        if not ("33plus" in steps_text or "33 plus" in steps_text):
            return False, f"RECETA RECHAZADA SSOT V36.1.0: '{recipe.title}' no menciona ni disuelve el 33Plus en los pasos."
        if any(phrase in steps_text for phrase in ["colar el 33plus", "filtrar la fórmula 33plus", "tamizar el 33plus", "colar la fórmula 33plus"]):
            return False, f"RECETA RECHAZADA SSOT V36.1.0: '{recipe.title}' comete el absurdo de filtrar el polvo 33Plus en el tamiz."

    if has_34_title:
        if not any("34plus" in item or "34 plus" in item for item in bom_items):
            return False, f"RECETA RECHAZADA SSOT V36.1.0: '{recipe.title}' promete 34Plus pero no existe en el BOM."
        if not ("34plus" in steps_text or "34 plus" in steps_text):
            return False, f"RECETA RECHAZADA SSOT V36.1.0: '{recipe.title}' no menciona ni disuelve el 34Plus en los pasos."
        if any(phrase in steps_text for phrase in ["colar el 34plus", "filtrar la fórmula 34plus", "tamizar el 34plus", "colar la fórmula 34plus"]):
            return False, f"RECETA RECHAZADA SSOT V36.1.0: '{recipe.title}' comete el absurdo de filtrar el polvo 34Plus en el tamiz."

    # 7.16. SSOT V36.1.0: Gestión Térmica en Gelatinas (Protocolo B)
    if "gelatina" in title_lower and (has_33_title or has_34_title):
        if any(bad in steps_text for bad in ["hervir la fórmula", "hervir 33plus", "hervir 34plus"]):
            return False, f"RECETA RECHAZADA SSOT V36.1.0: Gelatina '{recipe.title}' somete la fórmula a ebullición destructiva."

    # 7.17. SSOT V36.1.0: Gobernanza Circadiana Estricta (33Plus solo en Desayunos, 34Plus solo en Cenas)
    is_desayuno = meal_type == "Desayuno" or "desayuno" in title_lower
    is_cena = meal_type == "Cena" or "cena" in title_lower or "nocturna" in title_lower
    
    if is_desayuno:
        if has_34_title or any("34plus" in b or "34 plus" in b for b in bom_items):
            return False, f"RECETA RECHAZADA SSOT V36.1.0: Aberración circadiana. '{recipe.title}' contiene 34Plus en Desayuno (reservado exclusivamente para Cenas)."
    if is_cena:
        if has_33_title or any("33plus" in b or "33 plus" in b for b in bom_items):
            return False, f"RECETA RECHAZADA SSOT V36.1.0: Aberración circadiana. '{recipe.title}' contiene 33Plus en Cena (reservado exclusivamente para Desayunos)."

    # 7.18. SSOT V36.2.0: Gobernanza Digestiva Nocturna y Protección de Proteína Limpia en Cenas
    if is_cena and (course_role in ["main", "Plato Principal"] or "principal" in title_lower or any(m in title_lower for m in ["sirloin", "ribeye", "mignon", "costilla", "chambarete", "bife"])):
        forbidden_red_meats = ["res", "sirloin", "ribeye", "mignon", "costilla", "chambarete", "bife"]
        for red in forbidden_red_meats:
            if re.search(r'\b' + red + r'\b', title_lower):
                return False, f"RECETA RECHAZADA SSOT V36.2.0: Aberración digestiva nocturna. Cena principal '{recipe.title}' contiene carne roja pesada ('{red}')."

    # 7.19. SSOT V36.6 REV3: Sinergia Trofológica Cúrcuma-Piperina (Ratio 1:10)
    has_curcumin = any("cúrcuma" in b or "curcuma" in b for b in bom_items) or "cúrcuma" in title_lower or "curcuma" in title_lower
    if has_curcumin:
        has_pepper = any("pimienta" in b or "piperina" in b for b in bom_items) or "pimienta" in steps_text or "piperina" in steps_text
        if not has_pepper:
            return False, f"RECETA RECHAZADA SSOT V36.6 REV3: '{recipe.title}' contiene Cúrcuma pero carece de Pimienta Negra / Piperina para activación trofológica."

    # 7.20. SSOT V36.6 REV3: Mandato Matutino de Huevo y Exclusión de Carnes Rojas Pesadas
    if is_desayuno and (course_role in ["main", "Plato Principal"] or "principal" in title_lower or "desayuno" in title_lower):
        has_egg = any(e in title_lower for e in ["huevo", "huevos", "clara", "claras", "yema", "yemas", "omelette", "tamagoyaki", "chawanmushi", "çılbır", "cilbir"]) or any(e in item for item in bom_items for e in ["huevo", "huevos", "clara", "claras", "yema", "yemas"])
        if not has_egg:
            return False, f"RECETA RECHAZADA SSOT V36.6 REV3: Desayuno '{recipe.title}' no incluye Huevo Orgánico de Pastoreo como matriz proteica."
        
        forbidden_heavy_beef = ["ribeye", "sirloin", "arrachera", "corte de res", "bistec", "bisteck", "lomo de res"]
        for heavy in forbidden_heavy_beef:
            if re.search(r'\b' + heavy + r'\b', title_lower):
                return False, f"RECETA RECHAZADA SSOT V36.6 REV3: Desayuno '{recipe.title}' contiene corte pesado de res ('{heavy}')."

    # 7.21. SSOT V36.6 REV3: Pureza BOM 3D (Prohibición de Adjetivaciones Culinarias en Inventario)
    forbidden_bom_adjectives = ["jugoso", "jugosa", "marinado", "marinada", "dorado", "dorada", "fresco a la parrilla", "fresca a la plancha", "crujiente"]
    for b_item in bom_items:
        for adj in forbidden_bom_adjectives:
            if adj in b_item:
                return False, f"RECETA RECHAZADA SSOT V36.6 REV3: Pureza BOM violada. Ítem en inventario '{b_item}' contiene adjetivación culinaria '{adj}'."

    return True, "OK"


GENERIC_DISH_STOPWORDS = {
    "de", "la", "el", "los", "las", "con", "y", "en", "al", "a", "del", "para", "por", "un", "una",
    "fresco", "fresca", "frescos", "frescas", "granja", "herami", "33plus", "34plus", "33", "34", "plus",
    "artesanal", "orgánico", "orgánica", "orgánicos", "orgánicas", "viva", "vivos", "puro", "pura",
    "rústico", "rústica", "gourmet", "suave", "suaves", "estilo", "supremo", "seleccionado", "seleccionada"
}


def calculate_token_similarity(text1: str, text2: str) -> float:
    """Calcula similitud Jaccard de tokens significativos entre dos títulos de platillos."""
    t1 = set(w.lower() for w in re.findall(r'\w+', strip_accents(text1)) if w.lower() not in GENERIC_DISH_STOPWORDS and len(w) > 2)
    t2 = set(w.lower() for w in re.findall(r'\w+', strip_accents(text2)) if w.lower() not in GENERIC_DISH_STOPWORDS and len(w) > 2)
    if not t1 or not t2:
        return 0.0
    intersection = t1.intersection(t2)
    union = t1.union(t2)
    return len(intersection) / len(union)


def validate_consecutive_day_rotations(plan_days: list) -> Tuple[bool, str]:
    """
    Validación de ventana deslizante Día(N) vs Día(N-1) SSOT V36.2.0.
    Rechaza si platillos principales o acompañamientos de días contiguos superan el 80% de similitud.
    """
    for i in range(1, len(plan_days)):
        prev_day = plan_days[i-1]
        curr_day = plan_days[i]
        
        prev_meals = prev_day.get("meals", []) if isinstance(prev_day, dict) else getattr(prev_day, "meals", [])
        curr_meals = curr_day.get("meals", []) if isinstance(curr_day, dict) else getattr(curr_day, "meals", [])
        
        for p_meal in prev_meals:
            p_mtype = p_meal.get("meal_type")
            p_main = p_meal.get("main_dish_name", "")
            p_side = p_meal.get("side_dish_name", "")
            
            for c_meal in curr_meals:
                c_mtype = c_meal.get("meal_type")
                if p_mtype == c_mtype:
                    c_main = c_meal.get("main_dish_name", "")
                    c_side = c_meal.get("side_dish_name", "")
                    
                    if p_main and c_main:
                        sim_main = calculate_token_similarity(p_main, c_main)
                        if sim_main > 0.8:
                            return False, f"ABERRACIÓN DE ROTACIÓN SSOT V36.2.0: Plato Principal en {c_mtype} del {curr_day.get('day')} ('{c_main}') supera 80% de similitud con el día previo ({prev_day.get('day')}: '{p_main}')."
                    
                    if p_side and c_side:
                        sim_side = calculate_token_similarity(p_side, c_side)
                        if sim_side > 0.8:
                            return False, f"ABERRACIÓN DE ROTACIÓN SSOT V36.2.0: Acompañamiento en {c_mtype} del {curr_day.get('day')} ('{c_side}') supera 80% de similitud con el día previo ({prev_day.get('day')}: '{p_side}')."
    return True, "OK"








