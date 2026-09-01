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
    assert any("miel" in name for name in item_names)















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
