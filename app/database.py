import sqlite3
import threading
from contextlib import contextmanager
from app.config import settings
from app.logger import logger

_db_lock = threading.RLock()

@contextmanager
def get_db():
    conn = None
    with _db_lock:
        try:
            conn = sqlite3.connect(
                settings.DATABASE_PATH,
                timeout=10.0,
                check_same_thread=False
            )
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA busy_timeout = 10000;")
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Error en transacción SQLite: {e}")
            raise e
        finally:
            if conn:
                conn.close()

def init_db():
    logger.info("Inicializando esquema de base de datos SQLite con tablas multivista...")
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pantry_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE NOT NULL,
            quantity REAL NOT NULL DEFAULT 0,
            unit TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week_start TEXT NOT NULL,
            diners_count INTEGER NOT NULL,
            plan_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            item_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS shopping_list_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            day TEXT DEFAULT 'Semanal',
            item_name TEXT NOT NULL,
            quantity REAL DEFAULT 1.0,
            unit TEXT DEFAULT 'unidad',
            is_checked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            recipe_id TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            math_matrix_json TEXT NOT NULL,
            steps_json TEXT NOT NULL,
            inventory_tags_json TEXT DEFAULT '[]',
            is_rescue_flag INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Seed Benchmark Portobello Recipe
        cursor.execute("SELECT recipe_id FROM recipes WHERE recipe_id = 'portobello_gouda_pavo'")
        if not cursor.fetchone():
            import json
            matrix = {
                "portobello_count": 2.0,
                "turkey_qty": 40.0,
                "gouda_qty": 30.0,
                "olive_oil_tbsp": 0.5
            }
            steps = [
                {
                    "step_number": 1,
                    "title": "Preparar los champiñones",
                    "instruction": "Limpia {portobello_count} champiñones Portobello suavemente con un paño húmedo (evita lavarlos bajo el chorro directo de agua para que no absorban humedad extra). Con mucho cuidado, retira los tallos y raspa ligeramente las láminas oscuras del interior con una cuchara para ganar espacio para el relleno. Acomoda los Portobello en una charola para horno previamente engrasada o con papel encerado, con el hueco hacia arriba. Sazona el interior con una pizca de sal, pimienta y {olive_oil_tbsp} cdas de aceite de oliva para {diners_count} personas."
                },
                {
                    "step_number": 2,
                    "title": "Saltear el relleno",
                    "instruction": "Calienta {olive_oil_tbsp} cdas de aceite de oliva en una sartén a fuego medio. Agrega la cebolla y el ajo picados; sofríe hasta que estén transparentes y aromáticos. Incorpora los cubitos o tiras de pavo ({turkey_qty} g). Sazona con un poco de hierbas provenzales, sal y pimienta. Saltea durante 3 a 4 minutos hasta que el pavo tome un ligero tono dorado. Retira del fuego."
                },
                {
                    "step_number": 3,
                    "title": "Rellenar los Portobello",
                    "instruction": "Rellena generosamente cada champiñón con la mezcla de pavo salteado, presionando ligeramente para que queden bien compactos. Cubre la superficie de cada uno con una capa abundante de queso Gouda rallado ({gouda_qty} g), asegurándote de que el relleno quede bien sellado por el queso."
                },
                {
                    "step_number": 4,
                    "title": "Hornear",
                    "instruction": "Precalienta tu horno a 190°C. Hornea los champiñones durante 15 a 20 minutos. El tiempo dependerá del tamaño del hongo; sabrás que están listos cuando el champiñón esté tierno y jugoso por dentro, y el queso de la superficie se haya fundido por completo, adquiriendo un tono dorado y burbujeante."
                },
                {
                    "step_number": 5,
                    "title": "Servir",
                    "instruction": "Retira del horno con cuidado y déjalos reposar un par de minutos antes de llevarlos a la mesa para {diners_count} comensales. Puedes acompañarlos con una ensalada fresca de hojas verdes."
                }
            ]
            cursor.execute(
                "INSERT INTO recipes (recipe_id, display_name, math_matrix_json, steps_json) VALUES (?, ?, ?, ?)",
                ("portobello_gouda_pavo", "Champiñones Portobello Rellenos de Queso Gouda y Jamón de Pavo al Horno", json.dumps(matrix), json.dumps(steps))
            )

        # Seed Pechuga Rellena Recipe
        cursor.execute("SELECT recipe_id FROM recipes WHERE recipe_id = 'pechuga_rellena_queso_crema_espinacas'")
        if not cursor.fetchone():
            import json
            p_matrix = {
                "chicken_breast_g": 180.0,
                "cream_cheese_g": 40.0,
                "spinach_g": 30.0,
                "parmesan_g": 15.0,
                "olive_oil_tbsp": 0.5
            }
            p_steps = [
                {
                    "step_number": 1,
                    "title": "Preparar el relleno cremoso",
                    "instruction": "En un tazón pequeño, mezcla {cream_cheese_g} g de queso crema con {spinach_g} g de espinacas picadas, ajo y {parmesan_g} g de queso parmesano. Sazona con una pizca de sal y pimienta. Reserva."
                },
                {
                    "step_number": 2,
                    "title": "Preparar las pechugas",
                    "instruction": "Haz un corte lateral en cada pechuga ({chicken_breast_g} g) para crear un \"bolsillo\" (cuidado de no cortar hasta el otro extremo para que el relleno no se salga). Salpimenta el interior y el exterior de las pechugas. Espolvorea un poco de pimentón por fuera para darles un color dorado apetitoso."
                },
                {
                    "step_number": 3,
                    "title": "Rellenar",
                    "instruction": "Introduce la mezcla de queso crema y espinacas dentro de cada bolsillo. Cierra las aperturas utilizando los palillos de madera, atravesándolos para sellar bien los bordes."
                },
                {
                    "step_number": 4,
                    "title": "Sellar en sartén (opcional pero recomendado)",
                    "instruction": "Calienta {olive_oil_tbsp} cdas de aceite de oliva en una sartén a fuego medio-alto. Dora las pechugas rellenas durante 2 minutos por lado hasta que tengan una costra dorada. Esto ayuda a sellar los jugos del pollo."
                },
                {
                    "step_number": 5,
                    "title": "Hornear",
                    "instruction": "Precalienta tu horno a 200°C. Coloca las pechugas en una bandeja para horno. Hornea durante 20 a 25 minutos o hasta que el pollo esté totalmente cocido por dentro (puedes verificar que el centro esté firme y los jugos salgan claros)."
                },
                {
                    "step_number": 6,
                    "title": "Reposo y servicio",
                    "instruction": "Retira del horno y deja reposar las pechugas 5 minutos antes de cortarlas para {diners_count} comensales. Esto es fundamental para que el relleno cremoso no se desparrame inmediatamente al abrir la pechuga. Retira los palillos antes de servir."
                }
            ]
            cursor.execute(
                "INSERT INTO recipes (recipe_id, display_name, math_matrix_json, steps_json) VALUES (?, ?, ?, ?)",
                ("pechuga_rellena_queso_crema_espinacas", "Pechuga de Pollo Rellena de Queso Crema y Espinacas al Horno", json.dumps(p_matrix), json.dumps(p_steps))
            )

    logger.info("Esquema SQLite inicializado con éxito.")
