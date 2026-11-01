# -*- coding: utf-8 -*-
"""
Datos Maestros Canónicos para la Semana 42 (11 al 17 de Octubre de 2026)
Ecosistema NutriKeto Atelier T.I.L.O.®
7 Días, 21 Servicios, 63 Platillos, Arquitectura Culinaria COCT y Métricas SSOT.
"""

from scratch.s42_days_dom_lun import get_domingo_lunes
from scratch.s42_days_mar_mie import get_martes_miercoles
from scratch.s42_days_jue_vie_sab import get_jueves_viernes_sabado

def get_semana_42_data():
    all_days = []
    all_days.extend(get_domingo_lunes())
    all_days.extend(get_martes_miercoles())
    all_days.extend(get_jueves_viernes_sabado())
    
    for d in all_days:
        for m in d.get("meals", []):
            if "main_dish" in m and "main" not in m:
                m["main"] = m["main_dish"]
            if "side_dish" in m and "side" not in m:
                m["side"] = m["side_dish"]

    return {
        "diners_count": 6,
        "week_name": "Semana 42",
        "week_label": "Semana 42 (11 al 17 de Octubre de 2026)",
        "week_start": "2026-10-11",
        "date_range": "11 al 17 de Octubre de 2026",
        "days": all_days
    }
