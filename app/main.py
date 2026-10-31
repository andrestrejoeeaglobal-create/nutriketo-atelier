import os
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.schemas import (
    WeeklyMenuRequest, WeeklyMenuPlan,
    NegotiationRequest, NegotiationResponse,
    SuggestionRequest, SuggestionResponse,
    ShoppingSyncRequest, DishServedSyncRequest,
    PantryStatusResponse, ToggleShoppingRequest,
    InventoryIntakeRequest, InventoryIntakeResponse,
    CompilePhasesRequest, CompilePhasesResponse
)
from app.services.keto_architect import KetoAIArchitect, compile_dynamic_prep_phases
from app.services.inventory_master import InventorySyncMaster
from app.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando Arquitectura Herami API Server — Atelier T.I.L.O.®...")
    init_db()
    yield
    logger.info("Deteniendo Arquitectura Herami API Server...")

app = FastAPI(
    title="Arquitectura Herami API — Atelier T.I.L.O.®",
    description="Backend API RESTful con soporte multivista (Diseño Paramétrico, Fichas de Ensamblaje, Abastecimiento Tridimensional, Métricas Culinarias) e integración T.I.L.O. Cortex.",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

architect = KetoAIArchitect()

@app.middleware("http")
async def disable_browser_cache(request, call_next):
    if request.method == "OPTIONS":
        from fastapi.responses import Response
        preflight = Response(status_code=204)
        preflight.headers["Access-Control-Allow-Origin"] = request.headers.get("origin") or "*"
        preflight.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        preflight.headers["Access-Control-Allow-Headers"] = request.headers.get("access-control-request-headers") or "*"
        preflight.headers["Access-Control-Allow-Private-Network"] = "true"
        preflight.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return preflight
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin") or "*"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

app.mount("/static", StaticFiles(directory="app/static"), name="static")

from fastapi.responses import FileResponse, HTMLResponse

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(
        content=content,
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"}
    )

@app.get("/mobile", response_class=HTMLResponse)
def read_mobile():
    mobile_path = os.path.join(os.path.dirname(__file__), "static", "mobile.html")
    with open(mobile_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(
        content=content,
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"}
    )

@app.get("/expediente", response_class=FileResponse)
def read_expediente():
    exp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expediente_nutriketo.html")
    return FileResponse(
        exp_path,
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"}
    )

@app.post("/api/menu/generate", response_model=WeeklyMenuPlan, status_code=status.HTTP_200_OK)
def generate_menu(request: WeeklyMenuRequest):
    """
    Genera el plan de menú semanal con escalado atómico server-side en Python.
    """
    try:
        plan = architect.generate_weekly_plan(
            diners_count=request.diners_count,
            preferences=request.preferences
        )
        return plan
    except Exception as e:
        logger.error(f"Error al generar menú semanal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/menu/suggest", response_model=SuggestionResponse, status_code=status.HTTP_200_OK)
def suggest_menu_options(request: SuggestionRequest):
    """
    Retorna 3 sugerencias gastronómicas ultraligeras (<200ms) calibradas por comensales y cosecha.
    """
    try:
        response = architect.suggest_alternative_dishes(request)
        return response
    except Exception as e:
        logger.error(f"Error al obtener sugerencias de menú: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/menu/negotiate", response_model=NegotiationResponse, status_code=status.HTTP_200_OK)
def negotiate_menu(request: NegotiationRequest):
    """
    Procesa solicitudes de cambio de platillo con contraoferta obligatoria y reconstrucción 3D.
    """
    try:
        response = architect.negotiate_dish(request)
        return response
    except Exception as e:
        logger.error(f"Error en negociación de menú: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/shopping/items", status_code=status.HTTP_200_OK)
def get_shopping_items(day: Optional[str] = None, diners_count: int = 6):
    """
    Recupera el checklist interactivo de compras persistente en SQLite con escalado dinámico por diners_count.
    """
    try:
        items = InventorySyncMaster.get_shopping_list_items(day=day, diners_count=diners_count)
        return {"items": items, "diners_count": diners_count}
    except Exception as e:
        logger.error(f"Error al obtener checklist de compras: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/shopping/toggle", status_code=status.HTTP_200_OK)
def toggle_shopping_item(request: ToggleShoppingRequest):
    """
    Persiste en SQLite el estado del checkbox de compras (is_checked) y sincroniza la alacena.
    """
    try:
        success = InventorySyncMaster.toggle_shopping_item(request.item_id, request.is_checked)
        return {"success": success, "item_id": request.item_id, "is_checked": request.is_checked}
    except Exception as e:
        logger.error(f"Error al alternar estado de compras: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/inventory/shopping-check", response_model=PantryStatusResponse, status_code=status.HTTP_200_OK)
def sync_shopping_list(request: ShoppingSyncRequest):
    try:
        updated_pantry = InventorySyncMaster.sync_shopping_list(request.items)
        return PantryStatusResponse(pantry=updated_pantry)
    except Exception as e:
        logger.error(f"Error en sync_shopping_list: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/inventory/served-dish", response_model=PantryStatusResponse, status_code=status.HTTP_200_OK)
def sync_served_dish(request: DishServedSyncRequest):
    try:
        updated_pantry = InventorySyncMaster.sync_served_dish(request.dish_name, request.ingredients)
        return PantryStatusResponse(pantry=updated_pantry)
    except Exception as e:
        logger.error(f"Error en sync_served_dish: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/inventory/pantry", response_model=PantryStatusResponse, status_code=status.HTTP_200_OK)
def get_pantry():
    try:
        items = InventorySyncMaster.get_all_pantry_items()
        return PantryStatusResponse(pantry=items)
    except Exception as e:
        logger.error(f"Error al obtener alacena: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/inventory/intake", response_model=InventoryIntakeResponse, status_code=status.HTTP_200_OK)
def register_inventory_intake(request: InventoryIntakeRequest):
    try:
        response = InventorySyncMaster.register_inventory_intake(request)
        return response
    except Exception as e:
        logger.error(f"Error en register_inventory_intake: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/menu/compile-phases", response_model=CompilePhasesResponse, status_code=status.HTTP_200_OK)
def compile_phases(request: CompilePhasesRequest):
    """
    Micro-Agente de Ensamblaje JIT (V15.3.1):
    Compila asíncronamente las 4 fases técnicas para los platillos recibidos.
    """
    try:
        compiled_phases = {}
        for item in request.items:
            phases = compile_dynamic_prep_phases(item.dish_name, item.approved_ingredients, item.diners_count)
            compiled_phases[item.dish_name] = phases
        return CompilePhasesResponse(success=True, compiled_phases=compiled_phases)
    except Exception as e:
        logger.error(f"Error al compilar fases JIT: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/inventory/live-sync", status_code=status.HTTP_200_OK)
@app.post("/api/pantry/save-ssot", status_code=status.HTTP_200_OK)
async def live_sync_inventory_snapshot(payload: dict):
    """
    Persiste en tiempo real cualquier cambio de inventario realizado en el navegador
    (Alacena, Cuarentena y Cosecha Activa en Granja El Herami) hacia `pantry_live_state.json`
    y actualiza en vivo `DEFAULT_PANTRY_STOCK` en `menu_hard_gate_auditor.py`.
    """
    import json
    from app.services.menu_hard_gate_auditor import save_live_pantry_ssot
    try:
        root_dir = os.path.dirname(os.path.dirname(__file__))
        target_path = os.path.join(root_dir, "live_inventory_state.json")
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        ssot_res = save_live_pantry_ssot(payload)
        return {
            "status": "synced",
            "path": "pantry_live_state.json",
            "items_count": len(ssot_res.get("auditor_pantry", {})),
        }
    except Exception as e:
        logger.error(f"Error en live_sync_inventory_snapshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pantry/live-state", status_code=status.HTTP_200_OK)
async def get_live_pantry_ssot():
    """
    Retorna el estado SSOT vivo almacenado en `pantry_live_state.json`.
    """
    from app.services.menu_hard_gate_auditor import load_live_pantry_ssot
    res = load_live_pantry_ssot()
    return res.get("raw_state", {})



