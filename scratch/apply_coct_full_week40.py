# -*- coding: utf-8 -*-
"""
Motor CoCT: Escalado Completo Semana 40 (Domingo, Martes, Miércoles, Jueves, Viernes, Sábado)
Aplica la Arquitectura Cognitiva Dual a los 6 días restantes:
- Bloque `coct_reasoning` estructurado (termodinámica, sabor/aromas, arquitectura de textura, puntos críticos).
- Pasos dinámicos (`steps: string[]`) según la técnica real del plato (3 a 5 pasos).
- Prosa libre de contabilidad aritmética.
- 100% de preservación de ingredientes, gramajes, macros y BOM 3D.
"""

import json

COCT_WEEK_DATA = {
    "Domingo": {
        "desayuno": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (4°C a 10°C). Sin calor. Preserva antocianinas y polifenoles intactos frente a estrés oxidativo.",
                    "flavor_and_aromatics": "Acidez silvestre terrosa de la mora contrastada con la dulzura tostada y aceites lípidos de la almendra fileteada; chía neutra como estabilizador.",
                    "textural_architecture": "Contraste de drupeolos túrgidos con láminas crocantes de almendra y toque seco perlado de chía.",
                    "critical_control_points": "Secado por gravedad sobre papel absorbente para no magullar moras; almendras tostadas a 140°C en seco previamente; chía al pase."
                },
                "steps": [
                    "1. Acondicionamiento y Cadena de Frío: Inspeccionar las moras frescas manteniéndolas a 4°C; secar con delicadeza sobre papel absorbente para evitar rotura celular.",
                    "2. Tostado Aromático de Almendras: Verificar el tostado ligero en seco de las almendras fileteadas a 140°C hasta obtener una coloración marfil y aroma a nuez.",
                    "3. Montaje y Servicio Inmediato: Disponer las moras enteras en cuencos fríos; intercalar las almendras fileteadas y espolvorear la chía seca en la superficie justo antes del pase."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Desnaturalización de ovoalbúmina y vitelina (62°C a 68°C). Blanqueado de ejotes fija clorofila y previene pérdida hídrica. La cuajada de huevo debe quedar tierna y húmeda por calor residual sin sobrecocer.",
                    "flavor_and_aromatics": "Base lipídica de mantequilla artesanal con notas avellanadas sutiles que abrazan el amargor fresco del ejote blanqueado y la salinidad mineral de Colima.",
                    "textural_architecture": "Cuajada de huevo aterciopelada y cremosa salpicada por la resistencia crocante y elástica del ejote al dente.",
                    "critical_control_points": "Blanquear ejotes 3 min y sumergir en hielo; sartén a fuego medio-bajo (120°C a 130°C); remover con espátula de silicona en ondas lentas; retirar antes de secar la cuajada."
                },
                "steps": [
                    "1. Blanqueado y Choque Térmico de Ejotes: Cortar los ejotes en segmentos de 3 cm; sumergir en agua hirviendo con sal durante 3 minutos y cortar cocción inmediatamente en baño de hielo para fijar la clorofila; escurrir y secar perfectamente.",
                    "2. Homogeneización Proteica en Crudo: Cascar los huevos en un cuenco hondo; sazonar con la sal de mar mineral y batir con batidor de globo durante 40 segundos rompiendo chalazas hasta lograr una masa lisa sin espuma de aire.",
                    "3. Salteo Aromático de Hortaliza: Fundir la mitad de la mantequilla en sartén gruesa a 125°C; saltear los ejotes blanqueados durante 90 segundos para impregnar el medio lipídico sin dorar.",
                    "4. Cuajado Lento y Conducción Residual: Incorporar el resto de la mantequilla, verter los huevos batidos y reducir el fuego al mínimo. Revolver con espátula de silicón desde los bordes hacia el centro formando pliegues suaves y húmedos durante 3 minutos. Retirar del fuego y servir a 65°C con textura jugosa."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Hidratación de grenetina a 15°C y disolución a 60°C. La adición de la fórmula 33Plus se realiza a 45°C para blindar L-teanina y fitonutrientes activos. Gelificación a 4°C.",
                    "flavor_and_aromatics": "Fondo herbal refrescante de frutos rojos y menta que neutraliza la astringencia del colágeno, aromatizado con moras frescas.",
                    "textural_architecture": "Gel translúcido con firmeza elástica y disolución suave en boca a temperatura corporal.",
                    "critical_control_points": "Hidratar grenetina 8 min en agua fría; disolver a 60°C; incorporar 33Plus a 45°C; reposo de 3 horas a 4°C."
                },
                "steps": [
                    "1. Infusión Base y Maceración: Preparar la infusión de frutos rojos y menta, dejando enfriar a temperatura ambiente; macerar suavemente las moras enteras para liberar aromas.",
                    "2. Hidratación Bloom de Grenetina: Hidratar la grenetina en el agua purificada fría durante 8 minutos hasta constituir una matriz gelificada homogénea.",
                    "3. Disolución Controlada e Inyección Nootrópica: Calentar la infusión a 60°C y fundir la grenetina hidratada con agitación constante. Dejar descender la temperatura a 45°C e integrar la Fórmula Nootrópica 33Plus® y las moras maceradas.",
                    "4. Moldeado y Reticulación Nocturna: Repartir en moldes individuales y refrigerar a 4°C por un mínimo de 3 horas hasta consolidar gel elástico cristalino. Servir frío."
                ]
            }
        },
        "comida": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cocción suave de flavonoides y pigmentos carotenoides de la flor de calabaza (80°C a 85°C). La caseína del queso de cabra se emulsiona sin hervir para evitar grumos.",
                    "flavor_and_aromatics": "Dulzura floral vegetal envuelta en la acidez láctica untuosa del queso de cabra artesanal y la riqueza de la mantequilla.",
                    "textural_architecture": "Sopa aterciopelada y satinada con consistencia nappe densa sin almidones añadidos.",
                    "critical_control_points": "Retirar pistilos y cálices amargos de la flor; sudar en mantequilla sin dorar; emulsionar queso a fuego apagado; procesar a alta velocidad."
                },
                "steps": [
                    "1. Limpieza y Despunte Botánico: Retirar cuidadosamente los tallos, pistilos y cálices verdes de las flores de calabaza; enjuagar y secar sobre paño limpio.",
                    "2. Sudado Aromático en Mantequilla: En cazuela honda, fundir la mantequilla a 110°C; incorporar las flores de calabaza y sudar a fuego suave durante 3 minutos hasta que colapsen liberando su néctar vegetal.",
                    "3. Cocción en Fondo y Licuado Térmico: Verter el caldo casero caliente y la sal de mar mineral; cocinar a fuego bajo (85°C) durante 6 minutos. Trasvasar a vaso de licuadora de alta potencia, añadir el queso de cabra desmoronado y procesar durante 90 segundos hasta conseguir una crema tersa y homogénea.",
                    "4. Colado y Servicio Caliente: Pasar por colador fino a la cazuela tibia, rectificar textura a 70°C y servir en tazones precalentados."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Reacción de Maillard rápida a 190°C en superficie de arrachera para desarrollar compuestos pirazínicos aromáticos, manteniendo el centro a 54°C (término medio jugoso). Mantequilla de ajo compuesta aplicada en reposo por calor residual.",
                    "flavor_and_aromatics": "Fondo cárnico profundo con costra caramelizada; el ajo confitado aporta notas dulces sin acritud y el tomillo fresco libera timol en la grasa tibia.",
                    "textural_architecture": "Exterior crujiente y sellado; interior tierno con fibras musculares jugosas que se cortan fácilmente contra la veta.",
                    "critical_control_points": "Atemperar la carne 20 min antes del fuego; secar superficie con papel absorbente; parrilla o sartén de hierro muy caliente; reposo de 5 min antes de trinchar."
                },
                "steps": [
                    "1. Atemperado y Secado de la Proteína: Retirar la arrachera del frío 20 minutos antes; secar minuciosamente la superficie con papel absorbente para garantizar reacción de Maillard sin vapor.",
                    "2. Elaboración de Mantequilla de Ajo y Tomillo: En un cuenco, incorporar el ajo fresco machacado y el tomillo picado a la mantequilla pomada con una pizca de sal, formando una emulsión compacta.",
                    "3. Sellado a Alta Temperatura: Calentar la parrilla o sartén de hierro a 190°C con un velo de aceite de oliva extra virgen. Colocar la arrachera sazonada con sal mineral y sellar 2.5 minutos por lado sin mover hasta lograr costra dorada oscura y centro a 54°C.",
                    "4. Reposo Térmico y Montaje: Retirar a tabla tibia; colocar quenelles de mantequilla de ajo sobre la carne caliente para que funda sobre los jugos. Dejar reposar 5 minutos tapada holgadamente con papel aluminio antes de cortar en tiras perpendiculares a la fibra."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Rostizado a 180°C por calor seco convectivo. La celulosa de los espárragos se ablanda manteniendo turgencia al dente. El jugo de limón se aplica tras la cocción para preservar vitamina C.",
                    "flavor_and_aromatics": "Notas herbáceas y terrosas concentradas por la evaporación del agua superficial, abrillantadas por los polifenoles del aceite VEVO y la sal de Colima.",
                    "textural_architecture": "Tallo crocante con mordida elástica y puntas tiernas ligeramente tostadas.",
                    "critical_control_points": "Quebrar la base leñosa de los espárragos; hornear en una sola capa sin encimar a 180°C; aderezar con limón al salir del horno."
                },
                "steps": [
                    "1. Limpieza y Despunte Mecánico: Lavar los espárragos y quebrar con la mano el extremo fibroso inferior por su punto natural de ruptura; secar bien.",
                    "2. Aliño y Disposición en Bandeja: Disponer los espárragos en una charola para horno en una sola capa; barnizar con el aceite de oliva extra virgen y espolvorear la sal de mar mineral.",
                    "3. Rostizado Convectivo: Hornear a 180°C durante 10 a 12 minutos hasta que los tallos estén tiernos pero firmes y las puntas presenten un tostado sutil.",
                    "4. Toque Cítrico al Pase: Retirar del horno, rociar el jugo de limón natural fresco por toda la charola y transferir de inmediato como guarnición caliente."
                ]
            }
        },
        "cena": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (8°C a 12°C). Cero calor. Los lípidos monoinsaturados del aguacate Hass requieren corte limpio para evitar oxidación enzimática (polifenol oxidasa).",
                    "flavor_and_aromatics": "Untuosidad mantecosa vegetal enaltecida por el frutado del aceite de oliva virgen extra y la chispa crujiente de los granos de sal de Colima.",
                    "textural_architecture": "Textura cremosa y aterciopelada que se deshace en paladar, con contraste crocante mineral.",
                    "critical_control_points": "Aguacates en punto exacto de firmeza elástica; cortar inmediatamente antes del servicio; laminar con cuchillo humedecido."
                },
                "steps": [
                    "1. Corte y Deshuesado de Precisión: Cortar los aguacates por la mitad longitudinalmente, retirar el hueso con un toque seco de hoja y pelar la piel con cuchara amplia.",
                    "2. Laminado en Abanico: Realizar cortes finos paralelos de 3 mm sin llegar a la punta; presionar con la palma para desplegar en abanico armónico.",
                    "3. Aliño y Emplatado: Disponer en platos fríos; rociar con el aceite de oliva extra virgen en hilo fino y terminar con cristales de sal de mar mineral. Servir de inmediato."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Sellado unilateral con costra a 145°C. El pavo magro se seca con facilidad si supera 74°C internos. La costra de sésamo y Parmesano actúa como escudo térmico protector.",
                    "flavor_and_aromatics": "Fondo proteico suave protegido por las notas a nuez del sésamo tostado y el umami salino del queso Parmesano Reggiano fundido.",
                    "textural_architecture": "Costra dorada muy crujiente en el exterior con núcleo de pavo tierno y jugoso.",
                    "critical_control_points": "Rebozar solo una cara en sésamo y queso; sartén a fuego medio (145°C); no mover durante los primeros 3 min para asentar la costra; terminar a fuego suave."
                },
                "steps": [
                    "1. Porcionado y Secado de Medallones: Cortar la pechuga de pavo en medallones gruesos de 2 cm; secar sobre papel absorbente y sazonar ligeramente con sal mineral.",
                    "2. Formación de Costra Protectora: Mezclar en un plato plano las semillas de sésamo con el queso Parmesano rallado fino; presionar la cara superior de cada medallón sobre la mezcla para fijar una costra densa.",
                    "3. Sellado Crujiente de la Costra: Calentar la mantequilla y el aceite de oliva en sartén a fuego medio (145°C); colocar los medallones por el lado de la costra y dorar sin perturbar durante 3.5 minutos hasta crear costra dorada y firme.",
                    "4. Cocción Final y Reposo: Voltear delicadamente los medallones a fuego mínimo, tapar la sartén y cocinar 4 minutos más hasta alcanzar 74°C internos. Dejar reposar 3 minutos sobre tabla antes de servir."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Extracción hidrosoluble de aceites esenciales (citral, geraniol) a 85°C. La Fórmula 34Plus requiere temperatura inferior a 60°C para mantener bioactividad.",
                    "flavor_and_aromatics": "Aroma cítrico y herbal sedante del toronjil fresco que relaja el sistema nervioso central y prepara el reposo nocturno.",
                    "textural_architecture": "Infusión limpia, etérea y tibia.",
                    "critical_control_points": "Infundir tapado 5 minutos; atemperar a 55°C antes de verter 34Plus; mezclar con suavidad."
                },
                "steps": [
                    "1. Infusión Termocontrolada: Calentar el agua purificada a 85°C; añadir las hojas de toronjil limpio en tetera con émbolo, tapar e infusionar 5 minutos.",
                    "2. Colado y Descenso Térmico: Decantar la infusión y esperar a que la temperatura baje a 55°C en el termómetro.",
                    "3. Integración Celular y Servicio: Disolver los 30 g de Fórmula 34Plus® con cuchara de madera en el líquido tibio. Servir en tazas cerámicas tibias."
                ]
            }
        }
    },
    "Martes": {
        "desayuno": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (6°C a 10°C). Sin calor. Preserva ácido elágico y antocianinas de la granada.",
                    "flavor_and_aromatics": "Explosión agridulce y astringente limpia de los arilos combinada con la crocancia mantecosa de las almendras.",
                    "textural_architecture": "Arilos que estallan bajo presión dental, acompañados de láminas crujientes de almendra.",
                    "critical_control_points": "Desgranar granada sumergida en agua fría para eliminar membranas blancas amargas; escurrir; integrar chía seca al servir."
                },
                "steps": [
                    "1. Desgranado y Purificación Fría: Desgranar la granada en un bol con agua fría permitiendo que las membranas amargas floten; colar los arilos rojos y secar sobre paño.",
                    "2. Texturizado de Frutos Secos: Tostar ligeramente las almendras fileteadas en seco a 130°C hasta liberar aceites esenciales sin oscurecer.",
                    "3. Montaje al Pase: Disponer los arilos de granada en copas frías, espolvorear las almendras fileteadas y finalizar con las semillas de chía en la superficie."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Rehidratación lipídica de la carne seca sonorense a 120°C en mantequilla antes de incorporar huevo. La proteína seca absorbe humedad de las claras mientras cuajan suavemente a 65°C.",
                    "flavor_and_aromatics": "Profundo sabor umami cárnico concentrado por el secado artesanal, suavizado por la mantequilla y el orégano silvestre.",
                    "textural_architecture": "Hebra de machaca carnosa y maleable integrada dentro de una cuajada de huevo cremosa y jugosa.",
                    "critical_control_points": "Deshebrar la machaca finamente; sofreír 1 min en mantequilla para hidratar sin quemar; agregar huevos y retirar con calor residual."
                },
                "steps": [
                    "1. Acondicionamiento de la Machaca: Desmenuzar la machaca de res asegurando fibras finas y homogéneas; frotar el orégano silvestre entre las palmas para liberar aceites.",
                    "2. Rehidratación Lipídica en Sartén: Calentar la mantequilla en sartén a fuego medio-bajo (120°C); añadir la machaca y el orégano, sofriendo durante 90 segundos para que la fibra se impregne de grasa tibia.",
                    "3. Integración de Huevos y Batido Suave: Verter los 18 huevos previamente cascados y batidos con la sal de mar mineral.",
                    "4. Revuelto Cremoso y Servicio: Mover suavemente con espátula de silicón desde los bordes hacia el centro durante 2 a 3 minutos hasta cuajada brillante y untuosa. Retirar del fuego y servir de inmediato."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Disolución coloidal a 60°C; enfriamiento a 45°C para salvaguardar activos de 33Plus; consolidación a 4°C.",
                    "flavor_and_aromatics": "Fondo botánico de manzanilla y frutos rojos que armoniza la vibrante acidez de la granada.",
                    "textural_architecture": "Matriz de gel transparente con arilos suspendidos que explotan en boca.",
                    "critical_control_points": "Disolver grenetina sin grumos; atemperar infusión antes de añadir 33Plus; reposo en frío 3 horas."
                },
                "steps": [
                    "1. Infusión y Extracción: Preparar infusión de manzanilla y frutos rojos a 85°C; colar y atemperar; reservar arilos frescos en frío.",
                    "2. Hidratación de Grenetina: Espolvorear la grenetina en agua fría 8 minutos hasta esponjar.",
                    "3. Fusión Térmica e Incorporación de Activos: Calentar la infusión a 60°C, disolver la grenetina y enfriar a 45°C. Integrar la Fórmula 33Plus® y los arilos de granada.",
                    "4. Gelificación Controlada: Verter en copas y refrigerar a 4°C por 3 horas hasta textura firme y elástica."
                ]
            }
        },
        "comida": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Rostizado previo de coliflor a 190°C para caramelizar azúcares naturales por Maillard; cocción en caldo a 85°C y emulsión con queso de cabra.",
                    "flavor_and_aromatics": "Notas tostadas y acarameladas de la coliflor dorada equilibradas con la cremosidad ácida del queso de cabra y el toque aromático del ajo confitado.",
                    "textural_architecture": "Velouté denso, terso y sin grumos fibrosos.",
                    "critical_control_points": "Rostizar coliflor y ajo hasta bordes dorados; licuar en caliente a velocidad máxima; rectificar densidad con fondo casero."
                },
                "steps": [
                    "1. Rostizado de Coliflor y Ajo: Mezclar los floretes de coliflor y los dientes de ajo con una parte de mantequilla fundida; hornear a 190°C por 18 minutos hasta bordes dorados caramelizados.",
                    "2. Cocción en Fondo Claro: Trasladar la coliflor y el ajo a una cazuela, verter el caldo casero caliente y la sal mineral; cocer a fuego bajo por 8 minutos.",
                    "3. Emulsión Cremosa: Añadir el queso de cabra suave y el resto de la mantequilla; transferir a licuadora y triturar a alta velocidad durante 2 minutos hasta conseguir emulsión aterciopelada.",
                    "4. Servicio Caliente: Servir en tazones hondos precalentados a 70°C con un hilo sutil de aceite de oliva."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Sellado térmico a 180°C con mantequilla clarificada (Ghee) de alto punto de humo (250°C). Centro de sirloin a 52°C–54°C (jugoso). Desglasado con caldo y emulsión de eneldo.",
                    "flavor_and_aromatics": "Intensidad cárnica caramelizada complementada con la frescura anisada del eneldo y la riqueza láctea del Ghee.",
                    "textural_architecture": "Superficie dorada con resistencia crujiente; corazón fibroso sumamente blando y jugoso.",
                    "critical_control_points": "Carne a temperatura ambiente; sellar 2 min por cara sin mover; retirar medallones antes de verter caldo y eneldo para montar salsa."
                },
                "steps": [
                    "1. Atemperado y Salado de Sirloin: Secar los medallones de sirloin; sazonar con la sal de mar mineral 15 minutos antes de la cocción.",
                    "2. Sellado de Precisión en Ghee: Calentar sartén pesada de hierro a 180°C con la mitad del Ghee; sellar los medallones 2.5 minutos por lado hasta costra dorada oscura y centro a 54°C. Retirar a plato caliente para reposar.",
                    "3. Reducción y Emulsión de Eneldo: En la misma sartén caliente, verter el caldo de res concentrado raspando los jugos adheridos del fondo; añadir el resto del Ghee frío y el eneldo fresco picado, batiendo con varilla hasta salsa satinada.",
                    "4. Bañado y Emplatado: Servir los medallones de sirloin salseados con la emulsión aromática de eneldo recién montada."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Vaporización rápida a 100°C en recipiente tapado durante 6 minutos. Preserva celulosa crocante sin reblandecer el chayote. Lustrado en Ghee a 60°C.",
                    "flavor_and_aromatics": "Frescura vegetal suave y sutil enriquecida por las notas a nuez del Ghee purificado y sal de Colima.",
                    "textural_architecture": "Láminas translúcidas con mordida firme y húmeda.",
                    "critical_control_points": "Pelar y rebanar en láminas de 4 mm homogéneas; no sobrecocer en vapor; escurrir de inmediato."
                },
                "steps": [
                    "1. Rebanado Geométrico: Pelar los chayotes bajo agua fría y cortar en láminas uniformes de 4 mm con mandolina o cuchillo afilado.",
                    "2. Cocción al Vapor: Disponer las láminas en vaporera sobre agua hirviendo; tapar y cocer durante 6 minutos hasta consistencia al dente.",
                    "3. Lustrado en Ghee y Sal Marina: Retirar de la vaporera, transferir a sartén tibia con el Ghee fundido y saltear suavemente 1 minuto con la sal de mar mineral. Servir calientes."
                ]
            }
        },
        "cena": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cero calor. Choque en hielo para turgencia celular de zucchini y apio.",
                    "flavor_and_aromatics": "Notas amargas y refrescantes que despiertan el paladar con la acidez del limón natural.",
                    "textural_architecture": "Corteza vegetal muy crujiente y acuosa.",
                    "critical_control_points": "Cortar en bastones de 8 cm; inmersión de 5 min en hielo; secar antes de limón."
                },
                "steps": [
                    "1. Bastoneado de Vegetales: Cortar calabacitas y apio en bastones simétricos de 8 cm de largo por 1 cm de grosor.",
                    "2. Hidratación Osmótica: Sumergir en agua purificada con hielo durante 6 minutos para tensar tejidos.",
                    "3. Servicio Frío: Secar rigurosamente, montar en vasos y aliñar con gotas de limón fresco y sal mineral de Colima."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Horneado convectivo a 170°C. La miosina del pescado blanco cuaja a 55°C–58°C. El velo de aceite VEVO y finas hierbas evita la evaporación de jugos musculares.",
                    "flavor_and_aromatics": "Delicadeza marina marina limpia perfumada con aceites esenciales de tomillo, perejil y orégano.",
                    "textural_architecture": "Láminas de pescado que se desgajan en lascas jugosas y perladas con tenedor.",
                    "critical_control_points": "Secar filetes; pincelar con aceite VEVO; hornear exactamente 9 a 11 min a 170°C; gotas de limón al salir."
                },
                "steps": [
                    "1. Limpieza y Secado de Filetes: Disponer los filetes de pescado blanco en refractario para horno; secar suavemente con papel absorbente.",
                    "2. Maceración Aromática: Emulsionar el aceite de oliva extra virgen con las finas hierbas picadas y sal de mar; pintar pródigamente los filetes por ambas caras.",
                    "3. Horneado Convectivo: Introducir al horno precalentado a 170°C durante 10 minutos hasta que el centro alcance 58°C y la carne se separe en lascas blancas húmedas.",
                    "4. Pase con Cítrico: Rociar con unas gotas de limón fresco recién exprimido y servir caliente con sus propios jugos de horneado."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Infusión de manzanilla a 90°C para extraer camazuleno y flavonoides; atemperado a 55°C antes de 34Plus.",
                    "flavor_and_aromatics": "Aroma dulce floral reconfortante de flores de manzanilla pura que favorece la digestión nocturna.",
                    "textural_architecture": "Tisana cristalina y sedosa.",
                    "critical_control_points": "Infundir 5 min tapada; filtrar flores; añadir 34Plus a 55°C."
                },
                "steps": [
                    "1. Infusión Calmante: Infundir las flores de manzanilla en agua purificada a 90°C durante 5 minutos en tetera con filtro.",
                    "2. Decantado y Termocontrol: Filtrar la infusión y dejar reposar hasta alcanzar 55°C en el termómetro.",
                    "3. Adición de Micronutrientes: Incorporar los 30 g de Fórmula 34Plus® removiendo con suavidad hasta integrar. Servir tibia."
                ]
            }
        }
    },
    "Miércoles": {
        "desayuno": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (4°C a 10°C). Preserva antocianinas y flavonoides en arándanos enteros.",
                    "flavor_and_aromatics": "Contraste dulce y ácido frutal con los taninos grasos de la nuez pecana y las semillas de girasol tostadas.",
                    "textural_architecture": "Piel elástica de arándano que explota en líquido, escoltada por crujido de semillas y nuez.",
                    "critical_control_points": "Arándanos limpios y secos; tostar semillas de girasol en seco 2 min; montar sin aplastar."
                },
                "steps": [
                    "1. Selección en Frío: Seleccionar los arándanos frescos eliminando frutos magullados; mantener a 4°C y secar con papel absorbente.",
                    "2. Tostado Ligero de Girasol: Tostar las semillas de girasol en una sartén seca a fuego bajo durante 2 minutos para despertar notas tostadas.",
                    "3. Armado y Servicio: Distribuir los arándanos en cuencos, esparcir las nueces pecana troceadas y coronar con las semillas de girasol tostadas."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Montaje de nube de clara horneada a 180°C (espuma de ovoalbúmina cuajada a 70°C) con yema tierna fluida central; emulsión termocontrolada de holandesa a 58°C–62°C con mantequilla avellanada y limón.",
                    "flavor_and_aromatics": "Complejo untuoso y ácido de salsa holandesa casera balanceado con el ahumado salado del tocino de pavo y notas tostadas de Parmesano.",
                    "textural_architecture": "Nube aireada y esponjosa de clara con corazón de yema líquida caliente, cubierta de salsa cremosa satinada y tocino crujiente.",
                    "critical_control_points": "Montar claras a punto de nieve con sal; hornear nidos 4 min antes de depositar yemas; holandesa al baño María sin superar 63°C para que no se corte."
                },
                "steps": [
                    "1. Crujiente de Tocino de Pavo: Dorar las tiras de tocino de pavo en sartén a fuego medio hasta textura quebradiza; reservar sobre papel absorbente y picar en lardones finos.",
                    "2. Nubes de Clara al Horno: Separar yemas de claras guardando cada yema en cascarón o tacita; batir las claras a punto de turrón con una pizca de sal y la mitad del Parmesano. Formar 6 nidos sobre papel encerado y hornear a 180°C durante 4 minutos hasta dorar ligero.",
                    "3. Sellado Térmico de Yemas: Colocar una yema en el centro de cada nido de clara y hornear 2 minutos más hasta que la superficie de la yema esté brillante y sellada pero el interior completamente fluido.",
                    "4. Emulsión Holandesa y Napado: Batir 6 yemas con el jugo de limón a baño María suave (60°C); incorporar la mantequilla fundida en hilo continuo hasta formar salsa densa y satinada. Sazonar con sal mineral, bañar las nubes al salir del horno y coronar con el tocino de pavo crujiente."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Gelatina en frío a 4°C; disolución a 60°C y adición de 33Plus a 45°C. Retención molecular de bioactivos.",
                    "flavor_and_aromatics": "Fondo limpio de té blanco y frutos rojos con notas frescas de arándano.",
                    "textural_architecture": "Gel coloidal transparente y firme.",
                    "critical_control_points": "Hidratar grenetina 8 min; infundir té blanco 4 min a 80°C; enfriar a 45°C antes de 33Plus."
                },
                "steps": [
                    "1. Infusión de Té Blanco y Frutos Rojos: Infundir el té blanco a 80°C por 4 minutos; colar y reservar.",
                    "2. Hidratación de Colágeno: Hidratar la grenetina en agua fría durante 8 minutos.",
                    "3. Fusión e Integración Nootrópica: Disolver la grenetina en la infusión caliente (60°C), bajar temperatura a 45°C e integrar la Fórmula 33Plus® y los arándanos frescos enteros.",
                    "4. Reticulación Fría: Enfriar en refrigeración a 4°C durante 3 horas. Servir fría."
                ]
            }
        },
        "comida": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cocción suave de nopales a 90°C en medio ligeramente ácido para precipitar mucílago (baba). Clarificado del caldo a 80°C con epazote fresco.",
                    "flavor_and_aromatics": "Consomé transparente y profundo con notas terrosas de epazote fresco y acidez herbal de nopal tierno.",
                    "textural_architecture": "Caldo límpido y ligero con dados de nopal tiernos pero con mordida elástica.",
                    "critical_control_points": "Cocer cubos de nopal en agua hirviendo con sal 4 min y escurrir de inmediato para eliminar mucílago; integrar al consomé claro caliente al final."
                },
                "steps": [
                    "1. Purga y Corte de Nopales: Picar los nopales en cubos pequeños de 1 cm; blanquear en agua hirviendo con una pizca de sal durante 4 minutos, enjuagar con agua fría para eliminar mucílago y escurrir.",
                    "2. Clarificado e Infusión de Consomé: Calentar el caldo claro de ave a 85°C; añadir las hojas de epazote fresco y sal de mar mineral, infusionando a fuego mínimo durante 6 minutos.",
                    "3. Integración y Servicio: Retirar el epazote, incorporar los cubos de nopal purgados y unas gotas de aceite de oliva virgen extra. Servir humeante a 75°C en cuencos hondos."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Sellado inicial a 160°C para Maillard superficial; horneado suave a 160°C hasta 74°C internos. El relleno de queso crema y espinaca actúa como aislante térmico que mantiene húmeda la pechuga.",
                    "flavor_and_aromatics": "Fondo umami lácteo por crema, Parmesano y queso crema, equilibrado por el sabor vegetal fresco de las espinacas.",
                    "textural_architecture": "Exterior sellado con costra dorada; carne de ave suculenta rellena de crema fundente, napada en salsa untuosa.",
                    "critical_control_points": "Abrir pechugas en mariposa sin perforar fondo; cerrar con palillos; sellar con cuidado; salsa a fuego bajo (80°C)."
                },
                "steps": [
                    "1. Relleno Cremoso de Espinacas: Saltear las espinacas picadas en mantequilla 2 minutos hasta marchitar; mezclar con el queso crema, sal mineral y una pizca de Parmesano hasta obtener pasta suave.",
                    "2. Relleno y Sellado de Supremas: Realizar un bolsillo longitudinal en cada suprema de pollo; rellenar con la crema de espinacas y cerrar con palillo. Sellar en sartén a fuego medio-alto (160°C) con mantequilla durante 3 minutos por lado.",
                    "3. Horneado y Cocción Interna: Transferir las pechugas selladas al horno a 160°C durante 10 minutos hasta alcanzar 74°C en el centro.",
                    "4. Salsa de Parmesano al Nappe: En la sartén de sellado, verter la crema entera y desglasar el fondo; apagar el fuego, integrar el queso Parmesano rallado con varilla y salsear las pechugas al momento de servir."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Salteo flash a 150°C en aceite VEVO durante 3 min. Los ejotes conservan turgencia celular. Almendras incorporadas al final para no ablandar su costra.",
                    "flavor_and_aromatics": "Notas frescas de verdura verde combinadas con el tostado dulce de las almendras y sal marina.",
                    "textural_architecture": "Doble crujido: resistencia vegetal crujiente del ejote y fractura seca de la almendra tostada.",
                    "critical_control_points": "Ejotes despuntados y secos; sartén amplia caliente; almendras tostadas previamente añadidas al último minuto."
                },
                "steps": [
                    "1. Acondicionamiento de Ejotes: Despuntar los ejotes y cortar en mitades; secar rigurosamente con paño de cocina.",
                    "2. Salteo Vivo en VEVO: Calentar el aceite de oliva extra virgen en sartén amplia a fuego medio-alto (150°C); añadir los ejotes y saltear 3 minutos con sal de mar mineral.",
                    "3. Coronación con Almendras: Incorporar las almendras fileteadas tostadas en el último minuto de cocción para que se impregnen de los aromas sin perder crocancia. Servir de inmediato."
                ]
            }
        },
        "cena": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cero calor. Cadena de frío (4°C a 8°C). Choque en hielo para aumentar tensión en vacuolos celulares.",
                    "flavor_and_aromatics": "Astringencia acuosa fresca del pepino y calabacita con acidez cítrica brillante.",
                    "textural_architecture": "Crujiente acústico vibrante.",
                    "critical_control_points": "Retirar semillas; secar perfectamente del hielo; aliñar al instante."
                },
                "steps": [
                    "1. Corte de Bastones: Cortar pepino y calabacitas tiernas en bastones uniformes de 8 cm por 1 cm.",
                    "2. Hidratación en Frío Extremo: Dejar reposar 5 minutos en agua con hielo abundante; escurrir y secar sobre paño limpio.",
                    "3. Aderezo Cítrico Mineral: Acomodar en vasos individuales, bañar con el jugo de limón recién exprimido y rematar con sal de mar de Colima."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Cero calor. Cadena de frío para proteína de pavo cocida (4°C a 10°C). La grasa monoinsaturada del aguacate emulsiona con el limón y VEVO formando un aliño cremoso natural.",
                    "flavor_and_aromatics": "Frescura cítrica y notas aromáticas vivas de cilantro que realzan la pechuga de pavo suavemente sazonada.",
                    "textural_architecture": "Hebra de carne tierna y fibrosa abrazada por cubos sedosos de aguacate maduro.",
                    "critical_control_points": "Deshebrar el pavo muy fino en frío; cortar aguacate en cubos intactos; mezclar envolventemente con espátula de goma para no hacer puré el aguacate."
                },
                "steps": [
                    "1. Deshebrado de Pavo en Frío: Deshebrar finamente la pechuga de pavo horneada manteniéndola refrigerada a 4°C.",
                    "2. Emulsión Cítrica de Cilantro: En un tazón hondo, mezclar el jugo de limón fresco, el aceite de oliva extra virgen, el cilantro picado y la sal mineral, batiendo con tenedor hasta emulsionar.",
                    "3. Integración Envolvente de Aguacate: Cortar el aguacate Hass en dados de 1.5 cm; incorporar al tazón junto con el pavo deshebrado y mezclar con espátula en movimientos amplios envolventes para cubrir cada hebra sin romper el aguacate.",
                    "4. Montaje y Degustación: Disponer en platos fríos en timbal rústico y servir inmediatamente a temperatura fresca."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Infusión de toronjil a 85°C por 5 min; decantar y enfriar a 55°C antes de verter 34Plus.",
                    "flavor_and_aromatics": "Aroma herbal cítrico que estimula el nervio vago y la relajación neuromuscular nocturna.",
                    "textural_architecture": "Infusión traslúcida y reconfortante.",
                    "critical_control_points": "Tetera tapada; termómetro a 55°C; disolver suavemente."
                },
                "steps": [
                    "1. Infusión Relajante: Infundir las hojas de toronjil en agua caliente a 85°C durante 5 minutos en tetera con émbolo tapada.",
                    "2. Control Térmico: Decantar la tisana y dejar reposar hasta que la temperatura baje a 55°C.",
                    "3. Disolución de 34Plus: Incorporar los 30 g de Fórmula 34Plus® en lluvia fina, mezclando con cuchara de madera. Servir en tazas cerámicas."
                ]
            }
        }
    },
    "Jueves": {
        "desayuno": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (6°C a 10°C). Sin calor. Preserva betalaínas y mucílagos prebióticos de la pitaya.",
                    "flavor_and_aromatics": "Dulzura sutil y floral de la pitaya equilibrada por la riqueza tostada de la almendra, el coco rallado y la chía.",
                    "textural_architecture": "Cubos tiernos y pulposos con micro-semillas crujientes, coco sedoso y fractura seca de almendra.",
                    "critical_control_points": "Pelar la piel gruesa sin dañar la pulpa; cortar en dados homogéneos de 2 cm; servir frío."
                },
                "steps": [
                    "1. Corte de Pitaya: Retirar la corteza de las pitayas con cuidado; cortar la pulpa en dados uniformes de 2 cm y mantener en frío.",
                    "2. Tostado de Aromáticos Secos: Asegurar el tostado ligero de las almendras fileteadas y el coco rallado a 130°C.",
                    "3. Montaje y Servicio: Colocar los dados de pitaya en cuencos fríos, esparcir el coco y las almendras fileteadas tostadas, rematando con semillas de chía en la superficie."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Fritura plana en aceite VEVO a 160°C en sartén de hierro precalentada. La clara forma encaje crujiente dorado en la base mientras la yema se mantiene completamente líquida y caliente a 55°C por cocción unilateral convectiva de aceite rociado con cuchara.",
                    "flavor_and_aromatics": "Fondo afrutado de aceite de oliva extra virgen fundido con el timol del tomillo fresco liberado por choque térmico en la grasa caliente.",
                    "textural_architecture": "Puntilla (encaje) dorada crujiente en la base de la clara, clara superior vaporosa y yema untuosa y fluida que baña el plato.",
                    "critical_control_points": "Sartén de hierro a 160°C; cascar los huevos directo en el aceite caliente; bañar las claras con aceite caliente usando cuchara sin tocar las yemas; sazonar las yemas al final."
                },
                "steps": [
                    "1. Calentamiento y Aromatización de Aceite: Calentar el aceite de oliva extra virgen en sartén amplia de hierro fundido a 160°C; añadir las ramitas de tomillo fresco durante 15 segundos para perfumar la grasa sin carbonizar las hojas.",
                    "2. Cascar y Fritura Unilateral: Cascar los huevos cuidadosamente de dos en dos deslizándolos cerca del aceite caliente.",
                    "3. Técnica de Bañado con Cuchara (Basting): Inclinar ligeramente la sartén y, con una cuchara de metal, recoger el aceite caliente aromatizado y bañarlo sobre las claras alrededor de las yemas para cuajarlas en 90 segundos, creando una puntilla dorada crujiente en los bordes y manteniendo las yemas líquidas.",
                    "4. Sazón y Montaje al Momento: Espolvorear sal de mar mineral de Colima directamente sobre cada yema brillante y retirar con espátula plana a platos precalentados para servir de inmediato a 65°C."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Disolución coloidal a 60°C; enfriamiento a 45°C antes de 33Plus; gelificación a 4°C.",
                    "flavor_and_aromatics": "Infusión de zacate limón y menta que otorga notas cítricas y refrescantes que realzan la pulpa de pitaya.",
                    "textural_architecture": "Gel coloidal transparente y firme con suspensión uniforme de pulpa.",
                    "critical_control_points": "Infundir zacate limón 5 min a 90°C; atemperar a 45°C antes de añadir 33Plus; refrigerar 3 horas."
                },
                "steps": [
                    "1. Infusión Cítrica Herbal: Preparar la infusión de zacate limón y menta fresca a 90°C; colar y dejar reposar.",
                    "2. Hidratación de Grenetina: Hidratar la grenetina en agua purificada fría durante 8 minutos.",
                    "3. Integración Nootrópica: Disolver la grenetina en la infusión a 60°C, enfriar a 45°C e incorporar la Fórmula 33Plus® y los cubos de pitaya macerada.",
                    "4. Cuajado y Servicio: Distribuir en recipientes individuales y refrigerar a 4°C por 3 horas hasta cuajar con consistencia firme."
                ]
            }
        },
        "comida": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (6°C a 10°C). El anetol del bulbo de hinojo es volátil y se preserva en frío.",
                    "flavor_and_aromatics": "Notas anisadas y dulces del hinojo contrastadas con el picor pimienta de la arúgula y la vinagreta cítrica.",
                    "textural_architecture": "Láminas translúcidas de hinojo crujiente con hojas de arúgula frescas y ligeras.",
                    "critical_control_points": "Cortar hinojo en mandolina a 1 mm; sumergir 3 min en agua con hielo para rizar; centrifugar y aderezar al pase."
                },
                "steps": [
                    "1. Laminado Translúcido de Hinojo: Cortar el bulbo de hinojo en láminas casi transparentes de 1 mm con mandolina; sumergir 3 minutos en agua helada para tensar la fibra y secar minuciosamente.",
                    "2. Emulsión Cítrica: Batir el jugo de limón con la sal de mar mineral y el aceite de oliva extra virgen en un cuenco pequeño.",
                    "3. Mezcla y Pase: Combinar el hinojo rizado con las hojas de arúgula en un tazón hondo; bañar con la vinagreta envolviendo con suavidad y servir al instante en platos fríos."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Cocción unilateral con piel crujiente (skin crisp) a 170°C. La piel de huachinango contiene colágeno que se vuelve crujiente al presionarse contra la sartén caliente; la carne se cocina por calor ascendente protegiendo la humedad de la carne blanca hasta 55°C internos.",
                    "flavor_and_aromatics": "Pescado noble marino con piel caramelizada y tostada, bañado en emulsión tibia de mantequilla de ajo confitado y gotas de limón.",
                    "textural_architecture": "Piel ultra-crocante como barquillo; carne blanca blanda y translúcida que se separa en pétalos tiernos.",
                    "critical_control_points": "Piel completamente seca raspada con cuchillo; cortes superficiales en la piel para que no se curve; presionar con espátula los primeros 60 segundos; terminar con mantequilla espumosa fuera del fuego."
                },
                "steps": [
                    "1. Preparación y Secado de la Piel: Raspar la piel de los filetes de huachinango con el lomo del cuchillo para retirar exceso de humedad; realizar 3 incisiones diagonales superficiales en la piel y secar rigurosamente con papel absorbente.",
                    "2. Sellado Unilateral a la Plancha: Calentar una sartén de acero o plancha a 170°C con un hilo de aceite VEVO. Colocar los filetes con la piel hacia abajo y presionar firmemente con espátula plana durante 60 segundos para evitar que se curve. Cocinar sin mover durante 4 minutos hasta que la piel esté dorada y crujiente y los bordes de la carne comiencen a blanquear.",
                    "3. Volteo Efímero y Reposo: Voltear los filetes por solo 30 segundos para sellar la cara superior sin secar el núcleo; retirar inmediatamente a plato tibio.",
                    "4. Emulsión de Mantequilla de Ajo y Limón: En la misma sartén fuera del fuego, fundir la mantequilla con el ajo picado muy fino y el jugo de limón, emulsionando con espátula. Salsear la base del plato y colocar el filete encima con la piel crujiente expuesta."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Salteo a 150°C en Ghee durante 3 min. Evita deshidratación y preserva color clorofílico vibrante.",
                    "flavor_and_aromatics": "Dulzura vegetal con notas tostadas de almendra y aroma mantequilloso del Ghee.",
                    "textural_architecture": "Ejotes tiernos al dente con almendras crujientes.",
                    "critical_control_points": "Despuntar y secar ejotes; saltear en Ghee bien caliente; almendras al final."
                },
                "steps": [
                    "1. Acondicionamiento: Despuntar los ejotes verdes tiernos y secar perfectamente.",
                    "2. Salteo en Ghee: Calentar el Ghee en sartén amplia a fuego medio-alto (150°C); añadir los ejotes y saltear durante 3 minutos con la sal mineral de Colima.",
                    "3. Integración de Almendras: Incorporar las almendras fileteadas tostadas en el último minuto de sartén. Servir como guarnición caliente."
                ]
            }
        },
        "cena": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (8°C a 12°C). Cero calor. Preserva lípidos monoinsaturados intactos.",
                    "flavor_and_aromatics": "Riqueza mantecosa vegetal del aguacate Hass contrastada con el frutado picante del aceite VEVO y sal de Colima.",
                    "textural_architecture": "Cremoso sedoso con fractura de cristales salinos.",
                    "critical_control_points": "Cortar en abanico justo al pase; no refrigerar en exceso para no opacar el brillo graso."
                },
                "steps": [
                    "1. Deshuesado y Pelado: Cortar el aguacate por la mitad, retirar el hueso y pelar la cáscara con cuchara para no marcar la pulpa.",
                    "2. Despliegue en Abanico: Realizar incisiones finas longitudinales y abrir en abanico sobre platos fríos.",
                    "3. Sazón: Rociar con el aceite de oliva extra virgen y coronar con granos de sal mineral de Colima."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Sellado en sartén a 160°C para caramelizar sombreros de Portobello; gratinado a 190°C durante 6 min. La mezcla de queso crema y nuez pecana confita las espinacas dentro de la cavidad cóncava sin deshidratar el hongo.",
                    "flavor_and_aromatics": "Intenso perfil umami terroso del hongo asado combinado con la suavidad del queso crema, el crocante de la nuez pecana y la salinidad del Parmesano fundido.",
                    "textural_architecture": "Sombrero carnoso y suculento como carne vegetal, coronado con relleno cremoso y costra de Parmesano dorada.",
                    "critical_control_points": "Limpiar sombreros con paño húmedo sin mojar en agua; saltear espinacas previamente para evaporar agua; hornear a 190°C hasta gratinar."
                },
                "steps": [
                    "1. Limpieza y Sellado de Sombreros: Limpiar los sombreros de Portobello con paño húmedo y retirar los tallos; marcar en sartén con aceite VEVO caliente a 160°C durante 2 minutos por lado hasta tiernizar ligeramente.",
                    "2. Elaboración del Relleno: Saltear las espinacas picadas 90 segundos hasta colapsar; escurrir el líquido y mezclar en un bol con el queso crema artesanal, las nueces pecana troceadas y sal mineral.",
                    "3. Relleno y Coronación de Parmesano: Colocar los sombreros con la cavidad hacia arriba en una bandeja para horno; rellenar generosamente con la mezcla cremosa y espolvorear con el queso Parmesano Reggiano rallado.",
                    "4. Gratinado y Servicio: Hornear a 190°C durante 6 a 8 minutos hasta que el queso esté gratinado y burbujeante y el hongo perfectamente cocido. Servir caliente."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Infusión de toronjil a 85°C; descenso térmico a 55°C para protección de 34Plus.",
                    "flavor_and_aromatics": "Aroma cítrico sedante que induce relajación previa al descanso.",
                    "textural_architecture": "Tisana limpia y reconfortante.",
                    "critical_control_points": "Infundir tapado 5 min; colar; añadir 34Plus a 55°C."
                },
                "steps": [
                    "1. Infusión Caliente: Calentar el agua a 85°C; infusionar el toronjil fresco en tetera tapada durante 5 minutos.",
                    "2. Control de Temperatura: Filtrar la infusión y esperar a que descienda a 55°C.",
                    "3. Adición de Fórmula y Servicio: Disolver los 30 g de Fórmula 34Plus® en el líquido tibio con suavidad. Servir en tazas cerámicas."
                ]
            }
        }
    },
    "Viernes": {
        "desayuno": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (4°C a 10°C). Sin calor. Preserva la integridad celular y vitamina C de las fresas.",
                    "flavor_and_aromatics": "Frescura dulce y acidez brillante balanceada con los lípidos amargos nobles de la nuez de Castilla y chía.",
                    "textural_architecture": "Fruta jugosa tierna con mordida quebradiza de nuez de Castilla.",
                    "critical_control_points": "Lavar con pedúnculo; retirar hojas y cortar en mitades; secar sobre paño."
                },
                "steps": [
                    "1. Acondicionamiento de Fresas: Lavar las fresas, retirar el pedúnculo y cortar en mitades simétricas; secar suavemente sobre papel absorbente.",
                    "2. Troceado de Nueces: Trocear las nueces de Castilla en cuartos irregulares con las manos.",
                    "3. Ensamble al Pase: Disponer las fresas en cuencos fríos, añadir las nueces de Castilla y espolvorear las semillas de chía en la superficie."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Cocción japonesa multicapa a 120°C. Cada capa fina de huevo batido cuaja en 30 segundos sin dorar; al enrollar sucesivamente sobre sí misma, crea un cilindro compacto con centro húmedo donde los bastones de queso Panela se funden suavemente por calor residual.",
                    "flavor_and_aromatics": "Dulzura natural del huevo fresco enriquecida por la mantequilla artesanal y la frescura láctea del queso Panela.",
                    "textural_architecture": "Rollo de capas sedosas y esponjosas que ceden con suavidad, albergando el corazón tierno de queso Panela.",
                    "critical_control_points": "Sartén rectangular o redonda a fuego bajo (120°C); engrasar con mantequilla entre capa y capa; verter el huevo en 3 tandas delgadas; enrollar con espátula antes de que la superficie seque por completo."
                },
                "steps": [
                    "1. Batido y Colado de Masa de Huevo: Cascar los 18 huevos en un bol; sazonar con la sal de mar mineral y batir con palillos o tenedor en vaivén suave para romper yemas y claras sin incorporar aire; colar por malla fina para retirar grumos.",
                    "2. Primera Capa y Colocación de Queso: Calentar una sartén a fuego bajo (120°C) untada con mantequilla; verter un tercio de la mezcla de huevo formando una película delgada. Al cuajar el fondo (superficie aún húmeda), colocar los bastones de queso Panela en el extremo y enrollar la tortilla sobre el queso con ayuda de espátula.",
                    "3. Adición de Capas Sucesivas: Empujar el rollo al fondo de la sartén, engrasar la superficie libre con mantequilla y verter otro tercio de huevo, levantando ligeramente el rollo previo para que el huevo crudo penetre por debajo. Cuando comience a cuajar, volver a enrollar envolviendo la nueva capa.",
                    "4. Sellado Final y Reposo: Repetir con el último tercio de huevo para completar el rollo grueso. Retirar a esterilla o tabla de madera; reposar 2 minutos para que el calor residual funda el queso interior antes de cortar en rodajas gruesas de 3 cm. Servir caliente."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Disolución coloidal a 60°C; atemperado a 45°C antes de 33Plus; reticulación en frío a 4°C.",
                    "flavor_and_aromatics": "Fondo botánico de frutos rojos y jamaica con fresas frescas maceradas.",
                    "textural_architecture": "Gel firme y cristalino.",
                    "critical_control_points": "Hidratar grenetina 8 min; fundir a 60°C; enfriar a 45°C antes de 33Plus; reposo de 3 horas a 4°C."
                },
                "steps": [
                    "1. Infusión de Frutos Rojos: Elaborar infusión de frutos rojos y flores de jamaica suave a 85°C; colar y atemperar; macerar las fresas frescas.",
                    "2. Hidratación de Grenetina: Hidratar la grenetina en agua fría 8 minutos.",
                    "3. Fusión e Incorporación: Calentar la infusión a 60°C, fundir la grenetina y bajar a 45°C. Integrar la Fórmula 33Plus® y las fresas maceradas.",
                    "4. Gelificación: Verter en copas y refrigerar a 4°C durante 3 horas. Servir fría."
                ]
            }
        },
        "comida": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Salteo de champiñones a 140°C para evaporar agua y concentrar ácido glutámico natural (umami); activación de cúrcuma en mantequilla; triturado térmico.",
                    "flavor_and_aromatics": "Notas terrosas intensas de hongo Portobello con el brillo cálido de la cúrcuma y la sapidez salina del Parmesano Reggiano.",
                    "textural_architecture": "Crema untuosa densa con brillo dorado y textura sedosa.",
                    "critical_control_points": "Dorar champiñones sin quemar mantequilla; procesar en caliente con caldo casero; integrar Parmesano al final fuera del fuego."
                },
                "steps": [
                    "1. Salteo y Caramelizado de Hongos: Cortar los Portobellos en dados; en cazuela honda, fundir la mantequilla a fuego medio (140°C) y saltear los hongos con la cúrcuma durante 5 minutos hasta que doren y suelten aroma cálido.",
                    "2. Cocción en Caldo: Añadir el caldo casero caliente y la sal mineral; cocer tapado a fuego suave durante 8 minutos.",
                    "3. Emulsión Térmica: Licuar a velocidad máxima hasta lograr una crema tersa sin grumos; regresar a la cazuela tibia e incorporar el queso Parmesano Reggiano rallado batiendo con varilla hasta que funda por completo.",
                    "4. Servicio Caliente: Servir en platos hondos precalentados a 70°C."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Sellado flash de costra a 190°C (30 a 45 segundos por cara). La mioglobina del atún fresco calidad sashimi se desnaturaliza por encima de 45°C perdiendo sujugosidad; el interior debe permanecer estrictamente crudo/rojo (tataki) a 25°C–30°C mientras la costra de sésamo se tuesta intensamente.",
                    "flavor_and_aromatics": "Pescado azul marino untuoso contrastado con el aceite de sésamo tostado de las semillas y la acidez viva del limón fresco.",
                    "textural_architecture": "Costra crujiente crocante de ajonjolí tostado en el exterior; núcleo de atún sedoso, fresco y elástico que se funde en boca.",
                    "critical_control_points": "Atún a 4°C; secar perfectamente; rebozar con sésamo presionando para que se adhiera; sartén humeante a fuego vivo con aceite VEVO; retirar inmediatamente para cortar inercia térmica."
                },
                "steps": [
                    "1. Acondicionamiento y Encostrado: Retirar los medallones de atún del frío (4°C); secar con papel absorbente y sazonar con sal mineral de Colima. Extender las semillas de sésamo en una bandeja plana y presionar las caras de los medallones para fijar una costra compacta.",
                    "2. Sellado Flash a Alta Temperatura: Calentar una sartén pesada a fuego vivo (190°C) con el aceite de oliva extra virgen. Colocar los medallones y sellar durante exactamente 40 segundos por lado hasta tostar las semillas sin calentar el centro.",
                    "3. Reposo y Enfriamiento de Inercia: Retirar de inmediato a una tabla fría; dejar reposar 2 minutos para que los jugos se asienten.",
                    "4. Trinche y Aliño Cítrico: Cortar los medallones en filetes transversales de 1 cm con cuchillo afilado de un solo trazo, revelando el centro rojo brillante. Rociar con unas gotas de limón natural fresco al emplatar y servir al momento."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Asado en sartén a 160°C por 8 min con VEVO. El calor seco ablanda la celulosa del espárrago manteniendo la clorofila intacta.",
                    "flavor_and_aromatics": "Sabor vegetal puro y ligeramente tostado, elevado por el ácido cítrico del limón al salir del calor.",
                    "textural_architecture": "Tallo crocante con textura tierna y jugosa al morder.",
                    "critical_control_points": "Despuntar tallos; sartén amplia sin amontonar; bañar con limón y sal de Colima al pase."
                },
                "steps": [
                    "1. Limpieza y Despunte: Lavar los espárragos y retirar las bases leñosas; secar con paño.",
                    "2. Asado en Sartén: Calentar el aceite de oliva en sartén amplia a fuego medio-alto (160°C); disponer los espárragos en paralelo y saltear durante 7 a 8 minutos volteándolos ocasionalmente hasta que doren ligeramente.",
                    "3. Sazón Cítrica: Espolvorear con sal de mar mineral, retirar del calor y rociar con el jugo de limón fresco antes de servir."
                ]
            }
        },
        "cena": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cero calor. Choque en hielo para turgencia celular.",
                    "flavor_and_aromatics": "Frescura astringente marina del apio y calabacita con limón.",
                    "textural_architecture": "Crujiente acuoso sonoro.",
                    "critical_control_points": "Cortar bastones simétricos; 5 min en hielo; secar antes de limón."
                },
                "steps": [
                    "1. Bastones: Cortar calabacitas y apio en bastones de 8 cm por 1 cm.",
                    "2. Choque Osmótico: Reposar 5 minutos en agua purificada con hielo.",
                    "3. Montaje: Secar, colocar en vasos individuales y bañar con limón recién exprimido y sal mineral de Colima."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío rigurosa para pescado blanco crudo (2°C a 4°C). El ácido cítrico desnaturaliza químicamente la superficie del robalo si se deja reposar; el aderezo se emulsiona y se incorpora justo al momento de emplatar para conservar la textura cruda y cristalina del robalo.",
                    "flavor_and_aromatics": "Pescado blanco salvaje noble con perfume fresco de cilantro, acidez limpia del limón y untuosidad mantecosa del aguacate Hass en brunoise.",
                    "textural_architecture": "Cubos firmes de robalo con resistencia fresca en boca, intercalados con dados aterciopelados de aguacate.",
                    "critical_control_points": "Robalo a 2°C; cortar en cubos de 5 mm con cuchillo fileteador sin desgarrar carne; mezclar en bol frío sobre cama de hielo; servir inmediatamente."
                },
                "steps": [
                    "1. Corte Brunoise de Precisión: Retirar el filete de robalo del frío (2°C); cortar con cuchillo muy afilado en cubos pequeños homogéneos de 5 mm sin aplastar la carne.",
                    "2. Acondicionamiento de Aguacate y Cilantro: Cortar el aguacate Hass en dados de la misma dimensión (5 mm); picar finamente las hojas de cilantro fresco.",
                    "3. Emulsión Fría al Instante: En un tazón de cristal frío, mezclar el aceite de oliva extra virgen con el jugo de limón fresco y la sal de mar mineral batiendo con tenedor.",
                    "4. Integración y Moldeado en Timbal: Añadir los cubos de robalo, el aguacate y el cilantro al tazón; integrar delicadamente con espátula durante 20 segundos. Emplatar en timbal o aro sobre platos enfriados y servir de inmediato a 4°C."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Infusión de hinojo a 90°C para extraer anetol; atemperado a 55°C antes de 34Plus.",
                    "flavor_and_aromatics": "Aroma anisado suave digestivo que desinflama y calma el tracto gastrointestinal.",
                    "textural_architecture": "Infusión translúcida y tibia.",
                    "critical_control_points": "Infundir 5 min tapado; colar semillas; disolver 34Plus a 55°C."
                },
                "steps": [
                    "1. Infusión Anisada: Infundir las semillas y hojas de hinojo en agua a 90°C durante 5 minutos en tetera con émbolo tapada.",
                    "2. Filtrado y Control Térmico: Decantar la infusión y esperar a que la temperatura baje a 55°C.",
                    "3. Adición de 34Plus: Incorporar los 30 g de Fórmula 34Plus® removiendo hasta su disolución completa. Servir en tazas cerámicas."
                ]
            }
        }
    },
    "Sábado": {
        "desayuno": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (4°C a 10°C). Preserva antocianinas y polifenoles de las zarzamoras.",
                    "flavor_and_aromatics": "Acidez frutal profunda de la zarzamora con las notas tostadas de la almendra fileteada y chía.",
                    "textural_architecture": "Drupeolos jugosos con fractura seca crujiente de almendra.",
                    "critical_control_points": "Seleccionar zarzamoras firmes; secar por gravedad; chía al pase."
                },
                "steps": [
                    "1. Acondicionamiento Frío: Seleccionar las zarzamoras manteniendo la cadena de frío a 4°C; secar con cuidado sobre papel absorbente.",
                    "2. Tostado Aromático: Tostar las almendras fileteadas en seco a 130°C hasta que desprendan aroma a fruto seco.",
                    "3. Montaje: Colocar las zarzamoras en cuencos fríos, añadir las almendras fileteadas y finalizar con semillas de chía en la superficie."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Horneado en cazuela de hierro a 180°C. La espinaca salteada previamente en mantequilla actúa como lecho aislante térmico húmedo; al verter los huevos sobre nidos de espinaca y hornear tapado 6 min y destapado 3 min, las claras coagulan a 65°C mientras las yemas permanecen líquidas y untuosas a 62°C, con el queso de cabra gratinado en superficie por radiación superior.",
                    "flavor_and_aromatics": "Fondo vegetal terroso de espinacas en mantequilla con el toque mineral salino y la acidez cremosa del queso de cabra artesanal gratinado.",
                    "textural_architecture": "Lecho sedoso de espinacas tiernas, clara cuajada firme pero suave, yema fluida caliente y toques fundidos de queso de cabra.",
                    "critical_control_points": "Saltear espinacas antes para evaporar agua y que no agüen la cazuela; precalentar la cazuela a 180°C; abrir nidos para las yemas; retirar cuando la clara esté blanca pero la yema tiemble al mover la cazuela."
                },
                "steps": [
                    "1. Salteo y Deshidratación de Espinacas: En sartén amplia, fundir la mitad de la mantequilla a fuego medio; saltear las espinacas limpias durante 2 minutos hasta marchitar; retirar del fuego y escurrir el exceso de líquido en un colador.",
                    "2. Acondicionamiento de la Cazuela de Hierro: Enmantequillar una cazuela de hierro fundido amplia con el resto de la mantequilla; distribuir las espinacas salteadas cubriendo el fondo y formar 6 huecos o nidos con el dorso de una cuchara.",
                    "3. Disposición de Huevos y Queso: Cascar un huevo en cada nido de espinaca, sazonar con la sal de mar mineral y desmoronar el queso de cabra suave artesanal en los espacios entre los huevos.",
                    "4. Horneado de Precisión: Introducir la cazuela al horno precalentado a 180°C durante 7 a 9 minutos hasta que las claras estén completamente cuajadas y blancas pero las yemas se conserven líquidas y brillantes. Retirar con guantes térmicos y servir al centro de la mesa a 65°C."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Disolución a 60°C; adición de 33Plus a 45°C; gelificación a 4°C.",
                    "flavor_and_aromatics": "Infusión de frutos negros y menta con zarzamoras frescas enteras.",
                    "textural_architecture": "Gel firme y transparente con fractura limpia.",
                    "critical_control_points": "Hidratar grenetina 8 min; disolver a 60°C; atemperar a 45°C antes de 33Plus; refrigerar 3 horas."
                },
                "steps": [
                    "1. Infusión Base: Infundir frutos negros y hojas de menta en agua caliente a 85°C; colar y dejar atemperar.",
                    "2. Hidratación de Colágeno: Hidratar la grenetina en agua fría 8 minutos.",
                    "3. Integración de Activos: Calentar la infusión a 60°C, disolver la grenetina y dejar enfriar a 45°C. Añadir la Fórmula 33Plus® y las zarzamoras maceradas.",
                    "4. Gelificación Fría: Servir en moldes y refrigerar a 4°C por 3 horas hasta cuajar. Servir fría."
                ]
            }
        },
        "comida": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Rostizado previo de ajo a 170°C para eliminar alicina amarga y caramelizar; cocción rápida de espinacas a 85°C para conservar clorofila brillante sin oscurecer.",
                    "flavor_and_aromatics": "Notas vegetales profundas enriquecidas con la dulzura del ajo rostizado y el umami salino del Parmesano Reggiano.",
                    "textural_architecture": "Velouté verde esmeralda denso y satinado.",
                    "critical_control_points": "Rostizar ajo envuelto en papel aluminio; cocer espinacas en caldo solo 3 min; licuar de inmediato a alta velocidad."
                },
                "steps": [
                    "1. Rostizado de Ajo Confitado: Hornear los dientes de ajo en papillote con unas gotas de mantequilla a 170°C por 15 minutos hasta consistencia de pasta dulce.",
                    "2. Cocción Corta de Espinacas en Caldo: Calentar el caldo claro casero a 85°C con la mantequilla; añadir las espinacas frescas y la pasta de ajo rostizado, cocinando durante solo 3 minutos para mantener el verde esmeralda.",
                    "3. Triturado y Emulsión: Licuar inmediatamente a alta velocidad con la sal de mar mineral y el queso Parmesano Reggiano rallado hasta obtener una crema satinada y untuosa.",
                    "4. Servicio Caliente: Servir en tazones tibios a 70°C."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Sellado en sartén a 160°C en mantequilla con romero y horneado a 165°C hasta 74°C internos. La mantequilla perfumada con romero baña la carne constantemente creando una película protectora que retiene los jugos mioglobínicos.",
                    "flavor_and_aromatics": "Fondo limpio de ave con aroma balsámico y amaderado del romero fresco frito en mantequilla de pastoreo.",
                    "textural_architecture": "Exterior dorado y fragante con fibras de pavo sumamente jugosas y tiernas al corte transversal.",
                    "critical_control_points": "Atemperar pavo 15 min; secar bien; sellar 3 min por cara bañando con mantequilla y romero; hornear a 165°C; reposar 5 min antes de cortar."
                },
                "steps": [
                    "1. Atemperado y Secado de Pechuga: Retirar la pechuga de pavo del frío 15 minutos antes; secar con papel absorbente y sazonar con la sal de mar mineral.",
                    "2. Sellado Aromático en Mantequilla y Romero: Calentar la mantequilla y el aceite VEVO en sartén apta para horno a 160°C; incorporar las hojas de romero fresco y sellar la pechuga de pavo durante 3 minutos por lado, bañándola con la mantequilla espumosa con una cuchara.",
                    "3. Horneado Convectivo: Pasar la sartén al horno a 165°C durante 12 a 14 minutos hasta que la sonda interna marque 74°C en el centro de la pieza.",
                    "4. Reposo y Trinchado: Transferir a tabla de madera y dejar reposar 5 minutos tapada con papel aluminio para redistribuir jugos internos. Cortar en medallones de 1.5 cm contra la fibra y bañar con los jugos de romero de la sartén."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Salteo flash a 160°C en mantequilla durante 3 min. Evita que la calabacita suelte agua celular.",
                    "flavor_and_aromatics": "Frescura vegetal de la calabacita tierna bañada en mantequilla dorada y sal mineral.",
                    "textural_architecture": "Medias lunas tiernas con resistencia elástica al dente.",
                    "critical_control_points": "Cortar en medias lunas de 5 mm; sartén humeante; saltear rápido sin tapar."
                },
                "steps": [
                    "1. Corte: Lavar las calabacitas y cortar en medias lunas de 5 mm de grosor; secar con paño.",
                    "2. Salteo Vivo: Fundir la mantequilla en sartén a fuego medio-alto (160°C); añadir las calabacitas y saltear durante 3 minutos con movimientos ágiles.",
                    "3. Sazón al Salir: Espolvorear la sal de mar mineral en el último segundo y retirar del fuego para servir como guarnición caliente."
                ]
            }
        },
        "cena": {
            "starter": {
                "coct_reasoning": {
                    "thermodynamics": "Cadena de frío (6°C a 10°C). El vinagre de manzana sin filtrar reactiva enzimas gástricas.",
                    "flavor_and_aromatics": "Picor amargo de arúgula con suavidad de espinaca baby y acidez frutal de vinagre de manzana y VEVO.",
                    "textural_architecture": "Hojas verdes crujientes y frescas.",
                    "critical_control_points": "Lavar y centrifugar hojas; emulsionar vinagreta antes de verter; mezclar 60 seg antes de servir."
                },
                "steps": [
                    "1. Higienizado y Centrifugado: Lavar el mix de arúgula y espinacas en agua fría; centrifugar rigurosamente para eliminar humedad superficial.",
                    "2. Emulsión de Vinagre de Manzana: En un cuenco, batir el vinagre de manzana orgánico con el aceite de oliva extra virgen y la sal de Colima.",
                    "3. Aderezo Ligero: Rociar la vinagreta sobre las hojas en bol amplio, envolver con pinzas de madera y montar en platos fríos."
                ]
            },
            "main": {
                "coct_reasoning": {
                    "thermodynamics": "Ensamble frío/templado sin calor en la lechuga. Las hojas de lechuga orejona viva se mantienen sumergidas en hielo a 4°C para conservar máxima turgencia estructural (rigidez para actuar como taco sin quebrarse); el pollo deshebrado templado y el aguacate en láminas se montan en el momento del pase.",
                    "flavor_and_aromatics": "Fondo limpio de pollo jugoso aliñado con limón natural y aceite VEVO, abrazado por la frescura crujiente acuosa de la lechuga orejona y la manteca vegetal del aguacate.",
                    "textural_architecture": "Contraste tectónico: crocancia rígida y refrescante de la hoja de lechuga viva exterior con relleno tierno de pollo deshebrado y suavidad untuosa del aguacate.",
                    "critical_control_points": "Seleccionar 18 hojas grandes enteras de lechuga orejona; sumergir 5 min en baño de hielo y secar sobre paño; aliñar el pollo con limón, VEVO y sal antes de armar los wraps para no reblandecer la hoja."
                },
                "steps": [
                    "1. Choque Térmico de Hojas de Lechuga: Separar 18 hojas grandes y firmes de lechuga orejona; sumergir en un cuenco con agua purificada y hielo durante 5 minutos para hiperpolarizar la turgencia celular; escurrir y secar meticulosamente con paño limpio sin doblar la nervadura central.",
                    "2. Aliño y Sazón del Pollo: En un tazón, mezclar la pechuga de pollo deshebrada con el aceite de oliva extra virgen, el jugo de limón recién exprimido y la sal mineral de Colima, integrando con tenedor para humedecer uniformemente la fibra.",
                    "3. Corte de Aguacate en Láminas: Abrir los aguacates Hass maduros, retirar el hueso y cortar en láminas longitudinales finas.",
                    "4. Ensamblaje de Taco Wraps al Pase: Disponer 3 hojas de lechuga orejona por comensal en platos planos fríos; rellenar la nervadura central con la porción de pollo aliñado y coronar con las láminas de aguacate. Servir de inmediato como tacos vivos crujientes."
                ]
            },
            "side": {
                "coct_reasoning": {
                    "thermodynamics": "Infusión de toronjil a 85°C; descenso térmico a 55°C antes de incorporar 34Plus.",
                    "flavor_and_aromatics": "Aroma cítrico y herbal que prepara el sueño profundo reparador.",
                    "textural_architecture": "Infusión traslúcida reconfortante.",
                    "critical_control_points": "Tetera tapada; colar hojas; 34Plus a 55°C."
                },
                "steps": [
                    "1. Infusión: Infundir el toronjil fresco en agua caliente a 85°C durante 5 minutos en tetera con émbolo tapada.",
                    "2. Control Térmico: Decantar la tisana y dejar reposar hasta que la temperatura descienda a 55°C.",
                    "3. Adición de 34Plus: Incorporar los 30 g de Fórmula 34Plus® en lluvia fina mezclando con varilla. Servir en tazas cerámicas tibias."
                ]
            }
        }
    }
}

def apply_all_coct():
    master_path = r"C:\Users\andre\OneDrive\Escritorio\Archivos de prueba\nutriketo\semana_40_master.json"
    with open(master_path, "r", encoding="utf-8") as f:
        master = json.load(f)

    for day in master["days"]:
        dname = day["day"]
        if dname in COCT_WEEK_DATA:
            day_data = COCT_WEEK_DATA[dname]
            for meal in day["meals"]:
                mtype = meal["meal_type"].lower()
                if mtype in day_data:
                    mdata = day_data[mtype]
                    for course in ["starter", "main", "side"]:
                        if course in meal and course in mdata:
                            meal[course]["coct_reasoning"] = mdata[course]["coct_reasoning"]
                            meal[course]["steps"] = mdata[course]["steps"]

    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    print("semana_40_master.json updated successfully with full CoCT intelligence across all 7 days!")

if __name__ == "__main__":
    apply_all_coct()
