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
    SEVEN_CULINARY_SCHOOLS,
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
    # DÍA 2: MARTES (HOY — Salmón en Comida ya descongelado)
    # Veg families: Desayuno (ninguno de _HG_VEG_FAMILIES) | Comida (calabacitas, brocoli, pepino) | Cena (acelgas 2/2, champinon)
    # =========================================================================
    d2_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.5,
        starter=_course(
            title="Compota Tibia de Fresas Asadas al Horno con Semillas de Chía, Nuez de la India y Nuez Pecana de la Granja",
            technique="oven_berry_compote",
            note="Fresas asadas brevemente al horno sin lácteos con semillas de chía orgánicas, nuez de la India del ticket Sam's Club y nuez pecana de la granja.",
            thermo="Horneado corto a 170°C por 6 minutos para concentrar los jugos antioxidantes de la fresa sin lácteos.",
            flavor="Fresa tibia caramelizada en sus propios jugos con el doble perfil oleaginoso de nuez de la India y nuez pecana.",
            texture="Compota rústica tibia contrastada con la crocancia de las nueces y las semillas de chía.",
            ccp="Añadir las semillas de chía y las nueces al salir del horno.",
            ingredients=[
                _ing("Fresas", 240, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
            ],
            steps=[
                "Cortar las fresas en cuartos y asar en refractario a 170°C durante 6 minutos hasta formar una compota tibia.",
                "Espolvorear las semillas de chía orgánicas y coronar con la nuez de la India y la nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Clafoutis Salado de Huevos Batidos, Queso Ricotta y Hierbas Finas con Germinado de Alfalfa",
            technique="savory_egg_clafoutis",
            note="Matriz cremosa tipo clafoutis salado de 3 huevos por comensal batidos con queso ricotta de alacena y hierbas finas, cuajada suavemente en mantequilla y coronada con germinado.",
            thermo="Cuajado lento a 155°C con mantequilla y queso ricotta integrado en la emulsión del huevo.",
            flavor="Huevo a las finas hierbas en mantequilla fundido con queso ricotta y brotes de germinado.",
            texture="Textura flan-clafoutis sedosa y elástica con corazón cremoso de ricotta y brotes de germinado.",
            ccp="Retirar del calor cuando el centro aún conserve temblor cremoso y coronar con el germinado.",
            archetype="huevo_clafoutis_ricotta",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Queso ricotta", 240, "g", CAT_DAIRY),
                _ing("Germinado", 60, "g", CAT_VEG),
                _ing("Mantequilla", 60, "g", CAT_FAT),
                _ing("Hierbas finas", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Batir los huevos con el queso ricotta, una pizca de sal de mar y las hierbas finas hasta obtener un aparato homogéneo de clafoutis salado.",
                "Verter sobre cazuela engrasada con la mantequilla y cuajar a fuego suave hasta que tome estructura sedosa.",
                "Servir caliente coronando con el germinado de alacena.",
            ],
        ),
        side=_course(
            title="Tisana Matutina de Té Chai Especiado y Canela (≤60°C) con Fórmula Nootrópica 33Plus®",
            technique="spiced_tea_infusion",
            note="Tisana termogénica matutina de té chai de alacena y canela molida enriquecida con la Toma 2 de MultiSinergix®.",
            thermo="Infusión a 90°C templada a ≤60°C antes de incorporar el complejo nootrópico.",
            flavor="Notas cálidas de cardamomo, clavo y canela del té chai.",
            texture="Tisana aromática ligera.",
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
        "Comida", "14:30", 64.0, 42.0, 4.3, 6.7,
        starter=_course(
            title="Potaje Rústico de Calabacitas Asadas al Romero de la Granja y Orégano en Caldo Aromático",
            technique="roasted_zucchini_potage",
            note="Potaje de mediodía libre de lácteos ([R2]) elaborado asando previamente las calabacitas en cubos con aceite de oliva, romero de la granja y orégano en agua purificada.",
            thermo="Asado previo de calabacita a 185°C por 4 minutos e infusión en caldo aromático de romero y orégano a 92°C.",
            flavor="Notas caramelizadas de calabacita asada con romero de la granja y orégano.",
            texture="Cubos tiernos de calabacita asada en caldo reconfortante (0% crema licuada).",
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
            note="Segunda porción de lomo de salmón del ticket Sam's Club ya descongelada (600 g, completando 1,200 g de 1,250 g en stock) horneada en salsa cremosa de queso ricotta, limón real y romero de la granja sobre brócoli.",
            thermo="Horneado suave a 180°C durante 11 minutos bañado en emulsión de queso ricotta y mantequilla.",
            flavor="Salmón rico en omega-3 con salsa cremosa de ricotta al limón real y romero de la granja (0% costra de nueces).",
            texture="Lomo jugoso cubierto por velouté de ricotta sobre floretes de brócoli.",
            ccp="Sincronización circadiana [R6]: el salmón descongelado (pescado azul denso) se sirve hoy en la comida de mediodía.",
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
            title="Carpaccio de Pepino Encurtido al Limón de la Granja, Orégano y Aceite de Oliva VEVO",
            technique="cold_citrus_carpaccio",
            note="Guarnición refrescante en láminas finas tipo carpaccio sin lácteos ([R2]): pepino macerado en limón de la granja, orégano y aceite de oliva.",
            thermo="Servicio en frío a 8°C con corte laminar.",
            flavor="Acidez cítrica de limón real y orégano sobre láminas de pepino.",
            texture="Láminas traslúcidas y crujientes.",
            ccp="Aliñar al momento de pasar a mesa.",
            ingredients=[
                _ing("Pepino", 480, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Laminar el pepino en rodajas sumamente delgadas y disponer en abanico tipo carpaccio.",
                "Encurtir brevemente con jugo de limón real, aceite de oliva extra virgen, orégano y sal de mar.",
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
    # DÍA 3: MIÉRCOLES (MAÑANA — Carne de Res ya descongelada en Comida)
    # Veg families: Desayuno (ejotes) | Comida (lechuga, pepino, esparragos) | Cena (calabacitas, morron)
    # =========================================================================
    d3_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.1, 6.5,
        starter=_course(
            title="Reducción Templada de Zarzamoras de Alacena al Sartén con Semillas de Chía, Nuez Pecana de la Granja y Extracto de Vainilla",
            technique="warm_berry_reduction",
            note="Segunda porción de zarzamoras del ticket Sam's Club (completando los 340 g de alacena) reducida suavemente al sartén sin lácteos con semillas de chía orgánicas, nuez pecana de la granja y vainilla.",
            thermo="Reducción suave en sartén a 85°C por 3 minutos para liberar los jugos de la zarzamora sin lácteos.",
            flavor="Zarzamora templada perfumada a la vainilla con nuez pecana tostada de la granja.",
            texture="Salsa espesa de zarzamora con semillas de chía y nuez pecana crujiente.",
            ccp="Completar exactamente los 340 g de zarzamora en alacena (0 g sobregiro).",
            ingredients=[
                _ing("Zarzamora", 160, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez pecana", 90, "g", CAT_FAT),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
            ],
            steps=[
                "Templar las zarzamoras de alacena en sartén a fuego bajo con el extracto de vainilla durante 3 minutos hasta formar una reducción jugosa.",
                "Servir coronando con las semillas de chía orgánicas y la nuez pecana de la granja.",
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
        "Comida", "14:30", 64.0, 41.5, 4.4, 6.7,
        starter=_course(
            title="Ensalada Griega de Lechuga Romana de Alacena, Germinado de Alfalfa y Cilantro de la Granja al Limón Real",
            technique="greek_ribbon_salad",
            note="Ensalada verde obligatoria [R2] libre de lácteos y mantequilla para acompañar la carne de res descongelada: cintas de lechuga romana de alacena (`1 pza`), germinado y cilantro al limón real.",
            thermo="Montaje en frío a 8°C libre de lácteos y mantequilla.",
            flavor="Clorofila viva de lechuga y cilantro con vinagreta cítrica de limón real y aceite de oliva.",
            texture="Cintas crujientes de lechuga y brotes de germinado.",
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
                "Cortar la lechuga romana de alacena en cintas finas y mezclar con el germinado y el cilantro de la granja.",
                "Aderezar con jugo de limón real, aceite de oliva extra virgen y sal de mar.",
            ],
        ),
        main=_course(
            title="Kefta Árabe de Carne Molida de Res Estofada al Sartén con Tzatziki de Yogur Griego, Pepino y Cilantro de la Granja",
            technique="griddle_kofta_sear",
            note="Kefta especiada de carne de res del ticket Sam's Club ya descongelada (660 g, ligada por amasado miofibrilar con 0 huevos) servida con salsa tzatziki de yogur griego de alacena, pepino y cilantro de la granja.",
            thermo="Sellado en sartén con aceite de coco a 185°C por 4 minutos por lado hasta 70°C internos, servida con tzatziki de yogur griego.",
            flavor="Carne de res especiada con comino y cebolla en contraste con el tzatziki de yogur griego, pepino y cilantro.",
            texture="Keftas jugosas por dentro con emulsión cremosa de yogur griego.",
            ccp="Amasar en frío la carne de res con sal de mar para ligar sin usar huevo (manteniendo la invariante [R12] de 126 huevos).",
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
                "Amasar la carne molida de res con la cebolla finamente picada, comino y sal de mar hasta activar la miosina y formar las keftas.",
                "Cocinar las keftas en sartén caliente con aceite de coco durante 4 minutos por lado.",
                "Mezclar el yogur griego con el pepino en brunoise y el cilantro de la granja para formar el tzatziki y servir con las keftas.",
            ],
        ),
        side=_course(
            title="Puntas de Espárragos Verdes de Alacena Braseadas al Limón de la Granja y Aceite de Oliva",
            technique="braised_asparagus_tips",
            note="Puntas y tallos de espárragos verdes del ticket Sam's Club braseados en sartén con aceite de oliva y limón real, libres de lácteos y mantequilla ([R2]).",
            thermo="Braseado corto en sartén a 165°C durante 5 minutos para conservar firmeza.",
            flavor="Notas verdes de espárrago braseado con jugo de limón de la granja.",
            texture="Tallos tiernos y jugosos.",
            ccp="No añadir lácteos ni mantequilla en la guarnición.",
            ingredients=[
                _ing("Espárragos", 300, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Brasear los espárragos de alacena en sartén con aceite de oliva y unas gotas de jugo de limón durante 5 minutos.",
                "Servir sazonando con sal de mar.",
            ],
        ),
    )

    d3_d = _meal(
        "Cena", "20:00", 51.0, 35.5, 3.8, 5.9,
        starter=_course(
            title="Cazuelita Tibia de Espinacas Salteadas con Dados de Aguacate Hass, Queso Ricotta y Nuez Pecana de la Granja",
            technique="warm_spinach_skillet",
            note="Hojas de espinaca brevemente salteadas en aceite de oliva servidas en cazuelita tibia con dados de aguacate Hass, queso ricotta de alacena y nuez pecana tostada (permitido en [R2] porque el plato fuerte es mojarra ligera).",
            thermo="Salteado corto de 90 segundos a 140°C y montaje tibio con aguacate y nuez pecana.",
            flavor="Espinaca tibia con cremosidad de aguacate, ricotta y nuez pecana al limón real.",
            texture="Hojas sedosas, dados cremosos y crocancia de nuez.",
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
                "Saltear brevemente las hojas de espinaca en aceite de oliva con sal de mar y jugo de limón real.",
                "Servir en cazuelitas tibias coronando con dados de aguacate Hass, copos de queso ricotta y nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Blanquette Francesa de Fajitas de Mojarra Pochadas en Mantequilla, Cilantro de la Granja, Pimiento Morrón, Finas Hierbas y Limón Real",
            technique="blanquette_butter_poach",
            note="Segunda porción clínica de fajitas de mojarra del ticket Sam's Club (990 g = 165 g/comensal) pochada al estilo blanquette en emulsión de mantequilla, cilantro de la granja, pimiento morrón y limón real.",
            thermo="Pochado suave en emulsión de mantequilla y limón a 88°C durante 6 minutos hasta 63°C internos.",
            flavor="Emulsión sedosa de mantequilla y limón real con cilantro de la granja, pimiento morrón y hierbas finas.",
            texture="Fajitas blancas sumamente tiernas con julianas de pimiento morrón.",
            ccp="Pochar suavemente en la emulsión sin freír a fuego alto.",
            archetype="mojarra_blanquette_limon",
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
                "Fundir la mantequilla a fuego bajo con el jugo de limón real, las hierbas finas y las tiras de pimiento morrón para formar el baño de blanquette.",
                "Incorporar las fajitas de mojarra sazonadas con sal de mar y pochar tapadas durante 6 minutos, terminando con cilantro de la granja.",
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
    # Veg families: Desayuno (esparragos) | Comida (brocoli, calabacitas, nopales 2/2) | Cena (espinacas, pepino)
    # =========================================================================
    d4_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.1, 6.4,
        starter=_course(
            title="Coulis Tibio de Frambuesas de Alacena a la Canela con Semillas de Chía, Nuez de la India y Nuez Pecana",
            technique="warm_berry_coulis",
            note="Segunda porción de frambuesas del ticket Sam's Club (completando los 340 g de alacena) reducida en coulis tibio sin lácteos con semillas de chía orgánicas, nuez de la India, nuez pecana y canela.",
            thermo="Reducción breve en cazo a 80°C por 3 minutos para formar un coulis aromático de frambuesa.",
            flavor="Frambuesa tibia y canela con nuez de la India y nuez pecana de la granja.",
            texture="Coulis sedoso con crocancia de semillas y nueces.",
            ccp="Completar exactamente los 340 g de frambuesas en alacena (0 g sobregiro).",
            ingredients=[
                _ing("Frambuesas", 160, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Canela molida", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Templar las frambuesas de alacena con la canela molida en cazo a fuego suave por 3 minutos hasta formar un coulis.",
                "Servir coronando con las semillas de chía orgánicas, la nuez de la India y la nuez pecana de la granja.",
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
        "Comida", "14:30", 63.0, 41.0, 4.4, 6.8,
        starter=_course(
            title="Tiradito Templado de Floretes de Brócoli al Vapor con Emulsión de Aceite de Oliva, Hojas de Laurel y Cilantro de la Granja",
            technique="steamed_broccoli_tiradito",
            note="Entrada vegetal templada sin lácteos elaborada con floretes de brócoli cocidos al vapor en infusión de agua purificada y hojas de laurel, bañados con aceite de oliva y cilantro.",
            thermo="Cocción al vapor aromático de laurel a 95°C durante 5 minutos.",
            flavor="Brócoli tierno perfumado al laurel con cilantro de la granja y aceite de oliva extra virgen.",
            texture="Floretes firmes al dente dispuestos en tiradito.",
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
                "Aromatizar el agua purificada de la vaporera con las hojas de laurel y cocer los floretes de brócoli por 5 minutos.",
                "Disponer los floretes templados en plato extendido y emulsionar con aceite de oliva, cilantro de la granja y sal de mar.",
            ],
        ),
        main=_course(
            title="Terrina Caliente de Lomos de Sardina en Salsa Espesa de Nuez de la India, Tomate Asado, Comino y Cilantro de la Granja",
            technique="cashew_terrine_braise",
            note="Porción clínica de sardinas de alacena (840 g = 140 g/comensal de los 1,700 g en stock) dispuestas en terrina caliente con salsa espesa de nuez de la India tostada, tomate de alacena asado, comino y cilantro con calabacitas.",
            thermo="Tostado de nuez de la India a 160°C, molienda con tomate asado y cocción suave en terrina a 90°C por 5 minutos con los lomos de sardina.",
            flavor="Riqueza marina en omega-3 y calcio envuelta en salsa espesa de nuez de la India, tomate verde, comino y cilantro de la granja.",
            texture="Lomos íntegros de sardina napados en pasta aterciopelada de nuez de la India con calabacitas tiernas.",
            ccp="Integrar los lomos de sardina en la salsa de nuez de la India durante los últimos 4 minutos.",
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
                "Asar el tomate de alacena y moler con la nuez de la India tostada, el cilantro de la granja, comino y sal de mar hasta obtener una salsa espesa.",
                "Brasear las calabacitas en medias lunas con aceite de oliva durante 3 minutos y disponer en terrina con la salsa de nuez de la India.",
                "Acomodar los lomos de sardina y calentar a fuego bajo por 4 minutos bañándolos con la emulsión de nuez.",
            ],
        ),
        side=_course(
            title="Milhojas de Nopales de la Granja Curados en Sal de Mar con Cilantro, Limón Real y Aceite de Oliva VEVO",
            technique="salt_cured_cactus_millefeuille",
            note="Segunda y última aparición semanal de nopales de la granja ([R4]: 960 g totales), curados tradicionalmente en sal de mar y montados en capas tipo milhojas con cilantro, limón real y aceite de oliva.",
            thermo="Curado osmótico en sal de mar y templado ligero a 45°C con aceite de oliva y limón.",
            flavor="Nopal curado con cilantro de la granja, jugo de limón real y aceite de oliva extra virgen.",
            texture="Láminas tiernas y limpias de mucílago en capas.",
            ccp="Respetar el tope máximo de 2 apariciones de nopales en la semana.",
            ingredients=[
                _ing("Nopales", 480, "g", CAT_VEG),
                _ing("Cilantro", 36, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Curar las láminas de nopal de la granja con sal de mar durante 10 minutos, enjuagar brevemente y escurrir.",
                "Montar en capas con cilantro de la granja picado, jugo de limón real y aceite de oliva extra virgen.",
            ],
        ),
    )

    d4_d = _meal(
        "Cena", "20:00", 51.0, 36.0, 3.8, 6.0,
        starter=_course(
            title="Mosaico Templado de Ejotes Tiernos de Alacena al Vapor con Dados de Aguacate Hass y Nuez de la India al Limón Real",
            technique="warm_bean_mosaic",
            note="Segunda porción de ejotes de alacena (completando 480 g de 500 g) al vapor con dados de aguacate Hass y nuez de la India (permitido en [R2] porque el plato fuerte es ave blanca sin lácteos).",
            thermo="Ejotes al vapor templados a 18°C con dados de aguacate y nuez de la India.",
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
                "Cocer los ejotes de alacena al vapor por 4 minutos y disponer en mosaico templado.",
                "Coronar con el aguacate en cubos, la nuez de la India, aceite de oliva, limón real y sal de mar.",
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
            title="Tisana Nocturna de Manzanilla y Tomillo de Alacena (≤60°C) con Fórmula Reparadora 34Plus®",
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
    # Veg families: Desayuno (acelgas) | Comida (lechuga, espinacas, coliflor) | Cena (calabacitas, pepino)
    # =========================================================================
    d5_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.3, 6.4,
        starter=_course(
            title="Fresas Glaseadas al Sartén a la Canela con Semillas de Chía y Nuez Pecana de la Granja",
            technique="skillet_berry_glaze",
            note="Fresas laminadas brevemente glaseadas en sartén sin lácteos con semillas de chía orgánicas, canela molida y nuez pecana de la granja.",
            thermo="Salteado rápido a 140°C por 2 minutos para glasear la fresa en su propio jugo con canela.",
            flavor="Fresa tibia glaseada a la canela con nuez pecana tostada.",
            texture="Láminas jugosas y crocancia de nuez.",
            ccp="Integrar semillas y nueces al retirar del fuego.",
            ingredients=[
                _ing("Fresas", 240, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez pecana", 90, "g", CAT_FAT),
                _ing("Canela molida", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Laminar las fresas y glasear brevemente en sartén con la canela molida durante 2 minutos.",
                "Servir espolvoreando las semillas de chía orgánicas y la nuez pecana de la granja.",
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
        "Comida", "14:30", 64.0, 42.0, 4.4, 6.7,
        starter=_course(
            title="Ensalada Mediterránea de Cogollos de Lechuga Romana de Alacena, Jitomate y Cilantro de la Granja al Limón Real",
            technique="mediterranean_heart_salad",
            note="Ensalada verde obligatoria [R2] libre de lácteos y mantequilla para acompañar el pastel de carne de sirloin (`1 pza` de lechuga).",
            thermo="Ensamble en frío a 8°C.",
            flavor="Cogollos de lechuga romana y jitomate de alacena con cilantro y limón de la granja.",
            texture="Cogollos crujientes y gajos jugosos de jitomate.",
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
                "Cortar los cogollos de lechuga romana y el jitomate de alacena y mezclar con el cilantro de la granja.",
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
            title="Cuscús Rústico de Coliflor Salteado al Tomillo y Aceite de Oliva VEVO",
            technique="skillet_cauliflower_couscous",
            note="Guarnición ligera sin lácteos ni mantequilla ([R2]): coliflor finamente picada tipo cuscús salteada al sartén con tomillo de alacena y aceite de oliva.",
            thermo="Salteado rápido en seco con aceite de oliva a 175°C por 5 minutos manteniendo textura al dente.",
            flavor="Notas aromáticas de coliflor al tomillo y aceite de oliva extra virgen.",
            texture="Grano vegetal suelto y dorado tipo cuscús.",
            ccp="Cero lácteos ni mantequilla en la guarnición.",
            ingredients=[
                _ing("Coliflor", 480, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Picar finamente los floretes de coliflor hasta obtener textura de cuscús rústico.",
                "Saltear en sartén con aceite de oliva, tomillo y sal de mar durante 5 minutos.",
            ],
        ),
    )

    d5_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.8, 5.9,
        starter=_course(
            title="Medallones de Calabacita Tierna Braseados en Caldo de Leche de Coco y Romero de la Granja",
            technique="braised_zucchini_medallions",
            note="Medallones enteros de calabacita braseados (0% crema licuada) en caldo de agua purificada, leche de coco de alacena y romero de la granja.",
            thermo="Braseado a 92°C por 6 minutos conservando los medallones enteros al dente.",
            flavor="Suavidad vegetal de la calabacita braseada con leche de coco y perfume de romero de la granja.",
            texture="Medallones firmes de calabacita en caldo aromático de coco.",
            ccp="Servir los medallones enteros sin licuar.",
            ingredients=[
                _ing("Agua purificada", 900, "ml", CAT_SPICE),
                _ing("Calabacitas", 480, "g", CAT_VEG),
                _ing("Leche de coco", 240, "ml", CAT_FAT),
                _ing("Romero", 12, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Dorar ligeramente los medallones gruesos de calabacita con aceite de oliva y romero de la granja.",
                "Incorporar el agua purificada, la leche de coco de alacena y sal de mar, y brasear 6 minutos manteniendo los medallones enteros.",
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
            title="Tisana Nocturna de Manzanilla, Canela y Limón de la Granja (≤60°C) con Fórmula Reparadora 34Plus®",
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
    # Veg families: Desayuno (calabacitas) | Comida (lechuga, espinacas, champinon) | Cena (coliflor)
    # =========================================================================
    d6_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.5,
        starter=_course(
            title="Macerado de Fresas en Brunoise a la Vainilla con Semillas de Chía, Nuez de la India y Nuez Pecana",
            technique="brunoise_berry_maceration",
            note="Fresas picadas en brunoise maceradas sin lácteos con extracto de vainilla, semillas de chía orgánicas, nuez de la India y nuez pecana de la granja.",
            thermo="Maceración en frío a 6°C en corte brunoise fino.",
            flavor="Fresa macerada a la vainilla con nuez de la India y nuez pecana.",
            texture="Brunoise jugoso de fresa y crocancia de nueces.",
            ccp="Servir inmediatamente tras el macerado.",
            ingredients=[
                _ing("Fresas", 240, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
            ],
            steps=[
                "Picar las fresas en brunoise y macerar brevemente con el extracto de vainilla.",
                "Espolvorear las semillas de chía orgánicas, la nuez de la India y la nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Flan Salado de Huevos al Baño María Gratinado con Queso Manchego y Calabacitas Tiernas",
            technique="bain_marie_savory_flan",
            note="Matriz sedosa tipo flan salado de 3 huevos por comensal cuajada al baño María con medias lunas de calabacita y gratinado de queso manchego de alacena.",
            thermo="Cocción suave al baño María a 165°C durante 14 minutos hasta cuajar el flan salado y fundir el queso manchego.",
            flavor="Suavidad láctea del queso manchego fundido con calabacitas en mantequilla.",
            texture="Estructura tersa de flan salado con cubierta dorada de queso manchego.",
            ccp="Cocinar en baño María para lograr una textura sedosa sin alveolos secos.",
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
                "Saltear las calabacitas en medias lunas con la mantequilla y distribuir en moldes individuales.",
                "Batir los huevos con sal de mar y pimienta negra, verter sobre las calabacitas y cubrir con el queso manchego rallado.",
                "Cuajar al baño María durante 14 minutos hasta que el flan salado esté firme y gratinado.",
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
            title="Ensalada de Corazones de Lechuga Romana de Alacena a la Plancha con Alcaparras y Limón Real al Aceite de Oliva",
            technique="grilled_romaine_hearts",
            note="Tercera pieza de lechuga romana de alacena (completando las 3 piezas en stock) sellada brevemente en mitades a la plancha con alcaparras, limón de la granja y aceite de oliva sin lácteos ([R2]).",
            thermo="Sellado rápido de los corazones de lechuga a 180°C por 45 segundos conservando el centro crujiente.",
            flavor="Contraste mediterráneo de alcaparras y limón real sobre corazones de lechuga romana.",
            texture="Bordes ligeramente asados y centro crujiente.",
            ccp="Completar exactamente las 3 piezas de lechuga en alacena.",
            ingredients=[
                _ing("Lechuga", 1, "piezas", CAT_VEG),
                _ing("Alcaparras", 60, "g", CAT_SPICE),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cortar la lechuga romana de alacena en cuartos longitudinales y sellar brevemente en plancha caliente.",
                "Aliñar con las alcaparras, jugo de limón de la granja, aceite de oliva extra virgen y sal de mar.",
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
            title="Duxelles Rústica de Champiñones Silvestres Salteados al Tomillo con Limón Real y Aceite de Oliva VEVO",
            technique="skillet_mushroom_duxelles",
            note="Séptima guarnición de Comida 100% distinta ([R4-SIDE] 7/7 vegetales): duxelles rústica de champiñones finamente picados salteados en aceite de oliva extra virgen con tomillo y limón real sin lácteos ni mantequilla ([R2]).",
            thermo="Salteado en sartén a 175°C durante 5 minutos para concentrar el umami del champiñón picado.",
            flavor="Umami terroso de la duxelles de champiñón al tomillo con el toque cítrico del limón real.",
            texture="Duxelles rústica jugosa y dorada.",
            ccp="Cero lácteos ni mantequilla en la guarnición ([R2]) y 7ª hortaliza distinta en guarnición de comida ([R4-SIDE]).",
            ingredients=[
                _ing("Champiñón", 780, "g", CAT_VEG),
                _ing("Aceite de oliva", 30, "ml", CAT_FAT),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Picar finamente los champiñones para formar una duxelles rústica.",
                "Saltear a fuego vivo en aceite de oliva durante 5 minutos y sazonar con tomillo, jugo de limón real y sal de mar.",
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


# =============================================================================
# V17.0 — CÓRTEX DEL HEPTÁGONO CULINARIO T.I.L.O.® (7 ESCUELAS DE RESTAURANTE)
# =============================================================================
def _build_heptagon_cycle_a_days(day_entries: List[Dict[str, Any]], target_week: int = 45) -> List[Dict[str, Any]]:
    """
    Construye los 7 días del Heptágono Culinario T.I.L.O.® (Rotación A: Semanas 45, 49, 53, 57...),
    asignando 1 Escuela Culinaria por día de la semana (Escuelas 1 a 7), con:
      - 126 huevos exactos (18 por desayuno, 0 en comidas y cenas).
      - 7 vegetales distintos en las 7 guarniciones de Comida ([R4-SIDE] 7/7).
      - Cero repetición de títulos, arquetipos, ADN estructural 4D ni Jaccard >= 0.60 contra S41-S44.
      - Frontera Sábado(W-1) -> Domingo(W) validada ([R9]).
    """
    days_out: List[Dict[str, Any]] = []

    # =========================================================================
    # DÍA 0: DOMINGO — 🇲🇽 ESCUELA 1: ANTOJO Y DESAYUNO MEXICANO DE AUTOR (Inspiración Nizú)
    # Veg families: Desayuno (morron) | Comida (calabacitas, ejotes) | Cena (pepino, champinon, espinacas)
    # =========================================================================
    d0_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.4,
        starter=_course(
            title="Espejo de Zarzamora Macerada al Limón Real con Semillas de Chía, Nuez de la India y Nuez Pecana",
            technique="citrus_blackberry_maceration",
            note="Entrada matutina 0% lácteos ([R4.6]) con zarzamora macerada al limón de la granja, semillas de chía orgánicas, nuez de la India y nuez pecana.",
            thermo="Maceración en frío a 6°C para preservar antocianinas.",
            flavor="Contraste ácido de zarzamora y limón real con nuez pecana y nuez de la India.",
            texture="Fruta firme con crocancia de semillas y nueces.",
            ccp="Cero lácteos en la entrada frutal ([R4.6]).",
            ingredients=[
                _ing("Zarzamora", 170, "g", CAT_FRUIT),
                _ing("Limones", 30, "g", CAT_VEG),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
            ],
            steps=[
                "Disponer la zarzamora desinfectada en copas frías y rociar con jugo de limón de la granja.",
                "Coronar con las semillas de chía orgánicas, la nuez de la India y la nuez pecana.",
            ],
        ),
        main=_course(
            title="Huevos Peyis Estrellados Bañados en Salsa Fundente de 3 Quesos (Queso Manchego, Queso Ricotta y Queso Philadelphia) con Juliana de Pimiento Morrón Asado",
            technique="peyis_three_cheese_skillet",
            note="Escuela 1 (Inspiración Nizú): 3 huevos estrellados por comensal (18 piezas) bañados en salsa fundente de queso manchego, queso ricotta y queso Philadelphia con juliana de pimiento morrón asado.",
            thermo="Fusión lenta de los 3 quesos a 78°C y fritura limpia de los huevos en mantequilla a 145°C con yema cremosa.",
            flavor="Riqueza láctea triple (manchego, ricotta y Philadelphia) con el dulzor ahumado del pimiento morrón asado.",
            texture="Yemas líquidas y claras tiernas cubiertas por emulsión aterciopelada de 3 quesos.",
            ccp="No hervir la salsa de 3 quesos para evitar separación lipídica.",
            archetype="huevo_peyis_tres_quesos",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Queso manchego", 90, "g", CAT_DAIRY),
                _ing("Queso ricotta", 180, "g", CAT_DAIRY),
                _ing("Queso Philadelphia", 120, "g", CAT_DAIRY),
                _ing("Morrón", 2, "piezas", CAT_VEG),
                _ing("Mantequilla", 48, "g", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Asar y cortar el pimiento morrón en juliana fina y saltear en mantequilla.",
                "Fundir a fuego suave el queso manchego, el queso ricotta y el queso Philadelphia hasta obtener una salsa tersa.",
                "Estrellar los 18 huevos en sartén con mantequilla, sazonar con sal de mar y bañar con la salsa caliente de 3 quesos y la juliana de morrón.",
            ],
        ),
        side=_course(
            title="Gelatina Artesanal de Flor de Jamaica y Canela (4°C) con Fórmula Nootrópica 33Plus®",
            technique="collagen_hibiscus_gel",
            note="Primera gelatina matutina semanal ([R8]) de flor de Jamaica y canela con colágeno hidrolizado y la Toma 2 de MultiSinergix®.",
            thermo="Hidratación y fusión a 60°C, templado a ≤42°C y gelificación a 4°C.",
            flavor="Notas florales de Jamaica y canela.",
            texture="Gel firme y cristalino a 4°C.",
            ccp="Incorporar MultiSinergix® a ≤42°C.",
            ingredients=[
                _ing("Flor de Jamaica molida en polvo", 24, "g", CAT_SPICE),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("Grenetina", 16, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la flor de Jamaica y la canela en agua purificada e hidratar la grenetina.",
                "Templar a 40°C, disolver MultiSinergix® (33Plus®) y refrigerar en moldes a 4°C.",
            ],
        ),
    )

    d0_l = _meal(
        "Comida", "14:30", 65.0, 43.0, 4.3, 6.8,
        starter=_course(
            title="Consomé Tatemado de Jitomate, Cebolla y Cilantro de la Granja en Fondo Claro de Pollo al Aceite de Oliva",
            technique="charred_tomato_clear_consomme",
            note="Entrada ligera y desinflamatoria sin lácteos ([R2]) que prepara el paladar para las Enchiladas Espuma de la Escuela 1.",
            thermo="Asado de jitomate y cebolla e infusión suave en fondo claro de pollo a 90°C.",
            flavor="Caldo limpio con notas tatemadas de jitomate y cilantro de la granja.",
            texture="Consomé diáfano y reconfortante.",
            ccp="Servir a 72°C libre de cremas y quesos ([R2]).",
            ingredients=[
                _ing("Fondo claro de pollo", 900, "ml", CAT_SPICE),
                _ing("Jitomate", 1, "piezas", CAT_VEG),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Cilantro", 18, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Tatemar el jitomate y la cebolla e infusionar en el fondo claro de pollo caliente por 8 minutos.",
                "Perfumar con cilantro de la granja picado, aceite de oliva extra virgen y sal de mar.",
            ],
        ),
        main=_course(
            title="Rollos Estilo Enchiladas Espuma de Pechuga de Pavo y Calabacitas Tiernas Bañados en Salsa Cremosa de Aguacate Hass, Tomate y Cilantro Gratinados con Queso Manchego",
            technique="avocado_foam_keto_enchiladas",
            note="Escuela 1 (Inspiración Nizú): sustitución cetogénica de tortilla de maíz por láminas tiernas de calabacita y pechuga de pavo enrolladas, bañadas en salsa emulsionada de aguacate Hass, tomate verde y cilantro con gratinado de queso manchego (0 huevos en comida [R12]).",
            thermo="Horneado y gratinado corto a 185°C por 6 minutos sobre la salsa aterciopelada de aguacate y tomate.",
            flavor="Cremosidad herbácea de aguacate Hass, tomate y cilantro de la granja con costra fundida de queso manchego.",
            texture="Rollos jugosos de pavo y calabacita bajo cubierta gratinada.",
            ccp="Única presencia diaria de aguacate ([R5]) y centro térmico de 74°C.",
            archetype="pavo_enchiladas_espuma_aguacate",
            ingredients=[
                _ing("Pechuga de pavo", 700, "g", CAT_PROT),
                _ing("Calabacitas", 360, "g", CAT_VEG),
                _ing("Aguacate", 1, "piezas", CAT_FAT),
                _ing("Tomate", 180, "g", CAT_VEG),
                _ing("Queso manchego", 90, "g", CAT_DAIRY),
                _ing("Cilantro", 24, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Sellar las láminas de pechuga de pavo y calabacita en aceite de oliva y formar rollos tipo enchilada.",
                "Emulsionar el tomate cocido con la pulpa de aguacate Hass, cilantro de la granja y sal de mar hasta obtener una salsa espuma.",
                "Bañar los rollos con la salsa, cubrir con queso manchego rallado y gratinar 6 minutos.",
            ],
        ),
        side=_course(
            title="Ejotes Tiernos al Vapor Salteados al Limón Real, Orégano y Aceite de Oliva VEVO",
            technique="steamed_citrus_green_beans",
            note="Primera guarnición de Comida ([R4-SIDE] 1/7: ejotes) libre de lácteos ([R2]).",
            thermo="Vapor a 96°C por 5 minutos y salteado rápido en aceite de oliva.",
            flavor="Frescura herbal de ejotes con limón real y orégano.",
            texture="Ejotes crujientes al dente.",
            ccp="Cero lácteos en la guarnición ([R2]).",
            ingredients=[
                _ing("Ejotes", 240, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cocer los ejotes al vapor durante 5 minutos manteniendo su firmeza.",
                "Aliñar con aceite de oliva extra virgen, jugo de limón de la granja, orégano y sal de mar.",
            ],
        ),
    )

    d0_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.9, 6.2,
        starter=_course(
            title="Ensalada Nocturna de Pepino en Rodajas Finas con Limón Real, Orégano y Aceite de Oliva",
            technique="crisp_cucumber_oregano_salad",
            note="Ensalada crujiente y alcalina sin lácteos ([R2]) con pepino en rodajas, limón real y orégano.",
            thermo="Emplatado en frío a 8°C.",
            flavor="Acidez limpia de limón real con notas herbales de orégano.",
            texture="Rodajas crujientes e hidratantes de pepino.",
            ccp="Laminar y aderezar al momento de servir.",
            ingredients=[
                _ing("Pepino", 360, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cortar el pepino en rodajas delgadas.",
                "Aderezar con jugo de limón real, aceite de oliva extra virgen, orégano y sal de mar.",
            ],
        ),
        main=_course(
            title="Dobladitas Keto en Costra Dorada de Queso Manchego al Comal Rellenas de Champiñones Salteados, Queso Ricotta, Queso Philadelphia, Espinacas, Nuez Pecana y Cilantro",
            technique="cheese_crust_keto_dobladitas",
            note="Escuela 1 (Inspiración Nizú): dobladitas cetogénicas formando la tortilla con costra dorada de queso manchego (240 g) al comal, rellenas de champiñones salteados, queso ricotta (300 g), queso Philadelphia (180 g), espinacas, nuez pecana de la granja y cilantro (35 g de proteína AVB láctea/vegetal por comensal).",
            thermo="Fundido y dorado de la costra de queso manchego en comal a 170°C hasta lograr pliegue flexible y crujiente sobre el relleno cremoso de ricotta y Philadelphia.",
            flavor="Umami de champiñón salteado, 3 quesos (manchego, ricotta y Philadelphia), espinacas, nuez pecana y cilantro.",
            texture="Exterior crujiente de queso dorado al comal con interior cremoso de hongos y nuez pecana.",
            ccp="Doblar la costra de queso manchego en caliente sobre el relleno proteico de 3 quesos y champiñones.",
            archetype="dobladitas_ines_champinon",
            ingredients=[
                _ing("Champiñón", 660, "g", CAT_VEG),
                _ing("Espinacas", 300, "g", CAT_VEG),
                _ing("Queso ricotta", 300, "g", CAT_DAIRY),
                _ing("Queso manchego", 240, "g", CAT_DAIRY),
                _ing("Queso Philadelphia", 180, "g", CAT_DAIRY),
                _ing("Nuez pecana", 90, "g", CAT_FAT),
                _ing("Cilantro", 24, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Saltear los champiñones fileteados y las espinacas en aceite de oliva con cilantro de la granja, orégano y sal de mar, e integrar el queso ricotta, el queso Philadelphia y la nuez pecana picada.",
                "Formar discos de queso manchego rallado sobre el comal caliente hasta dorar ligeramente, rellenar con los champiñones a los 3 quesos y doblar en media luna.",
            ],
        ),
        side=_course(
            title="Tisana Nocturna de Manzanilla y Canela (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="chamomile_cinnamon_infusion",
            note="Primera tisana nocturna libre de teína con la Toma 3 de AminoSinergix®.",
            thermo="Infusión a 85°C templada a ≤60°C.",
            flavor="Notas suaves de manzanilla y canela.",
            texture="Infusión cálida y sedante.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y la canela en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C e incorporar AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 1: LUNES — 🇺🇸 ESCUELA 2: BRUNCH & GRILL AMERICANO CLÁSICO (Inspiración IHOP)
    # Veg families: Desayuno (champinon, espinacas) | Comida (lechuga, morron, brocoli) | Cena (calabacitas)
    # =========================================================================
    d1_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.1, 6.3,
        starter=_course(
            title="Copa de Frambuesas Maceradas a la Vainilla con Semillas de Chía, Nuez de la India y Nuez Pecana",
            technique="vanilla_raspberry_maceration",
            note="Frambuesas con extracto de vainilla, semillas de chía orgánicas, nuez de la India y nuez pecana sin lácteos ([R4.6]).",
            thermo="Servicio en frío a 6°C.",
            flavor="Aroma de vainilla y frambuesa con nueces tostadas.",
            texture="Bayas enteras con semillas de chía y nuez pecana.",
            ccp="Cero lácteos en la entrada frutal.",
            ingredients=[
                _ing("Frambuesas", 125, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
            ],
            steps=[
                "Perfumar las frambuesas con extracto de vainilla en tazones individuales.",
                "Añadir las semillas de chía orgánicas, la nuez de la India y la nuez pecana de la granja.",
            ],
        ),
        main=_course(
            title="Crepas Florentinas (100% Huevo sin Harina) Rellenas de Champiñones Salteados, Espinacas y Cebolla, Cubiertas en Emulsión Holandesa de Mantequilla y Limón Real",
            technique="florentine_egg_crepe_hollandaise",
            note="Escuela 2 (Inspiración IHOP): crepas elaboradas 100% con huevo batido sin harinas, rellenas de champiñones salteados, espinacas y cebolla, bañadas en emulsión holandesa de mantequilla y limón real.",
            thermo="Cocción de láminas finas de huevo a 140°C y emulsión holandesa tibia a 58°C.",
            flavor="Clásico brunch americano florentino con acidez cítrica de holandesa en mantequilla.",
            texture="Crepa elástica y sedosa rellena de champiñones y espinacas.",
            ccp="Emulsionar la mantequilla con el limón real a baja temperatura.",
            archetype="huevo_crepa_florentina_holandesa",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Champiñón", 360, "g", CAT_VEG),
                _ing("Espinacas", 300, "g", CAT_VEG),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Mantequilla", 72, "g", CAT_FAT),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Extender porciones de huevo batido en sartén antiadherente para formar crepas finas sin harina.",
                "Saltear los champiñones, las espinacas y la cebolla picada en la mitad de la mantequilla y rellenar las crepas.",
                "Emulsionar el resto de la mantequilla tibia con jugo de limón de la granja y sal de mar, y napar las crepas florentinas.",
            ],
        ),
        side=_course(
            title="Gelatina Cítrica de Limón Real y Romero de la Granja (4°C) con Fórmula Nootrópica 33Plus®",
            technique="citrus_rosemary_collagen_gel",
            note="Segunda gelatina matutina ([R8]) con limón de la granja, romero y la Toma 2 de MultiSinergix®.",
            thermo="Gelificación a 4°C tras integrar MultiSinergix® a ≤42°C.",
            flavor="Cítrico herbal de limón real y romero.",
            texture="Gel firme a 4°C.",
            ccp="Proteger termolabilidad a ≤42°C.",
            ingredients=[
                _ing("Limones", 90, "g", CAT_VEG),
                _ing("Romero", 6, "g", CAT_VEG),
                _ing("Grenetina", 16, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar el romero en agua purificada, hidratar la grenetina y templar a 40°C.",
                "Añadir el jugo de limón real y MultiSinergix® (33Plus®), y refrigerar a 4°C.",
            ],
        ),
    )

    d1_l = _meal(
        "Comida", "14:30", 65.0, 43.0, 4.2, 6.5,
        starter=_course(
            title="Ensalada House Grill de Lechuga Romana con Jitomate, Alcaparras, Limón Real y Aceite de Oliva",
            technique="american_house_green_salad",
            note="Ensalada crujiente sin lácteos ([R2]) con hojas de lechuga romana, jitomate, alcaparras y vinagreta cítrica.",
            thermo="Ensamble en frío a 8°C.",
            flavor="Acidez vibrante de alcaparras y limón real sobre lechuga crujiente.",
            texture="Hojas enteras crujientes.",
            ccp="Aderezar al momento de emplatar.",
            ingredients=[
                _ing("Lechuga", 1, "piezas", CAT_VEG),
                _ing("Jitomate", 1, "piezas", CAT_VEG),
                _ing("Alcaparras", 36, "g", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Trocear la lechuga romana y el jitomate en gajos.",
                "Aliñar con las alcaparras, jugo de limón de la granja, aceite de oliva extra virgen y sal de mar.",
            ],
        ),
        main=_course(
            title="Philly Cheese Steak Keto al Skillet de Hierro con Tiras de Flat Steak, Juliana de Pimiento Morrón, Cebolla Asada y Costra Fundida de Queso Manchego",
            technique="philly_cheese_steak_skillet",
            note="Escuela 2 (Inspiración IHOP): clásico Philly Cheese Steak servido en sartén de hierro sin pan, con tiras jugosas de flat steak, pimiento morrón, cebolla caramelizada y queso manchego fundido.",
            thermo="Sellado a 195°C en hierro fundido y gratinado del queso manchego a 180°C.",
            flavor="Jugos tostados de res con pimiento morrón, cebolla asada y queso manchego fundido.",
            texture="Tiras tiernas de flat steak cubiertas por manto fundente de queso.",
            ccp="Sellar a fuego vivo para conservar los jugos internos de la res (68°C).",
            archetype="res_philly_cheese_steak_skillet",
            ingredients=[
                _ing("Flat steak", 660, "g", CAT_PROT),
                _ing("Morrón", 2, "piezas", CAT_VEG),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Queso manchego", 90, "g", CAT_DAIRY),
                _ing("Mantequilla", 48, "g", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
                _ing("Pimienta negra", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Saltear en el skillet con mantequilla la cebolla fileteada y la juliana de pimiento morrón hasta dorar.",
                "Incorporar las tiras de flat steak sazonadas con sal con ajo y pimienta negra, sellar a fuego alto y cubrir con el queso manchego hasta fundir.",
            ],
        ),
        side=_course(
            title="Floretes de Brócoli al Vapor con Limón Real, Orégano y Aceite de Oliva VEVO",
            technique="steamed_oregano_broccoli",
            note="Segunda guarnición de Comida ([R4-SIDE] 2/7: brócoli) libre de lácteos ([R2]).",
            thermo="Vapor corto a 96°C por 4 minutos.",
            flavor="Brócoli al dente con notas herbales de orégano y limón real.",
            texture="Floretes firmes y crujientes.",
            ccp="Cero lácteos ni mantequilla ([R2]).",
            ingredients=[
                _ing("Brócoli", 540, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cocer los floretes de brócoli al vapor durante 4 minutos.",
                "Aderezar con aceite de oliva extra virgen, jugo de limón de la granja, orégano y sal de mar.",
            ],
        ),
    )

    d1_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.8, 6.0,
        starter=_course(
            title="Caldo Claro Americano de Fondo de Pollo al Orégano y Limón Real",
            technique="clear_american_poultry_broth",
            note="Caldo reconfortante sin lácteos ([R2]) que antecede a los Zoodles Alfredo.",
            thermo="Infusión suave a 90°C.",
            flavor="Fondo claro de pollo con orégano y limón de la granja.",
            texture="Caldo limpio y ligero.",
            ccp="Servir caliente a 72°C sin grasas pesadas.",
            ingredients=[
                _ing("Fondo claro de pollo", 900, "ml", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Calentar el fondo claro de pollo con orégano y sal de mar.",
                "Servir con unas gotas de limón de la granja y aceite de oliva.",
            ],
        ),
        main=_course(
            title="Zoodles Alfredo de Calabacita con Fajitas de Pechuga de Pavo en Salsa Cremosa de Queso Ricotta, Crema Ácida y Mantequilla al Ajo",
            technique="alfredo_turkey_zoodles_skillet",
            note="Escuela 2 (Inspiración IHOP): sustitución cetogénica de fettuccine por espirales (zoodles) de calabacita al dente con fajitas de pechuga de pavo en salsa Alfredo de queso ricotta, crema ácida y mantequilla.",
            thermo="Salteado de pechuga de pavo a 74°C y ligado de la salsa Alfredo a 75°C sobre zoodles tiernos.",
            flavor="Salsa Alfredo cremosa de ricotta y mantequilla al ajo envolviendo los zoodles de calabacita.",
            texture="Fajitas jugosas de pavo sobre espirales firmes de calabacita.",
            ccp="Saltear los zoodles solo 90 segundos para evitar que suelten agua.",
            archetype="pavo_alfredo_mushroom_zoodles",
            ingredients=[
                _ing("Pechuga de pavo", 700, "g", CAT_PROT),
                _ing("Calabacitas", 480, "g", CAT_VEG),
                _ing("Queso ricotta", 240, "g", CAT_DAIRY),
                _ing("Crema ácida", 180, "g", CAT_DAIRY),
                _ing("Mantequilla", 36, "g", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cortar las calabacitas en espirales tipo zoodles y dorar las fajitas de pechuga de pavo en mantequilla con sal con ajo.",
                "Integrar el queso ricotta y la crema ácida a fuego bajo para formar la salsa Alfredo y envolver los zoodles por 90 segundos.",
            ],
        ),
        side=_course(
            title="Tisana Nocturna de Manzanilla, Limón Real y Clavo de Olor (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="chamomile_clove_infusion",
            note="Segunda tisana nocturna con la Toma 3 de AminoSinergix®.",
            thermo="Infusión templada a ≤60°C.",
            flavor="Manzanilla aromática con toque especiado de clavo y limón real.",
            texture="Infusión cálida.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Clavo de olor", 2, "g", CAT_SPICE),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y el clavo de olor en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C, añadir jugo de limón real y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 2: MARTES — 🌴 ESCUELA 3: ALTA COCINA DEL SURESTE YUCATECO-TABASQUEÑO (Inspiración El Teapaneco)
    # Veg families: Desayuno (ninguno) | Comida (pepino, morron, nopales) | Cena (espinacas)
    # =========================================================================
    d2_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.4,
        starter=_course(
            title="Carpaccio de Fresas a la Canela con Semillas de Chía, Nuez de la India y Nuez Pecana",
            technique="cinnamon_strawberry_carpaccio",
            note="Láminas de fresa sin lácteos ([R4.6]) con canela molida, semillas de chía orgánicas, nuez de la India y nuez pecana.",
            thermo="Emplatado en frío a 6°C.",
            flavor="Fresas aromáticas a la canela con nuez pecana de la granja.",
            texture="Láminas finas de fresa con crocancia de semillas y nueces.",
            ccp="Cero lácteos en la entrada frutal.",
            ingredients=[
                _ing("Fresas", 300, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Canela molida", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Filetear las fresas en láminas tipo carpaccio y espolvorear con canela molida.",
                "Distribuir las semillas de chía orgánicas, la nuez de la India y la nuez pecana.",
            ],
        ),
        main=_course(
            title="Huevos Motuleños Keto sobre Costra Crujiente de Queso Manchego al Comal con Salsa Yucateca de Jitomate Asado, Cebolla y Cilantro",
            technique="yucatecan_motulenos_cheese_crust",
            note="Escuela 3 (Inspiración El Teapaneco): versión cetogénica de los Huevos Motuleños sustituyendo la tortilla frita por una costra crujiente de queso manchego al comal, coronada con 3 huevos por comensal y salsa tatemada de jitomate, cebolla y cilantro.",
            thermo="Costra de queso manchego dorada a 175°C y huevos estrellados en mantequilla a 145°C.",
            flavor="Sazón yucateca de jitomate asado y cilantro sobre costra dorada de queso manchego.",
            texture="Base crujiente de queso con yema cremosa y salsa roja.",
            ccp="Dorar la costra de queso manchego hasta que sea autosoportante.",
            archetype="huevo_motulenos_costra_queso",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Queso manchego", 110, "g", CAT_DAIRY),
                _ing("Jitomate", 1, "piezas", CAT_VEG),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Cilantro", 24, "g", CAT_VEG),
                _ing("Mantequilla", 48, "g", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Fundir y dorar el queso manchego en el comal formando 6 costras circulares crujientes.",
                "Asar el jitomate y la cebolla y moler con cilantro de la granja y sal de mar para la salsa motuleña.",
                "Estrellar los 18 huevos en mantequilla, montar sobre las costras de queso manchego y bañar con la salsa caliente.",
            ],
        ),
        side=_course(
            title="Gelatina Cristalina de Limón Real y Vainilla (4°C) con Fórmula Nootrópica 33Plus®",
            technique="lemon_vanilla_collagen_gel",
            note="Tercera gelatina matutina ([R8]) con limón de la granja, vainilla y MultiSinergix®.",
            thermo="Gelificación a 4°C tras incorporación a ≤42°C.",
            flavor="Cítrico suave a la vainilla.",
            texture="Gel terso a 4°C.",
            ccp="Integrar MultiSinergix® a ≤42°C.",
            ingredients=[
                _ing("Limones", 90, "g", CAT_VEG),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
                _ing("Grenetina", 16, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Hidratar y fundir la grenetina en agua purificada y templar a 40°C.",
                "Agregar el jugo de limón real, el extracto de vainilla y MultiSinergix® (33Plus®), y refrigerar a 4°C.",
            ],
        ),
    )

    d2_l = _meal(
        "Comida", "14:30", 65.0, 43.0, 4.3, 6.6,
        starter=_course(
            title="Ensalada Sureste de Pepino, Cilantro de la Granja y Limón Real al Aceite de Oliva",
            technique="southeast_cucumber_herb_salad",
            note="Ensalada verde obligatoria para plato denso de carne molida ([R2]), 100% libre de lácteos y mantequilla.",
            thermo="Servicio en frío a 8°C.",
            flavor="Frescura cítrica de pepino, cilantro de la granja y aceite de oliva.",
            texture="Medias lunas crujientes de pepino.",
            ccp="Cero mantequilla ni lácteos ([R2] Regla 2.3).",
            ingredients=[
                _ing("Pepino", 360, "g", CAT_VEG),
                _ing("Cilantro", 24, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cortar el pepino en medias lunas y mezclar con el cilantro de la granja finamente picado.",
                "Aliñar con jugo de limón real, aceite de oliva extra virgen y sal de mar.",
            ],
        ),
        main=_course(
            title="Cazuela de Queso Relleno Yucateco (Queso Manchego y Queso Ricotta Fundidos) con Picadillo de Carne Molida de Res, Aceitunas Manzanilla, Alcaparras y Pimiento Morrón en Caldo K'ool de Jitomate",
            technique="yucatecan_queso_relleno_casserole",
            note="Escuela 3 (Inspiración El Teapaneco): clásico Queso Relleno Yucateco elaborado en cazuela con queso manchego y queso ricotta rellenos de picadillo de carne molida de res, aceitunas manzanilla, alcaparras y pimiento morrón sobre salsa roja de jitomate.",
            thermo="Cocción del picadillo de res a 72°C y gratinado en cazuela a 180°C.",
            flavor="Contraste barroco del sureste entre el queso fundido, las alcaparras, las aceitunas y la carne de res.",
            texture="Picadillo jugoso coronado por capa fundente de queso manchego y ricotta.",
            ccp="Escurrir la salmuera de aceitunas y alcaparras antes de integrar al picadillo.",
            archetype="res_queso_relleno_yucateco",
            ingredients=[
                _ing("Carne molida", 600, "g", CAT_PROT),
                _ing("Queso manchego", 90, "g", CAT_DAIRY),
                _ing("Queso ricotta", 240, "g", CAT_DAIRY),
                _ing("Aceitunas manzanilla", 60, "g", CAT_SPICE),
                _ing("Alcaparras", 36, "g", CAT_SPICE),
                _ing("Morrón", 1, "piezas", CAT_VEG),
                _ing("Jitomate", 1, "piezas", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cocinar la carne molida de res con el pimiento morrón picado, las aceitunas manzanilla, las alcaparras, el jitomate asado y el orégano.",
                "Disponer en cazuela con el queso ricotta y cubrir con el queso manchego para gratinar al horno.",
            ],
        ),
        side=_course(
            title="Pencas de Nopal de la Granja Asadas al Comal con Orégano, Cilantro y Aceite de Oliva VEVO",
            technique="griddled_farm_cactus_paddles",
            note="Tercera guarnición de Comida ([R4-SIDE] 3/7: nopales) libre de mantequilla y lácteos ([R2]).",
            thermo="Asado en seco al comal a 185°C por 4 minutos por lado.",
            flavor="Notas herbales de nopal de la granja al orégano y aceite de oliva.",
            texture="Pencas tiernas y asadas sin mucílago.",
            ccp="Cero mantequilla ni lácteos ([R2]).",
            ingredients=[
                _ing("Nopales", 480, "g", CAT_VEG),
                _ing("Cilantro", 18, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Asar las pencas de nopal de la granja en el comal caliente con sal de mar y orégano.",
                "Terminar con cilantro picado y aceite de oliva extra virgen.",
            ],
        ),
    )

    d2_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.9, 6.1,
        starter=_course(
            title="Sopa de Lima Yucateca en Fondo Claro de Pollo con Jitomate, Cilantro de la Granja y Limón Real",
            technique="yucatecan_lime_clear_soup",
            note="Escuela 3 (Inspiración El Teapaneco): aromática Sopa de Lima elaborada en fondo claro de pollo con jitomate asado, orégano, cilantro y limón de la granja.",
            thermo="Infusión aromática a 90°C sin frituras ni harinas.",
            flavor="Perfume cítrico del sureste con fondo claro de ave y cilantro.",
            texture="Caldo cristalino y sedoso.",
            ccp="Añadir el jugo cítrico al final para evitar amargor.",
            archetype="entrada_sopa_lima_yucateca",
            ingredients=[
                _ing("Fondo claro de pollo", 900, "ml", CAT_SPICE),
                _ing("Jitomate", 1, "piezas", CAT_VEG),
                _ing("Cilantro", 24, "g", CAT_VEG),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Infusionar el fondo claro de pollo con jitomate asado, orégano y aceite de oliva durante 8 minutos.",
                "Perfumar fuera del fuego con jugo de limón de la granja y hojas de cilantro.",
            ],
        ),
        main=_course(
            title="Milanesa de Pechuga de Pollo en Costra Crujiente de Nuez Pecana y Nuez de la India al Horno sobre Cama de Espinacas al Aceite de Coco",
            technique="pecan_cashew_crusted_chicken_cutlet",
            note="Escuela 3 (Inspiración El Teapaneco): milanesa cetogénica sin pan molido ni huevo ([R12]), empanizada en polvo tostado de nuez pecana y nuez de la India al horno sobre espinacas.",
            thermo="Horneado por convección a 190°C hasta alcanzar 74°C en centro térmico.",
            flavor="Dorado de nuez pecana de la granja y nuez de la India con espinacas tiernas.",
            texture="Costra crujiente de frutos secos con pechuga jugosa.",
            ccp="Verificar 74°C internos sin usar huevo en el rebozado ([R12]).",
            archetype="pollo_milanesa_costra_nuez",
            ingredients=[
                _ing("Pechuga de pollo", 900, "g", CAT_PROT),
                _ing("Nuez pecana", 90, "g", CAT_FAT),
                _ing("Nuez de la India", 90, "g", CAT_FAT),
                _ing("Espinacas", 360, "g", CAT_VEG),
                _ing("Aceite de coco", 48, "g", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
                _ing("Orégano", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Triturar la nuez pecana y la nuez de la India con sal con ajo y orégano, y adherir a las milanesas de pechuga de pollo barnizadas con aceite de coco.",
                "Hornear a 190°C durante 14 minutos y servir sobre cama de espinacas salteadas.",
            ],
        ),
        side=_course(
            title="Tisana Nocturna de Manzanilla y Hierbas Finas (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="chamomile_herbs_infusion",
            note="Tercera tisana nocturna con la Toma 3 de AminoSinergix®.",
            thermo="Infusión templada a ≤60°C.",
            flavor="Manzanilla floral y hierbas finas.",
            texture="Infusión cálida.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Hierbas finas", 3, "g", CAT_SPICE),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y las hierbas finas en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 3: MIÉRCOLES — 🇪🇸 ESCUELA 4: ASADOR ESPAÑOL Y TAPAS DE CAZUELA (Inspiración Asador Castellano)
    # Veg families: Desayuno (esparragos) | Comida (calabacitas) | Cena (espinacas, morron)
    # =========================================================================
    d3_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.1, 6.3,
        starter=_course(
            title="Tartar de Zarzamora a la Vainilla con Semillas de Chía, Nuez de la India y Nuez Pecana",
            technique="blackberry_vanilla_tartare",
            note="Zarzamora con vainilla, semillas de chía orgánicas, nuez de la India y nuez pecana sin lácteos ([R4.6]).",
            thermo="Servicio en frío a 6°C.",
            flavor="Zarzamora perfumada a la vainilla con nuez pecana.",
            texture="Dado fino de fruta con semillas.",
            ccp="Cero lácteos en la entrada frutal.",
            ingredients=[
                _ing("Zarzamora", 170, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
            ],
            steps=[
                "Mezclar la zarzamora con el extracto de vainilla en moldes individuales.",
                "Coronar con las semillas de chía orgánicas, la nuez de la India y la nuez pecana.",
            ],
        ),
        main=_course(
            title="Tortilla Española Cetogénica al Sartén de Huevos de Granja Rellena de Puntas de Espárragos Trigueros, Cebolla Confitada y Aceite de Oliva",
            technique="castilian_asparagus_spanish_tortilla",
            note="Escuela 4 (Inspiración Asador Castellano): tortilla española cetogénica sustituyendo la papa por puntas de espárragos trigueros y cebolla confitada en aceite de oliva extra virgen.",
            thermo="Confitado lento en aceite de oliva a 130°C y cuajado jugoso de la tortilla española a 145°C.",
            flavor="Tradición de taberna castellana con aceite de oliva, cebolla confitada y espárragos.",
            texture="Exterior dorado y centro jugoso estilo Betanzos.",
            ccp="Voltear la tortilla española con plato tibio manteniendo el corazón tierno.",
            archetype="huevo_tortilla_espanola_calabacita",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Espárragos", 420, "g", CAT_VEG),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Confitar la cebolla fileteada y los espárragos troceados en el aceite de oliva a fuego suave durante 6 minutos.",
                "Integrar los 18 huevos batidos con sal de mar y cuajar la tortilla española en sartén por ambos lados.",
            ],
        ),
        side=_course(
            title="Gelatina de Flor de Jamaica y Limón Real (4°C) con Fórmula Nootrópica 33Plus®",
            technique="hibiscus_citrus_collagen_gel",
            note="Cuarta gelatina matutina ([R8]) con flor de Jamaica, limón real y MultiSinergix®.",
            thermo="Gelificación a 4°C tras integrar a ≤42°C.",
            flavor="Acidez equilibrada de Jamaica y limón de la granja.",
            texture="Gel firme a 4°C.",
            ccp="Proteger MultiSinergix® a ≤42°C.",
            ingredients=[
                _ing("Flor de Jamaica molida en polvo", 24, "g", CAT_SPICE),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("Grenetina", 16, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la flor de Jamaica en agua purificada, hidratar la grenetina y templar a 40°C.",
                "Incorporar el jugo de limón real y MultiSinergix® (33Plus®) y refrigerar a 4°C.",
            ],
        ),
    )

    d3_l = _meal(
        "Comida", "14:30", 65.0, 43.0, 4.2, 6.4,
        starter=_course(
            title="Sopa Castellana de Cebolla Caramelizada en Fondo de Res con Tomillo y Aceite de Oliva",
            technique="castilian_caramelized_onion_soup",
            note="Escuela 4 (Inspiración Asador Castellano): sopa de cebolla de asador español elaborada en fondo de res casero con tomillo y aceite de oliva sin pan ni lácteos ([R2]).",
            thermo="Caramelización lenta de la cebolla a 140°C y hervor suave en fondo de res.",
            flavor="Dulzor natural de cebolla dorada con fondo de res y tomillo.",
            texture="Caldo ambarino con hebras tiernas de cebolla.",
            ccp="Caramelizar la cebolla sin azúcares añadidos.",
            archetype="entrada_sopa_cebolla_castellana",
            ingredients=[
                _ing("Fondo de res", 900, "ml", CAT_SPICE),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Rehogar la cebolla en pluma fina con el aceite de oliva y tomillo hasta que adquiera tono dorado.",
                "Verter el fondo de res casero, sazonar con sal de mar y hervir suavemente 8 minutos.",
            ],
        ),
        main=_course(
            title="Fajitas de Mojarra a la Murciana en Cazuela de Jitomate Asado, Alcaparras, Aceitunas Manzanilla, Orégano y Aceite de Oliva",
            technique="murcian_fish_claypot_braise",
            note="Escuela 4 (Inspiración Asador Castellano): pescado a la murciana cocinado en cazuela con jitomate asado, alcaparras, aceitunas manzanilla, orégano y aceite de oliva.",
            thermo="Cocción suave en cazuela a 155°C por 8 minutos hasta alcanzar 63°C en el pescado.",
            flavor="Salsa mediterránea española de jitomate, alcaparras y aceitunas manzanilla.",
            texture="Fajitas de mojarra jugosas en su jugo de cazuela.",
            ccp="No sobrecocinar la mojarra para preservar su textura firme.",
            archetype="pescado_a_la_murciana_cazuela",
            ingredients=[
                _ing("Fajitas de mojarra", 450, "g", CAT_PROT),
                _ing("Jitomate", 1, "piezas", CAT_VEG),
                _ing("Alcaparras", 42, "g", CAT_SPICE),
                _ing("Aceitunas manzanilla", 55, "g", CAT_SPICE),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Sofreír el jitomate troceado en aceite de oliva con las alcaparras, las aceitunas manzanilla y el orégano.",
                "Incorporar las fajitas de mojarra en la cazuela, tapar y cocinar 7 minutos a fuego medio.",
            ],
        ),
        side=_course(
            title="Láminas de Calabacitas Asadas al Comal con Romero de la Granja y Aceite de Oliva VEVO",
            technique="griddled_rosemary_zucchini_ribbons",
            note="Cuarta guarnición de Comida ([R4-SIDE] 4/7: calabacitas) libre de lácteos.",
            thermo="Sellado en comal a 180°C por 2 minutos por lado.",
            flavor="Calabacitas asadas perfumadas con romero de la granja.",
            texture="Láminas tiernas con marcas de asado.",
            ccp="Cortar longitudinalmente de grosor uniforme.",
            ingredients=[
                _ing("Calabacitas", 540, "g", CAT_VEG),
                _ing("Romero", 6, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Laminar las calabacitas a lo largo y asar en el comal con aceite de oliva.",
                "Perfumar con romero de la granja y sal de mar.",
            ],
        ),
    )

    d3_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.9, 6.2,
        starter=_course(
            title="Ensalada de Hojas de Espinacas con Limón Real, Orégano y Aceite de Oliva",
            technique="castilian_spinach_citrus_salad",
            note="Entrada verde sin lácteos ([R2]) que equilibra los Pimientos Rellenos Gratinados.",
            thermo="Emplatado en frío a 8°C.",
            flavor="Hojas de espinaca con limón de la granja y orégano.",
            texture="Hojas enteras y tiernas.",
            ccp="Cero lácteos en la entrada ([R2]).",
            ingredients=[
                _ing("Espinacas", 300, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Disponer las hojas de espinaca desinfectadas en platos fríos.",
                "Aliñar con jugo de limón real, aceite de oliva extra virgen, orégano y sal de mar.",
            ],
        ),
        main=_course(
            title="Pimientos Morrones Asados Rellenos de Atún en Agua, Queso Ricotta y Cebolla con Costra Gratinada de Queso Manchego al Horno",
            technique="castilian_stuffed_peppers_bake",
            note="Escuela 4 (Inspiración Asador Castellano): pimientos morrones enteros asados y rellenos de lomo de atún en agua, queso ricotta y cebolla al orégano, gratinados con queso manchego.",
            thermo="Asado de los pimientos morrones y gratinado al horno a 185°C por 8 minutos.",
            flavor="Dulzor del pimiento morrón asado con relleno cremoso de atún, ricotta y manchego.",
            texture="Pimiento tierno con corazón proteico y costra dorada.",
            ccp="Drenar completamente el atún en agua antes de mezclar con el queso ricotta.",
            archetype="atun_pimientos_rellenos_gratinados",
            ingredients=[
                _ing("Atún en agua", 660, "g", CAT_PROT),
                _ing("Morrón", 2, "piezas", CAT_VEG),
                _ing("Queso ricotta", 240, "g", CAT_DAIRY),
                _ing("Queso manchego", 90, "g", CAT_DAIRY),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Asar los pimientos morrones cortados en mitades y retirar las semillas.",
                "Mezclar el atún en agua drenado con la cebolla acitronada en aceite de oliva, el queso ricotta, orégano y sal de mar.",
                "Rellenar los pimientos morrones, cubrir con el queso manchego y gratinar al horno por 8 minutos.",
            ],
        ),
        side=_course(
            title="Tisana Nocturna de Manzanilla, Canela y Limón Real (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="chamomile_lemon_infusion",
            note="Cuarta tisana nocturna con la Toma 3 de AminoSinergix®.",
            thermo="Infusión templada a ≤60°C.",
            flavor="Manzanilla, canela y limón real.",
            texture="Infusión cálida.",
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
                "Templar a 58°C, agregar jugo de limón real y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 4: JUEVES — 🇫🇷 ESCUELA 5: BISTRÓ EUROPEO DE FOCACCIAS KETO Y ENSALADAS (Inspiración Alda Café)
    # Veg families: Desayuno (coliflor) | Comida (lechuga, pepino, esparragos) | Cena (champinon, espinacas)
    # =========================================================================
    d4_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.4,
        starter=_course(
            title="Compota Fría de Frambuesas y Canela con Semillas de Chía, Nuez de la India y Nuez Pecana",
            technique="cold_raspberry_cinnamon_compote",
            note="Frambuesas maceradas con canela, semillas de chía orgánicas, nuez de la India y nuez pecana sin lácteos ([R4.6]).",
            thermo="Maceración en frío a 6°C.",
            flavor="Frambuesa y canela con frutos secos.",
            texture="Compota rústica con semillas y nueces.",
            ccp="Cero lácteos en la entrada frutal.",
            ingredients=[
                _ing("Frambuesas", 125, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Canela molida", 3, "g", CAT_SPICE),
            ],
            steps=[
                "Macerar ligeramente las frambuesas con la canela molida.",
                "Servir con las semillas de chía orgánicas, la nuez de la India y la nuez pecana.",
            ],
        ),
        main=_course(
            title="Focaccia Keto Horneada de Coliflor y 3 Quesos (Queso Manchego, Queso Ricotta y Queso Philadelphia) con Huevos al Plato y Romero de la Granja",
            technique="bistro_three_cheese_keto_focaccia",
            note="Escuela 5 (Inspiración Alda Café): pan focaccia cetogénico horneado con base de coliflor prensada, queso manchego, queso ricotta y queso Philadelphia al romero, coronado con 3 huevos por comensal.",
            thermo="Horneado de la masa de focaccia keto a 190°C por 12 minutos y cuajado de los huevos a 175°C.",
            flavor="Aroma de bistró europeo con romero de la granja y 3 quesos fundidos.",
            texture="Base alveolada de focaccia keto dorada con huevos tiernos.",
            ccp="Prensar los floretes de coliflor para lograr una focaccia firme y crujiente.",
            archetype="focaccia_keto_tres_quesos_esparragos",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Coliflor", 250, "g", CAT_VEG),
                _ing("Queso manchego", 90, "g", CAT_DAIRY),
                _ing("Queso ricotta", 180, "g", CAT_DAIRY),
                _ing("Queso Philadelphia", 120, "g", CAT_DAIRY),
                _ing("Romero", 6, "g", CAT_VEG),
                _ing("Mantequilla", 36, "g", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Rallar la coliflor, mezclar con el queso manchego, el queso ricotta, el queso Philadelphia y el romero, y hornear formando una focaccia dorada.",
                "Cascar los 18 huevos sobre la focaccia con mantequilla y sal de mar, y hornear 6 minutos hasta cuajar las claras.",
            ],
        ),
        side=_course(
            title="Infusión Matutina de Té Chai, Canela y Aceite de Coco (≤60°C) con Fórmula Nootrópica 33Plus®",
            technique="chai_mct_emulsion",
            note="Infusión especiada matutina con té chai, canela, aceite de coco y la Toma 2 de MultiSinergix®.",
            thermo="Infusión a 85°C templada a ≤60°C.",
            flavor="Especias chai con cuerpo lipídico de coco.",
            texture="Bebida sedosa.",
            ccp="Integrar MultiSinergix® a ≤60°C.",
            ingredients=[
                _ing("Té chai", 12, "g", CAT_SPICE),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("Aceite de coco", 30, "g", CAT_FAT),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar el té chai y la canela en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 55°C, emulsionar con el aceite de coco y MultiSinergix® (33Plus®).",
            ],
        ),
    )

    d4_l = _meal(
        "Comida", "14:30", 65.0, 43.0, 4.1, 6.3,
        starter=_course(
            title="Ensalada Bistró de Lechuga Romana y Pepino al Limón Real, Orégano y Aceite de Oliva",
            technique="european_bistro_cucumber_salad",
            note="Ensalada europea crujiente sin lácteos ([R2]) para acompañar el Salmón Estilo Alda.",
            thermo="Emplatado en frío a 8°C.",
            flavor="Vinagreta de limón real, orégano y aceite de oliva sobre lechuga y pepino.",
            texture="Hojas crujientes y rodajas de pepino.",
            ccp="Cero lácteos en la entrada ([R2]).",
            ingredients=[
                _ing("Lechuga", 1, "piezas", CAT_VEG),
                _ing("Pepino", 300, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Cortar la lechuga romana y el pepino en rodajas finas.",
                "Aderezar con jugo de limón real, aceite de oliva extra virgen, orégano y sal de mar.",
            ],
        ),
        main=_course(
            title="Lomo de Salmón Estilo Alda al Sartén sobre Espejo de Queso Philadelphia, Alcaparras, Limón Real y Hierbas Finas en Mantequilla",
            technique="alda_bistro_salmon_philadelphia_mirror",
            note="Escuela 5 (Inspiración Alda Café): lomo de salmón sellado en mantequilla servido sobre espejo cremoso de queso Philadelphia, alcaparras, limón real y hierbas finas.",
            thermo="Sellado del salmón por el lado de la piel a 175°C hasta 63°C internos sobre espejo templado de Philadelphia.",
            flavor="Armonía bistró entre el salmón en mantequilla, la acidez de las alcaparras y el queso Philadelphia.",
            texture="Piel crujiente y lomo jugoso sobre espejo untuoso.",
            ccp="No sobrecocinar el salmón (63°C internos) para preservar sus ácidos grasos Omega-3.",
            archetype="salmon_estilo_alda_philadelphia_alcaparras",
            ingredients=[
                _ing("Lomo de salmón", 600, "g", CAT_PROT),
                _ing("Queso Philadelphia", 180, "g", CAT_DAIRY),
                _ing("Alcaparras", 42, "g", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Mantequilla", 48, "g", CAT_FAT),
                _ing("Hierbas finas", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Acremar el queso Philadelphia tibio con jugo de limón real y hierbas finas para formar el espejo en el plato.",
                "Sellar el lomo de salmón en sartén con la mantequilla y sal de mar, montar sobre el espejo y coronar con las alcaparras.",
            ],
        ),
        side=_course(
            title="Espárragos Verdes Asados a la Plancha con Limón Real, Sal con Ajo y Aceite de Oliva VEVO",
            technique="chargrilled_citrus_asparagus",
            note="Quinta guarnición de Comida ([R4-SIDE] 5/7: espárragos) libre de lácteos ([R2]).",
            thermo="Asado en plancha a 185°C durante 4 minutos.",
            flavor="Notas tostadas de espárrago verde con limón real y sal con ajo.",
            texture="Tallos tiernos y puntas crujientes.",
            ccp="Cero lácteos en la guarnición ([R2]).",
            ingredients=[
                _ing("Espárragos", 420, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Asar los espárragos verdes en plancha caliente con aceite de oliva y sal con ajo.",
                "Terminar con jugo de limón de la granja al servir.",
            ],
        ),
    )

    d4_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.9, 6.1,
        starter=_course(
            title="Consomé Bistró de Fondo Claro de Pollo al Tomillo y Limón Real",
            technique="bistro_thyme_clear_consomme",
            note="Consomé ligero sin lácteos ([R2]) con tomillo y limón de la granja.",
            thermo="Infusión a 90°C.",
            flavor="Aroma herbal de tomillo en fondo claro de ave.",
            texture="Caldo diáfano.",
            ccp="Servir caliente sin cremas ([R2]).",
            ingredients=[
                _ing("Fondo claro de pollo", 900, "ml", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Hervir suavemente el fondo claro de pollo con el tomillo y sal de mar por 6 minutos.",
                "Servir con jugo de limón real y aceite de oliva.",
            ],
        ),
        main=_course(
            title="Focaccia Keto de Champiñones Salteados, Espinacas, Queso Ricotta y Queso Manchego Dorada al Sartén de Hierro con Romero",
            technique="iron_skillet_mushroom_keto_focaccia",
            note="Escuela 5 (Inspiración Alda Café): focaccia cetogénica dorada en sartén de hierro con cubierta de champiñones salteados, espinacas, queso ricotta, queso manchego y romero de la granja (0 huevos en cena [R12]).",
            thermo="Dorado de la base en sartén de hierro a 170°C y fundido superior con tapa a 150°C.",
            flavor="Umami de champiñones y romero sobre base dorada de queso manchego y ricotta.",
            texture="Base crujiente de sartén con topping jugoso de hongos y espinacas.",
            ccp="Dorar en sartén de hierro sin usar huevo en la cena ([R12]).",
            archetype="focaccia_keto_hongos_gratinados",
            ingredients=[
                _ing("Champiñón", 660, "g", CAT_VEG),
                _ing("Espinacas", 300, "g", CAT_VEG),
                _ing("Queso ricotta", 240, "g", CAT_DAIRY),
                _ing("Queso manchego", 100, "g", CAT_DAIRY),
                _ing("Romero", 6, "g", CAT_VEG),
                _ing("Mantequilla", 36, "g", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Formar la base en el sartén de hierro con queso manchego y queso ricotta hasta que dore por debajo.",
                "Cubrir con los champiñones y las espinacas salteados en mantequilla con romero y sal de mar, y tapar 3 minutos para fundir.",
            ],
        ),
        side=_course(
            title="Tisana Nocturna de Manzanilla y Orégano (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="chamomile_oregano_infusion",
            note="Quinta tisana nocturna con la Toma 3 de AminoSinergix®.",
            thermo="Infusión templada a ≤60°C.",
            flavor="Manzanilla suave con toque de orégano.",
            texture="Infusión cálida.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y el orégano en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 5: VIERNES — 🌊 ESCUELA 6: PACÍFICO & ORIENTE (Costa Mexicana, Teppanyaki & Curry Dorado)
    # Veg families: Desayuno (coliflor) | Comida (pepino, morron, acelgas) | Cena (calabacitas)
    # =========================================================================
    d5_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.5,
        starter=_course(
            title="Coulis Rústico de Fresas al Limón Real con Semillas de Chía, Nuez de la India y Nuez Pecana",
            technique="citrus_strawberry_coulis_bowl",
            note="Fresas machacadas en frío con limón real, semillas de chía orgánicas, nuez de la India y nuez pecana sin lácteos ([R4.6]).",
            thermo="Preparación en frío a 6°C.",
            flavor="Fresas vibrantes con limón de la granja y nueces.",
            texture="Coulis rústico con crocancia de semillas y nuez pecana.",
            ccp="Cero lácteos en la entrada frutal.",
            ingredients=[
                _ing("Fresas", 300, "g", CAT_FRUIT),
                _ing("Limones", 30, "g", CAT_VEG),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
            ],
            steps=[
                "Trocear las fresas con jugo de limón de la granja formando un coulis rústico.",
                "Añadir las semillas de chía orgánicas, la nuez de la India y la nuez pecana.",
            ],
        ),
        main=_course(
            title="Omurice Keto Japonés (Omelette Terso de Huevos Relleno de Grano Fino de Coliflor Salteado al Wok con Germinado, Cebolla y Aceite de Coco)",
            technique="japanese_keto_omurice_wok",
            note="Escuela 6 (Pacífico & Oriente): versión cetogénica del clásico Omurice japonés empleando grano fino de coliflor salteado al wok con germinado, cebolla y aceite de coco, envuelto en manto terso de 3 huevos por comensal.",
            thermo="Salteado de la coliflor al wok a 185°C y omelette japonés a 140°C.",
            flavor="Notas orientales tostadas del wok con coliflor, germinado y huevo sedoso.",
            texture="Interior granulado al dente de coliflor y exterior aterciopelado de huevo.",
            ccp="Rallar la coliflor en grano fino y saltear en seco antes de añadir el aceite de coco.",
            archetype="huevo_omurice_keto_coliflor",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Coliflor", 250, "g", CAT_VEG),
                _ing("Germinado", 180, "g", CAT_VEG),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Aceite de coco", 48, "g", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Rallar la coliflor en grano fino y saltear al wok con el aceite de coco, la cebolla picada y el germinado.",
                "Cuajar los 18 huevos batidos en mantos finos y envolver la coliflor salteada al estilo Omurice japonés.",
            ],
        ),
        side=_course(
            title="Gelatina de Flor de Jamaica y Romero de la Granja (4°C) con Fórmula Nootrópica 33Plus®",
            technique="hibiscus_rosemary_collagen_gel",
            note="Quinta gelatina matutina semanal ([R8] >= 5 gelatinas cumplidas) con flor de Jamaica, romero y MultiSinergix®.",
            thermo="Gelificación a 4°C tras integrar MultiSinergix® a ≤42°C.",
            flavor="Jamaica herbal al romero de la granja.",
            texture="Gel cristalino a 4°C.",
            ccp="Incorporar MultiSinergix® a ≤42°C.",
            ingredients=[
                _ing("Flor de Jamaica molida en polvo", 24, "g", CAT_SPICE),
                _ing("Romero", 6, "g", CAT_VEG),
                _ing("Grenetina", 16, "g", CAT_SUPP),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 720, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la flor de Jamaica y el romero en agua purificada, hidratar la grenetina y templar a 40°C.",
                "Incorporar MultiSinergix® (33Plus®) y refrigerar en moldes a 4°C.",
            ],
        ),
    )

    d5_l = _meal(
        "Comida", "14:30", 65.0, 43.0, 4.2, 6.5,
        starter=_course(
            title="Ensalada Oriental Sunomono de Pepino en Láminas con Nuez de la India, Limón Real y Aceite de Oliva",
            technique="japanese_sunomono_cucumber_salad",
            note="Escuela 6 (Pacífico & Oriente): ensalada japonesa Sunomono de pepino laminado con nuez de la India y limón real sin lácteos ([R2]).",
            thermo="Maceración rápida en frío a 8°C.",
            flavor="Frescura cítrica oriental con nuez de la India tostada.",
            texture="Cintas crujientes de pepino.",
            ccp="Cero lácteos ni mantequilla ([R2]).",
            ingredients=[
                _ing("Pepino", 360, "g", CAT_VEG),
                _ing("Nuez de la India", 36, "g", CAT_FAT),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Laminar el pepino finamente y drenar el exceso de humedad con una pizca de sal de mar.",
                "Aliñar con jugo de limón real, aceite de oliva extra virgen y nuez de la India picada.",
            ],
        ),
        main=_course(
            title="Teppanyaki de Flat Steak a la Plancha con Pimiento Morrón, Cebolla Asada y Germinado en Aceite de Coco",
            technique="japanese_teppanyaki_flat_steak",
            note="Escuela 6 (Pacífico & Oriente): cubos de flat steak sellados a la plancha estilo Teppanyaki con pimiento morrón, cebolla asada y germinado en aceite de coco.",
            thermo="Plancha de hierro a 200°C para sellado rápido Maillard (68°C internos).",
            flavor="Umami de plancha japonesa con germinado crujiente y aceite de coco.",
            texture="Bocados jugosos de res con vegetales al dente.",
            ccp="Añadir el germinado en los últimos 45 segundos para mantener su crocancia.",
            archetype="res_teppanyaki_plancha_germinado",
            ingredients=[
                _ing("Flat steak", 660, "g", CAT_PROT),
                _ing("Morrón", 2, "piezas", CAT_VEG),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Germinado", 180, "g", CAT_VEG),
                _ing("Aceite de coco", 48, "g", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Calentar la plancha con el aceite de coco y sellar el flat steak cortado en cubos junto con la cebolla y el pimiento morrón.",
                "Incorporar el germinado y sazonar con sal con ajo antes de retirar de la plancha.",
            ],
        ),
        side=_course(
            title="Acelgas de la Granja Salteadas al Wok con Limón Real, Orégano y Aceite de Oliva VEVO",
            technique="wok_sauteed_oregano_chard",
            note="Sexta guarnición de Comida ([R4-SIDE] 6/7: acelgas) libre de lácteos ([R2]).",
            thermo="Salteado rápido al wok a 180°C por 3 minutos.",
            flavor="Hojas de acelga de la granja con orégano y limón real.",
            texture="Tallos tiernos y hojas sedosas.",
            ccp="Cero lácteos en la guarnición ([R2]).",
            ingredients=[
                _ing("Acelgas", 480, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Saltear las acelgas de la granja troceadas en el wok con aceite de oliva durante 3 minutos.",
                "Perfumar con jugo de limón real, orégano y sal de mar.",
            ],
        ),
    )

    d5_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.9, 6.1,
        starter=_course(
            title="Caldo Oriental Claro de Fondo de Pollo al Cilantro de la Granja y Limón Real",
            technique="oriental_cilantro_clear_broth",
            note="Caldo ligero y digestivo sin lácteos.",
            thermo="Infusión a 90°C.",
            flavor="Fondo claro de ave con cilantro de la granja y limón real.",
            texture="Caldo limpio.",
            ccp="Servir a 72°C.",
            ingredients=[
                _ing("Fondo claro de pollo", 900, "ml", CAT_SPICE),
                _ing("Cilantro", 24, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Calentar el fondo claro de pollo con sal de mar y aceite de oliva.",
                "Perfumar al servir con cilantro de la granja y jugo de limón real.",
            ],
        ),
        main=_course(
            title="Fajitas de Mojarra Bicolor a las Brasas Estilo Contramar (Mitad en Adobo Rojo de Achiote y Jitomate, Mitad en Emulsión Verde de Cilantro y Tomate) sobre Calabacitas",
            technique="contramar_bicolor_grilled_fish",
            note="Escuela 6 (Pacífico & Oriente — Inspiración Contramar): pescado bicolor sin chiles irritantes ([R1]), mitad marinado en adobo rojo de achiote y jitomate asado y mitad en salsa verde de cilantro y tomate sobre calabacitas asadas.",
            thermo="Asado a la plancha/brasas a 185°C hasta 63°C en centro térmico.",
            flavor="Doble perfil costero mexicano: tierra especiada de achiote y frescura herbal de cilantro.",
            texture="Lomos firmes de mojarra sobre cama de calabacitas.",
            ccp="Elaborar el adobo rojo con achiote y jitomate 0% capsaicina ([R1]).",
            archetype="mojarra_bicolor_estilo_contramar",
            ingredients=[
                _ing("Fajitas de mojarra", 450, "g", CAT_PROT),
                _ing("Calabacitas", 420, "g", CAT_VEG),
                _ing("Achiote", 18, "g", CAT_SPICE),
                _ing("Jitomate", 1, "piezas", CAT_VEG),
                _ing("Tomate", 180, "g", CAT_VEG),
                _ing("Cilantro", 24, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Preparar el adobo rojo moliendo el achiote con el jitomate asado, y la emulsión verde moliendo el tomate con el cilantro de la granja.",
                "Untar la mitad de las fajitas de mojarra con el adobo rojo y la otra mitad con la emulsión verde, y asar a la plancha sobre láminas de calabacitas.",
            ],
        ),
        side=_course(
            title="Tisana Nocturna de Manzanilla y Canela Molida (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="night_chamomile_infusion",
            note="Sexta tisana nocturna con la Toma 3 de AminoSinergix®.",
            thermo="Infusión templada a ≤60°C.",
            flavor="Manzanilla y canela.",
            texture="Infusión cálida.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y la canela en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    # =========================================================================
    # DÍA 6: SÁBADO — 🇮🇹 ESCUELA 7: MARE NOSTRUM (Alta Trattoria Italiana & Islas Griegas)
    # Veg families: Desayuno (ninguno) | Comida (lechuga, calabacitas, champinon) | Cena (espinacas, pepino)
    # =========================================================================
    d6_b = _meal(
        "Desayuno", "08:30", 49.0, 34.5, 4.2, 6.4,
        starter=_course(
            title="Macerado Mediterráneo de Fresas con Semillas de Chía, Nuez de la India, Nuez Pecana y Vainilla",
            technique="mediterranean_strawberry_maceration",
            note="Fresas sin lácteos ([R4.6]) con vainilla, semillas de chía orgánicas, nuez de la India y nuez pecana.",
            thermo="Servicio en frío a 6°C.",
            flavor="Fresas a la vainilla con nuez pecana de la granja.",
            texture="Bayas en cuartos con semillas de chía.",
            ccp="Cero lácteos en la entrada frutal.",
            ingredients=[
                _ing("Fresas", 300, "g", CAT_FRUIT),
                _ing("Semillas de chía orgánicas", 48, "g", CAT_FAT),
                _ing("Nuez de la India", 60, "g", CAT_FAT),
                _ing("Nuez pecana", 60, "g", CAT_FAT),
                _ing("Extracto de vainilla", 6, "ml", CAT_SPICE),
            ],
            steps=[
                "Perfumar las fresas con el extracto de vainilla.",
                "Distribuir las semillas de chía orgánicas, la nuez de la India y la nuez pecana.",
            ],
        ),
        main=_course(
            title="Uova in Purgatorio de la Trattoria Napolitana (Huevos Escalfados en Salsa Rústica de Jitomate Asado, Queso Ricotta, Hierbas Finas y Aceite de Oliva)",
            technique="neapolitan_uova_in_purgatorio",
            note="Escuela 7 (Mare Nostrum — Trattoria Italiana): 3 huevos por comensal escalfados directamente sobre reducción napolitana de jitomate asado, rosetones de queso ricotta, hierbas finas y aceite de oliva.",
            thermo="Reducción del sugo de jitomate a 92°C y escalfado de los huevos a 85°C por 4 minutos.",
            flavor="Sugo italiano de jitomate asado y hierbas finas con cremosidad de queso ricotta.",
            texture="Claras cuajadas en el sugo y yemas líquidas con ricotta.",
            ccp="Mantener las yemas cremosas al retirar del fuego.",
            archetype="huevo_uova_in_purgatorio",
            ingredients=[
                _ing("Huevo", 18, "piezas", CAT_PROT),
                _ing("Jitomate", 1, "piezas", CAT_VEG),
                _ing("Queso ricotta", 240, "g", CAT_DAIRY),
                _ing("Hierbas finas", 6, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Asar y triturar el jitomate con el aceite de oliva, las hierbas finas y la sal con ajo formando un sugo rústico en sartén amplia.",
                "Formar 18 cavidades en la salsa, cascar los huevos y escalfar tapados por 4 minutos; terminar con rosetones de queso ricotta.",
            ],
        ),
        side=_course(
            title="Infusión Templada de Flor de Jamaica, Canela y Limón Real (≤60°C) con Fórmula Nootrópica 33Plus®",
            technique="hibiscus_cinnamon_morning_infusion",
            note="Infusión matutina antioxidante con la Toma 2 de MultiSinergix®.",
            thermo="Infusión templada a ≤60°C.",
            flavor="Flor de Jamaica, canela y limón de la granja.",
            texture="Infusión cálida.",
            ccp="Integrar MultiSinergix® a ≤60°C.",
            ingredients=[
                _ing("Flor de Jamaica molida en polvo", 24, "g", CAT_SPICE),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("Limones", 60, "g", CAT_VEG),
                _ing("MultiSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la flor de Jamaica y la canela en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 55°C, añadir jugo de limón real y disolver MultiSinergix® (33Plus®).",
            ],
        ),
    )

    d6_l = _meal(
        "Comida", "14:30", 65.0, 43.0, 4.3, 6.7,
        starter=_course(
            title="Ensalada Mare Nostrum de Lechuga Romana, Aceitunas Manzanilla, Orégano y Limón Real al Aceite de Oliva",
            technique="mare_nostrum_olive_salad",
            note="Ensalada verde obligatoria para plato denso de carne molida ([R2]), libre de mantequilla y lácteos.",
            thermo="Emplatado en frío a 8°C.",
            flavor="Perfil griego de aceitunas manzanilla, orégano y limón real.",
            texture="Hojas crujientes de lechuga romana.",
            ccp="Cero lácteos ni mantequilla ([R2]).",
            ingredients=[
                _ing("Lechuga", 1, "piezas", CAT_VEG),
                _ing("Aceitunas manzanilla", 55, "g", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Trocear la lechuga romana y disponer en tazones con las aceitunas manzanilla.",
                "Aliñar con jugo de limón real, aceite de oliva extra virgen, orégano y sal de mar.",
            ],
        ),
        main=_course(
            title="Moussaka Griega al Horno en Capas de Calabacitas Asadas, Ragú de Carne Molida de Res a la Canela y Gratinado de Queso Ricotta y Queso Manchego",
            technique="greek_keto_zucchini_moussaka",
            note="Escuela 7 (Mare Nostrum — Islas Griegas): Moussaka tradicional helénica adaptada con láminas de calabacita asada, ragú especiado de carne molida de res con toque de canela y orégano, y cobertura gratinada de queso ricotta y queso manchego.",
            thermo="Cocción del ragú a 75°C y horneado en capas a 185°C por 12 minutos.",
            flavor="Perfume cálido del Egeo con canela, orégano, carne de res y gratinado de ricotta y manchego.",
            texture="Capas tiernas de calabacita y ragú bajo costra dorada.",
            ccp="Asar previamente las láminas de calabacita para evitar humedad excesiva en la Moussaka.",
            archetype="res_moussaka_griega_horno",
            ingredients=[
                _ing("Carne molida", 600, "g", CAT_PROT),
                _ing("Calabacitas", 480, "g", CAT_VEG),
                _ing("Queso ricotta", 240, "g", CAT_DAIRY),
                _ing("Queso manchego", 100, "g", CAT_DAIRY),
                _ing("Cebolla", 1, "piezas", CAT_VEG),
                _ing("Canela molida", 3, "g", CAT_SPICE),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Asar las calabacitas en láminas longitudinales y cocinar el ragú de carne molida con cebolla, canela molida, orégano y sal de mar.",
                "Armar capas alternadas de calabacita y ragú, cubrir con mezcla de queso ricotta y queso manchego, y gratinar al horno.",
            ],
        ),
        side=_course(
            title="Champiñones Silvestres Salteados al Ajillo con Tomillo, Limón Real y Aceite de Oliva VEVO",
            technique="garlic_thyme_sauteed_mushrooms",
            note="Séptima guarnición de Comida ([R4-SIDE] 7/7: champiñón) libre de mantequilla y lácteos ([R2]).",
            thermo="Salteado a 180°C en aceite de oliva por 5 minutos.",
            flavor="Champiñones al ajillo y tomillo con toque de limón real.",
            texture="Láminas carnosas y doradas.",
            ccp="Cero mantequilla ni lácteos ([R2]).",
            ingredients=[
                _ing("Champiñón", 660, "g", CAT_VEG),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Filetear los champiñones y saltear a fuego vivo en aceite de oliva con sal con ajo y tomillo.",
                "Terminar con jugo de limón de la granja.",
            ],
        ),
    )

    d6_d = _meal(
        "Cena", "20:00", 51.0, 35.0, 3.9, 6.1,
        starter=_course(
            title="Caldo Claro de la Trattoria de Fondo de Pollo con Hojas de Espinacas, Limón Real y Orégano",
            technique="trattoria_spinach_clear_broth",
            note="Caldo italiano ligero con hojas de espinaca y limón real.",
            thermo="Cocción suave a 90°C por 4 minutos.",
            flavor="Fondo claro de pollo con espinacas tiernas y orégano.",
            texture="Caldo sedoso con hojas de espinaca.",
            ccp="Incorporar las espinacas 1 minuto antes de servir.",
            ingredients=[
                _ing("Fondo claro de pollo", 900, "ml", CAT_SPICE),
                _ing("Espinacas", 300, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal de mar", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Hervir el fondo claro de pollo con orégano y sal de mar, e incorporar las hojas de espinaca por 1 minuto.",
                "Servir con jugo de limón real y aceite de oliva.",
            ],
        ),
        main=_course(
            title="Shawarma Griego de Fajitas de Pechuga de Pollo Maridado al Limón Real, Comino y Orégano con Salsa Tzatziki de Yogur Griego y Pepino",
            technique="greek_chicken_shawarma_tzatziki",
            note="Escuela 7 (Mare Nostrum — Islas Griegas): fajitas de pechuga de pollo marinadas al limón real, comino y orégano doradas a la plancha, servidas con salsa Tzatziki fría de yogur griego y pepino.",
            thermo="Sellado a la plancha a 180°C hasta 74°C internos y salsa Tzatziki a 8°C.",
            flavor="Especias mediterráneas (comino, orégano y limón) con la acidez láctea del Tzatziki de pepino.",
            texture="Tiras doradas de ave sobre crema fría de yogur griego y pepino.",
            ccp="Drenar el pepino rallado antes de integrarlo al yogur griego.",
            archetype="pavo_shawarma_griego_tzatziki",
            ingredients=[
                _ing("Pechuga de pollo", 900, "g", CAT_PROT),
                _ing("Yogur griego", 360, "g", CAT_DAIRY),
                _ing("Pepino", 360, "g", CAT_VEG),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("Comino", 3, "g", CAT_SPICE),
                _ing("Orégano", 3, "g", CAT_SPICE),
                _ing("Aceite de oliva", 18, "ml", CAT_FAT),
                _ing("Sal con ajo", 6, "g", CAT_SPICE),
            ],
            steps=[
                "Marinar las fajitas de pechuga de pollo con jugo de limón real, comino, orégano, sal con ajo y aceite de oliva, y asar en plancha caliente.",
                "Mezclar el yogur griego con el pepino en dados finos y servir acompañando el shawarma caliente.",
            ],
        ),
        side=_course(
            title="Tisana Nocturna de Manzanilla, Tomillo y Limón Real (≤60°C) con Fórmula Reparadora 34Plus®",
            technique="chamomile_thyme_night_infusion",
            note="Séptima tisana nocturna con la Toma 3 de AminoSinergix®.",
            thermo="Infusión templada a ≤60°C.",
            flavor="Manzanilla floral con tomillo y limón de la granja.",
            texture="Infusión cálida.",
            ccp="Disolver AminoSinergix® a ≤60°C.",
            ingredients=[
                _ing("Manzanilla", 6, "g", CAT_SPICE),
                _ing("Tomillo", 3, "g", CAT_SPICE),
                _ing("Limones", 48, "g", CAT_VEG),
                _ing("AminoSinergix®", 30, "g", CAT_SUPP),
                _ing("Agua purificada", 1200, "ml", CAT_SPICE),
            ],
            steps=[
                "Infusionar la manzanilla y el tomillo en agua purificada a 85°C por 5 minutos y colar.",
                "Templar a 58°C, añadir jugo de limón real y disolver AminoSinergix® (34Plus®).",
            ],
        ),
    )

    base_meals_by_school = [
        [d0_b, d0_l, d0_d],  # Escuela 1: Nizú
        [d1_b, d1_l, d1_d],  # Escuela 2: IHOP
        [d2_b, d2_l, d2_d],  # Escuela 3: El Teapaneco
        [d3_b, d3_l, d3_d],  # Escuela 4: Asador Castellano
        [d4_b, d4_l, d4_d],  # Escuela 5: Alda Café
        [d5_b, d5_l, d5_d],  # Escuela 6: Pacífico & Oriente
        [d6_b, d6_l, d6_d],  # Escuela 7: Mare Nostrum
    ]

    school_keys = list(SEVEN_CULINARY_SCHOOLS.keys())
    for idx, d_meta in enumerate(day_entries):
        d_obj = copy.deepcopy(d_meta)
        s_key = school_keys[idx % 7]
        d_obj["culinary_school_id"] = s_key
        d_obj["culinary_school_name"] = SEVEN_CULINARY_SCHOOLS[s_key]["name"]
        d_obj["meals"] = copy.deepcopy(base_meals_by_school[idx])
        days_out.append(d_obj)

    return days_out


def export_heptagon_exchange_pool() -> Dict[str, List[Dict[str, Any]]]:
    """
    Exporta el banco de platillos del Heptágono Culinario T.I.L.O.® (7 Escuelas)
    en el formato exacto de `window.DISH_EXCHANGE_POOL` (`starters`, `mains`, `sides`)
    para los modales interactivos '✨ Negociar Platillo' y '🎲 ¡Sorpréndeme!'.
    """
    meta = compute_week_dates(45)
    heptagon_days = _build_heptagon_cycle_a_days(meta["day_entries"], 45)
    starters: List[Dict[str, Any]] = []
    mains: List[Dict[str, Any]] = []
    sides: List[Dict[str, Any]] = []

    for d_obj in heptagon_days:
        s_name = d_obj.get("culinary_school_name", "")
        for meal in d_obj.get("meals", []):
            mtype = meal.get("meal_type", "Comida")
            st = meal.get("starter") or {}
            mn = meal.get("main") or {}
            sd = meal.get("side") or {}
            if st.get("title"):
                starters.append({
                    "name": st["title"],
                    "category": "starter",
                    "meal_type": mtype,
                    "culinary_school": s_name,
                    "macros": {"kcal": 65.0, "fat_g": 4.5, "protein_g": 2.0, "net_carbs_g": 1.5},
                    "recipe": st,
                })
            if mn.get("title"):
                mains.append({
                    "name": mn["title"],
                    "category": "main",
                    "meal_type": mtype,
                    "culinary_school": s_name,
                    "archetype": mn.get("archetype", ""),
                    "macros": {"kcal": 340.0, "fat_g": 24.0, "protein_g": 28.0, "net_carbs_g": 1.8},
                    "recipe": mn,
                })
            if sd.get("title"):
                sides.append({
                    "name": sd["title"],
                    "category": "side",
                    "meal_type": mtype,
                    "culinary_school": s_name,
                    "macros": {"kcal": 55.0, "fat_g": 3.0, "protein_g": 1.0, "net_carbs_g": 0.8},
                    "recipe": sd,
                })
    return {"starters": starters, "mains": mains, "sides": sides}


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
    - Para `target_week == 44`: Retorna el plan maestro congelado de la Semana 44 (`Ciclo D`),
      respetando la instrucción de no tocar la Semana 44 en curso.
    - Para `target_week >= 45`: Activa el Córtex del Heptágono Culinario T.I.L.O.® V17.0
      (7 Escuelas de Restaurante, 1 Escuela por día de la semana) y ejecuta la Compuerta
      Hard-Gate [R1]–[R12] garantizando 0% de repetición en ventanas móviles de 4 semanas.
    """
    from app.services.menu_hard_gate_auditor import S43_S44_HISTORICAL_PANTRY_STOCK, load_live_pantry_ssot

    if int(target_week) >= 45:
        live_ssot = load_live_pantry_ssot()
        harvest = farm_harvest if farm_harvest is not None else live_ssot["farm_harvest"]
        pantry = pantry_stock if pantry_stock is not None else live_ssot["auditor_pantry"]
    else:
        harvest = farm_harvest if farm_harvest is not None else DEFAULT_FARM_HARVEST
        pantry = pantry_stock if pantry_stock is not None else S43_S44_HISTORICAL_PANTRY_STOCK
    meta = compute_week_dates(target_week)
    cycle_id = get_cycle_id_for_week(target_week)

    if int(target_week) <= 44:
        days_list = _build_cycle_d_canonical_days(meta["day_entries"])
    elif int(target_week) % 2 == 1:
        days_list = _build_heptagon_cycle_a_days(meta["day_entries"], int(target_week))
    else:
        days_list = _build_cycle_d_canonical_days(meta["day_entries"])

    week_plan = {
        "week_name": meta["week_name"],
        "week_label": meta["week_label"],
        "week_start": meta["week_start"],
        "date_range": meta["date_range"],
        "diners_count": diners_count,
        "cycle_id": cycle_id,
        "heptagon_v17": int(target_week) >= 45,
        "culinary_schools": list(SEVEN_CULINARY_SCHOOLS.keys()) if int(target_week) >= 45 else [],
        "days": days_list,
        "selected_harvest": list(harvest),
    }

    prev_week = history_weeks[-1] if history_weeks else None
    report = assert_zero_violations(
        week_data=week_plan,
        pantry_stock=pantry,
        farm_harvest=harvest,
        enforce_pantry_overdraft=True,
        prev_week_data=prev_week,
    )
    week_plan["hard_gate_audit"] = report
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

