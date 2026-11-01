# -*- coding: utf-8 -*-
"""
Días Jueves 15, Viernes 16 y Sábado 17 Oct para Semana 42
Ecosistema NutriKeto Atelier T.I.L.O.®
Arquitectura COCT, Atwater y Gobernanza Bioquímica.
"""

def get_jueves_viernes_sabado():
    return [
        # -------------------------------------------------------------
        # JUEVES 15 DE OCTUBRE DE 2026
        # -------------------------------------------------------------
        {
            "day": "Jueves",
            "date_str": "15 Oct",
            "day_num": "15",
            "month": "Octubre",
            "full_date_title": "Jueves 15 de Octubre de 2026",
            "iso_date": "2026-10-15",
            "meals": [
                {
                    "meal_type": "Desayuno",
                    "starter_name": "Tazón de Arándanos Frescos con Semillas de Girasol y Chía",
                    "main_dish_name": "Rollo Tamagoyaki Culinario en Capas con Queso Gouda y Pavo",
                    "side_dish_name": "Gelatina Artesanal de Arándanos Vivos (4°C) con Fórmula Nootrópica 33Plus®",
                    "fat_g": 38.5,
                    "protein_g": 36.5,
                    "net_carbs_g": 5.2,
                    "starter": {
                        "title": "Tazón de Arándanos Frescos con Semillas de Girasol y Chía",
                        "technique": "raw_assembly",
                        "note": "Antocianinas y antioxidantes vasculares con semillas tostadas ricas en zinc.",
                        "ingredients": [
                            {"name": "Arándanos frescos", "amount": 300, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 50},
                            {"name": "Semillas de girasol", "amount": 60, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10},
                            {"name": "Semillas de chía orgánicas", "amount": 48, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 8}
                        ],
                        "steps": [
                            "1. Selección fría: Mantener arándanos a 4°C y secar suavemente.",
                            "2. Tostado de girasol: Tostar semillas de girasol a 130°C por 2 minutos.",
                            "3. Ensamble: Distribuir arándanos, espolvorear chía y semillas de girasol crocantes."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cadena de frío en frutos y semillas crujientes.",
                            "flavor_and_aromatics": "Dulzura ácida vibrante con tostado denso de semilla.",
                            "textural_architecture": "Estallido jugoso de arándano y crujido fino de girasol.",
                            "critical_control_points": "Servir fresco al momento."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 8,
                        "texture_target": "Fresco y crujiente",
                        "service_notes": "Servir en cuencos refrigerados."
                    },
                    "main_dish": {
                        "title": "Rollo Tamagoyaki Culinario en Capas con Queso Gouda y Pavo",
                        "technique": "saute_and_sear",
                        "note": "3 huevos de pastoreo por comensal doblados en capas milimétricas con mantequilla de pastoreo, queso gouda y finas hebras de pechuga de pavo.",
                        "ingredients": [
                            {"name": "Huevos orgánicos de pastoreo", "amount": 18, "unit": "piezas", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 3},
                            {"name": "Queso Gouda", "amount": 180, "unit": "g", "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "per_guest": 30},
                            {"name": "Pechuga de pavo artesanal", "amount": 120, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 20},
                            {"name": "Mantequilla de pastoreo", "amount": 70, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 11.6},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Batido homogéneo: Batir los 18 huevos con sal marina colando suavemente para eliminar burbujas.",
                            "2. Capas laminadas: En sartén rectangular barnizada con mantequilla a 125°C, verter una capa delgada de huevo; al cuajar colocar hebras de pavo y queso gouda, enrollar hacia un extremo.",
                            "3. Segunda y tercera capa: Barnizar con mantequilla, verter otra capa de huevo levantando el rollo para que penetre la mezcla líquida y enrollar sucesivamente hasta formar un cilindro de capas densas y tiernas.",
                            "4. Corte: Retirar a tabla, reposar 60 segundos y cortar en rodajas transversales de 2.5 cm."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Coagulación controlada en láminas delgadas que atrapa vapor interno manteniendo textura esponjosa y húmeda a 66°C.",
                            "flavor_and_aromatics": "Sabor rico a huevo dorado con el fundido salino del gouda y la sutileza del pavo.",
                            "textural_architecture": "Capas concéntricas aterciopeladas con núcleo elástico de queso fundido.",
                            "critical_control_points": "Fuego moderado continuo para no quemar las capas exteriores."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla",
                        "service_temp_c": 66,
                        "texture_target": "Esponjoso, laminar y fundente",
                        "service_notes": "Servir las rodajas luciendo el espiral interior."
                    },
                    "side_dish": {
                        "title": "Gelatina Artesanal de Arándanos Vivos (4°C) con Fórmula Nootrópica 33Plus®",
                        "technique": "gelatin_molding",
                        "note": "Dosis nootrópica matutina con colágeno hidrolizado puro y Fórmula 33Plus®.",
                        "ingredients": [
                            {"name": "Arándanos frescos", "amount": 120, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 20},
                            {"name": "Grenetina natural en polvo", "amount": 42, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 7},
                            {"name": "Fórmula Nootrópica 33Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Extracción: Procesar arándanos con agua purificada.",
                            "2. Grenetina: Disolver la grenetina a 60°C.",
                            "3. Fusión templada: Enfriar a 39°C, mezclar la Fórmula 33Plus® agitando.",
                            "4. Cuajado: Moldear y refrigerar a 4°C por 4 horas."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Protección térmica de adaptógenos nootrópicos.",
                            "flavor_and_aromatics": "Arándano puro aromático.",
                            "textural_architecture": "Gel firme y cristalino.",
                            "critical_control_points": "Servir recién desmoldada."
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
                    "starter_name": "Crema Sedosa de Espárragos Verdes con Aceite de Oliva VEVO",
                    "main_dish_name": "Filete de Salmón al Horno con Costra de Nuez de la India Tostada",
                    "side_dish_name": "Nopales Asados al Orégano y Aceite de Oliva VEVO",
                    "fat_g": 53.0,
                    "protein_g": 48.0,
                    "net_carbs_g": 5.0,
                    "starter": {
                        "title": "Crema Sedosa de Espárragos Verdes con Aceite de Oliva VEVO",
                        "technique": "boil_and_blend",
                        "note": "Espárragos verdes tiernos de la granja cocidos en fondo de pollo y emulsionados con aceite de oliva VEVO.",
                        "ingredients": [
                            {"name": "Espárragos verdes", "amount": 480, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 80},
                            {"name": "Fondo claro de pollo", "amount": 480, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 80},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 35, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5.8},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Cocción en fondo: Cocer los espárragos en el fondo de pollo hirviendo durante 5 minutos.",
                            "2. Emulsión: Licuar en caliente a alta velocidad durante 60 segundos vertiendo el aceite VEVO en hilo.",
                            "3. Pase: Servir cremosa y caliente."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Emulsión mecánica que satura la fibra soluble creando viscosidad natural.",
                            "flavor_and_aromatics": "Sabor vegetal noble y limpio con el frutado del VEVO.",
                            "textural_architecture": "Terciopelo líquido homogéneo.",
                            "critical_control_points": "Retirar la base leñosa de los espárragos antes de hervir."
                        },
                        "broth_volume_ml": 80,
                        "deglaze_agent": "Fondo de pollo",
                        "service_temp_c": 70,
                        "texture_target": "Aterciopelado y satinado",
                        "service_notes": "Decorar con puntas de espárrago al dente."
                    },
                    "main_dish": {
                        "title": "Filete de Salmón al Horno con Costra de Nuez de la India Tostada",
                        "technique": "saute_and_sear",
                        "note": "Lomo de salmón rico en astaxantina y Omega-3, horneado con una costra crujiente de Nuez de la India (Sam's Club) y mantequilla de pastoreo.",
                        "ingredients": [
                            {"name": "Lomo de salmón fresco", "amount": 900, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 150},
                            {"name": "Nuez de la India", "amount": 90, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 15},
                            {"name": "Mantequilla de pastoreo", "amount": 60, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10},
                            {"name": "Eneldo fresco", "amount": 12, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 2},
                            {"name": "Jugo de limón fresco", "amount": 25, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 4.1},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Costra de nuez: Procesar toscamente la nuez de la India con el eneldo fresco y 20 g de mantequilla pomada creando una pasta crujiente.",
                            "2. Acondicionamiento de salmón: Sazonar los lomos de salmón con sal de mar y jugo de limón; disponer sobre bandeja engrasada con mantequilla.",
                            "3. Cubierta y horneado: Extender la pasta de nuez de la India sobre la cara superior del salmón; hornear a 180°C durante 8 minutos hasta que la costra esté dorada y el centro del salmón alcance 50°C interno (jugoso y rosado).",
                            "4. Servicio: Servir de inmediato preservando la textura crocante de la nuez."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cocción suave al horno que previene la exudación de albúmina blanca manteniendo la grasa miocárdica a 50°C.",
                            "flavor_and_aromatics": "Intensidad marina del salmón equilibrada por la dulzura mantecosa de la nuez de la India y el frescor anisado del eneldo.",
                            "textural_architecture": "Lascas de pescado sedosas y tiernas que contrastan con una cubierta crocante y dorada.",
                            "critical_control_points": "No sobrecocer para evitar que la nuez de la India se queme."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla fundida",
                        "service_temp_c": 54,
                        "texture_target": "Lascas sedosas con costra crujiente",
                        "service_notes": "Servir en platos llanos precalentados."
                    },
                    "side_dish": {
                        "title": "Nopales Asados al Orégano y Aceite de Oliva VEVO",
                        "technique": "roast_bake",
                        "note": "Nopales tiernos de la huerta asados a la plancha seca para evaporar la baba natural.",
                        "ingredients": [
                            {"name": "Nopales tiernos", "amount": 480, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 80},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 30, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5},
                            {"name": "Orégano seco", "amount": 5, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.8},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Marcado: Cortar nopales en tiras; barnizar con aceite VEVO, sal marina y orégano.",
                            "2. Asado comal: Asar a 170°C durante 3 minutos por lado hasta secar baba.",
                            "3. Pase: Servir calientes y carnosos."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Calor seco en comal que desnaturaliza mucílagos.",
                            "flavor_and_aromatics": "Acidez vegetal rústica perfumada de orégano.",
                            "textural_architecture": "Carnosidad turgente sin baba.",
                            "critical_control_points": "Plancha muy caliente para evaporación inmediata."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 65,
                        "texture_target": "Carnoso y firme",
                        "service_notes": "Disponer junto al filete de salmón."
                    }
                },
                {
                    "meal_type": "Cena",
                    "starter_name": "Bastones de Pepino y Apio al Limón con Sal Marina",
                    "main_dish_name": "Salpicón Fresco de Pechuga de Pavo con Aguacate Hass y Cilantro",
                    "side_dish_name": "Infusión Nocturna Digestiva de Menta y Limón con Fórmula 34Plus®",
                    "fat_g": 36.5,
                    "protein_g": 41.0,
                    "net_carbs_g": 3.6,
                    "starter": {
                        "title": "Bastones de Pepino y Apio al Limón con Sal Marina",
                        "technique": "raw_assembly",
                        "note": "Apertura digestiva crujiente e hidratante.",
                        "ingredients": [
                            {"name": "Pepino fresco", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Apio fresco", "amount": 180, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 30},
                            {"name": "Jugo de limón fresco", "amount": 20, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Bastones: Cortar pepino y apio en bastones uniformes.",
                            "2. Aliño: Servir con jugo de limón y sal de mar."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble frío a 8°C.",
                            "flavor_and_aromatics": "Fresco, mineral y cítrico.",
                            "textural_architecture": "Crujiente y acuoso.",
                            "critical_control_points": "Servir recién cortado."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 8,
                        "texture_target": "Crocante",
                        "service_notes": "Servir en vasos refrigerados."
                    },
                    "main_dish": {
                        "title": "Salpicón Fresco de Pechuga de Pavo con Aguacate Hass y Cilantro",
                        "technique": "raw_assembly",
                        "note": "Proteína magra deshebrada mezclada con aguacate en cubos, cilantro fresco y vinagreta suave al limón.",
                        "ingredients": [
                            {"name": "Pechuga de pavo artesanal", "amount": 720, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 120},
                            {"name": "Aguacate Hass fresco", "amount": 3, "unit": "piezas", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 0.5},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 30, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5},
                            {"name": "Cilantro fresco", "amount": 20, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3.3},
                            {"name": "Jugo de limón fresco", "amount": 25, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 4.1},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Deshebrado fino: Deshebrar la pechuga de pavo cocida en hebras delgadas.",
                            "2. Dados de aguacate: Cortar el aguacate en cubos de 1 cm.",
                            "3. Mezcla y aliño: En cuenco amplio, combinar el pavo, aguacate, cilantro picado, jugo de limón, aceite VEVO y sal de mar mezclando con cuidado para no deshacer el aguacate.",
                            "4. Pase: Servir inmediatamente fresco."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble frío que facilita reposo digestivo.",
                            "flavor_and_aromatics": "Fresco, cítrico y herbáceo con la cremosidad del aguacate.",
                            "textural_architecture": "Hebras tiernas de carne con cubos mantecosos de aguacate.",
                            "critical_control_points": "Integrar el aguacate al final con movimientos envolventes."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 12,
                        "texture_target": "Fresco, tierno y cremoso",
                        "service_notes": "Servir en ensaladeras frías."
                    },
                    "side_dish": {
                        "title": "Infusión Nocturna Digestiva de Menta y Limón con Fórmula 34Plus®",
                        "technique": "steeping_and_infusion",
                        "note": "Infusión botánica con Fórmula 34Plus® para calmar inflamación y modular microbiota.",
                        "ingredients": [
                            {"name": "Hierbas botánicas (toronjil y menta)", "amount": 20, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 3.3},
                            {"name": "Fórmula Reparadora 34Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Infusión caliente: Hervir agua a 88°C e infusionar hojas de menta durante 5 minutos.",
                            "2. Filtrado: Colar y templar a 48°C.",
                            "3. Activación: Disolver la Fórmula 34Plus®.",
                            "4. Pase: Servir tibia."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Temperatura controlada a <50°C.",
                            "flavor_and_aromatics": "Aroma limpio de menta y limón.",
                            "textural_architecture": "Líquido sedoso tibio.",
                            "critical_control_points": "Consumir 45 minutos antes de dormir."
                        },
                        "broth_volume_ml": 120,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 46,
                        "texture_target": "Tibio y relajante",
                        "service_notes": "Servir en tazas precalentadas."
                    }
                }
            ]
        },

        # -------------------------------------------------------------
        # VIERNES 16 DE OCTUBRE DE 2026
        # -------------------------------------------------------------
        {
            "day": "Viernes",
            "date_str": "16 Oct",
            "day_num": "16",
            "month": "Octubre",
            "full_date_title": "Viernes 16 de Octubre de 2026",
            "iso_date": "2026-10-16",
            "meals": [
                {
                    "meal_type": "Desayuno",
                    "starter_name": "Tazón de Fresas Frescas con Nueces de Castilla y Chía",
                    "main_dish_name": "Huevos al Sartén en Anillo de Pimiento Morrón con Mantequilla de Pastoreo",
                    "side_dish_name": "Gelatina Artesanal de Fresa Viva (4°C) con Fórmula Nootrópica 33Plus®",
                    "fat_g": 38.5,
                    "protein_g": 36.2,
                    "net_carbs_g": 5.2,
                    "starter": {
                        "title": "Tazón de Fresas Frescas con Nueces de Castilla y Chía",
                        "technique": "raw_assembly",
                        "note": "Antioxidantes matutinos con grasas saludables omega-3 vegetales de nuez de Castilla.",
                        "ingredients": [
                            {"name": "Fresas frescas", "amount": 300, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 50},
                            {"name": "Nueces de Castilla", "amount": 90, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 15},
                            {"name": "Semillas de chía orgánicas", "amount": 48, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 8}
                        ],
                        "steps": [
                            "1. Selección fría: Lavar y cortar fresas a 4°C.",
                            "2. Tostado leve: Tostar nueces a 120°C por 2 minutos.",
                            "3. Ensamble: Colocar fresas, espolvorear chía y nueces crujientes."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble frío para turgencia celular.",
                            "flavor_and_aromatics": "Dulzura ácida fresca con nuez tostada.",
                            "textural_architecture": "Pulpa jugosa con crujido denso.",
                            "critical_control_points": "Servir al momento."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 8,
                        "texture_target": "Fresco y crujiente",
                        "service_notes": "Servir en cuencos refrigerados."
                    },
                    "main_dish": {
                        "title": "Huevos al Sartén en Anillo de Pimiento Morrón con Mantequilla de Pastoreo",
                        "technique": "saute_and_sear",
                        "note": "3 huevos de pastoreo por comensal cocidos dentro de aros gruesos de pimiento morrón dulce con mantequilla clarificada y cilantro fresco.",
                        "ingredients": [
                            {"name": "Huevos orgánicos de pastoreo", "amount": 18, "unit": "piezas", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 3},
                            {"name": "Pimientos morrones dulces", "amount": 360, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 60},
                            {"name": "Mantequilla de pastoreo", "amount": 70, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 11.6},
                            {"name": "Cilantro fresco", "amount": 20, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Aros de pimiento: Cortar los pimientos en aros transversales de 2 cm retirando semillas.",
                            "2. Sellado de aro: Fundir mantequilla en sartén amplia a 140°C; colocar los aros dorando 90 segundos por cara.",
                            "3. Cascar dentro del anillo: Cascar un huevo en el interior de cada aro de pimiento; tapar y cocinar a fuego suave (120°C) durante 3 minutos hasta clara blanca firme y yema líquida brillante.",
                            "4. Pase: Servir los aros coronados con cilantro fresco y sal de mar en escamas."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Contención térmica en el anillo de vegetal que concentra calor suave (64°C) sobre la yema.",
                            "flavor_and_aromatics": "Dulzura caramelizada del pimiento morrón realzando la riqueza grasa de la yema.",
                            "textural_architecture": "Anillo crujiente y jugoso que abraza la suavidad tierna de la clara y la yema sedosa.",
                            "critical_control_points": "Sartén bien plana para que la clara no escape por debajo del aro."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla",
                        "service_temp_c": 66,
                        "texture_target": "Tierno, sedoso y aromático",
                        "service_notes": "Servir en platos tibios con una pizca de cilantro picado."
                    },
                    "side_dish": {
                        "title": "Gelatina Artesanal de Fresa Viva (4°C) con Fórmula Nootrópica 33Plus®",
                        "technique": "gelatin_molding",
                        "note": "Vehículo matutino nootrópico con colágeno hidrolizado puro y Fórmula 33Plus®.",
                        "ingredients": [
                            {"name": "Fresas frescas", "amount": 120, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 20},
                            {"name": "Grenetina natural en polvo", "amount": 42, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 7},
                            {"name": "Fórmula Nootrópica 33Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Puré: Licuar fresas con agua purificada.",
                            "2. Grenetina: Disolver la grenetina a 60°C.",
                            "3. Integración 33Plus®: Enfriar a 39°C, agregar la Fórmula 33Plus® batiendo.",
                            "4. Cuajado: Moldear y refrigerar a 4°C por 4 horas."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Protección estricta de adaptógenos termosensibles.",
                            "flavor_and_aromatics": "Fruta viva limpia.",
                            "textural_architecture": "Gel elástico suave.",
                            "critical_control_points": "Mantener refrigerada."
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
                    "starter_name": "Sopa de Calabacitas al Queso Parmesano y Cilantro Fresco",
                    "main_dish_name": "Lomo de Robalo Fresco al Sartén en Mantequilla de Alcaparras y Eneldo",
                    "side_dish_name": "Brócoli Fresco al Vapor con Queso Ricotta y Sal de Mar",
                    "fat_g": 52.0,
                    "protein_g": 48.5,
                    "net_carbs_g": 5.1,
                    "starter": {
                        "title": "Sopa de Calabacitas al Queso Parmesano y Cilantro Fresco",
                        "technique": "boil_and_blend",
                        "note": "Calabacitas tiernas cocidas en fondo claro de ave coronadas con queso parmesano rallado.",
                        "ingredients": [
                            {"name": "Calabacitas verdes tiernas", "amount": 360, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 60},
                            {"name": "Fondo claro de pollo", "amount": 600, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 100},
                            {"name": "Queso Parmesano artesanal", "amount": 60, "unit": "g", "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "per_guest": 10},
                            {"name": "Cilantro fresco", "amount": 18, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Cocción: Cocinar las calabacitas en rodajas en el fondo hirviendo a 90°C durante 5 minutos.",
                            "2. Ensamble: Servir caliente en tazones, espolvorear parmesano recién rallado y cilantro."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cocción suave que conserva la textura al dente de la calabacita.",
                            "flavor_and_aromatics": "Umami del parmesano fundiéndose en el caldo aromático.",
                            "textural_architecture": "Caldo límpido con virutas fundentes de queso.",
                            "critical_control_points": "Espolvorear el parmesano al pase."
                        },
                        "broth_volume_ml": 100,
                        "deglaze_agent": "Fondo de pollo",
                        "service_temp_c": 70,
                        "texture_target": "Líquido aromático con verdura tierna",
                        "service_notes": "Servir en cuencos hondos."
                    },
                    "main_dish": {
                        "title": "Lomo de Robalo Fresco al Sartén en Mantequilla de Alcaparras y Eneldo",
                        "technique": "saute_and_sear",
                        "note": "Robalo blanco magro con piel crujiente sellado en mantequilla avellanada y bañado con salsa tibia de alcaparras y eneldo fresco.",
                        "ingredients": [
                            {"name": "Filete de Robalo fresco", "amount": 900, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 150},
                            {"name": "Mantequilla de pastoreo", "amount": 70, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 11.6},
                            {"name": "Alcaparras", "amount": 30, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 5},
                            {"name": "Eneldo fresco", "amount": 15, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 2.5},
                            {"name": "Jugo de limón fresco", "amount": 25, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 4.1},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Secado y salado: Secar los filetes de robalo con piel; sazonar con sal de mar.",
                            "2. Piel hipercrocante: En sartén de hierro bien caliente con 20 g de mantequilla a 160°C, sellar los filetes por el lado de la piel presionando suavemente durante 4 minutos hasta lograr piel crujiente dorada.",
                            "3. Volteo y arrosé: Dar vuelta delicadamente; añadir el resto de la mantequilla, las alcaparras escurridas, el eneldo picado y el jugo de limón.",
                            "4. Bañado continuo: Bañar los lomos con la mantequilla espumosa durante 90 segundos hasta que el corazón alcance 58°C nacarado; servir con la piel hacia arriba."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Sellado asimétrico (80% del tiempo sobre la piel) protegiendo el músculo delicado del robalo.",
                            "flavor_and_aromatics": "Sabor marino limpio complementado por el punto salino y ácido de las alcaparras y la grasa avellanada.",
                            "textural_architecture": "Piel hipercrocante que cede a lascas nacaradas, tiernas y colmadas de jugo.",
                            "critical_control_points": "Montar siempre con la piel hacia arriba para evitar que el vapor de la salsa la ablande."
                        },
                        "broth_volume_ml": 25,
                        "deglaze_agent": "Jugo de limón y mantequilla",
                        "service_temp_c": 64,
                        "texture_target": "Piel hipercrocante y lascas jugosas",
                        "service_notes": "Servir en platos tibios salseando alrededor."
                    },
                    "side_dish": {
                        "title": "Brócoli Fresco al Vapor con Queso Ricotta y Sal de Mar",
                        "technique": "boil_and_blend",
                        "note": "Floretes de brócoli de la huerta al vapor acompañados de quenelles tibias de Queso Ricotta (Sam's Club).",
                        "ingredients": [
                            {"name": "Brócoli fresco", "amount": 480, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 80},
                            {"name": "Queso Ricotta", "amount": 180, "unit": "g", "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "per_guest": 30},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 30, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Vapor de precisión: Cocinar los floretes de brócoli al vapor a 100°C durante 4.5 minutos hasta verde brillante y crujientes al morder.",
                            "2. Aliño y quenelle: Disponer el brócoli caliente en el plato, aliñar con aceite VEVO y sal marina; colocar a un lado una quenelle de queso ricotta fresco."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cocción al vapor rápida que mantiene sulforafanos activos.",
                            "flavor_and_aromatics": "Notas vegetales limpias enriquecidas por la cremosidad suave del ricotta.",
                            "textural_architecture": "Floretes elásticos y turgentes que se complementan con la textura untuosa del queso.",
                            "critical_control_points": "No sobrecocer el brócoli."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Aceite VEVO",
                        "service_temp_c": 64,
                        "texture_target": "Crujiente al dente y cremoso",
                        "service_notes": "Servir junto al robalo a las alcaparras."
                    }
                },
                {
                    "meal_type": "Cena",
                    "starter_name": "Abanico de Aguacate Hass Fresco con Sal Marina y Limón",
                    "main_dish_name": "Champiñones Portobello Rellenos de Espinacas, Queso Ricotta y Nuez de la India",
                    "side_dish_name": "Infusión Relajante de Toronjil y Azahar con Fórmula 34Plus®",
                    "fat_g": 36.5,
                    "protein_g": 40.5,
                    "net_carbs_g": 3.8,
                    "starter": {
                        "title": "Abanico de Aguacate Hass Fresco con Sal Marina y Limón",
                        "technique": "raw_assembly",
                        "note": "Grasas monoinsaturadas cardiosaludables dispuestas en finas láminas.",
                        "ingredients": [
                            {"name": "Aguacate Hass fresco", "amount": 3, "unit": "piezas", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 0.5},
                            {"name": "Jugo de limón fresco", "amount": 20, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Laminado: Cortar aguacate en láminas finas y abrir en abanico.",
                            "2. Aliño: Sazonar con jugo de limón fresco y sal marina al pase."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble frío para textura de mantequilla vegetal.",
                            "flavor_and_aromatics": "Grasa limpia con acidez vivaz.",
                            "textural_architecture": "Sedoso y fundente al paladar.",
                            "critical_control_points": "Servir recién cortado para evitar pardeamiento enzimático."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 12,
                        "texture_target": "Sedoso y fundente",
                        "service_notes": "Servir en platos individuales."
                    },
                    "main_dish": {
                        "title": "Champiñones Portobello Rellenos de Espinacas, Queso Ricotta y Nuez de la India",
                        "technique": "roast_bake",
                        "note": "Sombreros carnosos de Portobello horneados y rellenos con espinacas salteadas, Queso Ricotta (Sam's Club) y coronados con Nuez de la India tostada.",
                        "ingredients": [
                            {"name": "Champiñones Portobello", "amount": 720, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 120},
                            {"name": "Queso Ricotta", "amount": 240, "unit": "g", "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "per_guest": 40},
                            {"name": "Espinacas frescas", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Nuez de la India", "amount": 60, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 30, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Preparación de hongos: Limpiar los sombreros de Portobello y barnizar con aceite VEVO y sal marina.",
                            "2. Relleno cremoso: Saltear las espinacas en 10 ml de VEVO hasta colapsar; picar y mezclar con el queso ricotta y sal marina.",
                            "3. Horneado y gratinado: Rellenar cada Portobello con la mezcla de ricotta y espinacas; colocar en bandeja y hornear a 180°C durante 10 minutos hasta que el hongo esté tierno y jugoso.",
                            "4. Pase: Coronar con la nuez de la India tostada y troceada para dar textura crujiente."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Horneado medio a 180°C que extrae el umami vegetal del hongo sin deshidratar el relleno lácteo.",
                            "flavor_and_aromatics": "Notas terrosas y profundas de hongo fundidas con la frescura láctea del ricotta y el tostado dulce de la nuez.",
                            "textural_architecture": "Carne carnosa y tierna de Portobello que sostiene una crema suave contrastada por la nuez crujiente.",
                            "critical_control_points": "No lavar los Portobello en agua sumergida para no saturar de humedad su pulpa esponjosa."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Aceite VEVO",
                        "service_temp_c": 66,
                        "texture_target": "Carnoso, tierno y relleno cremoso",
                        "service_notes": "Servir calientes en platos medianos."
                    },
                    "side_dish": {
                        "title": "Infusión Relajante de Toronjil y Azahar con Fórmula 34Plus®",
                        "technique": "steeping_and_infusion",
                        "note": "Preparación nocturna para inducción de sueño profundo y regeneración celular con 34Plus®.",
                        "ingredients": [
                            {"name": "Flores de manzanilla y azahar", "amount": 20, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 3.3},
                            {"name": "Fórmula Reparadora 34Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Infusión: Calentar agua a 88°C e infusionar 6 minutos.",
                            "2. Filtrado: Colar y templar a 48°C.",
                            "3. Activación: Disolver la Fórmula 34Plus®.",
                            "4. Pase: Servir tibia."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Temperatura segura para prebióticos y micronutrientes.",
                            "flavor_and_aromatics": "Floral apacible y relajante.",
                            "textural_architecture": "Líquido sedoso.",
                            "critical_control_points": "Tomar antes del descanso."
                        },
                        "broth_volume_ml": 120,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 46,
                        "texture_target": "Tibio y relajante",
                        "service_notes": "Servir en tazas precalentadas."
                    }
                }
            ]
        },

        # -------------------------------------------------------------
        # SÁBADO 17 DE OCTUBRE DE 2026
        # -------------------------------------------------------------
        {
            "day": "Sábado",
            "date_str": "17 Oct",
            "day_num": "17",
            "month": "Octubre",
            "full_date_title": "Sábado 17 de Octubre de 2026",
            "iso_date": "2026-10-17",
            "meals": [
                {
                    "meal_type": "Desayuno",
                    "starter_name": "Tazón de Moras Silvestres con Semillas de Chía y Coco Rallado",
                    "main_dish_name": "Frittata Ranchera de Huevos con Tocino de Pavo y Queso Gouda",
                    "side_dish_name": "Gelatina Artesanal de Moras Vivas (4°C) con Fórmula Nootrópica 33Plus®",
                    "fat_g": 38.5,
                    "protein_g": 36.5,
                    "net_carbs_g": 5.1,
                    "starter": {
                        "title": "Tazón de Moras Silvestres con Semillas de Chía y Coco Rallado",
                        "technique": "raw_assembly",
                        "note": "Antioxidantes y grasas de cadena media (MCT) de coco natural sin azúcar.",
                        "ingredients": [
                            {"name": "Moras frescas", "amount": 300, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 50},
                            {"name": "Semillas de chía orgánicas", "amount": 48, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 8},
                            {"name": "Almendras fileteadas tostadas", "amount": 60, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10}
                        ],
                        "steps": [
                            "1. Selección fría: Moras lavadas a 4°C.",
                            "2. Ensamble: Colocar moras en cuenco, espolvorear chía y almendras fileteadas crujientes."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble fresco.",
                            "flavor_and_aromatics": "Frutos rojos vivos con toque tostado.",
                            "textural_architecture": "Pulpa jugosa y láminas crujientes.",
                            "critical_control_points": "Servir al momento."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 8,
                        "texture_target": "Fresco y crujiente",
                        "service_notes": "Servir en cuencos refrigerados."
                    },
                    "main_dish": {
                        "title": "Frittata Ranchera de Huevos con Tocino de Pavo y Queso Gouda",
                        "technique": "saute_and_sear",
                        "note": "3 huevos por comensal (Leucina ≥2.5 g) cuajados en sartén de hierro con tocino de pavo dorado, queso gouda derretido y pimientos.",
                        "ingredients": [
                            {"name": "Huevos orgánicos de pastoreo", "amount": 18, "unit": "piezas", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 3},
                            {"name": "Queso Gouda", "amount": 180, "unit": "g", "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "per_guest": 30},
                            {"name": "Pechuga de pavo artesanal", "amount": 180, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 30},
                            {"name": "Mantequilla de pastoreo", "amount": 60, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10},
                            {"name": "Cilantro fresco", "amount": 20, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Dorado base: En sartén de hierro con mantequilla a 140°C, saltear cubos de pavo durante 2 minutos hasta dorar.",
                            "2. Batido: Batir los 18 huevos con sal marina y cilantro picado.",
                            "3. Cuajado y gratinado: Verter los huevos sobre el pavo caliente; a fuego medio-bajo dejar cuajar los bordes durante 3 minutos; distribuir el queso gouda en superficie y terminar bajo el grill del horno a 190°C durante 3 minutos hasta inflar y gratinar dorado.",
                            "4. Corte: Cortar en 6 porciones triangulares generosas y servir calientes."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cocción mixta (estufa y grill) para base suave cuajada a 68°C y superficie gratinada a 190°C.",
                            "flavor_and_aromatics": "Riqueza cárnica y láctea con el tostado del queso gratinado.",
                            "textural_architecture": "Cuajada esponjosa y aireada con costra superior crujiente y queso fundente.",
                            "critical_control_points": "Vigilar el grill para que el queso dore sin quemar."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla",
                        "service_temp_c": 68,
                        "texture_target": "Esponjoso, gratinado y fundente",
                        "service_notes": "Servir en rebanadas triangulares sobre platos calientes."
                    },
                    "side_dish": {
                        "title": "Gelatina Artesanal de Moras Vivas (4°C) con Fórmula Nootrópica 33Plus®",
                        "technique": "gelatin_molding",
                        "note": "Gelatina matutina de colágeno y Fórmula 33Plus® para encendido cognitivo del fin de semana.",
                        "ingredients": [
                            {"name": "Moras frescas", "amount": 120, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 20},
                            {"name": "Grenetina natural en polvo", "amount": 42, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 7},
                            {"name": "Fórmula Nootrópica 33Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Puré: Licuar moras con agua purificada y tamizar.",
                            "2. Grenetina: Disolver a 60°C.",
                            "3. Fusión templada: Enfriar a 39°C e incorporar la Fórmula 33Plus®.",
                            "4. Cuajado: Moldear y refrigerar a 4°C por 4 horas."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Protección de bioactivos mediante enfriamiento previo a adición.",
                            "flavor_and_aromatics": "Moras silvestres aromáticas y limpias.",
                            "textural_architecture": "Gel firme y tembloroso de disolución rápida.",
                            "critical_control_points": "Mantener refrigerada hasta el pase."
                        },
                        "broth_volume_ml": 120,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 4,
                        "texture_target": "Fresco, firme y elástico",
                        "service_notes": "Servir en copas refrigeradas."
                    }
                },
                {
                    "meal_type": "Comida",
                    "starter_name": "Caldo Rústico de Hortalizas y Fondo Claro con Cilantro Fresco",
                    "main_dish_name": "Puntas de Filete de Res Salteadas con Pimientos y Champiñones al Jugo",
                    "side_dish_name": "Ejotes Tiernos Salteados en Mantequilla con Láminas de Almendra",
                    "fat_g": 52.5,
                    "protein_g": 49.0,
                    "net_carbs_g": 5.0,
                    "starter": {
                        "title": "Caldo Rústico de Hortalizas y Fondo Claro con Cilantro Fresco",
                        "technique": "boil_and_blend",
                        "note": "Caldo reconfortante de fin de semana con hortalizas de la granja cocidas en fondo claro.",
                        "ingredients": [
                            {"name": "Calabacitas verdes tiernas", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Apio fresco", "amount": 120, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 20},
                            {"name": "Fondo claro de pollo", "amount": 600, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 100},
                            {"name": "Cilantro fresco", "amount": 18, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Cocción: Cortar apio y calabacitas en media luna; cocer en fondo hirviendo durante 5 minutos a 90°C.",
                            "2. Pase: Retirar del fuego, añadir cilantro fresco picado y sal de mar; servir caliente."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Hervor suave para mantener el fondo transparente.",
                            "flavor_and_aromatics": "Fondo limpio perfumado con hierbas frescas.",
                            "textural_architecture": "Caldo cristalino con mordida vegetal tierna.",
                            "critical_control_points": "No hervir a borbotones."
                        },
                        "broth_volume_ml": 100,
                        "deglaze_agent": "Fondo de pollo",
                        "service_temp_c": 70,
                        "texture_target": "Límpido con verduras al dente",
                        "service_notes": "Servir en tazones de barro o cerámica."
                    },
                    "main_dish": {
                        "title": "Puntas de Filete de Res Salteadas con Pimientos y Champiñones al Jugo",
                        "technique": "saute_and_sear",
                        "note": "Filete de res magro cortado en bocados y salteado a fuego muy vivo con pimientos morrones y champiñones en reducción de jugo de carne y mantequilla.",
                        "ingredients": [
                            {"name": "Carne molida / Filete de Sirloin magro", "amount": 900, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 150},
                            {"name": "Pimientos morrones dulces", "amount": 300, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 50},
                            {"name": "Champiñones Portobello", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Mantequilla de pastoreo", "amount": 70, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 11.6},
                            {"name": "Ajo fresco", "amount": 18, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Mise en place cárnica: Cortar el filete en cubos de 2 cm; sazonar con sal de mar y pimienta.",
                            "2. Salteo a fuego máximo: Calentar wok o sartén amplia con 30 g de mantequilla a 190°C; saltear las puntas de res en dos tandas durante 2 minutos hasta sellar la superficie dorada manteniendo el centro jugoso a 55°C; retirar a plato.",
                            "3. Salteo de vegetales y desglasado: En la misma sartén, añadir el resto de la mantequilla, el ajo laminado, pimientos y champiñones cortados en cuartos salteando durante 3 minutos; desglasar los jugos concentrados con 40 ml de fondo de res o agua mineral.",
                            "4. Unión final: Reincorporar la carne y sus jugos de reposo salteando todo junto durante 45 segundos para amalgamar sabores y servir de inmediato."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Salteo ultrarrápido (wok hei doméstico a 190°C) para caramelizar sin sobrecocer el músculo vacuno.",
                            "flavor_and_aromatics": "Umami cárnico intenso balanceado por la dulzura de los pimientos y la tierra noble del champiñón.",
                            "textural_architecture": "Bocados de carne tiernos y elásticos que se funden al masticar, con vegetales crocantes.",
                            "critical_control_points": "No saltear toda la carne junta para no bajar la temperatura de la sartén."
                        },
                        "broth_volume_ml": 40,
                        "deglaze_agent": "Jugo de carne y mantequilla",
                        "service_temp_c": 70,
                        "texture_target": "Jugoso, tierno y satinado",
                        "service_notes": "Servir en platos hondos con sus jugos calientes."
                    },
                    "side_dish": {
                        "title": "Ejotes Tiernos Salteados en Mantequilla con Láminas de Almendra",
                        "technique": "saute_and_sear",
                        "note": "Ejotes frescos de la granja salteados al dente con mantequilla y almendras tostadas.",
                        "ingredients": [
                            {"name": "Ejotes verdes", "amount": 480, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 80},
                            {"name": "Mantequilla de pastoreo", "amount": 50, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 8.3},
                            {"name": "Almendras fileteadas tostadas", "amount": 45, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 7.5},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Blanqueado: Cocinar ejotes en agua hirviendo con sal 2 minutos; enfriar en agua con hielo.",
                            "2. Salteo: Saltear en mantequilla fundida durante 2 minutos a fuego vivo.",
                            "3. Pase: Servir coronados con las almendras tostadas crujientes."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Choque térmico que bloquea la pérdida de clorofila.",
                            "flavor_and_aromatics": "Dulzura vegetal y mantequilla avellanada.",
                            "textural_architecture": "Mordida turgente y elástica con láminas quebradizas.",
                            "critical_control_points": "Secar perfectamente los ejotes tras el hielo."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla derretida",
                        "service_temp_c": 65,
                        "texture_target": "Al dente crujiente",
                        "service_notes": "Acompañar junto a las puntas de filete."
                    }
                },
                {
                    "meal_type": "Cena",
                    "starter_name": "Bastones de Zucchini al Limón con Sal Marina",
                    "main_dish_name": "Tacos en Hoja de Lechuga Sweet con Salpicón de Pollo y Guacamole",
                    "side_dish_name": "Infusión Nocturna con Bisglicinato de Magnesio y Fórmula 34Plus®",
                    "fat_g": 36.0,
                    "protein_g": 41.0,
                    "net_carbs_g": 3.6,
                    "starter": {
                        "title": "Bastones de Zucchini al Limón con Sal Marina",
                        "technique": "raw_assembly",
                        "note": "Apertura ligera y refrescante.",
                        "ingredients": [
                            {"name": "Calabacitas verdes tiernas", "amount": 300, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 50},
                            {"name": "Jugo de limón fresco", "amount": 20, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Corte: Cortar en bastones finos.",
                            "2. Aliño: Servir con jugo de limón y sal marina."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Ensamble frío.",
                            "flavor_and_aromatics": "Fresco y crujiente.",
                            "textural_architecture": "Acuoso y turgente.",
                            "critical_control_points": "Servir al momento."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 8,
                        "texture_target": "Crocante",
                        "service_notes": "Servir en platos refrigerados."
                    },
                    "main_dish": {
                        "title": "Tacos en Hoja de Lechuga Sweet con Salpicón de Pollo y Guacamole",
                        "technique": "raw_assembly",
                        "note": "Tacos keto sin gluten amortizando la Lechuga Sweet de Sam's Club, rellenos de pechuga de pollo deshebrada, aguacate Hass machacado y cilantro fresco.",
                        "ingredients": [
                            {"name": "Pechuga de pollo", "amount": 720, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 120},
                            {"name": "Lechuga Sweet", "amount": 240, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 40},
                            {"name": "Aguacate Hass fresco", "amount": 3, "unit": "piezas", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 0.5},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 30, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5},
                            {"name": "Cilantro fresco", "amount": 18, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3},
                            {"name": "Jugo de limón fresco", "amount": 20, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 3.3},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Pollo deshebrado: Deshebrar la pechuga de pollo cocida y saltear ligeramente con 10 ml de VEVO y sal de mar para atemperar.",
                            "2. Guacamole rústico: Machacar el aguacate con cilantro picado, jugo de limón y sal marina.",
                            "3. Hojas cóncavas: Disponer las hojas limpias y secas de lechuga sweet en forma de taco.",
                            "4. Relleno y pase: Colocar el pollo deshebrado tibio dentro de cada hoja y coronar con una cucharada generosa de guacamole fresco."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Contraste de hoja fría crocante (8°C) con pollo tibio (45°C) y guacamole cremoso a temperatura ambiente.",
                            "flavor_and_aromatics": "Frescura vegetal de la lechuga ensalzando la suavidad del pollo y la riqueza untuosa del aguacate.",
                            "textural_architecture": "Crocancia acústica inicial que da paso a una fibra tierna y un puré sedoso.",
                            "critical_control_points": "Secar meticulosamente la lechuga para que no humedezca las manos del comensal."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 35,
                        "texture_target": "Crocante, tierno y cremoso",
                        "service_notes": "Servir en bandejas de madera para degustar con las manos."
                    },
                    "side_dish": {
                        "title": "Infusión Nocturna con Bisglicinato de Magnesio y Fórmula 34Plus®",
                        "technique": "steeping_and_infusion",
                        "note": "Poción nocturna reparadora con 34Plus®, bisglicinato de magnesio e infusión botánica de manzanilla para conciliación óptima del descanso de fin de semana.",
                        "ingredients": [
                            {"name": "Flores de manzanilla y azahar", "amount": 20, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 3.3},
                            {"name": "Fórmula Reparadora 34Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Infusión: Calentar agua a 88°C e infusionar las flores durante 6 minutos.",
                            "2. Filtrado: Colar y templar a 48°C.",
                            "3. Disolución: Añadir la Fórmula 34Plus® removiendo hasta disolución cristalina.",
                            "4. Pase: Servir tibia en tazas térmicas."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Temperatura agradable que induce vasodilatación periférica y calma fisiológica previa al sueño.",
                            "flavor_and_aromatics": "Aroma sutil floral y notas apacibles.",
                            "textural_architecture": "Líquido tibio, sedoso y muy relajante.",
                            "critical_control_points": "Tomar 30 minutos antes de apagar las luces."
                        },
                        "broth_volume_ml": 120,
                        "deglaze_agent": "N/A",
                        "service_temp_c": 46,
                        "texture_target": "Tibio, límpido y relajante",
                        "service_notes": "Servir en tazas de cerámica tibia."
                    }
                }
            ]
        }
    ]
