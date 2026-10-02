# -*- coding: utf-8 -*-
"""
Generador Maestro y Compilador SSOT para la Semana 41 (04 al 10 de Octubre de 2026)
Ecosistema NutriKeto Atelier T.I.L.O.®
Construye:
1. semana_41_master.json (Estructura canónica completa de 7 días, 21 servicios, 63 platos, COCT y métricas culinarias)
2. expediente_completo_semana_41.md (Expediente Clínico Integral en 5 secciones)
3. Sincronización en el directorio de artefactos del brain
"""

import os
import sys
import json
import re

# Ensure root is in path
sys.path.insert(0, os.path.abspath('.'))

def build_s41_full_data():
    days_data = [
        # -------------------------------------------------------------
        # DOMINGO 04 DE OCTUBRE DE 2026
        # -------------------------------------------------------------
        {
            "day": "Domingo",
            "date_str": "04 Oct",
            "day_num": "04",
            "month": "Octubre",
            "full_date_title": "Domingo 04 de Octubre de 2026",
            "iso_date": "2026-10-04",
            "meals": [
                {
                    "meal_type": "Desayuno",
                    "starter_name": "Tazón de Fresas Silvestres y Semillas de Chía con Almendras Fileteadas",
                    "main_dish_name": "Huevos Revueltos a la Mantequilla con Chayote Tierno Salteado y Finas Hierbas",
                    "side_dish_name": "Gelatina Artesanal de Fresas y Menta (4°C) con Fórmula Nootrópica 33Plus®",
                    "fat_g": 38.5,
                    "protein_g": 35.8,
                    "net_carbs_g": 5.4,
                    "starter": {
                        "title": "Tazón de Fresas Silvestres y Semillas de Chía con Almendras Fileteadas",
                        "technique": "raw_assembly",
                        "note": "Apertura cetogénica antioxidante rica en antocianinas y flavonoides, con textura crocante de almendra tostada y fibra mucilaginosa de chía.",
                        "ingredients": [
                            {"name": "Fresas frescas", "amount": 300, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 50},
                            {"name": "Semillas de chía orgánicas", "amount": 48, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 8},
                            {"name": "Almendras fileteadas tostadas", "amount": 90, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 15}
                        ],
                        "steps": [
                            "1. Cadena de frío e inspección: Lavar y desinfectar las fresas manteniéndolas a 4°C; secar sobre paño absorbente y cortar en cuartos longitudinales.",
                            "2. Hidratación ligera: Disponer las fresas en el fondo del cuenco y espolvorear la chía permitiendo que los jugos de corte comiencen una hidratación superficial sin colapsar.",
                            "3. Pase y coronación: Integrar las almendras fileteadas tostadas a 140°C en seco al momento del servicio para preservar crocancia acústica."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cadena de frío estricta (4°C a 10°C). Sin intervención térmica para preservar enzimas activas y vitamina C termosensible.",
                            "flavor_and_aromatics": "Acidez vibrante de la fresa equilibrada por las notas a nuez tostada y la neutralidad lipídica de la chía.",
                            "textural_architecture": "Turgencia jugosa de la fresa en contraste con la delgadez quebradiza de la almendra fileteada.",
                            "critical_control_points": "Secado riguroso por gravedad; adición de almendra estrictamente al pase."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A (Ensamble en Frío)",
                        "service_temp_c": 8,
                        "texture_target": "Fresco, crujiente y jugoso",
                        "service_notes": "Servir en cuencos refrigerados a 4°C."
                    },
                    "main_dish": {
                        "title": "Huevos Revueltos a la Mantequilla con Chayote Tierno Salteado y Finas Hierbas",
                        "technique": "saute_and_sear",
                        "note": "Plato fuerte matutino de alta densidad proteica y leucina (≥2.5 g), con cuajada cremosa de 3 huevos por comensal y chayote tierno amortizado de alacena.",
                        "ingredients": [
                            {"name": "Huevos orgánicos de pastoreo", "amount": 18, "unit": "piezas", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 3},
                            {"name": "Chayotes tiernos pelados", "amount": 1, "unit": "piezas", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 0.16},
                            {"name": "Mantequilla de pastoreo", "amount": 90, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 15},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1},
                            {"name": "Cebollín fresco de la granja", "amount": 30, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 5}
                        ],
                        "steps": [
                            "1. Mise en place de hortaliza: Pelar el chayote tierno de alacena y cortarlo en brunoise fina de 3 mm; blanquear en agua hirviendo con sal durante 90 segundos para ablandar sin perder turgencia; escurrir perfectamente.",
                            "2. Batido suave: Cascar los 18 huevos en cuenco hondo de acero; sazonar con la sal de mar y batir con tenedor durante 30 segundos rompiendo chalazas sin incorporar aire espumoso.",
                            "3. Salteo de fondo: Fundir 40 g de mantequilla en sartén antiadherente amplia a 125°C; incorporar el chayote y cebollín salteando durante 2 minutos hasta impregnar aroma sin tomar color.",
                            "4. Cuajado térmico controlado: Añadir el resto de la mantequilla, verter los huevos y reducir el fuego al mínimo (110°C). Remover en círculos concéntricos con espátula de silicón formando pliegues suaves y húmedos durante 3 minutos. Retirar del fuego con textura cremosa y jugosa a 65°C."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Desnaturalización controlada de ovoalbúmina (62°C a 68°C). La grasa de pastoreo emulsiona la fase acuosa previniendo la sinéresis del huevo.",
                            "flavor_and_aromatics": "Complejidad láctea avellanada con notas herbáceas frescas de cebollín y la dulzura vegetal neutra del chayote.",
                            "textural_architecture": "Cuajada suntuosa aterciopelada salpicada por la resistencia tierna y crujiente del chayote en brunoise.",
                            "critical_control_points": "Retirar del calor directo 15 segundos antes del punto deseado; el calor residual finaliza la cocción."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "N/A (Fuego Suave)",
                        "service_temp_c": 65,
                        "texture_target": "Baveuse, sedosa y untuosa",
                        "service_notes": "Servir de inmediato en platos tibios para evitar el enfriamiento de la grasa láctea."
                    },
                    "side_dish": {
                        "title": "Gelatina Artesanal de Fresas y Menta (4°C) con Fórmula Nootrópica 33Plus®",
                        "technique": "gelatin_molding",
                        "note": "Vehículo biotecnológico matutino que aporta colágeno hidrolizado puro, adaptógenos y L-Teanina para sostener el enfoque cognitivo matutino.",
                        "ingredients": [
                            {"name": "Fresas frescas", "amount": 120, "unit": "g", "category": "🍓 Frutas de Bajo Índice Glucémico", "per_guest": 20},
                            {"name": "Grenetina natural en polvo", "amount": 42, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 7},
                            {"name": "Fórmula Nootrópica 33Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Hojas de menta fresca", "amount": 15, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 2.5},
                            {"name": "Agua purificada", "amount": 720, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 120}
                        ],
                        "steps": [
                            "1. Hidratación bloom: Hidratar la grenetina en 180 ml de agua purificada fría durante 8 minutos hasta formar una esponja compacta.",
                            "2. Infusión y disolución: Calentar el resto del agua a 70°C con las hojas de menta; retirar del fuego, retirar la menta y disolver la grenetina hidratada agitando con varilla.",
                            "3. Integración biotecnológica: Dejar enfriar el líquido a 42°C (temperatura segura que preserva los fitonutrientes termosensibles de 33Plus®); incorporar la Fórmula 33Plus® y las fresas trituradas rústicamente.",
                            "4. Moldeado y reposo: Repartir en 6 moldes refractarios de cristal y refrigerar a 4°C por 3 horas hasta lograr gelificación elástica cristalina."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Disolución a 60°C y templado a 42°C previo a inyección nootrópica. Blindaje térmico estricto de polifenoles y L-Teanina.",
                            "flavor_and_aromatics": "Fondo herbal refrescante de menta que mitiga el perfil mineral del colágeno, aromatizado con ésteres de fresa.",
                            "textural_architecture": "Gel firme pero de ruptura elástica suave en boca a 36°C.",
                            "critical_control_points": "Monitoreo con termómetro de cocina; no incorporar 33Plus® por encima de 45°C."
                        },
                        "broth_volume_ml": 120,
                        "deglaze_agent": "N/A (Gelificación)",
                        "service_temp_c": 4,
                        "texture_target": "Gel elástico cristalino",
                        "service_notes": "Mantener en cámara fría hasta el momento exacto del pase."
                    }
                },
                {
                    "meal_type": "Comida",
                    "starter_name": "Crema Sedosa de Calabacitas Tiernas al Ajo Rostizado y Aceite VEVO",
                    "main_dish_name": "Corte Magro de Ribeye de Res a la Parrilla con Mantequilla de Romero y Ajo",
                    "side_dish_name": "Espárragos Verdes Salteados al Limón con Láminas de Queso Parmesano",
                    "fat_g": 48.2,
                    "protein_g": 45.5,
                    "net_carbs_g": 4.8,
                    "starter": {
                        "title": "Crema Sedosa de Calabacitas Tiernas al Ajo Rostizado y Aceite VEVO",
                        "technique": "boil_and_blend",
                        "note": "Entrada reconfortante baja en carbohidratos que aprovecha la pulpa rica en agua y pectina de las calabacitas de la huerta, emulsionada con aceite VEVO.",
                        "ingredients": [
                            {"name": "Calabacitas verdes tiernas de la granja", "amount": 600, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 100},
                            {"name": "Ajo fresco", "amount": 18, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 3},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 60, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 10},
                            {"name": "Fondo claro de pollo casero", "amount": 480, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 80},
                            {"name": "Sal de mar", "amount": 6, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1}
                        ],
                        "steps": [
                            "1. Rostizado de base aromática: En olla de fondo grueso, calentar 20 ml de VEVO a 140°C y dorar suavemente las láminas de ajo hasta liberar aroma sin amargar.",
                            "2. Cocción corta: Incorporar las calabacitas cortadas en rodajas y el fondo claro hirviendo; cocer a hervor suave tapado durante 6 minutos fijando color esmeralda.",
                            "3. Emulsificación vorticial: Transferir al vaso de licuadora de alta potencia, añadir la sal de mar y procesar a máxima velocidad mientras se vierte el resto de VEVO en hilo continuo durante 60 segundos.",
                            "4. Pase: Rectificar textura sedosa y servir en platos hondos calientes."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Cocción ultracorta (6 min) para evitar degradación de clorofila. Emulsión mecánica lípido-agua que confiere sedosidad sin espesantes amiláceos.",
                            "flavor_and_aromatics": "Dulzura vegetal sutil con fondo profundo de ajo caramelizado y notas picantes frutales del aceite de oliva virgen extra.",
                            "textural_architecture": "Crema untuosa de baja viscosidad y alta cobertura palatal.",
                            "critical_control_points": "No sobrecocer la calabacita; emulsionar en caliente para lograr estabilidad coloidal."
                        },
                        "broth_volume_ml": 160,
                        "deglaze_agent": "Fondo claro de pollo",
                        "service_temp_c": 70,
                        "texture_target": "Terciopelo líquido homogéneo",
                        "service_notes": "Decorar con gotas crudas de VEVO y pimienta negra recién molida."
                    },
                    "main_dish": {
                        "title": "Corte Magro de Ribeye de Res a la Parrilla con Mantequilla de Romero y Ajo",
                        "technique": "saute_and_sear",
                        "note": "Proteína principal de máxima calidad biológica con reacción de Maillard superficial intensa y centro jugoso a término medio (54°C).",
                        "ingredients": [
                            {"name": "Corte magro de Ribeye de res premium", "amount": 900, "unit": "g", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 150},
                            {"name": "Mantequilla de pastoreo", "amount": 80, "unit": "g", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 13.3},
                            {"name": "Romero fresco", "amount": 10, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1.6},
                            {"name": "Ajo fresco machacado", "amount": 12, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 2},
                            {"name": "Sal de mar", "amount": 8, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1.3}
                        ],
                        "steps": [
                            "1. Atemperado y secado: Retirar la carne del frío 30 minutos antes; secar minuciosamente la superficie con papel absorbente para asegurar caramelización inmediata.",
                            "2. Sellado a alta temperatura: Calentar plancha o sartén de hierro colado a 180°C; colocar los medallones sazonados con sal de mar y sellar 3 minutos por lado sin mover.",
                            "3. Arrosé aromático: En el último minuto, añadir la mantequilla, los dientes de ajo machacados y el romero; baar continuamente la carne con la mantequilla espumosa avellanada.",
                            "4. Reposo miogénico: Retirar sobre rejilla tibia y dejar reposar 4 minutos para redistribución osmótica de jugos antes de trinchar."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Reacción de Maillard (150°C a 165°C) que sintetiza pirazinas y furanos aromáticos. Desnaturalización de mioglobina controlada a 54°C interno.",
                            "flavor_and_aromatics": "Umami cárnico profundo acentuado por la grasa butírica infusionada con terpenos de romero y alicina tostada.",
                            "textural_architecture": "Corteza crujiente y crocante con núcleo tierno, húmedo y elástico que cede al corte.",
                            "critical_control_points": "Superficie de carne completamente seca al entrar al hierro; reposo obligatorio de 4 min."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Mantequilla espumosa aromática",
                        "service_temp_c": 56,
                        "texture_target": "Corteza crujiente, centro jugoso y suave",
                        "service_notes": "Trinchar en láminas de 1 cm perpendicular a la fibra muscular."
                    },
                    "side_dish": {
                        "title": "Espárragos Verdes Salteados al Limón con Láminas de Queso Parmesano",
                        "technique": "saute_and_sear",
                        "note": "Acompañamiento vegetal crujiente rico en asparagina, ácido fólico y potasio, con acidez cítrica desengrasante y umami curado de parmesano.",
                        "ingredients": [
                            {"name": "Espárragos verdes frescos de la granja", "amount": 480, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 80},
                            {"name": "Queso Parmesano artesanal", "amount": 60, "unit": "g", "category": "🧀 Lácteos y Quesos (Sin Gluten — Keto)", "per_guest": 10},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 30, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5},
                            {"name": "Jugo de limón fresco", "amount": 25, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 4.1},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Calibración: Retirar el tercio leñoso inferior de los espárragos mediante quiebre natural.",
                            "2. Salteo vivo: Calentar el aceite VEVO en sartén amplia a 160°C; disponer los espárragos en una sola capa y saltear 4 minutos rotándolos hasta lograr un tierno crujiente.",
                            "3. Desglasado cítrico: Verter el jugo de limón recién exprimido levantando los azúcares naturales del fondo y retirar del fuego.",
                            "4. Acabado: Servir calientes y coronar con láminas finas de queso parmesano recién cortadas con pelador."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Calor rápido en medio lipídico que reblandece la celulosa manteniendo la pectina estructural firme (al dente).",
                            "flavor_and_aromatics": "Amargor verde primaveral equilibrado por la salinidad cítrica del limón y el glutamato natural del parmesano.",
                            "textural_architecture": "Tallo flexible y crujiente con cubierta umami fundente de queso.",
                            "critical_control_points": "No sobrecocer; los espárragos deben mantener color verde brillante y resistencia al dente."
                        },
                        "broth_volume_ml": 0,
                        "deglaze_agent": "Jugo de limón fresco recién exprimido",
                        "service_temp_c": 60,
                        "texture_target": "Al dente, turgente y crujiente",
                        "service_notes": "Montar alineados en paralelo junto al corte de carne."
                    }
                },
                {
                    "meal_type": "Cena",
                    "starter_name": "Tazón de Caldo Claro de Huesos con Cilantro Fresco y Limón",
                    "main_dish_name": "Sardinas al Sartén con Salsa Rústica de Tomate Verde, Cilantro y Aguacate Hass",
                    "side_dish_name": "Infusión Digestiva de Manzanilla y Azahar con Fórmula Reparadora 34Plus®",
                    "fat_g": 36.5,
                    "protein_g": 41.2,
                    "net_carbs_g": 3.6,
                    "starter": {
                        "title": "Tazón de Caldo Claro de Huesos con Cilantro Fresco y Limón",
                        "technique": "boil_and_blend",
                        "note": "Elíxir mineral reconfortante rico en glicina, prolina y electrolitos biodisponibles que prepara el tracto digestivo nocturno.",
                        "ingredients": [
                            {"name": "Caldo concentrado y fondo de res casero", "amount": 600, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 100},
                            {"name": "Cilantro fresco de la granja", "amount": 24, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 4},
                            {"name": "Jugo de limón fresco", "amount": 30, "unit": "ml", "category": "🍋 Cítricos y Ácidos Naturales", "per_guest": 5},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Clarificación térmica: Calentar el caldo de huesos a 85°C retirando cualquier impureza superficial con espumadera.",
                            "2. Infusión de aromas: Incorporar el jugo de limón y la sal de mar ajustando el perfil ácido-mineral.",
                            "3. Pase: Servir humeante en cuencos y añadir el cilantro fresco picado rústicamente al instante."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Temperatura de servicio a 75°C que dilata vasos gástricos y estimula la motilidad sin alterar los micronutrientes del cilantro.",
                            "flavor_and_aromatics": "Fondo profundo de colágeno cárnico contrastado con la frescura ácida y notas aldehídicas del cilantro.",
                            "textural_architecture": "Líquido traslúcido ligero con densidad coloidal envolvente.",
                            "critical_control_points": "Añadir cilantro y limón en el último segundo para evitar oxidación."
                        },
                        "broth_volume_ml": 100,
                        "deglaze_agent": "N/A (Fondo Claro)",
                        "service_temp_c": 75,
                        "texture_target": "Líquido límpido y reconfortante",
                        "service_notes": "Servir en tazas térmicas de cerámica."
                    },
                    "main_dish": {
                        "title": "Sardinas al Sartén con Salsa Rústica de Tomate Verde, Cilantro y Aguacate Hass",
                        "technique": "saute_and_sear",
                        "note": "Cena antiinflamatoria de altísimo valor en ácidos grasos Omega-3 (EPA/DHA), calcio y fósforo, amortizando sardinas y tomate verde del inventario.",
                        "ingredients": [
                            {"name": "Sardinas enlatadas", "amount": 1, "unit": "latas", "category": "🥩 Carnes, Pescados y Proteínas", "per_guest": 0.16},
                            {"name": "Tomate verde fresco", "amount": 360, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 60},
                            {"name": "Aguacate Hass fresco", "amount": 2, "unit": "piezas", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 0.33},
                            {"name": "Cebolla blanca fresca", "amount": 60, "unit": "g", "category": "🥬 Verduras, Hortalizas y Frescos", "per_guest": 10},
                            {"name": "Aceite de oliva extra virgen VEVO", "amount": 30, "unit": "ml", "category": "🥑 Grasas, Aceites y Semillas", "per_guest": 5},
                            {"name": "Sal de mar", "amount": 4, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 0.6}
                        ],
                        "steps": [
                            "1. Tueste de salsa rústica: En comal o sartén seco a 170°C, tatemar los tomates verdes y la cebolla blanca hasta que la piel muestre manchas oscuras; majar en molcajete o pulsar en procesador con sal de mar y cilantro.",
                            "2. Salteo y sellado: Calentar el aceite VEVO en sartén a 130°C; verter la salsa verde rústica cocinando 3 minutos; acomodar con cuidado los lomos de sardina escurridos dejando que se impregnen del guisado durante 2 minutos sin romper los filetes.",
                            "3. Montaje graso: Disponer las sardinas guisadas con su salsa tibia y acompañar con abanicos de aguacate Hass fresco sazonados con un toque de sal mineral."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Tatemado de tomate verde que concentra pectinas y neutraliza acidez punzante. Tratamiento suave de la sardina para no oxidar los ácidos grasos poliinsaturados.",
                            "flavor_and_aromatics": "Acidez ahumada de tomate verde y cebolla rostizada que corta la intensidad grasa de la sardina azul y se redondea con el aguacate.",
                            "textural_architecture": "Carne suave y desmenuzable de pescado azul sobre salsa untuosa rústica con cremosidad mantecosa de aguacate.",
                            "critical_control_points": "No agitar violentamente la sartén para mantener íntegros los lomos de sardina."
                        },
                        "broth_volume_ml": 60,
                        "deglaze_agent": "Salsa tatemada de tomate verde",
                        "service_temp_c": 60,
                        "texture_target": "Guisado rústico tierno y cremoso",
                        "service_notes": "Servir tibio con el aguacate a temperatura ambiente."
                    },
                    "side_dish": {
                        "title": "Infusión Digestiva de Manzanilla y Azahar con Fórmula Reparadora 34Plus®",
                        "technique": "steep_beverage",
                        "note": "Cierre crepuscular neuro-metabólico con inductores de GABA, cromo e inulina de agave para estabilización nocturna de la glucosa y autofagia celular.",
                        "ingredients": [
                            {"name": "Flores de manzanilla seca", "amount": 18, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 3},
                            {"name": "Flores de azahar", "amount": 10, "unit": "g", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 1.6},
                            {"name": "Fórmula Reparadora 34Plus®", "amount": 30, "unit": "g", "category": "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA", "per_guest": 5},
                            {"name": "Agua purificada", "amount": 900, "unit": "ml", "category": "🌶️ Chiles, Condimentos e Infusiones", "per_guest": 150}
                        ],
                        "steps": [
                            "1. Infusión botánica: Calentar el agua purificada a 90°C; apagar el fuego, verter las flores de manzanilla y azahar y tapar durante 6 minutos extrayendo aceites esenciales calmantes.",
                            "2. Filtrado: Colar sobre jarra térmica.",
                            "3. Incorporación celular: Dejar atemperar la infusión hasta 55°C (umbral biológico seguro); disolver la Fórmula 34Plus® con agitador magnético o batidor mini asegurando completa dispersión coloidal.",
                            "4. Servicio nocturno: Servir en tazas precalentadas 45 minutos antes de dormir."
                        ],
                        "coct_reasoning": {
                            "thermodynamics": "Infusión tapada para no volatilizar apigenina y terpenos. Incorporación de 34Plus a 55°C para garantizar integridad de enzimas y fibra prebiótica.",
                            "flavor_and_aromatics": "Fondo floral dulce y relajante de manzanilla y azahar con final limpio sin amargor.",
                            "textural_architecture": "Tisana sedosa, ligera y cálida.",
                            "critical_control_points": "No hervir las flores directamente; servir a temperatura reconfortante de 52°C."
                        },
                        "broth_volume_ml": 150,
                        "deglaze_agent": "N/A (Infusión Caliente)",
                        "service_temp_c": 52,
                        "texture_target": "Infusión traslúcida aromática",
                        "service_notes": "Tomar en ambiente de luz cálida tenue."
                    }
                }
            ]
        }
    ]
    return days_data

print("Script template ready")
