# -*- coding: utf-8 -*-
"""
Compilador Canónico del Expediente Clínico y Gastronómico Integral — Semana 46 (08 al 14 de Noviembre de 2026)
Sincronizado con `pantry_live_state.json` (Saldo Real Post-S45 + Ticket Sam's Club Santa Fe 09 Nov 2026, Orden 1569462808300642304).
"""
from app.services.s45_dossier_compiler import compile_s46_dossier

__all__ = ["compile_s46_dossier"]

if __name__ == "__main__":
    res = compile_s46_dossier()
    print(
        f"[OK] Compilado expediente_completo_semana_46.md ({res['lines_count']} líneas) "
        f"-> Cubiertos en Alacena: {len(res['bom_summary']['pantry_covered_items'])}, "
        f"Compras Mercado: {len(res['bom_summary']['market_purchases'])}"
    )
