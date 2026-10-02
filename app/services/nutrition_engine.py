"""
Módulo Canónico de Nutrición, Factor Atwater y Fibra Botánica (SSOT V36.6)
NutriKeto Atelier T.I.L.O.® — Arquitectura Bioquímica

Garantiza:
1. Cálculo Atwater exacto y determinista: Kcal = (G * 9) + (P * 4) + (NetCarbs * 4).
2. Definición estricta: Carbohidratos Netos = Carbohidratos Totales - Fibra Dietética.
   La fibra prebiótica nunca se computa como energía calórica disponible en cetosis.
3. Catálogo de densidad botánica de fibra por cada 100g para erradicar fallbacks sintéticos.
4. Motor clínico circadiano y ontología biológica inmune a colisiones léxicas (ej. 'res' in 'fresco').
"""

import re
import math
import unicodedata
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("nutriketo.nutrition_engine")

def strip_accents(text: str) -> str:
    """Preprocesamiento canónico que elimina tildes y caracteres diacríticos."""
    if not text:
        return ""
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8').lower()


# =============================================================================
# 1. CÁLCULO ATWATER ESTANDARIZADO
# =============================================================================

def compute_atwater_kcal(fat_g: float, protein_g: float, net_carbs_g: float) -> int:
    """Calcula las calorías según el sistema de factores específicos de Atwater.
    Multiplica estrictamente carbohidratos netos (excluyendo la fibra insoluble).
    """
    return round((float(fat_g) * 9.0) + (float(protein_g) * 4.0) + (float(net_carbs_g) * 4.0))


# =============================================================================
# 2. CATÁLOGO DE DENSIDAD DE FIBRA BOTÁNICA POR 100g
# =============================================================================

BOTANICAL_FIBER_DENSITY_PER_100G = {
    # Semillas y Frutos Secos
    "chía": 34.4,
    "chia": 34.4,
    "linaza": 27.3,
    "coco": 16.3,
    "almendra": 12.5,
    "sésamo": 11.8,
    "sesamo": 11.8,
    "ajonjolí": 11.8,
    "ajonjoli": 11.8,
    "pecana": 9.6,
    "girasol": 8.6,
    "castilla": 6.7,
    "nuez": 6.7,
    "macadamia": 8.6,

    # Frutas Cetogénicas (Bajo Índice Glucémico)
    "frambuesa": 6.5,
    "mora": 5.3,
    "zarzamora": 5.3,
    "granada": 4.0,
    "arilos": 4.0,
    "pitaya": 2.9,
    "pitahaya": 2.9,
    "arándano": 2.4,
    "arandano": 2.4,
    "fresa": 2.0,

    # Hortalizas y Verduras Frescas
    "aguacate": 6.7,
    "hinojo": 3.1,
    "ejote": 2.7,
    "arúgula": 2.6,
    "arugula": 2.6,
    "arándano": 2.4,
    "espinaca": 2.2,
    "nopal": 2.2,
    "nopales": 2.2,
    "espárrago": 2.1,
    "esparrago": 2.1,
    "coliflor": 2.0,
    "chayote": 1.7,
    "apio": 1.6,
    "flor de calabaza": 1.5,
    "portobello": 1.5,
    "champiñón": 1.5,
    "champinon": 1.5,
    "lechuga": 1.3,
    "tomate": 1.2,
    "jitomate": 1.2,
    "calabacita": 1.0,
    "zucchini": 1.0,
    "pepino": 0.5
}


ZERO_FIBER_ANIMAL_OR_FAT_PATTERN = re.compile(
    r'\b(aceite|mantequilla|ghee|grasa|manteca|vevo|salmon|atun|robalo|huachinango|pescado|'
    r'pollo|pavo|pechuga|muslo|sirloin|arrachera|machaca|res|carne|tuetano|hueso|huesos|'
    r'retazo|huevo|huevos|clara|claras|yema|yemas|tocino|jamon|panceta|queso|parmesano|'
    r'gouda|manchego|panela|cabra|crema|yogur|agua|sal de mar|sal marina|sal mineral|colageno|grenetina|gelatina)\b',
    re.IGNORECASE
)


def calculate_ingredient_fiber_g(item_name: str, qty_g: float) -> float:
    """Calcula la fibra dietética real de un insumo botánico en gramos según su masa.
    Cualquier ingrediente animal o graso puro se resuelve explícitamente como 0.0 g/100g.
    """
    if not item_name or qty_g <= 0:
        return 0.0
    clean_name = strip_accents(item_name)

    # Salvaguarda Cero-Fibra: Insumos animales o grasas puras son estrictamente 0.0 g/100g
    if ZERO_FIBER_ANIMAL_OR_FAT_PATTERN.search(clean_name):
        return 0.0

    # Salvaguarda 2: Catálogo de densidad botánica
    for key, density in BOTANICAL_FIBER_DENSITY_PER_100G.items():
        clean_key = strip_accents(key)
        if clean_key in clean_name:
            return round((qty_g * density) / 100.0, 2)

    # Advertencia de log solo si el insumo botánico no está registrado
    logger.warning("Insumo botánico no registrado en BOTANICAL_FIBER_DENSITY: '%s'", item_name)
    return 0.0


def calculate_dish_fiber_g(ingredients: List[Dict[str, Any]], diners: int = 6) -> float:
    """Calcula la fibra dietética total por comensal de un platillo a partir de sus ingredientes."""
    if not ingredients:
        return 0.0
    total_fiber_batch = 0.0
    for ing in ingredients:
        name = ing.get("name") or ing.get("item_name", "")
        # Gramaje por persona o total
        if "base_qty_per_person" in ing:
            qty_g = float(ing["base_qty_per_person"])
            total_fiber_batch += calculate_ingredient_fiber_g(name, qty_g) * diners
        else:
            qty = float(ing.get("amount") or ing.get("quantity") or ing.get("base_qty", 0.0))
            unit = str(ing.get("unit", "g")).lower()
            if "kg" in unit:
                qty *= 1000.0
            elif "piezas" in unit or "pz" in unit:
                if "aguacate" in name.lower():
                    qty *= 150.0  # ~150g pulpa comestible por pieza
                elif "portobello" in name.lower():
                    qty *= 80.0
                elif "limon" in name.lower():
                    qty *= 20.0
                else:
                    qty *= 50.0
            total_fiber_batch += calculate_ingredient_fiber_g(name, qty)
    return round(total_fiber_batch / float(diners), 1)


# =============================================================================
# 3. ONTO-TAXONOMÍA BIOLÓGICA & LÍMITES LÉXICOS ESTRICTOS (SALVAGUARDAS A, B, C)
# =============================================================================

SPECIES_PATTERNS = [
    # 1. Especies Marinas Pelágicas (Omega-3 / EPA-DHA)
    ("marine_pelagic", re.compile(r'\b(salmon|atun)\b', re.IGNORECASE)),
    # 2. Especies Marinas Blancas (Digestión rápida, minerales traza)
    ("marine_white", re.compile(r'\b(robalo|huachinango|pescado|pescado blanco)\b', re.IGNORECASE)),
    # 3. Aves (Proteína magra de alta digestibilidad - Salvaguarda C con límites léxicos estrictos)
    ("poultry", re.compile(r'\b(pollo|pollos|pavo|pavos|ave|aves|pechuga|pechugas)\b', re.IGNORECASE)),
    # 4. Bovinos de Pastoreo (Hierro hemo, zinc, creatina - Límite estricto \bres\b para evitar 'fresco' / 'fresca')
    ("bovine_red_meat", re.compile(r'\b(arrachera|sirloin|machaca|res|vacuno|tuetano)\b', re.IGNORECASE)),
    # 5. Ovoproductos (Leucina, colina, albumina)
    ("ovoproduct", re.compile(r'\b(huevo|huevos|clara|claras|yema|yemas|omelette|tamagoyaki|cazuela|benedictino|revuelt[oa]s?|estrellad[oa]s?)\b', re.IGNORECASE)),
    # 6. Fúngicos (Betaglucanos, umami)
    ("fungal", re.compile(r'\b(portobello|champinon|champinones|setas?)\b', re.IGNORECASE)),
]


def resolve_main_dish_species(dish_name: str) -> str:
    """Identifica la especie biológica primaria de un platillo con precedencia estricta.
    Fuerza preprocesamiento canónico con strip_accents() antes de evaluar los tokens.
    """
    if not dish_name:
        return "generic_protein"
    clean_dish = strip_accents(dish_name)
    for species_id, pattern in SPECIES_PATTERNS:
        if pattern.search(clean_dish):
            return species_id
    return "generic_protein"


# =============================================================================
# 4. MOTOR CLÍNICO CIRCADIANO (JUSTIFICACIONES SIN INVERSIÓN TEMPORAL)
# =============================================================================

def get_clinical_starter_justification(starter_name: str, meal_type: str) -> str:
    """Genera la justificación neuroendocrina de la entrada respetando el ciclo circadiano."""
    nl = (starter_name or "").lower()
    mtype = (meal_type or "").lower()

    if any(k in nl for k in ['mora', 'granada', 'fresa', 'arándano', 'arandano', 'frambuesa', 'pitaya', 'pitahaya', 'zarzamora']):
        return "Aporte de polifenoles vivos, antocianinas, fibra soluble prebiótica y micronutrientes que modulan la absorción de glucosa y acondicionan la mucosa gastrointestinal matutina."

    if any(k in nl for k in ['crema', 'consomé', 'caldo', 'fondo']):
        return "Emulsión velouté tibia rica en lípidos saludables y electrolitos que estimula la motilidad gástrica y optimiza la secreción de enzimas pancreáticas para el almuerzo."

    if "cena" in mtype:
        return "Aporte de lípidos monoinsaturados (ácido oleico) y agua biológica con electrolitos para una digestión liviana y máxima estabilidad glucémica previa al reposo nocturno."
    else:
        return "Carga botánica fresca rica en clorofila, agua estructurada y fibra prebiótica que estimula la digestión diurna sin sobrecarga metabólica."


def get_clinical_main_justification(main_name: str, meal_type: str) -> str:
    """Genera la justificación fisiológica del platillo fuerte basada en la especie biológica real
    y la fase circadiana del comensal.
    """
    species = resolve_main_dish_species(main_name)
    mtype = (meal_type or "").lower()

    if species == "ovoproduct":
        return "Activación obligatoria del umbral de leucina (≥ 2.5 g vía 3 huevos enteros de libre pastoreo) para encender la vía de síntesis proteica muscular (mTOR) y generar saciedad bifásica."

    if species == "bovine_red_meat":
        return "Densidad de hierro hemo de alta absorción, zinc elemental, creatina natural y proteína densa de pastoreo para anabolismo tisular diurno y preservación de masa magra."

    if species == "marine_pelagic":
        if "cena" in mtype:
            return "Proteína marina noble rica en ácidos grasos poliinsaturados Omega-3 (EPA/DHA) y selenio, de digestibilidad acelerada para un reposo fisiológico nocturno sin inflamación."
        else:
            return "Aporte de ácidos grasos Omega-3 de cadena larga (EPA/DHA), fósforo y proteína marina noble para enfoque cognitivo diurno y modulación cardiovascular."

    if species == "marine_white":
        if "cena" in mtype:
            return "Proteína blanca de captura salvaje con alta digestibilidad, bajo residuo gástrico y mínimo costo termogénico nocturno, facilitando la fase previa al sueño."
        else:
            return "Proteína marina magra de captura salvaje, rica en yodo y minerales traza oceánicos, ideal para una comida ligera que previene la somnolencia posprandial."

    if species == "poultry":
        if "cena" in mtype:
            return "Proteína magra de alta digestibilidad rica en L-triptófano y aminoácidos esenciales, favoreciendo la biosíntesis de serotonina y melatonina nocturna."
        else:
            return "Proteína magra de ave de libre pastoreo rica en aminoácidos de cadena ramificada, que sostiene el anabolismo muscular diurno sin enlentecer el vaciamiento gástrico."

    if species == "fungal":
        return "Aporte de betaglucanos fúngicos, glutamato natural de umami y matriz vegetal densa en fibra prebiótica con saciedad prolongada y soporte inmunológico."

    return "Suministro balanceado de aminoácidos esenciales para balance nitrogenado positivo y saciedad fisiológica dentro del protocolo cetogénico."


def get_clinical_side_justification(side_name: str, meal_type: str) -> str:
    """Genera la justificación del acompañamiento respetando adaptógenos y biorritmos circadianos."""
    nl = (side_name or "").lower()
    mtype = (meal_type or "").lower()

    if "33plus" in nl or "desayuno" in mtype:
        return "Soporte osteoarticular y de matriz conectiva vía 7g de colágeno hidrolizado puro, con activación mitocondrial y enfoque neurocognitivo mediante la Fórmula Nootrópica 33Plus®."

    if "34plus" in nl or "cena" in mtype or "tisana" in nl:
        return "Inducción circadiana del descanso fisiológico mediante fitonutrientes ansiolíticos naturales (modulación GABAérgica) y sustratos bioactivos reparadores de la Fórmula 34Plus®."

    if any(k in nl for k in ['espárragos', 'esparragos', 'ejotes', 'nopales', 'calabacitas', 'chayotes', 'zoodles']):
        return "Aporte de potasio intracelular y fibra prebiótica insoluble que optimiza la microbiota y el tránsito gastrointestinal sin impacto en la glucemia ni interrupción de la cetosis."

    return "Aporte de electrolitos esenciales y sustratos funcionales compatibles con el estado de cetosis nutricional profunda."
