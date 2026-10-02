# -*- coding: utf-8 -*-
"""
Datos Maestros Canónicos para la Semana 41 (04 al 10 de Octubre de 2026)
Ecosistema NutriKeto Atelier T.I.L.O.®
7 Días, 21 Servicios, 63 Platillos, Arquitectura Culinaria COCT y Métricas SSOT.
"""

from scratch.s41_days_dom_lun import get_domingo_lunes
from scratch.s41_days_mar_mie import get_martes_miercoles
from scratch.s41_days_jue_vie_sab import get_jueves_viernes_sabado

def get_semana_41_data():
    all_days = []
    all_days.extend(get_domingo_lunes())
    all_days.extend(get_martes_miercoles())
    all_days.extend(get_jueves_viernes_sabado())
    
    return {
        "diners_count": 6,
        "week_name": "Semana 41",
        "week_label": "Semana 41 (04 al 10 de Octubre de 2026)",
        "week_start": "2026-10-04",
        "date_range": "04 al 10 de Octubre de 2026",
        "days": all_days
    }
