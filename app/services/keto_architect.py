import json
import re
import asyncio
from typing import List, Optional, Dict
from google import genai
from google.genai import types
from app.config import settings
from app.logger import logger
from app.database import get_db
from app.schemas import (
    WeeklyMenuPlan, DailyMenu, Meal, Ingredient, PreparationRecipe, NutritionMetrics,
    NegotiationRequest, NegotiationResponse, SuggestionRequest, SuggestionResponse, SuggestionItem,
    PantryItem, PreliminaryPrep, MealPrepBlock, DishProcedure,
    RecipeStep, RecipeValidationSchema, DynamicPrepPhases, CompilePhasesItem, CompilePhasesRequest, CompilePhasesResponse,
    ComprehensiveNutritionView, MealFunctionalAnalysis, FunctionalJustification,
    MealNutritionFactTable, NutritionFactItem, ClinicalGlycemicSection, MealGlycemicSynergy, FoodGlycemicAnalysis
)
from app.services.inventory_master import InventorySyncMaster

def compile_dynamic_prep_phases(dish_name: str, approved_ingredients: List[Ingredient], diners_count: int = 6) -> DynamicPrepPhases:
    """
    Micro-Agente de Ensamblaje Tipificado (V15.4.3 JIT Compiler):
    DIRECTIVA DE EJECUCIÓN CULINARIA ESTRICTA — PROHIBICIÓN TOTAL DE PLANTILLAS GENÉRICAS
    Calcula dinámicamente las fases de preparación técnica basadas estrictamente en la técnica real del plato
    (raw_assembly, poach_and_emulsion, gelatin_molding, boil_and_blend, roast_bake, saute_and_sear, steep_beverage).
    """
    import pydantic
    from app.schemas import TypedRecipeSchema, RecipeIngredientDetail, RecipeStepDetail, RecipeServiceDetail, RecipeYieldInfo, RecipeMacroTarget

    factor = diners_count / 6.0
    ing_text_list = []
    ing_details_prompt = []

    for ing in approved_ingredients:
        scaled_qty = round(ing.quantity * factor, 2)
        qty_str = f"{scaled_qty}".rstrip('.0') if scaled_qty == int(scaled_qty) else f"{scaled_qty:.1f}"
        ing_text_list.append(f"{ing.name}: {qty_str} {ing.unit}")
        ing_details_prompt.append({"name": ing.name, "quantity": scaled_qty, "unit": ing.unit})
    
    ing_summary = ", ".join(ing_text_list) if ing_text_list else "Ingredientes específicos asignados"

    api_key = settings.GEMINI_API_KEY
    if api_key and api_key.strip():
        try:
            client = genai.Client(api_key=api_key.strip())
            model_name = settings.GEMINI_MODEL or "gemini-1.5-flash"
            system_prompt = (
                f"DIRECTIVA DE EJECUCIÓN CULINARIA ESTRICTA — PROHIBICIÓN TOTAL DE PLANTILLAS GENÉRICAS\n"
                f"Eres el Micro-Agente de Ensamblaje y Químico Culinario del Atelier Herami (Ecosistema T.I.L.O.®).\n"
                f"Tu función es compilar la receta gastronómica estructurada para el platillo: '{dish_name}' para {diners_count} personas.\n\n"
                f"1. PROHIBICIÓN ABSOLUTA DE PLACEHOLDERS:\n"
                f"   - Queda estrictamente prohibido usar frases como 'insumos seleccionados de la granja/alacena', 'sazonadores y grasas', o 'proteínas y hortalizas de [Nombre del Plato]'.\n"
                f"   - Cada platillo DEBE listar sus ingredientes exactos con gramaje/volumen real escalado matemáticamente para los {diners_count} comensales indicados.\n\n"
                f"2. COHERENCIA TÉCNICA OBLIGATORIA POR TIPO DE PLATO:\n"
                f"   - FRUTAS / TARTAS FRÍAS / BOWLS / ENSALADAS (raw_assembly): Prohibido hablar de calor, sartenes, sellado o trinchado. Pasos: lavado, desgranado/corte, hidratación (chía/aderezo), ensamblaje en frío.\n"
                f"   - HUEVOS POCHADOS / ÇILBIR (poach_and_emulsion): Pasos: templar yogur con ajo y sal; pochar huevos en agua con vinagre a hervor bajo (85-90°C) por 3 min; fundir mantequilla con paprika/chile; montar huevos sobre yogur y bañar con mantequilla.\n"
                f"   - GELATINAS (gelatin_molding): Pasos: extracción/jugo, hidratación de grenetina/gelificante en agua fría 5 min, disolución tibia (60°C), vertido en moldes y refrigeración a 4°C hasta cuajar. NUNCA tratar como infusión herbal.\n"
                f"   - CREMAS Y SOPAS (boil_and_blend): Sofrito base en mantequilla -> cocción en caldo -> licuado terso -> integración láctea a fuego mínimo.\n"
                f"   - VEGETALES HORNEADOS (COLIFLOR/BRÓCOLI) (roast_bake): Troceado -> aliño con aceite y especias -> horneado a 200°C por 20-25 min. NUNCA 'trinchar contra la fibra a 58°C'.\n"
                f"   - INFUSIONES / TÉS (steep_beverage): Calentar agua a 90-95°C -> infundir hojas/hierbas 5 min -> colar y servir.\n"
                f"   - SALMÓN / PROTEÍNAS SELLADAS (saute_and_sear): Secado y costra de ajonjolí -> salsa fría de eneldo/yogur -> sello en sartén 180°C (4 min piel crocante, 2-3 min ajonjolí hasta 50-52°C interno).\n\n"
                f"3. ACCIONES Y VERBOS PROPIOS:\n"
                f"   - Redacta cada paso describiendo la transformación física y química del ingrediente con su nombre real.\n\n"
                f"Devuelve un JSON estrictamente conforme a TypedRecipeSchema con las claves: 'recipe_id', 'name', 'category', 'cooking_technique', 'yield', 'macro_target', 'equipment', 'ingredients', 'steps', 'service'."
            )
            response = client.models.generate_content(
                model=model_name,
                contents=f"Compila la receta técnica estructurada para {diners_count} personas del platillo: {dish_name}. Insumos: {json.dumps(ing_details_prompt)}",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
            raw_text = sanitize_genai_json_response(response.text or "{}")
            typed_recipe = TypedRecipeSchema.model_validate_json(raw_text)
            return typed_recipe.to_dynamic_prep_phases()
        except (pydantic.ValidationError, Exception) as e:
            logger.warning(f"Resiliencia JIT: Fallo en parsing TypedRecipeSchema LLM para '{dish_name}': {e}. Activando compilador determinístico de recetas reales.")

    return build_dynamic_prep_phases(dish_name, diners_count)


def resolve_technique(dish_name: str, category: str = "") -> str:
    name = (dish_name or "").lower()
    
    # 1. Bebidas / Infusiones reales
    if any(k in name for k in ["infusión", "infusion", "té ", "te ", "tisana", "café", "cafe"]):
        return "steep_beverage"
    
    # 2. Cremas y Sopas
    if any(k in name for k in ["crema", "sopa", "caldo", "consomé", "consome"]):
        return "boil_and_blend"
    
    # 3. Gelatinas / Mousses
    if any(k in name for k in ["gelatina", "mousse", "panna cotta"]):
        return "gelatin_molding"
        
    # 4. Huevos Pochados / Çılbır (poach_and_emulsion)
    if any(k in name for k in ["çılbır", "cilbir", "turcos", "pochado", "pochados", "benedict"]):
        return "poach_and_emulsion"

    # 5. Huevos Fritos / Omelettes / Sartenes (pan_fry_egg)
    if any(k in name for k in ["omelette", "huevo", "revuelto", "frittata", "shakshuka"]):
        return "pan_fry_egg"
        
    # 6. Platos fríos / Frutas / Ensaladas / Bastones
    if any(k in name for k in ["higos", "granada", "fruta", "ensalada", "bastones", "pepino", "tartar"]):
        return "raw_assembly"
        
    # 7. Proteínas y Salteados
    if any(k in name for k in ["salmón", "salmon", "pechuga", "pavo", "pollo", "carne", "corte"]):
        return "saute_and_sear"
        
    return "raw_assembly"  # Default seguro NUNCA debe ser infusión


def build_dynamic_prep_phases(dish_name: str, diners: int) -> DynamicPrepPhases:
    d = (dish_name or '').lower()
    n = diners or 6
    factor = n / 6.0
    g_meat = f"{round(n * 180)} g" if (n * 180) < 1000 else f"{(n * 0.18):.2f} kg"
    g_veg = f"{round(n * 120)} g" if (n * 120) < 1000 else f"{(n * 0.12):.2f} kg"

    if "frijol" in d or "frijoles" in d:
        dish_name = "Consomé Claro de Nopales y Hortalizas Tiernas"
        d = dish_name.lower()

    tech = resolve_technique(dish_name)

    # 1. Granada Fresca con Semillas de Chía y Nueces Pecana
    if "granada fresca con semillas" in d or ("granada" in d and "chía" in d):
        f1 = f"Fase 1 (Mise en Place y Gramajes): Arilos de granada fresca limpia ({round(300 * factor)} g), Nueces pecana troceadas ({round(120 * factor)} g), Semillas de chía ({round(60 * factor)} g), Leche de almendra sin azúcar o yogur natural ({round(360 * factor)} ml), Canela en polvo (1 pizca), Miel pura de la granja (≤ 5 g por comensal)."
        f2 = f"Fase 2 (Hidratación y Tostado): En tazón mediano, mezclar las semillas de chía con la leche o yogur y la canela. Dejar reposar 10-15 min en refrigeración (4°C) hasta formar gel ligero. Tostar ligeramente las nueces pecana en sartén seca a fuego medio-bajo por 2-3 min para liberar aceites aromáticos; retirar y picar toscamente."
        f3 = f"Fase 3 (Montaje en Frío): Dividir la base de chía hidratada en {n} copas o cuencos individuales. Coronar con los arilos de granada fresca y las nueces tostadas."
        f4 = f"Fase 4 (Servicio): Servir fresco a 8-10°C."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

    # 2. Huevos Turcos Çılbır (Pochados sobre Yogur Griego al Ajo) — poach_and_emulsion
    if tech == "poach_and_emulsion" or "turcos" in d or "çılbır" in d or "cilbir" in d or ("huevos" in d and "yogur" in d):
        f1 = f"Fase 1 (Mise en Place y Gramajes): Huevos frescos ({int(12 * factor)} piezas, 2 por comensal), Yogur griego natural sin azúcar a temp. ambiente ({round(750 * factor)} g / 3 tazas), Dientes de ajo finamente rallados ({max(1, int(3 * factor))} piezas), Mantequilla pura de pastoreo ({round(135 * factor)} g / 9 cdas), Aceite de oliva VEVO ({round(45 * factor)} ml / 3 cdas), Hojuelas de chile Aleppo o paprika ({round(15 * factor)} g / 1 cda), Comino molido (1.5 cditas), Vinagre blanco (3 cdas), Sal de mar y eneldo fresco picado."
        f2 = f"Fase 2 (Base de Yogur y Mantequilla Especiada): Mezclar en tazón el yogur griego con el ajo rallado, eneldo picado y 1 cdita de sal. Distribuir formando cama en {n} platos hondos. En sartén a fuego medio-bajo, derretir la mantequilla con el aceite de oliva hasta dorar ligeramente (mantequilla avellanada); retirar del fuego e incorporar el chile Aleppo y comino."
        f3 = f"Fase 3 (Pochado Regulado en Agua): Hierve abundante agua en cacerola amplia con el vinagre; reducir a ebullición suave (85°C-90°C). Cuelar exceso de clara líquida y pochar los huevos de 3 a 4 por tanda durante 3 minutos exactos para mantener la yema líquida. Retirar con espumadera y escurrir brevemente."
        f4 = f"Fase 4 (Servicio Gourmet): Colocar 2 huevos pochados calientes sobre la cama de yogur en cada plato. Bañar generosamente con la mantequilla especiada tibia y terminar con hojas de eneldo fresco y pimienta negra molida. Servir a 55-60°C."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

    # 3. Omelettes / Huevos Revueltos / Frittatas — pan_fry_egg
    if tech == "pan_fry_egg" or "omelette" in d or "revuelto" in d or "frittata" in d:
        f1 = f"Fase 1 (Mise en Place y Gramajes): Huevos frescos ({int(12 * factor)} piezas, 2 por comensal), Mantequilla de pastoreo ({round(40 * factor)} g), Queso o vegetal aromático picado ({round(120 * factor)} g), Sal de mar y pimienta."
        f2 = f"Fase 2 (Batido e Integración): Batir los huevos energéticamente con un batidor de globo hasta homogenizar clara y yema. Sazonar con sal de mar."
        f3 = f"Fase 3 (Cocción Regulada en Sartén): Calentar sartén antiadherente a fuego medio-bajo con mantequilla. Verter la mezcla de huevo y cuajar suavemente durante 3 a 4 minutos moviendo los bordes."
        f4 = f"Fase 4 (Servicio): Doblar o porcionar y servir de inmediato a 60°C."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

    # 4. Gelatina Artesanal de Granada Viva
    if tech == "gelatin_molding" or "gelatina" in d:
        f1 = f"Fase 1 (Mise en Place y Gramajes): Jugo de granada fresca recién exprimido ({round(900 * factor)} ml), Agua purificada ({round(300 * factor)} ml), Grenetina en polvo sin sabor ({round(28 * factor)} g / 4 sobres), Miel pura de la granja (≤ 5 g por comensal), Arilos de granada ({round(60 * factor)} g)."
        f2 = f"Fase 2 (Hidratación): Espolvorear la grenetina en los {round(300 * factor)} ml de agua fría y dejar hidratar durante 5 minutos hasta formar un gel esponjoso."
        f3 = f"Fase 3 (Disolución y Moldeo): Calentar la mitad del jugo a 60°C (sin hervir). Agregar la grenetina hidratada y mezclar con globo hasta disolver. Integrar el resto del jugo frío. Verter en {n} moldes individuales con arilos en el fondo."
        f4 = f"Fase 4 (Refrigeración y Servicio): Refrigerar a 4°C por 3 horas hasta firmeza total. Servir frío a 4°C."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)


    # 4. Sopa o Crema de Calabacitas / Brócoli / Espárragos (boil_and_blend)
    if tech == "boil_and_blend" or any(k in d for k in ['crema', 'sopa', 'consomé', 'consome', 'caldo', 'puré', 'pure']):
        f1 = f"Fase 1 (Mise en Place y Gramajes): Calabacitas/Vegetales tiernos ({round(900 * factor)} g), Cebolla blanca picada ({max(1, int(1 * factor))} pieza), Dientes de ajo picados ({max(1, int(2 * factor))} piezas), Cilantro fresco ({round(40 * factor)} g), Caldo de pollo o vegetales ({round(1000 * factor)} ml), Mantequilla ({round(40 * factor)} g), Crema de leche ({round(150 * factor)} ml), Queso parmesano recién rallado ({round(100 * factor)} g), Sal y pimienta."
        f2 = f"Fase 2 (Sofrito Base Aromático): En olla a fuego medio, derretir mantequilla y sofrito la cebolla y ajo por 3-4 min hasta acitronar."
        f3 = f"Fase 3 (Cocción, Licuado & Cremado): Añadir vegetales y caldo. Cocinar tapado a fuego medio-bajo por 8-10 min hasta tiernos. Incorporar cilantro al final. Licuar a alta velocidad hasta textura terciopelo. Regresar a fuego bajo, incorporar crema y la mitad del parmesano agitando con globo sin hervir."
        f4 = f"Fase 4 (Servicio Gourmet): Servir en tazones hondos a 68°C decorando con láminas de parmesano, hojas de cilantro y pimienta negra."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

    # 5. Salmón o Pescado / Proteínas con Costra (saute_and_sear)
    if tech == "saute_and_sear" or "salmón" in d or "salmon" in d or "pescado" in d:
        f1 = f"Fase 1 (Mise en Place y Gramajes): Filetes de salmón/pescado/proteína fresca con piel ({n} porciones de 180 g c/u), Semillas de ajonjolí blanco y negro ({round(60 * factor)} g), Aceite de oliva VEVO ({round(30 * factor)} ml), Yogur griego o crema agria ({round(180 * factor)} g), Eneldo fresco picado (2 cdas), Jugo de 1 limón, Sal y pimienta."
        f2 = f"Fase 2 (Acondicionamiento y Salsa de Eneldo): Secar bien los lomos con papel absorbente. Sazonar con sal y pimienta y presionar cara superior en el ajonjolí. En tazón pequeño, mezclar yogur con jugo de limón, eneldo picado y sal. Reservar salsa en frío."
        f3 = f"Fase 3 (Sello Térmico Regulado): Calentar sartén pesada con aceite a 180°C. Colocar la proteína con la piel hacia abajo y cocinar 4 min para piel crocante; voltear con cuidado sobre ajonjolí 2-3 min hasta punto jugoso (50-52°C interno)."
        f4 = f"Fase 4 (Servicio Gourmet): Servir de inmediato cada lomo acompañado de una porción de salsa fría de eneldo y gajo de limón a 65°C."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

    # 6. Coliflor / Brócoli Asado (roast_bake)
    if "coliflor" in d or "asada" in d or "paprika" in d or "horno" in d or "waffle" in d or "crepa" in d:
        f1 = f"Fase 1 (Mise en Place y Gramajes): 1 cabeza grande de coliflor en floretes medianos ({round(800 * factor)} g), Aceite de oliva VEVO ({round(45 * factor)} ml), Paprika dulce o ahumada (1.5 cdas), Ajo en polvo (1 cdita), Sal de mar y pimienta."
        f2 = f"Fase 2 (Aliño Específico): En tazón grande, mezclar la coliflor con aceite de oliva, paprika, ajo en polvo, sal y pimienta hasta impregnar todos los floretes."
        f3 = f"Fase 3 (Horneado Caramelizado): Distribución en charola para horno en una sola capa. Horneo a 200°C durante 20 a 25 min (moviendo a mitad de cocción) hasta que los bordes estén dorados y el centro tierno."
        f4 = f"Fase 4 (Servicio): Pasar a fuente de servicio tibia a 65°C como guarnición."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

    # 7. Bastones de Pepino Fresco o Ensaladas Frías (raw_assembly)
    if tech == "raw_assembly" or "bastones" in d or "pepino" in d or "tartar" in d or "ceviche" in d or "frutas" in d or "higo" in d:
        f1 = f"Fase 1 (Mise en Place y Gramajes): Pepinos/Insumos frescos firmes ({max(1, int(4 * factor))} piezas / {round(700 * factor)} g), Jugo de 2 limones, Aceite de oliva VEVO ({round(20 * factor)} ml), Escamas de sal de mar."
        f2 = f"Fase 2 (Corte Estético en Frío): Pelar parcialmente dejando tiras verde claro alternadas, retirar semillas con cuchara y cortar en bastones regulares de 7 a 8 cm o cubos uniformes."
        f3 = f"Fase 3 (Aliño en Frío): Disponer en platos fríos. Aliñar con limón recién exprimido, hilo de aceite VEVO y escamas de sal al instante."
        f4 = f"Fase 4 (Servicio): Servir crujiente a 6-8°C."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

    # 8. Pechuga de Pavo Desmenuzada o Ensalada Proteica (salad_assembly)
    if "pavo" in d or "mayonesa" in d or "ensalada de pechuga" in d:
        f1 = f"Fase 1 (Mise en Place y Gramajes): Pechuga de pavo cocida y deshebrada ({round(700 * factor)} g), Tallos de apio limpios en cubitos finos ({round(150 * factor)} g), Mayonesa casera de oliva ({round(140 * factor)} g), Mostaza Dijon (1 cda), Cebollín picado ({round(20 * factor)} g), Sal y pimienta."
        f2 = f"Fase 2 (Integración y Emulsión): En tazón amplio, emulsionar mayonesa con mostaza Dijon, sal y pimienta. Incorporar pavo deshebrado, apio crocante y cebollín."
        f3 = f"Fase 3 (Reposo y Asentamiento): Mezclar envolvente y refrigerar 15 minutos a 4°C para asentar texturas."
        f4 = f"Fase 4 (Servicio): Servir porciones individuales sobre hojas de lechuga orejona o endivias frescas a 8-10°C."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

    # 9. Infusión Relajante de Hierbas (steep_beverage)
    if tech == "steep_beverage" or any(k in d for k in ['té', 'te', 'infusión', 'infusion', 'tisana']):
        f1 = f"Fase 1 (Mise en Place de Infusión): Agua purificada ({round(1500 * factor)} ml), Mezcla de manzanilla, menta/hierbabuena y toronjil ({round(30 * factor)} g)."
        f2 = f"Fase 2 (Calentamiento de Agua): Llevar agua purificada a 90-95°C en tetera (punto previo al hervor descontrolado)."
        f3 = f"Fase 3 (Infusión Controlada): Colocar hierbas en infusor, verter agua caliente, tapar y dejar reposar 5 a 6 minutos para extraer aceites esenciales sin amargar."
        f4 = f"Fase 4 (Servicio): Colar y servir caliente en tazas térmicas a 68-70°C."
        return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

    # Default seguro NUNCA debe ser infusión
    f1 = f"Fase 1 (Mise en Place y Gramajes): Insumos frescos de {dish_name} para {n} comensales ({round(700 * factor)} g), Aceite VEVO ({round(20 * factor)} ml), Sal de mar y limón."
    f2 = f"Fase 2 (Corte Estético en Frío): Higienizar a 4°C y cortar en porciones uniformes estéticas."
    f3 = f"Fase 3 (Aliño / Macerado en Frío): Marinarse y aderezar en frío a 4°C por 8 minutos."
    f4 = f"Fase 4 (Servicio): Montar en vajilla refrigerada y servir fresco a 6-8°C."
    return DynamicPrepPhases(fase_1_mise_en_place=f1, fase_2_acondicionamiento=f2, fase_3_termodinamica=f3, fase_4_servicio=f4)

KETO_CULINARY_CORTEX_PROMPT = """
# SYSTEM PROMPT MAESTRO - CORTEX CULINARIO ATELIER HERAMI (ANTIGRAVITY 2.0 V14.0)

**[ROLE & IDENTITY]**
Eres el Cortex Gatekeeper de Arquitectura Herami, un Atelier culinario impulsado por el marco T.I.L.O.®. Tu función es auditar y negociar diseños de menús con precisión milimétrica, asegurando alta hospitalidad, balance metabólico y cero redundancia, utilizando ingredientes de alto rendimiento biotecnológico de Granja El Herami.

**[DECÁLOGO OFICIAL DE GOBERNANZA Y PLANIFICACIÓN DE MENÚS (ARQUITECTURA HERAMI / ATELIER T.I.L.O.®)]**
1. 🛡️ Cero Redundancia por Servicio: En un mismo tiempo de comida, entrada, plato principal y acompañamiento DEBEN usar vegetales e ingredientes base distintos.
2. 🔄 Rotación Culinaria de 4 Semanas: Ningún platillo puede repetirse si ha aparecido en los últimos 28 días (3 semanas previas).
3. 🧪 Trofología Clínica y Fruta Única: Cero mezcla de frutas con lactoproteínas densas (Queso Cottage solo con Fresas). Fruta Única por preparación (una sola fruta por porción).
4. 🍓 Acompañamiento Fijo en Desayunos: Gelatina Artesanal elaborada con Grenetina Natural y Fruta Fresca de la Granja.
5. 🥑 Unicidad de Grasa Dominante: Cero duplicación de la misma fuente de grasa vegetal pesada en el mismo plato (si hay aguacate en el principal, la entrada/acompañamiento usa aceite de oliva o mantequilla).
6. 🥩 Cero Cerdo y Protección de Proteínas: ≤ 5g carbohidratos netos por platillo. Prohibida taxativamente la carne de cerdo y sus derivados (usar únicamente res magra/semimagra, pavo, pollo, pescados salvajes y huevo de granja).
7. 🍯 Política de Endulzantes: Cero azúcar refinada, estevia, eritritol o edulcorantes artificiales. Miel de la granja permitida únicamente en microdosis (≤ 5g) en desayunos o entradas amortiguadas con grasas/proteínas.
8. 🍳 Perfil Gastroprotector y Termoestabilidad: Cero picante / capsaicina (todas las preparaciones sin chile). Cero frituras profundas o carbonizados.
9. 🧬 Crononutrición y Sinergix: Secuencia de ingesta (1° Fibra/Verdes -> 2° Proteínas/Grasas -> 3° Gelatina/Fruta) y cronograma de 4 tomas Sinergix.
10. 📐 Abastecimiento Tridimensional (3D): Integración paramétrica con diners_count y balance de cosecha de la Granja El Herami ($0).

**[TASK]**
Recibirás el nombre de un platillo inédito. Tu única tarea es generar un JSON estricto que contenga la matriz matemática de ingredientes base (calculada matemáticamente para exactamente 1 comensal) y los pasos de preparación física reales.

**[STRICT MATHEMATICAL RULES (ZERO-TOUCH PIPELINE)]**
1. ❌ PROHIBICIÓN ABSOLUTA DE HARDCODING: Tienes strictly prohibido escribir números absolutos de peso, volumen o porciones en el texto de las instrucciones (ej. NUNCA escribas "300g", "2 personas", "50 ml", "1 taza").
2. NOMENCLATURA ESTÁNDAR EN INGLÉS: Las claves de la `math_matrix` DEBEN estar en inglés, formato snake_case, y usar terminaciones de unidad estándar (`_g` para gramos, `_ml` para líquidos, `_tbsp` para cucharadas, `_count` para unidades). Ej: `chicken_breast_g`, `spinach_g`, `olive_oil_tbsp`, `portobello_count`.
3. USO DE TOKENS MATEMÁTICOS: Todo ingrediente cuantificable debe declararse primero en la `math_matrix`. En el texto de las instrucciones, ÚNICAMENTE utilizarás las variables encapsuladas entre llaves (ej. `{chicken_breast_g}`, `{olive_oil_tbsp}`).
4. DINERS COUNT: Para referirte al número de comensales en el texto, utiliza exclusivamente el token reservado `{diners_count}`.
5. CONSTANTES TÉRMICAS PERMITIDAS: Las únicas cifras absolutas permitidas en el texto son la temperatura (ej. "200°C") y el tiempo (ej. "15 minutos"), ya que no escalan con el número de personas.

**[CULINARY STANDARD RULES]**
1. Cero Plantillas: No uses frases sintéticas ni genéricas (como "Limpieza de proteína e insumos" o "Cocción sellada a 65°C").
2. Técnica Real: Usa verbos culinarios profesionales (blanquear, desglasar, sofreír, sellar, emulsionar, hornear, raspar, infusionar).
3. Estructura Libre: Usa de 3 a N pasos reales. Incluye `inventory_tags` en español para la lista de compras.

**[JSON SCHEMA OUTPUT]**
Debes devolver ÚNICAMENTE un objeto JSON válido, sin formato markdown extra ni introducciones, con la siguiente estructura exacta:
{
  "recipe_id": "string (formato snake_case)",
  "display_name": "string (Nombre oficial del platillo)",
  "math_matrix": {
    "token_1_g": float,
    "token_2_tbsp": float
  },
  "inventory_tags": ["string (Ingrediente en español)"],
  "steps": [
    {
      "step_number": int,
      "title": "string (Acción principal)",
      "instruction": "string (Instrucción usando EXCLUSIVAMENTE los {tokens})"
    }
  ]
}
"""

def sanitize_genai_json_response(raw_text: str) -> str:
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', raw_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return raw_text.strip()

_recipe_locks: Dict[str, asyncio.Lock] = {}

async def get_or_create_lock(recipe_id: str) -> asyncio.Lock:
    if recipe_id not in _recipe_locks:
        _recipe_locks[recipe_id] = asyncio.Lock()
    return _recipe_locks[recipe_id]

def get_emergency_rescue_recipe(dish_name: str) -> RecipeValidationSchema:
    d_clean = dish_name.lower().strip().replace(" ", "_")
    return RecipeValidationSchema(
        recipe_id=d_clean,
        display_name=dish_name,
        math_matrix={"protein_g": 180.0, "olive_oil_tbsp": 0.5, "veggie_g": 100.0},
        inventory_tags=["Proteína Base", "Aceite de Oliva", "Hortalizas de la Granja"],
        steps=[
            RecipeStep(step_number=1, title="Preparación e Higienización", instruction="Lavar e higienizar {veggie_g} g de vegetales frescos y sazonar {protein_g} g de proteína con sal de mar y pimienta."),
            RecipeStep(step_number=2, title="Cocción y Sellado", instruction="Calentar {olive_oil_tbsp} cdas de aceite de oliva en sartén a fuego medio. Sellado preciso hasta lograr término jugoso para {diners_count} comensales."),
            RecipeStep(step_number=3, title="Servicio Gourmet", instruction="Emplatar de inmediato a temperatura de servicio adecuada para {diners_count} personas.")
        ],
        is_rescue_flag=True
    )

def generate_autonomous_recipe(dish_name: str, max_retries: int = 3) -> RecipeValidationSchema:
    api_key = settings.GEMINI_API_KEY
    if not api_key or not api_key.strip():
        logger.warning(f"Sin GEMINI_API_KEY configurado. Usando receta de rescate para {dish_name}.")
        return get_emergency_rescue_recipe(dish_name)

    client = genai.Client(api_key=api_key.strip())
    model_name = settings.GEMINI_MODEL or "gemini-1.5-flash"
    
    last_error = ""
    prompt_user = f"Genera la receta autónoma en JSON para el platillo: '{dish_name}'"

    for attempt in range(max_retries):
        try:
            current_prompt = prompt_user
            if last_error:
                current_prompt += f"\n\nATENCIÓN: Tu intento anterior falló por la siguiente razón de validación:\n'{last_error}'.\nPor favor CORRIGE el JSON declarando todos los tokens cuantificables en math_matrix y usando ÚNICAMENTE los {{tokens}} en el texto sin números estáticos."

            response = client.models.generate_content(
                model=model_name,
                contents=current_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=KETO_CULINARY_CORTEX_PROMPT,
                    temperature=0.2
                )
            )
            raw_text = response.text or ""
            clean_json = sanitize_genai_json_response(raw_text)
            recipe_obj = RecipeValidationSchema.model_validate_json(clean_json)
            recipe_obj.is_rescue_flag = False
            return recipe_obj
        except Exception as e:
            last_error = str(e)
            logger.warning(f"Intento {attempt + 1}/{max_retries} fallido para receta '{dish_name}': {last_error}")

    logger.error(f"Fallo crítico en Zero-Touch Pipeline tras {max_retries} reintentos para '{dish_name}'. Ejecutando Receta de Rescate.")
    return get_emergency_rescue_recipe(dish_name)

class RecipeMathEngine:
    @staticmethod
    def interpolate_text(instruction: str, math_matrix: dict, diners_count: int) -> str:
        text = instruction.replace("{diners_count}", str(diners_count))
        for token, base_qty in math_matrix.items():
            calc_val = base_qty * diners_count
            formatted_val = str(int(calc_val)) if isinstance(calc_val, (int, float)) and calc_val.is_integer() else f"{calc_val:.1f}"
            text = text.replace(f"{{{token}}}", formatted_val)
        return text

class RecipeRepositoryManager:
    @staticmethod
    def get_procedure(dish_name: str, diners_count: int = 6) -> DishProcedure:
        d_lower = dish_name.lower().strip()
        
        if any(k in d_lower for k in ["portobello", "champiñón", "champiñon", "champiñones"]):
            recipe_key = "portobello_gouda_pavo"
        elif "pechuga" in d_lower and ("rellena" in d_lower or "espinaca" in d_lower or "queso crema" in d_lower):
            recipe_key = "pechuga_rellena_queso_crema_espinacas"
        else:
            recipe_key = d_lower.replace(" ", "_")

        # 1. Consultar SQLite excluyendo recetas marcadas como de rescate (is_rescue_flag = 1)
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT display_name, math_matrix_json, steps_json FROM recipes WHERE recipe_id = ? AND (is_rescue_flag = 0 OR is_rescue_flag IS NULL)", 
                    (recipe_key,)
                )
                row = cursor.fetchone()
                if row:
                    matrix = json.loads(row["math_matrix_json"])
                    steps_raw = json.loads(row["steps_json"])
                    
                    interpolated_steps = []
                    for s in steps_raw:
                        interp_inst = RecipeMathEngine.interpolate_text(s["instruction"], matrix, diners_count)
                        interpolated_steps.append(RecipeStep(
                            step_number=s["step_number"],
                            title=s["title"],
                            instruction=interp_inst
                        ))
                    return DishProcedure(dish_name=row["display_name"], steps=interpolated_steps)
        except Exception as e:
            logger.warning(f"Error consultando repositorio de recetas SQLite: {e}")

        # 2. Generación Cognitiva Zero-Touch Pipeline en caso de Cache Miss
        try:
            autonomous_recipe = generate_autonomous_recipe(dish_name)
            
            # Solo persistir si NO es una receta de rescate de emergencia
            if not autonomous_recipe.is_rescue_flag:
                try:
                    with get_db() as conn:
                        cursor = conn.cursor()
                        steps_dicts = [s.model_dump() for s in autonomous_recipe.steps]
                        cursor.execute(
                            "INSERT OR REPLACE INTO recipes (recipe_id, display_name, math_matrix_json, steps_json, inventory_tags_json, is_rescue_flag) VALUES (?, ?, ?, ?, ?, 0)",
                            (
                                autonomous_recipe.recipe_id, 
                                autonomous_recipe.display_name, 
                                json.dumps(autonomous_recipe.math_matrix), 
                                json.dumps(steps_dicts),
                                json.dumps(autonomous_recipe.inventory_tags)
                            )
                        )
                except Exception as db_err:
                    logger.error(f"Error al guardar receta autónoma en SQLite: {db_err}")

            interpolated_steps = []
            for s in autonomous_recipe.steps:
                interp_inst = RecipeMathEngine.interpolate_text(s.instruction, autonomous_recipe.math_matrix, diners_count)
                interpolated_steps.append(RecipeStep(
                    step_number=s.step_number,
                    title=s.title,
                    instruction=interp_inst
                ))
            return DishProcedure(dish_name=autonomous_recipe.display_name, steps=interpolated_steps)
        finally:
            _recipe_locks.pop(recipe_key, None)

    @staticmethod
    def _generate_dynamic_fallback(dish_name: str, diners_count: int) -> DishProcedure:
        d_lower = dish_name.lower()
        
        if "pochado" in d_lower or ("huevo" in d_lower and "espinaca" in d_lower):
            matrix = {"eggs_count": 2.0, "spinach_g": 80.0, "garlic_g": 5.0, "butter_g": 15.0}
            steps = [
                RecipeStep(step_number=1, title="Saltear la cama de espinacas", instruction="Calienta {butter_g} g de mantequilla en sartén a fuego medio. Añade {garlic_g} g de ajo picado y sofríe 30s. Incorpora {spinach_g} g de espinacas frescas para {diners_count} personas sazonando con sal, pimienta y pizca de nuez moscada. Cocina 2 a 3 min hasta verde brillante."),
                RecipeStep(step_number=2, title="Preparar agua para pochar", instruction="Calienta una olla con agua a ebullición suave (burbujas pequeñas) con 1 chorrito de vinagre blanco para acelerar la coagulación de la clara. Rompe {eggs_count} huevos individualmente en una taza."),
                RecipeStep(step_number=3, title="Pochar los huevos", instruction="Crea un remolino suave en el centro del agua con una cuchara. Desliza los huevos uno a uno en el centro del remolino y cocina de 3 a 3.5 min para lograr yema líquida y cremosa. Retira con espumadera."),
                RecipeStep(step_number=4, title="Armar y Servir", instruction="Coloca los huevos pochados sobre la cama de espinacas salteadas calientes. Coronar con queso parmesano o de cabra desmoronado al gusto para {diners_count} comensales.")
            ]
        elif any(k in d_lower for k in ["parrillada", "aguja", "agujas", "carne para asar", "sirloin"]):
            matrix = {"meat_g": 180.0, "nopal_count": 2.0, "butter_g": 20.0}
            steps = [
                RecipeStep(step_number=1, title="Marinación Norteña", instruction="Limpia y corta {meat_g} g de carne para asar y agujas norteñas. Marina con sal de mar gruesa, ajo aplastado, pimienta negra quebrada y chorrito de aceite de oliva."),
                RecipeStep(step_number=2, title="Encendido de Parrilla", instruction="Calienta la parrilla o comal de hierro fundido a fuego alto (220°C). Sella los barrotes con {butter_g} g de mantequilla."),
                RecipeStep(step_number=3, title="Asado y Sellado", instruction="Coloca la carne a fuego directo de 3 a 4 min por lado para un sellado jugoso a término medio o tres cuartos."),
                RecipeStep(step_number=4, title="Reposo y Servicio", instruction="Deja reposar la carne 3 min sobre tabla para redistribuir jugos. Trincha en tiras contra la fibra y sirve caliente acompañado de {nopal_count} nopales asados para {diners_count} personas.")
            ]
        elif "nogada" in d_lower or ("atún" in d_lower and "nogada" in d_lower) or ("atun" in d_lower and "nogada" in d_lower):
            matrix = {"tuna_g": 150.0, "fruit_g": 40.0, "walnut_g": 30.0, "goat_cheese_g": 20.0, "pomegranate_g": 15.0}
            steps = [
                RecipeStep(step_number=1, title="Sellar atún y base aromática", instruction="Calienta aceite de oliva en cacerola. Sofreír cebolla y ajo. Incorpora {tuna_g} g de medallones de atún fresco picados en cubitos. Sazona con sal, pimienta, canela y clavo molido; saltea 3 a 4 min."),
                RecipeStep(step_number=2, title="Caldillo de jitomate y frutos secos", instruction="Verter jitomates maduros licuados sobre el atún. Cocinar a fuego medio-bajo 6 a 8 min. Agregar {walnut_g} g de nuez picada e integrar por 3 min."),
                RecipeStep(step_number=3, title="Fruta fresca y reposo", instruction="Añadir {fruit_g} g de cubitos de manzana, pera y durazno. Cocinar a fuego lento 5 min moviendo con delicadeza. Verter chorrito de jerez seco 1 min y dejar atemperar."),
                RecipeStep(step_number=4, title="Napar con Nogada y Decoración", instruction="Formar una base compacta de picadillo de atún. Napar generosamente con la salsa en nogada fría ({goat_cheese_g} g de queso de cabra). Coronar con {pomegranate_g} g de granada fresca y perejil picado para {diners_count} comensales.")
            ]
        else:
            matrix = {"protein_g": 180.0, "veggie_g": 100.0, "fat_g": 20.0}
            steps = [
                RecipeStep(step_number=1, title="Preparación de Insumos", instruction="Lavar e higienizar {veggie_g} g de vegetales frescos de la granja y sazonar {protein_g} g de proteína con sal de mar, pimienta y ajo."),
                RecipeStep(step_number=2, title="Sellado y Cocción Culinaria", instruction="Calentar {fat_g} g de grasa saludable (mantequilla de pastoreo / aceite de coco / oliva extra virgen) en sartén a fuego medio. Sellado preciso hasta lograr término jugoso."),
                RecipeStep(step_number=3, title="Integración de Sabores", instruction="Incorporar guarnición de vegetales, salteando suavemente 3 a 5 min a temperatura controlada para mantener nutrientes activos."),
                RecipeStep(step_number=4, title="Servicio Gourmet", instruction="Emplatar de inmediato a temperatura de servicio adecuada para {diners_count} comensales acompañando con infusión o té botánico.")
            ]

        val_schema = RecipeValidationSchema(
            recipe_id=d_lower.replace(" ", "_"),
            display_name=dish_name,
            math_matrix=matrix,
            steps=steps
        )
        
        interpolated_steps = []
        for s in val_schema.steps:
            interp_inst = RecipeMathEngine.interpolate_text(s.instruction, val_schema.math_matrix, diners_count)
            interpolated_steps.append(RecipeStep(
                step_number=s.step_number,
                title=s.title,
                instruction=interp_inst
            ))

        return DishProcedure(dish_name=dish_name, steps=interpolated_steps)

KETO_ARCHITECT_SYSTEM_PROMPT = """
Eres KetoAIArchitect, el motor de inteligencia clínica cetogénica del Ecosistema T.I.L.O.® y Equipo en Acción®.
Generas planes semanales estructurados escalables dinámicamente según el número de comensales.
Reglas Estrictas:
1. Semana 33: Del Domingo 09 de Agosto al Sábado 15 de Agosto de 2026.
2. Lunes 10 de Agosto (Cena): Evento Especial de Aniversario. Fijar nota 'Cena en Restaurante (Evento Especial)'. NO generar receta ni insumos para compras.
3. Escalado dinámico de cantidades y textos de preparación según el número de comensales activo.
4. Sin picante (100% suave). Sin snacks.
"""

NEGOTIATION_SYSTEM_PROMPT = """
Eres el Cortex Gatekeeper de Arquitectura Herami, un Atelier culinario impulsado por el marco T.I.L.O.®. Tu función es auditar y negociar diseños de menús con precisión milimétrica, asegurando alta hospitalidad, balance metabólico y cero redundancia, utilizando ingredientes de alto rendimiento biotecnológico de Granja El Herami.
"""



class KetoAIArchitect:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL or "gemini-1.5-flash"
        self.client = None
        if self.api_key and self.api_key.strip():
            try:
                self.client = genai.Client(api_key=self.api_key.strip())
            except Exception as e:
                logger.error(f"Error al inicializar cliente Google GenAI: {e}")
                self.client = None
        else:
            self.client = None

        # Esquema oficial de 4 tomas diarias Sinergix (1 Dosis Completa por toma)
        self.sinergix_schedule = [
            {
                "slot": "TOMA 1",
                "timing": "Al despertar",
                "formula": "Multi Sinergix",
                "fraction": 1.0,
                "specification": "1 Dosis Completa. Ignición mitocondrial. Activación de CoQ10, PQQ y soporte energético en ayunas."
            },
            {
                "slot": "TOMA 2",
                "timing": "Desayuno",
                "formula": "Multi Sinergix",
                "fraction": 1.0,
                "specification": "1 Dosis Completa. Soporte enzimático y metabólico. Mezclado con yogur griego keto o infusión/té."
            },
            {
                "slot": "TOMA 3",
                "timing": "Cena",
                "formula": "Amino Sinergix",
                "fraction": 1.0,
                "specification": "1 Dosis Completa. Aporte de péptidos de colágeno, aminoácidos esenciales y electrolitos con el alimento."
            },
            {
                "slot": "TOMA 4",
                "timing": "Antes de dormir",
                "formula": "Amino Sinergix",
                "fraction": 1.0,
                "specification": "1 Dosis Completa. Carga final para el cross-linking nocturno, melatonina y Bisglicinato de Magnesio."
            }
        ]

    def calculate_sinergix_inventory_requirement(self, diners_count: int = 6, days_count: int = 7) -> dict:
        scaling_factor = diners_count / 6.0
        doses_per_day = 2.0  # 2 dosis completas diarias por persona por fórmula (1 dosis por toma)
        total_multi_required = (doses_per_day * days_count) * scaling_factor
        total_amino_required = (doses_per_day * days_count) * scaling_factor
        
        return {
            "Multi_Sinergix_doses": round(total_multi_required, 2),
            "Amino_Sinergix_doses": round(total_amino_required, 2),
            "breakdown": self.sinergix_schedule
        }

    def generate_daily_supplementation_block(self) -> list:
        block = []
        for dose in self.sinergix_schedule:
            block.append({
                "momento": dose["timing"],
                "formula": dose["formula"],
                "proporcion": "1 Dosis Completa (100%)",
                "especificacion_tecnica": dose["specification"]
            })
        return block

    @staticmethod
    def validate_no_duplicate_broths(meal_structure: dict) -> dict:
        """
        Bloquea la asignación simultánea de caldos, consomés o sopas 
        en la entrada y el plato principal de un mismo tiempo de comida.
        """
        starter = meal_structure.get("starter", "").lower()
        main = meal_structure.get("main", "").lower()
        
        if any(k in starter for k in ["caldo", "consomé", "consome", "sopa"]) and any(k in main for k in ["caldo", "consomé", "consome", "sopa"]):
            meal_structure["starter"] = "Ensalada de Hojas Verdes de la Granja"
        return meal_structure

    @staticmethod
    def enforce_fat_source_uniqueness(meal_structure: dict) -> dict:
        """
        Evita la duplicidad de aguacate o complementos grasos iguales 
        entre el plato principal/entrada y el acompañamiento.
        """
        starter = meal_structure.get("starter", "").lower()
        main = meal_structure.get("main", "").lower()
        side = meal_structure.get("side", "").lower()
        
        if ("aguacate" in main or "guacamole" in main or "aguacate" in starter) and ("aguacate" in side or "guacamole" in side):
            meal_structure["side"] = "Bastones de Pepino Fresco con Sal de Mar"
        return meal_structure

    @staticmethod
    def validate_no_internal_ingredient_repetition(meal_structure: dict) -> dict:
        """
        Regla 3: Si un ingrediente base (espinacas, nopales, calabacitas) se usa en la entrada,
        se prohíbe en el plato principal o acompañamiento del mismo tiempo de comida.
        """
        st = meal_structure.get("starter", "").lower()
        main = meal_structure.get("main", "").lower()
        side = meal_structure.get("side", "").lower()
        
        ingredients_to_check = ["espinaca", "espinacas", "nopal", "nopales", "calabacita", "calabacitas", "apio", "mayonesa"]
        for ing in ingredients_to_check:
            if ing in st and ing in main:
                raise ValueError(f"Fallo de Repetición Interna: '{ing}' repetido en Entrada y Principal de la misma comida.")
            if ing in st and ing in side:
                raise ValueError(f"Fallo de Repetición Interna: '{ing}' repetido en Entrada y Acompañamiento de la misma comida.")
            if ing in main and ing in side:
                raise ValueError(f"Fallo de Repetición Interna: '{ing}' repetido en Principal y Acompañamiento de la misma comida.")
        return meal_structure

    def _validate_menu_diversity(self, spec: list) -> None:
        """
        Filtro Estricto de Unicidad Semanal y Diversidad Culinaria Antigravity 2.0:
        1. Regla de Exclusividad Semanal: Ningún plato principal puede repetirse en la semana.
        2. Blindaje contra Bucles Consecutivos: No 2 días consecutivos con desayunos/comidas idénticos.
        3. Cero Repetición Interna por Tiempo de Comida: Ingrediente base de Entrada no se repite en Principal/Acompañamiento.
        4. Cierres Organolépticos Dulces Keto en Comida/Cena (Gelatinas, Mousses sin azúcar).
        """
        seen_main_dishes = set()
        prev_day_meals = None

        for day_idx, day_data in enumerate(spec):
            day_name = day_data["day"]
            avocado_count = 0
            curr_day_meals = []

            for m_type, din_spec, st_name, m_name, sd_name, fat, prot, carbs, ings in day_data["meals"]:
                meal_struct = {"starter": st_name, "main": m_name, "side": sd_name}

                # 1. Exclusividad Semanal de Platillo Principal
                clean_main = m_name.strip().lower()
                if clean_main in seen_main_dishes:
                    raise ValueError(f"Fallo de Exclusividad Semanal en {day_name}: El plato principal '{m_name}' ya fue programado en la semana.")
                seen_main_dishes.add(clean_main)

                # 2. Sanitize & Validate Broths, Fat Sources & Internal Repetitions
                self.validate_no_duplicate_broths(meal_struct)
                self.enforce_fat_source_uniqueness(meal_struct)
                self.validate_no_internal_ingredient_repetition(meal_struct)

                curr_day_meals.append((st_name.lower(), clean_main, sd_name.lower()))

                meal_text = f"{st_name} {m_name} {sd_name}".lower()
                if "aguacate" in meal_text or "guacamole" in meal_text:
                    avocado_count += 1

            # 3. Blindaje contra Bucles Consecutivos
            if prev_day_meals is not None:
                for idx, (curr_st, curr_m, curr_sd) in enumerate(curr_day_meals):
                    prev_st, prev_m, prev_sd = prev_day_meals[idx]
                    if curr_m == prev_m:
                        raise ValueError(f"Fallo de Bucle Consecutivo en {day_name}: El platillo '{curr_m}' es idéntico al día anterior.")

            prev_day_meals = curr_day_meals

            if avocado_count > 1:
                raise ValueError(f"Fallo de Diversidad en {day_name}: Aguacate/Guacamole aparece {avocado_count} veces en el mismo día (Máximo: 1).")

    def _format_pantry_context(self, pantry_items: List[PantryItem]) -> str:
        if not pantry_items:
            return "Alacena actual: Sin registro previo."
        items_str = ", ".join([f"{item.item_name} ({item.quantity} {item.unit})" for item in pantry_items])
        return f"Inventario actual en alacena: {items_str}"

    def generate_weekly_plan(self, diners_count: int = 6, preferences: str = "") -> WeeklyMenuPlan:
        pantry = InventorySyncMaster.get_all_pantry_items()
        pantry_context = self._format_pantry_context(pantry)

        logger.info(f"KetoAIArchitect: Cargando Plan Semana 34 (16 al 22 Ago 2026) para {diners_count} comensales...")

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT plan_json FROM weekly_plans WHERE diners_count = ? ORDER BY id DESC LIMIT 1", (diners_count,))
            row = cursor.fetchone()
            if row and not preferences:
                try:
                    plan_dict = json.loads(row["plan_json"])
                    plan = WeeklyMenuPlan.model_validate(plan_dict)
                    InventorySyncMaster.seed_shopping_list_from_plan(plan)
                    return plan
                except Exception as e:
                    logger.warning(f"Caché SQLite no válido: {e}")

        plan = self._generate_fallback_weekly_plan(diners_count)
        self._cache_plan(diners_count, plan)
        InventorySyncMaster.seed_shopping_list_from_plan(plan)
        return plan

    def _cache_plan(self, diners_count: int, plan: WeeklyMenuPlan) -> None:
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM weekly_plans WHERE diners_count = ?", (diners_count,))
                cursor.execute(
                    "INSERT INTO weekly_plans (week_start, diners_count, plan_json) VALUES (?, ?, ?)",
                    ("2026-08-16", diners_count, plan.model_dump_json())
                )
        except Exception as e:
            logger.error(f"Error al guardar plan en caché: {e}")

    def suggest_alternative_dishes(self, request: SuggestionRequest) -> SuggestionResponse:
        m_type = (request.meal_type or "Comida").lower()
        target = (request.target_field or "main").lower()

        if "desayuno" in m_type:
            if target == "starter":
                items = [
                    SuggestionItem(
                        title="Pitahaya Fresca de la Granja con Semillas de Chía y Nueces Pecana",
                        description="Porción de fruta fresca desinfectada a 4°C con gel ligero de chía y nueces en trozos.",
                        key_ingredients=["Pitahaya fresca", "Semillas de chía", "Nueces pecana"]
                    ),
                    SuggestionItem(
                        title="Fresas Frescas de la Granja con Nueces Pecana y Chía",
                        description="Gajos de fresas de cosecha con chía hidratada en agua purificada.",
                        key_ingredients=["Fresas frescas", "Semillas de chía", "Nueces pecana"]
                    ),
                    SuggestionItem(
                        title="Durazno Fresco con Semillas de Chía y Coco Rallado",
                        description="Láminas de durazno tierno de la granja coronadas con coco sin azúcar.",
                        key_ingredients=["Durazno fresco", "Coco rallado", "Semillas de chía"]
                    )
                ]
            elif target == "side":
                items = [
                    SuggestionItem(
                        title="Gelatina Artesanal de Fresas de la Granja",
                        description="Postre fresco cuajado con grenetina natural e infusión de fruta de cosecha.",
                        key_ingredients=["Grenetina natural", "Fresas frescas", "Agua purificada"]
                    ),
                    SuggestionItem(
                        title="Gelatina Artesanal de Granada Viva de la Granja",
                        description="Gelatina de grenetina natural con infusión de granada roja.",
                        key_ingredients=["Grenetina natural", "Granada viva", "Agua purificada"]
                    ),
                    SuggestionItem(
                        title="Gelatina Artesanal de Granada Viva Frescos de la Granja",
                        description="Postre cuajado a 4°C con grenetina sin sabor y pulpa natural de higos.",
                        key_ingredients=["Grenetina natural", "Higos frescos", "Agua purificada"]
                    )
                ]
            else:
                items = [
                    SuggestionItem(
                        title="Shakshuka Tradicional (Huevos Estrellados en Salsa de Jitomate Bola)",
                        description="Huevos de granja pochados suavemente en reducción de jitomate al comino.",
                        key_ingredients=["Huevos frescos", "Jitomate bola", "Aceite de oliva extra virgen"]
                    ),
                    SuggestionItem(
                        title="Frittata Italiana de Campo con Jamón de Pavo y Queso Panela",
                        description="Tortilla horneada a fuego lento con espinacas baby y queso panela artesanal.",
                        key_ingredients=["Huevos frescos", "Tocino de pavo", "Queso panela", "Espinacas"]
                    ),
                    SuggestionItem(
                        title="Omelette de Queso de Cabra y Tocino de Pavo Ahumado",
                        description="Huevos batidos a baja temperatura con queso de cabra y tocino crujiente de pavo.",
                        key_ingredients=["Huevos frescos", "Queso de cabra", "Tocino de pavo"]
                    )
                ]
        elif "cena" in m_type:
            if target == "starter":
                items = [
                    SuggestionItem(
                        title="Bastones de Pepino y Apio al Limón con Sal de Mar",
                        description="Vegetales crujientes desinfectados en agua helada con aderezo ligero.",
                        key_ingredients=["Pepino fresco", "Apio fresco", "Aceite de oliva extra virgen"]
                    ),
                    SuggestionItem(
                        title="Ensalada de Espinacas Baby a la Vinagreta de Manzana",
                        description="Hojas tiernas de espinaca con vinagre de manzana y aceite de oliva.",
                        key_ingredients=["Espinacas baby", "Aceite de oliva extra virgen", "Vinagre de manzana"]
                    ),
                    SuggestionItem(
                        title="Abanico de Aguacate Hass con Sal de Mar Marina",
                        description="Láminas pulcras de aguacate Hass sazonadas con sal de mar marina.",
                        key_ingredients=["Aguacate Hass", "Aceite de oliva extra virgen", "Sal de mar"]
                    )
                ]
            elif target == "side":
                items = [
                    SuggestionItem(
                        title="Infusión Nocturna de Té de Hierbas Digestivo",
                        description="Bebida caliente de hierbas secas infundidas a 95°C para relajación nocturna.",
                        key_ingredients=["Hojas secas de té", "Agua de manantial"]
                    ),
                    SuggestionItem(
                        title="Infusión Fría de Té Verde con Menta de la Granja",
                        description="Extracto herbal helado preparado sin edulcorantes sintéticos.",
                        key_ingredients=["Hojas de té verde", "Menta fresca", "Agua purificada"]
                    ),
                    SuggestionItem(
                        title="Gelatina Casera de Jamaica y Canela",
                        description="Postre ligero ultraligero cuajado a 4°C para facilitar la digestión nocturna.",
                        key_ingredients=["Grenetina natural", "Flor de jamaica", "Canela"]
                    )
                ]
            else:
                items = [
                    SuggestionItem(
                        title="Salpicón Fresco de Pechuga de Pavo Desmenuzada",
                        description="Proteína magra desmenuzada con cebolla morada, limón y hierbas finas.",
                        key_ingredients=["Pechuga de pavo", "Jitomate bola", "Cilantro fresco"]
                    ),
                    SuggestionItem(
                        title="Ceviche Fresco de Filete de Pescado Blanco al Limón",
                        description="Cubos de pescado curados en jugo de limón fresco con aguacate Hass.",
                        key_ingredients=["Pescado blanco salvaje", "Aguacate Hass", "Limón fresco"]
                    ),
                    SuggestionItem(
                        title="Tartar de Atún Fresco con Aguacate Hass y Sésamo",
                        description="Lomo de atún fresco cortado a cuchillo con vinagreta de sésamo y aguacate.",
                        key_ingredients=["Atún fresco salvaje", "Aguacate Hass", "Aceite de sésamo"]
                    )
                ]
        else: # Comida
            if target == "starter":
                items = [
                    SuggestionItem(
                        title="Ensalada Verde de Arúgula y Espinaca Baby a la Vinagreta",
                        description="Mezcla de hojas tiernas de la granja aderezadas con aceite de oliva extra virgen.",
                        key_ingredients=["Arúgula fresca", "Espinacas baby", "Aceite de oliva extra virgen"]
                    ),
                    SuggestionItem(
                        title="Consomé Claro de Nopales y Hortalizas Tiernas",
                        description="Fondo de res desgrasado con nopales picados en brunoise y cilantro fresco.",
                        key_ingredients=["Consomé claro de res", "Nopales tiernos", "Cilantro fresco"]
                    ),
                    SuggestionItem(
                        title="Crema Ligera de Espárragos Verdes al Parmesano",
                        description="Sopa tersa licuada con espárragos de cosecha y mantequilla de pastoreo.",
                        key_ingredients=["Espárragos verdes", "Mantequilla de pastoreo", "Queso parmesano"]
                    )
                ]
            elif target == "side":
                items = [
                    SuggestionItem(
                        title="Espárragos Verdes Asados con Limón y Mantequilla",
                        description="Tallos de espárrago sellados a la plancha a 180°C con mantequilla de pastoreo.",
                        key_ingredients=["Espárragos verdes", "Mantequilla de pastoreo", "Limón"]
                    ),
                    SuggestionItem(
                        title="Chayote Tierno al Vapor con Mantequilla de Pastoreo",
                        description="Cubos de chayote de la granja cocinados al vapor con sal de mar marina.",
                        key_ingredients=["Chayote tierno", "Mantequilla de pastoreo", "Sal de mar"]
                    ),
                    SuggestionItem(
                        title="Bastones de Zucchini y Pepino al Limón y Sal de Mar",
                        description="Hortalizas frescas cortadas en bastones crujientes aderezadas a 4°C.",
                        key_ingredients=["Zucchini fresco", "Pepino fresco", "Aceite de oliva extra virgen"]
                    )
                ]
            else:
                items = [
                    SuggestionItem(
                        title="Ribeye de Res a la Sartén con Mantequilla de Tomillo",
                        description="Corte de res de pastoreo sellado a 230°C con mantequilla y romero.",
                        key_ingredients=["Ribeye de res", "Mantequilla de pastoreo", "Ajo", "Romero"]
                    ),
                    SuggestionItem(
                        title="Salmón Sellado en Costra de Ajonjolí con Salsa de Eneldo",
                        description="Lomo de salmón salvaje crocante por el lado de la piel con salsa de eneldo.",
                        key_ingredients=["Salmón salvaje", "Ajonjolí", "Aceite de oliva extra virgen"]
                    ),
                    SuggestionItem(
                        title="Pechuga de Pollo en Salsa Alfredo Tradicional",
                        description="Fajitas de pavo/pollo selladas a fuego lento bañadas en crema entera y parmesano.",
                        key_ingredients=["Pechuga de pollo/pavo", "Crema entera", "Queso parmesano"]
                    )
                ]

        return SuggestionResponse(suggestions=items)

    def negotiate_dish(self, request: NegotiationRequest) -> NegotiationResponse:
        diners = getattr(request, "diners_count", 6) or 6
        target = getattr(request, "target_field", "main") or "main"
        meal_type = getattr(request.current_meal, "meal_type", "Comida") or "Comida"

        # Si es solicitud de auto-sugerencias (Modo B exploración) o está vacío el prompt
        if request.is_auto_suggest or not (request.user_request or "").strip():
            sug_req = SuggestionRequest(
                meal_type=meal_type,
                target_field=target,
                current_dish_name=getattr(request.current_meal, f"{target}_name", "") or "",
                diners_count=diners
            )
            sug_res = self.suggest_alternative_dishes(sug_req)
            titles = [s.title for s in sug_res.suggestions]
            return NegotiationResponse(
                is_approved=False,
                rejection_reason="💡 Opciones alternativas recomendadas por el Cortex Gatekeeper del Atelier:",
                revised_meal=None,
                alternative_suggestions=titles
            )

        req_lower = request.user_request.lower()

        # Helper para obtener 3 sugerencias contextualmente válidas
        def get_fallback_suggestions() -> List[str]:
            s_res = self.suggest_alternative_dishes(SuggestionRequest(meal_type=meal_type, target_field=target, diners_count=diners))
            return [s.title for s in s_res.suggestions]

        # 1. Regla Directiva 6: Cero Leguminosas (Frijoles, Lentejas, Habas, Garbanzos)
        legumes = ["frijol", "frijoles", "lenteja", "lentejas", "haba", "habas", "garbanzo", "garbanzos", "alubia", "alubias"]
        for leg in legumes:
            if leg in req_lower:
                return NegotiationResponse(
                    is_approved=False,
                    rejection_reason=f"⚠️ Rechazado por el Cortex: Se prohíbe '{leg}' por restricción de leguminosas, alto contenido en carbohidratos netos y lectinas (Decálogo Directiva 6). He diseñado estas 3 opciones para ti:",
                    revised_meal=None,
                    alternative_suggestions=get_fallback_suggestions()
                )

        # 2. Regla Directiva 1: Cero Cerdo / Manteca de Cerdo / Tocino de Cerdo
        pork_terms = ["cerdo", "puerco", "chicharrón", "chicharron", "manteca"]
        for p in pork_terms:
            if p in req_lower:
                return NegotiationResponse(
                    is_approved=False,
                    rejection_reason=f"⚠️ Rechazado por el Cortex: Se prohíbe el uso de '{p}' y sus derivados por protocolo institucional T.I.L.O. (Decálogo Directiva 1). He diseñado estas 3 opciones para ti:",
                    revised_meal=None,
                    alternative_suggestions=get_fallback_suggestions()
                )

        # 3. Regla Directiva 2: Cero Capsaicina / Picante
        spicy_terms = ["chile", "habanero", "serrano", "jalapeño", "jalapeno", "chipotle", "picante", "salsa macha", "tabasco"]
        for s in spicy_terms:
            if s in req_lower:
                return NegotiationResponse(
                    is_approved=False,
                    rejection_reason=f"⚠️ Rechazado por el Cortex: Se prohíbe '{s}' por presencia de capsaicina irritante de la mucosa digestiva (Decálogo Directiva 2). He diseñado estas 3 opciones para ti:",
                    revised_meal=None,
                    alternative_suggestions=get_fallback_suggestions()
                )

        # 4. Regla Directivas 4 y 7: Cero Mezcla de Fruta con Lácteos y Cero Azúcar / Carbohidratos Netos Altos
        forbidden_carbs = ["azucar", "azúcar", "miel", "jarabe", "mango", "platano", "plátano", "piña", "manzana", "uva", "papa", "arroz", "pan", "tortilla de maiz", "pasta", "camote"]
        for f in forbidden_carbs:
            if f in req_lower:
                return NegotiationResponse(
                    is_approved=False,
                    rejection_reason=f"⚠️ Rechazado por el Cortex: La propuesta incluye '{f}', ingrediente de alto índice glucémico que interrumpe la cetosis. He diseñado estas 3 opciones para ti:",
                    revised_meal=None,
                    alternative_suggestions=get_fallback_suggestions()
                )

        # 5. Regla Mezcla Fruta + Lácteo (ej. Yoghurt con fruta o Pitaya con Yoghurt)
        if ("yoghurt" in req_lower or "yogurt" in req_lower or "leche" in req_lower or "queso" in req_lower) and any(fr in req_lower for fr in ["pitaya", "pitahaya", "fresa", "fresas", "higo", "higos", "durazno", "granada"]):
            return NegotiationResponse(
                is_approved=False,
                rejection_reason="⚠️ Rechazado por el Cortex: Se prohíbe combinar fruta fresca con lácteos en el mismo servicio (Decálogo Directiva 7). He diseñado estas 3 opciones para ti:",
                revised_meal=None,
                alternative_suggestions=get_fallback_suggestions()
            )

        revised = request.current_meal.model_copy(deep=True)

        if target == "starter":
            revised.starter_name = request.user_request
        elif target == "side":
            revised.side_dish_name = request.user_request
        else:
            revised.main_dish_name = request.user_request

        # Recompilar plan completo para diners_count
        plan = self._generate_fallback_weekly_plan(diners)

        # Re-evaluar inventario completo desde el backend
        full_shop_list = InventorySyncMaster.get_shopping_list_items(diners_count=diners)

        # Persistir en SQLite con conn.commit() garantizado ANTES de retornar HTTP 200 OK
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM weekly_plans WHERE diners_count = ?", (diners,))
                cursor.execute(
                    "INSERT INTO weekly_plans (week_start, diners_count, plan_json) VALUES (?, ?, ?)",
                    ("2026-08-16", diners, plan.model_dump_json())
                )
                conn.commit()  # COMMIT ATÓMICO ANTES DE SALIR
        except Exception as db_err:
            logger.error(f"Error al guardar plan negociado en SQLite: {db_err}")

        target_dish = getattr(revised, f"{target}_name", request.user_request) or request.user_request
        revised_phases = build_dynamic_prep_phases(target_dish, diners)

        return NegotiationResponse(
            is_approved=True,
            rejection_reason="",
            revised_meal=revised,
            alternative_suggestions=[],
            revised_prep_phases=revised_phases,
            full_recalculated_shopping_list=full_shop_list
        )

    def _generate_fallback_weekly_plan(self, diners_count: int) -> WeeklyMenuPlan:
        """
        Matriz de Menús Semana 34 (16 al 22 de Agosto de 2026)
        Escalado Proporcional Dinámico para `diners_count` comensales.
        """
        factor = diners_count / 6.0

        spec = [
            # DOMINGO 16 AGO
            {
                "day": "Domingo", "date_str": "16 AGO", "day_num": "16", "month": "Agosto",
                "preliminary": [
                    {
                        "base_name": "Mousse Keto de Frutos Rojos y Crema",
                        "ingredients": [("Fresas frescas", round(200.0 * factor, 1), "g"), ("Crema para batir sin azúcar", round(250.0 * factor, 1), "ml"), ("Queso crema", round(100.0 * factor, 1), "g")],
                        "cutting_prep": f"Procesar fresas en frío para {diners_count} personas.",
                        "cooking_process": "Batir crema con queso crema y fresas hasta espesar suavemente.",
                        "storage_reserve": "Mantener refrigerado a 4°C para el cierre dulce de la cena."
                    }
                ],
                "meals": [
                    ("Desayuno", f"{diners_count} Personas", "Pitahaya Fresca con Queso Cottage", "Quesadillas Keto en Crosta de Queso Gouda y Jamón de Pavo", "Café de Grano Recién Molido", 26.0, 22.0, 3.5, [("Queso Gouda", 60*diners_count, "g"), ("Jamón de pavo", 40*diners_count, "g"), ("Queso cottage", 50*diners_count, "g"), ("Café de grano / molido", 1*diners_count, "taza")]),
                    ("Comida", f"{diners_count} Personas en el servicio principal", "Calabacitas Asadas al Queso Parmesano", "Albóndigas de Res Rellenas de Huevo Cocido en Salsa Keto", "Gelatina Casera de Jamaica y Canela Sin Azúcar", 34.0, 36.0, 3.5, [("Carne molida de sirloin", 150*diners_count, "g"), ("Huevos enteros cocidos", 1*diners_count, "pza"), ("Jitomate Bola / Saladette", 80*diners_count, "g")]),
                    ("Cena", f"{diners_count} Personas", "Pico de Gallo Suave (Sin Chile)", "Parrillada de Agujas Norteñas y Carne para Asar al Comal", "Mousse Keto de Frutos Rojos y Crema", 38.0, 40.0, 3.2, [("Carne para asar / Agujas norteñas", 180*diners_count, "g"), ("Nopales tiernos", 2*diners_count, "pza"), ("Jitomate Bola / Saladette", 40*diners_count, "g")])
                ]
            },

            # LUNES 17 AGO
            {
                "day": "Lunes", "date_str": "17 AGO", "day_num": "17", "month": "Agosto",
                "preliminary": [
                    {
                        "base_name": "Puré de Coliflor con Mantequilla de Pastoreo",
                        "ingredients": [("Coliflor fresca", round(1.5 * factor, 2), "kg"), ("Mantequilla de vaca (sin sal)", round(100.0 * factor, 1), "g"), ("Dientes de ajo", round(10.0 * factor, 1), "g")],
                        "cutting_prep": f"Separar ramilletes de coliflor y lavar para {diners_count} personas.",
                        "cooking_process": "Cocinar al vapor 12 min y procesar con mantequilla y ajo hasta obtener consistencia tersa.",
                        "storage_reserve": "Reservar para acompañar el filete del almuerzo."
                    }
                ],
                "meals": [
                    ("Desayuno", f"{diners_count} Personas", "Espinacas Frescas Salteadas a la Mantequilla", "Omelette de 3 Claras de Huevo a Baja Temperatura (63°C) con Queso Panela", "Té Verde Botánico", 18.0, 24.0, 2.0, [("Claras de huevo", 3*diners_count, "pza"), ("Queso Panela", 50*diners_count, "g"), ("Espinacas frescas", 60*diners_count, "g")]),
                    ("Comida", f"{diners_count} Personas en el servicio principal", "Ensalada Verde de Arúgula de la Granja", "Filete de Res Magro (150g) al Sartén con Aceite de Coco", "Puré de Coliflor con Mantequilla de Pastoreo", 30.0, 38.0, 4.0, [("Filete de Res", 150*diners_count, "g"), ("Coliflor fresca", 200*diners_count, "g"), ("Mantequilla de vaca (sin sal)", 25*diners_count, "g")]),
                    ("Cena", f"{diners_count} Personas", "Abanico de Aguacate Hass con Limón", "Filete de Pescado Blanco al Sartén con Aceite de Oliva y Cilantro", "Gelatina Casera de Granada y Limón Sin Azúcar", 22.0, 26.0, 2.5, [("Filete de Pescado Blanco", 160*diners_count, "g"), ("Ejotes frescos", 80*diners_count, "g"), ("Aguacates Hass medianos", max(1, int(0.5*diners_count)), "pza")])
                ]
            },

            # MARTES 18 AGO
            {
                "day": "Martes", "date_str": "18 AGO", "day_num": "18", "month": "Agosto",
                "preliminary": [
                    {
                        "base_name": "Pudín de Chía con Leche de Coco y Fresas",
                        "ingredients": [("Semillas de chía", round(180.0 * factor, 1), "g"), ("Leche de coco (sin azúcar)", round(800.0 * factor, 1), "ml"), ("Nueces pecana", round(120.0 * factor, 1), "g"), ("Fresas frescas", round(150.0 * factor, 1), "g")],
                        "cutting_prep": f"Rebanar fresas frescas para {diners_count} personas.",
                        "cooking_process": "Mezclar chía con leche de coco en frío y dejar reposar 4 horas para hidratación activa.",
                        "storage_reserve": "Servir helado coronado con nueces pecana y fresas."
                    }
                ],
                "meals": [
                    ("Desayuno", f"{diners_count} Personas", "Fresas Frescas y Nueces Pecana", "Pudín de Chía Preparado con Leche de Coco Sin Azúcar y Nueces", "Café en grano / molido", 24.0, 10.0, 4.5, [("Semillas de chía", 30*diners_count, "g"), ("Leche de coco (sin azúcar)", 130*diners_count, "ml"), ("Nueces pecana", 20*diners_count, "g"), ("Fresas frescas", 25*diners_count, "g")]),
                    ("Comida", f"{diners_count} Personas en el servicio principal", "Espárragos Verdes Asados con Sal de Mar", "Filete de Salmón a la Plancha Sellado en Aceite de Coco", "Gelatina Keto de Vainilla y Canela Sin Azúcar", 32.0, 36.0, 3.2, [("Filete de Salmón", 180*diners_count, "g"), ("Brócoli fresco", 100*diners_count, "g"), ("Espárragos verdes", 80*diners_count, "g"), ("Mantequilla de vaca (sin sal)", 20*diners_count, "g")]),
                    ("Cena", f"{diners_count} Personas", "Champiñones Portobello Asados al Comal", "Pechuga de Pavo al Horno con Queso Gouda Gratinado", "Bastones de Pepino Fresco con Sal de Mar", 28.0, 22.0, 3.8, [("Pechuga de pavo", 150*diners_count, "g"), ("Queso Gouda", 40*diners_count, "g"), ("Brócoli fresco", 100*diners_count, "g")])
                ]
            },

            # MIÉRCOLES 19 AGO
            {
                "day": "Miércoles", "date_str": "19 AGO", "day_num": "19", "month": "Agosto",
                "preliminary": [
                    {
                        "base_name": "Salsa en Nogada Tradicional",
                        "ingredients": [("Nuez de Castilla fresca", round(300.0 * factor, 1), "g"), ("Queso de cabra artesanal", round(100.0 * factor, 1), "g"), ("Leche de vaca / Crema para batir", round(240.0 * factor, 1), "ml"), ("Vino blanco seco / Jerez", round(30.0 * factor, 1), "ml"), ("Granada fresca", round(100.0 * factor, 1), "g"), ("Perejil fresco", round(20.0 * factor, 1), "g")],
                        "cutting_prep": f"Limpiar las nueces: Sumergir nueces de Castilla en agua tibia durante unos minutos para retirar la piel de color canela que recubre la nuez y aporta amargor para {diners_count} personas.",
                        "cooking_process": "Licuar la base y dar textura: Licuar nueces limpias con queso de cabra y la mitad de la leche a velocidad media-alta. Añadir el resto de la leche poco a poco hasta lograr consistencia de crema ligera. Incorporar el jerez seco y pizca de canela.",
                        "storage_reserve": "Reposo en frío: Guardar la nogada en recipiente de vidrio en refrigeración a 4°C por al menos 30 min para asentar sabores y cuerpo antes de napar."
                    }
                ],
                "meals": [
                    ("Desayuno", f"{diners_count} Personas", "Nopales Tiernos Asados al Comal", "Huevos Pochados en Cama de Espinacas", "Té de hierbas digestivo", 24.0, 18.0, 3.0, [("Huevos enteros", 2*diners_count, "pza"), ("Espinacas frescas", 100*diners_count, "g"), ("Ajo picado", 10*diners_count, "g"), ("Queso parmesano o de cabra", 20*diners_count, "g")]),
                    ("Comida", f"{diners_count} Personas en el servicio principal", "Ensalada Verde de Arúgula de la Granja", "Picadillo de Atún con Nogada Tradicional", "Gelatina Casera de Jamaica y Menta Sin Azúcar", 34.0, 36.0, 3.5, [("Medallones de atún fresco", 150*diners_count, "g"), ("Manzana / Pera / Durazno picados", 40*diners_count, "g"), ("Nuez de Castilla fresca", 30*diners_count, "g"), ("Queso de cabra artesanal", 20*diners_count, "g"), ("Granada fresca", 15*diners_count, "g")]),
                    ("Cena", f"{diners_count} Personas", "Rodajas de Calabacitas Verdes Salteadas", "Pechuga de Pollo Desmenuzada a las Hierbas Secas al Sartén", "Mousse Keto de Limón y Queso Crema", 32.0, 36.0, 3.8, [("Pechuga de pollo", 180*diners_count, "g"), ("Queso crema", 40*diners_count, "g"), ("Limones frescos", 2*diners_count, "pza")])
                ]
            },

            # JUEVES 20 AGO
            {
                "day": "Jueves", "date_str": "20 AGO", "day_num": "20", "month": "Agosto",
                "preliminary": [
                    {
                        "base_name": "Mantequilla de Hierbas Finas de la Granja",
                        "ingredients": [("Mantequilla de vaca (sin sal)", round(200.0 * factor, 1), "g"), ("Hierbas secas (Orégano/Tomillo)", round(10.0 * factor, 1), "g"), ("Dientes de ajo", round(5.0 * factor, 1), "g")],
                        "cutting_prep": f"Picar hierbas y ajo extremadamente finos para {diners_count} personas.",
                        "cooking_process": "Acremar mantequilla a temperatura ambiente e integrar las hierbas finas.",
                        "storage_reserve": "Formar rodillo en papel encerado y refrigerar."
                    }
                ],
                "meals": [
                    ("Desayuno", f"{diners_count} Personas", "Ejotes Frescos Salteados en Aceite de Coco", "Huevos Revueltos a Baja Temperatura (63°C) con Tocino de Pavo Picado", "Té de hierbas digestivo", 24.0, 18.0, 3.0, [("Huevos enteros", 2*diners_count, "pza"), ("Ejotes frescos", 60*diners_count, "g"), ("Tocino de pavo", 40*diners_count, "g")]),
                    ("Comida", f"{diners_count} Personas en el servicio principal", "Brócoli Fresco al Vapor con Mantequilla", "Filete de Res en Crosta de Parmesano y Mantequilla de Hierbas", "Gelatina Casera de Granada Sin Azúcar", 38.0, 42.0, 3.2, [("Filete de Res", 180*diners_count, "g"), ("Brócoli fresco", 100*diners_count, "g"), ("Mantequilla de vaca (sin sal)", 20*diners_count, "g")]),
                    ("Cena", f"{diners_count} Personas", "Ensalada de Hojas Verdes de la Granja", "Pechuga de Pollo Rellena de Queso Crema y Espinacas al Horno", "Bastones de Zucchini Fresco con Sal de Mar", 26.0, 34.0, 2.8, [("Pechuga de pollo", 180*diners_count, "g"), ("Queso crema", 40*diners_count, "g"), ("Espinacas frescas", 50*diners_count, "g")])
                ]
            },

            # VIERNES 21 AGO
            {
                "day": "Viernes", "date_str": "21 AGO", "day_num": "21", "month": "Agosto",
                "preliminary": [
                    {
                        "base_name": "Puré de Coliflor con Queso Parmesano",
                        "ingredients": [("Coliflor fresca", round(1.5 * factor, 2), "kg"), ("Mantequilla de vaca (sin sal)", round(100.0 * factor, 1), "g"), ("Queso parmesano", round(60.0 * factor, 1), "g")],
                        "cutting_prep": f"Separar ramilletes de coliflor y lavar para {diners_count} personas.",
                        "cooking_process": "Cocinar al vapor 12 min y procesar con mantequilla y queso parmesano.",
                        "storage_reserve": "Reservar para acompañar el pescado blanco."
                    }
                ],
                "meals": [
                    ("Desayuno", f"{diners_count} Personas", "Fresas Frescas de la Cosecha con Queso Cottage", "Omelette de Huevo de Granja con Jamón de Pavo y Queso Gouda", "Café de Grano Recién Molido", 22.0, 24.0, 3.2, [("Huevos enteros", 3*diners_count, "pza"), ("Queso Gouda", 50*diners_count, "g"), ("Jamón de pavo", 40*diners_count, "g")]),
                    ("Comida", f"{diners_count} Personas en el servicio principal", "Ensalada de Hojas Verdes Mixtas con Aceite de Oliva", "Filete de Pescado Blanco al Vapor con Mantequilla de Ajo y Cilantro", "Puré de Coliflor con Queso Parmesano", 36.0, 38.0, 3.5, [("Filete de Pescado Blanco", 180*diners_count, "g"), ("Coliflor fresca", 150*diners_count, "g"), ("Mantequilla de vaca (sin sal)", 20*diners_count, "g")]),
                    ("Cena", f"{diners_count} Personas", "Pico de Gallo Suave (Sin Chile)", "Chicharrón de Queso Gouda al Comal", "Mousse Keto de Frutos Rojos y Crema", 24.0, 28.0, 2.5, [("Queso Gouda", 80*diners_count, "g"), ("Crema para batir sin azúcar", 40*diners_count, "g"), ("Fresas frescas", 30*diners_count, "g")])
                ]
            },

            # SÁBADO 22 AGO
            {
                "day": "Sábado", "date_str": "22 AGO", "day_num": "22", "month": "Agosto",
                "preliminary": [
                    {
                        "base_name": "Aderezo al Pastor Keto sin Azúcar",
                        "ingredients": [("Achiote puro en barra", round(40.0 * factor, 1), "g"), ("Vinagre de manzana orgánico", round(60.0 * factor, 1), "ml"), ("Dientes de ajo", round(15.0 * factor, 1), "g"), ("Orégano seco", round(5.0 * factor, 1), "g")],
                        "cutting_prep": f"Licuar achiote con vinagre y especias para {diners_count} personas.",
                        "cooking_process": "Macerar la pechuga de pavo durante 20 min antes de asar.",
                        "storage_reserve": "Aderezar el pavo al pastor keto al comal."
                    }
                ],
                "meals": [
                    ("Desayuno", f"{diners_count} Personas", "Hojas de Arúgula Fresca con Aceite de Oliva", "Hot Cakes de Harina de Almendras (Keto) con Claras a Baja Temperatura", "Té Verde Botánico", 26.0, 20.0, 3.8, [("Harina de almendras (Keto)", 40*diners_count, "g"), ("Claras de huevo", 2*diners_count, "pza"), ("Arúgula fresca", 40*diners_count, "g")]),
                    ("Comida", f"{diners_count} Personas en el servicio principal", "Rodajas de Nopales Tiernos Asados al Comal", "Pechuga de Pavo al Pastor Keto Gratinada con Queso Gouda", "Gelatina Casera de Vainilla y Canela Sin Azúcar", 34.0, 36.0, 3.5, [("Pechuga de pavo", 180*diners_count, "g"), ("Queso Gouda", 60*diners_count, "g"), ("Achiote puro", 10*diners_count, "g")]),
                    ("Cena", f"{diners_count} Personas", "Ensalada Verde de Espinacas de la Granja", "Champiñones Portobello Rellenos de Queso Gouda y Jamón de Pavo al Horno", "Guacamole Casero con Totopos Keto de Queso", 36.0, 26.0, 3.2, [("Champiñones Portobello", 2*diners_count, "pza"), ("Queso Gouda", 60*diners_count, "g"), ("Jamón de pavo", 40*diners_count, "g"), ("Aguacates Hass medianos", max(1, int(1*diners_count)), "pza")])
                ]
            }
        ]

        self._validate_menu_diversity(spec)

        daily_menus = []
        for d in spec:
            prelim_list = []
            for p in d["preliminary"]:
                prelim_list.append(PreliminaryPrep(
                    base_name=p["base_name"],
                    ingredients=[Ingredient(name=in_name, quantity=in_qty, unit=in_unit) for in_name, in_qty, in_unit in p["ingredients"]],
                    cutting_prep=p["cutting_prep"],
                    cooking_process=p["cooking_process"],
                    storage_reserve=p["storage_reserve"]
                ))

            meals = []
            meal_prep_blocks = []
            sec1_functional = []
            sec2_tables = []
            sec3_glycemic_synergies = []

            for m_type, din_spec, st_name, m_name, sd_name, fat, prot, carbs, ings in d["meals"]:
                meal_obj = Meal(
                    meal_type=m_type,
                    starter_name=st_name,
                    main_dish_name=m_name,
                    side_dish_name=sd_name,
                    fat_g=round(fat * factor, 1), protein_g=round(prot * factor, 1), net_carbs_g=carbs,
                    ingredients=[Ingredient(name=in_name, quantity=in_qty, unit=in_unit) for in_name, in_qty, in_unit in ings]
                )
                meals.append(meal_obj)

                # Procedimiento de preparación paso a paso real usando el Repositorio de Recetas Dinámico
                def build_dish_procedure(d_name: str, diners: int) -> DishProcedure:
                    if "Evento Especial" in d_name or "Restaurante" in d_name:
                        return DishProcedure(
                            dish_name=d_name,
                            steps=[
                                RecipeStep(step_number=1, title="Evento Especial", instruction="Servicio externo en restaurante de aniversario."),
                                RecipeStep(step_number=2, title="Elección Keto", instruction="Selección de platillos sin carbohidratos en carta.")
                            ]
                        )
                    return RecipeRepositoryManager.get_procedure(d_name, diners)

                    # 9. Calabacitas Asadas al Queso Parmesano / Gratinados
                    if any(k in d_lower for k in ["gratinad", "lasaña", "lasagna"]) or ("calabacita" in d_lower and any(k in d_lower for k in ["parmesan", "horno"])):
                        return DishProcedure(
                            dish_name=d_name,
                            phase_1=f"Cortar las calabacitas: Lavado meticuloso en frío, retirar extremos y cortar en rodajas de 0.5 cm de grosor o láminas longitudinales tipo lasaña para {diners} comensales.",
                            phase_2=f"Sellar las calabacitas: Calentar aceite de oliva virgen extra en sartén grande a fuego medio-alto. Saltear rodajas 3 a 5 min por lado sazonando con sal de mar, pimienta y ajo en polvo hasta dorar ligeramente pero firmes. Precalentar horno a 200°C.",
                            phase_3=f"Armar el platillo: En un refractario apto para horno, extender una capa delgada de salsa de tomate keto en el fondo. Colocar capa de calabacitas, espolvorear porción generosa de queso parmesano y mozzarella. Repetir en capas terminando con queso abundante arriba.",
                            phase_4=f"Gratinar y Servir: Hornear a 200°C durante 15 a 20 min hasta que la salsa burbujee y el queso dore (grill 2 min finales opcional). Retirar, decorar con hojas de albahaca fresca y servir caliente."
                        )

                    # Perfil 5: Vegetales Asados / Salteados
                    if any(k in d_lower for k in ["calabacita", "ejote", "brócoli", "nopal", "ensalada verde", "parmesano"]):
                        return DishProcedure(
                            dish_name=d_name,
                            phase_1=f"Lavado, desinfección y corte en julianas o rodajas finas para {d_name}.",
                            phase_2=f"Blanqueado breve o sazonado con ajo y aceite de oliva virgen extra para {diners} comensales.",
                            phase_3=f"Salteado rápido a fuego medio en sartén para preservar crocantez y clorofila.",
                            phase_4=f"Servir como acompañamiento tibio con queso parmesano o semillas."
                        )

                    # Perfil 6: Proteínas y Platos Fuertes Calientes (Aceite de coco / Mantequilla)
                    return DishProcedure(
                        dish_name=d_name,
                        phase_1=f"Limpieza e higienización de la proteína e insumos de la granja para {d_name}.",
                        phase_2=f"Troceado, molienda o marinado exacto para {diners} comensales.",
                        phase_3=f"Cocción sellada a fuego medio/lento predominantemente en aceite de coco u oliva/mantequilla.",
                        phase_4=f"Porcionado de plato caliente a 65°C de temperatura de servicio."
                    )

                starter_proc = build_dish_procedure(st_name, diners_count)
                main_proc = build_dish_procedure(m_name, diners_count)
                side_proc = build_dish_procedure(sd_name, diners_count)

                meal_prep_blocks.append(MealPrepBlock(
                    meal_type=m_type,
                    diners_spec=din_spec,
                    starter=starter_proc,
                    main_dish=main_proc,
                    side_dish=side_proc
                ))

                # SECCIÓN 1 NUTR: Justificación Nutricional Cualitativa y Funcional
                if "Evento Especial" in st_name or "Restaurante" in st_name:
                    sec1_functional.append(MealFunctionalAnalysis(
                        meal_type=m_type,
                        diners_spec=din_spec,
                        starter_justification=FunctionalJustification(
                            category_title="Evento Social y Registro Libre",
                            source_ingredient="Restaurante de Aniversario",
                            physiological_impact="Se recomienda seleccionar proteínas magras, ensaladas verdes y evitar carbohidratos simples."
                        ),
                        main_justification=FunctionalJustification(
                            category_title="Plato Fuerte en Restaurante",
                            source_ingredient="Cena de Aniversario",
                            physiological_impact="Mantener consumo de vegetales de hoja y carnes a la parrilla/horno."
                        ),
                        side_justification=FunctionalJustification(
                            category_title="Acompañamiento Libre",
                            source_ingredient="Restaurante",
                            physiological_impact="Optar por agua mineral con limón y vegetales asados."
                        )
                    ))
                else:
                    sec1_functional.append(MealFunctionalAnalysis(
                        meal_type=m_type,
                        diners_spec=din_spec,
                        starter_justification=FunctionalJustification(
                            category_title="Fibra viva, antioxidantes y enzimas digestivas",
                            source_ingredient=st_name,
                            physiological_impact="Acondiciona el tracto gastrointestinal y amortigua el vaciamiento gástrico."
                        ),
                        main_justification=FunctionalJustification(
                            category_title="Proteínas de alto valor biológico y lípidos esenciales",
                            source_ingredient=m_name,
                            physiological_impact="Activa la síntesis proteica muscular, proporciona saciedad prolongada y mantiene insulina basal plana."
                        ),
                        side_justification=FunctionalJustification(
                            category_title="Micronutrientes y volumen sin carga glucémica",
                            source_ingredient=sd_name,
                            physiological_impact="Aporta electrolitos esenciales (Potasio, Magnesio) sin interferir con la cetosis."
                        )
                    ))

                # SECCIÓN 2 NUTR: Matriz Cuantitativa Estandarizada (Nutrition Facts)
                calories_blk = round((fat * 9 + prot * 4 + carbs * 4) * factor, 1) if fat > 0 else 0.0
                sec2_tables.append(MealNutritionFactTable(
                    meal_type=m_type,
                    portion_size=f"1 servicio completo para {din_spec}",
                    total_calories_kcal=calories_blk,
                    facts=[
                        NutritionFactItem(nutrient_name="Grasas Totales", amount_str=f"{round(fat * factor, 1)} g", daily_value_pct=f"{int((fat * factor / 70.0) * 100)}%"),
                        NutritionFactItem(nutrient_name="Grasas Saturadas", amount_str=f"{round(fat * factor * 0.35, 1)} g", daily_value_pct=f"{int((fat * factor * 0.35 / 20.0) * 100)}%"),
                        NutritionFactItem(nutrient_name="Proteína de Valor", amount_str=f"{round(prot * factor, 1)} g", daily_value_pct=f"{int((prot * factor / 50.0) * 100)}%"),
                        NutritionFactItem(nutrient_name="Carbohidratos Netos", amount_str=f"{round(carbs, 1)} g", daily_value_pct=f"{int((carbs / 25.0) * 100)}%"),
                        NutritionFactItem(nutrient_name="Fibra Dietética", amount_str="4.5 g" if fat > 0 else "0.0 g", daily_value_pct="18%" if fat > 0 else "0%"),
                        NutritionFactItem(nutrient_name="Colesterol", amount_str="280 mg" if fat > 0 else "0 mg", daily_value_pct="93%" if fat > 0 else "0%"),
                        NutritionFactItem(nutrient_name="Sodio", amount_str="450 mg" if fat > 0 else "0 mg", daily_value_pct="20%" if fat > 0 else "0%")
                    ],
                    base_ingredients=[ing.name for ing in meal_obj.ingredients] if meal_obj.ingredients else [st_name, m_name, sd_name]
                ))

                # SECCIÓN 3 NUTR: Análisis Clínico de IG y Sinergia Metabólica
                sec3_glycemic_synergies.append(MealGlycemicSynergy(
                    meal_type=m_type,
                    food_analyses=[
                        FoodGlycemicAnalysis(
                            food_name=st_name,
                            ig_range="IG 15-30 (Bajo)",
                            risk_category="Riesgo Mínimo",
                            physiological_reason="Matriz de insumos frescos que mantiene la glucemia plana."
                        ),
                        FoodGlycemicAnalysis(
                            food_name=m_name,
                            ig_range="IG 0 (Nulo)",
                            risk_category="Sin Riesgo Glucémico",
                            physiological_reason="Proteínas magras y lípidos cetogénicos de alta biodisponibilidad."
                        ),
                        FoodGlycemicAnalysis(
                            food_name=sd_name,
                            ig_range="IG 10-25 (Muy Bajo)",
                            risk_category="Riesgo Bajo",
                            physiological_reason="Acompañamiento rico en fibra y minerales."
                        )
                    ],
                    synergy_summary=f"En {m_type}, la combinación cetogénica para {diners_count} personas garantiza saciedad y estabilidad metabólica."
                ))

            def resolve_keto_dish_alias(d_name: str) -> str:
                if not d_name:
                    return d_name
                lower = d_name.lower()
                if "frijol" in lower or "frijoles" in lower:
                    return "Consomé Claro de Nopales y Hortalizas Tiernas"
                if "chipotle" in lower:
                    d_name = re.sub(r'chipotle', 'Ajo y Tomillo', d_name, flags=re.IGNORECASE)
                if "arroz" in lower and "coliflor" not in lower:
                    d_name = re.sub(r'arroz', 'Cuscús de Coliflor', d_name, flags=re.IGNORECASE)

                # PATCH V13.2 & V13.3: NOMENCLATURA GASTRONÓMICA Y DEPURACIÓN SENSORIAL
                d_name = re.sub(r'\s*Keto\b', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\s*Cetogénico\b', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\s*Cetogénica\b', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\s*Low-Carb\b', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\(Fideos Keto\)', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\(Keto\)', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\s*Sin Azúcar\b', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\s*Sin Azucar\b', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\s*Zero\b', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\s*Dietético\b', '', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'de Grenetina con', 'de', d_name, flags=re.IGNORECASE)
                d_name = re.sub(r'\s+', ' ', d_name).strip()
                return d_name


            recipes = []
            for m in meals:
                if "Restaurante" not in m.main_dish_name:
                    n = diners_count
                    p_name = resolve_keto_dish_alias(m.main_dish_name)
                    p_phases = build_dynamic_prep_phases(p_name, n)

                    recipes.append(PreparationRecipe(
                        dish_name=p_name,
                        category=m.meal_type,
                        prep_time_min=20,
                        phase_1=p_phases.fase_1_mise_en_place,
                        phase_2=p_phases.fase_2_acondicionamiento,
                        phase_3=p_phases.fase_3_termodinamica,
                        phase_4=p_phases.fase_4_servicio,
                        scaled_ingredients=m.ingredients
                    ))

            sec3_clinical = ClinicalGlycemicSection(
                micro_analyses=sec3_glycemic_synergies,
                macro_daily_summary=f"Evaluación Fisiológica de {d['day']} ({d['date_str']}): Estabilidad cetogénica constante para {diners_count} personas, control de insulina basal y soporte metabólico optimizado."
            )

            comprehensive_nutr = ComprehensiveNutritionView(
                section_1_functional=sec1_functional,
                section_2_tables=sec2_tables,
                section_3_glycemic=sec3_clinical
            )

            nutrition = NutritionMetrics(
                calories_kcal=round(1550.0 * factor, 1),
                total_fat_g=round(124.0 * factor, 1),
                sat_fat_g=round(40.0 * factor, 1),
                cholesterol_mg=370.0,
                sodium_mg=1400.0,
                net_carbs_g=8.5,
                fiber_g=14.0,
                protein_g=round(98.0 * factor, 1),
                ig_impact="Bajo (Curva glucémica plana / Sin picos)",
                metabolic_notes=f"Cetosis óptima para la Semana 33 ajustada dinámicamente para {diners_count} comensales."
            )

            full_title = f"Menú Completo para el {d['day']} {d['day_num']} de {d['month']} ({diners_count} Personas)"

            daily_menus.append(DailyMenu(
                day=d["day"],
                date_str=d["date_str"],
                day_num=d["day_num"],
                full_date_title=full_title,
                preliminary_preps=prelim_list,
                meal_prep_blocks=meal_prep_blocks,
                meals=meals,
                recipes=recipes,
                clinical_nutrition=comprehensive_nutr,
                nutrition=nutrition
            ))

        return WeeklyMenuPlan(diners_count=diners_count, days=daily_menus)



from fastapi import HTTPException
from app.schemas import TypedRecipeSchema, CulinaryTechniqueEnum, IngredientGroupSchema, IngredientItemSchema
from app.services.recipe_validator import validate_recipe_compliance

def generate_validated_typed_recipe(dish_name: str, course_type: str = "starter", max_retries: int = 3) -> TypedRecipeSchema:
    """
    Genera y valida una receta cumpliendo estrictamente con la Directiva Sistémica Vinculante V15.25.2.
    Aplica hasta max_retries reintentos. Si se agotan los reintentos, lanza una excepción HTTP 502 explícita.
    """
    clean_title = dish_name.strip()
    clean_lower = clean_title.lower()
    last_error = ""

    for attempt in range(1, max_retries + 1):
        # 1. Determinar técnica culinaria real
        technique = CulinaryTechniqueEnum.SAUTE_AND_SEAR
        if any(kw in clean_lower for kw in ["fresas", "higos", "moras", "kiwi", "zarzamoras", "frambuesas", "durazno", "pitahaya", "granada", "carambola", "maracuyá", "arándanos", "ensalada", "coctel", "carpaccio", "bastones", "abanico"]):
            technique = CulinaryTechniqueEnum.RAW_ASSEMBLY
        elif any(kw in clean_lower for kw in ["crema", "sopa", "consomé", "puchero"]):
            technique = CulinaryTechniqueEnum.BOIL_AND_BLEND
        elif any(kw in clean_lower for kw in ["pochado", "çılbır"]):
            technique = CulinaryTechniqueEnum.POACH_AND_EMULSION
        elif any(kw in clean_lower for kw in ["omelette", "revueltos", "frittata", "scramble", "waffles", "crepas", "panqueques", "muffins"]):
            technique = CulinaryTechniqueEnum.PAN_FRY_EGG
        elif any(kw in clean_lower for kw in ["asado", "gratinado", "horno", "relleno"]):
            technique = CulinaryTechniqueEnum.ROAST_BAKE
        elif any(kw in clean_lower for kw in ["té", "infusión", "tisana"]):
            technique = CulinaryTechniqueEnum.STEEP_BEVERAGE
        elif any(kw in clean_lower for kw in ["gelatina", "mousse"]):
            technique = CulinaryTechniqueEnum.GELATIN_MOLDING

        # 2. Generar grupos de ingredientes desglosados
        groups = []
        if technique == CulinaryTechniqueEnum.RAW_ASSEMBLY:
            fruit_item = clean_title.split(" con ")[0] if " con " in clean_title else clean_title
            groups = [
                IngredientGroupSchema(
                    category="🌱 Fruta / Base Viva",
                    items=[IngredientItemSchema(name=f"{fruit_item} frescas", base_qty_per_person=75.0, unit="g", source="Granja El Herami", unit_cost=0.0)]
                ),
                IngredientGroupSchema(
                    category="🥑 Frutos Secos y Fibra Cetogénica",
                    items=[
                        IngredientItemSchema(name="Nuez de Castilla troceada / Almendras tostadas", base_qty_per_person=15.0, unit="g", source="Granja El Herami", unit_cost=0.0),
                        IngredientItemSchema(name="Semillas de chía orgánicas", base_qty_per_person=5.0, unit="g", source="Granja El Herami", unit_cost=0.0)
                    ]
                ),
                IngredientGroupSchema(
                    category="🥛 Base Cremosa y Aromáticos",
                    items=[
                        IngredientItemSchema(name="Yogur griego natural sin azúcar / Crema de coco", base_qty_per_person=30.0, unit="g", source="Mercado", unit_cost=5.0),
                        IngredientItemSchema(name="Hojas de menta fresca y pizca de canela", base_qty_per_person=2.0, unit="g", source="Granja El Herami", unit_cost=0.0)
                    ]
                )
            ]
            steps = [
                f"1. Higienizado y Corte: Lavar y desinfectar los insumos de {clean_title}; retirar pedúnculo y cortar en cuartos longitudinales.",
                "2. Tostado de Frutos Secos: Tostar ligeramente las nueces en sartén seca a fuego muy bajo durante 2 minutos (sin grasa) para resaltar aceites esenciales; dejar enfriar.",
                "3. Hidratación y Ensamble: Mezclar la chía con el yogur griego (o disponerla sobre la fruta). Disponer los insumos frescos en 6 cuencos individuales.",
                "4. Montaje Final: Distribuir las nueces troceadas, espolvorear la chía y coronar con hojas de menta fresca. Servir fresco a 6–8°C."
            ]
        elif technique == CulinaryTechniqueEnum.GELATIN_MOLDING or technique == CulinaryTechniqueEnum.STEEP_BEVERAGE:
            is_gel = technique == CulinaryTechniqueEnum.GELATIN_MOLDING
            groups = [
                IngredientGroupSchema(
                    category="🍵 Base / Infusión",
                    items=[
                        IngredientItemSchema(name="Grenetina natural de colágeno" if is_gel else "Hojas de infusión botánica", base_qty_per_person=10.0 if is_gel else 3.0, unit="g", source="Granja El Herami", unit_cost=0.0),
                        IngredientItemSchema(name="Agua purificada o extracto frutal vivo", base_qty_per_person=100.0, unit="ml", source="Granja El Herami", unit_cost=0.0)
                    ]
                )
            ]
            steps = [
                "1. Hidratar la grenetina en agua fría e infusionar a 85°C." if is_gel else "1. Infusionar la mezcla botánica en agua caliente a 85°C por 5 minutos.",
                "2. Verter en moldes individuales y refrigerar a 4°C por 3 horas." if is_gel else "2. Colar y servir caliente o con hielo mineral.",
                "3. Servir frío libre de carbohidratos netos." if is_gel else "3. Servir de inmediato."
            ]
        else:
            prot_item = clean_title.split(" ")[0]
            groups = [
                IngredientGroupSchema(
                    category="🥩 Proteína Principal",
                    items=[IngredientItemSchema(name=f"{prot_item} seleccionado", base_qty_per_person=150.0, unit="g", source="Mercado", unit_cost=35.0)]
                ),
                IngredientGroupSchema(
                    category="🧈 Grasas Saludables y Sazón",
                    items=[
                        IngredientItemSchema(name="Mantequilla de pastoreo / Aceite VEVO", base_qty_per_person=10.0, unit="g", source="Granja El Herami", unit_cost=0.0),
                        IngredientItemSchema(name="Sal de mar, tomillo y ajo rostizado", base_qty_per_person=2.0, unit="g", source="Granja El Herami", unit_cost=0.0)
                    ]
                )
            ]
            steps = [
                f"1. Atemperar y sazonar {clean_title} con sal de mar y hierbas finas.",
                "2. Calentar la grasa en sartén de hierro a 180°C y sellar la proteína hasta dorar.",
                "3. Dejar reposar 3 minutos para redistribuir jugos y servir caliente."
            ]

        candidate = TypedRecipeSchema(
            title=clean_title,
            cooking_technique=technique,
            sensory_description=f"Preparación artesanal de {clean_title} optimizada para nutrición cetogénica celular y balance de macronutrientes.",
            ingredient_groups=groups,
            steps=steps
        )

        is_valid, reason = validate_recipe_compliance(candidate)
        if is_valid:
            return candidate

        last_error = f"Reintento {attempt}: {reason}"

    # ESTADO TERMINAL EXPLÍCITO V15.25.2
    raise HTTPException(
        status_code=502,
        detail=f"Fallo de coherencia gastronómica tras {max_retries} intentos. Motivo final: {last_error}"
    )



def get_canonical_benedictine_recipe(dish_name: str) -> dict:
    return {
        "title": "Huevos Benedictinos Keto sobre Nube de Clara y Tocino de Pavo Crujiente con Salsa Holandesa Casera",
        "cooking_technique": "poach_and_emulsion",
        "sensory_description": "Versión gourmet cetogénica que sustituye el pan tradicional por huevos nube esponjosos y horneados, coronados con tocino de pavo crujiente, huevo pochado de yema fluida y salsa holandesa emulsionada a baño maría.",
        "ingredient_groups": [
            {
                "category": "☁️ Bases de Huevo Nube (2 unidades)",
                "items": [
                    {"name": "Claras de huevo (temperatura ambiente)", "base_qty_per_person": 1.0, "unit": "piezas", "source": "Granja El Herami", "unit_cost": 0.0},
                    {"name": "Sal marina", "base_qty_per_person": 0.5, "unit": "g", "source": "Granja El Herami", "unit_cost": 0.0},
                    {"name": "Crémor tártaro o jugo de limón", "base_qty_per_person": 0.5, "unit": "g", "source": "Granja El Herami", "unit_cost": 0.0},
                    {"name": "Queso Parmesano finamente rallado", "base_qty_per_person": 10.0, "unit": "g", "source": "Mercado", "unit_cost": 8.0}
                ]
            },
            {
                "category": "🥓 Cubierta y Proteína",
                "items": [
                    {"name": "Tocino de pavo artesanal", "base_qty_per_person": 2.0, "unit": "piezas", "source": "Granja El Herami", "unit_cost": 0.0},
                    {"name": "Huevos frescos enteros (para pochar)", "base_qty_per_person": 1.0, "unit": "piezas", "source": "Granja El Herami", "unit_cost": 0.0},
                    {"name": "Vinagre blanco (para pochado)", "base_qty_per_person": 7.5, "unit": "ml", "source": "Granja El Herami", "unit_cost": 0.0}
                ]
            },
            {
                "category": "🧈 Salsa Holandesa Casera",
                "items": [
                    {"name": "Yemas de huevo frescas", "base_qty_per_person": 1.0, "unit": "piezas", "source": "Granja El Herami", "unit_cost": 0.0},
                    {"name": "Mantequilla sin sal derretida tibia", "base_qty_per_person": 37.5, "unit": "g", "source": "Mercado", "unit_cost": 15.0},
                    {"name": "Jugo de limón recién exprimido", "base_qty_per_person": 2.5, "unit": "ml", "source": "Granja El Herami", "unit_cost": 0.0},
                    {"name": "Agua tibia", "base_qty_per_person": 2.5, "unit": "ml", "source": "Granja El Herami", "unit_cost": 0.0},
                    {"name": "Pimienta de cayena y sal marina", "base_qty_per_person": 0.5, "unit": "g", "source": "Granja El Herami", "unit_cost": 0.0}
                ]
            },
            {
                "category": "🌿 Servicio y Decoración",
                "items": [
                    {"name": "Cebollín fresco o eneldo picado", "base_qty_per_person": 2.0, "unit": "g", "source": "Granja El Herami", "unit_cost": 0.0},
                    {"name": "Pimienta negra recién molida", "base_qty_per_person": 0.5, "unit": "g", "source": "Granja El Herami", "unit_cost": 0.0}
                ]
            }
        ],
        "steps": [
            "1. Hornear los Huevos Nube: Precalentar horno a 180°C. Batir las claras con sal y crémor tártaro a velocidad alta hasta picos firmes. Integrar suavemente el parmesano rallado con espátula. Formar nidos sobre papel encerado y horneado por 10-12 minutos hasta dorar ligero.",
            "2. Cocinar el Tocino de Pavo: Dorar las tiras de tocino de pavo en sartén seca a fuego medio hasta que queden crujientes por ambos lados; escurrir sobre papel absorbente.",
            "3. Elaborar la Salsa Holandesa a Baño María: En un tazón sobre agua hirviendo suave (sin tocar el agua), batir las yemas con agua y jugo de limón hasta espesar. Verter la mantequilla derretida tibia en hilo fino sin parar de batir hasta emulsionar terso y cremoso. Sazonar con cayena y reservar tibio.",
            "4. Pochar los Huevos: Calentar agua con vinagre a 85°C–90°C (burbujeo suave). Crear un remolino con cuchara, verter el huevo deslizado suavemente y pochar durante 3 minutos exactos para mantener la yema fluida.",
            "5. Armado y Montaje: Colocar la base de huevo nube caliente, disponer dos tiras de tocino de pavo cruzadas, asentar el huevo pochado en el centro, cubrir con salsa holandesa tibia y coronar con cebollín picado y pimienta negra."
        ]
    }
