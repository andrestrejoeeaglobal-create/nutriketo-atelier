import sqlite3
import re
from typing import List, Dict, Any, Optional
from app.database import get_db
from app.logger import logger
from app.schemas import ShoppingCheckItem, WeeklyMenuPlan, PantryItem, InventoryIntakeRequest, InventoryIntakeResponse

# Lista Base de Compras Consolidada (Semana 33) calculada para 6 comensales base
RAW_SHOPPING_ITEMS_BASE = [
    # 🌾 Cosecha Directa de la Granja / Huerto
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Espinacas frescas", "base_qty": 10.0, "unit": "manojos grandes"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Calabacitas verdes tiernas", "base_qty": 3.5, "unit": "kg"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Brócoli fresco", "base_qty": 4.0, "unit": "cabezas grandes"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Espárragos verdes", "base_qty": 3.0, "unit": "manojos"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Nopales tiernos", "base_qty": 15.0, "unit": "piezas"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Ejotes frescos", "base_qty": 1.5, "unit": "kg"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Cilantro fresco", "base_qty": 3.0, "unit": "manojos"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Arúgula fresca", "base_qty": 3.0, "unit": "manojos"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Higos frescos", "base_qty": 1.5, "unit": "kg"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Pitayas frescas", "base_qty": 1.0, "unit": "kg"},
    {"category": "🌾 Cosecha Directa de la Granja / Huerto", "item_name": "Granadas frescas", "base_qty": 6.0, "unit": "piezas"},

    # 🥩 Carnes, Pescados y Proteínas
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Huevos enteros", "base_qty": 8.0, "unit": "casilleros"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Claras de huevo", "base_qty": 2.0, "unit": "litros"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Pechuga de pollo", "base_qty": 3.2, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Pollo entero para caldo", "base_qty": 2.5, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Carne molida de Sirloin", "base_qty": 2.0, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Filete de res magro", "base_qty": 1.5, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Carne para caldo rico (costilla — tuétano)", "base_qty": 3.0, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Filete de pescado blanco", "base_qty": 1.2, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Filete de salmón fresco", "base_qty": 1.2, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Pechuga de pavo", "base_qty": 1.2, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Jamón de pavo en cubos", "base_qty": 1.0, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Tocino de pavo crujiente", "base_qty": 1.0, "unit": "kg"},
    {"category": "🥩 Carnes, Pescados y Proteínas", "item_name": "Lomo de atún fresco", "base_qty": 1.2, "unit": "kg"},

    # 🧀 Lácteos y Quesos (Sin Gluten / Keto)
    {"category": "🧀 Lácteos y Quesos (Sin Gluten / Keto)", "item_name": "Queso crema", "base_qty": 1.2, "unit": "kg"},
    {"category": "🧀 Lácteos y Quesos (Sin Gluten / Keto)", "item_name": "Queso Panela", "base_qty": 1.0, "unit": "kg"},
    {"category": "🧀 Lácteos y Quesos (Sin Gluten / Keto)", "item_name": "Queso Gouda", "base_qty": 1.5, "unit": "kg"},
    {"category": "🧀 Lácteos y Quesos (Sin Gluten / Keto)", "item_name": "Queso Parmesano", "base_qty": 400.0, "unit": "g"},
    {"category": "🧀 Lácteos y Quesos (Sin Gluten / Keto)", "item_name": "Mantequilla de vaca (sin sal)", "base_qty": 900.0, "unit": "g"},
    {"category": "🧀 Lácteos y Quesos (Sin Gluten / Keto)", "item_name": "Crema entera — para batir", "base_qty": 1.0, "unit": "litro"},

    # 🥬 Verduras, Hortalizas y Frescos
    {"category": "🥬 Verduras, Hortalizas y Frescos", "item_name": "Aguacates Hass medianos", "base_qty": 24.0, "unit": "piezas"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "item_name": "Jitomate Bola — Saladette", "base_qty": 3.5, "unit": "kg"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "item_name": "Cebolla blanca", "base_qty": 2.0, "unit": "kg"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "item_name": "Limones frescos", "base_qty": 2.0, "unit": "kg"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "item_name": "Champiñones Portobello", "base_qty": 12.0, "unit": "piezas"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "item_name": "Dientes de ajo", "base_qty": 3.0, "unit": "cabezas"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "item_name": "Apio fresco", "base_qty": 1.0, "unit": "manojo"},
    {"category": "🥬 Verduras, Hortalizas y Frescos", "item_name": "Fresas frescas", "base_qty": 500.0, "unit": "g"},

    # 🛒 Abarrotes, Semillas y Grasas
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Semillas de chía", "base_qty": 400.0, "unit": "g"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Leche de coco (sin azúcar)", "base_qty": 3.0, "unit": "latas"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Nueces pecana", "base_qty": 400.0, "unit": "g"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Almendras enteras", "base_qty": 400.0, "unit": "g"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Harina de almendras (Keto)", "base_qty": 1.0, "unit": "kg"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Multi Sinergix (Fórmula Energética & Mitocondrial)", "base_qty": 14.0, "unit": "dosis completas"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Amino Sinergix (Fórmula Nocturna & Péptidos)", "base_qty": 14.0, "unit": "dosis completas"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Aceite de coco (orgánico)", "base_qty": 1.0, "unit": "frasco (1 kg)"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Aceite de oliva virgen extra", "base_qty": 2.0, "unit": "litros"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Vinagre de manzana (orgánico)", "base_qty": 1.0, "unit": "frasco"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Vinagre balsámico (orgánico — keto)", "base_qty": 1.0, "unit": "frasco"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Alcaparras en salmuera", "base_qty": 1.0, "unit": "frasco"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Aceitunas deshuesadas", "base_qty": 1.0, "unit": "frasco"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Mostaza Dijon — Tipo Antigua", "base_qty": 1.0, "unit": "frasco"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Salsa Tamari — Soya Keto", "base_qty": 1.0, "unit": "frasco"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Queso de cabra artesanal", "base_qty": 400.0, "unit": "g"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Nuez de la India — Macadamias", "base_qty": 400.0, "unit": "g"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Mayonesa casera — keto", "base_qty": 1.0, "unit": "frasco"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Té verde", "base_qty": 1.0, "unit": "paquete"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Té de hierbas", "base_qty": 1.0, "unit": "paquete"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Café en grano — molido", "base_qty": 1.0, "unit": "paquete"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Hierbas secas (Orégano — Tomillo)", "base_qty": 1.0, "unit": "frasco"},
    {"category": "🛒 Abarrotes, Semillas y Grasas", "item_name": "Sal de mar", "base_qty": 1.0, "unit": "frasco"}
]

import unicodedata

INGREDIENT_CANONICAL_MAP = {
    "calabacita-fresca": ["calabacita", "calabacitas", "zucchini", "zoodles", "zoodles de calabacita", "bastones de zucchini"],
    "coliflor-fresca": ["coliflor", "floretes de coliflor", "coliflor rostizada"],
    "espinaca-fresca": ["espinaca", "espinacas", "espinaca baby", "espinacas baby"],
    "esparrago-fresco": ["espárrago", "esparrago", "espárragos", "esparragos"],
    "aceite-oliva": ["aceite de oliva", "aceite de oliva extra virgen", "aceite vevo", "aceite de oliva extra virgen vevo", "aceite de oliva virgen extra"],
    "te-verde": ["té verde", "te verde", "té verde orgánico", "matcha"],
    "huevo-organico": ["huevo", "huevos", "huevos frescos", "huevos orgánicos", "huevos frescos orgánicos", "huevos frescos orgánicos de pastoreo", "huevos enteros"],
    "pechuga-pavo": ["pechuga de pavo", "pavo artesanal", "pechuga de pavo artesanal", "jamón de pavo", "tocino de pavo"],
    "pechuga-pollo": ["pechuga de pollo", "pollo fresco", "pechuga de pollo fresca", "muslos de pollo"],
    "sirloin-magro": ["carne molida de sirloin", "sirloin magro", "carne molida de sirloin magra"],
    "filete-res": ["filete de res", "filete de res magro", "ribeye", "sirloin", "medallones de mignon"],
    "huachinango-fresco": ["huachinango", "filete de huachinango", "filete de huachinango fresco", "filete de huachinango al horno"],
    "robalo-fresco": ["róbalo", "robalo", "filete de róbalo", "filete de robalo fresco", "filete de róbalo a la plancha"],
    "salmon-salvaje": ["salmón", "salmon", "salmón salvaje", "filete de salmón fresco", "filete de salmón salvaje", "filete de salmón fresco con piel"],
    "pescado-blanco": ["pescado blanco", "filete de pescado blanco", "filete de pescado blanco fresco"],
    "atun-fresco": ["atún", "atun", "filete de atún fresco"],
    "queso-parmesano": ["queso parmesano", "parmesano maduro", "queso parmesano maduro"],
    "queso-manchego": ["queso manchego", "manchego maduro", "queso manchego maduro"],
    "queso-gouda": ["queso gouda", "gouda maduro", "queso gouda maduro"],
    "queso-panela": ["queso panela", "panela fresco", "queso panela fresco"],
    "queso-cabra": ["queso de cabra", "cabra artesanal", "queso de cabra artesanal"],
    "queso-crema": ["queso crema", "queso crema artesanal"],
    "mantequilla-pastoreo": ["mantequilla", "mantequilla de vaca", "mantequilla de pastoreo", "mantequilla sin sal"],
    "jitomate-bola": ["jitomate", "jitomates", "jitomate bola", "jitomate bola jugoso"],
    "33plus": ["33plus", "33 plus", "fórmula 33plus", "elixir 33plus"],
    "34plus": ["34plus", "34 plus", "fórmula 34plus", "tisana 34plus"]
}

def strip_accents(text: str) -> str:
    if not text:
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def validate_physical_state_invariant(canonical_id: str, physical_state: str, unit: str, existing_items: dict) -> None:
    """
    INVARIANTE DE ESTADO FÍSICO:
    Garantiza que ningún canonical_id mezcle estados físicos (solid vs liquid vs unit) o unidades incompatibles.
    """
    if canonical_id in existing_items:
        existing = existing_items[canonical_id]
        if existing['physical_state'] != physical_state:
            raise ValueError(
                f"🚨 INVARIANTE VIOLADA: Ingrediente '{canonical_id}' declara estado físico '{physical_state}' "
                f"pero ya existe como '{existing['physical_state']}'."
            )
        # Unit dimension compatibility check
        solid_units = {'g', 'kg', 'mg'}
        liquid_units = {'ml', 'l', 'lt', 'litro', 'litros'}
        unit_clean = unit.strip().lower()
        exist_unit_clean = existing['unit'].strip().lower()
        
        if (unit_clean in solid_units and exist_unit_clean in liquid_units) or \
           (unit_clean in liquid_units and exist_unit_clean in solid_units):
            raise ValueError(
                f"🚨 INVARIANTE VIOLADA: Unidades incompatibles para '{canonical_id}': '{unit}' vs '{existing['unit']}'."
            )

def format_cooking_step(step_text: str, protein_family: Optional[str] = None) -> str:
    """
    INYECCIÓN ALGORÍTMICA DETERMINISTA DE TEMPERATURA DE INOCUIDAD:
    Deduce la temperatura objetivo según la familia de proteína.
    """
    if not protein_family or protein_family == 'none':
        return step_text

    pf = protein_family.lower()
    if pf in ['poultry', 'turkey', 'chicken', 'pavo', 'pollo']:
        target_clause = " Cocinar hasta alcanzar una temperatura interna crítica mínima de 74°C en el centro térmico de la pieza antes del reposo y servicio."
        if "74°C" not in step_text and "74 °C" not in step_text:
            return step_text + target_clause
    elif pf in ['bovine', 'res', 'sirloin', 'mignon', 'ribeye']:
        target_clause = " Asegurar una temperatura interna de servicio de 68°C a 72°C en el centro térmico."
        if "68°C" not in step_text and "72°C" not in step_text:
            return step_text + target_clause
    elif pf in ['fish', 'pescado', 'huachinango', 'robalo', 'salmon', 'salmón']:
        target_clause = " Mantener una temperatura interna de cocción de 63°C a 68°C."
        if "63°C" not in step_text and "68°C" not in step_text:
            return step_text + target_clause

    return step_text

def normalize_to_canonical_slug(raw_name: str) -> str:
    if not raw_name:
        return ""
    clean = raw_name.strip().lower()
    clean_no_acc = strip_accents(clean)
    
    for slug, aliases in INGREDIENT_CANONICAL_MAP.items():
        for alias in aliases:
            alias_clean = strip_accents(alias.strip().lower())
            if alias_clean in clean_no_acc or clean_no_acc in alias_clean:
                return slug
                
    sanitized = re.sub(r'[^a-z0-9\s-]', '', clean_no_acc)
    sanitized = re.sub(r'\s+', '-', sanitized).strip('-')
    return sanitized


class InventorySyncMaster:

    @staticmethod
    def format_scaled_qty(base_qty: float, unit: str, diners_count: int) -> str:
        factor = diners_count / 6.0
        scaled_val = round(base_qty * factor, 2)
        if scaled_val.is_integer():
            val_str = str(int(scaled_val))
        else:
            val_str = f"{scaled_val:.1f}"

        return f"{val_str} {unit}"

    @staticmethod
    def categorize_ingredient_name(name: str) -> str:
        slug = normalize_to_canonical_slug(name)
        name_lower = name.lower()
        if slug in ["33plus", "34plus"] or any(k in name_lower for k in ["33plus", "34plus", "grenetina", "colágeno", "colageno"]):
            return "💊 SUPLEMENTACIÓN CELULAR / BIOTECNOLOGÍA"
        if re.search(r'\b(huevo|huevos|clara|claras|pollo|sirloin|res|mignon|ribeye|pescado|salmón|salmon|pavo|machaca|jamón|jamon|tocino|atún|atun|huachinango|robalo|róbalo)\b', name_lower):
            return "🥩 Carnes, Pescados y Proteínas"
        if any(k in name_lower for k in ["fresa", "frambuesa", "mora", "arándano", "arandano", "pitahaya", "pitaya", "higo", "granada", "arilos", "durazno"]):
            return "🍓 Frutas de Bajo Índice Glucémico"
        if any(k in name_lower for k in ["queso", "mantequilla", "ghee", "crema"]):
            return "🧀 Lácteos y Quesos (Sin Gluten / Keto)"
        if any(k in name_lower for k in ["romero", "orégano", "oregano", "tomillo", "pimienta", "sal", "vinagre", "adobo", "tajín", "tajin", "hierbas", "especias", "condimento", "albahaca", "laurel", "epazote", "mostaza", "comino", "pimentón", "pimenton", "eneldo", "salvia", "canela", "cúrcuma", "curcuma", "té", "te", "matcha", "jamaica", "toronjil", "manzanilla", "menta", "infusión", "infusion", "tisana", "elixir", "caldo", "azahar"]):
            return "🌶️ Chiles, Condimentos e Infusiones"
        if any(k in name_lower for k in ["calabacita", "zoodles", "zucchini", "espárrago", "esparrago", "nopal", "chayote", "coliflor", "espinaca", "arúgula", "arugula", "flor de calabaza", "champiñón", "champinon", "portobello", "jitomate", "cebolla", "ajo", "pepino", "apio", "hinojo", "pimiento", "aguacate", "limón", "limon", "ejote"]):
            return "🥬 Verduras, Hortalizas y Frescos"
        return "🛒 Abarrotes, Semillas y Grasas"

    @staticmethod
    def sync_shopping_list(plan: WeeklyMenuPlan) -> None:
        InventorySyncMaster.seed_consolidated_shopping_list(diners_count=plan.diners_count, plan=plan)

    @staticmethod
    def seed_shopping_list_from_plan(plan: WeeklyMenuPlan) -> None:
        InventorySyncMaster.seed_consolidated_shopping_list(diners_count=plan.diners_count, plan=plan)

    @staticmethod
    def seed_consolidated_shopping_list(diners_count: int = 6, plan: Optional[WeeklyMenuPlan] = None) -> None:
        try:
            items_to_sync = [it for it in RAW_SHOPPING_ITEMS_BASE if "california" not in it["item_name"].lower()]
            if plan and hasattr(plan, 'days'):
                extracted_names = set(item["item_name"].lower() for item in items_to_sync)
                for day in plan.days:
                    for meal in day.meals:
                        for ing in getattr(meal, 'ingredients', []):
                            ing_name = ing.name.strip()
                            if ing_name.lower() not in extracted_names and "california" not in ing_name.lower():
                                cat = InventorySyncMaster.categorize_ingredient_name(ing_name)
                                items_to_sync.append({
                                    "category": cat,
                                    "item_name": ing_name,
                                    "base_qty": getattr(ing, 'quantity', 1.0),
                                    "unit": getattr(ing, 'unit', 'g')
                                })
                                extracted_names.add(ing_name.lower())

            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, item_name FROM shopping_list_items")
                existing = {row["item_name"]: row["id"] for row in cursor.fetchall()}

                if not existing:
                    for item in items_to_sync:
                        qty_str = InventorySyncMaster.format_scaled_qty(item["base_qty"], item["unit"], diners_count)
                        cursor.execute(
                            "INSERT INTO shopping_list_items (category, day, item_name, quantity, unit, is_checked) VALUES (?, ?, ?, ?, ?, 0)",
                            (item["category"], f"Semana 33 ({diners_count} comensales)", item["item_name"], item["base_qty"] * (diners_count / 6.0), qty_str)
                        )
                else:
                    for item in items_to_sync:
                        qty_str = InventorySyncMaster.format_scaled_qty(item["base_qty"], item["unit"], diners_count)
                        scaled_qty = item["base_qty"] * (diners_count / 6.0)
                        if item["item_name"] in existing:
                            cursor.execute(
                                "UPDATE shopping_list_items SET day = ?, quantity = ?, unit = ? WHERE item_name = ?",
                                (f"Semana 33 ({diners_count} comensales)", scaled_qty, qty_str, item["item_name"])
                            )
                        else:
                            cursor.execute(
                                "INSERT INTO shopping_list_items (category, day, item_name, quantity, unit, is_checked) VALUES (?, ?, ?, ?, ?, 0)",
                                (item["category"], f"Semana 33 ({diners_count} comensales)", item["item_name"], scaled_qty, qty_str)
                            )
            logger.info(f"InventorySyncMaster: Lista de Compras Semana 33 actualizada dinámicamente ({diners_count} comensales).")
        except Exception as e:
            logger.error(f"Error al sembrar/actualizar lista de compras Semana 33: {e}")

    @staticmethod
    def get_shopping_list_items(day: Optional[str] = None, day_filter: Optional[str] = None, diners_count: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            if diners_count is not None:
                InventorySyncMaster.seed_consolidated_shopping_list(diners_count=diners_count)
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, category, day, item_name, quantity, unit, is_checked FROM shopping_list_items ORDER BY id ASC")
                rows = cursor.fetchall()
                return [
                    {
                        "id": row["id"],
                        "category": row["category"] or "General",
                        "day": row["day"],
                        "item_name": row["item_name"],
                        "quantity_str": row["unit"],
                        "quantity": row["quantity"],
                        "unit": row["unit"],
                        "is_checked": bool(row["is_checked"])
                    } for row in rows
                ]
        except Exception as e:
            logger.error(f"Error al obtener lista de compras: {e}")
            return []

    @staticmethod
    def toggle_shopping_item(item_id: int, is_checked: bool) -> bool:
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE shopping_list_items SET is_checked = ? WHERE id = ?",
                    (1 if is_checked else 0, item_id)
                )
            return True
        except Exception as e:
            logger.error(f"Error al actualizar checkbox {item_id}: {e}")
            return False

    @staticmethod
    def sync_served_dish(dish_name: str, ingredients: List[Dict[str, Any]]) -> None:
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                for ing in ingredients:
                    cursor.execute(
                        "INSERT INTO inventory_transactions (transaction_type, item_name, quantity, unit, notes) VALUES (?, ?, ?, ?, ?)",
                        ("DEDUCTION_DISH_SERVED", ing.get("name"), ing.get("quantity"), ing.get("unit"), f"Servido: {dish_name}")
                    )
            logger.info(f"InventorySyncMaster: Descontados ingredientes del platillo servido '{dish_name}'.")
        except Exception as e:
            logger.error(f"Error al descontar platillo servido: {e}")

    @staticmethod
    def get_all_pantry_items() -> List[PantryItem]:
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, item_name, quantity, unit, updated_at FROM pantry_inventory ORDER BY item_name ASC")
                rows = cursor.fetchall()
                return [
                    PantryItem(
                        id=row["id"],
                        item_name=row["item_name"],
                        quantity=row["quantity"],
                        unit=row["unit"],
                        updated_at=str(row["updated_at"]) if row["updated_at"] else ""
                    ) for row in rows
                ]
        except Exception as e:
            logger.error(f"Error al obtener alacena: {e}")
            return []

    @staticmethod
    def register_inventory_intake(req: InventoryIntakeRequest) -> InventoryIntakeResponse:
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT quantity FROM pantry_inventory WHERE item_name = ?", (req.item_name,))
                row = cursor.fetchone()
                
                if row:
                    new_qty = row["quantity"] + req.quantity
                    cursor.execute(
                        "UPDATE pantry_inventory SET quantity = ?, unit = ?, updated_at = CURRENT_TIMESTAMP WHERE item_name = ?",
                        (new_qty, req.unit, req.item_name)
                    )
                else:
                    new_qty = req.quantity
                    cursor.execute(
                        "INSERT INTO pantry_inventory (item_name, quantity, unit) VALUES (?, ?, ?)",
                        (req.item_name, new_qty, req.unit)
                    )

                notes_detail = f"Fuente: {req.source_type} | Destino: {req.storage_destination} | Fecha: {req.intake_date or 'N/A'}. {req.batch_notes or ''}"
                cursor.execute(
                    "INSERT INTO inventory_transactions (transaction_type, item_name, quantity, unit, notes) VALUES (?, ?, ?, ?, ?)",
                    ("INGRESO_INVENTARIO", req.item_name, req.quantity, req.unit, notes_detail)
                )

            logger.info(f"InventorySyncMaster: Ingreso de trazabilidad registrado exitosamente '{req.item_name}' +{req.quantity} {req.unit} -> {req.storage_destination} (Total: {new_qty}).")
            return InventoryIntakeResponse(
                success=True,
                message=f"📦 Abastecimiento consolidado: +{req.quantity} {req.unit} de '{req.item_name}' asignados a {req.storage_destination}.",
                updated_item_name=req.item_name,
                new_total_quantity=new_qty,
                unit=req.unit,
                storage_destination=req.storage_destination
            )
        except Exception as e:
            logger.error(f"Error al registrar ingreso de inventario: {e}")
            return InventoryIntakeResponse(
                success=False,
                message=f"Error al registrar ingreso: {str(e)}",
                updated_item_name=req.item_name,
                new_total_quantity=0.0,
                unit=req.unit,
                storage_destination=req.storage_destination
            )

    @staticmethod
    def get_smart_item_category(item_name: str, explicit_category: str = "") -> str:
        if explicit_category and "Cosecha" in explicit_category:
            return "🌾 Cosecha Directa de la Granja / Huerto"
        
        name = (item_name or "").lower()

        def has_word(text: str, kw_list: List[str]) -> bool:
            for kw in kw_list:
                pattern = r"(?:^|\s|[^a-záéíóúñ])" + re.escape(kw) + r"(?:$|\s|[^a-záéíóúñ])"
                if re.search(pattern, text, re.IGNORECASE):
                    return True
            return False

        dairy_keywords = ["queso", "quesos", "leche", "mantequilla", "crema", "cottage", "gouda", "panela", "parmesano", "manchego", "mascarpone", "oaxaca", "mozzarella", "requezon", "requeron", "requesón", "ghee", "suero", "asadero", "chihuahua", "brie", "camembert", "feta", "provolone", "ricotta", "chèvre", "chevre"]
        if has_word(name, dairy_keywords):
            return "🧀 Lácteos y Quesos (Sin Gluten / Keto)"

        protein_keywords = ["carne", "carnes", "sirloin", "ribeye", "res", "pollo", "pollos", "pechuga", "pechugas", "pavo", "pavos", "tocino", "jamón", "jamon", "jamones", "pescado", "pescados", "salmón", "salmon", "atún", "atun", "atunes", "huevo", "huevos", "clara", "claras", "lomo", "lomos", "medallón", "medallon", "medallones", "albóndiga", "albondiga", "albóndigas", "albondigas", "costilla", "costillas", "tuétano", "tuetano", "arrachera", "arracheras", "bistec", "bisteck", "milanesa", "milanesas", "cecina", "chorizo", "longaniza"]
        if has_word(name, protein_keywords):
            return "🥩 Carnes, Pescados y Proteínas"

        spice_keywords = ["chile", "chiles", "jalapeño", "jalapeños", "jalapeno", "jalapenos", "rajas", "habanero", "habaneros", "serrano", "serranos", "poblano", "poblanos", "chipotle", "chipotles", "pasilla", "ancho", "guajillo", "tajín", "tajin", "chamoy", "pimienta", "orégano", "oregano", "tomillo", "laurel", "canela", "vainilla", "clavo", "clavos", "comino", "cúrcuma", "curcuma", "paprika", "pimentón", "pimenton", "epazote", "albahaca", "romero", "mostaza", "alcaparra", "alcaparras", "aceituna", "aceitunas", "sal", "salsa", "tamari", "soya", "vinagre", "balsámico", "balsamico", "adobo", "sazonador", "hierbas", "especias", "condimento", "condimentos"]
        if has_word(name, spice_keywords):
            return "🌶️ Chiles, Condimentos y Especias"

        veggie_keywords = ["espinaca", "espinacas", "calabacita", "calabacitas", "brócoli", "brocoli", "espárrago", "esparrago", "espárragos", "esparragos", "nopal", "nopales", "ejote", "ejotes", "cilantro", "arúgula", "arugula", "higo", "higos", "pitaya", "pitayas", "durazno", "duraznos", "granada", "granadas", "aguacate", "aguacates", "jitomate", "jitomates", "cebolla", "cebollas", "limón", "limon", "limones", "champiñón", "champiñones", "champiñon", "portobello", "portobellos", "ajo", "ajos", "apio", "apios", "fresa", "fresas", "pepino", "pepinos", "chayote", "chayotes", "zanahoria", "zanahorias", "papa", "papas", "lechuga", "lechugas", "verdura", "verduras", "hortaliza", "hortalizas", "coliflor", "coliflores", "betabel", "pimiento", "pimientos"]
        if has_word(name, veggie_keywords):
            return "🥬 Verduras, Hortalizas y Frescos"

        supp_keywords = ["sinergix", "suplemento", "suplementos", "vitamina", "vitaminas", "colágeno", "colageno", "electrolitos"]
        if has_word(name, supp_keywords):
            return "💊 Suplementación y Fórmulas Sinergix"

        if explicit_category and explicit_category.strip():
            return explicit_category
        return "🛒 Abarrotes, Semillas y Grasas"



