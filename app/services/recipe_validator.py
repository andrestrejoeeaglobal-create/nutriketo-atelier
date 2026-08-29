"""
Atelier T.I.L.O.® — Validador de Cumplimiento Gastronómico y Gobernanza Clínica (V15.25.2)
Garantiza el cumplimiento estricto de la Directiva Sistémica Vinculante.
"""

from typing import Tuple
from app.schemas import TypedRecipeSchema, CulinaryTechniqueEnum

FORBIDDEN_KEYWORDS = [
    "cerdo", "puerco", "tocino de cerdo", "jamon de cerdo", "manteca", "chicharron",
    "chile", "serrano", "jalapeño", "habanero", "chipotle", "cayena", "paprika picante",
    "trigo", "maiz", "arroz", "harina refinada", "azucar"
]

def validate_recipe_compliance(recipe: TypedRecipeSchema) -> Tuple[bool, str]:
    """
    Valida la receta generada contra la Directiva Sistémica Vinculante.
    Retorna (True, "OK") si cumple con todos los criterios o (False, motivo) si debe ser rechazada.
    """
    if not recipe or not (recipe.title or recipe.name):
        return False, "La receta está vacía o no tiene título."

    title_lower = (recipe.title or recipe.name or "").lower().strip()
    
    # REGLA 1: Erradicación de Ingrediente Monolítico (Sin Falsos Positivos)
    ingredient_items = []
    if recipe.ingredient_groups:
        for g in recipe.ingredient_groups:
            if g.items:
                for item in g.items:
                    ingredient_items.append(item.name if hasattr(item, "name") else str(item))
    if hasattr(recipe, "ingredients") and recipe.ingredients:
        for item in recipe.ingredients:
            ingredient_items.append(item.name if hasattr(item, "name") else str(item))

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

    # REGLA 2: Coherencia Térmica por Técnica Culinaria
    steps_combined = " ".join([str(s.action_description if hasattr(s, "action_description") else s) for s in recipe.steps]).lower() if recipe.steps else ""
    
    if recipe.cooking_technique == CulinaryTechniqueEnum.RAW_ASSEMBLY:
        forbidden_thermal = ["cocinar a fuego", "hervir", "sellar", "sartén caliente", "fuego medio", "fuego alto"]
        for kw in forbidden_thermal:
            if kw in steps_combined:
                return False, f"Incoherencia térmica en raw_assembly: término prohibido '{kw}'."

    # REGLA 3: Prohibición de Pasos Genéricos Vagos
    generic_patterns = [
        "preparar e higienizar insumos",
        "cocinar a fuego medio controlando la temperatura",
        "servir de inmediato en plato amplio"
    ]
    matches = sum(1 for p in generic_patterns if p in steps_combined)
    if matches >= 2:
        return False, "Secuencia de pasos detectada como plantilla genérica vaga."

    return True, "OK"
