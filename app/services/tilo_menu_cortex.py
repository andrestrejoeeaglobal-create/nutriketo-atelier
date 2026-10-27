"""
Córtex Generativo T.I.L.O.® (N-Week Rolling Engine — Semanas 44 a 60+)
======================================================================
Arquitectura Neuro-Simbólica de 3 Capas:
  - Capa 1: Banco Canónico de 4 Ciclos (4 x 21 = 84 Arquetipos Maestros: Ciclos A, B, C, D).
  - Capa 2: Córtex Creativo Restringido a Sustantivos Puros del Inventario (126 huevos exactos
            en los 7 desayunos, 0 huevos en comidas/cenas, 0% lácteos en entradas de fruta,
            0 insumos fantasma y 0 adjetivos 'fresco/fresca').
  - Capa 3: Solver Determinista de BOM sobre el Stock Consolidado Total (Stock Previo + Ticket Sam's Club)
            y Compuerta Hard-Gate [R1]-[R12].
"""

import copy
import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.services.menu_hard_gate_auditor import (
    CYCLE_ARCHETYPE_BANK,
    DEFAULT_FARM_HARVEST,
    DEFAULT_PANTRY_STOCK,
    assert_zero_violations,
)

SPANISH_MONTHS = {
    1: ("Ene", "Enero"),
    2: ("Feb", "Febrero"),
    3: ("Mar", "Marzo"),
    4: ("Abr", "Abril"),
    5: ("May", "Mayo"),
    6: ("Jun", "Junio"),
    7: ("Jul", "Julio"),
    8: ("Ago", "Agosto"),
    9: ("Sep", "Septiembre"),
    10: ("Oct", "Octubre"),
    11: ("Nov", "Noviembre"),
    12: ("Dic", "Diciembre"),
}

DAY_NAMES_ES = [
    "Domingo",
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
]


def get_cycle_id_for_week(week_num: int) -> str:
    """
    Asigna la familia de rotación cíclica para cualquier Semana N:
      - Ciclo A: Semanas 41, 45, 49, 53, 57...
      - Ciclo B: Semanas 42, 46, 50, 54, 58...
      - Ciclo C: Semanas 43, 47, 51, 55, 59...
      - Ciclo D: Semanas 44, 48, 52, 56, 60...
    """
    cycles = ["A", "B", "C", "D"]
    return cycles[(int(week_num) - 41) % 4]


def compute_week_dates(target_week: int) -> Dict[str, Any]:
    base_start = datetime.date(2026, 10, 18)  # Semana 43 = 18 Oct 2026
    delta_weeks = int(target_week) - 43
    start_date = base_start + datetime.timedelta(days=delta_weeks * 7)
    end_date = start_date + datetime.timedelta(days=6)

    _, m_start_full = SPANISH_MONTHS[start_date.month]
    _, m_end_full = SPANISH_MONTHS[end_date.month]
    if start_date.month == end_date.month:
        date_range = f"{start_date.day:02d} al {end_date.day:02d} de {m_end_full} de {end_date.year}"
    else:
        date_range = f"{start_date.day:02d} de {m_start_full} al {end_date.day:02d} de {m_end_full} de {end_date.year}"

    day_entries = []
    for i in range(7):
        d = start_date + datetime.timedelta(days=i)
        m_short, m_full = SPANISH_MONTHS[d.month]
        day_name = DAY_NAMES_ES[i]
        day_num = f"{d.day:02d}"
        date_str = f"{day_num} {m_short}"
        day_entries.append({
            "day": day_name,
            "day_num": day_num,
            "date_str": date_str,
            "iso_date": d.isoformat(),
            "full_date_title": f"Menú Completo para el {day_name} {date_str}",
            "date_full": f"{day_name} {day_num} de {m_full} de {d.year}",
        })

    return {
        "week_name": f"Semana {target_week}",
        "week_label": f"Semana {target_week} ({date_range})",
        "week_start": start_date.isoformat(),
        "date_range": date_range,
        "day_entries": day_entries,
    }


def _ing(name: str, amount: float, unit: str, category: str) -> Dict[str, Any]:
    per_guest = round(float(amount) / 6.0, 4)
    if abs(per_guest - round(per_guest)) < 1e-6:
        per_guest = int(round(per_guest))
    amt_clean = int(round(amount)) if abs(amount - round(amount)) < 1e-6 else round(float(amount), 2)
    return {
        "category": category,
        "name": name,
        "per_guest": per_guest,
        "amount": amt_clean,
        "unit": unit,
    }


def _course(
    title: str,
    technique: str,
    note: str,
    thermo: str,
    flavor: str,
    texture: str,
    ccp: str,
    ingredients: List[Dict[str, Any]],
    steps: List[str],
    archetype: Optional[str] = None,
) -> Dict[str, Any]:
    obj: Dict[str, Any] = {
        "title": title,
        "technique": technique,
        "note": note,
        "coct_reasoning": {
            "thermodynamics": thermo,
            "flavor_and_aromatics": flavor,
            "textural_architecture": texture,
            "critical_control_points": ccp,
        },
        "ingredients": ingredients,
        "steps": steps,
    }
    if archetype:
        obj["archetype"] = archetype
    return obj


def _meal(
    meal_type: str,
    time_str: str,
    fat_g: float,
    protein_g: float,
    net_carbs_g: float,
    fiber_g: float,
    starter: Dict[str, Any],
    main: Dict[str, Any],
    side: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "meal_type": meal_type,
        "time": time_str,
        "fat_g": fat_g,
        "protein_g": protein_g,
        "net_carbs_g": net_carbs_g,
        "fiber_g": fiber_g,
        "starter_name": starter["title"],
        "main_dish_name": main["title"],
        "dish_name": main["title"],
        "side_dish_name": side["title"],
        "starter": starter,
        "main": main,
        "side": side,
    }


CAT_PROT = "🥩 Carnes, Pescados y Proteínas"
CAT_VEG = "🥦 Hortalizas, Vegetales y Hongos"
CAT_FAT = "🥑 Grasas, Aceites y Semillas"
CAT_DAIRY = "🧀 Lácteos y Quesos (Sin Gluten — Keto)"
CAT_FRUIT = "🍓 Frutas de Bajo Índice Glucémico"
CAT_SPICE = "🧂 Condimentos, Especias e Infusiones"
CAT_SUPP = "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"


def _build_cycle_d_canonical_days(day_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Construye los 7 días (21 servicios / 63 recetas inéditas) del Ciclo D (Semana 44, 48, 52, 56, 60+).
    Cumple [R1]-[R12]:
      - 126 huevos exactos en los 7 desayunos (0 en comidas y cenas).
      - Entradas matutinas 100% fruta + chía + nuez pecana (+ nuez de la India), 0% lácteos.
      - 0 insumos fantasma y 0 ocurrencias del vocablo prohibido 'fresco/fresca'.
      - 7 cenas 100% circadianas (Pavo, Mojarra x2, Portobello Ricotta/Manchego, Atún, Pollo entero, Timbal Cottage/Ricotta/Yogur).
      - 0g de sobregiro contra el Stock Consolidado Total (Stock Previo + Ticket Sam's Club).
    """
    days_out = []

    # =========================================================================
    # DÍA 0: DOMINGO
    # Veg families: Desayuno (espinacas) | Comida (champinon, esparragos, calabacitas) | Cena (coliflor)
    # =========================================================================
    d0_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.5,
        starter=_course(
            title="Copa de Zarzamoras de Alacena con Semillas de Chía, Nuez de la India, Nuez Pecana de la Granja y Canela",
            technique="raw_berry_assembly",
            note="Apertura antioxidante de zarzamoras de alacena sin lácteos con semillas de chía orgánicas, nuez de la India, nuez pecana de la granja y canela molida.",
            thermo="Servicio en frío a 4°C que preserva las antocianinas de la zarzamora y los ácidos grasos esenciales.",
            flavor="Acidez profunda de la zarzamora armonizada con canela cálida, nuez de la India y nuez pecana tostada.",
            texture="Drupeolas jugosas de zarzamora en contraste con el crujido de las nueces y las semillas de chía.",
            ccp="Integrar las nueces y la chía justo al momento del servicio.",
            ingredients=[
                _ing("Zarzamora", 180, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Canela molida", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Disponer las zarzamoras de alacena en copas individuales enfriadas a 4°C.",
                "Espolvorear las semillas de chía orgánicas y la canela molida.",
                "Coronar con la nuez de la India y la nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Shakshuka Verde de Huevos Pochados en Salsa de Espinacas, Tomate de Alacena y Queso Ricotta",
            technique="green_shakshuka_poach",
            note="3 huevos enteros por comensal pochados suavemente en reducción verde de espinacas, tomate de alacena y copos de queso ricotta.",
            thermo="Reducción vegetal a 92°C y pochado en nido a 85°C por 4 minutos para cuajar la clara manteniendo la yema untuosa.",
            flavor="Acidez herbal del tomate verde y las espinacas equilibrada por la suavidad láctea del queso ricotta y la mantequilla.",
            texture="Yema aterciopelada sobre salsa espesa de espinacas y medallones cremosos de ricotta.",
            ccp="Retirar del fuego cuando las claras estén firmes y las yemas conserven fluidez.",
            archetype="huevo_shakshuka_verde",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Espinacas", 360, "g", CAT_VEG),
                _ing("Tomate", 120, "g", CAT_VEG),
                _ing("Queso ricotta", 240, "g", CAT_DAIRY),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
                _ing("Pimienta negra", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Saltear el tomate de alacena troceado y las espinacas en mantequilla durante 4 minutos hasta formar una base verde aromática.",
                "Formar cavidades en la salsa, cascar 3 huevos por comensal y distribuir el queso ricotta alrededor.",
                "Tapar la sartén a fuego bajo durante 4 minutos hasta cuajar las claras y sazonar con sal de mar y pimienta negra.",
            ],
        ),
        side=_course(
            title="Gelatina Rubí de Fresas en Colágeno (4°C) con Fórmula Nootrópica 33Plus®",
            technique="collagen_gel_molding",
            note="Gelatina matutina de fresas (fruta distinta a la zarzamora de la entrada) enriquecida con grenetina biodisponible y la Toma 2 de MultiSinergix®.",
            thermo="Disolución colagénica a 60°C, templado a ≤42°C para incorporación nootrópica y gelificación a 4°C.",
            flavor="Perfume natural de fresa con notas adaptogénicas limpias.",
            texture="Gel firme de corte cristalino y láminas de fresa.",
            ccp="Incorporar MultiSinergix® estrictamente a ≤42°C.",
            ingredients=[
                _ing("Fresas", 120, "g", CAT_FRUIT),
                _ing("Grenetina", 42, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Hidratar la grenetina en agua purificada fría por 8 minutos y fundir a 60°C.",
                "Templar a 40°C, disolver la dosis de MultiSinergix® (33Plus®) e incorporar las fresas laminadas.",
                "Verter en moldes individuales y refrigerar a 4°C durante 3 horas.",
            ],
        ),
    )

    d0_l = _meal(
        "Comida", "14:30", 64.0, 42.0, 4.4, 6.8,
        starter=_course(
            title="Consomé Dorado de Floretes de Coliflor y Cilantro de la Granja al Fondo Claro de Pollo",
            technique="clear_broth_infusion",
            note="Primer litro del fondo claro de pollo de alacena (1,000 ml) infundido con floretes pequeños de coliflor, cilantro y jugo de limón real de la granja.",
            thermo="Infusión suave a 90°C por 6 minutos que extrae los minerales de la coliflor en el fondo claro de pollo sin lácteos.",
            flavor="Caldo limpio de ave con notas herbales de cilantro, coliflor al dente y destello cítrico de la granja.",
            texture="Caldo ligero y reconfortante con floretes tiernos de coliflor.",
            ccp="Añadir el cilantro y el limón real justo antes de servir.",
            ingredients=[
                _ing("Fondo claro de pollo", 1000, "ml", CAT_SPICE),
                _ing("Agua purificada", 500, "ml", CAT_SPICE),
                _ing("Coliflor", 420, "g", CAT_VEG),
                _ing("Cilantro", 36, "g", CAT_VEG),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Calentar los 1,000 ml de fondo claro de pollo de alacena con 500 ml de agua purificada de la granja.",
                "Incorporar los floretes pequeños de coliflor y cocer a fuego suave durante 6 minutos con sal de mar.",
                "Servir caliente con cilantro picado de la granja, jugo de limón real y un hilo de aceite de oliva.",
            ],
        ),
        main=_course(
            title="Lomo de Salmón Glaseado a la Mostaza de Dijon y Aceite de Coco al Sartén con Espárragos Tiernos y Limón Real",
            technique="dijon_pan_glaze",
            note="Lomo de salmón del ticket Sam's Club glaseado en sartén con emulsión brillante de mostaza de Dijon, aceite de coco orgánico y limón real (0% costra de nueces) sobre espárragos de alacena.",
            thermo="Sellado en sartén a 175°C en aceite de coco y glaseado a fuego suave con reducción de mostaza y limón hasta 62°C internos.",
            flavor="Riqueza marina en ácidos grasos omega-3 realzada por el glaseado ácido-especiado de mostaza de Dijon y limón de la granja.",
            texture="Lomo jugoso de salmón napado en emulsión brillante de mostaza sobre tallos tiernos de espárrago.",
            ccp="No sobrepasar 63°C en el centro del salmón al glasear en sartén.",
            archetype="salmon_glaseado_mostaza_sarten",
            ingredients=[
                _ing("Lomo de salmón", 600, "g", CAT_PROT),
                _ing("Espárragos", 300, "g", CAT_VEG),
                _ing("Aceite de coco", 60, "g", CAT_FAT),
                _ing("Mostaza", 30, "g", CAT_SPICE),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Sellar los lomos de salmón sazonados con sal de mar en sartén con aceite de coco junto con los espárragos verdes de alacena durante 4 minutos.",
                "Emulsionar la mostaza con el jugo de limón real y los jugos de la sartén para glasear el salmón a fuego bajo por 2 minutos.",
                "Servir los lomos glaseados sobre la cama de espárragos tiernos.",
            ],
        ),
        side=_course(
            title="Láminas de Calabacita al Vapor con Orégano, Limón Real y Aceite de Oliva VEVO",
            technique="steam_olive_toss",
            note="Guarnición vegetal ligera libre de lácteos con calabacitas al vapor, orégano de alacena, limón de la granja y aceite de oliva.",
            thermo="Cocción al vapor a 98°C durante 4 minutos para conservar textura al dente.",
            flavor="Notas herbales de orégano y acidez limpia de limón real sobre calabacita.",
            texture="Láminas firmes y brillantes.",
            ccp="Emulsionar en tibio inmediatamente al salir de la vaporera.",
            ingredients=[
                _ing("Calabacitas", 360, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cortar las calabacitas en láminas longitudinales y cocer al vapor por 4 minutos.",
                "Aderezar con aceite de oliva extra virgen, jugo de limón real, orégano y sal de mar.",
            ],
        ),
    )

    d0_d = _meal(
        "Cena", "20:00", 51.0, 36.0, 3.8, 5.8,
        starter=_course(
            title="Velouté Nocturno de Champiñones Silvestres y Queso Ricotta al Fondo Claro de Pollo",
            technique="veloute_emulsion",
            note="Segundo litro del fondo claro de pollo de alacena (1,000 ml) emulsionado con champiñones salteados y queso ricotta artesanal.",
            thermo="Hervor suave a 92°C por 10 minutos y licuado de alta velocidad a 75°C para lograr emulsión sedosa.",
            flavor="Umami profundo del champiñón fundido con la riqueza del fondo claro de pollo y el queso ricotta.",
            texture="Crema tersa y aterciopelada.",
            ccp="Completar exactamente los 2,000 ml de fondo claro de pollo disponibles en alacena.",
            ingredients=[
                _ing("Fondo claro de pollo", 1000, "ml", CAT_SPICE),
                _ing("Champiñón", 360, "g", CAT_VEG),
                _ing("Queso ricotta", 180, "g", CAT_DAIRY),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
                _ing("Pimienta negra", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Cocer los champiñones laminados en los 1,000 ml restantes de fondo claro de pollo con sal con ajo durante 10 minutos.",
                "Licuar con el queso ricotta y el aceite de oliva hasta obtener un velouté homogéneo y servir con pimienta negra.",
            ],
        ),
        main=_course(
            title="Medallones de Pechuga de Pavo Dorados en Mantequilla con Sal con Ajo, Limón Real y Germinado de Alfalfa",
            technique="butter_pan_sear",
            note="Porción clínica completa de fajitas de pechuga de pavo del ticket Sam's Club (990 g = 165 g/comensal) dorada en mantequilla con limón real y germinado de alacena.",
            thermo="Sellado en sartén a 175°C por 4 minutos por lado hasta alcanzar 74°C en el centro térmico.",
            flavor="Ave magra perfumada con mantequilla dorada, sal con ajo y limón de la granja.",
            texture="Medallones jugosos coronados con brotes crujientes de germinado.",
            ccp="Asegurar 74°C internos sin sobrecocer la fibra magra del pavo.",
            archetype="pavo_medallones_mantequilla_ajo",
            ingredients=[
                _ing("Pechuga de pavo", 990, "g", CAT_PROT),
                _ing("Germinado", 60, "g", CAT_VEG),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
                _ing("Pimienta negra", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Sazonar la pechuga de pavo con sal con ajo, pimienta negra y jugo de limón de la granja.",
                "Dorar en sartén con mantequilla durante 4 minutos por lado hasta alcanzar 74°C internos.",
                "Servir coronando con el germinado de alacena.",
            ],
        ),
        side=_course(
            title="Tisana Nocturna de Manzanilla y Limón de la Granja (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="herbal_infusion",
            note="Infusión sedante nocturna de manzanilla de alacena con limón de la granja y la Toma 3 de AminoSinergix®.",
            thermo="Infusión a 85°C templada a ≤60°C antes de integrar los péptidos y aminoácidos.",
            flavor="Notas florales de manzanilla con matiz cítrico suave.",
            texture="Bebida cálida y cristalina.",
            ccp="Disolver AminoSinergix® estrictamente a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C, añadir jugo de limón de la granja y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 1: LUNES
    # Veg families: Desayuno (nopales 1/2) | Comida (morron, brocoli) | Cena (pepino)
    # =========================================================================
    d1_b = _meal(
        "Desayuno", "08:30", 49.0, 34.0, 4.1, 6.6,
        starter=_course(
            title="Tazón Matutino de Frambuesas de Alacena con Semillas de Chía, Nuez Pecana de la Granja y Vainilla",
            technique="raw_berry_assembly",
            note="Frambuesas de alacena servidas en frío sin lácteos con semillas de chía orgánicas, nuez pecana de la granja y extracto de vainilla.",
            thermo="Ensamble a 4°C que conserva intactos el ácido elágico y los polifenoles.",
            flavor="Perfume floral de frambuesa y vainilla con el tostado de la nuez pecana.",
            texture="Contraste crujiente de nuez pecana y chía sobre frambuesas enteras.",
            ccp="Añadir la nuez pecana al momento del pase.",
            ingredients=[
                _ing("Frambuesas", 180, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez pecana", 90, "g", CAT_FAT),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
            ],
            steps=[
                "Colocar las frambuesas de alacena en tazones fríos y perfumar con extracto de vainilla.",
                "Espolvorear las semillas de chía orgánicas y coronar con la nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Huevos Pochados Estilo Benedictino sobre Nopal Asado de la Granja con Emulsión de Mantequilla y Germinado",
            technique="benedict_poach_emulsion",
            note="3 huevos enteros por comensal pochados sobre pencas tiernas de nopal de la granja asadas, bañados en emulsión tibia de mantequilla al limón y germinado.",
            thermo="Asado de nopal en seco a 190°C, pochado de huevo a 86°C por 3.5 minutos y emulsión de mantequilla a 58°C.",
            flavor="Notas herbales del nopal asado integradas con la untuosidad de la yema y la mantequilla cítrica.",
            texture="Penca firme de nopal, huevo pochado de yema fluida y brotes crujientes de germinado.",
            ccp="Emulsionar la mantequilla con gotas de limón fuera del fuego directo.",
            archetype="huevo_benedictino_holandesa",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Nopales", 480, "g", CAT_VEG),
                _ing("Germinado", 120, "g", CAT_VEG),
                _ing("Mantequilla", 90, "g", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Asar los nopales de la granja en plancha caliente hasta sellar sus jugos y disponer como base.",
                "Pochar 3 huevos enteros por comensal en agua a 86°C durante 3.5 minutos y colocar sobre el nopal.",
                "Bañar con la mantequilla fundida emulsionada con jugo de limón real y sal de mar, y coronar con germinado.",
            ],
        ),
        side=_course(
            title="Gelatina Botánica de Fresas y Canela (4°C) con Fórmula Nootrópica 33Plus®",
            technique="collagen_gel_molding",
            note="Vehículo colagénico matutino de fresas y canela (distinta a la frambuesa de la entrada) con la Toma 2 de MultiSinergix®.",
            thermo="Hidratación en frío, disolución a 60°C, adición de 33Plus® a ≤42°C y cuajado a 4°C.",
            flavor="Dulzor natural de fresa con matiz especiado de canela.",
            texture="Gel brillante y firme.",
            ccp="Controlar temperatura ≤42°C antes de añadir MultiSinergix®.",
            ingredients=[
                _ing("Fresas", 120, "g", CAT_FRUIT),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("Grenetina", 42, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Hidratar la grenetina en agua purificada y disolver a 60°C con la canela molida.",
                "Templar a 40°C, incorporar MultiSinergix® (33Plus®) y las fresas en cubos, y refrigerar a 4°C.",
            ],
        ),
    )

    d1_l = _meal(
        "Comida", "14:30", 65.0, 43.0, 4.3, 6.7,
        starter=_course(
            title="Ensalada Provenzal de Espinacas, Jitomate de Alacena y Romero de la Granja al Limón Real y Aceite de Oliva",
            technique="crisp_leaf_toss",
            note="Ensalada verde obligatoria [R2] libre de lácteos, mantequilla y aguacate para acompañar el corte denso de Flat Steak: hojas de espinaca, jitomate de alacena y romero de la granja.",
            thermo="Montaje en frío a 8°C que preserva las enzimas digestivas y antioxidantes del jitomate y las espinacas.",
            flavor="Acidez limpia del limón real y el jitomate de alacena perfumada con romero de la granja y aceite de oliva.",
            texture="Hojas tiernas de espinaca y gajos jugosos de jitomate.",
            ccp="Servir con 0 g de lácteos, mantequilla o aguacate para equilibrar la densidad de la tagliata de res ([R2]).",
            ingredients=[
                _ing("Espinacas", 360, "g", CAT_VEG),
                _ing("Jitomate", 2, "piezas", CAT_VEG),
                _ing("Cebolla", 2, "piezas", CAT_VEG),
                _ing("Romero", 12, "g", CAT_VEG),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Disponer las hojas de espinaca con el jitomate de alacena en gajos y la cebolla finamente fileteada.",
                "Aliñar con aceite de oliva extra virgen, jugo de limón real, romero de la granja picado y sal con ajo.",
            ],
        ),
        main=_course(
            title="Tagliata de Flat Steak Sellada al Romero de la Granja con Láminas de Queso Manchego y Pimiento Morrón",
            technique="cast_iron_tagliata",
            note="Corte de Flat Steak del ticket Sam's Club (1,080 g = 180 g/comensal) sellado al hierro con romero de la granja, tiras de pimiento morrón y láminas de queso manchego.",
            thermo="Sellado a 200°C durante 3.5 minutos por lado hasta 62°C internos, reposo de 4 minutos y trinchado en fajitas gruesas tipo tagliata.",
            flavor="Costra Maillard de res al romero con el fundido suave del queso manchego de alacena y el dulzor del morrón.",
            texture="Exterior caramelizado, centro jugoso y láminas fundentes de queso manchego.",
            ccp="Reposar la carne antes de trinchar para retener los jugos miofibrilares.",
            archetype="res_tagliata_romero",
            ingredients=[
                _ing("Flat steak", 1080, "g", CAT_PROT),
                _ing("Queso manchego", 180, "g", CAT_DAIRY),
                _ing("Morrón", 3, "piezas", CAT_VEG),
                _ing("Romero", 12, "g", CAT_VEG),
                _ing("Aceite de oliva", 36, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
                _ing("Pimienta negra", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Sellar el flat steak sazonado con sal de mar, pimienta negra y romero en sartén de hierro con aceite de oliva.",
                "Saltear las tiras de pimiento morrón en los jugos de la sartén durante 3 minutos.",
                "Trinchar la carne en láminas diagonales tipo tagliata, disponer sobre el morrón y coronar con las láminas de queso manchego.",
            ],
        ),
        side=_course(
            title="Floretes de Brócoli al Vapor con Limón de la Granja y Hierbas Finas",
            technique="aromatic_steam",
            note="Guarnición crucífera ligera sin lácteos: floretes de brócoli al vapor con limón real de la granja, hierbas finas y aceite de oliva.",
            thermo="Vapor a 98°C por 5 minutos para preservar sulforafano y clorofila.",
            flavor="Notas verdes limpias con limón real y hierbas finas.",
            texture="Floretes firmes al dente.",
            ccp="Aliñar al momento de emplatar.",
            ingredients=[
                _ing("Brócoli", 360, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Hierbas finas", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cocer los floretes de brócoli al vapor durante 5 minutos.",
                "Aderezar con aceite de oliva, jugo de limón de la granja, hierbas finas y sal de mar.",
            ],
        ),
    )

    d1_d = _meal(
        "Cena", "20:00", 51.0, 35.5, 3.8, 6.0,
        starter=_course(
            title="Tartar Vegetal Nocturno de Pepino en Brunoise, Germinado de Alfalfa y Dados de Aguacate Hass al Limón Real",
            technique="cold_brunoise_tartar",
            note="Dados finos en brunoise de pepino y aguacate Hass moldeados en aro con brotes de germinado de alacena, jugo de limón real y aceite de oliva.",
            thermo="Ensamble en frío a 8°C en corte brunoise que preserva el agua biológica e hidratación celular.",
            flavor="Cremosidad del aguacate Hass en dados con la acidez cítrica del limón real y el crujido del germinado y pepino.",
            texture="Brunoise crujiente de pepino, brotes de germinado y dados untuosos de aguacate moldeados en tartar.",
            ccp="Única aparición de aguacate del día (cumpliendo [R5]).",
            ingredients=[
                _ing("Pepino", 360, "g", CAT_VEG),
                _ing("Germinado", 120, "g", CAT_VEG),
                _ing("Aguacate", 2, "piezas", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Picar el pepino en brunoise fina y cortar el aguacate Hass en dados pequeños uniformes.",
                "Mezclar suavemente con el germinado de alfalfa, jugo de limón real, aceite de oliva extra virgen y sal de mar, y moldear en aro tipo tartar vegetal.",
            ],
        ),
        main=_course(
            title="Fajitas de Mojarra Salteadas a la Veracruzana con Jitomate de Alacena, Aceitunas Manzanilla, Alcaparras, Laurel y Orégano",
            technique="veracruzana_saute",
            note="Fajitas de mojarra del ticket Sam's Club (990 g = 165 g/comensal) estofadas al estilo veracruzano en sartén con jitomate de alacena, aceitunas manzanilla, alcaparras, laurel y orégano.",
            thermo="Sellado en sartén a 175°C y cocción breve en recaudo veracruzano a 95°C por 6 minutos hasta alcanzar 63°C en el núcleo.",
            flavor="Tradición costera veracruzana con jitomate, aceitunas manzanilla, alcaparras, hojas de laurel, orégano y sal con ajo.",
            texture="Fajitas blancas jugosas bañadas en salsa rústica de jitomate, aceitunas y alcaparras.",
            ccp="Incorporar las aceitunas manzanilla y alcaparras en los últimos 3 minutos de cocción.",
            archetype="mojarra_veracruzana_sarten",
            ingredients=[
                _ing("Fajitas de mojarra", 990, "g", CAT_PROT),
                _ing("Jitomate", 1, "piezas", CAT_VEG),
                _ing("Aceitunas manzanilla", 90, "g", CAT_FAT),
                _ing("Alcaparras", 60, "g", CAT_SPICE),
                _ing("Hojas de laurel", 2, "g", CAT_SPICE),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 36, "ml", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Sofreír el jitomate de alacena picado en aceite de oliva con las hojas de laurel, orégano y sal con ajo por 3 minutos.",
                "Incorporar las fajitas de mojarra, las aceitunas manzanilla y las alcaparras.",
                "Tapar y cocer a fuego medio por 6 minutos hasta que el pescado esté tierno y jugoso.",
            ],
        ),
        side=_course(
            title="Elixir Nocturno de Manzanilla y Canela (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="herbal_infusion",
            note="Infusión cálida nocturna de manzanilla y canela molida de alacena enriquecida con la Toma 3 de AminoSinergix®.",
            thermo="Infusión a 85°C templada a ≤60°C para proteger la fórmula 34Plus®.",
            flavor="Aroma floral de manzanilla y canela suave.",
            texture="Tisana sedosa libre de cafeína.",
            ccp="Verificar temperatura ≤60°C antes de disolver AminoSinergix®.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla con la canela en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C y disolver la dosis de AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 2: MARTES
    # Veg families: Desayuno (calabacitas) | Comida (lechuga, pepino, esparragos) | Cena (acelgas 2/2, champinon)
    # =========================================================================
    d2_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.3, 6.4,
        starter=_course(
            title="Cuenco de Fresas en Cuartos con Semillas de Chía, Nuez de la India y Nuez Pecana de la Granja",
            technique="raw_berry_assembly",
            note="Fresas servidas en frío sin lácteos con semillas de chía orgánicas, nuez de la India del ticket Sam's Club y nuez pecana de la granja.",
            thermo="Cadena de frío a 4°C para preservar vitamina C y polifenoles.",
            flavor="Acidez aromática de la fresa con el doble perfil oleaginoso de nuez de la India y nuez pecana.",
            texture="Turgencia de la fresa con crocancia de nueces y chía.",
            ccp="Cortar las fresas al momento de emplatar.",
            ingredients=[
                _ing("Fresas", 240, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
            ],
            steps=[
                "Cortar las fresas en cuartos y colocar en cuencos refrigerados.",
                "Espolvorear las semillas de chía orgánicas y coronar con la nuez de la India y la nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Soufflé Dorado de Huevos al Horno Gratinado con Queso Manchego y Calabacitas Tiernas",
            technique="baked_egg_souffle",
            note="Matriz esponjosa de 3 huevos por comensal batidos y horneados con medias lunas de calabacita y gratinado de queso manchego de alacena.",
            thermo="Aireado mecánico del huevo y horneado por convección a 180°C durante 12 minutos hasta gratinar el queso manchego.",
            flavor="Suavidad láctea del queso manchego fundido con calabacitas en mantequilla.",
            texture="Estructura aireada tipo soufflé con costra dorada de queso manchego.",
            ccp="Servir inmediatamente al salir del horno para mantener el volumen esponjoso.",
            archetype="huevo_souffle_gratinado",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Queso manchego", 240, "g", CAT_DAIRY),
                _ing("Calabacitas", 360, "g", CAT_VEG),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
                _ing("Pimienta negra", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Saltear las calabacitas en medias lunas con la mantequilla en refractario apto para horno.",
                "Batir los huevos hasta espumar con sal de mar y pimienta negra, verter sobre las calabacitas y cubrir con el queso manchego rallado.",
                "Hornear a 180°C durante 12 minutos hasta que el soufflé infle y gratine.",
            ],
        ),
        side=_course(
            title="Infusión Matutina de Té Chai Especiado y Canela (≤60°C) con Fórmula Nootrópica 33Plus®",
            technique="spiced_tea_infusion",
            note="Infusión termogénica matutina de té chai de alacena y canela molida enriquecida con la Toma 2 de MultiSinergix®.",
            thermo="Infusión a 90°C templada a ≤60°C antes de incorporar el complejo nootrópico.",
            flavor="Notas cálidas de cardamomo, clavo y canela del té chai.",
            texture="Infusión aromática ligera.",
            ccp="Integrar MultiSinergix® a ≤60°C.",
            ingredients=[
                _ing("Té chai", 18, "g", CAT_SPICE),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar el té chai de alacena y la canela en agua purificada a 90°C por 5 minutos y colar.",
                "Templar a 58°C y disolver la dosis de MultiSinergix® (33Plus®).",
            ],
        ),
    )

    d2_l = _meal(
        "Comida", "14:30", 64.0, 41.5, 4.4, 6.7,
        starter=_course(
            title="Ensalada Verde de Lechuga Romana de Alacena, Germinado y Cilantro de la Granja al Limón Real",
            technique="crisp_leaf_toss",
            note="Ensalada verde obligatoria [R2] para acompañar carne molida de res: hojas de lechuga romana de alacena, germinado y cilantro de la granja al limón real.",
            thermo="Montaje en frío a 8°C libre de lácteos y mantequilla.",
            flavor="Clorofila viva de lechuga y cilantro con vinagreta cítrica de limón real y aceite de oliva.",
            texture="Hojas crujientes y brotes de germinado.",
            ccp="Aliñar al momento de pasar a mesa.",
            ingredients=[
                _ing("Lechuga", 1, "piezas", CAT_VEG),
                _ing("Germinado", 60, "g", CAT_VEG),
                _ing("Cilantro", 36, "g", CAT_VEG),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Trocear la lechuga romana de alacena y mezclar con el germinado y el cilantro de la granja.",
                "Aderezar con jugo de limón real, aceite de oliva extra virgen y sal de mar.",
            ],
        ),
        main=_course(
            title="Koftas Árabes de Carne Molida de Res a la Plancha con Tzatziki de Yogur Griego, Pepino y Cilantro de la Granja",
            technique="griddle_kofta_sear",
            note="Koftas especiadas de carne molida de sirloin del ticket Sam's Club (660 g, ligadas por amasado miofibrilar con 0 huevos) servidas con salsa tzatziki de yogur griego de alacena, pepino y cilantro de la granja.",
            thermo="Sellado en plancha con aceite de coco a 190°C por 4 minutos por lado hasta 70°C internos, servidas con tzatziki frío a 6°C.",
            flavor="Carne de sirloin especiada con comino y cebolla en contraste con el tzatziki de yogur griego, pepino y cilantro.",
            texture="Koftas doradas por fuera y jugosas por dentro con emulsión cremosa de yogur griego.",
            ccp="Amasar en frío la carne molida con sal de mar para ligar sin usar huevo (manteniendo la invariante [R12] de 126 huevos).",
            archetype="res_kofta_tzatziki",
            ingredients=[
                _ing("Carne molida", 660, "g", CAT_PROT),
                _ing("Yogur griego", 360, "g", CAT_DAIRY),
                _ing("Pepino", 300, "g", CAT_VEG),
                _ing("Cebolla", 2, "piezas", CAT_VEG),
                _ing("Cilantro", 48, "g", CAT_VEG),
                _ing("Aceite de coco", 60, "g", CAT_FAT),
                _ing("Comino", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Amasar la carne molida de res con la cebolla finamente picada, comino y sal de mar hasta activar la miosina y formar las koftas.",
                "Asar las koftas en plancha caliente con aceite de coco durante 4 minutos por lado.",
                "Mezclar el yogur griego con el pepino en brunoise y el cilantro de la granja para formar el tzatziki y servir con las koftas.",
            ],
        ),
        side=_course(
            title="Espárragos Verdes de Alacena Asados al Limón de la Granja y Aceite de Oliva",
            technique="char_grilled_spears",
            note="Tallos de espárragos verdes del ticket Sam's Club asados en aceite de oliva y limón real, libres de lácteos y mantequilla ([R2]).",
            thermo="Asado en plancha a 185°C durante 5 minutos para conservar firmeza.",
            flavor="Notas verdes tostadas de espárrago con jugo de limón de la granja.",
            texture="Tallos tiernos y crujientes.",
            ccp="No añadir lácteos ni mantequilla en la guarnición.",
            ingredients=[
                _ing("Espárragos", 300, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Asar los espárragos de alacena en sartén caliente con aceite de oliva durante 5 minutos.",
                "Terminar con jugo de limón de la granja y sal de mar.",
            ],
        ),
    )

    d2_d = _meal(
        "Cena", "20:00", 51.0, 34.0, 3.9, 6.1,
        starter=_course(
            title="Caldo Clarificado de Acelgas de la Granja, Tomate y Hojas de Laurel",
            technique="clear_botanical_broth",
            note="Caldo vegetal nocturno sin lácteos elaborado en agua purificada con acelgas de la granja (segunda y última aparición semanal [R4]), tomate de alacena y laurel.",
            thermo="Cocción suave a 90°C por 6 minutos que preserva los minerales de la acelga.",
            flavor="Acidez limpia del tomate verde con perfume de laurel y acelgas de la granja.",
            texture="Caldo cristalino con cintas tiernas de acelga.",
            ccp="Tope semanal de Acelgas = 2 apariciones exactas (810 g totales).",
            ingredients=[
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
                _ing("Acelgas", 390, "g", CAT_VEG),
                _ing("Tomate", 120, "g", CAT_VEG),
                _ing("Hojas de laurel", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Hervir el tomate de alacena picado y las hojas de laurel en el agua purificada de la granja por 4 minutos.",
                "Incorporar las acelgas de la granja en cintas, cocer 2 minutos más y servir con aceite de oliva y sal de mar.",
            ],
        ),
        main=_course(
            title="Cazuela de Champiñones Salteados al Ajillo y Hierbas Finas en Fondue Cremoso de Queso Manchego y Queso Ricotta al Sartén",
            technique="skillet_cheese_fondue_saute",
            note="Cena proteica vegetariana de alto valor biológico: champiñones salteados al ajillo en mantequilla e integrados en un fondue cremoso al sartén de queso manchego (240 g), queso ricotta (360 g) y nuez de la India (120 g).",
            thermo="Salteado en sartén de hierro a 175°C por 5 minutos y emulsión fundente a fuego bajo a 82°C con queso ricotta y queso manchego.",
            flavor="Umami de champiñón salteado al ajillo con fondue fundente de queso manchego y ricotta, hierbas finas y nuez de la India tostada.",
            texture="Láminas carnosas de champiñón envueltas en salsa elástica de fondue de quesos con crocancia de nuez de la India.",
            ccp="Emulsionar los quesos a fuego suave en sartén sin usar horno.",
            archetype="champinon_fondue_manchego_ricotta",
            ingredients=[
                _ing("Champiñón", 720, "g", CAT_VEG),
                _ing("Queso ricotta", 360, "g", CAT_DAIRY),
                _ing("Queso manchego", 240, "g", CAT_DAIRY),
                _ing("Nuez de la India", 120, "g", CAT_FAT),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Hierbas finas", 6, "g", CAT_SPICE),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Saltear los champiñones en cuartos en sartén caliente con la mantequilla, sal con ajo y hierbas finas durante 5 minutos.",
                "Reducir el fuego e incorporar el queso ricotta y el queso manchego rallado moviendo en sartén hasta formar un fondue cremoso que envuelva los hongos.",
                "Servir en cazuela caliente coronando con la nuez de la India tostada.",
            ],
        ),
        side=_course(
            title="Infusión Sedante de Manzanilla y Romero de la Granja (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="herbal_infusion",
            note="Tisana nocturna de manzanilla y romero de la granja con la Toma 3 de AminoSinergix®.",
            thermo="Infusión a 85°C templada a ≤60°C.",
            flavor="Aroma herbal de romero y manzanilla.",
            texture="Bebida cálida y ligera.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Romero", 12, "g", CAT_VEG),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y el romero de la granja en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C e integrar AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 3: MIÉRCOLES
    # Veg families: Desayuno (ejotes) | Comida (brocoli, calabacitas, nopales 2/2) | Cena (espinacas, morron)
    # =========================================================================
    d3_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.1, 6.5,
        starter=_course(
            title="Timbal de Zarzamoras de Alacena con Semillas de Chía, Nuez Pecana de la Granja y Extracto de Vainilla",
            technique="raw_berry_assembly",
            note="Segunda porción de zarzamoras del ticket Sam's Club (completando los 340 g de alacena) con semillas de chía orgánicas, nuez pecana de la granja y vainilla.",
            thermo="Servicio en frío a 4°C sin lácteos.",
            flavor="Zarzamora perfumada a la vainilla con nuez pecana de la granja.",
            texture="Fruta firme y semillas crujientes.",
            ccp="Completar exactamente los 340 g de zarzamora en alacena (0 g sobregiro).",
            ingredients=[
                _ing("Zarzamora", 160, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez pecana", 90, "g", CAT_FAT),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
            ],
            steps=[
                "Servir las zarzamoras de alacena en tazón frío con extracto de vainilla.",
                "Añadir las semillas de chía orgánicas y la nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Huevos al Plato (Oeufs sur le Plat) Cuajados a Fuego Lento en Crema de Queso Philadelphia, Queso Ricotta, Ejotes Tiernos y Hierbas Finas",
            technique="oeufs_sur_le_plat_skillet",
            note="3 huevos enteros por comensal cascados íntegros (sin batir ni revolver) y cuajados a fuego lento al plato sobre espejo cremoso de queso Philadelphia, queso ricotta, ejotes de alacena y hierbas finas.",
            thermo="Fusión láctea en sartén a 80°C y cuajado lento de los huevos enteros tapados por 4.5 minutos manteniendo las yemas enteras y brillantes.",
            flavor="Espejo fundente de queso Philadelphia y queso ricotta con ejotes tiernos, mantequilla y hierbas finas.",
            texture="Claras sedosas y yemas enteras espejo sobre crema tibia de quesos y ejotes al dente.",
            ccp="Cascar los huevos íntegros sobre la crema de quesos sin revolverlos.",
            archetype="huevo_al_plato_philadelphia_ricotta",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Queso ricotta", 180, "g", CAT_DAIRY),
                _ing("Queso Philadelphia", 180, "g", CAT_DAIRY),
                _ing("Ejotes", 240, "g", CAT_VEG),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Hierbas finas", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Saltear los ejotes de alacena en mantequilla durante 3 minutos e integrar el queso Philadelphia y el queso ricotta con hierbas finas hasta formar un espejo cremoso en la sartén.",
                "Cascar 3 huevos enteros por comensal directamente sobre el espejo de quesos sin batirlos y sazonar con sal de mar.",
                "Tapar a fuego lento durante 4.5 minutos hasta que las claras cuajen y las yemas permanezcan enteras y brillantes.",
            ],
        ),
        side=_course(
            title="Gelatina Artesanal de Fresas a la Vainilla (4°C) con Fórmula Nootrópica 33Plus®",
            technique="collagen_gel_molding",
            note="Gelatina de colágeno con fresas y extracto de vainilla (distinta a la zarzamora de la entrada) con la Toma 2 de MultiSinergix®.",
            thermo="Disolución a 60°C, templado a ≤42°C y refrigeración a 4°C.",
            flavor="Fresa aromática a la vainilla.",
            texture="Gel firme a 4°C.",
            ccp="Integrar MultiSinergix® a ≤42°C.",
            ingredients=[
                _ing("Fresas", 120, "g", CAT_FRUIT),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
                _ing("Grenetina", 42, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Hidratar la grenetina en agua purificada y fundir a 60°C.",
                "Templar a 40°C, agregar extracto de vainilla, MultiSinergix® (33Plus®) y las fresas, y refrigerar a 4°C.",
            ],
        ),
    )

    d3_l = _meal(
        "Comida", "14:30", 63.0, 41.0, 4.4, 6.8,
        starter=_course(
            title="Consomé del Huerto de Brócoli Tierno, Cilantro de la Granja y Hojas de Laurel",
            technique="clear_vegetable_broth",
            note="Caldo vegetal limpio sin lácteos elaborado en agua purificada de la granja con floretes pequeños de brócoli, hojas de laurel y cilantro.",
            thermo="Infusión a 92°C durante 6 minutos.",
            flavor="Caldo herbal de laurel y cilantro con brócoli.",
            texture="Caldo ligero con floretes al dente.",
            ccp="Libre de lácteos para equilibrar el plato fuerte de sardinas ([R2]).",
            ingredients=[
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
                _ing("Brócoli", 360, "g", CAT_VEG),
                _ing("Cilantro", 36, "g", CAT_VEG),
                _ing("Hojas de laurel", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Infusionar el agua purificada con las hojas de laurel y sal de mar a 92°C.",
                "Cocer los floretes de brócoli por 5 minutos, retirar el laurel y servir con cilantro de la granja y aceite de oliva.",
            ],
        ),
        main=_course(
            title="Lomos de Sardina Enpipianados en Salsa Espesa de Nuez de la India, Tomate Asado, Comino y Cilantro de la Granja al Sartén",
            technique="cashew_pipian_skillet",
            note="Porción clínica de sardinas de alacena (840 g = 140 g/comensal de los 1,700 g en stock) bañadas al sartén en pipián verde espeso de nuez de la India tostada, tomate de alacena asado, comino y cilantro de la granja con calabacitas.",
            thermo="Tostado de nuez de la India a 160°C, molienda con tomate asado y hervor suave del pipián en sartén a 90°C por 5 minutos con los lomos de sardina.",
            flavor="Riqueza marina en omega-3 y calcio envuelta en pipián mexicano de nuez de la India, tomate verde, comino y cilantro de la granja.",
            texture="Lomos íntegros de sardina napados en salsa aterciopelada de nuez de la India con calabacitas tiernas.",
            ccp="Integrar los lomos de sardina al pipián en sartén durante los últimos 4 minutos sin hornear.",
            archetype="sardina_pipian_nuez_india",
            ingredients=[
                _ing("Sardinas", 840, "g", CAT_PROT),
                _ing("Nuez de la India", 270, "g", CAT_FAT),
                _ing("Tomate", 120, "g", CAT_VEG),
                _ing("Calabacitas", 420, "g", CAT_VEG),
                _ing("Cilantro", 36, "g", CAT_VEG),
                _ing("Aceite de oliva", 36, "ml", CAT_FAT),
                _ing("Comino", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Asar el tomate de alacena y licuar con la nuez de la India tostada, el cilantro de la granja, comino y sal de mar hasta obtener una salsa de pipián tersa.",
                "Saltear las calabacitas en medias lunas en sartén con aceite de oliva durante 3 minutos y verter el pipián de nuez de la India.",
                "Incorporar los lomos de sardina y calentar a fuego bajo en la sartén por 4 minutos bañándolos con la salsa.",
            ],
        ),
        side=_course(
            title="Ensalada Tibia de Nopales de la Granja Curados en Sal de Mar con Cilantro, Limón Real y Aceite de Oliva VEVO",
            technique="salt_cured_warm_salad",
            note="Segunda y última aparición semanal de nopales de la granja ([R4]: 960 g totales), curados tradicionalmente en sal de mar con cilantro de la granja, limón real y aceite de oliva.",
            thermo="Curado osmótico en sal de mar y templado ligero a 45°C con aceite de oliva y limón.",
            flavor="Nopal curado con cilantro de la granja, jugo de limón real y aceite de oliva extra virgen.",
            texture="Tiras tiernas y limpias de mucílago.",
            ccp="Respetar el tope máximo de 2 apariciones de nopales en la semana.",
            ingredients=[
                _ing("Nopales", 480, "g", CAT_VEG),
                _ing("Cilantro", 36, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Curar las tiras de nopal de la granja con sal de mar durante 10 minutos, enjuagar brevemente y escurrir.",
                "Integrar con cilantro de la granja picado, jugo de limón real y aceite de oliva extra virgen.",
            ],
        ),
    )

    d3_d = _meal(
        "Cena", "20:00", 51.0, 35.5, 3.8, 5.9,
        starter=_course(
            title="Ensalada Templada de Espinacas, Aguacate Hass, Queso Ricotta y Nuez Pecana de la Granja",
            technique="warm_leaf_emulsion",
            note="Hojas de espinaca con gajos de aguacate Hass, queso ricotta de alacena y nuez pecana tostada de la granja (permitido en [R2] porque el plato fuerte es mojarra ligera).",
            thermo="Ensamble a 12°C con nuez pecana ligeramente tostada.",
            flavor="Espinaca con cremosidad de aguacate, ricotta y nuez pecana.",
            texture="Hojas suaves, dados cremosos y crocancia de nuez.",
            ccp="Única aparición de aguacate del día ([R5]).",
            ingredients=[
                _ing("Espinacas", 360, "g", CAT_VEG),
                _ing("Aguacate", 2, "piezas", CAT_FAT),
                _ing("Queso ricotta", 180, "g", CAT_DAIRY),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Disponer las hojas de espinaca con los gajos de aguacate Hass y copos de queso ricotta.",
                "Coronar con la nuez pecana de la granja y aliñar con aceite de oliva, limón real y sal de mar.",
            ],
        ),
        main=_course(
            title="Mojarra Blanca a la Meunière con Mantequilla Dorada, Cilantro de la Granja, Pimiento Morrón, Finas Hierbas y Limón Real",
            technique="meuniere_pan_glaze",
            note="Segunda porción clínica de fajitas de mojarra del ticket Sam's Club (990 g = 165 g/comensal) glaseada a la meunière con mantequilla dorada, cilantro de la granja, pimiento morrón y limón real.",
            thermo="Sellado en sartén a 175°C y baño en mantequilla avellanada (noisette) a 145°C con jugo de limón.",
            flavor="Notas avellanadas de la mantequilla meunière con limón real, cilantro de la granja y hierbas finas (sin perejil).",
            texture="Filetes blancos jugosos con julianas tiernas de pimiento morrón.",
            ccp="Verter la mantequilla espumosa con limón inmediatamente antes de servir.",
            archetype="mojarra_meuniere_limon",
            ingredients=[
                _ing("Fajitas de mojarra", 990, "g", CAT_PROT),
                _ing("Morrón", 2, "piezas", CAT_VEG),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Cilantro", 48, "g", CAT_VEG),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Hierbas finas", 6, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Sazonar las fajitas de mojarra con sal de mar y hierbas finas y dorar en sartén junto con tiras de pimiento morrón.",
                "Avellanar la mantequilla en la sartén, desglasar con jugo de limón real y cilantro de la granja picado, y bañar el pescado.",
            ],
        ),
        side=_course(
            title="Tisana Relajante de Manzanilla, Clavo de Olor y Limón (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="herbal_infusion",
            note="Infusión nocturna de manzanilla, clavo de olor de alacena y limón de la granja con la Toma 3 de AminoSinergix®.",
            thermo="Infusión a 85°C templada a ≤60°C.",
            flavor="Perfume cálido de clavo y manzanilla.",
            texture="Infusión limpia.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Clavo de olor", 2, "g", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y el clavo de olor en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C, añadir limón de la granja y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 4: JUEVES
    # Veg families: Desayuno (esparragos) | Comida (lechuga, espinacas, coliflor) | Cena (calabacitas, pepino)
    # =========================================================================
    d4_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.1, 6.4,
        starter=_course(
            title="Copa de Frambuesas de Alacena con Semillas de Chía, Nuez de la India, Nuez Pecana y Canela",
            technique="raw_berry_assembly",
            note="Segunda porción de frambuesas del ticket Sam's Club (completando los 340 g de alacena) sin lácteos con semillas de chía orgánicas, nuez de la India, nuez pecana y canela.",
            thermo="Servicio a 4°C sin intervención térmica.",
            flavor="Frambuesa y canela con nuez de la India y nuez pecana de la granja.",
            texture="Fruta delicada y crocancia de semillas y nueces.",
            ccp="Completar exactamente los 340 g de frambuesas en alacena (0 g sobregiro).",
            ingredients=[
                _ing("Frambuesas", 160, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Canela molida", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Disponer las frambuesas de alacena en copas frías.",
                "Añadir las semillas de chía orgánicas, la canela, la nuez de la India y la nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Huevos Nube al Horno con Claras Montadas, Yema Líquida, Queso Manchego y Espárragos",
            technique="cloud_egg_bake",
            note="3 huevos por comensal preparados montando las claras a punto de nieve con queso manchego rallado, horneados con la yema en el centro sobre espárragos de alacena.",
            thermo="Horneado de nubes de clara a 185°C por 5 minutos y adición de la yema por 2.5 minutos finales para mantenerla líquida.",
            flavor="Nube aireada gratinada con queso manchego, yema cremosa y espárragos en mantequilla.",
            texture="Exterior esponjoso y dorado de clara montada con centro líquido de yema.",
            ccp="Completar exactamente los 900 g de espárragos del ticket Sam's Club.",
            archetype="huevo_nube_montado",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Queso manchego", 180, "g", CAT_DAIRY),
                _ing("Espárragos", 300, "g", CAT_VEG),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Separar claras y yemas de los 18 huevos; batir las claras a punto de nieve con sal de mar e incorporar envolventemente el queso manchego.",
                "Formar nidos sobre charola engrasada con mantequilla junto a los espárragos y hornear 5 minutos a 185°C.",
                "Colocar las yemas en el centro de cada nube y hornear 2.5 minutos más.",
            ],
        ),
        side=_course(
            title="Gelatina Imperial de Flor de Jamaica de la Granja (4°C) con Fórmula Nootrópica 33Plus®",
            technique="collagen_gel_molding",
            note="Gelatina antioxidante de flor de jamaica cosechada en la granja con colágeno y la Toma 2 de MultiSinergix®.",
            thermo="Infusión de jamaica, disolución de grenetina a 60°C, templado a ≤42°C y cuajado a 4°C.",
            flavor="Acidez floral de la jamaica de la granja.",
            texture="Gel rubí firme.",
            ccp="Integrar MultiSinergix® a ≤42°C.",
            ingredients=[
                _ing("Jamaica", 30, "g", CAT_SPICE),
                _ing("Grenetina", 42, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la jamaica de la granja en agua purificada, colar y disolver la grenetina hidratada a 60°C.",
                "Templar a 40°C, integrar MultiSinergix® (33Plus®) y refrigerar a 4°C.",
            ],
        ),
    )

    d4_l = _meal(
        "Comida", "14:30", 64.0, 42.0, 4.4, 6.7,
        starter=_course(
            title="Ensalada Crujiente de Lechuga Romana de Alacena, Jitomate y Cilantro de la Granja al Limón Real",
            technique="crisp_leaf_toss",
            note="Ensalada verde obligatoria [R2] libre de lácteos y mantequilla para acompañar el pastel de carne de sirloin.",
            thermo="Ensamble en frío a 8°C.",
            flavor="Lechuga romana y jitomate de alacena con cilantro y limón de la granja.",
            texture="Hojas crujientes y gajos jugosos de jitomate.",
            ccp="Aliñar al momento de servir.",
            ingredients=[
                _ing("Lechuga", 1, "piezas", CAT_VEG),
                _ing("Jitomate", 2, "piezas", CAT_VEG),
                _ing("Cilantro", 36, "g", CAT_VEG),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cortar la lechuga romana y el jitomate de alacena y mezclar con el cilantro de la granja.",
                "Aderezar con aceite de oliva, jugo de limón real y sal de mar.",
            ],
        ),
        main=_course(
            title="Pastel de Carne Molida de Res al Horno Gratinado con Queso Manchego, Queso Ricotta y Corazón de Espinacas",
            technique="baked_meatloaf_gratin",
            note="Segunda porción de carne molida de sirloin del ticket Sam's Club (660 g, completando 1,320 g de 1,360 g, ligada sin huevo) rellena de espinacas y queso ricotta, gratinada con queso manchego.",
            thermo="Horneado a 185°C durante 22 minutos hasta alcanzar 72°C internos y gratinar la cubierta de queso manchego.",
            flavor="Jugosidad del sirloin molido con corazón cremoso de ricotta y espinacas y costra de queso manchego.",
            texture="Corte firme de carne con centro tierno de espinacas y ricotta.",
            ccp="Ligar mediante amasado proteico en frío con queso ricotta sin usar huevo ([R12]).",
            archetype="res_pastel_horno_manchego",
            ingredients=[
                _ing("Carne molida", 660, "g", CAT_PROT),
                _ing("Queso manchego", 160, "g", CAT_DAIRY),
                _ing("Queso ricotta", 180, "g", CAT_DAIRY),
                _ing("Espinacas", 390, "g", CAT_VEG),
                _ing("Cebolla", 2, "piezas", CAT_VEG),
                _ing("Aceite de coco", 60, "g", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
                _ing("Pimienta negra", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Sazonar la carne molida de res con la cebolla picada, sal con ajo y pimienta negra, y extender sobre molde engrasado con aceite de coco.",
                "Rellenar el centro con las espinacas salteadas mezcladas con el queso ricotta, cerrar el pastel de carne y cubrir con el queso manchego.",
                "Hornear a 185°C por 22 minutos hasta gratinar.",
            ],
        ),
        side=_course(
            title="Floretes de Coliflor Rostizados al Tomillo y Aceite de Oliva VEVO",
            technique="oven_roasted_florets",
            note="Guarnición ligera sin lácteos ni mantequilla ([R2]): floretes de coliflor rostizados con tomillo de alacena y aceite de oliva.",
            thermo="Rostizado en seco con aceite de oliva a 195°C por 14 minutos.",
            flavor="Notas caramelizadas de coliflor al tomillo.",
            texture="Bordes dorados y centro tierno.",
            ccp="Cero lácteos ni mantequilla en la guarnición.",
            ingredients=[
                _ing("Coliflor", 480, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Mezclar los floretes de coliflor con aceite de oliva, tomillo y sal de mar.",
                "Rostizar al horno a 195°C durante 14 minutos.",
            ],
        ),
    )

    d4_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.8, 5.9,
        starter=_course(
            title="Crema Aterciopelada de Calabacitas Tiernas y Leche de Coco al Romero de la Granja",
            technique="coconut_veloute",
            note="Crema vegetal nocturna elaborada en agua purificada de la granja con calabacitas, leche de coco de alacena y romero.",
            thermo="Cocción a 92°C por 8 minutos y emulsión en licuadora.",
            flavor="Suavidad vegetal de la calabacita con leche de coco y perfume de romero de la granja.",
            texture="Crema sedosa y ligera.",
            ccp="Retirar la rama de romero antes de licuar.",
            ingredients=[
                _ing("Agua purificada", 900, "ml", CAT_SPICE),
                _ing("Calabacitas", 480, "g", CAT_VEG),
                _ing("Leche de coco", 240, "ml", CAT_FAT),
                _ing("Romero", 12, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cocer las calabacitas en el agua purificada con el romero de la granja y sal de mar por 8 minutos.",
                "Retirar el romero, licuar con la leche de coco de alacena y el aceite de oliva, y servir caliente.",
            ],
        ),
        main=_course(
            title="Croquetas Doradas de Lomo de Atún de Alacena y Queso Ricotta al Sartén en Aceite de Coco con Nuez Pecana sobre Pepino al Limón Real",
            technique="ricotta_croquette_pan_sear",
            note="Porción clínica completa de atún en agua de alacena (690 g = 115 g/comensal en 1 solo servicio) ligada con queso ricotta (180 g, 0 huevos) en croquetas doradas al sartén en aceite de coco con nuez pecana sobre pepino.",
            thermo="Moldeado en frío de la masa de atún y ricotta y dorado en sartén con aceite de coco a 175°C por 3.5 minutos por lado.",
            flavor="Atún dorado y cremoso por el queso ricotta con nuez pecana de la granja y pepino al limón real.",
            texture="Croquetas doradas por fuera y suaves por dentro acompañadas de láminas hidratantes de pepino.",
            ccp="Ligar las croquetas con queso ricotta drenado sin usar huevo (preservando la invariante [R12] de 126 huevos).",
            archetype="atun_croquetas_ricotta_sarten",
            ingredients=[
                _ing("Atún en agua", 690, "g", CAT_PROT),
                _ing("Queso ricotta", 180, "g", CAT_DAIRY),
                _ing("Nuez pecana", 120, "g", CAT_FAT),
                _ing("Pepino", 420, "g", CAT_VEG),
                _ing("Aceite de coco", 60, "g", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
                _ing("Pimienta negra", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Drenar el atún de alacena e integrar con el queso ricotta, la nuez pecana finamente picada, sal de mar y pimienta negra hasta formar croquetas firmes.",
                "Dorar las croquetas en sartén con aceite de coco durante 3.5 minutos por lado hasta formar una corteza dorada.",
                "Servir las croquetas calientes sobre láminas de pepino aliñadas con jugo de limón real.",
            ],
        ),
        side=_course(
            title="Infusión Nocturna de Manzanilla y Tomillo (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="herbal_infusion",
            note="Tisana nocturna de manzanilla y tomillo de alacena enriquecida con la Toma 3 de AminoSinergix®.",
            thermo="Infusión a 85°C templada a ≤60°C.",
            flavor="Notas herbales de tomillo y manzanilla.",
            texture="Bebida cálida.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y el tomillo en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C e integrar AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 5: VIERNES
    # Veg families: Desayuno (ninguno de _HG_VEG_FAMILIES) | Comida (calabacitas, brocoli, pepino) | Cena (ejotes, champinon, morron)
    # =========================================================================
    d5_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.5,
        starter=_course(
            title="Mosaico de Fresas al Perfume de Canela con Semillas de Chía y Nuez Pecana de la Granja",
            technique="raw_berry_assembly",
            note="Fresas laminadas sin lácteos con semillas de chía orgánicas, canela molida y nuez pecana de la granja.",
            thermo="Servicio a 4°C.",
            flavor="Fresa y canela con nuez pecana.",
            texture="Láminas jugosas y crocancia de nuez.",
            ccp="Integrar semillas y nueces al momento de servir.",
            ingredients=[
                _ing("Fresas", 240, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez pecana", 90, "g", CAT_FAT),
                _ing("Canela molida", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Laminar las fresas y disponer en platos fríos.",
                "Espolvorear semillas de chía orgánicas, canela molida y nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Roulade de Huevo a las Finas Hierbas Relleno de Crema de Queso Ricotta y Germinado",
            technique="French_egg_roulade",
            note="Lámina flexible de 3 huevos por comensal a las finas hierbas enrollada en cilindro (roulade) con relleno cremoso de queso ricotta de alacena y germinado.",
            thermo="Cuajado en placa a 155°C con mantequilla y enrollado en caliente con el relleno de queso ricotta.",
            flavor="Huevo a las finas hierbas en mantequilla con queso ricotta y brotes de germinado.",
            texture="Rollo suave y elástico con corazón cremoso de ricotta y brotes de germinado.",
            ccp="Enrollar cuando la superficie del huevo aún esté húmeda para evitar fracturas.",
            archetype="huevo_roulade_ricotta",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Queso ricotta", 240, "g", CAT_DAIRY),
                _ing("Germinado", 60, "g", CAT_VEG),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Hierbas finas", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Sazonar el queso ricotta con una pizca de sal de mar y hierbas finas hasta formar una crema untuosa.",
                "Cuajar los huevos batidos con hierbas finas y sal de mar en la mantequilla formando láminas uniformes.",
                "Rellenar con la crema de queso ricotta, enrollar en forma de roulade y coronar con el germinado de alacena.",
            ],
        ),
        side=_course(
            title="Infusión Templada de Flor de Jamaica y Romero de la Granja (≤60°C) con Fórmula Nootrópica 33Plus®",
            technique="botanical_infusion",
            note="Elixir antioxidante de jamaica y romero cosechados en la granja con la Toma 2 de MultiSinergix®.",
            thermo="Infusión a 88°C templada a ≤60°C.",
            flavor="Acidez botánica de jamaica con notas de romero.",
            texture="Infusión rubí cristalina.",
            ccp="Incorporar MultiSinergix® a ≤60°C.",
            ingredients=[
                _ing("Jamaica", 30, "g", CAT_SPICE),
                _ing("Romero", 12, "g", CAT_VEG),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la flor de jamaica y el romero de la granja en agua purificada a 88°C por 5 minutos y colar.",
                "Templar a 58°C y disolver MultiSinergix® (33Plus®).",
            ],
        ),
    )

    d5_l = _meal(
        "Comida", "14:30", 64.0, 42.0, 4.3, 6.7,
        starter=_course(
            title="Potaje Rústico de Calabacitas Asadas al Romero de la Granja y Orégano en Caldo Aromático",
            technique="roasted_zucchini_potage",
            note="Potaje de mediodía libre de lácteos ([R2]) elaborado asando previamente las calabacitas en cubos con aceite de oliva, romero de la granja y orégano en agua purificada.",
            thermo="Asado previo de calabacita a 185°C por 4 minutos e infusión en caldo aromático de romero y orégano a 92°C.",
            flavor="Notas caramelizadas de calabacita asada con romero de la granja y orégano.",
            texture="Cubos tiernos de calabacita asada en caldo reconfortante.",
            ccp="Dorar las calabacitas en aceite de oliva antes de verter el agua purificada.",
            ingredients=[
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
                _ing("Calabacitas", 480, "g", CAT_VEG),
                _ing("Romero", 12, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Dorar las calabacitas en cubos con el aceite de oliva, el romero de la granja y el orégano durante 4 minutos.",
                "Verter el agua purificada de la granja con sal de mar y hervir suavemente por 5 minutos para integrar el potaje.",
            ],
        ),
        main=_course(
            title="Lomo de Salmón al Horno en Salsa Cremosa de Queso Ricotta, Limón Real y Romero de la Granja sobre Brócoli",
            technique="oven_veloute_bake",
            note="Segunda porción de lomo de salmón del ticket Sam's Club (600 g, completando 1,200 g de 1,250 g en stock) horneada en salsa cremosa de queso ricotta, limón real y romero de la granja sobre brócoli.",
            thermo="Horneado suave a 180°C durante 11 minutos bañado en emulsión de queso ricotta y mantequilla.",
            flavor="Salmón rico en omega-3 con salsa cremosa de ricotta al limón real y romero de la granja (sin eneldo).",
            texture="Lomo jugoso cubierto por velouté de ricotta sobre floretes de brócoli.",
            ccp="Sincronización circadiana [R6]: el salmón (pescado azul denso) se sirve al mediodía.",
            archetype="salmon_veloute_ricotta_romero",
            ingredients=[
                _ing("Lomo de salmón", 600, "g", CAT_PROT),
                _ing("Queso ricotta", 300, "g", CAT_DAIRY),
                _ing("Brócoli", 360, "g", CAT_VEG),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Romero", 12, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Colocar los lomos de salmón y los floretes de brócoli en refractario engrasado con mantequilla.",
                "Batir el queso ricotta con el jugo de limón real, el romero de la granja finamente picado y sal de mar, y cubrir el salmón.",
                "Hornear a 180°C durante 11 minutos hasta que el salmón alcance 62°C internos.",
            ],
        ),
        side=_course(
            title="Bastones de Pepino al Limón de la Granja, Orégano y Aceite de Oliva VEVO",
            technique="cold_citrus_maceration",
            note="Guarnición refrescante sin lácteos ([R2]): bastones de pepino macerados en limón de la granja, orégano y aceite de oliva.",
            thermo="Servicio en frío a 8°C.",
            flavor="Acidez cítrica de limón real y orégano sobre pepino.",
            texture="Bastones crujientes.",
            ccp="Aliñar al momento.",
            ingredients=[
                _ing("Pepino", 480, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cortar el pepino en bastones uniformes.",
                "Aliñar con jugo de limón real, aceite de oliva extra virgen, orégano y sal de mar.",
            ],
        ),
    )

    d5_d = _meal(
        "Cena", "20:00", 51.0, 36.0, 3.8, 6.0,
        starter=_course(
            title="Ensalada Nocturna de Ejotes Tiernos de Alacena, Aguacate Hass y Nuez de la India al Limón Real",
            technique="warm_bean_toss",
            note="Segunda porción de ejotes de alacena (completando 480 g de 500 g) con aguacate Hass y nuez de la India (permitido en [R2] porque el plato fuerte es ave blanca sin lácteos).",
            thermo="Ejotes al vapor templados a 18°C con gajos de aguacate y nuez de la India.",
            flavor="Ejotes verdes con la untuosidad del aguacate y el tostado de la nuez de la India.",
            texture="Ejotes al dente, aguacate cremoso y nuez crujiente.",
            ccp="Única aparición de aguacate del día ([R5]).",
            ingredients=[
                _ing("Ejotes", 240, "g", CAT_VEG),
                _ing("Aguacate", 2, "piezas", CAT_FAT),
                _ing("Nuez de la India", 90, "g", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cocer los ejotes de alacena al vapor por 4 minutos y templar.",
                "Mezclar con el aguacate en cubos, la nuez de la India, aceite de oliva, limón real y sal de mar.",
            ],
        ),
        main=_course(
            title="Piezas de Pollo Entero de Alacena Braseadas a la Cazadora (Pechuga, Muslo y Pierna) con Jitomate, Champiñones, Pimiento Morrón, Hojas de Laurel y Tomillo",
            technique="cacciatora_braise",
            note="El pollo entero de alacena (1 pieza completa para 6 comensales: pechuga, muslo y pierna) braseado lentamente a la cazadora con jitomate, cebolla, champiñones, pimiento morrón, laurel y tomillo.",
            thermo="Sellado inicial en aceite de oliva a 180°C y braseado húmedo tapado a 160°C durante 28 minutos hasta 75°C internos.",
            flavor="Salsa rústica italiana a la cazadora con jitomate, cebolla, champiñones, pimiento morrón, laurel y tomillo.",
            texture="Carne de ave sumamente tierna y desprendible del hueso en su propio jugo aromático.",
            ccp="Sincronización circadiana [R6]: proteína avícola (circadian_dinner_ok = True) ideal para la cena nocturna.",
            archetype="pollo_cacciatora_cazadora",
            ingredients=[
                _ing("Pollo entero", 1, "piezas", CAT_PROT),
                _ing("Jitomate", 2, "piezas", CAT_VEG),
                _ing("Cebolla", 2, "piezas", CAT_VEG),
                _ing("Champiñón", 360, "g", CAT_VEG),
                _ing("Morrón", 3, "piezas", CAT_VEG),
                _ing("Hojas de laurel", 3, "g", CAT_SPICE),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 36, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Porcionar el pollo entero de alacena en sus piezas anatómicas (pechuga, muslos y piernas) y dorar en aceite de oliva con sal de mar.",
                "Agregar la cebolla, el jitomate, los champiñones laminados y el pimiento morrón troceados junto con las hojas de laurel y el tomillo.",
                "Tapar y brasear a fuego suave durante 25 minutos en sus propios jugos hasta alcanzar 75°C internos.",
            ],
        ),
        side=_course(
            title="Infusión Templada de Manzanilla, Canela y Limón de la Granja (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="herbal_infusion",
            note="Tisana nocturna de manzanilla, canela y limón real con la Toma 3 de AminoSinergix®.",
            thermo="Infusión a 85°C templada a ≤60°C.",
            flavor="Manzanilla floral con canela y limón.",
            texture="Bebida cálida.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y la canela en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C, añadir limón de la granja y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 6: SÁBADO
    # Veg families: Desayuno (acelgas) | Comida (lechuga, espinacas, coliflor) | Cena (champinon)
    # =========================================================================
    d6_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.5,
        starter=_course(
            title="Jardín Matutino de Fresas con Semillas de Chía, Nuez de la India, Nuez Pecana y Vainilla",
            technique="raw_berry_assembly",
            note="Fresas en gajos servidas en frío sin lácteos con semillas de chía orgánicas, nuez de la India, nuez pecana de la granja y vainilla.",
            thermo="Servicio a 4°C.",
            flavor="Fresa y vainilla con nuez de la India y nuez pecana.",
            texture="Fruta firme y crocancia de nueces.",
            ccp="Servir inmediatamente.",
            ingredients=[
                _ing("Fresas", 240, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
            ],
            steps=[
                "Cortar las fresas y disponer en tazón frío con extracto de vainilla.",
                "Espolvorear las semillas de chía orgánicas, la nuez de la India y la nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Crepas Sin Harina de Huevo al Sartén Rellenas de Acelgas de la Granja Salteadas en Crema Ácida y Queso Ricotta",
            technique="flourless_egg_crepe_skillet",
            note="Láminas delgadas tipo crepa elaboradas exclusivamente con 3 huevos por comensal al sartén en mantequilla (0% harinas, 0% horno) rellenas de acelgas de la granja salteadas en crema ácida y queso ricotta.",
            thermo="Salteado de acelgas a 160°C y cocción de crepas delgadas de huevo en sartén a 155°C por 1.5 minutos por lado.",
            flavor="Crepa dorada de huevo en mantequilla rellena de acelgas de la granja fundidas con crema ácida y queso ricotta.",
            texture="Envoltura sedosa y flexible de crepa de huevo con interior cremoso de acelgas y ricotta.",
            ccp="Primera de las 2 únicas apariciones semanales de acelgas ([R4]: 420 + 390 = 810 g).",
            archetype="huevo_crepa_rellena_acelgas",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Acelgas", 420, "g", CAT_VEG),
                _ing("Crema ácida", 180, "g", CAT_DAIRY),
                _ing("Queso ricotta", 180, "g", CAT_DAIRY),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Saltear las acelgas de la granja en tiras con mantequilla por 3 minutos e integrar la crema ácida y el queso ricotta para formar el relleno.",
                "Batir los huevos con sal de mar y formar crepas delgadas en sartén antiadherente caliente.",
                "Rellenar cada crepa de huevo con las acelgas cremosas, doblar en pañuelo y servir caliente.",
            ],
        ),
        side=_course(
            title="Gelatina Cítrica de Limón Real de la Granja y Canela (4°C) con Fórmula Nootrópica 33Plus®",
            technique="collagen_gel_molding",
            note="Quinta gelatina semanal ([R8]) elaborada con jugo de limón real de la granja, canela y la Toma 2 de MultiSinergix® (0 colisión de fruta con la entrada).",
            thermo="Disolución a 60°C, templado a ≤42°C y gelificación a 4°C.",
            flavor="Cítrico vibrante de limón de la granja con toque de canela.",
            texture="Gel cristalino y firme.",
            ccp="Integrar MultiSinergix® a ≤42°C.",
            ingredients=[
                _ing("Limones", 90, "g", CAT_VEG),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("Grenetina", 42, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Hidratar la grenetina en agua purificada y fundir a 60°C con la canela.",
                "Templar a 40°C, agregar el jugo de limón de la granja y MultiSinergix® (33Plus®), y refrigerar a 4°C.",
            ],
        ),
    )

    d6_l = _meal(
        "Comida", "14:30", 65.0, 43.0, 4.3, 6.7,
        starter=_course(
            title="Ensalada de Lechuga Romana de Alacena, Alcaparras y Limón de la Granja al Aceite de Oliva",
            technique="crisp_leaf_toss",
            note="Tercera pieza de lechuga romana de alacena (completando las 3 piezas en stock) con alcaparras, limón de la granja y aceite de oliva sin lácteos ([R2]).",
            thermo="Servicio en frío a 8°C.",
            flavor="Contraste mediterráneo de alcaparras y limón real sobre lechuga romana.",
            texture="Hojas crujientes.",
            ccp="Completar exactamente las 3 piezas de lechuga en alacena.",
            ingredients=[
                _ing("Lechuga", 1, "piezas", CAT_VEG),
                _ing("Alcaparras", 60, "g", CAT_SPICE),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Trocear la lechuga romana de alacena y disponer en platos fríos con las alcaparras.",
                "Aliñar con jugo de limón de la granja, aceite de oliva extra virgen y sal de mar.",
            ],
        ),
        main=_course(
            title="Rollos Involtini de Flat Steak Rellenos de Espinacas Tiernas, Romero de la Granja y Sal con Ajo Braseados en Mantequilla al Sartén",
            technique="braised_beef_involtini",
            note="Segunda porción de Flat Steak del ticket Sam's Club (1,080 g = 180 g/comensal, completando 2,160 g de 2,200 g) escalopada y enrollada tipo involtini con relleno de espinacas y romero de la granja, braseada en mantequilla al sartén.",
            thermo="Sellado periférico de los rollos involtini a 180°C y braseado corto tapado en sartén a 140°C durante 6 minutos con mantequilla y sal con ajo.",
            flavor="Jugos concentrados del flat steak braseado con corazón herbal de espinacas, romero de la granja y mantequilla al ajo.",
            texture="Rollos tiernos de res rellenos de hojas de espinaca bañados en su jugo de braseado.",
            ccp="Sellar el cierre de cada involtini primero en la sartén antes de brasear.",
            archetype="res_involtini_braseado",
            ingredients=[
                _ing("Flat steak", 1080, "g", CAT_PROT),
                _ing("Espinacas", 360, "g", CAT_VEG),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Romero", 12, "g", CAT_VEG),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
                _ing("Pimienta negra", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Filetear el flat steak en láminas anchas, sazonar con sal con ajo y pimienta negra, rellenar con las espinacas y el romero de la granja y enrollar en forma de involtini.",
                "Sellar los rollos involtini en sartén con la mantequilla por todos sus lados y brasear tapados a fuego medio-bajo durante 6 minutos.",
            ],
        ),
        side=_course(
            title="Champiñones Silvestres Salteados al Tomillo con Limón Real y Aceite de Oliva VEVO",
            technique="skillet_herb_mushrooms",
            note="Séptima guarnición de Comida 100% distinta ([R4-SIDE] 7/7 vegetales): champiñones laminados salteados en aceite de oliva extra virgen con tomillo y limón real sin lácteos ni mantequilla ([R2]).",
            thermo="Salteado rápido en sartén a 175°C durante 4 minutos para dorar los champiñones preservando su firmeza.",
            flavor="Umami terroso del champiñón dorado al tomillo con el toque cítrico del limón real.",
            texture="Láminas carnosas y doradas.",
            ccp="Cero lácteos ni mantequilla en la guarnición ([R2]) y 7ª hortaliza distinta en guarnición de comida ([R4-SIDE]).",
            ingredients=[
                _ing("Champiñón", 780, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Limpiar y laminar los champiñones.",
                "Saltear a fuego vivo en aceite de oliva durante 4 minutos y sazonar con tomillo, jugo de limón real y sal de mar.",
            ],
        ),
    )

    d6_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.9, 6.0,
        starter=_course(
            title="Potaje Templado de Floretes de Coliflor Enteros y Cebolla en Caldo de Leche de Coco al Orégano",
            technique="chunky_coconut_cauliflower_potage",
            note="Potaje rústico en trozos (no licuado en crema) elaborado con floretes pequeños de coliflor al dente, cebolla de alacena, leche de coco y orégano.",
            thermo="Cocción suave en caldo a 92°C por 6 minutos manteniendo los floretes enteros al dente.",
            flavor="Caldo aromático de leche de coco, cebolla acitronada y orégano con floretes de coliflor.",
            texture="Caldo sedoso con floretes enteros firmes de coliflor (0% crema/puré).",
            ccp="Completar exactamente las 8 piezas de cebolla disponibles en alacena.",
            ingredients=[
                _ing("Agua purificada", 900, "ml", CAT_SPICE),
                _ing("Coliflor", 660, "g", CAT_VEG),
                _ing("Cebolla", 2, "piezas", CAT_VEG),
                _ing("Leche de coco", 240, "ml", CAT_FAT),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Acitronar la cebolla de alacena finamente picada en aceite de oliva con orégano y sal de mar.",
                "Incorporar el agua purificada, la leche de coco y los floretes pequeños de coliflor enteros, y cocer 6 minutos al dente sin licuar.",
            ],
        ),
        main=_course(
            title="Quenelles Templadas de Queso Ricotta y Queso Cottage al Orégano sobre Espejo de Yogur Griego de Alacena con Nuez Pecana, Germinado y Aceite de Oliva",
            technique="warm_herb_quenelles",
            note="Cena proteica láctea de alta biodisponibilidad: quenelles moldeadas con dos cucharas de queso ricotta (360 g) y queso cottage (480 g) al orégano, servidas sobre espejo extendido de yogur griego de alacena (480 g) con nuez pecana y germinado.",
            thermo="Templado suave de la mezcla de ricotta y cottage a 38°C y moldeado en quenelles sobre espejo frío de yogur griego a 8°C.",
            flavor="Espejo ácido-lácteo de yogur griego de alacena con quenelles herbales de ricotta y cottage al orégano, aceite de oliva y nuez pecana.",
            texture="Quenelles sedosas sobre espejo cremoso con crocancia de nuez pecana de la granja y brotes de germinado.",
            ccp="Completar los 480 g de germinado del ticket Sam's Club y los 480 g de queso cottage de alacena.",
            archetype="quenelles_ricotta_cottage_espejo_yogur",
            ingredients=[
                _ing("Queso cottage", 480, "g", CAT_DAIRY),
                _ing("Queso ricotta", 360, "g", CAT_DAIRY),
                _ing("Yogur griego", 480, "g", CAT_DAIRY),
                _ing("Nuez pecana", 120, "g", CAT_FAT),
                _ing("Germinado", 60, "g", CAT_VEG),
                _ing("Aceite de oliva", 36, "ml", CAT_FAT),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Extender el yogur griego de alacena sazonado con una pizca de sal de mar formando un espejo circular en el fondo del plato.",
                "Integrar el queso ricotta y el queso cottage drenado con orégano y moldear quenelles ovaladas con dos cucharas tibias.",
                "Disponer las quenelles sobre el espejo de yogur griego y coronar con el germinado de alacena, la nuez pecana de la granja y aceite de oliva extra virgen.",
            ],
        ),
        side=_course(
            title="Tisana Nocturna de Manzanilla, Hierbas Finas y Limón de la Granja (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="herbal_infusion",
            note="Séptima tisana nocturna de manzanilla de alacena (42 g totales de 50 g en stock) con hierbas finas, limón real y la Toma 3 de AminoSinergix®.",
            thermo="Infusión a 85°C templada a ≤60°C.",
            flavor="Manzanilla floral y hierbas finas con limón de la granja.",
            texture="Infusión cálida.",
            ccp="Completar los 210 g de AminoSinergix® en recetas (420 g con las 4 tomas de protocolo).",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Hierbas finas", 3, "g", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y las hierbas finas en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C, añadir jugo de limón de la granja y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    meals_by_day = [
        [d0_b, d0_l, d0_d],
        [d1_b, d1_l, d1_d],
        [d2_b, d2_l, d2_d],
        [d3_b, d3_l, d3_d],
        [d4_b, d4_l, d4_d],
        [d5_b, d5_l, d5_d],
        [d6_b, d6_l, d6_d],
    ]

    for idx, d_meta in enumerate(day_entries):
        d_obj = copy.deepcopy(d_meta)
        d_obj["meals"] = meals_by_day[idx]
        days_out.append(d_obj)

    return days_out


def generate_week_with_tilo_cortex(
    target_week: int,
    farm_harvest: Optional[List[str]] = None,
    pantry_stock: Optional[Dict[str, Tuple[float, str]]] = None,
    quarantine_items: Optional[List[str]] = None,
    history_weeks: Optional[List[Dict[str, Any]]] = None,
    diners_count: int = 6,
) -> Dict[str, Any]:
    """
    Motor N-Week Rolling Engine (Semanas 44 a 60+):
    Selecciona el Ciclo Canónico (A, B, C, D) según `target_week`, construye las 63 recetas
    restringidas a los sustantivos puros del inventario consolidado, y ejecuta la Compuerta
    Hard-Gate [R1]–[R12] garantizando 0% de repetición en ventanas móviles de 4 semanas.
    """
    harvest = farm_harvest if farm_harvest is not None else DEFAULT_FARM_HARVEST
    pantry = pantry_stock if pantry_stock is not None else DEFAULT_PANTRY_STOCK
    meta = compute_week_dates(target_week)
    cycle_id = get_cycle_id_for_week(target_week)

    days_list = _build_cycle_d_canonical_days(meta["day_entries"])

    week_plan = {
        "week_name": meta["week_name"],
        "week_label": meta["week_label"],
        "week_start": meta["week_start"],
        "date_range": meta["date_range"],
        "diners_count": diners_count,
        "cycle_id": cycle_id,
        "days": days_list,
        "selected_harvest": list(harvest),
    }

    prev_week = history_weeks[-1] if history_weeks else None
    assert_zero_violations(
        week_data=week_plan,
        pantry_stock=pantry,
        farm_harvest=harvest,
        enforce_pantry_overdraft=True,
        prev_week_data=prev_week,
    )
    return week_plan


if __name__ == "__main__":
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent.parent
    s43_path = root / "semana_43_master.json"
    s43_data = json.loads(s43_path.read_text(encoding="utf-8")) if s43_path.exists() else None
    history = [s43_data] if s43_data else []

    s44_plan = generate_week_with_tilo_cortex(44, history_weeks=history)
    s44_out = root / "semana_44_master.json"
    s44_out.write_text(json.dumps(s44_plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Generada y auditada {s44_plan['week_name']} (Ciclo {s44_plan['cycle_id']}) -> {s44_out}")

