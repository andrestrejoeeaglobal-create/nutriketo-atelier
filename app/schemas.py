import re
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, model_validator

class Ingredient(BaseModel):
    name: str = Field(..., description="Nombre del ingrediente")
    quantity: float = Field(..., description="Cantidad requerida", ge=0)
    unit: str = Field(..., description="Unidad de medida (ej. g, ml, pza, cda)")

class RecipeStep(BaseModel):
    step_number: int = Field(..., description="Número de paso (1, 2, 3...)")
    title: str = Field(..., description="Título del paso de preparación")
    instruction: str = Field(..., description="Instrucción detallada con tokens de interpolación {token}")

class RecipeValidationSchema(BaseModel):
    recipe_id: str = Field(..., description="ID único de la receta en formato snake_case")
    display_name: str = Field(..., description="Nombre oficial del platillo")
    math_matrix: Dict[str, float] = Field(default_factory=dict, description="Cantidades base por 1 comensal con tokens estándar en inglés")
    inventory_tags: List[str] = Field(default_factory=list, description="Etiquetas de ingredientes para inventario")
    steps: List[RecipeStep] = Field(default_factory=list, description="Lista de pasos dinámicos reales")
    is_rescue_flag: bool = Field(default=False, description="True si es una receta de rescate en emergencia")

    @model_validator(mode="after")
    def validate_tokens_and_no_hardcoded_numbers(self):
        matrix_keys = set(self.math_matrix.keys())
        extracted_tokens = set()
        
        # Regex to detect forbidden hardcoded quantities in instruction text
        forbidden_pattern = re.compile(r'\b\d+\s*(g|gr|gramos|kg|ml|porciones|personas|comensales)\b', re.IGNORECASE)

        for step in self.steps:
            if forbidden_pattern.search(step.instruction):
                raise ValueError(f"Instrucción con cantidad estática harcodeada detectada en paso {step.step_number}: '{step.instruction}'")
            
            tokens = re.findall(r'\{([a-zA-Z0-9_]+)\}', step.instruction)
            for t in tokens:
                if t != "diners_count":
                    extracted_tokens.add(t)

        missing_in_matrix = extracted_tokens - matrix_keys
        if missing_in_matrix:
            raise ValueError(f"Tokens usados en las instrucciones no declarados en math_matrix: {missing_in_matrix}")
        
        return self

class Meal(BaseModel):
    meal_type: str = Field(..., description="Tipo de comida: Desayuno, Comida, Cena")
    starter_name: Optional[str] = Field(default="Entrada Keto", description="Nombre de la Entrada")
    main_dish_name: Optional[str] = Field(default="Plato Principal Keto", description="Nombre del Plato Principal Keto")
    side_dish_name: Optional[str] = Field(default="Acompañamiento Keto", description="Nombre del Acompañamiento")
    dish_name_legacy: Optional[str] = Field(default=None, alias="dish_name")
    fat_g: float = Field(..., description="Gramos de grasa saludables", ge=0)
    protein_g: float = Field(..., description="Gramos de proteína", ge=0)
    net_carbs_g: float = Field(..., description="Gramos de carbohidratos netos (<10g)", ge=0)
    ingredients: List[Ingredient] = Field(default_factory=list, description="Lista de ingredientes del platillo")

    @model_validator(mode="before")
    @classmethod
    def sync_dish_names(cls, data):
        if isinstance(data, dict):
            dish_val = data.get("dish_name") or data.get("main_dish_name")
            if dish_val and not data.get("main_dish_name"):
                data["main_dish_name"] = dish_val
        return data

    @property
    def dish_name(self) -> str:
        return self.main_dish_name or self.dish_name_legacy or "Platillo Principal"

class PreliminaryPrep(BaseModel):
    base_name: str = Field(..., description="Preparación de [Nombre de la Base/Salsa/Compota/Gelatina]")
    ingredients: List[Ingredient] = Field(default_factory=list, description="Ingredientes con cantidades exactas")
    cutting_prep: str = Field(..., description="Instrucciones de limpieza y corte preliminar")
    cooking_process: str = Field(..., description="Tiempos, temperatura y método de cocción")
    storage_reserve: str = Field(..., description="Instrucciones de enfriamiento, conservación o reserva")

class DynamicPrepPhases(BaseModel):
    fase_1_mise_en_place: str = Field(..., description="Gramajes exactos y absolutos para N comensales basados en approved_ingredients.")
    fase_2_acondicionamiento: str = Field(..., description="Tipos de corte e higienización técnica.")
    fase_3_termodinamica: str = Field(..., description="Curva termodinámica en °C y tiempos cronometrados en minutos.")
    fase_4_servicio: str = Field(..., description="Arquitectura de emplatado y temperatura de salida al comensal.")

    @model_validator(mode="before")
    @classmethod
    def map_short_phase_keys(cls, data):
        if isinstance(data, dict):
            if "f1" in data and "fase_1_mise_en_place" not in data:
                data["fase_1_mise_en_place"] = data["f1"]
            if "f2" in data and "fase_2_acondicionamiento" not in data:
                data["fase_2_acondicionamiento"] = data["f2"]
            if "f3" in data and "fase_3_termodinamica" not in data:
                data["fase_3_termodinamica"] = data["f3"]
            if "f4" in data and "fase_4_servicio" not in data:
                data["fase_4_servicio"] = data["f4"]
        return data

class RecipeIngredientDetail(BaseModel):
    name: str = Field(..., description="Nombre del ingrediente")
    quantity: float = Field(..., ge=0, description="Cantidad numérica")
    unit: str = Field(..., description="Unidad (g, ml, piezas, dientes, tazas, cdas, etc.)")
    category: str = Field(..., description="Categoría: vegetable, fat_oil, protein, dairy, liquid_base, spice_seasoning, garnish")
    prep_state: str = Field(default="", description="Corte o preparación previa (ej. en cubos de 2 cm, picado fino)")

class RecipeStepDetail(BaseModel):
    step_number: int = Field(..., ge=1, description="Número de paso")
    phase_name: str = Field(..., description="Fase técnica: mise_en_place, base_sofrito, cooking_liquid, processing_blending, fat_incorporation, seasoning_finish")
    action_description: str = Field(..., description="Instrucción procedimental detallada")
    heat_level: str = Field(default="none", description="Nivel de fuego: none, low, medium-low, medium, medium-high, high")
    duration_minutes: float = Field(default=0.0, ge=0, description="Duración en minutos")
    temperature_target_c: Optional[float] = Field(default=None, description="Temperatura de control en °C")

class RecipeServiceDetail(BaseModel):
    serving_temperature_c: float = Field(default=65.0, description="Temperatura de servicio en °C")
    plating_instructions: str = Field(default="", description="Instrucciones de emplatado")
    garnishes: List[str] = Field(default_factory=list, description="Guarniciones y acabados")

class RecipeYieldInfo(BaseModel):
    servings: int = Field(default=6, ge=1)
    serving_size_g: float = Field(default=350.0, ge=1.0)

class RecipeMacroTarget(BaseModel):
    calories: float = Field(default=0.0, ge=0)
    protein_g: float = Field(default=0.0, ge=0)
    net_carbs_g: float = Field(default=0.0, ge=0)
    fat_g: float = Field(default=0.0, ge=0)

class TypedRecipeSchema(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
    recipe_id: Optional[str] = None
    category: Optional[str] = None
    cooking_technique: Optional[Any] = None
    sensory_description: Optional[str] = ""
    ingredient_groups: Optional[List[IngredientGroupSchema]] = Field(default_factory=list)
    ingredients: Optional[List[Any]] = Field(default_factory=list)
    steps: Optional[List[Any]] = Field(default_factory=list)
    yield_info: Optional[Any] = None
    macro_target: Optional[Any] = None
    equipment: Optional[List[str]] = Field(default_factory=list)
    service: Optional[Any] = None

    @property
    def get_title(self) -> str:
        return self.title or self.name or "Platillo"

    def to_dynamic_prep_phases(self):
        from app.services.keto_architect import compile_dynamic_prep_phases
        return compile_dynamic_prep_phases(self.get_title, getattr(self, "ingredients", []) or [])

class CompilePhasesItem(BaseModel):
    dish_name: str = Field(..., description="Nombre del platillo")
    approved_ingredients: List[Ingredient] = Field(default_factory=list, description="Ingredientes aprobados")
    diners_count: int = Field(default=6, description="Número de comensales")

class CompilePhasesRequest(BaseModel):
    items: List[CompilePhasesItem] = Field(..., description="Lista de platillos a compilar JIT")

class CompilePhasesResponse(BaseModel):
    success: bool = True
    compiled_phases: Dict[str, DynamicPrepPhases] = Field(default_factory=dict)
    typed_recipes: Optional[Dict[str, TypedRecipeSchema]] = Field(default=None)

class DishProcedure(BaseModel):
    dish_name: str
    steps: List[RecipeStep] = Field(default_factory=list, description="Lista de pasos dinámicos reales")
    dynamic_prep: Optional[DynamicPrepPhases] = None
    phase_1: str = Field(default="", description="Fase 1 (Compatibilidad)")
    phase_2: str = Field(default="", description="Fase 2 (Compatibilidad)")
    phase_3: str = Field(default="", description="Fase 3 (Compatibilidad)")
    phase_4: str = Field(default="", description="Fase 4 (Compatibilidad)")


    @model_validator(mode="after")
    def sync_phase_compatibility(self):
        if self.steps and not self.phase_1:
            if len(self.steps) >= 1: self.phase_1 = f"1. {self.steps[0].title}: {self.steps[0].instruction}"
            if len(self.steps) >= 2: self.phase_2 = f"2. {self.steps[1].title}: {self.steps[1].instruction}"
            if len(self.steps) >= 3: self.phase_3 = f"3. {self.steps[2].title}: {self.steps[2].instruction}"
            if len(self.steps) >= 4: self.phase_4 = f"4. {self.steps[3].title}: {self.steps[3].instruction}"
            if len(self.steps) > 4:
                extra_steps = " | ".join([f"{s.step_number}. {s.title}: {s.instruction}" for s in self.steps[3:]])
                self.phase_4 += f" | {extra_steps}"
        return self

class MealPrepBlock(BaseModel):
    meal_type: str = Field(..., description="Desayuno, Comida, Cena")
    diners_spec: str = Field(default="6 Personas: 5 adultos y 1 adolescente")
    starter: DishProcedure
    main_dish: DishProcedure
    side_dish: DishProcedure

class PreparationRecipe(BaseModel):
    dish_name: str
    category: str = Field(..., description="Categoría: Desayuno, Comida, Cena")
    prep_time_min: int = 15
    steps: List[RecipeStep] = Field(default_factory=list)
    phase_1: str = Field(default="")
    phase_2: str = Field(default="")
    phase_3: str = Field(default="")
    phase_4: str = Field(default="")
    scaled_ingredients: List[Ingredient] = Field(default_factory=list)

# MODELOS DE LAS 3 SECCIONES DE NUTR.
class FunctionalJustification(BaseModel):
    category_title: str = Field(..., description="Categoría Nutricional")
    source_ingredient: str = Field(..., description="Ingrediente de Origen")
    physiological_impact: str = Field(..., description="Impacto Fisiológico")

class MealFunctionalAnalysis(BaseModel):
    meal_type: str
    diners_spec: str = Field(default="6 Personas: 5 adultos y 1 adolescente")
    starter_justification: FunctionalJustification
    main_justification: FunctionalJustification
    side_justification: FunctionalJustification

class NutritionFactItem(BaseModel):
    nutrient_name: str
    amount_str: str
    daily_value_pct: str

class MealNutritionFactTable(BaseModel):
    meal_type: str
    portion_size: str
    total_calories_kcal: float
    facts: List[NutritionFactItem]
    base_ingredients: List[str]

class FoodGlycemicAnalysis(BaseModel):
    food_name: str
    ig_range: str
    risk_category: str
    physiological_reason: str

class MealGlycemicSynergy(BaseModel):
    meal_type: str
    food_analyses: List[FoodGlycemicAnalysis]
    synergy_summary: str

class ClinicalGlycemicSection(BaseModel):
    micro_analyses: List[MealGlycemicSynergy]
    macro_daily_summary: str

class ComprehensiveNutritionView(BaseModel):
    section_1_functional: List[MealFunctionalAnalysis] = Field(default_factory=list)
    section_2_tables: List[MealNutritionFactTable] = Field(default_factory=list)
    section_3_glycemic: Optional[ClinicalGlycemicSection] = None

class NutritionMetrics(BaseModel):
    calories_kcal: float = Field(..., ge=0)
    total_fat_g: float = Field(..., ge=0)
    sat_fat_g: float = Field(..., ge=0)
    cholesterol_mg: float = Field(..., ge=0)
    sodium_mg: float = Field(..., ge=0)
    net_carbs_g: float = Field(..., ge=0)
    fiber_g: float = Field(..., ge=0)
    protein_g: float = Field(..., ge=0)
    ig_impact: str = Field(default="Bajo (Curva plana / Sin pico glucémico)")
    metabolic_notes: str = Field(default="Amortiguación enzimática óptima por grasas y fibra.")

class DailyMenu(BaseModel):
    day: str = Field(..., description="Día de la semana: Domingo a Sábado")
    date_str: Optional[str] = Field(default="", description="Fecha legible ej. 04 AGO")
    day_num: Optional[str] = Field(default="04", description="Número de día de dos dígitos ej. 04")
    full_date_title: Optional[str] = Field(default="", description="Menú Completo para el [Día] [Número] de [Mes]")
    preliminary_preps: List[PreliminaryPrep] = Field(default_factory=list)
    meal_prep_blocks: List[MealPrepBlock] = Field(default_factory=list)
    meals: List[Meal] = Field(..., description="Comidas del día")
    recipes: List[PreparationRecipe] = Field(default_factory=list)
    clinical_nutrition: Optional[ComprehensiveNutritionView] = None
    nutrition: Optional[NutritionMetrics] = None

class WeeklyMenuPlan(BaseModel):
    diners_count: int = Field(..., ge=1)
    days: List[DailyMenu] = Field(...)

class WeeklyMenuRequest(BaseModel):
    diners_count: int = Field(default=2, ge=1)
    preferences: Optional[str] = Field(default="")

class NegotiationRequest(BaseModel):
    day: Optional[str] = Field(default="Hoy")
    current_meal: Meal
    user_request: str = Field(default="")
    target_field: Optional[str] = Field(default="main", description="Campo objetivo a modificar: starter, main, side")
    diners_count: Optional[int] = Field(default=6, description="Número de comensales activos")
    is_auto_suggest: bool = Field(default=False, description="True si solicita sugerencias automáticas de exploración")

class SuggestionRequest(BaseModel):
    meal_type: str = Field(default="Comida", description="Tipo de comida: Desayuno, Comida, Cena")
    target_field: str = Field(default="main", description="Campo objetivo: starter, main, side")
    current_dish_name: Optional[str] = Field(default="", description="Nombre actual del platillo a sustituir")
    diners_count: int = Field(default=6, description="Comensales activos para control volumétrico")

class SuggestionItem(BaseModel):
    title: str = Field(..., description="Nombre del platillo sugerido")
    description: str = Field(..., description="Breve descripción gastronómica")
    key_ingredients: List[str] = Field(default_factory=list, description="Ingredientes principales de cosecha y alacena")

class SuggestionResponse(BaseModel):
    suggestions: List[SuggestionItem] = Field(default_factory=list, description="3 Opciones recomendadas por Cortex Gatekeeper")

class NegotiationResponse(BaseModel):
    is_approved: bool
    rejection_reason: Optional[str] = ""
    revised_meal: Optional[Meal] = None
    alternative_suggestions: List[str] = Field(default_factory=list)
    revised_prep_phases: Optional[Union[DynamicPrepPhases, Dict[str, Any]]] = None
    full_recalculated_shopping_list: Optional[List[Dict]] = None

class ShoppingCheckItem(BaseModel):
    id: Optional[int] = None
    day: str
    item_name: str
    quantity: float
    unit: str
    is_checked: bool = False

class ToggleShoppingRequest(BaseModel):
    item_id: int
    is_checked: bool

class ShoppingSyncItem(BaseModel):
    item_name: str
    quantity: float = Field(..., ge=0)
    unit: str

class ShoppingSyncRequest(BaseModel):
    items: List[ShoppingSyncItem]

class DishServedSyncRequest(BaseModel):
    dish_name: str
    ingredients: List[Ingredient]

class PantryItem(BaseModel):
    id: Optional[int] = None
    item_name: str
    quantity: float
    unit: str
    updated_at: Optional[str] = None

class PantryStatusResponse(BaseModel):
    pantry: List[PantryItem]

class InventoryIntakeRequest(BaseModel):
    source_type: str = Field(default="🛒 Supermercado / Compra Neta", description="Fuente de abastecimiento")
    item_name: str = Field(..., description="Nombre del insumo ingresado")
    quantity: float = Field(..., gt=0, description="Cantidad que ingresa al stock")
    unit: str = Field(default="unidad/frasco", description="Unidad de medida")
    category: str = Field(default="🛒 Abarrotes, Aceites y Grasas", description="Clasificación botánica / culinaria")
    storage_destination: str = Field(default="🏺 Alacena Principal / Seca", description="Destino de almacenaje")
    intake_date: Optional[str] = Field(default=None, description="Fecha de ingreso o cosecha (YYYY-MM-DD)")
    batch_notes: Optional[str] = Field(default="", description="Lote u observaciones de frescura")

class InventoryIntakeResponse(BaseModel):
    success: bool
    message: str
    updated_item_name: str
    new_total_quantity: float
    unit: str
    storage_destination: Optional[str] = None




from enum import Enum

class CulinaryTechniqueEnum(str, Enum):
    RAW_ASSEMBLY = "raw_assembly"          # Frutas, ensaladas frías, tartares
    BOIL_AND_BLEND = "boil_and_blend"      # Cremas y sopas
    POACH_AND_EMULSION = "poach_and_emulsion" # Pochados y salsas emulsionadas
    PAN_FRY_EGG = "pan_fry_egg"            # Omelettes y revueltos
    ROAST_BAKE = "roast_bake"              # Vegetales asados, gratinados
    SAUTE_AND_SEAR = "saute_and_sear"      # Proteínas sólidas, filetes
    STEEP_BEVERAGE = "steep_beverage"      # Tés, tisanas e infusiones
    GELATIN_MOLDING = "gelatin_molding"    # Gelatinas y mousses

class IngredientItemSchema(BaseModel):
    name: str
    base_qty_per_person: float
    unit: str
    source: str = "Granja El Herami"
    unit_cost: float = 0.0

class IngredientGroupSchema(BaseModel):
    category: str
    items: List[IngredientItemSchema]

class TypedRecipeSchema(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
    recipe_id: Optional[str] = None
    category: Optional[str] = None
    cooking_technique: Optional[Any] = None
    sensory_description: Optional[str] = ""
    ingredient_groups: Optional[List[IngredientGroupSchema]] = Field(default_factory=list)
    ingredients: Optional[List[Any]] = Field(default_factory=list)
    steps: Optional[List[Any]] = Field(default_factory=list)
    yield_info: Optional[Any] = None
    macro_target: Optional[Any] = None
    equipment: Optional[List[str]] = Field(default_factory=list)
    service: Optional[Any] = None

    @property
    def get_title(self) -> str:
        return self.title or self.name or "Platillo"

    def to_dynamic_prep_phases(self):
        from app.services.keto_architect import compile_dynamic_prep_phases
        return compile_dynamic_prep_phases(self.get_title, getattr(self, "ingredients", []) or [])

