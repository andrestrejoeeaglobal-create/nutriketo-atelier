# -*- coding: utf-8 -*-
"""
Días Martes 13 Oct y Miércoles 14 Oct para Semana 42
Ecosistema NutriKeto Atelier T.I.L.O.®
Arquitectura COCT, Atwater y Gobernanza Bioquímica.
"""

def get_martes_miercoles():
    return [
        # -------------------------------------------------------------
        # MARTES 13 DE OCTUBRE DE 2026
        # -------------------------------------------------------------
        {
            "day": "Martes",
            "date_str": "13 Oct",
            "day_num": "13",
            "month": "Octubre",
            "full_date_title": "Martes 13 de Octubre de 2026",
            "iso_date": "2026-10-13",
            "meals": [
                {
                    "meal_type": "Desayuno",
                    "starter_name": "Tazón de Frambuesas Frescas con Nueces de Castilla y Chía",
                    "main_dish_name": "Omelette de Queso Panela Artesanal con Flor de Calabaza y Epazote",
                    "side_dish_name": "Gelatina Artesanal de Frambuesa Viva (4°C) con Fórmula Nootrópica 33Plus®",
                    "fat_g": 38.5,
                    "protein_g": 36.2,
                    "net_carbs_g": 5.1,
                    "starter": {
                        "title": "Tazón de Frambuesas Frescas con Nueces de Castilla y Chía",
                        "technique": "raw_assembly",
                        "note": "Frambuesas ricas en ácido elágico y cetonas naturales con nueces de Castilla cardiosaludables.",
                        "ingredients": [
                            {"name": "Frambuesas frescas", "amount": 300, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 50},
                            {"name": "Nueces de Castilla", "amount": 90, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 15},
                            {"name": "Semillas de chía orgánicas", "amount": 48, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 8}
                        ],
                        "steps": [
                            "1. Selección fría: Lavar y secar frambuesas a 4°C.",
                            "2. Tostado leve: Tostar nueces de Castilla a 120°C por 2 minutos; trocear toscamente.",
                            "3. Ensamble: Distribuir frambuesas, espolvorear chía y nuez crujiente."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble frío que protege la integridad celular del fruto.",
                            "flavor_and_aromatics": "Acidez vibrante con final graso y amaderado de nuez.",
                            "textural_architecture": "Pulpa tierna y semillas crujientes con crujido denso de nuez.",
                            "critical_control_points": "No humedecer las nueces antes de servir."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 8,
                        "texture_target": "Fresco y crujiente",
                        "service_notes": "Servir en cuencos refrigerados."
                    },
                    "main_dish": {
                        "title": "Omelette de Queso Panela Artesanal con Flor de Calabaza y Epazote",
                        "technique": "saute_and_sear",
                        "note": "3 huevos de pastoreo por comensal (Leucina ≥2.5 g) con flor de calabaza y queso panela asado.",
                        "ingredients": [
                            {"name": "Huevos orgánicos de pastoreo", "amount": 18, "unit": "piezas", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 3},
                            {"name": "Queso Panela artesanal", "amount": 180, "unit": "g", "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "per_guest": 30},
                            {"name": "Flor de calabaza", "amount": 120, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 20},
                            {"name": "Mantequilla de pastoreo", "amount": 70, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 11.6},
                            {"name": "Epazote fresco", "amount": 12, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 2},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Salteo aromático: Saltear la flor de calabaza limpia con epazote picado en 20 g de mantequilla durante 1 minuto.",
                            "2. Batido: Batir los 18 huevos con sal de mar suavemente.",
                            "3. Cuajado y relleno: Calentar sartén a 120°C con mantequilla; verter huevos y al cuajar la base colocar la flor de calabaza salteada y cubos de panela.",
                            "4. Cierre: Plegar el omelette en media luna y servir jugoso."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cocción suave (65°C) que mantiene la ternura de la flor de calabaza y suaviza la panela.",
                            "flavor_and_aromatics": "Aroma rústico de epazote que armoniza con la sutileza de la flor y la neutralidad del huevo.",
                            "textural_architecture": "Envoltura suave y esponjosa con corazón jugoso y cubos elásticos de panela.",
                            "critical_control_points": "Retirar pistilos amargos de la flor de calabaza."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla",
                        "service_temp_c": 66,
                        "texture_target": "Esponjoso, tierno y aromático",
                        "service_notes": "Servir en platos tibios."
                    },
                    "side_dish": {
                        "title": "Gelatina Artesanal de Frambuesa Viva (4°C) con Fórmula Nootrópica 33Plus®",
                        "technique": "gelatin_molding",
                        "note": "Suministro nootrópico matutino de colágeno hidrolizado y adaptógenos de 33Plus®.",
                        "ingredients": [
                            {"name": "Frambuesas frescas", "amount": 120, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 20},
                            {"name": "Grenetina natural en polvo", "amount": 42, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 7},
                            {"name": "Fórmula Nootrópica 33Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Puré y colado: Licuar frambuesas con agua purificada y colar semillas.",
                            "2. Gelatina: Hidratar la grenetina y disolver a 60°C.",
                            "3. Fusión templada: Enfriar a 39°C, integrar la Fórmula 33Plus® batiendo suavemente.",
                            "4. Cuajado: Moldear y refrigerar a 4°C por 4 horas."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Control estricto de temperatura antes de añadir 33Plus®.",
                            "flavor_and_aromatics": "Acidez refrescante y aromática.",
                            "textural_architecture": "Gel firme y tembloroso de disolución limpia.",
                            "critical_control_points": "No calentar después de añadir el suplemento."
                        },
                        "broth_volume_ml": 120,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 4,
                        "texture_target": "Fresco, firme y elástico",
                        "service_notes": "Servir en copas heladas."
                    }
                },
                {
                    "meal_type": "Comida",
                    "starter_name": "Consomé Clarificado de Pollo con Nopales Tiernos al Cilantro",
                    "main_dish_name": "Pechuga de Pollo Rellena de Queso Ricotta y Espinacas en Salsa Cremosa",
                    "side_dish_name": "Zoodles de Calabacita Verde al Sartén con Aceite de Oliva VEVO",
                    "fat_g": 52.0,
                    "protein_g": 49.5,
                    "net_carbs_g": 5.2,
                    "starter": {
                        "title": "Consomé Clarificado de Pollo con Nopales Tiernos al Cilantro",
                        "technique": "boil_and_blend",
                        "note": "Fondo límpido de ave enriquecido con nopales tiernos de la granja desprovistos de baba.",
                        "ingredients": [
                            {"name": "Fondo claro de pollo", "amount": 600, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 100},
                            {"name": "Nopales tiernos", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Cilantro fresco", "amount": 18, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3},
                            {"name": "Jugo de limón fresco", "amount": 20, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Cocción de nopales: Cortar nopales en bastones finos y cocer en agua hirviendo con sal durante 3 minutos; escurrir y enjuagar con agua fría para eliminar baba.",
                            "2. Calentado de fondo: Llevar el fondo de pollo a hervor suave a 88°C.",
                            "3. Ensamble: Incorporar los nopales escurridos al caldo caliente, apagar el fuego, añadir jugo de limón y cilantro picado."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Choque térmico en nopal para corte de mucílago y servicio a 70°C.",
                            "flavor_and_aromatics": "Fondo de pollo aromático con el toque cítrico del limón y cilantro.",
                            "textural_architecture": "Caldo límpido con nopales elásticos y carnosos sin viscosidad.",
                            "critical_control_points": "Lavar perfectamente los nopales antes de incorporarlos al consomé."
                        },
                        "broth_volume_ml": 100,
                        "deglaze_agent": "Fondo de pollo",
                        "service_temp_c": 70,
                        "texture_target": "Líquido aromático con verdura firme",
                        "service_notes": "Servir en cuencos hondos de loza."
                    },
                    "main_dish": {
                        "title": "Pechuga de Pollo Rellena de Queso Ricotta y Espinacas en Salsa Cremosa",
                        "technique": "saute_and_sear",
                        "note": "Pechuga de pollo orgánica rellena de Queso Ricotta (Sam's Club) y espinacas tiernas, sellada y horneada en salsa reducida de crema ácida.",
                        "ingredients": [
                            {"name": "Pechuga de pollo", "amount": 900, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 150},
                            {"name": "Queso Ricotta", "amount": 240, "unit": "g", "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "per_guest": 40},
                            {"name": "Espinacas frescas", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Crema ácida", "amount": 120, "unit": "g", "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "per_guest": 20},
                            {"name": "Mantequilla de pastoreo", "amount": 60, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Relleno cremoso: Saltear las espinacas en 15 g de mantequilla hasta reducir; picar finamente y mezclar con el queso ricotta, sal marina y pimienta.",
                            "2. Apertura y rellenado: Realizar un bolsillo longitudinal en cada suprema de pechuga de pollo; introducir el relleno cremoso y asegurar con palillo de bambú.",
                            "3. Sellado dorado: Calentar sartén amplia con el resto de la mantequilla a 160°C; sellar las pechugas rellenas durante 3 minutos por lado hasta dorar.",
                            "4. Cocción final y salsa: Bajar el fuego a 120°C, agregar la crema ácida de alacena y 50 ml de fondo de pollo; tapar y cocinar a fuego lento durante 8 minutos hasta que el centro alcance 74°C interno; retirar palillos y servir bañadas en su salsa emulsionada."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Sellado inicial para Maillard y cocción tapada en medio húmedo graso para evitar el secado de la fibra magra de la pechuga.",
                            "flavor_and_aromatics": "Sabor suntuoso lácteo del ricotta y la crema ácida realzando la jugosidad del pollo.",
                            "textural_architecture": "Fibra muscular tierna y jugosa con un corazón cremoso y sedoso de queso ricotta y espinaca.",
                            "critical_control_points": "Control estricto con termómetro a 74°C en el centro del ave."
                        },
                        "broth_volume_ml": 30,
                        "deglaze_agent": "Crema ácida y fondo de pollo",
                        "service_temp_c": 70,
                        "texture_target": "Jugoso, dorado y relleno cremoso",
                        "service_notes": "Cortar en rodajas gruesas mostrando el corte relleno al emplatar."
                    },
                    "side_dish": {
                        "title": "Zoodles de Calabacita Verde al Sartén con Aceite de Oliva VEVO",
                        "technique": "saute_and_sear",
                        "note": "Espaguetis de calabacita fresca de la huerta salteados al dente en aceite de oliva VEVO.",
                        "ingredients": [
                            {"name": "Calabacitas verdes tiernas", "amount": 480, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 80},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 40, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 6.6},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Espiralizado: Procesar las calabacitas en espiralizador formando zoodles continuos.",
                            "2. Salteo de 90 segundos: Calentar el aceite VEVO en sartén a 160°C; incorporar los zoodles y saltear a fuego máximo durante solo 90 segundos para que no suelten agua.",
                            "3. Pase: Sazonar con sal marina y servir inmediatamente."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Salteo ultracorto a fuego muy vivo que calienta el vegetal sin colapsar sus vacuolas celulares.",
                            "flavor_and_aromatics": "Dulzura fresca vegetal con el frutado intenso del aceite VEVO.",
                            "textural_architecture": "Hilos largos y flexibles con mordida al dente crujiente.",
                            "critical_control_points": "No salar antes del salteo para evitar exudación osmótica de agua."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Aceite VEVO",
                        "service_temp_c": 64,
                        "texture_target": "Al dente, turgente y satinado",
                        "service_notes": "Montar en nido al lado de la pechuga rellena."
                    }
                },
                {
                    "meal_type": "Cena",
                    "starter_name": "Bastones de Zucchini Fresco con Sal Marina y Limón",
                    "main_dish_name": "Filete de Robalo Fresco al Horno con Costra de Almendras y Eneldo",
                    "side_dish_name": "Infusión Nocturna de Menta y Toronjil con Fórmula 34Plus®",
                    "fat_g": 37.0,
                    "protein_g": 41.5,
                    "net_carbs_g": 3.4,
                    "starter": {
                        "title": "Bastones de Zucchini Fresco con Sal Marina y Limón",
                        "technique": "raw_assembly",
                        "note": "Apertura ligera e hidratante de fácil digestión nocturna.",
                        "ingredients": [
                            {"name": "Calabacitas verdes tiernas", "amount": 300, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 50},
                            {"name": "Jugo de limón fresco", "amount": 20, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Corte: Cortar las calabacitas tiernas en bastones uniformes de 5 cm.",
                            "2. Aliño: Rociar con jugo de limón y espolvorear sal marina al momento de servir."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble en frío para turgencia crocante.",
                            "flavor_and_aromatics": "Frescura crujiente vegetal con acidez viva.",
                            "textural_architecture": "Mordida turgente y acuosa.",
                            "critical_control_points": "Servir recién preparado."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 8,
                        "texture_target": "Crocante y fresco",
                        "service_notes": "Servir en platos pequeños refrigerados."
                    },
                    "main_dish": {
                        "title": "Filete de Robalo Fresco al Horno con Costra de Almendras y Eneldo",
                        "technique": "saute_and_sear",
                        "note": "Pescado blanco magro rico en fósforo y selenio horneado con mantequilla clarificada y almendras crujientes.",
                        "ingredients": [
                            {"name": "Filete de Robalo fresco", "amount": 900, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 150},
                            {"name": "Almendras fileteadas tostadas", "amount": 60, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10},
                            {"name": "Mantequilla de pastoreo", "amount": 60, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10},
                            {"name": "Eneldo fresco", "amount": 15, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 2.5},
                            {"name": "Jugo de limón fresco", "amount": 20, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Sazón de filetes: Colocar los filetes de robalo en bandeja para hornear barnizada con mantequilla; sazonar con sal de mar y eneldo picado.",
                            "2. Costra crocante: Presionar las almendras fileteadas sobre la cara superior de cada filete y bañar con mantequilla fundida.",
                            "3. Horneado suave: Hornear a 170°C durante 9 minutos hasta que las almendras doren y el pescado esté nacarado y tierno en su centro (58°C interno).",
                            "4. Pase: Terminar con unas gotas de jugo de limón fresco."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cocción al horno a 170°C con grasa protectora de mantequilla para evitar pérdida de humedad.",
                            "flavor_and_aromatics": "Delicadeza marina del robalo contrastada con el aroma anisado del eneldo y la nuez tostada.",
                            "textural_architecture": "Lascas de pescado nacaradas y jugosas con una cubierta crujiente quebradiza.",
                            "critical_control_points": "No sobrecocer para preservar las lascas sedosas del pescado."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla fundida",
                        "service_temp_c": 64,
                        "texture_target": "Nacarado, crujiente y jugoso",
                        "service_notes": "Servir en platos tibios decorados con una ramita de eneldo fresco."
                    },
                    "side_dish": {
                        "title": "Infusión Nocturna de Menta y Toronjil con Fórmula 34Plus®",
                        "technique": "steeping_and_infusion",
                        "note": "Preparación botánica calmante potenciada con 34Plus® para relajación muscular y regeneración celular nocturna.",
                        "ingredients": [
                            {"name": "Hierbas botánicas (toronjil y menta)", "amount": 24, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 4},
                            {"name": "Fórmula Reparadora 34Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Infusión: Calentar el agua a 88°C y verter sobre las hierbas; tapar y dejar reposar 5 minutos.",
                            "2. Filtrado: Colar y dejar templar a 48°C.",
                            "3. Activación: Incorporar la Fórmula 34Plus® batiendo hasta disolución completa.",
                            "4. Pase: Servir tibia en tazas."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Temperatura controlada a <50°C para integridad de los nutrientes de 34Plus®.",
                            "flavor_and_aromatics": "Aroma mentolado suave y reconfortante.",
                            "textural_architecture": "Líquido sedoso tibio.",
                            "critical_control_points": "Consumir 40 minutos antes de dormir."
                        },
                        "broth_volume_ml": 120,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 46,
                        "texture_target": "Tibio, límpido y relajante",
                        "service_notes": "Servir en tazas precalentadas."
                    }
                }
            ]
        },

        # -------------------------------------------------------------
        # MIÉRCOLES 14 DE OCTUBRE DE 2026
        # -------------------------------------------------------------
        {
            "day": "Miércoles",
            "date_str": "14 Oct",
            "day_num": "14",
            "month": "Octubre",
            "full_date_title": "Miércoles 14 de Octubre de 2026",
            "iso_date": "2026-10-14",
            "meals": [
                {
                    "meal_type": "Desayuno",
                    "starter_name": "Tazón de Fresas Silvestres con Nuez de la India y Chía",
                    "main_dish_name": "Huevos Estrellados en Sartén de Hierro con Aceite VEVO y Espárragos Verdes",
                    "side_dish_name": "Gelatina Artesanal de Fresa Viva (4°C) con Fórmula Nootrópica 33Plus®",
                    "fat_g": 39.0,
                    "protein_g": 36.0,
                    "net_carbs_g": 5.0,
                    "starter": {
                        "title": "Tazón de Fresas Silvestres con Nuez de la India y Chía",
                        "technique": "raw_assembly",
                        "note": "Antioxidantes matutinos con la cremosidad de la nuez de la India de alacena.",
                        "ingredients": [
                            {"name": "Fresas frescas", "amount": 300, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 50},
                            {"name": "Nuez de la India", "amount": 90, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 15},
                            {"name": "Semillas de chía orgánicas", "amount": 48, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 8}
                        ],
                        "steps": [
                            "1. Selección fría: Lavar y cortar fresas a 4°C.",
                            "2. Tostado leve: Tostar nuez de la India a 120°C por 2 minutos.",
                            "3. Ensamble: Colocar fresas, espolvorear chía y nueces."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble fresco.",
                            "flavor_and_aromatics": "Fruta viva con notas a nuez tostada.",
                            "textural_architecture": "Pulpa jugosa con crujido mantecoso.",
                            "critical_control_points": "Servir al momento."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 8,
                        "texture_target": "Fresco y crujiente",
                        "service_notes": "Servir en cuencos refrigerados."
                    },
                    "main_dish": {
                        "title": "Huevos Estrellados en Sartén de Hierro con Aceite VEVO y Espárragos Verdes",
                        "technique": "saute_and_sear",
                        "note": "3 huevos de pastoreo por comensal cocinados con puntilla dorada en aceite VEVO acompañados de espárragos de la huerta.",
                        "ingredients": [
                            {"name": "Huevos orgánicos de pastoreo", "amount": 18, "unit": "piezas", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 3},
                            {"name": "Espárragos verdes", "amount": 360, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 60},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 60, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Salteo de espárragos: En sartén de hierro con 20 ml de VEVO, saltear las puntas de espárrago a 150°C durante 3 minutos hasta tiernas; reservar al lado.",
                            "2. Cocción de huevos con puntilla: Verter el resto del aceite VEVO elevando el calor a 160°C; cascar los huevos dejando que la clara cree encaje dorado crujiente en los bordes mientras la yema permanece líquida y cremosa.",
                            "3. Servicio: Retirar con espátula flexible, sazonar con sal de mar en escamas y colocar junto a los espárragos verdes."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Contraste térmico de clara frita crocante a 160°C y yema caliente cremosa sin coagular a 60°C.",
                            "flavor_and_aromatics": "Riqueza lipídica de la yema combinada con el amargor fresco del espárrago y el frutado del VEVO.",
                            "textural_architecture": "Puntilla crujiente exterior con yema fluida que funciona como salsa natural sobre el espárrago al dente.",
                            "critical_control_points": "No romper las yemas al cascar."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Aceite VEVO",
                        "service_temp_c": 66,
                        "texture_target": "Puntilla crocante y yema sedosa",
                        "service_notes": "Servir inmediatamente en platos tibios."
                    },
                    "side_dish": {
                        "title": "Gelatina Artesanal de Fresa Viva (4°C) con Fórmula Nootrópica 33Plus®",
                        "technique": "gelatin_molding",
                        "note": "Colágeno hidrolizado puro y 33Plus® para sostén del enfoque cognitivo.",
                        "ingredients": [
                            {"name": "Fresas frescas", "amount": 120, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 20},
                            {"name": "Grenetina natural en polvo", "amount": 42, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 7},
                            {"name": "Fórmula Nootrópica 33Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Puré: Licuar fresas con agua purificada.",
                            "2. Grenetina: Disolver la grenetina a 60°C.",
                            "3. Suplementación: Enfriar a 39°C, agregar la Fórmula 33Plus® y batir.",
                            "4. Gelificación: Cuajar a 4°C por 4 horas."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Enfriamiento controlado para protección biotecnológica.",
                            "flavor_and_aromatics": "Fresa limpia y viva.",
                            "textural_architecture": "Gel elástico de fácil disolución.",
                            "critical_control_points": "Mantener refrigerada hasta el servicio."
                        },
                        "broth_volume_ml": 120,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 4,
                        "texture_target": "Firme y refrescante",
                        "service_notes": "Servir en copas frías."
                    }
                },
                {
                    "meal_type": "Comida",
                    "starter_name": "Crema Aterciopelada de Coliflor Rostizada con Ajo Confitado y Aceite VEVO",
                    "main_dish_name": "Corte Magro de Ribeye de Res a la Parrilla con Mantequilla de Romero y Ajo",
                    "side_dish_name": "Chayotes Tiernos al Vapor con Mantequilla Clarificada y Sal de Mar",
                    "fat_g": 53.0,
                    "protein_g": 48.5,
                    "net_carbs_g": 4.9,
                    "starter": {
                        "title": "Crema Aterciopelada de Coliflor Rostizada con Ajo Confitado y Aceite VEVO",
                        "technique": "boil_and_blend",
                        "note": "Coliflor de la granja rostizada al horno para caramelizar azúcares naturales y emulsionada con ajo confitado.",
                        "ingredients": [
                            {"name": "Coliflor fresca", "amount": 480, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 80},
                            {"name": "Fondo claro de pollo", "amount": 480, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 80},
                            {"name": "Ajo fresco", "amount": 18, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 35, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5.8},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Rostizado: Hornear los floretes de coliflor barnizados con aceite VEVO a 190°C durante 12 minutos hasta bordes dorados avellanados.",
                            "2. Cocción suave: Llevar la coliflor y el ajo confitado al fondo de pollo hirviendo durante 4 minutos.",
                            "3. Emulsión: Licuar a máxima potencia durante 60 segundos vertiendo el resto de VEVO en hilo hasta textura sedosa de terciopelo."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Reacción de Maillard vegetal en horno y emulsión mecánica en caliente a 72°C.",
                            "flavor_and_aromatics": "Complejidad profunda de nuez tostada y dulzura de coliflor caramelizada.",
                            "textural_architecture": "Terciopelo espeso homogéneo sin grumos.",
                            "critical_control_points": "Licuar a potencia máxima para micronizar la fibra."
                        },
                        "broth_volume_ml": 80,
                        "deglaze_agent": "Fondo de pollo",
                        "service_temp_c": 70,
                        "texture_target": "Sedoso, aterciopelado y satinado",
                        "service_notes": "Servir con pimienta negra recién molida al pase."
                    },
                    "main_dish": {
                        "title": "Corte Magro de Ribeye de Res a la Parrilla con Mantequilla de Romero y Ajo",
                        "technique": "saute_and_sear",
                        "note": "Corte magro de Ribeye de res premium amortizando el stock de Sam's Club, sellado a la parrilla y bañado en mantequilla de pastoreo aromatizada con romero.",
                        "ingredients": [
                            {"name": "Corte magro de Ribeye de res premium", "amount": 900, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 150},
                            {"name": "Mantequilla de pastoreo", "amount": 70, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 11.6},
                            {"name": "Romero fresco", "amount": 10, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1.6},
                            {"name": "Ajo fresco", "amount": 18, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Atemperado y secado: Atemperar los cortes de Ribeye a 18°C ambiente durante 20 minutos; secar con papel absorbente y sazonar con sal de mar.",
                            "2. Sellado de alta temperatura: Calentar sartén de hierro o parrilla a 200°C; colocar los cortes sellando 3 minutos por lado logrando corteza caramelizada intensa.",
                            "3. Arrosé de mantequilla: Bajar el fuego a medio, añadir la mantequilla, los dientes de ajo machacados y las ramas de romero fresco; bañar los filetes continuamente con la mantequilla espumosa durante 90 segundos hasta alcanzar 56°C interno (término medio jugoso).",
                            "4. Reposo: Dejar reposar los cortes sobre tabla de madera durante 4 minutos antes de servir."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Calor intenso a 200°C para Maillard óptima y redistribución de humedad en reposo a 56°C centro.",
                            "flavor_and_aromatics": "Umami puro vacuno ensalzado por la riqueza avellanada de la mantequilla y los terpenos balsámicos del romero.",
                            "textural_architecture": "Corteza crujiente exterior con un centro jugoso, tierno y fundente que cede sin resistencia.",
                            "critical_control_points": "Respetar los 4 minutos de reposo para evitar fuga de jugos en el plato."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla fundida",
                        "service_temp_c": 64,
                        "texture_target": "Corteza caramelizada y centro tierno",
                        "service_notes": "Servir en platos llanos precalentados con los jugos de reposo vertidos por encima."
                    },
                    "side_dish": {
                        "title": "Chayotes Tiernos al Vapor con Mantequilla Clarificada y Sal de Mar",
                        "technique": "boil_and_blend",
                        "note": "Chayote tierno de alacena cocido al vapor en rodajas uniformes con mantequilla clarificada.",
                        "ingredients": [
                            {"name": "Chayotes tiernos", "amount": 2, "unit": "piezas", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 0.33},
                            {"name": "Mantequilla de pastoreo", "amount": 40, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 6.6},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Corte: Pelar los chayotes y cortar en medias lunas de 6 mm.",
                            "2. Vapor controlado: Cocinar en vaporera a 100°C durante 6 minutos hasta tiernos pero firmes al centro.",
                            "3. Mantequilla y sal: Pasar los chayotes calientes a un tazón, barnizar con mantequilla derretida y espolvorear sal de mar."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cocción al vapor que ablanda pectinas sin lixiviar minerales al agua.",
                            "flavor_and_aromatics": "Dulzura vegetal sutil arropada por la untuosidad de la mantequilla.",
                            "textural_architecture": "Turgencia crujiente suave y jugosa.",
                            "critical_control_points": "No sobrepasar los 7 minutos de vapor para no deshacer la pulpa."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla",
                        "service_temp_c": 65,
                        "texture_target": "Tierno, jugoso y satinado",
                        "service_notes": "Acompañar junto al ribeye a la parrilla."
                    }
                },
                {
                    "meal_type": "Cena",
                    "starter_name": "Ensalada de Lechuga Sweet con Pepino Persa y Vinagreta al Limón",
                    "main_dish_name": "Tostadas en Hoja de Lechuga con Atún Canónico y Aderezo Casero al Cilantro",
                    "side_dish_name": "Infusión Relajante de Toronjil y Manzanilla con Fórmula 34Plus®",
                    "fat_g": 36.0,
                    "protein_g": 41.0,
                    "net_carbs_g": 3.6,
                    "starter": {
                        "title": "Ensalada de Lechuga Sweet con Pepino Persa y Vinagreta al Limón",
                        "technique": "raw_assembly",
                        "note": "Ensalada crujiente y liviana con la lechuga sweet de Sam's Club y aceite VEVO.",
                        "ingredients": [
                            {"name": "Lechuga Sweet", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Pepino fresco", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 30, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5},
                            {"name": "Jugo de limón fresco", "amount": 20, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Higienización: Centrifugar lechuga bien fría a 4°C.",
                            "2. Rodajas: Cortar pepino en láminas.",
                            "3. Vinagreta: Emulsionar aceite VEVO, limón y sal marina justo al pase."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble frío para máxima turgencia.",
                            "flavor_and_aromatics": "Fresco, crujiente y cítrico.",
                            "textural_architecture": "Hojas tersas y crocantes.",
                            "critical_control_points": "Servir inmediatamente."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 8,
                        "texture_target": "Crocante y fresco",
                        "service_notes": "Servir en ensaladeras individuales."
                    },
                    "main_dish": {
                        "title": "Tostadas en Hoja de Lechuga con Atún Canónico y Aderezo Casero al Cilantro",
                        "technique": "raw_assembly",
                        "note": "Proteína marina de rápida asimilación amortizando el atún canónico de Sam's Club, montado en hojas crujientes de lechuga con aderezo casero de mayonesa.",
                        "ingredients": [
                            {"name": "Atún enlatado", "amount": 600, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 100},
                            {"name": "Lechuga Sweet", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Mayonesa", "amount": 120, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 20},
                            {"name": "Cilantro fresco", "amount": 18, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3},
                            {"name": "Jugo de limón fresco", "amount": 25, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 4.1},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Drenado y emulsión: Drenar el atún enlatado; desmenuzar en tazón con mayonesa, cilantro fresco finamente picado, jugo de limón y sal de mar.",
                            "2. Hojas cóncavas: Disponer 2 hojas firmes de lechuga sweet por comensal a modo de barquitas o tostadas naturales.",
                            "3. Relleno y pase: Colocar porciones generosas de ensalada cremosa de atún dentro de cada hoja de lechuga y servir bien frescas."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble frío a 8°C que facilita digestión ligera previa al reposo.",
                            "flavor_and_aromatics": "Fresco y aromático con la cremosidad de la mayonesa y el perfume del cilantro.",
                            "textural_architecture": "Hoja crocante y quebradiza que sostiene una ensalada tierna, jugosa y sedosa.",
                            "critical_control_points": "Drenar perfectamente el atún para que no agüe el aderezo."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 10,
                        "texture_target": "Crocante, fresco y cremoso",
                        "service_notes": "Servir de inmediato en platos planos."
                    },
                    "side_dish": {
                        "title": "Infusión Relajante de Toronjil y Manzanilla con Fórmula 34Plus®",
                        "technique": "steeping_and_infusion",
                        "note": "Infusión nocturna regeneradora con Fórmula 34Plus® para calmar el sistema nervioso y activar autofagia nocturna.",
                        "ingredients": [
                            {"name": "Hierbas botánicas (toronjil y menta)", "amount": 20, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 3.3},
                            {"name": "Fórmula Reparadora 34Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Infusión caliente: Hervir agua a 88°C e infusionar las hierbas durante 5 minutos tapado.",
                            "2. Filtrado: Colar y atemperar a 48°C.",
                            "3. Adición de 34Plus®: Disolver la Fórmula 34Plus® agitando suavemente.",
                            "4. Pase: Servir tibia."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Temperatura moderada para proteger los prebióticos de 34Plus®.",
                            "flavor_and_aromatics": "Floral apacible y aromático.",
                            "textural_architecture": "Líquido sedoso y tibio.",
                            "critical_control_points": "Tomar antes del descanso nocturno."
                        },
                        "broth_volume_ml": 120,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 46,
                        "texture_target": "Tibio, límpido y relajante",
                        "service_notes": "Servir en tazas precalentadas."
                    }
                }
            ]
        }
    ]
