# -*- coding: utf-8 -*-
"""
Sincronizador Permanente de Inventario Real (SSOT) — Atelier Gastronómico T.I.L.O.®
====================================================================================
Cierra las 3 grietas de persistencia entre la UI del navegador (Chrome Local / GitHub Pages)
y el Córtex en Python (`tilo_menu_cortex.py` y `menu_hard_gate_auditor.py`):

1. Lectura en Caliente de Chrome Abierto (Win32 Shared Read + SSTable `.ldb` + WAL `.log`):
   - Copia los archivos `.ldb` y `.log` de `Local Storage\\leveldb` usando la API Win32
     `CreateFileW` con `FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE` (0x07) hacia
     un directorio temporal aislado para evitar `PermissionError` cuando Chrome está abierto.
   - Decodifica tanto bloques Snappy en tablas `.ldb` como registros en vivo del Write-Ahead
     Log (`.log`) antes de su compactación, extrayendo la llave de mayor número de secuencia
     (`seq`) para `nutriketo_app_state_v42_2_exact_units`.
2. Guardado Bidireccional desde FastAPI (`/api/pantry/save-ssot`) y Respaldo de 1 Clic:
   - Normaliza cualquier payload de la UI hacia `pantry_live_state.json` en la raíz del proyecto.
"""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from datetime import datetime
import json
import os
import shutil
import struct
import tempfile
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PANTRY_LIVE_STATE_PATH = os.path.join(PROJECT_ROOT, "pantry_live_state.json")

CHROME_LEVELDB_DIRS = [
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\leveldb"),
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Profile 1\Local Storage\leveldb"),
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Local Storage\leveldb"),
]

PROHIBITED_ITEMS: Dict[str, Tuple[str, str]] = {
    "Salsa BBQ": ("550 g", "Alta en azúcares libres y jarabe de maíz de alta fructosa; rompe cetosis."),
    "Leche evaporada": ("960 ml", "Alta concentración de lactosa y azúcares lácteos simples; rompe cetosis."),
    "Leche": ("960 ml", "Lactosa no cetogénica (~12g carbs netos por porción); eleva glucemia."),
    "Salsa cátsup": ("2600 g", "Elevado aporte de azúcar añadida y jarabe de fructosa; fuera de protocolo keto."),
    "Pulpa de arándano": ("3840 g", "Concentrado de fruta con azúcar añadida y alta fructosa; rompe cetosis."),
    "Cacahuate enchilado": ("1200 g", "Leguminosa proinflamatoria con aceites refinados y almidón en cobertura."),
    "Granola": ("100 g", "Mezcla de avena, miel y azúcares refinados; alto impacto insulínico."),
    "Harina de trigo": ("1500 g", "Cereal refinado con gluten y altísima carga amilácea; rompe cetosis."),
    "Harina para hot cakes": ("500 g", "Harina procesada con azúcares añadidos, dextrosa y leudantes glucémicos."),
    "Cerezas": ("260 g", "Fruta con alto contenido de fructosa y azúcares simples; proscrita en inducción keto."),
    "Miguelito": ("100 g", "Dulce en polvo compuesto por azúcar pura y chile; eleva glucosa de inmediato."),
    "Chamoy": ("300 ml", "Salsa agridulce ultraprocesada con azúcar, almidón y jarabe de maíz."),
    "Chocolate para cobertura": ("165 g", "Chocolate comercial con alto contenido de sacarosa y grasas vegetales hidrogenadas."),
    "Concentrado de caldo de pollo en polvo": ("250 g", "Sazonador industrial con maltodextrina, glutamato monosódico y almidones."),
    "Café colombiano": ("100 g", "Excluido de recetas culinarias por regla clínica [R3]."),
    "Vinagre balsámico": ("200 ml", "Vinagre con reducción de mosto concentrado en azúcares simples residuales."),
    "Jugo Maggi": ("200 ml", "Ultraprocesado con trigo hidrolizado, colorante caramelo y glutamato monosódico."),
    "Manteca de cerdo": ("0 g", "Derivado porcino proscrito por regla clínica [R3]."),
    "Tang": ("104 g", "Polvo industrial para bebidas con azúcar y aditivos sintéticos no cetogénicos."),
    "Harina Power Cakes": ("1000 g", "Mezcla para panqueques con carbohidratos de rápida absorción; fuera de cetosis."),
    "Hojuelas de avena": ("100 g", "Cereal alto en carbohidratos netos y almidones; rompe cetosis."),
    "Maíz palomero": ("100 g", "Grano de maíz entero con elevada carga glucémica amilácea."),
    "Lentejas": ("100 g", "Leguminosa alta en carbohidratos netos y lectinas; rompe cetosis."),
    "Quinoa": ("100 g", "Pseudocereal amiláceo con elevada carga de carbohidratos netos."),
    "Palomitas para microondas": ("600 g", "Maíz procesado con grasas de palma y carbohidratos de alto impacto glucémico."),
    "Saborizante para arroz": ("48 g", "Sazonador industrial con maltodextrina y almidones para cereales."),
    "Chile chipotle": ("1320 g", "Picante irritante de mucosa gástrica / Capsaicina (Excluido por Regla 3.4)."),
    "Frijol pinto": ("1 costal / bolsa institucional", "Almidón / Leguminosa fuera de protocolo cetogénico."),
    "Queso de cabra con arándano": ("350 g", "Cubierta de arándano azucarado; fuera de protocolo cetogénico estricto."),
}

CANONICAL_NAME_FIX: Dict[str, str] = {
    "Brocoli": "Brócoli",
}

V63_SAMS_NOV09_POST_S45_STOCK_OVERRIDES: Dict[str, Tuple[float, str]] = {
    # 1. Carnes, Pescados, Aves y Huevos (Saldo Real Post-S45 + Sam's Club 09 Nov 2026 Orden 1569462808300642304)
    "Flat steak": (2025.0, "g"),           # 0 g post-S45 + 2,025 g (TOP SIRLOIN 1080G + NEW YORK REB 945G)
    "Carne molida": (2875.0, "g"),         # 1,115 g post-S45 + 1,760 g (MM CARNE MOL 1760G)
    "Lomo de salmón": (1780.0, "g"),       # 380 g post-S45 + 1,400 g (MM LOMO SALM 1400G)
    "Fajitas de mojarra": (2720.0, "g"),   # 0 g post-S45 + 2,720 g (2 × MM TILA 1.36)
    "Pechuga de pavo": (1633.3, "g"),      # 233.3 g post-S45 + 1,400 g (FAJITAS PAVO)
    "Huevo": (224.0, "piezas"),            # 44 pzas post-S45 + 180 pzas (180 HUE BLA)
    "Pechuga de pollo": (313.3, "g"),      # Saldo real post-S45
    "Pollo entero": (0.0, "piezas"),       # Saldo real post-S45
    "Atún en agua": (40.0, "g"),           # Saldo real post-S45
    "Sardinas": (0.0, "g"),                # Saldo real post-S45
    "Filete de atún": (0.0, "g"),
    # 2. Lácteos, Quesos y Mantequilla
    "Queso manchego": (1130.0, "g"),       # 130 g post-S45 + 1,000 g (QSO MANCH RA)
    "Queso cottage": (4840.0, "g"),        # 1,960 g post-S45 + 2,880 g (3 × 960GR QCOTTA)
    "Yogur griego": (3640.0, "g"),         # 1,840 g post-S45 + 1,800 g (OIKOS PROT 2)
    "Mantequilla": (1208.0, "g"),          # 128 g post-S45 + 1,080 g (12/90 MANTEQ)
    "Queso Philadelphia": (260.0, "g"),    # Saldo real post-S45
    "Queso doble crema": (140.0, "g"),     # Saldo real post-S45
    "Queso mozzarella": (0.0, "g"),        # Saldo real post-S45
    "Queso parmesano": (0.0, "g"),         # Saldo real post-S45
    "Queso ricotta": (0.0, "g"),           # Saldo real post-S45
    "Queso de cabra": (0.0, "g"),
    "Crema ácida": (920.0, "g"),           # Saldo real post-S45
    "Leche de coco": (0.0, "ml"),          # Saldo real post-S45
    # 3. Frutos Secos, Frutas y Hortalizas Frescas
    "Nuez de la India": (2062.0, "g"),     # 1,154 g post-S45 + 908 g (MM NUEZ INDI)
    "Semillas y nueces mixtas": (1108.0, "g"),  # 200 g post-S45 + 908 g (MIX NUEZ MM)
    "Nueces mixtas": (1108.0, "g"),
    "Fresas": (1821.0, "g"),               # 7 g post-S45 + 1,814 g (2 × FRESA 907g)
    "Frambuesas": (340.0, "g"),            # 0 g post-S45 + 340 g (FRAMBUESA)
    "Zarzamora": (170.0, "g"),             # Saldo real post-S45
    "Espinacas": (454.0, "g"),             # 0 g post-S45 + 454 g (ESPINACA BAB)
    "Champiñón": (866.7, "g"),             # 166.7 g post-S45 + 700 g (CHAMPINON BL)
    "Lechuga": (4.0, "piezas"),            # 0 pzas post-S45 + 4 pzas (LECHUGA SWEE)
    "Germinado": (640.0, "g"),             # 140 g post-S45 + 500 g (GERMINADO)
    "Botella de agua": (270.0, "botellas (355 ml)"),  # 150 + 120 (3 × MM 40/355ML)
    # 4. Resto de Saldos Reales Post-S45 en Alacena y Refrigerador
    "Calabacitas": (93.3, "g"),
    "Ejotes": (80.0, "g"),
    "Jitomate": (0.0, "piezas"),
    "Tomate": (200.0, "g"),
    "Cebolla": (1.0, "piezas"),
    "Morrón": (0.0, "piezas"),
    "Aguacate": (0.0, "piezas"),
    "Brócoli": (0.0, "g"),
    "Coliflor": (0.0, "g"),
    "Pepino": (0.0, "g"),
    "Espárragos": (0.0, "g"),
    "Aceite de coco": (1328.0, "g"),
    "Aceite de oliva": (118.0, "ml"),
    "Almendras fileteadas": (100.0, "g"),
    "Pistaches": (0.0, "g"),
    "Aceitunas manzanilla": (5.0, "g"),
    "Alcaparras": (44.0, "g"),
    "Achiote": (92.0, "g"),
    "Ajo": (7.0, "g"),
    "Canela molida": (725.0, "g"),
    "Clavo de olor": (48.0, "g"),
    "Comino": (47.0, "g"),
    "Cúrcuma": (82.0, "g"),
    "Extracto de vainilla": (376.0, "ml"),
    "Grenetina": (32.0, "g"),
    "Hierbas finas": (13.0, "g"),
    "Hojas de laurel": (0.0, "g"),
    "Manzanilla": (12.0, "g"),
    "Mostaza": (0.0, "g"),
    "Orégano": (98.0, "g"),
    "Pimienta negra": (124.0, "g"),
    "Sal con ajo": (52.0, "g"),
    "Sal de mar": (2810.0, "g"),
    "Té chai": (38.0, "g"),
    "Tomillo": (8.0, "g"),
    "MultiSinergix®": (0.0, "g"),
    "AminoSinergix®": (0.0, "g"),
}
V58_SAMS_COSTCO_TICKETS_STOCK_OVERRIDES = V63_SAMS_NOV09_POST_S45_STOCK_OVERRIDES


def _win32_shared_read_bytes(src_path: str) -> bytes:
    """
    Lee cualquier archivo `.ldb` o `.log` bloqueado por Google Chrome en Windows
    abriendo el descriptor con `FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE`.
    """
    if os.name != "nt":
        with open(src_path, "rb") as f:
            return f.read()

    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    kernel32 = ctypes.windll.kernel32
    kernel32.CreateFileW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ]
    kernel32.CreateFileW.restype = wintypes.HANDLE

    handle = kernel32.CreateFileW(
        src_path,
        GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None,
    )
    if handle == INVALID_HANDLE_VALUE or handle is None:
        with open(src_path, "rb") as f:
            return f.read()

    try:
        chunks: List[bytes] = []
        buf = ctypes.create_string_buffer(65536)
        bytes_read = wintypes.DWORD(0)
        while True:
            ok = kernel32.ReadFile(handle, buf, 65536, ctypes.byref(bytes_read), None)
            if not ok or bytes_read.value == 0:
                break
            chunks.append(buf.raw[: bytes_read.value])
        return b"".join(chunks)
    finally:
        kernel32.CloseHandle(handle)


def _read_varint(buf: bytes, pos: int) -> Tuple[int, int]:
    res = 0
    shift = 0
    while pos < len(buf):
        b = buf[pos]
        pos += 1
        res |= (b & 0x7F) << shift
        if not (b & 0x80):
            return res, pos
        shift += 7
    return res, pos


def _snappy_decompress(data: bytes) -> bytes:
    _, pos = _read_varint(data, 0)
    out = bytearray()
    while pos < len(data):
        tag = data[pos]
        pos += 1
        elem_type = tag & 0x03
        if elem_type == 0:
            length = (tag >> 2) + 1
            if length > 60:
                extra_bytes = length - 60
                length = int.from_bytes(data[pos : pos + extra_bytes], "little") + 1
                pos += extra_bytes
            out.extend(data[pos : pos + length])
            pos += length
        elif elem_type == 1:
            length = ((tag >> 2) & 0x07) + 4
            offset = ((tag & 0xE0) << 3) | data[pos]
            pos += 1
            for _ in range(length):
                out.append(out[-offset])
        elif elem_type == 2:
            length = (tag >> 2) + 1
            offset = int.from_bytes(data[pos : pos + 2], "little")
            pos += 2
            for _ in range(length):
                out.append(out[-offset])
        elif elem_type == 3:
            length = (tag >> 2) + 1
            offset = int.from_bytes(data[pos : pos + 4], "little")
            pos += 4
            for _ in range(length):
                out.append(out[-offset])
    return bytes(out)


def _decode_chrome_ls_value(val: bytes) -> str:
    if not val:
        return ""
    if val[0] == 0:
        return val[1:].decode("utf-16le", errors="ignore")
    if val[0] == 1:
        return val[1:].decode("latin1", errors="ignore")
    return val.decode("utf-8", errors="ignore")


def _parse_sstable_bytes(data: bytes) -> List[Tuple[int, str, str]]:
    """Extrae tuplas `(seq, key_str, val_str)` desde un archivo SSTable `.ldb`."""
    results: List[Tuple[int, str, str]] = []
    if len(data) < 48:
        return results
    footer = data[-48:]
    if footer[40:] != b"\x57\xfb\x80\x8b\x24\x75\x47\xdb":
        return results
    pos = 0
    _, pos = _read_varint(footer, pos)
    _, pos = _read_varint(footer, pos)
    index_off, pos = _read_varint(footer, pos)
    index_size, pos = _read_varint(footer, pos)

    idx_block = data[index_off : index_off + index_size]
    if data[index_off + index_size] == 1:
        idx_block = _snappy_decompress(idx_block)

    num_restarts = struct.unpack("<I", idx_block[-4:])[0]
    limit = len(idx_block) - 4 * (num_restarts + 1)
    p = 0
    last_key = b""
    handles: List[Tuple[int, int]] = []
    while p < limit:
        shared, p = _read_varint(idx_block, p)
        non_shared, p = _read_varint(idx_block, p)
        val_len, p = _read_varint(idx_block, p)
        key = last_key[:shared] + idx_block[p : p + non_shared]
        p += non_shared
        val = idx_block[p : p + val_len]
        p += val_len
        last_key = key
        vp = 0
        b_off, vp = _read_varint(val, vp)
        b_size, vp = _read_varint(val, vp)
        handles.append((b_off, b_size))

    for b_off, b_size in handles:
        block = data[b_off : b_off + b_size]
        ctype = data[b_off + b_size]
        if ctype == 1:
            try:
                block = _snappy_decompress(block)
            except Exception:
                continue
        if len(block) < 4:
            continue
        nr = struct.unpack("<I", block[-4:])[0]
        blimit = len(block) - 4 * (nr + 1)
        bp = 0
        lkey = b""
        while bp < blimit:
            sh, bp = _read_varint(block, bp)
            nsh, bp = _read_varint(block, bp)
            vlen, bp = _read_varint(block, bp)
            k = lkey[:sh] + block[bp : bp + nsh]
            bp += nsh
            v = block[bp : bp + vlen]
            bp += vlen
            lkey = k
            if b"nutriketo" in k and len(k) >= 8:
                user_key = k[:-8]
                tag = struct.unpack("<Q", k[-8:])[0]
                seq = tag >> 8
                vtype = tag & 0xFF
                if vtype == 1:
                    val_str = _decode_chrome_ls_value(v)
                    results.append((seq, user_key.decode("utf-8", errors="ignore"), val_str))
    return results


def _parse_wal_log_bytes(data: bytes) -> List[Tuple[int, str, str]]:
    """
    Decodifica bloques de 32KB del Write-Ahead Log (`.log`) de LevelDB para capturar
    escrituras recientes en Chrome que aún están en caché/WAL antes de compactarse a `.ldb`.
    """
    results: List[Tuple[int, str, str]] = []
    BLOCK_SIZE = 32768
    pos = 0
    fragment = bytearray()

    while pos < len(data):
        block_rem = BLOCK_SIZE - (pos % BLOCK_SIZE)
        if block_rem < 7:
            pos += block_rem
            continue
        if pos + 7 > len(data):
            break
        _, length, rtype = struct.unpack("<IHB", data[pos : pos + 7])
        pos += 7
        if length > len(data) - pos:
            break
        chunk = data[pos : pos + length]
        pos += length

        if rtype == 1:  # FULL
            record = bytes(chunk)
        elif rtype == 2:  # FIRST
            fragment = bytearray(chunk)
            continue
        elif rtype == 3:  # MIDDLE
            fragment.extend(chunk)
            continue
        elif rtype == 4:  # LAST
            fragment.extend(chunk)
            record = bytes(fragment)
            fragment.clear()
        else:
            continue

        if len(record) < 12:
            continue
        base_seq = struct.unpack("<Q", record[:8])[0]
        count = struct.unpack("<I", record[8:12])[0]
        rp = 12
        for idx in range(count):
            if rp >= len(record):
                break
            vtype = record[rp]
            rp += 1
            klen, rp = _read_varint(record, rp)
            k = record[rp : rp + klen]
            rp += klen
            if vtype == 1:
                vlen, rp = _read_varint(record, rp)
                v = record[rp : rp + vlen]
                rp += vlen
                if b"nutriketo" in k:
                    val_str = _decode_chrome_ls_value(v)
                    results.append((base_seq + idx, k.decode("utf-8", errors="ignore"), val_str))
    return results


def extract_latest_chrome_nutriketo_state() -> Optional[Dict[str, Any]]:
    """
    Copia en modo lectura compartida (`FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE`)
    los archivos `.ldb` y `.log` del perfil de Chrome a una carpeta temporal, extrae todos los
    snapshots de `nutriketo_app_state_v42_2_exact_units` y retorna el de mayor número de secuencia.
    """
    candidates: List[Tuple[int, str, str, Dict[str, Any]]] = []

    for leveldb_dir in CHROME_LEVELDB_DIRS:
        if not os.path.isdir(leveldb_dir):
            continue
        temp_dir = tempfile.mkdtemp(prefix="tilo_chrome_ls_")
        try:
            for fname in os.listdir(leveldb_dir):
                if not (fname.endswith(".ldb") or fname.endswith(".log")):
                    continue
                src_path = os.path.join(leveldb_dir, fname)
                dst_path = os.path.join(temp_dir, fname)
                try:
                    raw = _win32_shared_read_bytes(src_path)
                    with open(dst_path, "wb") as f:
                        f.write(raw)
                except Exception:
                    continue

            for fname in sorted(os.listdir(temp_dir)):
                fpath = os.path.join(temp_dir, fname)
                try:
                    with open(fpath, "rb") as f:
                        raw = f.read()
                except Exception:
                    continue
                records = _parse_sstable_bytes(raw) if fname.endswith(".ldb") else _parse_wal_log_bytes(raw)
                for seq, key_str, val_str in records:
                    if "nutriketo_app_state_v42_2_exact_units" not in key_str:
                        continue
                    try:
                        parsed = json.loads(val_str)
                        if isinstance(parsed, dict) and "pantryStock" in parsed:
                            candidates.append((seq, fname, key_str, parsed))
                    except Exception:
                        continue
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0], reverse=True)
    max_seq = candidates[0][0]
    best_seq, best_file, best_key, best_state = candidates[0]

    # Si el registro más alto es `270423` (el reset automático de v55 cuando el usuario refrescó github.io),
    # recuperar la captura manual real del usuario en `015745.ldb` (`seq=270082`, con `Pechuga de pavo == 1400`
    # y `Flat steak == 0`), guardando `max_seq` como marca de agua para que cualquier edición posterior (> 270423) gane.
    if max_seq <= 270423:
        for seq, fname, key_str, state in candidates:
            ps = state.get("pantryStock") or {}
            if ps.get("Pechuga de pavo") == 1400 and ps.get("Flat steak") == 0:
                best_seq, best_file, best_key, best_state = max_seq, fname, key_str, state
                break

    origin = best_key.split("\x00")[0].lstrip("_")
    return {
        "leveldb_seq": best_seq,
        "leveldb_file": best_file,
        "origin": origin,
        "state": best_state,
    }


def build_ssot_document_from_ui_state(
    ui_state: Dict[str, Any],
    source_meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Transforma el estado de la UI (`pantryStock`, `pantryCardUnits`, `selectedHarvest`,
    `deletedPantryItems`, `deletedFarmItems`) en el documento canónico `pantry_live_state.json`.
    """
    raw_ps = ui_state.get("pantryStock", {})
    raw_pcu = ui_state.get("pantryCardUnits", {})

    canonical_pantry_for_auditor: Dict[str, List[Any]] = {}
    ui_pantry_stock: Dict[str, Any] = {}
    ui_pantry_units: Dict[str, str] = {}

    for k, val in raw_ps.items():
        if k in ("Fondo claro de pollo", "Fondo de res", "Caldo de pollo", "Caldo de res"):
            continue
        c_name = CANONICAL_NAME_FIX.get(k, k)
        if isinstance(val, dict):
            qty = float(val.get("qty", 0.0))
            u = str(val.get("unit", raw_pcu.get(k, "g")))
        elif isinstance(val, (list, tuple)) and len(val) >= 2:
            qty = float(val[0])
            u = str(val[1])
        else:
            qty = float(val) if isinstance(val, (int, float)) else 0.0
            u = str(raw_pcu.get(k, "g"))

        if c_name == "Queso de cabra":
            qty = 0.0
        if c_name == "Coliflor" and u == "kg" and qty == 500.0:
            u = "g"
        if c_name == "Aceite de coco":
            u = "g"

        ui_pantry_stock[c_name] = qty if qty != int(qty) else int(qty)
        ui_pantry_units[c_name] = u

        if c_name not in PROHIBITED_ITEMS:
            if c_name in ("Sardinas", "Sardinas en tomate") and "lata" in u.lower():
                aud_qty = qty * 425.0
                aud_unit = "g"
            elif c_name == "Champiñón" and qty < 1.0:
                aud_qty = 0.0
                aud_unit = "g"
            else:
                aud_qty = qty
                aud_unit = u
            canonical_pantry_for_auditor[c_name] = [aud_qty, aud_unit]

    meta = source_meta or {}
    if not ui_state.get("v63_sams_09nov2026_post_s45_sync"):
        for t_name, (t_qty, t_unit) in V63_SAMS_NOV09_POST_S45_STOCK_OVERRIDES.items():
            ui_pantry_stock[t_name] = int(t_qty) if t_qty == int(t_qty) else t_qty
            ui_pantry_units[t_name] = t_unit
            canonical_pantry_for_auditor[t_name] = [float(t_qty), t_unit]

    ui_pantry_stock["Queso de cabra con arándano"] = 350
    ui_pantry_units["Queso de cabra con arándano"] = "g"

    del_pantry = list(dict.fromkeys(
        ui_state.get("deletedPantryItems", ["Elote", "Higos", "Nogada", "Zanahoria", "Agua mineral"])
        + ["Agua mineral"]
    ))

    return {
        "ssot_version": "v63_sams_09nov2026_post_s45_synced",
        "v63_sams_09nov2026_post_s45_sync": True,
        "sams_ticket_order": "1569462808300642304",
        "sams_ticket_date": "2026-11-09",
        "sams_ticket_store": "Sam's Club SM Santa Fe",
        "sams_ticket_total_mxn": 5127.48,
        "extracted_from": meta.get(
            "extracted_from",
            "Saldo Real Post-S45 + Ticket Sam's Club SM Santa Fe 09 Nov 2026 (Orden 1569462808300642304 — $5,127.48 MXN)",
        ),
        "leveldb_seq": int(meta.get("leveldb_seq", 274828)),
        "updated_at": datetime.now().isoformat(),
        "activeWeek": "Semana 46 (08 al 14 de Noviembre de 2026)",
        "activeDiners": ui_state.get("activeDiners", 6),
        "selectedHarvest": list(dict.fromkeys(ui_state.get(
            "selectedHarvest",
            ["Nopales", "Cilantro", "Limones", "Nuez pecana", "Acelgas", "Romero", "Agua purificada", "Jamaica", "Granadas"],
        ) + ["Granadas"])),
        "customFarmItems": ui_state.get("customFarmItems", []),
        "deletedFarmItems": ui_state.get(
            "deletedFarmItems",
            [
                "Zarzamoras",
                "Frambuesas",
                "Fresas",
                "Menta",
                "Arándanos",
                "Epazote",
                "Calabacitas",
                "Coliflor",
                "Espinacas",
                "Ejotes",
                "Espárragos",
                "Arúgula",
                "Brócoli",
            ],
        ),
        "deletedPantryItems": del_pantry,
        "pantryStock": ui_pantry_stock,
        "pantryCardUnits": ui_pantry_units,
        "auditorPantryStock": canonical_pantry_for_auditor,
        "quarantineItems": {
            k: {
                "packaging": v[0],
                "reason": v[1],
                "stock": ui_pantry_stock.get(k, 0),
                "unit": ui_pantry_units.get(k, "g"),
            }
            for k, v in PROHIBITED_ITEMS.items()
        },
        "dispatchedMeals": ui_state.get("dispatchedMeals", {}),
        "mealDinersState": ui_state.get(
            "mealDinersState",
            {
                "Semana 45 (01 al 07 de Noviembre de 2026)_day_0_Desayuno": 6,
                "Semana 45 (01 al 07 de Noviembre de 2026)_day_0_Comida": 4,
                "Semana 45 (01 al 07 de Noviembre de 2026)_day_0_Cena": 2,
            },
        ),
    }


def sync_pantry_ssot_from_chrome(force: bool = False) -> Optional[Dict[str, Any]]:
    """
    Sincroniza `pantry_live_state.json` desde el perfil de Chrome local si:
      - `pantry_live_state.json` aún no existe, o
      - `force=True`, o
      - El número de secuencia (`leveldb_seq`) en Chrome es mayor que el registrado en disco.
    """
    existing: Optional[Dict[str, Any]] = None
    if os.path.exists(PANTRY_LIVE_STATE_PATH):
        try:
            with open(PANTRY_LIVE_STATE_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = None

    extracted = extract_latest_chrome_nutriketo_state()
    if not extracted:
        return existing

    existing_seq = int((existing or {}).get("leveldb_seq", 270423) or 270423)
    new_seq = int(extracted.get("leveldb_seq", 0) or 0)
    existing_is_v63 = bool((existing or {}).get("v63_sams_09nov2026_post_s45_sync"))
    chrome_is_v63 = bool((extracted.get("state") or {}).get("v63_sams_09nov2026_post_s45_sync"))

    # No permitir que un estado antiguo de Chrome previo a V63 sobrescriba el alta de Sam's Club 09 Nov 2026
    if existing_is_v63 and not chrome_is_v63 and not force:
        return existing

    if existing is None or force or new_seq > existing_seq:
        doc = build_ssot_document_from_ui_state(
            extracted["state"],
            source_meta={
                "extracted_from": f"Google Chrome LocalStorage LevelDB ({extracted['leveldb_file']}, seq={new_seq})",
                "leveldb_seq": new_seq,
            },
        )
        with open(PANTRY_LIVE_STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        return doc

    return existing
