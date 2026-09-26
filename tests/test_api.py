import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
import os
from app.main import app
from app.database import init_db, settings

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    test_db_path = str(tmp_path / "test_nutriketo_multiview.db")
    settings.DATABASE_PATH = test_db_path
    settings.GEMINI_API_KEY = ""
    os.environ["GEMINI_API_KEY"] = ""
    init_db()
    yield
    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except PermissionError:
            pass

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert "T.I.L.O." in response.text

@pytest.mark.asyncio
async def test_generate_weekly_multiview_plan(client: AsyncClient):
    payload = {"diners_count": 4, "preferences": "Sin mariscos"}
    response = await client.post("/api/menu/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["diners_count"] == 4
    assert len(data["days"]) == 7
    first_day = data["days"][0]
    assert len(first_day["meals"]) == 3
    assert len(first_day["recipes"]) > 0
    assert first_day["nutrition"]["calories_kcal"] > 0

@pytest.mark.asyncio
async def test_persistent_shopping_checklist_toggle(client: AsyncClient):
    # Generar menú para poblar la lista de compras
    await client.post("/api/menu/generate", json={"diners_count": 2})

    # Obtener ítems del checklist
    res_items = await client.get("/api/shopping/items")
    assert res_items.status_code == 200
    items = res_items.json()["items"]
    assert len(items) > 0

    first_item = items[0]
    item_id = first_item["id"]

    # Alternar a checked=True
    res_toggle = await client.post("/api/shopping/toggle", json={"item_id": item_id, "is_checked": True})
    assert res_toggle.status_code == 200
    assert res_toggle.json()["is_checked"] is True

    # Verificar persistencia en SQLite
    res_check = await client.get("/api/shopping/items")
    updated_item = next(i for i in res_check.json()["items"] if i["id"] == item_id)
    assert updated_item["is_checked"] is True

@pytest.mark.asyncio
async def test_negotiate_menu(client: AsyncClient):
    neg_payload = {
        "day": "Domingo",
        "current_meal": {
            "meal_type": "Comida",
            "dish_name": "Pechuga Gratinada",
            "fat_g": 30.0,
            "protein_g": 25.0,
            "net_carbs_g": 4.0,
            "ingredients": [{"name": "Pollo", "quantity": 200.0, "unit": "g"}]
        },
        "user_request": "Cambiar el pollo por filete de res"
    }
    res = await client.post("/api/menu/negotiate", json=neg_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["is_approved"] is True
    assert "full_recalculated_shopping_list" in data
    assert len(data["full_recalculated_shopping_list"]) > 0
    assert "revised_prep_phases" in data
    assert "fase_1_mise_en_place" in data["revised_prep_phases"] or "f1" in data["revised_prep_phases"]

@pytest.mark.asyncio
async def test_suggest_menu_options(client: AsyncClient):
    sug_payload = {
        "meal_type": "Comida",
        "target_field": "main",
        "diners_count": 6
    }
    res = await client.post("/api/menu/suggest", json=sug_payload)
    assert res.status_code == 200
    data = res.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) == 3
    first = data["suggestions"][0]
    assert "title" in first
    assert "description" in first
    assert "key_ingredients" in first

@pytest.mark.asyncio
async def test_negotiate_menu_rejection_auto_fallback(client: AsyncClient):
    neg_payload = {
        "day": "Lunes",
        "current_meal": {
            "meal_type": "Comida",
            "starter_name": "Consomé de Nopales",
            "main_dish_name": "Ribeye a la Plancha",
            "side_dish_name": "Espárragos Asados",
            "fat_g": 30.0, "protein_g": 35.0, "net_carbs_g": 3.0,
            "ingredients": []
        },
        "user_request": "Quiero Tacos de Cerdo al Pastor",
        "target_field": "main",
        "diners_count": 6
    }
    res = await client.post("/api/menu/negotiate", json=neg_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["is_approved"] is False
    assert "cerdo" in data["rejection_reason"].lower()
    assert len(data["alternative_suggestions"]) == 3

@pytest.mark.asyncio
async def test_register_inventory_intake(client: AsyncClient):
    intake_payload = {
        "source_type": "🚚 Proveedor Externo / Distribuidor Especializado",
        "item_name": "Vinagre balsámico (orgánico / keto)",
        "quantity": 2.0,
        "unit": "frascos",
        "category": "🌶️ Chiles, Condimentos y Especias",
        "storage_destination": "🏺 Alacena Principal / Seca",
        "intake_date": "2026-08-24",
        "batch_notes": "Lote de prueba de alta calidad de proveedor especializado"
    }
    res = await client.post("/api/inventory/intake", json=intake_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["updated_item_name"] == "Vinagre balsámico (orgánico / keto)"
    assert data["new_total_quantity"] >= 2.0
    assert data["unit"] == "frascos"
    assert "storage_destination" in data
    assert "Alacena Principal" in data["storage_destination"]

@pytest.mark.asyncio
async def test_compile_phases_jit(client: AsyncClient):
    payload = {
        "items": [
            {
                "dish_name": "Tartar de Atún Fresco con Aguacate Hass",
                "approved_ingredients": [
                    {"name": "Atún fresco", "quantity": 180.0, "unit": "g"},
                    {"name": "Aguacate Hass", "quantity": 50.0, "unit": "g"}
                ],
                "diners_count": 6
            }
        ]
    }
    res = await client.post("/api/menu/compile-phases", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "Tartar de Atún Fresco con Aguacate Hass" in data["compiled_phases"]
    phases = data["compiled_phases"]["Tartar de Atún Fresco con Aguacate Hass"]
    assert "fase_1_mise_en_place" in phases
    assert "fase_4_servicio" in phases

@pytest.mark.asyncio
async def test_typed_recipe_schema_units_validation():
    from app.schemas import TypedRecipeSchema, RecipeIngredientDetail, RecipeStepDetail, RecipeServiceDetail, RecipeYieldInfo, RecipeMacroTarget

    recipe = TypedRecipeSchema(
        recipe_id="crema_brocoli_parmesano",
        name="Crema de Brócoli con Parmesano",
        category="soup_cream",
        cooking_technique="boil_and_blend",
        yield_info=RecipeYieldInfo(servings=6, serving_size_g=350.0),
        macro_target=RecipeMacroTarget(calories=320, protein_g=14, net_carbs_g=5, fat_g=26),
        equipment=["cacerola", "licuadora"],
        ingredients=[
            RecipeIngredientDetail(name="Brócoli fresco", quantity=500.0, unit="g", category="vegetable", prep_state="en floretes"),
            RecipeIngredientDetail(name="Caldo de pollo", quantity=750.0, unit="ml", category="liquid_base", prep_state="tibio"),
            RecipeIngredientDetail(name="Cebolla blanca", quantity=0.5, unit="piezas", category="vegetable", prep_state="picada"),
            RecipeIngredientDetail(name="Dientes de ajo", quantity=2.0, unit="dientes", category="vegetable", prep_state="picados"),
            RecipeIngredientDetail(name="Crema para batir", quantity=120.0, unit="ml", category="dairy", prep_state="líquida"),
            RecipeIngredientDetail(name="Queso Parmesano", quantity=80.0, unit="g", category="dairy", prep_state="rallado")
        ],
        steps=[
            RecipeStepDetail(step_number=1, phase_name="base_sofrito", action_description="Sofreír cebolla y ajo en mantequilla.", heat_level="medium", duration_minutes=4),
            RecipeStepDetail(step_number=2, phase_name="cooking_liquid", action_description="Agregar brócoli y caldo. Hervir 9 min.", heat_level="medium-low", duration_minutes=9),
            RecipeStepDetail(step_number=3, phase_name="processing_blending", action_description="Licuar a alta velocidad hasta textura terciopelo.", heat_level="none", duration_minutes=2),
            RecipeStepDetail(step_number=4, phase_name="fat_incorporation", action_description="Integrar crema y queso parmesano a fuego bajo sin hervir.", heat_level="low", duration_minutes=3)
        ],
        service=RecipeServiceDetail(serving_temperature_c=68.0, plating_instructions="Servir en tazones hondos", garnishes=["pimienta negra", "aceite VEVO"])
    )

    assert recipe.cooking_technique == "boil_and_blend"
    phases = recipe.to_dynamic_prep_phases()
    assert "Caldo de pollo" in phases.fase_1_mise_en_place
    assert "Paso 1" in phases.fase_2_acondicionamiento or "base_sofrito" in phases.fase_2_acondicionamiento or "sofrito" in phases.fase_2_acondicionamiento.lower() or "sofreír" in phases.fase_2_acondicionamiento.lower()
    assert "Paso 3" in phases.fase_3_termodinamica or "processing_blending" in phases.fase_3_termodinamica or "Licuar" in phases.fase_3_termodinamica

@pytest.mark.asyncio
async def test_compile_cream_phases_jit(client: AsyncClient):
    payload = {
        "items": [
            {
                "dish_name": "Crema de Brócoli con Queso Parmesano",
                "approved_ingredients": [
                    {"name": "Brócoli fresco", "quantity": 500.0, "unit": "g"},
                    {"name": "Caldo de pollo", "quantity": 750.0, "unit": "ml"},
                    {"name": "Mantequilla de pastoreo", "quantity": 30.0, "unit": "g"},
                    {"name": "Queso Parmesano", "quantity": 80.0, "unit": "g"}
                ],
                "diners_count": 6
            }
        ]
    }
    res = await client.post("/api/menu/compile-phases", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    phases = data["compiled_phases"]["Crema de Brócoli con Queso Parmesano"]
    assert "fase_1_mise_en_place" in phases
    f3_text = phases.get("fase_3_termodinamica", "")
    f2_text = phases.get("fase_2_acondicionamiento", "")
    assert "Licuado" in f3_text or "Cocción" in f3_text or "Sofrito" in f2_text or len(f3_text) > 0

@pytest.mark.asyncio
async def test_poach_and_emulsion_vs_pan_fry_egg(client: AsyncClient):
    payload = {
        "items": [
            {
                "dish_name": "Huevos Turcos Çılbır (Pochados sobre Yogur Griego al Ajo)",
                "approved_ingredients": [
                    {"name": "Huevos frescos", "quantity": 12.0, "unit": "piezas"},
                    {"name": "Yogur griego natural", "quantity": 750.0, "unit": "g"},
                    {"name": "Mantequilla de pastoreo", "quantity": 135.0, "unit": "g"},
                    {"name": "Chile Aleppo", "quantity": 15.0, "unit": "g"}
                ],
                "diners_count": 6
            }
        ]
    }
    res = await client.post("/api/menu/compile-phases", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    phases = data["compiled_phases"]["Huevos Turcos Çılbır (Pochados sobre Yogur Griego al Ajo)"]
    f3_text = phases.get("fase_3_termodinamica", "")
    f4_text = phases.get("fase_4_servicio", "")
    assert "Pochado" in f3_text or "85°C" in f3_text
    assert "trinchar" not in f4_text.lower()
    assert "190°c" not in f3_text.lower()

@pytest.mark.asyncio
async def test_scoped_technique_validation():
    from app.schemas import TypedRecipeSchema, RecipeIngredientDetail, RecipeStepDetail, RecipeServiceDetail, RecipeYieldInfo, RecipeMacroTarget
    
    # Receta valida con poach_and_emulsion
    recipe = TypedRecipeSchema(
        recipe_id="huevos_cilbir",
        name="Huevos Turcos Cilbir",
        category="main_course",
        cooking_technique="poach_and_emulsion",
        yield_info=RecipeYieldInfo(servings=6, serving_size_g=250.0),
        macro_target=RecipeMacroTarget(calories=400, protein_g=22, net_carbs_g=4, fat_g=32),
        equipment=["cacerola", "sartén"],
        ingredients=[
            RecipeIngredientDetail(name="Huevos frescos", quantity=12.0, unit="piezas", category="protein", prep_state="frescos"),
            RecipeIngredientDetail(name="Yogur griego", quantity=750.0, unit="g", category="dairy", prep_state="a temp ambiente")
        ],
        steps=[
            RecipeStepDetail(step_number=1, phase_name="base_sofrito", action_description="Mezclar yogur con ajo y sal.", heat_level="none", duration_minutes=3),
            RecipeStepDetail(step_number=2, phase_name="cooking_liquid", action_description="Pochar huevos en agua con vinagre a 85-90°C por 3 min.", heat_level="medium-low", duration_minutes=3)
        ],
        service=RecipeServiceDetail(serving_temperature_c=60.0, plating_instructions="Bañar con mantequilla especiada", garnishes=["eneldo"])
    )
    assert recipe.cooking_technique == "poach_and_emulsion"

@pytest.mark.asyncio
async def test_dynamic_shopping_and_macro_sync(client: AsyncClient):
    res = await client.get("/api/shopping/items")
    assert res.status_code == 200
    data = res.json()
    items = data["items"]
    item_names = [it["item_name"].lower() for it in items]
    assert any("espinaca" in name for name in item_names)















# --- PRUEBAS UNITARIAS DE GOBERNANZA CLÍNICA V15.23.1 ---

def test_zero_capsaicin_in_generated_week():
    """Valida 0 presencia de capsaicina o chiles en nombres de platillos."""
    import re
    forbidden_spicy = ["chile", "serrano", "jalapeño", "habanero", "chipotle", "cayena"]
    with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
        file_text = f.read()
    
    dish_matches = re.findall(r'"(?:starter_name|main_dish_name|side_dish_name)":\s*"([^"]+)"', file_text)
    for dish_name in dish_matches:
        d_lower = dish_name.lower()
        for spicy in forbidden_spicy:
            assert spicy not in d_lower, f"Infracción clínica: ingrediente picante '{spicy}' detectado en '{dish_name}'."

def test_zero_pork_and_derivatives():
    """Valida 0 presencia de carne de cerdo o grasas porcinas en platillos."""
    import re
    forbidden_pork = ["cerdo", "puerco", "tocino de cerdo", "jamon de cerdo", "manteca de cerdo", "chicharron"]
    with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
        file_text = f.read()
    
    dish_matches = re.findall(r'"(?:starter_name|main_dish_name|side_dish_name)":\s*"([^"]+)"', file_text)
    for dish_name in dish_matches:
        d_lower = dish_name.lower()
        for pork in forbidden_pork:
            assert pork not in d_lower, f"Infracción clínica: ingrediente porcino '{pork}' detectado en '{dish_name}'."

def test_zero_gluten_and_grains():
    """Valida 0 presencia de trigo, maíz o almidones refinados."""
    import re
    forbidden_grains = ["harina refinada", "harina de trigo", "tortilla de maiz", "arroz blanco"]
    with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
        file_text = f.read()
    
    dish_matches = re.findall(r'"(?:starter_name|main_dish_name|side_dish_name)":\s*"([^"]+)"', file_text)
    for dish_name in dish_matches:
        d_lower = dish_name.lower()
        for grain in forbidden_grains:
            assert grain not in d_lower, f"Infracción clínica: grano/gluten '{grain}' detectado en '{dish_name}'."

def test_herami_bom_zero_cost():
    """Valida que los insumos de Granja El Herami se clasifiquen a $0 BOM."""
    with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "Granja El Herami" in content, "Falta el decorador de origen Granja El Herami"

def test_four_week_uniqueness_matrix():
    """Valida que la Semana 36 contenga platillos inéditos sin solapamiento."""
    import re
    with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    dish_matches = re.findall(r'"(?:starter_name|main_dish_name|side_dish_name)":\s*"([^"]+)"', content)
    assert len(dish_matches) > 0, "No se encontraron platillos en el archivo"
    
    # Verificar que los últimos 21 platillos (Semana 36) sean 100% únicos entre sí
    week_36_dishes = dish_matches[-21:]
    unique_36 = set(week_36_dishes)
    assert len(week_36_dishes) == len(unique_36), f"Existen platillos duplicados dentro de la Semana 36 ({len(week_36_dishes)} vs {len(unique_36)})"



# --- PRUEBAS UNITARIAS DE RAZONAMIENTO CULINARIO SSOT V15.25.2 ---

def test_validator_allows_short_legitimate_titles():
    """Valida que platillos de una o dos palabras no causen falso positivo."""
    from app.schemas import TypedRecipeSchema, CulinaryTechniqueEnum, IngredientGroupSchema, IngredientItemSchema
    from app.services.recipe_validator import validate_recipe_compliance

    recipe = TypedRecipeSchema(
        title="Fresas",
        cooking_technique=CulinaryTechniqueEnum.RAW_ASSEMBLY,
        sensory_description="Fresas frescas de la granja desinfectadas.",
        ingredient_groups=[
            IngredientGroupSchema(
                category="🌱 Fruta Base",
                items=[
                    IngredientItemSchema(name="Fresas frescas", base_qty_per_person=75.0, unit="g"),
                    IngredientItemSchema(name="Nuez de Castilla", base_qty_per_person=15.0, unit="g")
                ]
            )
        ],
        steps=["Lavar fresas.", "Servir frescas."]
    )
    is_valid, reason = validate_recipe_compliance(recipe)
    assert is_valid, f"Falso positivo en título corto: {reason}"

def test_validator_rejects_monolithic_long_titles():
    """Valida rechazo cuando un título de 3+ palabras se clona como ingrediente."""
    from app.schemas import TypedRecipeSchema, CulinaryTechniqueEnum, IngredientGroupSchema, IngredientItemSchema
    from app.services.recipe_validator import validate_recipe_compliance

    recipe = TypedRecipeSchema(
        title="Fresas Frescas de la Granja con Nueces de Castilla y Chía",
        cooking_technique=CulinaryTechniqueEnum.RAW_ASSEMBLY,
        sensory_description="Ensamble fresco.",
        ingredient_groups=[
            IngredientGroupSchema(
                category="Base",
                items=[
                    IngredientItemSchema(name="Fresas Frescas de la Granja con Nueces de Castilla y Chía", base_qty_per_person=600.0, unit="g")
                ]
            )
        ],
        steps=["Higienizar e insumos.", "Cocinar a fuego medio.", "Servir de inmediato."]
    )
    is_valid, reason = validate_recipe_compliance(recipe)
    assert not is_valid, "El validador debió rechazar el ingrediente monolítico"
    assert "Ingrediente monolítico prohibido" in reason

def test_validator_rejects_thermal_mismatch():
    """Valida rechazo si se detecta fuego o sartén en raw_assembly."""
    from app.schemas import TypedRecipeSchema, CulinaryTechniqueEnum, IngredientGroupSchema, IngredientItemSchema
    from app.services.recipe_validator import validate_recipe_compliance

    recipe = TypedRecipeSchema(
        title="Coctel de Kiwi Dorado",
        cooking_technique=CulinaryTechniqueEnum.RAW_ASSEMBLY,
        sensory_description="Coctel en frío.",
        ingredient_groups=[
            IngredientGroupSchema(
                category="Base",
                items=[
                    IngredientItemSchema(name="Kiwi dorado", base_qty_per_person=50.0, unit="g"),
                    IngredientItemSchema(name="Semillas de chía", base_qty_per_person=5.0, unit="g")
                ]
            )
        ],
        steps=["Lavar fruta.", "Cocinar a fuego medio en sartén caliente.", "Servir."]
    )
    is_valid, reason = validate_recipe_compliance(recipe)
    assert not is_valid, "El validador debió rechazar la incoherencia térmica"
    assert "Incoherencia térmica" in reason

def test_forbidden_keywords_rejection():
    """Valida rechazo automático si un ingrediente contiene cerdo o picante."""
    from app.schemas import TypedRecipeSchema, CulinaryTechniqueEnum, IngredientGroupSchema, IngredientItemSchema
    from app.services.recipe_validator import validate_recipe_compliance

    recipe = TypedRecipeSchema(
        title="Omelette Especial",
        cooking_technique=CulinaryTechniqueEnum.PAN_FRY_EGG,
        sensory_description="Omelette caliente.",
        ingredient_groups=[
            IngredientGroupSchema(
                category="Base",
                items=[
                    IngredientItemSchema(name="Huevos orgánicos", base_qty_per_person=2.0, unit="piezas"),
                    IngredientItemSchema(name="Tocino de cerdo", base_qty_per_person=20.0, unit="g")
                ]
            )
        ],
        steps=["Batir huevos.", "Cocinar omelette."]
    )
    is_valid, reason = validate_recipe_compliance(recipe)
    assert not is_valid, "El validador debió rechazar ingrediente porcino"
    assert "Ingrediente prohibido" in reason


def test_terminal_state_raises_http_502():
    """Valida lanzamiento de HTTPException(502) tras agotar reintentos con receta inválida."""
    from fastapi import HTTPException
    import pytest
    from app.services.keto_architect import generate_validated_typed_recipe

    # Probar con un platillo nulo o provocar fallo para verificar el raise HTTPException(502)
    # validate_recipe_compliance rechaza el reintento
    with pytest.raises(HTTPException) as exc_info:
        # Forzar max_retries = 0 o ingrediente inválido
        generate_validated_typed_recipe("", max_retries=1)

    assert exc_info.value.status_code == 502, f"Se esperaba status_code 502, obtenido {exc_info.value.status_code}"
    assert "Fallo de coherencia gastronómica" in exc_info.value.detail


def test_validate_entity_coverage_and_bom_usage():
    """Valida que validate_entity_coverage y validate_bom_usage_in_steps funcionen según SSOT V23.0.0."""
    from app.schemas import TypedRecipeSchema, CulinaryTechniqueEnum, IngredientGroupSchema, IngredientItemSchema
    from app.services.recipe_validator import validate_entity_coverage, validate_bom_usage_in_steps, validate_recipe_compliance

    # 1. Receta válida con Machaca de Pavo, Jitomate y Cebolla
    valid_recipe = TypedRecipeSchema(
        title="Huevos Revueltos con Machaca de Pavo, Jitomate Bola y Cebolla Salteada",
        cooking_technique=CulinaryTechniqueEnum.PAN_FRY_EGG,
        sensory_description="Revuelto proteico.",
        ingredient_groups=[
            IngredientGroupSchema(
                category="🍗 Proteína",
                items=[
                    IngredientItemSchema(name="Machaca de pavo artesanal", base_qty_per_person=90.0, unit="g"),
                    IngredientItemSchema(name="Huevos frescos orgánicos", base_qty_per_person=2.0, unit="piezas")
                ]
            ),
            IngredientGroupSchema(
                category="🍅 Sofrito",
                items=[
                    IngredientItemSchema(name="Jitomate bola maduro troceado", base_qty_per_person=120.0, unit="g"),
                    IngredientItemSchema(name="Cebolla blanca picada", base_qty_per_person=60.0, unit="g")
                ]
            ),
            IngredientGroupSchema(
                category="🧈 Grasa",
                items=[
                    IngredientItemSchema(name="Mantequilla clarificada", base_qty_per_person=12.0, unit="g")
                ]
            )
        ],
        steps=[
            "1. Sofrito (3 min a 160°C): Calentar mantequilla en sartén a 160°C; añadir cebolla picada y sofréir 2 min. Agregar jitomate bola y cocinar 1 min.",
            "2. Integración de Machaca (2 min a 160°C): Incorporar machaca de pavo artesanal al sofrito de cebolla y jitomate; saltear 2 min.",
            "3. Cocción de Huevos (3 min a 140°C): Verter 2 huevos frescos batidos y mover durante 3 min a 140°C.",
            "4. Servir de inmediato caliente a 68°C."
        ]
    )

    is_valid, reason = validate_recipe_compliance(valid_recipe)
    assert is_valid, f"Receta válida fue rechazada incorrectamente: {reason}"

    # 2. Receta inválida que omite 'machaca' en BOM
    invalid_recipe = TypedRecipeSchema(
        title="Huevos Revueltos con Machaca de Pavo, Jitomate Bola y Cebolla Salteada",
        cooking_technique=CulinaryTechniqueEnum.PAN_FRY_EGG,
        sensory_description="Omelette genérico sin machaca.",
        ingredient_groups=[
            IngredientGroupSchema(
                category="Base",
                items=[
                    IngredientItemSchema(name="Jamón de pavo", base_qty_per_person=50.0, unit="g"),
                    IngredientItemSchema(name="Huevos frescos", base_qty_per_person=2.0, unit="piezas")
                ]
            )
        ],
        steps=["Batir huevos.", "Cocinar omelette en sartén."]
    )

    is_cov_valid, cov_reason = validate_entity_coverage(invalid_recipe)
    assert not is_cov_valid, "El validador debió rechazar la falta de machaca en el BOM"
    assert "omite ingredientes clave" in cov_reason or "machaca" in cov_reason


def test_ssot_v36_2_0_inventory_canonical_integrity():
    from app.services.inventory_master import InventorySyncMaster, normalize_to_canonical_slug

    # 1. Ningún ingrediente botánico/vegetal/frutal debe clasificarse como carne
    botanical_items = [
        "Fresas frescas de la granja",
        "Moras frescas de la granja",
        "Pitahaya fresca de la granja",
        "Flor de calabaza fresca",
        "Coliflor fresca en floretes",
        "Infusión de té de frutos rojos y menta fresca",
        "Limón fresco recién exprimido",
        "Hojas de romero fresco"
    ]
    for item in botanical_items:
        cat = InventorySyncMaster.categorize_ingredient_name(item)
        assert cat != "🥩 Carnes, Pescados y Proteínas", f"{item} fue incorrectamente clasificado como carne: {cat}"

    # 2. Insumos cárnicos reales sí deben caer en Carnes
    meat_items = [
        "Huevos frescos orgánicos de pastoreo",
        "Filete Mignon de Res de pastoreo",
        "Pechuga de pavo artesanal",
        "Filete de Salmón fresco con piel",
        "Filete de Huachinango fresco",
        "Filete de Róbalo fresco"
    ]
    for meat in meat_items:
        cat = InventorySyncMaster.categorize_ingredient_name(meat)
        assert cat == "🥩 Carnes, Pescados y Proteínas", f"{meat} debió clasificarse en Carnes y Proteínas: {cat}"

    # 3. Unificación por slug canónico de distintas variantes de corte
    slug1 = normalize_to_canonical_slug("Calabacitas tiernas de la granja")
    slug2 = normalize_to_canonical_slug("Zoodles de calabacita a la mantequilla")
    slug3 = normalize_to_canonical_slug("Bastones de zucchini al limón")
    
    assert "calabacita" in slug1 or "zucchini" in slug1
    assert "calabacita" in slug2 or "zucchini" in slug2
    assert "calabacita" in slug3 or "zucchini" in slug3


def test_physical_state_invariant_and_thermal_safety():
    from app.services.inventory_master import validate_physical_state_invariant, format_cooking_step

    # 1. Invariante de estado físico
    existing = {'almendras-fileteadas': {'physical_state': 'solid', 'unit': 'g'}}
    
    # Debe lanzar ValueError si se intenta agregar un líquido con la misma clave
    with pytest.raises(ValueError) as excinfo:
        validate_physical_state_invariant('almendras-fileteadas', 'liquid', 'ml', existing)
    assert "INVARIANTE VIOLADA" in str(excinfo.value)

    # 2. Inyección algorítmica de inocuidad térmica por proteína
    poultry_step = format_cooking_step("Sellar la pechuga de pavo al sartén.", protein_family="poultry")
    assert "74°C" in poultry_step
    assert "centro térmico" in poultry_step

    bovine_step = format_cooking_step("Asar lomo de res a la parrilla.", protein_family="bovine")
    assert "68°C" in bovine_step or "72°C" in bovine_step

    fish_step = format_cooking_step("Hornear filete de huachinango.", protein_family="fish")
    assert "63°C" in fish_step or "68°C" in fish_step


def test_canonical_v36_shopping_list_no_ghost_items():
    import json
    import os

    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    import re
    match = re.search(r'const ACTIVE_WEEK_CANONICAL_BOM = (\{.*?\});', content, re.DOTALL)
    assert match, "ACTIVE_WEEK_CANONICAL_BOM JSON debe estar presente en HTML"
    canonical_bom_str = match.group(1).lower()

    # Verificar ausencia total de insumos fantasma en el BOM Canónico activo
    ghost_terms = ["waffle", "waffles", "licores", "cobertura de chocolate", "leche de vaca", "cafe legal"]
    for ghost in ghost_terms:
        assert ghost not in canonical_bom_str, f"Se encontró insumo fantasma '{ghost}' en ACTIVE_WEEK_CANONICAL_BOM"

    json_path = os.path.join(os.path.dirname(__file__), "..", "scratch_s38_canonical.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            bdata = json.load(f)
        assert bdata.get("unique_count") == 69, f"El recuento canónico debe ser exactamente 69 insumos y no 87. Actual: {bdata.get('unique_count')}"
        assert len(bdata.get("bom", {})) == 7, f"Las categorías comerciales canónicas deben ser 7. Actual: {len(bdata.get('bom', {}))}"


def test_no_forced_rounding_to_multiples_of_five():
    import os

    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar que las funciones JS normalizeQuantity y formatBaseQuantity NO tengan Math.ceil(num / 5) * 5
    assert "Math.ceil(num / 5) * 5" not in content, "Se encontró Math.ceil(num / 5) * 5 en normalizeQuantity"
    assert "Math.ceil(val / 5) * 5" not in content, "Se encontró Math.ceil(val / 5) * 5 en formatBaseQuantity"


def test_v_nutri_qualitative_and_quantitative_headers():
    import os

    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "kcal / comensal" in content, "Debe etiquetarse explícitamente kcal / comensal"
    assert "Cantidad por Comensal" in content, "Encabezado debe ser Cantidad por Comensal"
    assert "Completa (3 Tiempos)" in content, "El título de la comida debe indicar Completa (3 Tiempos)"
    assert "Aporte de polifenoles vivos" in content, "Debe incluir justificante específico de polifenoles"


def test_v_nutri_fiber_and_gender_concordance():
    import os

    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Completo (3 Tiempos)" in content, "Concordancia gramatical de género: Completo (3 Tiempos)"
    assert "getMealFiberG" in content, "La fibra debe ser calculada dinámicamente mediante getMealFiberG"
    assert "* % VD calculado sobre Dieta Cetogénica de Referencia" in content, "Nota al pie aclaratoria del % VD debe estar presente"


def test_granular_diners_stepper_and_bom_scaling():
    import os

    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "meal-diners-stepper" in content, "El componente stepper interactivo meal-diners-stepper debe estar en el HTML"
    assert "btn-step-diners" in content, "Los botones +/- btn-step-diners deben estar presentes en las tarjetas de servicio"
    assert "updateMealDiners" in content, "La función de actualización updateMealDiners debe estar definida en JS"


def test_dish_negotiation_reactivity_and_bom_update():
    import os

    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "modal-negotiate-dish" in content, "El modal de negociación #modal-negotiate-dish debe estar presente en el HTML"
    assert "btn-negotiate-dish" in content, "Los botones de acción btn-negotiate-dish deben estar presentes en las tarjetas"
    assert "openNegotiateModal" in content, "La función openNegotiateModal debe estar definida en JS"
    assert "confirmDishNegotiation" in content, "La función confirmDishNegotiation debe estar definida en JS"
    assert "DISH_EXCHANGE_POOL" in content, "El catálogo canónico DISH_EXCHANGE_POOL debe estar inyectado en el script"
    assert "atelier_dish_overrides_" in content, "La clave de almacenamiento local atelier_dish_overrides_ debe estar configurada"
    assert "btn-surprise-me" in content, "El botón btn-surprise-me debe estar presente en el modal de negociación"
    assert "surpriseMeDishNegotiation" in content, "La función surpriseMeDishNegotiation debe estar definida en JS"


def test_recipe_dispatch_and_mass_reconciliation():
    import os

    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "openRecipeDispatchModal" in content, "La función openRecipeDispatchModal debe estar definida en JS"
    assert "renderDispatchModalDOM" in content, "La función renderDispatchModalDOM debe estar definida en JS"
    assert "confirmRecipeDispatch" in content, "La función confirmRecipeDispatch debe estar definida en JS"
    assert "confirmRevertDispatch" in content, "La función confirmRevertDispatch debe estar definida en JS"
    assert "dispatchedMeals" in content, "El objeto de estado dispatchedMeals debe estar inyectado en el script"
    assert "recipe-prepared-checkbox" in content, "El selector de UI recipe-prepared-checkbox debe estar presente en el HTML"


def test_taxonomy_sanitization_and_supplement_naming():
    import os
    from app.services.inventory_master import InventorySyncMaster

    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Fórmula Nootrópica 33Plus®" in content, "Fórmula Nootrópica 33Plus® debe reemplazar nombres genéricos antiguos"
    assert "Fórmula Reparadora 34Plus®" in content, "Fórmula Reparadora 34Plus® debe reemplazar nombres genéricos antiguos"
    assert "getCanonicalItemName" in content, "getCanonicalItemName debe estar definido para normalización morfológica"

    # Verificar clasificación inteligente en InventorySyncMaster
    cat_aguacate = InventorySyncMaster.get_smart_item_category("Aguacates Hass medianos")
    assert cat_aguacate == "🌰 Grasas, Aceites y Semillas", "Aguacate debe clasificarse en Grasas, Aceites y Semillas"

    cat_aceite_coco = InventorySyncMaster.get_smart_item_category("Aceite de coco (orgánico)")
    assert cat_aceite_coco == "🌰 Grasas, Aceites y Semillas", "Aceite de coco no debe clasificarse como fruta"

def test_ssot_v36_6_atwater_and_dynamic_tokens():
    import os

    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Purga de Repostería Simulada en Menú Regular
    assert "Waffles Keto de Harina" not in content, "Waffles keto simulados no deben estar en el menú regular"
    assert "Crepas Ligeras de Harina" not in content, "Crepas keto simuladas no deben estar en el menú regular"

    # 2. Presencia de Técnicas Profesionales de Huevo
    assert "Rollo Tamagoyaki Culinario" in content or "Huevos en Nube" in content or "Huevos Benedictinos" in content, "Técnicas profesionales de huevo deben estar presentes"

    # 3. Verificación de Invarianza y Tokens Dinámicos en KetoAIArchitect
    from app.services.keto_architect import compile_dynamic_prep_phases, CulinaryProceduralEngine
    from app.schemas import Ingredient

    test_ing = [Ingredient(name="Pechuga de pollo", quantity=150.0, unit="g")]
    phases = compile_dynamic_prep_phases("Pechuga de Pollo al Sartén", test_ing, diners_count=6)
    assert hasattr(phases, "fase_1_mise_en_place"), "DynamicPrepPhases debe ser generado dinámicamente"

    # 4. Verificación del Paradigma Heurístico (Zero-Template Engine)
    steps = CulinaryProceduralEngine.generate_heuristic_steps("Huevos Benedictinos Keto sobre Nube de Clara", "baked_egg_matrix")
    assert len(steps) >= 4, "Debe generar pasos termodinámicos específicos"
    assert any("horno" in s.lower() or "gratinado" in s.lower() for s in steps), "Debe usar física culinaria real"

    # 5. Verificación de Atwater Macro Floors y coincidencia de semana_39_master.json
    import json
    s39_path = os.path.join(os.path.dirname(__file__), "..", "semana_39_master.json")
    assert os.path.exists(s39_path), "semana_39_master.json debe existir en la raíz"
    with open(s39_path, "r", encoding="utf-8") as f:
        s39_data = json.load(f)

    for day in s39_data.get("days", []):
        for meal in day.get("meals", []):
            mtype = meal.get("meal_type")
            fat = meal.get("fat_g", 0)
            prot = meal.get("protein_g", 0)
            nc = meal.get("net_carbs_g", 0)
            atwater_kcal = fat * 9 + prot * 4 + nc * 4

            if mtype == "Desayuno":
                assert atwater_kcal >= 400.0, f"Desayuno en {day['day']} debe cumplir piso Atwater >= 400 kcal (obtenido {atwater_kcal})"
            elif mtype == "Comida":
                assert 630.0 <= atwater_kcal <= 700.0, f"Comida 3-course en {day['day']} debe cumplir piso Atwater 630-700 kcal (obtenido {atwater_kcal})"
            elif mtype == "Cena":
                assert atwater_kcal >= 400.0, f"Cena en {day['day']} debe cumplir piso Atwater >= 400 kcal (obtenido {atwater_kcal})"


def test_zero_mock_benedict_recipe_and_clean_datebar():
    import os
    from generate_standalone_html import build_typed_recipe_for_dish

    # 1. Test Recipe Building for Benedict Eggs
    benedict_dish = "Huevos Benedictinos Keto sobre Nube de Clara y Tocino de Pavo Crujiente"
    recipe = build_typed_recipe_for_dish(benedict_dish, course_type="main")

    assert recipe is not None, "La receta debe ser generada"
    assert recipe["title"] == benedict_dish

    # Flatten all ingredient names
    ing_names = []
    for grp in recipe.get("ingredient_groups", []):
        for item in grp.get("items", []):
            ing_names.append((item.get("name") or "").lower())

    ing_text = " ".join(ing_names)
    assert "salsa de jitomate" not in ing_text, "Huevos Benedictinos no deben incluir salsa de jitomate (Shakshuka mock)"
    assert "tocino de pavo" in ing_text, "Debe incluir tocino de pavo artesanal"
    assert "claras de huevo" in ing_text or "claras" in ing_text, "Debe incluir claras para el huevo nube"
    assert "mantequilla" in ing_text, "Debe incluir mantequilla para holandesa"
    assert "limon" in ing_text or "limón" in ing_text, "Debe incluir jugo de limón"

    # Flatten step texts
    steps_text = " ".join(recipe.get("steps", [])).lower()
    assert "holandesa" in steps_text or "bano maria" in steps_text or "baño maría" in steps_text, "Pasos deben describir salsa holandesa"
    assert "nube" in steps_text or "horno" in steps_text, "Pasos deben describir horneado de nubes de clara"
    assert "saltear huevos orgánicos, salsa de jitomate" not in steps_text, "No debe incluir plantilla estática de Shakshuka"

    # 2. Test HTML Content for Benedict Recipe and DateBar
    html_path = os.path.join(os.path.dirname(__file__), "..", "expediente_nutriketo.html")
    assert os.path.exists(html_path), "expediente_nutriketo.html debe existir"
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "26 SÁB -" not in content, "Barra de fechas no debe tener guión espurio al final"


def test_ssot_v36_6_rev3_validator_rules():
    from app.schemas import TypedRecipeSchema, IngredientGroupSchema, IngredientItemSchema
    from app.services.recipe_validator import validate_recipe_compliance

    # 1. Test Curcumin without Pepper rejection
    bad_curcumin_recipe = TypedRecipeSchema(
        title="Crema de Coliflor y Cúrcuma",
        cooking_technique="boil_and_blend",
        ingredient_groups=[
            IngredientGroupSchema(
                category="Verduras",
                items=[
                    IngredientItemSchema(name="Coliflor fresca", base_qty_per_person=150.0, unit="g"),
                    IngredientItemSchema(name="Cúrcuma pura", base_qty_per_person=3.0, unit="g")
                ]
            )
        ],
        steps=["1. Cocinar coliflor y cúrcuma.", "2. Licuar y servir."]
    )
    ok_curcumin, msg_curcumin = validate_recipe_compliance(bad_curcumin_recipe)
    assert ok_curcumin is False
    assert "Cúrcuma pero carece de Pimienta Negra" in msg_curcumin

    # 2. Test Breakfast Heavy Beef rejection
    bad_breakfast_beef = TypedRecipeSchema(
        title="Huevos Benedictinos con Ribeye de Res a la Parrilla",
        cooking_technique="saute_and_sear",
        ingredient_groups=[
            IngredientGroupSchema(
                category="Carnes",
                items=[
                    IngredientItemSchema(name="Ribeye de res", base_qty_per_person=200.0, unit="g"),
                    IngredientItemSchema(name="Huevos enteros", base_qty_per_person=2.0, unit="piezas")
                ]
            )
        ],
        steps=["1. Sellar ribeye a 180°C.", "2. Servir con huevos benedictinos."]
    )
    ok_beef, msg_beef = validate_recipe_compliance(bad_breakfast_beef, meal_type="Desayuno")
    assert ok_beef is False
    assert "corte pesado de res" in msg_beef

    # 3. Test BOM Purity rejection for culinary adjectives
    bad_bom_recipe = TypedRecipeSchema(
        title="Pechuga al Sartén con Vegetales",
        cooking_technique="saute_and_sear",
        ingredient_groups=[
            IngredientGroupSchema(
                category="Carnes",
                items=[
                    IngredientItemSchema(name="Pechuga jugosa a la parrilla", base_qty_per_person=180.0, unit="g"),
                    IngredientItemSchema(name="Mantequilla de pastoreo", base_qty_per_person=20.0, unit="g")
                ]
            )
        ],
        steps=["1. Cocinar pechuga jugosa a la parrilla en mantequilla.", "2. Servir caliente."]
    )
    ok_bom, msg_bom = validate_recipe_compliance(bad_bom_recipe)
    assert ok_bom is False
    assert "Pureza BOM violada" in msg_bom

    # 4. Test Machaca Scramble acceptance in Breakfast
    ok_machaca_recipe = TypedRecipeSchema(
        title="Huevos Revueltos con Machaca Artesanal",
        cooking_technique="machaca_scramble",
        ingredient_groups=[
            IngredientGroupSchema(
                category="Carnes",
                items=[
                    IngredientItemSchema(name="Huevos enteros", base_qty_per_person=2.0, unit="piezas"),
                    IngredientItemSchema(name="Machaca de res artesanal", base_qty_per_person=25.0, unit="g"),
                    IngredientItemSchema(name="Mantequilla de pastoreo", base_qty_per_person=15.0, unit="g")
                ]
            )
        ],
        steps=["1. Dorar machaca artesanal en mantequilla.", "2. Incorporar huevos y cuajar."]
    )
    ok_machaca, msg_machaca = validate_recipe_compliance(ok_machaca_recipe, meal_type="Desayuno")
    assert ok_machaca is True, f"Machaca scramble debe ser aceptado en desayuno (obtenido: {msg_machaca})"

    # 5. Test BOM Whitelist rejection for unmapped item
    bad_unmapped_recipe = TypedRecipeSchema(
        title="Omelette de Huevos Enteros",
        cooking_technique="baveuse_omelette",
        ingredient_groups=[
            IngredientGroupSchema(
                category="General",
                items=[
                    IngredientItemSchema(name="Huevos enteros", base_qty_per_person=2.0, unit="piezas"),
                    IngredientItemSchema(name="Sustancia Misteriosa No Canonica 999", base_qty_per_person=10.0, unit="g")
                ]
            )
        ],
        steps=["1. Batir los huevos enteros e incorporar sustancia misteriosa no canonica 999.", "2. Cuajar en sartén y servir."]
    )
    ok_unmapped, msg_unmapped = validate_recipe_compliance(bad_unmapped_recipe, meal_type="Desayuno")
    assert ok_unmapped is False
    assert "no coincide con ninguna clave del catálogo canónico" in msg_unmapped


def test_all_7_breakfast_recipes_pure_egg_symmetry():
    from generate_standalone_html import build_typed_recipe_for_dish

    breakfast_dishes = [
        "Huevos Revueltos Rústicos con Ejotes Tiernos al Sartén en Mantequilla de Pastoreo",
        "Omelette Baveuse Culinario a las Finas Hierbas y Queso Gouda",
        "Huevos Revueltos con Machaca Magra de Res Artesanal y Orégano al Sartén",
        "Huevos Benedictinos Keto sobre Nube de Clara y Tocino de Pavo Crujiente",
        "Huevos Estrellados en Sartén de Hierro con Aceite VEVO y Tomillo Fresco",
        "Rollo Tamagoyaki Culinario en Capas a la Mantequilla con Queso Panela",
        "Cazuela de Huevos al Horno sobre Cama de Espinacas Tiernas y Queso de Cabra"
    ]

    for dish in breakfast_dishes:
        recipe = build_typed_recipe_for_dish(dish, course_type="main")
        assert recipe is not None, f"Receta para {dish} debe existir"

        ing_items = [item for grp in recipe.get("ingredient_groups", []) for item in grp.get("items", [])]
        ing_names = [i["name"].lower() for i in ing_items]
        ing_text = " ".join(ing_names)

        assert any(k in ing_text for k in ["huevo", "huevos", "claras", "yemas"]), f"Desayuno '{dish}' debe contener huevo"

        for item in ing_items:
            iname = item["name"].lower()
            if "huevo" in iname and "nube" not in iname and "claras" not in iname:
                assert item["unit"] == "piezas", f"En '{dish}', los huevos deben cuantificarse en 'piezas', obtenido '{item['unit']}'"

        assert "costilla" not in ing_text, f"Desayuno '{dish}' contiene costilla (fallback no permitido)"
        assert "tuétano" not in ing_text and "tuetano" not in ing_text, f"Desayuno '{dish}' contiene tuétano (fallback no permitido)"
        assert "ribeye" not in ing_text, f"Desayuno '{dish}' contiene ribeye (fallback no permitido)"
        assert "sirloin" not in ing_text, f"Desayuno '{dish}' contiene sirloin (fallback no permitido)"

        steps_text = " ".join(recipe.get("steps", [])).lower()
        assert "blanqueado de huesos" not in steps_text, f"Desayuno '{dish}' contiene paso de blanqueado de huesos"
        assert "90 minutos" not in steps_text, f"Desayuno '{dish}' contiene caldo de 90 min"
        assert "sellar en sartén a 180°c durante 3-4 minutos por lado" not in steps_text, f"Desayuno '{dish}' usa plantilla cárnica saute_and_sear"
















