# -*- coding: utf-8 -*-
"""
Piloto CoCT: Lunes Semana 40
Aplica el contrato estricto de Arquitectura Cognitiva Dual:
1. Inyección de `coct_reasoning` estructurado en cada platillo.
2. Contrato JSON inmutable: `coct_reasoning {}` + `steps: string[]` dinámico.
3. Prosa libre de contabilidad: gramajes en la ficha, física y técnica pura en pasos.
4. Preservación absoluta de ingredientes, macros y BOM 3D (92 materias primas).
"""

import json
import os
import re

MASTER_JSON = r"C:\Users\andre\OneDrive\Escritorio\Archivos de prueba\nutriketo\semana_40_master.json"

LUNES_COCT_DATA = {
    "desayuno": {
        "starter": {
            "coct_reasoning": {
                "thermodynamics": "Cadena de frío vegetal estricta (4°C a 10°C). Sin intervención térmica para preservar la integridad celular de las antocianinas y polifenoles frutales.",
                "flavor_and_aromatics": "Acidez brillante y notas frutales rojas equilibradas por los lípidos dulces de la nuez pecana. La semilla de chía retiene humedad pasiva sin alterar el perfil.",
                "textural_architecture": "Trilogía de texturas: turgencia jugosa de la frambuesa, crocancia mantecosa de la nuez y micro-mordida seca de la chía.",
                "critical_control_points": "No lavar con presión mecánica para no romper drupeolos; secar por gravedad sobre papel absorbente (auxiliar neutro); añadir la chía inmediatamente antes del servicio."
            },
            "steps": [
                "1. Inspección y Acondicionamiento en Frío: Seleccionar las frambuesas manteniendo la cadena de frío (4°C a 8°C); disponer sobre papel absorbente para retirar cualquier vestigio de humedad superficial sin ejercer presión que comprometa las vesículas celulares.",
                "2. Tostado Ligero de Nuez y Texturizado: Trocear groseramente las nueces pecana con la mano o cuchillo en mitades irregulares para exponer sus aceites aromáticos sin generar polvillo amargo.",
                "3. Montaje y Emulsión de Texturas: Distribuir las frambuesas enteras en cuencos fríos; intercalar con las nueces troceadas y espolvorear las semillas de chía en lluvia superficial para conservar su crocancia activa antes de que el jugo frutal genere mucílago. Servir de inmediato."
            ]
        },
        "main": {
            "coct_reasoning": {
                "thermodynamics": "Curva de desnaturalización de ovoalbúmina (claras a 62°C–65°C; vitelina de yemas a 68°C–70°C). El estilo baveuse exige mantener el núcleo interior cremoso a 63°C–65°C mediante emulsión mecánica rápida y calor indirecto, evitando costra dorada o sobrecocción gomosa.",
                "flavor_and_aromatics": "Complejo lipídico de mantequilla avellanada sutil con sal mineral disuelta en crudo para abrir poros de proteína; aceites volátiles de finas hierbas (aliltiosulfinatos del cebollín y anetol del eneldo) activados por vapor interno.",
                "textural_architecture": "Corteza exterior sellada y elástica ultra-delgada, corazón untuoso y fluido con hebras de queso Gouda fundido por conducción residual.",
                "critical_control_points": "Sartén a fuego medio-bajo (125°C); batido sin incorporar burbujas de aire; incorporación de mantequilla fría cortada en cubitos para emulsionar la cuajada; enrollado francés al tercio de cocción."
            },
            "steps": [
                "1. Batido Homogéneo y Rompimiento Proteico: Cascar los huevos en un bol hondo; sazonar con la sal de mar mineral y batir con batidor de globo durante 40 segundos rompiendo los chalazas hasta lograr una emulsión uniforme y lisa, sin sobreincorporar burbujas de aire que resecan la cocción.",
                "2. Infusión Térmica de Hierbas y Precalentado: Calentar una sartén amplia de fondo grueso a fuego medio-bajo (125°C); fundir la mitad de la mantequilla hasta formar espuma ligera sin dorar. Incorporar la mitad de las finas hierbas para abrir sus aromas esenciales en el medio graso durante 15 segundos.",
                "3. Cocción Dinámica y Formación de Cuajada Baveuse: Verter la mezcla de huevos y agitar vigorosamente la sartén mientras se remueve el fondo con espátula de silicón en movimientos circulares rápidos. Al coagular el 70% de la masa en cuajada cremosa y húmeda, agregar los cubitos de mantequilla fría restante para cortar la inercia térmica y emulsionar el centro.",
                "4. Núcleo Fundente de Gouda y Enrollado Francés: Disponer el queso Gouda rallado en una línea transversal en el tercio superior; inclinar la sartén y enrollar la tortilla sobre sí misma envolviendo el queso. Pintar la superficie con el brillo residual de la espátula, coronar con las finas hierbas frescas restantes y servir de inmediato a 65°C con el interior cremoso."
            ]
        },
        "side": {
            "coct_reasoning": {
                "thermodynamics": "La grenetina requiere hidratación fría (bloom) y disolución térmica a 55°C–60°C. Los activos bioactivos de la Fórmula 33Plus son termosensibles y no deben exponerse a >65°C. Reticulación elástica en refrigeración a 4°C.",
                "flavor_and_aromatics": "Acidez fresca y notas silvestres de frambuesa macerada que balancean la textura coloidal con sutil toque herbal nootrópico.",
                "textural_architecture": "Gel coloidal transparente y firme con fractura suave en boca, albergando trozos de frambuesa en suspensión uniforme.",
                "critical_control_points": "Hidratar la grenetina en agua fría 8 min; fundir a 60°C; atemperar a 45°C antes de integrar la Fórmula 33Plus; reposo mínimo de 3 horas a 4°C."
            },
            "steps": [
                "1. Maceración y Extracción Fría: Disponer las frambuesas en un cuenco y prensar ligeramente con tenedor para liberar néctar y compuestos aromáticos sin triturar semillas, reservando en frío.",
                "2. Hidratación Bloom de Grenetina: Espolvorear la grenetina en forma de lluvia sobre 300 ml de agua purificada fría; dejar reposar 8 minutos hasta que los gránulos absorban la totalidad del líquido y formen una esponja compacta.",
                "3. Disolución Térmica e Integración Nootrópica: Calentar el resto del agua a 60°C; incorporar la grenetina hidratada removiendo suavemente hasta disolución cristalina completa. Dejar descender la temperatura a 45°C e incorporar la Fórmula Nootrópica 33Plus® y las frambuesas maceradas, homogeneizando sin generar espuma superficial.",
                "4. Dosificación y Gelificación Controlada: Verter la mezcla en moldes individuales o copas de vidrio; transferir a refrigeración constante a 4°C durante un mínimo de 3 horas hasta consolidar una estructura firme, tersa y de ruptura elástica. Servir fría."
            ]
        }
    },
    "comida": {
        "starter": {
            "coct_reasoning": {
                "thermodynamics": "Cadena de frío (6°C a 10°C). El ácido cítrico oxida la clorofila a feofitina (pardeamiento) si entra en contacto prolongado con las hojas; la vinagreta debe actuar como película protectora inmediata.",
                "flavor_and_aromatics": "Picor herbáceo y notas de nuez de la arúgula atenuadas por la suavidad mineral de la espinaca; la vinagreta de limón y aceite de oliva equilibra la astringencia y transporta la sal.",
                "textural_architecture": "Hojas túrgidas y crujientes con brillo lipídico sin saturación ni marchitamiento en el fondo del plato.",
                "critical_control_points": "Choque en agua helada para turgencia osmótica; centrifugado riguroso; emulsión enérgica previa del aliño; aderezo 60 segundos antes de servir."
            },
            "steps": [
                "1. Choque de Turgencia e Higienizado: Sumergir la arúgula y las espinacas baby en un cuenco con agua muy fría durante 3 minutos para reactivar la presión osmótica celular; centrifugar y secar sobre paño hasta que las hojas queden completamente desprovistas de humedad externa.",
                "2. Emulsión Mecánica de la Vinagreta: En un cuenco pequeño, disolver la sal de mar mineral en el jugo de limón recién exprimido; incorporar el aceite de oliva extra virgen en hilo continuo batiendo con tenedor o batidor pequeño hasta conformar una emulsión densa y opalescente.",
                "3. Aderezo Envolvente al Instante: Disponer las hojas mixtas en un bol amplio; verter la vinagreta recién emulsionada por las paredes del recipiente e integrar con pinzas en movimientos envolventes ligeros para lustrar cada hoja sin magullarla. Montar en platos fríos y servir inmediatamente."
            ]
        },
        "main": {
            "coct_reasoning": {
                "thermodynamics": "Carne de ave exige 74°C internos para inocuidad y coagulación de miosina sin expulsión hídrica excesiva. La curcumina y los terpenos del curry son liposolubles y requieren activación térmica suave en medio graso (80°C–100°C) sin quemar.",
                "flavor_and_aromatics": "Reacción de Maillard moderada en superficie de pollo; fondo especiado profundo con cúrcuma activada en mantequilla; emulsión láctea aterciopelada por caseína de crema y ácido glutámico (umami) del Parmesano Reggiano.",
                "textural_architecture": "Dados de pollo carnosos y jugosos cubiertos por una salsa untuosa con nappe perfecto, sin cortes de fase grasa.",
                "critical_control_points": "Secar el pollo antes de entrar al sartén; sellar en tandas a fuego medio-alto (150°C); bajar a fuego mínimo (80°C) antes de verter crema y queso para evitar disociación de emulsión."
            },
            "steps": [
                "1. Corte y Acondicionamiento Térmico del Ave: Porcionar la pechuga de pollo en dados regulares de 3 cm; secar minuciosamente sobre papel absorbente y sazonar con la sal de mar mineral, permitiendo un atemperado de 10 minutos a temperatura ambiente.",
                "2. Despertar Liposoluble de Especias: En una cazuela amplia o sautoir de fondo pesado, fundir la mantequilla a fuego bajo (100°C); incorporar la cúrcuma y el curry en polvo, sofriendo durante 45 segundos mientras se libera un aroma cálido y los pigmentos tiñen la grasa de un dorado intenso sin superar el punto de humo.",
                "3. Sellado de Proteína y Reacción de Maillard: Elevar el fuego a medio-alto (150°C) e introducir los cubos de pollo en una sola capa; sellar durante 3 a 4 minutos volteando cada cara para desarrollar un dorado ligero superficial que encapsule los jugos mioglobínicos internos.",
                "4. Reducción Untuosa y Emulsión de Parmesano: Reducir el fuego a mínimo (80°C a 85°C); verter la crema entera y remover el fondo desglasando los caramelizados adheridos. Tapar y dejar confitar a fuego suave durante 6 minutos hasta alcanzar 74°C en el corazón de la carne. Apagar el fuego, espolvorear el queso Parmesano Reggiano rallado e integrar con espátula hasta obtener una salsa satinada y homogénea. Servir caliente."
            ]
        },
        "side": {
            "coct_reasoning": {
                "thermodynamics": "La calabacita contiene >94% de agua celular libre. La cocción a baja temperatura o reposo prolongado con sal provoca exudación hídrica masiva (puré). Exige salteo rápido a alta temperatura (>160°C) por menos de 2.5 min para ablandar celulosa periférica manteniendo el núcleo elástico.",
                "flavor_and_aromatics": "Dulzura vegetal fresca acentuada por los compuestos fenólicos del aceite de oliva extra virgen; sazón mineral al final para no deshidratar la hortaliza.",
                "textural_architecture": "Hilos continuos elásticos tipo espagueti al dente con resistencia a la mordida y cero agua residual en el plato.",
                "critical_control_points": "Espiralizar justo antes de cocinar; secar humedad de corte con paño limpio; sartén humeante a fuego vivo; salado en el último segundo y retiro inmediato del fuego."
            },
            "steps": [
                "1. Espiralizado y Purga Superficial: Pasar las calabacitas limpias por espiralizador en cintas largas tipo espagueti; extender sobre un paño de cocina limpio durante 3 minutos presionando suavemente para retirar la humedad de corte.",
                "2. Salteo Flash de Alta Temperatura: Calentar una sartén amplia de hierro o acero a fuego vivo (160°C); añadir el aceite de oliva extra virgen e incorporar inmediatamente los zoodles, salteando con pinzas de cocina durante exactamente 2 minutos con movimientos continuos y aireados.",
                "3. Sazón Mineral al Cierre y Despacho: Espolvorear la sal de mar mineral en el último movimiento de sartén; retirar inmediatamente del fuego para cortar la conducción térmica residual y transferir a los platos de servicio como lecho vegetal crujiente para el pollo al curry."
            ]
        }
    },
    "cena": {
        "starter": {
            "coct_reasoning": {
                "thermodynamics": "Sin energía calórica. Choque térmico en frío (baño de hielo) para hiperpolarizar la presión osmótica de los vacuolos celulares de cucurbitáceas y apiáceas.",
                "flavor_and_aromatics": "Frescura acuosa, salina y astringente que limpia el paladar antes de los lípidos densos del salmón; el ácido cítrico estimula las papilas gustativas.",
                "textural_architecture": "Crujido limpio, tenaz y acústico.",
                "critical_control_points": "Retirar semillas acuosas del pepino; pelar hebras duras del apio; escurrir perfectamente del hielo antes de bañar con limón."
            },
            "steps": [
                "1. Corte de Precisión y Deshebrado: Pelar parcialmente el pepino dejando franjas verdes alternas, retirar el corazón de semillas y cortar en bastones de 8 cm por 1 cm; limpiar el apio retirando las hebras fibrosas exteriores y cortar a la misma dimensión geométrica.",
                "2. Choque Osmótico en Baño de Hielo: Sumergir los bastones en un cuenco con agua purificada y cubos de hielo durante 6 minutos para tensar las paredes celulares y potenciar el crujido crujiente; retirar y secar rigurosamente con paño limpio.",
                "3. Ensamblaje y Toque Cítrico Mineral: Disponer los bastones verticalmente en vasos cortos individuales; aderezar con unas gotas del jugo de limón recién exprimido y rematar con granos finos de sal de mar de Colima en el tope. Servir inmediatamente bien fríos."
            ]
        },
        "main": {
            "coct_reasoning": {
                "thermodynamics": "Grado sashimi riguroso: proteína mantenida entre 2°C y 4°C. Prohibido el calor. El ácido cítrico actúa como coagulante superficial por desnaturalización ácida si reposa, por lo que el aliño es de contacto efímero.",
                "flavor_and_aromatics": "Pescado azul graso con notas minerales yodadas suavizadas por la untuosidad vegetal del aguacate Hass; el aceite de ajonjolí prensado en frío añade profundidad tostada sin tapar la frescura del salmón.",
                "textural_architecture": "Láminas sedosas que se funden al calor bucal intercaladas con la cremosidad mantecosa del aguacate y el toque crujiente del sésamo.",
                "critical_control_points": "Cuchillo yanagiba o fileteador con filo de navaja; corte en un solo movimiento hacia el talón; platos de cerámica previamente enfriados; emulsión rociada justo al salir."
            },
            "steps": [
                "1. Fileteado de Precisión en Frío: Retirar el lomo de salmón del frío (2°C); con un cuchillo bien afilado, realizar cortes limpios al bies en ángulo de 45° con un solo trazo continuo, obteniendo láminas uniformes de 4 a 5 mm de grosor sin desgarrar la fibra muscular.",
                "2. Laminado de Aguacate: Abrir los aguacates Hass en su punto óptimo de madurez; cortar cada mitad en abanicos delgados de igual grosor que las láminas de salmón, reservando en frío protegidos de la oxidación.",
                "3. Emulsión Ligera de Sésamo y Cítrico: En un pequeño cuenco de cristal, mezclar el aceite de ajonjolí tostado prensado en frío con el jugo de limón y la sal mineral de Colima, emulsionando con un tenedor hasta integrar un aliño dorado brillante.",
                "4. Montaje y Servicio Inmediato: Disponer en platos fríos las láminas de salmón intercaladas armónicamente con los abanicos de aguacate; bañar con un hilo sutil de la emulsión cítrica de sésamo, coronar con las semillas de ajonjolí tostadas y servir de inmediato a temperatura de degustación fría."
            ]
        },
        "side": {
            "coct_reasoning": {
                "thermodynamics": "Extracción hidrosoluble de flavonoides y mentol a 85°C. La Fórmula 34Plus (péptidos, magnesio bisglicinato y cofactores) exige temperatura <60°C para no degradar su estructura molecular activa.",
                "flavor_and_aromatics": "Perfil aromático herbáceo, fresco y mentolado con notas balsámicas reconfortantes que redondean las notas minerales de la suplementación.",
                "textural_architecture": "Infusión traslúcida y limpia, cálida y de paso aterciopelado en garganta.",
                "critical_control_points": "Infundir tapado 5 minutos a 85°C; colar; enfriar a 55°C antes de verter 34Plus; disolución suave con cuchara de madera."
            },
            "steps": [
                "1. Infusión Termocontrolada de Hojas: Calentar el agua purificada a 85°C; colocar las hojas de menta limpia en una tetera con filtro o émbolo, verter el agua caliente, tapar de inmediato y dejar infusionar durante 5 minutos para extraer los aceites esenciales sin amargar los taninos de la hoja.",
                "2. Decantado y Descenso Térmico de Seguridad: Presionar el émbolo y colar la infusión; trasvasar a una jarra de servicio y monitorear la temperatura hasta que descienda a 55°C (por debajo del límite crítico de 60°C).",
                "3. Disolución Molecular de 34Plus y Servicio: Incorporar en lluvia fina los 30 g de Fórmula Biotecnológica Reparadora 34Plus®, mezclando con cuchara de madera o varilla con movimientos pausados hasta disolverla por completo en el líquido tibio. Servir en tazas de cerámica a 50°C como ritual previo al reposo nocturno."
            ]
        }
    }
}

def update_master():
    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        master = json.load(f)

    lunes_day = next(d for d in master["days"] if d["day"] == "Lunes")
    
    for meal in lunes_day["meals"]:
        mtype = meal["meal_type"].lower()
        if mtype in LUNES_COCT_DATA:
            mdata = LUNES_COCT_DATA[mtype]
            # Starter
            if "starter" in meal and "starter" in mdata:
                meal["starter"]["coct_reasoning"] = mdata["starter"]["coct_reasoning"]
                meal["starter"]["steps"] = mdata["starter"]["steps"]
            # Main
            if "main" in meal and "main" in mdata:
                meal["main"]["coct_reasoning"] = mdata["main"]["coct_reasoning"]
                meal["main"]["steps"] = mdata["main"]["steps"]
            # Side
            if "side" in meal and "side" in mdata:
                meal["side"]["coct_reasoning"] = mdata["side"]["coct_reasoning"]
                meal["side"]["steps"] = mdata["side"]["steps"]

    with open(MASTER_JSON, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    print("Master JSON updated successfully with CoCT Pilot for Lunes.")

if __name__ == "__main__":
    update_master()
