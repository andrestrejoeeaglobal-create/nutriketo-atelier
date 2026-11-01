
const fs = require('fs');

// We need DOM stubs or variables
let harvestList = ["Espinacas frescas", "Calabacitas verdes tiernas", "Brócoli fresco", "Espárragos verdes", "Nopales tiernos", "Ejotes frescos", "Cilantro fresco", "Arúgula fresca", "Coliflor fresca", "Limones agrios frescos de la granja", "Nuez pecana fresca de la granja"];

function stripAccents(str) {
  if (!str) return "";
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}
const INGREDIENT_CANONICAL_MAP_JS = {
  "aceite-oliva": ["aceite de oliva", "aceite de oliva extra virgen", "aceite vevo", "aceite de oliva extra virgen vevo", "aceite de oliva virgen extra"],
  "te-verde": ["té verde", "te verde", "té verde orgánico", "matcha"],
  "huevo-organico": ["huevo", "huevos", "huevos frescos", "huevos orgánicos", "huevos frescos orgánicos", "huevos frescos orgánicos de pastoreo", "huevos enteros"],
  "pechuga-pavo": ["pechuga de pavo", "pavo artesanal", "pechuga de pavo artesanal", "jamón de pavo", "tocino de pavo"],
  "pechuga-pollo": ["pechuga de pollo", "pollo fresco", "pechuga de pollo fresca", "muslos de pollo"],
  "sirloin-magro": ["carne molida de sirloin", "sirloin magro", "carne molida de sirloin magra"],
  "filete-res": ["filete de res", "filete de res magro", "ribeye", "sirloin", "medallones de mignon"],
  "huachinango-fresco": ["huachinango", "filete de huachinango", "filete de huachinango fresco", "filete de huachinango al horno"],
  "robalo-fresco": ["róbalo", "robalo", "filete de róbalo", "filete de robalo fresco", "filete de róbalo a la plancha"],
  "salmon-salvaje": ["salmón", "salmon", "salmón salvaje", "filete de salmón fresco", "filete de salmón salvaje", "filete de salmón fresco con piel"],
  "pescado-blanco": ["pescado blanco", "filete de pescado blanco", "filete de pescado blanco fresco"],
  "atun-fresco": ["atún", "atun", "filete de atún fresco"],
  "queso-parmesano": ["queso parmesano", "parmesano maduro", "queso parmesano maduro"],
  "queso-manchego": ["queso manchego", "manchego maduro", "queso manchego maduro"],
  "queso-gouda": ["queso gouda", "gouda maduro", "queso gouda maduro"],
  "queso-panela": ["queso panela", "panela fresco", "queso panela fresco"],
  "queso-cabra": ["queso de cabra", "cabra artesanal", "queso de cabra artesanal"],
  "queso-crema": ["queso crema", "queso crema artesanal"],
  "mantequilla-pastoreo": ["mantequilla", "mantequilla de vaca", "mantequilla de pastoreo", "mantequilla sin sal"],
  "jitomate-bola": ["jitomate", "jitomates", "jitomate bola", "jitomate bola jugoso", "jitomate saladet", "jitomate saladet fresco", "saladet"],
  "almendras-fileteadas": ["almendras fileteadas tostadas", "almendras fileteadas", "almendras tostadas", "almendras enteras", "almendra", "almendras"],
  "semillas-chia": ["semillas de chía orgánicas", "semillas de chia organicas", "semillas de chía", "semillas de chia", "chía", "chia"],
  "ajo-fresco": ["ajo fresco", "dientes de ajo fresco", "dientes de ajo", "ajo"],
  "limon-fresco": ["jugo de limón fresco recién exprimido", "jugo de limon fresco recien exprimido", "jugo de limón fresco", "limón fresco recién exprimido", "limones frescos", "limón", "limon"],
  "pimienta-negra": ["pimienta negra recién molida", "pimienta negra recien molida", "pimienta negra molida y sal marina", "pimienta negra molida", "pimienta negra"],
  "cebolla-blanca": ["cebolla blanca fresca", "cebolla blanca", "cebolla", "cebollas"],
  "romero-fresco": ["romero fresco", "romero"],
  "sal-mar": ["sal de mar", "sal de mar mineral", "sal mineral", "sal de colima", "sal de mar mineral de colima", "sal"],
  "chayotes-tiernos": ["chayotes tiernos", "chayote tierno", "chayotes tiernos pelados", "chayote", "chayotes", "chayotes tiernos pelados en laminas", "chayotes tiernos pelados en láminas"],
  "tomate-verde": ["tomate verde", "tomate verde fresco", "tomatillo", "tomates verdes"],
  "yoghurt-griego": ["yoghurt griego natural sin azúcar", "yoghurt griego", "yogurt griego", "yoghurt griego natural", "yogur griego"],
  "mayonesa": ["mayonesa", "mayonesa casera", "mayonesa keto"],
  "leche-coco": ["leche de coco", "leche de coco sin azúcar", "leche de coco sin azucar"],
  "sardinas": ["sardinas enlatadas", "sardinas", "sardina", "lata de sardinas", "latas de sardinas"],
  "papa": ["papa fresca", "papa", "papas", "papas frescas"],
  "lentejas": ["lentejas", "lenteja"],
  "garbanzo": ["garbanzo", "garbanzos"],
  "frijol": ["frijol", "frijoles"],
  "arroz": ["arroz tradicional", "arroz", "arroz blanco"],
  "multisinergix": ["multisinergix", "multi sinergix", "33plus", "33 plus", "fórmula 33plus", "elixir 33plus"],
  "aminosinergix": ["aminosinergix", "amino sinergix", "34plus", "34 plus", "fórmula 34plus", "tisana 34plus"],
  "33plus": ["33plus", "33 plus", "fórmula 33plus", "elixir 33plus", "multisinergix"],
  "34plus": ["34plus", "34 plus", "fórmula 34plus", "tisana 34plus", "aminosinergix"]
};
function normalizeToCanonicalSlug(rawName) {
  if (!rawName) return "";
  const clean = rawName.trim().toLowerCase();
  const cleanNoAcc = stripAccents(clean);

  for (const slug in INGREDIENT_CANONICAL_MAP_JS) {
    const aliases = INGREDIENT_CANONICAL_MAP_JS[slug];
    for (const alias of aliases) {
      const aliasClean = stripAccents(alias.trim().toLowerCase());
      if (aliasClean.includes(cleanNoAcc) || cleanNoAcc.includes(aliasClean)) {
        return slug;
      }
    }
  }

  const sanitized = cleanNoAcc.replace(/[^a-z0-9\\s-]/g, '').replace(/\\s+/g, '-').replace(/^-+|-+$/g, '');
  return sanitized || "insumo-general";
}


function getPieceGramWeight(itemName) {
  const n = (itemName || '').toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();
  if (/morron|pimiento/i.test(n)) return 160; // 1 pimiento morrón ~160 g
  if (/pechuga|pollo/i.test(n)) return 500; // 1 pechuga de pollo entera ~500 g
  if (/calabacita|calabaza/i.test(n)) return 180; // 1 calabacita tierna ~180 g
  if (/flor de calabaza/i.test(n)) return 180; // 1 manojo de flor de calabaza ~180 g
  if (/lechuga/i.test(n)) return 380; // 1 pieza de lechuga ~380 g
  if (/jitomate|tomate saladet/i.test(n)) return 120; // 1 jitomate ~120 g
  if (/tomate verde|tomatillo/i.test(n)) return 60; // 1 tomate verde ~60 g
  if (/cebolla/i.test(n)) return 160; // 1 cebolla ~160 g
  if (/aguacate/i.test(n)) return 180; // 1 aguacate Hass ~180 g
  if (/zanahoria/i.test(n)) return 120; // 1 zanahoria ~120 g
  if (/elote/i.test(n)) return 250; // 1 elote ~250 g
  if (/huevo/i.test(n)) return 55; // 1 huevo ~55 g
  if (/chayote/i.test(n)) return 200; // 1 chayote ~200 g
  if (/pepino/i.test(n)) return 200; // 1 pepino ~200 g
  if (/limon/i.test(n)) return 40; // 1 limón ~40 g
  if (/ajo/i.test(n)) return 50; // 1 cabeza de ajo ~50 g
  return 100;
}
function resolvePantryCommercialUnit(inputValue, unitType, multiplierOverride) {
      const num = parseFloat(inputValue) || 0;
      if (num <= 0) return { val: 0, type: 'mass', baseUnit: 'g' };

      if (typeof multiplierOverride === 'number' && multiplierOverride > 0) {
        return { val: num * multiplierOverride, type: 'mass', baseUnit: 'g' };
      }

      const u = (unitType || 'g').toLowerCase().trim();

      switch (u) {
        case 'bolsa_sal':
        case 'bolsa (1 kg)':
        case 'bolsa (1 kg / 1,000 g)':
        case 'bolsa_1000':
        case 'kg':
        case 'kilo':
        case 'kilos':
          return { val: num * 1000, type: 'mass', baseUnit: 'g' };
        case 'frasco_sal':
        case 'frasco_250':
        case 'bolsa_250':
        case 'domo_250':
        case 'paquete_250':
          return { val: num * 250, type: 'mass', baseUnit: 'g' };
        case 'frasco_100':
        case 'bolsa_100':
          return { val: num * 100, type: 'mass', baseUnit: 'g' };
        case 'frasco_50':
          return { val: num * 50, type: 'mass', baseUnit: 'g' };
        case 'bolsa_retazo':
        case 'bolsa_retazo_500':
        case 'paquete_500':
        case 'domo_500':
        case 'bolsa_500':
          return { val: num * 500, type: 'mass', baseUnit: 'g' };
        case 'paquete_3_2':
          return { val: num * 3200, type: 'mass', baseUnit: 'g' };
        case 'frasco_120':
          return { val: num * 120, type: 'mass', baseUnit: 'g' };
        case 'botellas de 1500 ml':
        case 'botellas (1500 ml)':
        case 'botella_1500':
          return { val: num * 1500, type: 'vol', baseUnit: 'ml' };
        case 'botellas de 355 ml':
        case 'botellas (355 ml)':
        case 'botella_355':
          return { val: num * 355, type: 'vol', baseUnit: 'ml' };
        case 'manojo':
          return { val: num, type: 'count', baseUnit: 'manojo' };
        case 'casillero':
          return { val: num * 30, type: 'count', baseUnit: 'piezas' };
        case 'docena':
          return { val: num * 12, type: 'count', baseUnit: 'piezas' };
        case 'malla_3':
        case 'malla (3 pzas)':
        case 'bolsa_3':
        case 'malla / bolsa (3 pzas)':
          return { val: num * 3, type: 'count', baseUnit: 'piezas' };
        case 'kg_aguacate':
          return { val: num * 5, type: 'count', baseUnit: 'piezas' };
        case 'botella_vevo':
        case 'botella_750':
          return { val: num * 750, type: 'vol', baseUnit: 'ml' };
        case 'botella_250':
          return { val: num * 250, type: 'vol', baseUnit: 'ml' };
        case 'frasco_500':
          return { val: num * 500, type: 'vol', baseUnit: 'ml' };
        case 'l':
        case 'lt':
        case 'litro':
        case 'litros':
          return { val: num * 1000, type: 'vol', baseUnit: 'ml' };
        case 'botellas_355':
        case 'botella_355':
        case 'botella (355 ml)':
        case 'botellas (355 ml)':
          return { val: num * 355, type: 'vol', baseUnit: 'ml' };
        case 'ml':
        case 'mililitro':
        case 'mililitros':
          return { val: num, type: 'vol', baseUnit: 'ml' };
        case 'g':
        case 'gramo':
        case 'gramos':
          return { val: num, type: 'mass', baseUnit: 'g' };
        case 'piezas':
        case 'pieza':
        case 'pza':
        case 'pzas':
        case 'pack':
        case 'packs':
        case 'paquete':
        case 'paquetes':
          return { val: num, type: 'count', baseUnit: 'piezas' };
        case 'latas':
        case 'lata':
          return { val: num, type: 'count', baseUnit: 'latas' };
        case 'bote_900':
          return { val: num * 900, type: 'mass', baseUnit: 'g' };
        case 'tetra_500':
          return { val: num * 500, type: 'vol', baseUnit: 'ml' };
        case 'bolsa_750':
          return { val: num * 750, type: 'mass', baseUnit: 'g' };
        default:
          return null;
      }
    }

    const CANONICAL_SECTION_ORDER = [
      "🍓 Frutas de Bajo Índice Glucémico",
      "🥑 Grasas, Aceites y Semillas",
      "🥩 Carnes, Pescados y Proteínas",
      "🌶️ Chiles, Condimentos e Infusiones",
      "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA",
      "🧀 Lácteos y Quesos (Sin Gluten — Keto)",
      "🥬 Verduras, Hortalizas y Frescos",
      "🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)"
    ];

    function getCategoryIndex(catName) {
      if (!catName) return 999;
      const name = catName.toLowerCase();
      if (name.includes('fruta')) return 0;
      if (name.includes('grasa') || name.includes('aceite')) return 1;
      if (name.includes('carne') || name.includes('pescado') || name.includes('proteína') || name.includes('proteina')) return 2;
      if (name.includes('chile') || name.includes('condimento') || name.includes('infusión') || name.includes('infusion')) return 3;
      if (name.includes('suplement') || name.includes('biotecnología') || name.includes('biotecnologia')) return 4;
      if (name.includes('lácteo') || name.includes('lacteo') || name.includes('queso')) return 5;
      if (name.includes('verdura') || name.includes('hortaliza') || name.includes('fresco')) return 6;
      if (name.includes('cuarentena') || name.includes('sugerido') || name.includes('prohibid') || name.includes('🛑')) return 7;
      return 8;
    }

    function getSmartItemCategory(itemName, explicitCategory) {
      if (explicitCategory && typeof explicitCategory === 'string' && explicitCategory.trim()) {
        const ec = explicitCategory.trim();
        if (ec.includes("Cuarentena") || ec.includes("🛑") || ec.includes("No Sugeridos") || ec.includes("prohibited")) return "🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)";
        if (ec.includes("Verduras") || ec.includes("Hortalizas") || ec.includes("Frescos")) return "🥬 Verduras, Hortalizas y Frescos";
        if (ec.includes("Carnes") || ec.includes("Pescados") || ec.includes("Proteínas")) return "🥩 Carnes, Pescados y Proteínas";
        if (ec.includes("Frutas")) return "🍓 Frutas de Bajo Índice Glucémico";
        if (ec.includes("Quesos") || (ec.includes("Lácteos") && !ec.includes("Grasas"))) return "🧀 Lácteos y Quesos (Sin Gluten — Keto)";
        if (ec.includes("Grasas") || ec.includes("Aceites") || ec.includes("Semillas")) return "🥑 Grasas, Aceites y Semillas";
        if (ec.includes("Suplementación") || ec.includes("Biotecnología") || ec.includes("Bases Hidrocoloides")) return "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA";
        if (ec.includes("Cítricos") || ec.includes("Ácidos")) return "🍋 Cítricos y Ácidos Naturales";
        if (ec.includes("Especias") || ec.includes("Hierbas") || ec.includes("Aromáticos") || ec.includes("Condimentos") || ec.includes("Infusiones")) return "🌶️ Chiles, Condimentos e Infusiones";
      }

      const name = (itemName || '').toLowerCase().trim();

      // 0.0 Inmunidad Taxonómica Estricta: Aceites vegetales, VEVO, ajonjolí, mantequilla y ghee son grasas puras (NUNCA lácteos ni quesos)
      if (/aceite|vevo|ajonjolí|ajonjoli|mantequilla|ghee/i.test(name)) {
        return '🥑 Grasas, Aceites y Semillas';
      }

      // 0.0 Prioridad Taxonómica Estricta: Leche de coco -> Grasas, Aceites y Semillas (NUNCA Cuarentena)
      if (/leche de coco/i.test(name)) {
        return '🥑 Grasas, Aceites y Semillas';
      }

      // 0.05 Prioridad Taxonómica Estricta: Hongos y Setas (NUNCA Grasas, NUNCA Carnes)
      if (/portobello|champiñon|champiñones|champinon|champinones|setas|hongos/i.test(name)) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      // 0.1 Prioridad Taxonómica Estricta: Cebollas (Verduras, Hortalizas y Frescos — NUNCA frutas)
      if (/cebolla|cebollas|cebollín|cebollin/i.test(name)) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      // 0.15 Prioridad Taxonómica Estricta: Grasas, Aceites y Semillas (Almendras, nueces, chía, etc. — NUNCA carnes aun si dicen fileteadas)
      if (/almendra|almendras|nuez|nueces|chía|chia|girasol|macadamia|macadamias|semilla|semillas|linaza|piñón|piñones|pepita|pepitas|ajonjolí|ajonjoli|aguacate|aceituna/i.test(name)) {
        return '🥑 Grasas, Aceites y Semillas';
      }

      // 0.2 Prioridad Taxonómica Estricta: Carnes / Proteínas (Arrachera, Sirloin, Pechuga, Pescado, Sardinas, etc.)
      if (/arrachera|corte|cortes|ribeye|sirloin|\bres\b|pollo|pollos|pechuga|pechugas|pavo|pavos|tocino|jamón|jamon|pescado|pescados|mojarra|tilapia|salmón|salmon|atún|atun|sardina|sardinas|huevo|huevos|clara|claras|lomo|lomos|medallón|medallon|medallones|huachinango|robalo|róbalo|filete|filetes|machaca|tuétano|tuetano|costilla/i.test(name)) {
        return '🥩 Carnes, Pescados y Proteínas';
      }

      // 0.3 Prioridad Taxonómica Estricta: Frutas de Bajo Índice Glucémico (Moras, Frambuesas, Arándanos, Granada, Pitaya, Zarzamora, Fresas)
      if (!name.includes('cebolla') && /mora|moras|frambuesa|frambuesas|fresa|fresas|arándano|arandano|arándanos|arandanos|granada|granadas|pitahaya|pitahayas|pitaya|pitayas|arilos|zarzamora|zarzamoras/i.test(name)) {
        return '🍓 Frutas de Bajo Índice Glucémico';
      }

      // 0.4 Prioridad Taxonómica Estricta: Insumos No Sugeridos / Cuarentena
      if ((explicitCategory && (explicitCategory.includes('cuarentena') || explicitCategory.includes('prohibited') || explicitCategory.includes('Cuarentena') || explicitCategory.includes('🛑'))) ||
          /durazno|duraznos|miel|harina de trigo|harina refinada|aceite vegetal mixto|azúcar|azucar|quinoa|cereza|cerezas|leche de vaca|higo|higos|papa|papas|lenteja|lentejas|garbanzo|garbanzos|frijol|frijoles|arroz/i.test(name)) {
        return '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)';
      }

      // 0.5 Prioridad Taxonómica Estricta: Hongos y Setas
      if (/portobello|champiñon|champiñones|champinon|champinones|setas|hongos/i.test(name)) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      // 0.6 Prioridad Taxonómica Estricta: Jitomate / Tomate
      if (/jitomate|tomate bola|\btomate\b/i.test(name) && !name.includes('tomillo')) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      // 1. Suplementación Celular — Biotecnología
      if (/33plus|34plus|sinergix|suplemento|suplementos|vitamina|vitaminas|colágeno|colageno|electrolitos|fórmula nootrópica|formula nootropica|fórmula reparadora|formula reparadora/i.test(name)) {
        return '💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA';
      }

      // 3. Grasas, Aceites y Semillas
      if (/aceite|mct|leche de coco|mantequilla|ghee|aguacate|aguacates|aceituna|aceitunas|nuez|nueces|almendra|almendras|chía|chia|girasol|macadamia|macadamias|semilla|semillas|linaza|piñón|piñones|pepita|pepitas|ajonjolí|ajonjoli|mayonesa/i.test(name)) {
        return '🥑 Grasas, Aceites y Semillas';
      }

      // 4. Lácteos y Quesos
      if (/queso|quesos|leche|crema|gouda|panela|parmesano|manchego|mascarpone|mozzarella|yoghurt|yogurt/i.test(name)) {
        return '🧀 Lácteos y Quesos (Sin Gluten — Keto)';
      }

      // 5. Cítricos y Ácidos Naturales
      if (/limón|limon|vinagre|balsámico|balsamico/i.test(name)) {
        return '🍋 Cítricos y Ácidos Naturales';
      }

      // 6. Chiles, Condimentos e Infusiones
      if (/\bsal\b|\bsal de\b|\bsal mineral\b|eneldo|romero|tomillo|comino|orégano|oregano|canela|menta|toronjil|manzanilla|jamaica|azahar|especias|condimento|condimentos|chile|chiles|jalapeño|jalapeno|pimienta|epazote|albahaca|mostaza|alcaparra|alcaparras|jengibre|agua|infusión|infusion|\bté\b|\bte\b|base líquida|base liquida|aderezo|bbq|café|cafe|cobertura de chocolate|salsa|tamari|soya|achiote/i.test(name)) {
        return '🌶️ Chiles, Condimentos e Infusiones';
      }

      // 7. Verduras, Hortalizas y Frescos
      if (/apio|arúgula|arugula|brócoli|brocoli|calabacita|calabacitas|chayote|chayotes|cilantro|coliflor|ejote|ejotes|espárrago|esparrago|esparragos|espárragos|espinaca|espinacas|flor de calabaza|hinojo|jitomate|jitomates|nopal|nopales|pepino|pepinos|pimiento|pimientos|tomate|zucchini|lechuga|col|cebolla|ajo|dientes de ajo|champiñones|champinon|champinones|portobello|setas/i.test(name)) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      return '🌶️ Chiles, Condimentos e Infusiones';
    }

    function loadAppState() {
      try {
        const storedVersion = localStorage.getItem('nutriketo_app_version');
        if (storedVersion !== CURRENT_APP_VERSION) {
          console.warn('Detectada versión anterior de localStorage. Migrando a V42 106 insumos canónicos...');
          const oldDataStr = localStorage.getItem('nutriketo_app_state_v40_2_ssot') || localStorage.getItem(LOCAL_STORAGE_KEY);
          let oldState = null;
          try { if (oldDataStr) oldState = JSON.parse(oldDataStr); } catch(e){}
          const legacyKeys = [
            'nutriketo_app_state_v40_2_ssot',
            'nutriketo_app_state_v38_canonical',
            'nutriketo_app_state_v34_granular',
            'nutriketo_app_state_v33',
            'nutriketo_app_state',
            'nutriketo_app_state_v36_6_ssot'
          ];
          for (const lKey of legacyKeys) {
            localStorage.removeItem(lKey);
          }
          localStorage.setItem('nutriketo_app_version', CURRENT_APP_VERSION);
          if (oldState) {
            if (oldState.activeWeek && datasets[oldState.activeWeek]) activeWeek = oldState.activeWeek;
            if (oldState.activeDiners) activeDiners = parseInt(oldState.activeDiners) || 6;
            if (Array.isArray(oldState.selectedHarvest)) selectedHarvest = oldState.selectedHarvest;
            if (Array.isArray(oldState.customFarmItems)) customFarmItems = oldState.customFarmItems;
            if (Array.isArray(oldState.deletedFarmItems)) deletedFarmItems = oldState.deletedFarmItems;
            if (oldState.mealDinersState) mealDinersState = oldState.mealDinersState;
            if (oldState.dispatchedMeals) dispatchedMeals = oldState.dispatchedMeals;
            if (Array.isArray(oldState.mealFeedbackLedger)) mealFeedbackLedger = oldState.mealFeedbackLedger;
          }
          saveAppState();
          return true;
        }

        let saved = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (!saved) {
          const legacyKeys = ['nutriketo_app_state_v34_granular', 'nutriketo_app_state_v33', 'nutriketo_app_state'];
          for (const lKey of legacyKeys) {
            const oldData = localStorage.getItem(lKey);
            if (oldData) {
              saved = oldData;
              localStorage.removeItem(lKey);
              break;
            }
          }
        }

        if (saved) {
          const state = JSON.parse(saved);
          if (state.activeWeek && datasets[state.activeWeek]) activeWeek = state.activeWeek;
          if (state.activeDiners) activeDiners = parseInt(state.activeDiners) || 6;

          if (Array.isArray(state.deletedFarmItems)) {
            deletedFarmItems = state.deletedFarmItems.filter(d => !areInsumosEquivalent(d, 'limon'));
          } else {
            deletedFarmItems = [];
          }

          if (Array.isArray(state.deletedPantryItems)) {
            deletedPantryItems = state.deletedPantryItems;
          } else {
            deletedPantryItems = [];
          }

          if (Array.isArray(state.customFarmItems)) {
            customFarmItems = state.customFarmItems.filter(f => {
              const fStr = typeof f === 'string' ? f : (f.item_name || f.name || '');
              return !/miel|durazno|higo/i.test(fStr);
            }).map(f => {
              const fStr = typeof f === 'string' ? f : (f.item_name || f.name || '');
              if (/nuex.*pecan|nuez.*pecan/i.test(fStr)) return "Nuez pecana fresca de la granja";
              return f;
            });
          }

          if (Array.isArray(state.selectedHarvest)) {
            selectedHarvest = state.selectedHarvest.filter(h => {
              const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
              return !/miel|durazno|higo/i.test(hStr);
            }).map(h => {
              const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
              if (/nuex.*pecan|nuez.*pecan/i.test(hStr)) return "Nuez pecana fresca de la granja";
              return h;
            });
            if (!selectedHarvest.some(h => areInsumosEquivalent(typeof h === 'string' ? h : (h.item_name || h.name || ''), 'limon'))) {
              selectedHarvest.push("Limones agrios frescos de la granja");
            }
            if (!selectedHarvest.some(h => areInsumosEquivalent(typeof h === 'string' ? h : (h.item_name || h.name || ''), 'nuez pecana')) && !deletedFarmItems.some(d => areInsumosEquivalent(d, 'nuez pecana'))) {
              selectedHarvest.push("Nuez pecana fresca de la granja");
            }
          } else {
            selectedHarvest = ["Espinacas frescas", "Calabacitas verdes tiernas", "Brócoli fresco", "Espárragos verdes", "Nopales tiernos", "Ejotes frescos", "Cilantro fresco", "Arúgula fresca", "Coliflor fresca", "Limones agrios frescos de la granja", "Nuez pecana fresca de la granja"];
          }

          if (state.pantryStock && typeof state.pantryStock === 'object') {
            pantryStock = {};
            Object.keys(state.pantryStock).forEach(itemName => {
              if (/miel|durazno|higo/i.test(itemName)) return;
              pantryStock[itemName] = state.pantryStock[itemName];
            });
          }

          if (state.pantryCardUnits && typeof state.pantryCardUnits === 'object') {
            window.pantryCardUnits = state.pantryCardUnits;
          } else {
            window.pantryCardUnits = {};
          }
          if (window.pantryCardUnits) {
            Object.keys(window.pantryCardUnits).forEach(k => {
              if (/aguacate/i.test(k) && (window.pantryCardUnits[k] === 'litros' || window.pantryCardUnits[k] === 'l' || window.pantryCardUnits[k] === 'ml' || window.pantryCardUnits[k] === 'botellas (355 ml)')) {
                window.pantryCardUnits[k] = 'piezas';
              }
            });
          }

          if (state.pantryStockInventory && typeof state.pantryStockInventory === 'object') {
            delete state.pantryStockInventory['miel-pura'];
            delete state.pantryStockInventory['duraznos-frescos'];
            delete state.pantryStockInventory['higos-frescos'];

            // Comprobante Sam's Club 03/10/2026 reemplazado por inventario físico canónico de 106 insumos

            window.PANTRY_STOCK_INVENTORY = Object.assign(window.PANTRY_STOCK_INVENTORY || {}, state.pantryStockInventory);
          }

          if (state.checkedRows) checkedRows = state.checkedRows;
          if (state.mealDinersState) mealDinersState = state.mealDinersState;
          if (state.dispatchedMeals && typeof state.dispatchedMeals === 'object') {
            dispatchedMeals = state.dispatchedMeals;
          } else {
            dispatchedMeals = {};
          }
          window.DISPATCHED_MEALS = dispatchedMeals;
          if (Array.isArray(state.mealFeedbackLedger)) {
            mealFeedbackLedger = state.mealFeedbackLedger;
          } else {
            mealFeedbackLedger = [];
          }
          if (state.customDishesState) {
            customDishesState = state.customDishesState;
            delete customDishesState['Semana 41 (04 al 10 de Octubre de 2026)_day_1_Comida'];
            delete customDishesState['Semana 41 (04 al 10 de Octubre de 2026)_day_3_Comida'];
            delete customDishesState['Semana 41_day_1_Comida'];
            delete customDishesState['Semana 41_day_3_Comida'];
          }
          if (window.MEAL_DISH_OVERRIDES) {
            delete window.MEAL_DISH_OVERRIDES['Semana 41 (04 al 10 de Octubre de 2026)_day_1_Comida'];
            delete window.MEAL_DISH_OVERRIDES['Semana 41 (04 al 10 de Octubre de 2026)_day_3_Comida'];
            delete window.MEAL_DISH_OVERRIDES['Semana 41_day_1_Comida'];
            delete window.MEAL_DISH_OVERRIDES['Semana 41_day_3_Comida'];
          }
          if (state.selectedIdx !== undefined && !isNaN(parseInt(state.selectedIdx))) {
            selectedIdx = parseInt(state.selectedIdx);
          } else {
            selectedIdx = currentDayNum;
          }

          if (Array.isArray(state.customShopItems)) {
            state.customShopItems.forEach(cItem => {
              if (!cItem || !cItem.item_name || /miel|durazno/i.test(cItem.item_name)) return;
              const smartCat = getSmartItemCategory(cItem.item_name, cItem.category);
              const cSlug = normalizeToCanonicalSlug(cItem.item_name);
              const existing = rawShopBase.find(r => normalizeToCanonicalSlug(r.item_name) === cSlug);
              if (existing) {
                existing.category = smartCat;
              } else {
                cItem.category = smartCat;
                rawShopBase.push(cItem);
              }
            });
          }

          // Sanitizar y deduplicar rawShopBase por slug canónico
          const cleanedShopBase = [];
          const seenShopSlugs = new Set();

          rawShopBase.forEach(item => {
            if (!item || !item.item_name) return;
            const cleanName = item.item_name.replace(/\\s*\\/\\s*/g, ' \u2014 ').replace(/\\//g, ' \u2014 ').trim();
            if (!cleanName) return;
            const slug = normalizeToCanonicalSlug(cleanName);
            if (deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === cleanName.toLowerCase())) return;
            if (deletedFarmItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === cleanName.toLowerCase())) return;

            const smartCat = getSmartItemCategory(cleanName, item.category);

            if (!seenShopSlugs.has(slug)) {
              seenShopSlugs.add(slug);
              cleanedShopBase.push({
                ...item,
                item_name: cleanName,
                category: smartCat
              });
            }
          });
          rawShopBase = cleanedShopBase;

          saveAppState();
          return true;
        }
      } catch(e) {
        console.error("Error al cargar localStorage:", e);
      }
      return false;
    }

    function saveAppState() {
      try {
        const customShopItems = rawShopBase.filter(i => i.id > 100);
        const state = {
          activeWeek,
          activeDiners,
          selectedHarvest,
          customFarmItems,
          deletedFarmItems,
          deletedPantryItems,
          pantryStock,
          pantryCardUnits: window.pantryCardUnits || {},
          pantryStockInventory: window.PANTRY_STOCK_INVENTORY || {},
          samsReceiptProcessed_20261003: true,
          checkedRows,
          customShopItems,
          selectedIdx,
          mealDinersState,
          customDishesState,
          dispatchedMeals,
          mealFeedbackLedger: window.MEAL_FEEDBACK_LEDGER || mealFeedbackLedger
        };
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(state));
        localStorage.setItem('nutriketo_app_version', CURRENT_APP_VERSION);
      } catch(e) {
        console.error("Error al guardar localStorage:", e);
      }
    }

    function getMealDiners(dayIdx, mealType) {
      const key = `${activeWeek}_day_${dayIdx}_${mealType}`;
      return (mealDinersState[key] !== undefined) ? parseInt(mealDinersState[key]) : activeDiners;
    }

    function updateMealDiners(dayIdx, mealType, val) {
      const parsed = Math.min(12, Math.max(1, parseInt(val) || activeDiners));
      const key = `${activeWeek}_day_${dayIdx}_${mealType}`;
      mealDinersState[key] = parsed;
      saveAppState();
      renderDay(selectedIdx);
      if (typeof render3DShoppingList === "function") {
        render3DShoppingList();
      }
    }

    function validateNoDuplicateBroths(mObj) {
      const st = (mObj.starter_name || '').toLowerCase();
      const main = (mObj.main_dish_name || mObj.dish_name || '').toLowerCase();
      if ((st.includes('caldo') || st.includes('consomé') || st.includes('sopa')) && (main.includes('caldo') || main.includes('consomé') || main.includes('sopa'))) {
        mObj.starter_name = "Ensalada de Hojas Verdes de la Granja";
      }
      return mObj;
    }

    function enforceFatSourceUniqueness(mObj) {
      const st = (mObj.starter_name || '').toLowerCase();
      const main = (mObj.main_dish_name || mObj.dish_name || '').toLowerCase();
      const side = (mObj.side_dish_name || '').toLowerCase();

      if ((st.includes('aguacate') || st.includes('guacamole') || main.includes('aguacate') || main.includes('guacamole')) && (side.includes('aguacate') || side.includes('guacamole'))) {
        mObj.side_dish_name = "Bastones de Pepino Fresco con Sal de Mar";
      }
      return mObj;
    }

    function validateNoFruitDairyMix(mObj) {
      let st = (mObj.starter_name || '');
      const stLower = st.toLowerCase();
      if ((stLower.includes('pitahaya') || stLower.includes('pitaya') || stLower.includes('higos') || stLower.includes('durazno')) && (stLower.includes('cottage') || stLower.includes('yogur') || stLower.includes('yogurth'))) {
        if (stLower.includes('fresas')) {
          mObj.starter_name = "Fresas Frescas de la Granja con Queso Cottage";
        } else if (stLower.includes('higos')) {
          mObj.starter_name = "Arilos de Granada Fresca con Semillas de Chía y Nueces Pecana";
        } else if (stLower.includes('pitahaya') || stLower.includes('pitaya')) {
          mObj.starter_name = "Pitahaya Fresca de la Granja con Semillas de Chía y Nueces Pecana";
        } else {
          mObj.starter_name = "Duraznos Frescos con Semillas de Chía y Coco Rayado Sin Azúcar";
        }
      }
      return mObj;
    }

    function enforceIngredientDiversityPerMeal(mObj) {
      const st = (mObj.starter_name || '').toLowerCase();
      const main = (mObj.main_dish_name || mObj.dish_name || '').toLowerCase();
      let side = (mObj.side_dish_name || '').toLowerCase();

      const vegRules = [
        { key: 'coliflor', alt: 'Ejotes Tiernos Salteados a la Mantequilla' },
        { key: 'brócoli', alt: 'Espárragos Verdes Asados al Limón' },
        { key: 'brocoli', alt: 'Espárragos Verdes Asados al Limón' },
        { key: 'calabacita', alt: 'Nopales Tiernos Gratinados con Queso Panela' },
        { key: 'espinaca', alt: 'Ensalada Mix de Hojas Verdes de la Granja' },
        { key: 'nopales', alt: 'Ejotes Salteados con Almendras Fileteadas' },
        { key: 'nopal', alt: 'Ejotes Salteados con Almendras Fileteadas' },
        { key: 'aguacate', alt: 'Bastones de Pepino y Apio con Sal de Mar' }
      ];

      vegRules.forEach(v => {
        const inSt = st.includes(v.key);
        const inMain = main.includes(v.key);
        const inSide = side.includes(v.key);

        if ((inSt && inSide) || (inMain && inSide)) {
          mObj.side_dish_name = v.alt;
        } else if (inSt && inMain) {
          mObj.starter_name = "Ensalada Mix de Hojas Verdes de la Granja";
        }
      });

      return mObj;
    }

    
    function getDishRecipeFromPool(dishName, category, mealType) {
      if (!dishName || !window.DISH_EXCHANGE_POOL) return null;
      const list = category === 'starter' ? window.DISH_EXCHANGE_POOL.starters : (category === 'side' ? window.DISH_EXCHANGE_POOL.sides : window.DISH_EXCHANGE_POOL.mains);
      const found = (list || []).find(item => item.name === dishName || item.name.toLowerCase() === dishName.toLowerCase());
      if (found && found.recipe) return found.recipe;
      return null;
    }

    function getMealObj(dayIdx, rawMeal) {
      if (!rawMeal) return {};
      const weekSlug = typeof activeWeek !== 'undefined' ? (activeWeek === 'Semana 38' ? 'semana_38' : activeWeek.toLowerCase().replace(/ /g, '_')) : 'semana_38';
      const key1 = `${weekSlug}_${dayIdx}_${rawMeal.meal_type}`;
      const key2 = `${activeWeek}_day_${dayIdx}_${rawMeal.meal_type}`;
      
      const override = (window.MEAL_DISH_OVERRIDES && window.MEAL_DISH_OVERRIDES[key1]) ||
                       (window.MEAL_DISH_OVERRIDES && window.MEAL_DISH_OVERRIDES[key2]) ||
                       (typeof customDishesState !== 'undefined' && (customDishesState[key1] || customDishesState[key2]));

      let mObj = { ...rawMeal };
      if (override) {
        mObj.starter_name = override.starter_name || rawMeal.starter_name;
        mObj.main_dish_name = override.main_dish_name || rawMeal.main_dish_name || rawMeal.dish_name;
        mObj.side_dish_name = override.side_dish_name || rawMeal.side_dish_name;
        mObj.is_negotiated = true;

        if (override.macros) {
          mObj.calories_kcal = override.macros.kcal;
          mObj.fat_g = override.macros.fat_g;
          mObj.protein_g = override.macros.protein_g;
          mObj.net_carbs_g = override.macros.net_carbs_g;
        }
        if (override.starter_recipe) mObj.starter_recipe = override.starter_recipe;
        if (override.main_recipe) mObj.main_recipe = override.main_recipe;
        if (override.side_recipe) mObj.side_recipe = override.side_recipe;
      }
      
      validateNoDuplicateBroths(mObj);
      enforceFatSourceUniqueness(mObj);
      validateNoFruitDairyMix(mObj);
      enforceIngredientDiversityPerMeal(mObj);
      enforceMetabolicLoadBalance(mObj);
      return mObj;
    }

    function classifyDishDensity(dishName) {
      if (!dishName) return 'LIGERO';
      const d = dishName.toLowerCase();
      if (d.includes('enchilada') || d.includes('mole') || d.includes('queso') || d.includes('ribeye') || d.includes('sirloin') || d.includes('tocino') || d.includes('gratinado') || d.includes('albóndiga') || d.includes('albondiga') || d.includes('waffle') || d.includes('crepa') || d.includes('parrillada') || d.includes('chiles rellenos')) {
        return 'DENSO';
      }
      if (d.includes('pollo') || d.includes('pavo') || d.includes('pescado') || d.includes('salmón') || d.includes('salmon') || d.includes('omelette') || d.includes('frittata') || d.includes('shakshuka')) {
        return 'MEDIO';
      }
      return 'LIGERO';
    }

    function enforceMetabolicLoadBalance(mObj) {
      if (!mObj) return mObj;
      const mainDensity = classifyDishDensity(mObj.main_dish_name || mObj.dish_name);

      if (mainDensity === 'DENSO') {
        const stLower = (mObj.starter_name || '').toLowerCase();
        const stDensity = classifyDishDensity(mObj.starter_name);
        if (stDensity !== 'LIGERO' || stLower.includes('aguacate') || stLower.includes('queso')) {
          mObj.starter_name = "Ensalada Verde de Arúgula y Espinaca Baby a la Vinagreta de Manzana";
        }

        const sdLower = (mObj.side_dish_name || '').toLowerCase();
        const sdDensity = classifyDishDensity(mObj.side_dish_name);
        if (sdDensity !== 'LIGERO' || sdLower.includes('puré') || sdLower.includes('pure') || sdLower.includes('queso')) {
          mObj.side_dish_name = "Gelatina Artesanal elaborada con Grenetina Natural y Fruta Fresca de la Granja Sin Azúcar";
        }
      }
      return mObj;
    }

    function resolveKetoDishAlias(dishName) {
      let name = dishName || '';
      if (!name) return name;
      let lower = name.toLowerCase();

      if (lower.includes('frijol') || lower.includes('frijoles')) {
        return 'Consomé Claro de Nopales y Hortalizas Tiernas';
      }
      if (lower.includes('chipotle')) {
        name = name.replace(/chipotle/gi, 'Ajo y Tomillo');
      }
      if (lower.includes('arroz') && !lower.includes('coliflor')) {
        name = name.replace(/arroz/gi, 'Cuscús de Coliflor y Ejotes');
      }

      // PATCH V13.2 & V13.3: NOMENCLATURA GASTRONÓMICA Y DEPURACIÓN SENSORIAL (SUPRESIÓN DE "KETO" Y "SIN AZÚCAR")
      name = name.replace(/\\s*Keto\\b/gi, '');
      name = name.replace(/\\s*Cetogénico\\b/gi, '');
      name = name.replace(/\\s*Cetogénica\\b/gi, '');
      name = name.replace(/\\s*Low-Carb\\b/gi, '');
      name = name.replace(/\\(Fideos Keto\\)/gi, '');
      name = name.replace(/\\(Keto\\)/gi, '');
      name = name.replace(/\\s*Sin Azúcar\\b/gi, '');
      name = name.replace(/\\s*Sin Azucar\\b/gi, '');
      name = name.replace(/\\s*Zero\\b/gi, '');
      name = name.replace(/\\s*Dietético\\b/gi, '');
      name = name.replace(/\\s*Dietética\\b/gi, '');
      name = name.replace(/de Grenetina con/gi, 'de');
      name = name.replace(/\\s+/g, ' ').trim();

      return name;
    }

    const compiledPhasesCache = {};

    async function fetchDayPrepPhasesJIT(dayIdx) {
      const day = (getPlanForWeek(activeWeek) && getPlanForWeek(activeWeek).days) ? getPlanForWeek(activeWeek).days[dayIdx] : null;
      if (!day || !day.meals) return;

      const itemsToCompile = [];
      day.meals.forEach(rawM => {
        const m = getMealObj(dayIdx, rawM);
        const diners = getMealDiners(dayIdx, m.meal_type);

        [m.starter_name, m.main_dish_name || m.dish_name, m.side_dish_name].forEach(name => {
          if (name && !compiledPhasesCache[name]) {
            itemsToCompile.push({
              dish_name: name,
              approved_ingredients: m.ingredients || [],
              diners_count: diners
            });
          }
        });
      });

      if (itemsToCompile.length === 0) return;

      try {
        const res = await fetch('/api/menu/compile-phases', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items: itemsToCompile })
        });
        if (res.ok) {
          const data = await res.json();
          if (data.compiled_phases) {
            Object.assign(compiledPhasesCache, data.compiled_phases);
            renderDay(dayIdx);
          }
        }
      } catch(e) {
        console.warn("JIT Phase compilation offline or fallback:", e);
      }
    }

    function renderDynamicPrepPhases(dishName, diners, ingredients) {
      const name = resolveKetoDishAlias(dishName);
      const phases = compiledPhasesCache[name] || compiledPhasesCache[dishName];
      if (phases) {
        const f1 = phases.fase_1_mise_en_place || phases.f1 || `Fase 1 (Mise en Place): Pesar insumos para ${diners} comensales.`;
        const f2 = phases.fase_2_acondicionamiento || phases.f2 || `Fase 2 (Acondicionamiento): Porcionado e higienización.`;
        const f3 = phases.fase_3_termodinamica || phases.f3 || `Fase 3 (Termodinámica): Cocción regulada a temperatura óptima.`;
        const f4 = phases.fase_4_servicio || phases.f4 || `Fase 4 (Servicio): Emplatado para ${diners} personas a 65°C.`;
        return `
          <ul>
            <li><span class="green-bullet">✦</span> <strong>Fase 1 (Mise en Place):</strong> ${f1}</li>
            <li><span class="green-bullet">✦</span> <strong>Fase 2 (Acondicionamiento):</strong> ${f2}</li>
            <li><span class="green-bullet">✦</span> <strong>Fase 3 (Termodinámica):</strong> ${f3}</li>
            <li><span class="green-bullet">✦</span> <strong>Fase 4 (Servicio):</strong> ${f4}</li>
          </ul>
        `;
      }
      
      const n = parseInt(diners) || 6;
      const dLower = (name || '').toLowerCase();
      
      function resolveTechniqueJS(dishName) {
        const nm = (dishName || '').toLowerCase();
        if (['infusión', 'infusion', 'té ', 'te ', 'tisana', 'café', 'cafe'].some(k => nm.includes(k))) return 'steep_beverage';
        if (['crema', 'sopa', 'caldo', 'consomé', 'consome'].some(k => nm.includes(k))) return 'boil_and_blend';
        if (['gelatina', 'mousse', 'panna cotta'].some(k => nm.includes(k))) return 'gelatin_molding';
        if (['çılbır', 'cilbir', 'turcos', 'pochado', 'pochados', 'benedict'].some(k => nm.includes(k))) return 'poach_and_emulsion';
        if (['omelette', 'huevo', 'revuelto', 'frittata', 'shakshuka'].some(k => nm.includes(k))) return 'pan_fry_egg';
        if (['higos', 'granada', 'fruta', 'ensalada', 'bastones', 'pepino', 'tartar'].some(k => nm.includes(k))) return 'raw_assembly';
        if (['salmón', 'salmon', 'pechuga', 'pavo', 'pollo', 'carne', 'corte'].some(k => nm.includes(k))) return 'saute_and_sear';
        return 'raw_assembly'; // Default seguro NUNCA debe ser infusión
      }

      const tech = resolveTechniqueJS(name);

      let f1, f2, f3, f4, techBadge;
      if (tech === 'steep_beverage') {
        techBadge = "🍵 Infusión Herbal & Bebida";
        f1 = `Fase 1 (Mise en Place de Bebidas):\n* Insumos base para ${n} personas: Sobres o mezcla de ${name}.\n* Agua purificada: ${n * 250} ml de agua de manantial.`;
        f2 = `Fase 2 (Calentamiento de Agua):\n* Llevar ${n * 250} ml de agua purificada a ebullición suave (95°C) en tetera.`;
        f3 = `Fase 3 (Infusión Herbal):\n* Verter el agua hirviendo sobre ${name} e infundir 5 a 6 minutos.`;
        f4 = `Fase 4 (Servicio):\n* Colar y servir caliente a 70°C en tazas térmicas.`;
      } else if (tech === 'boil_and_blend') {
        techBadge = "🍲 Crema / Sopa (Licuado & Cremado Lácteo)";
        f1 = `Fase 1 (Mise en Place y Gramajes de Crema):\n* Insumos base para ${n} personas: Vegetales e insumos de ${name}.\n* Base líquida: ${n * 125} ml de caldo tibio y mantequilla de pastoreo.`;
        f2 = `Fase 2 (Base Sofrito Aromático):\n* En cacerola a fuego medio, sofrito de cebolla, ajo y mantequilla por 4 minutos hasta acitronar sin quemar.`;
        f3 = `Fase 3 (Cocción en Caldo, Licuado & Cremado):\n* Verter el caldo y vegetales. Hervir suavemente (95°C) durante 8-10 minutos hasta ternura.\n* Licuar a alta velocidad por 2 minutos hasta lograr textura aterciopelada.\n* Regresar a fuego muy bajo, integrar crema/queso rallado agitando suavemente sin dejar hervir.`;
        f4 = `Fase 4 (Servicio Gourmet):\n* Servir en tazones hondos precalentados a 68°C con láminas de queso, pimienta negra y un hilo de aceite VEVO.`;
      } else if (tech === 'gelatin_molding') {
        techBadge = "🍮 Gelatina Artesanal & Moldeo a 4°C";
        f1 = `Fase 1 (Mise en Place y Gramajes):\n* Jugo fresco o base de ${name} para ${n} personas con grenetina natural e insumos de la granja.`;
        f2 = `Fase 2 (Hidratación & Disolución):\n* Hidratar grenetina en agua fría 5 minutos; disolver a 60°C mezclando con el jugo caliente.`;
        f3 = `Fase 3 (Moldeo & Refrigeración):\n* Integrar el resto del líquido fresco y verter en moldes individuales a 4°C por 3 horas.`;
        f4 = `Fase 4 (Servicio en Frío):\n* Servir frío a 4°C firmemente cuajado.`;
      } else if (tech === 'poach_and_emulsion') {
        techBadge = "🍳 Huevos Pochados Çılbır (Base de Yogur & Mantequilla Especiada)";
        f1 = `Fase 1 (Mise en Place y Gramajes):\n* 12 huevos frescos, 750 g (3 tazas) yogur griego natural a temp. ambiente, 3 dientes de ajo rallados, 135 g mantequilla de pastoreo, 45 ml aceite VEVO, 1 cda paprika dulce/orégano, 1.5 cditas comino molido, 3 cdas vinagre.`;
        f2 = `Fase 2 (Base de Yogur & Mantequilla Especiada):\n* Batir yogur con ajo y sal en tazón formando cama en 6 platos. Derretir mantequilla con aceite de oliva a fuego medio-bajo hasta dorar (avellanada); retirar e incorporar paprika dulce y comino.`;
        f3 = `Fase 3 (Pochado Regulado a 85-90°C):\n* Hervir agua con vinagre a 85-90°C. Cuelar clara líquida y pochar 3-4 huevos por tanda exactamente 3 minutos para yema líquida. Escurrir en papel absorbente.`;
        f4 = `Fase 4 (Montaje Gourmet por Capas):\n* Colocar 2 huevos pochados sobre cama de yogur en cada plato, bañar con mantequilla especiada tibia, eneldo fresco y pimienta negra. Servir a 55-60°C.`;
      } else if (tech === 'pan_fry_egg') {
        techBadge = "🍳 Huevos Revueltos / Omelette en Sartén";
        f1 = `Fase 1 (Mise en Place y Gramajes):\n* Huevos frescos (${n * 2} piezas), mantequilla de pastoreo, aromáticos y sal de mar.`;
        f2 = `Fase 2 (Batido e Integración):\n* Batir huevos energéticamente con globo homogenizando clara y yema.`;
        f3 = `Fase 3 (Cocción Regulada en Sartén):\n* Calentar sartén antiadherente a fuego medio-bajo con mantequilla. Cuajar suavemente 3-4 minutos.`;
        f4 = `Fase 4 (Servicio Culinario):\n* Servir de inmediato a 60°C.`;
      } else if (tech === 'saute_and_sear') {
        techBadge = "🔥 Sello Térmico & Reposo Culinario";
        f1 = `Fase 1 (Mise en Place y Gramajes Exactos):\n* Proteína e insumos de ${name} escalados para ${n} personas con grasas saludables y sal de mar.`;
        f2 = `Fase 2 (Acondicionamiento Culinario):\n* Porcionar en cortes uniformes sazonando homogéneamente.`;
        f3 = `Fase 3 (Termodinámica y Sello en Sartén):\n* Calentar sartén de hierro a 180°C con materia grasa. Sellar 4 min por lado hasta costra dorada. Reposar 4 min.`;
        f4 = `Fase 4 (Ensamblaje y Servicio):\n* Trinchar contra la fibra y emplatar repartiendo equitativamente para ${n} personas a 65°C.`;
      } else {
        techBadge = "🥗 Ensamblaje en Frío & Macerado (4°C)";
        f1 = `Fase 1 (Mise en Place en Frío):\n* Pesar hortalizas/insumos frescos de ${name} para ${n} personas.\n* Sazonadores y aceites a 4°C.`;
        f2 = `Fase 2 (Higienización y Corte):\n* Lavar e higienizar en agua helada (4°C). Porcionar en cubos de 1 cm o bastones de 7-8 cm.`;
        f3 = `Fase 3 (Emulsión en Frío):\n* Emulsionar el aderezo frío y marinar/macerar a 4°C por 8 minutos.`;
        f4 = `Fase 4 (Servicio en Frío):\n* Montar en vajilla refrigerada y servir fresco a 4-8°C.`;
      }

      return `
        <div style="font-size:0.75rem; font-weight:800; background:var(--bg-clinical); color:var(--color-corporate); padding:0.2rem 0.5rem; border-radius:6px; margin-bottom:0.4rem; display:inline-block; border:1px solid var(--border-clinical);">${techBadge}</div>
        <ul>
          <li><span class="green-bullet">✦</span> ${f1}</li>
          <li><span class="green-bullet">✦</span> ${f2}</li>
          <li><span class="green-bullet">✦</span> ${f3}</li>
          <li><span class="green-bullet">✦</span> ${f4}</li>
        </ul>
      `;
    }

    function initSetupPanel() {
      // 1. Cosecha Grid (sección editable ordenada A-Z de catálogo maestro + personalizados)
      const hGrid = document.getElementById('harvest-checklist-grid');
      if (hGrid) {
        hGrid.innerHTML = '';
        const activeFarmMaster = FARM_MASTER_CATALOG.filter(name => {
          const slug = normalizeToCanonicalSlug(name);
          return !deletedFarmItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === name.toLowerCase());
        });
        const activeCustomFarm = customFarmItems.filter(name => {
          const slug = normalizeToCanonicalSlug(name);
          return !deletedFarmItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === name.toLowerCase());
        });

        const allFarmNames = [...new Set([...activeFarmMaster, ...activeCustomFarm])];
        allFarmNames.sort((a, b) => a.localeCompare(b));

        allFarmNames.forEach((itemName, idx) => {
          const isCanonical = FARM_MASTER_CATALOG.includes(itemName);
          const slug = normalizeToCanonicalSlug(itemName);
          const isChecked = selectedHarvest.some(h => {
            const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
            return normalizeToCanonicalSlug(hStr) === slug || hStr.toLowerCase() === itemName.toLowerCase();
          });

          const div = document.createElement('div');
          div.className = 'option-row';
          div.style.color = 'var(--text-main)';
          const safeName = itemName.replace(/'/g, "\\'");
          div.style.cssText = 'display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; padding: 0.5rem 0.75rem; border-radius: 10px; background: var(--surface-card); border: 1px solid var(--border-clinical); box-shadow: var(--shadow-clinical-sm);';
          div.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem; flex: 1; min-width: 0;">
              <input type="checkbox" id="h-item-${idx}" value="${safeName}" ${isChecked ? 'checked' : ''} onchange="updateHarvestSelection('${safeName}', this.checked)">
              <label for="h-item-${idx}" style="cursor:pointer; flex: 1; color: var(--text-main); font-weight: 700; font-size: 0.85rem; word-break: break-word;">${itemName}</label>
            </div>
            <button type="button" onclick="deleteHarvestItem('${safeName}')" style="background: none; border: none; color: #ef4444; font-size: 0.95rem; cursor: pointer; padding: 0.1rem 0.3rem; opacity: 0.7; transition: opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.7'" title="Eliminar ${safeName} de la Cosecha">🗑️</button>
          `;
          hGrid.appendChild(div);
        });
      }

      // 2. Alacena Grid (sección editable seccionada por Categoría y ordenada A-Z)
      const pGrid = document.getElementById('pantry-stock-grid');
      if (pGrid) {
        pGrid.innerHTML = '';
        const nonFarm = [];
        const seenPantrySlugs = new Set();
        if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};

        // 2.1 Insumos Físicos de Despensa (window.PANTRY_STOCK_INVENTORY)
        // Regla de Oro: En Reconfigurar Parámetros sólo se muestran los 106 insumos que realmente existen en el inventario físico de la despensa.
        // const isCurrentlyHarvested = selectedHarvest.some(h => areInsumosEquivalent(h, 'test'));
        if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined') {
          Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(k => {
            const pObj = window.PANTRY_STOCK_INVENTORY[k];
            if (!pObj) return;
            // Excluir claves de compatibilidad interna con stock 0 (como frutas de catálogo o ajo-fresco de test)
            if (pObj.stock <= 0 && (!pObj.item_num || pObj.item_num <= 0)) return;
            // Excluir alias duplicados para no repetir el mismo ítem en la pantalla
            if (k === 'multisinergix' || k === 'aminosinergix' || k === '33plus' || k === '34plus' || k === 'zarzamoras-frescas' || k === 'fresas-frescas' || k === 'arilos-granada' || k === 'moras-frescas' || k === 'frambuesas-frescas' || k === 'arandanos-frescos' || k === 'pitaya-fresca' || k === 'ajo-fresco') return;

            const slug = normalizeToCanonicalSlug(pObj.name || k);
            if (deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === pObj.name.toLowerCase())) return;
            const alreadyInList = nonFarm.some(existing => areInsumosEquivalent(existing.item_name, pObj.name));
            if (!alreadyInList) {
              seenPantrySlugs.add(slug);
              const assignedCat = (pObj.status === 'prohibited')
                ? '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)'
                : (pObj.category || getSmartItemCategory(pObj.name));
              nonFarm.push({
                item_name: pObj.name,
                quantity: pObj.stock,
                unit: pObj.unit || 'g',
                category: assignedCat,
                status: pObj.status || 'canonical',
                packaging: pObj.packaging
              });
            }
          });
        }

        // 2.3 Insumos en Cuarentena (extraídos dinámicamente de window.PANTRY_STOCK_INVENTORY)
        const QUARANTINE_PANTRY_ITEMS = [];

        QUARANTINE_PANTRY_ITEMS.forEach(qItem => {
          const slug = normalizeToCanonicalSlug(qItem.item_name);
          if (!deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === qItem.item_name.toLowerCase())) {
            const alreadyInList = nonFarm.some(existing => areInsumosEquivalent(existing.item_name, qItem.item_name));
            if (!alreadyInList) {
              seenPantrySlugs.add(slug);
              nonFarm.push(qItem);
            }
          }
        });

        const categoriesMap = {};
        nonFarm.forEach(i => {
          const cat = i.category || getSmartItemCategory(i.item_name, i.category);
          if (!categoriesMap[cat]) categoriesMap[cat] = [];
          categoriesMap[cat].push(i);
        });

        const sortedCats = Object.keys(categoriesMap).sort((a, b) => getCategoryIndex(a) - getCategoryIndex(b));

        sortedCats.forEach(catName => {
          const isQuarantine = catName.includes('Cuarentena') || catName.includes('🛑');
          const catHeader = document.createElement('div');
          if (isQuarantine) {
            catHeader.style.cssText = 'grid-column: 1 / -1; font-weight: 800; font-size: 0.95rem; color: #dc2626; margin-top: 1.2rem; margin-bottom: 0.5rem; padding: 0.45rem 0.75rem; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #dc2626; border-radius: 8px; display: flex; align-items: center; gap: 0.4rem;';
          } else {
            catHeader.style.cssText = 'grid-column: 1 / -1; font-weight: 800; font-size: 0.92rem; color: var(--color-34plus); margin-top: 0.8rem; margin-bottom: 0.4rem; padding-bottom: 0.3rem; border-bottom: 2px solid var(--border-clinical); display: flex; align-items: center; gap: 0.4rem;';
          }
          catHeader.innerHTML = `<span>${catName}</span>`;
          pGrid.appendChild(catHeader);

          const items = categoriesMap[catName];
          items.sort((a, b) => a.item_name.localeCompare(b.item_name, 'es', { sensitivity: 'base' }));

          items.forEach(i => {
            const slug = normalizeToCanonicalSlug(i.item_name);
            const safeName = i.item_name.replace(/'/g, "\\'");

            const options = getCommercialUnitOptions(i.item_name, i.unit, i.quantity);
            let currentUnit = window.pantryCardUnits[i.item_name];
            if (!currentUnit) {
              if (window.PANTRY_STOCK_INVENTORY) {
                const invKey = Object.keys(window.PANTRY_STOCK_INVENTORY).find(k => areInsumosEquivalent(window.PANTRY_STOCK_INVENTORY[k].name, i.item_name));
                if (invKey && window.PANTRY_STOCK_INVENTORY[invKey].unit) {
                  currentUnit = window.PANTRY_STOCK_INVENTORY[invKey].unit;
                }
              }
            }
            if (!currentUnit && options.length > 0) {
              currentUnit = options[0].id;
            }
            window.pantryCardUnits[i.item_name] = currentUnit;

            let val = pantryStock[i.item_name];
            if (val === undefined) {
              const matchedKey = Object.keys(pantryStock).find(k => areInsumosEquivalent(k, i.item_name));
              if (matchedKey !== undefined) {
                val = pantryStock[matchedKey];
              } else if (window.PANTRY_STOCK_INVENTORY) {
                const invKey = Object.keys(window.PANTRY_STOCK_INVENTORY).find(k => areInsumosEquivalent(window.PANTRY_STOCK_INVENTORY[k].name, i.item_name));
                val = invKey ? window.PANTRY_STOCK_INVENTORY[invKey].stock : 0;
              } else {
                val = 0;
              }
            }

            const isEggItem = /huevo/i.test(i.item_name);
            const eggHelperBtn = isEggItem ? `
              <button type="button" onclick="addPantryCasillero('${safeName}')" style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 4px; padding: 2px 6px; font-size: 0.72rem; font-weight: 700; color: #047857; cursor: pointer; white-space: nowrap; transition: all 0.2s;" onmouseover="this.style.background='rgba(16,185,129,0.25)'" onmouseout="this.style.background='rgba(16,185,129,0.12)'" title="Sumar 1 casillero completo (+30 piezas)">+30 (1 Casillero)</button>
            ` : '';

            const selectHtml = options.length > 0 ? `
              <select style="padding: 0.25rem 0.35rem; font-weight: 700; font-size: 0.78rem; border: 1px solid ${isQuarantine ? 'rgba(239, 68, 68, 0.5)' : 'var(--border-clinical)'}; border-radius: 6px; background: var(--surface-card); color: var(--text-main); cursor: pointer; max-width: 145px;" onchange="updatePantryStockUnit('${safeName}', this.value, this.previousElementSibling)">
                ${options.map(opt => `<option value="${opt.id}" ${opt.id === currentUnit ? 'selected' : ''}>${opt.label}</option>`).join('')}
              </select>
            ` : `<span style="font-size: 0.78rem; font-weight: 600; color: ${isQuarantine ? '#dc2626' : 'var(--text-muted)'};">${i.unit}</span>`;

            const div = document.createElement('div');
            div.className = isQuarantine ? 'option-row quarantine-card-item' : 'option-row';
            div.style.color = 'var(--text-main)';
            if (isQuarantine) {
              div.style.cssText = 'display: flex; flex-direction: column; justify-content: space-between; gap: 0.4rem; padding: 0.55rem 0.75rem; border-radius: 10px; background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.35); box-shadow: var(--shadow-clinical-sm);';
            } else {
              div.style.cssText = 'display: flex; flex-direction: column; justify-content: space-between; gap: 0.4rem; padding: 0.55rem 0.75rem; border-radius: 10px; background: var(--surface-card); border: 1px solid var(--border-clinical); box-shadow: var(--shadow-clinical-sm);';
            }
            div.innerHTML = `
              <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 0.4rem; width: 100%;">
                <span style="font-weight: 700; font-size: 0.88rem; color: ${isQuarantine ? '#dc2626' : 'var(--text-main)'}; word-break: break-word; line-height: 1.25;">${i.item_name}</span>
                <button type="button" onclick="deletePantryItem('${safeName}')" style="background: none; border: none; color: #ef4444; font-size: 0.95rem; cursor: pointer; padding: 0.1rem 0.3rem; border-radius: 4px; opacity: 0.7; transition: opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.7'" title="Eliminar ${safeName} del Inventario">🗑️</button>
              </div>
              <div style="display: flex; align-items: center; justify-content: flex-end; gap: 0.4rem; width: 100%; margin-top: 0.2rem; flex-wrap: wrap;">
                ${eggHelperBtn}
                <input type="number" step="${currentUnit === 'piezas' || currentUnit === 'casillero' ? '1' : '0.1'}" min="0" value="${val}" style="width: 70px; padding: 0.25rem 0.4rem; font-weight: 800; text-align: center; border: 1px solid ${isQuarantine ? 'rgba(239, 68, 68, 0.5)' : 'var(--border-clinical)'}; border-radius: 6px; background: var(--surface-card); color: var(--text-main); font-size: 0.88rem;" onchange="updatePantryStock('${safeName}', this.value, window.pantryCardUnits['${safeName}'])">
                ${selectHtml}
              </div>
            `;
            pGrid.appendChild(div);
          });
        });
      }

      if (document.getElementById('setup-week')) document.getElementById('setup-week').value = activeWeek;
      if (document.getElementById('setup-diners')) document.getElementById('setup-diners').value = activeDiners;
    }

    function toggleEditDetails() {
      const details = document.getElementById('edit-inventory-details');
      if (details) {
        if (details.style.display === 'none' || !details.style.display) {
          details.style.display = 'block';
        } else {
          details.style.display = 'none';
        }
      }
    }

    function addNewHarvestItem() {
      const nameInput = document.getElementById('new-harvest-name');
      let val = nameInput ? nameInput.value.trim() : '';
      if (!val) {
        if (typeof showToast === 'function') {
          showToast('⚠️ Por favor escribe el nombre del insumo para la Cosecha.', 'warning');
        }
        if (nameInput) nameInput.focus();
        return;
      }

      if (/nuex/i.test(val)) {
        val = val.replace(/nuex/gi, 'nuez');
      }
      if (/^nuez\\s+pecana$/i.test(val.trim())) {
        val = "Nuez pecana fresca de la granja";
      }

      const slug = normalizeToCanonicalSlug(val);
      deletedFarmItems = deletedFarmItems.filter(d => normalizeToCanonicalSlug(d) !== slug && d.toLowerCase() !== val.toLowerCase());

      const existsInMaster = FARM_MASTER_CATALOG.some(m => normalizeToCanonicalSlug(m) === slug || m.toLowerCase() === val.toLowerCase());
      if (!existsInMaster) {
        const existsInCustom = customFarmItems.some(c => normalizeToCanonicalSlug(c) === slug || c.toLowerCase() === val.toLowerCase());
        if (!existsInCustom) {
          customFarmItems.push(val);
        }
      }

      const existsInSelected = selectedHarvest.some(h => {
        const hName = typeof h === 'string' ? h : (h.item_name || h.name || '');
        return normalizeToCanonicalSlug(hName) === slug || hName.toLowerCase() === val.toLowerCase();
      });

      if (!existsInSelected) {
        selectedHarvest.push(val);
      }

      const existsInShop = rawShopBase.some(i => normalizeToCanonicalSlug(i.item_name) === slug || i.item_name.toLowerCase() === val.toLowerCase());
      if (!existsInShop) {
        const newId = 100 + rawShopBase.length + 1;
        rawShopBase.push({
          id: newId,
          category: "🌾 Cosecha Directa de la Granja / Huerto",
          item_name: val,
          quantity: 1.0,
          unit: "kg/piezas",
          quantity_str: "1.0 kg/piezas"
        });
      }

      if (nameInput) nameInput.value = '';
      saveAppState();
      initSetupPanel();
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
      if (typeof showToast === 'function') showToast(`🌿 '${val}' añadido a Cosecha Activa.`);
    }

    function updatePantryCatBadge(cat) {
      const badge = document.getElementById('pantry-cat-indicator');
      if (!badge) return;
      if (cat.includes('Cuarentena') || cat.includes('🛑') || cat.includes('prohibited')) {
        badge.textContent = 'Destino: 🛑 Cuarentena (Fuera de Protocolo)';
        badge.style.background = 'rgba(239, 68, 68, 0.15)';
        badge.style.color = '#dc2626';
        badge.style.borderColor = 'rgba(239, 68, 68, 0.4)';
      } else {
        badge.textContent = `Destino: ${cat}`;
        badge.style.background = 'rgba(28,117,188,0.12)';
        badge.style.color = '#1C75BC';
        badge.style.borderColor = 'rgba(28,117,188,0.25)';
      }
    }

    function onNewPantryNameInput(val) {
      const catSelect = document.getElementById('new-pantry-cat');
      const unitSelect = document.getElementById('new-pantry-unit');
      const qBox = document.getElementById('pantry-quarantine-reason-box');
      if (!val || !val.trim()) {
        updatePantryCatBadge('🥬 Verduras, Hortalizas y Frescos');
        if (qBox) qBox.style.display = 'none';
        return;
      }

      // Sugerir categoría automáticamente si el usuario no la ha fijado manualmente
      if (catSelect && catSelect.dataset.userLocked !== 'true') {
        const smartCat = getSmartItemCategory(val, '');
        catSelect.value = smartCat;
        updatePantryCatBadge(smartCat);
        if (qBox) {
          qBox.style.display = (smartCat.includes('Cuarentena') || smartCat.includes('🛑')) ? 'block' : 'none';
        }
      }

      // Sugerir unidad de empaque comercial si el usuario no la ha fijado manualmente
      if (unitSelect && unitSelect.dataset.userLocked !== 'true') {
        const v = val.toLowerCase();
        if (/huevo|huevos/i.test(v)) {
          unitSelect.value = 'casillero';
        } else if (/sardina|sardinas|atún|atun/i.test(v)) {
          unitSelect.value = 'latas';
        } else if (/yogurt|yoghurt/i.test(v)) {
          unitSelect.value = 'bote_900';
        } else if (/leche de coco|leche/i.test(v)) {
          unitSelect.value = 'ml';
        } else if (/mayonesa|ghee|mantequilla|crema/i.test(v)) {
          unitSelect.value = 'frasco_500';
        } else if (/aceite|vinagre/i.test(v)) {
          unitSelect.value = 'botella_vevo';
        } else if (/frijol|arroz/i.test(v)) {
          unitSelect.value = 'bolsa_750';
        } else if (/lenteja|garbanzo/i.test(v)) {
          unitSelect.value = 'bolsa_500';
        } else if (/sal\b|pimienta|orégano|oregano|comino|canela|clavo|epazote|romero|tomillo/i.test(v)) {
          unitSelect.value = 'g';
        } else if (/chayote|pepino|aguacate/i.test(v)) {
          unitSelect.value = 'piezas';
        } else {
          unitSelect.value = 'kg';
        }
      }
    }

    function onNewPantryCatChange(cat) {
      const catSelect = document.getElementById('new-pantry-cat');
      if (catSelect) catSelect.dataset.userLocked = 'true';
      updatePantryCatBadge(cat);
      const qBox = document.getElementById('pantry-quarantine-reason-box');
      if (qBox) {
        qBox.style.display = (cat.includes('Cuarentena') || cat.includes('🛑')) ? 'block' : 'none';
      }
    }

    function addNewPantryItem() {
      const nameInput = document.getElementById('new-pantry-name');
      const catSelect = document.getElementById('new-pantry-cat');
      const qtyInput = document.getElementById('new-pantry-qty');
      const unitSelect = document.getElementById('new-pantry-unit');
      const reasonInput = document.getElementById('new-pantry-reason');

      const val = nameInput ? nameInput.value.trim() : '';
      const chosenCat = catSelect ? catSelect.value : getSmartItemCategory(val);
      const qty = parseFloat(qtyInput ? qtyInput.value : 1.0) || 1.0;
      const unit = (unitSelect ? unitSelect.value.trim() : '') || 'kg';
      const reason = (reasonInput ? reasonInput.value.trim() : '') || '';

      if (!val) {
        if (typeof showToast === 'function') {
          showToast('⚠️ Por favor escribe el nombre del insumo para la Alacena.', 'warning');
        }
        if (nameInput) nameInput.focus();
        return;
      }

      const isQuarantine = chosenCat.includes('Cuarentena') || chosenCat.includes('🛑');
      const itemStatus = isQuarantine ? 'prohibited' : 'canonical';

      const slug = normalizeToCanonicalSlug(val);
      deletedPantryItems = deletedPantryItems.filter(d => normalizeToCanonicalSlug(d) !== slug && d.toLowerCase() !== val.toLowerCase());

      const existingInShop = rawShopBase.find(i => normalizeToCanonicalSlug(i.item_name) === slug || i.item_name.toLowerCase() === val.toLowerCase());
      const canonicalName = existingInShop ? existingInShop.item_name : val;

      pantryStock[canonicalName] = qty;
      if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};
      window.pantryCardUnits[canonicalName] = unit;

      if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined' && window.PANTRY_STOCK_INVENTORY) {
        window.PANTRY_STOCK_INVENTORY[slug] = {
          name: canonicalName,
          stock: qty,
          unit: unit,
          category: chosenCat,
          status: itemStatus,
          reason: isQuarantine ? (reason || 'Insumo fuera de protocolo cetogénico (Cuarentena NOM-004)') : null
        };
      }

      // Si es canónico y no está en rawShopBase, lo registramos para que pueda calcularse amortización si entra al menú
      if (!isQuarantine && !existingInShop) {
        const newId = 200 + rawShopBase.length + 1;
        rawShopBase.push({
          id: newId,
          category: chosenCat,
          item_name: canonicalName,
          quantity: qty,
          unit: unit,
          quantity_str: `${qty} ${unit}`
        });
      }

      // Resetear campos
      if (nameInput) nameInput.value = '';
      if (qtyInput) qtyInput.value = '1';
      if (catSelect) {
        catSelect.dataset.userLocked = '';
        catSelect.value = '🥬 Verduras, Hortalizas y Frescos';
      }
      if (unitSelect) {
        unitSelect.dataset.userLocked = '';
        unitSelect.value = 'kg';
      }
      if (reasonInput) reasonInput.value = '';
      const qBox = document.getElementById('pantry-quarantine-reason-box');
      if (qBox) qBox.style.display = 'none';
      updatePantryCatBadge('🥬 Verduras, Hortalizas y Frescos');

      saveAppState();
      initSetupPanel();
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
      if (typeof showToast === 'function') {
        if (isQuarantine) {
          showToast(`🛑 '${canonicalName}' colocado en Cuarentena (${qty} ${unit}).`, 'warning');
        } else {
          showToast(`📦 '${canonicalName}' registrado en ${chosenCat} (${qty} ${unit}).`, 'success');
        }
      }
    }

    function updateHarvestSelection(itemName, isChecked) {
      const slug = normalizeToCanonicalSlug(itemName);
      if (isChecked) {
        const exists = selectedHarvest.some(h => {
          const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
          return normalizeToCanonicalSlug(hStr) === slug || hStr.toLowerCase() === itemName.toLowerCase();
        });
        if (!exists) {
          selectedHarvest.push(itemName);
        }
      } else {
        selectedHarvest = selectedHarvest.filter(h => {
          const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
          return normalizeToCanonicalSlug(hStr) !== slug && hStr.toLowerCase() !== itemName.toLowerCase();
        });
      }
      saveAppState();
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
    }

    function updatePantryStock(itemName, val, unit) {
      const parsed = parseFloat(val) || 0;
      if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};
      const cardUnit = unit || window.pantryCardUnits[itemName] || 'g';
      window.pantryCardUnits[itemName] = cardUnit;
      pantryStock[itemName] = parsed;

      const slug = normalizeToCanonicalSlug(itemName);
      if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined' && window.PANTRY_STOCK_INVENTORY) {
        const matchedKey = Object.keys(window.PANTRY_STOCK_INVENTORY).find(k => 
          k === slug || areInsumosEquivalent(window.PANTRY_STOCK_INVENTORY[k].name, itemName)
        );
        if (matchedKey) {
          window.PANTRY_STOCK_INVENTORY[matchedKey].stock = parsed;
          window.PANTRY_STOCK_INVENTORY[matchedKey].unit = cardUnit;
        } else {
          window.PANTRY_STOCK_INVENTORY[slug] = {
            name: itemName,
            stock: parsed,
            unit: cardUnit,
            status: 'canonical'
          };
        }
      }
      saveAppState();
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
    }

    function addPantryCasillero(itemName) {
      if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};
      const currentUnit = window.pantryCardUnits[itemName] || 'piezas';
      const current = parseFloat(pantryStock[itemName]) || 0;
      let increment = 30;
      if (currentUnit === 'casillero') {
        increment = 1;
      } else if (currentUnit === 'docena') {
        increment = 2.5;
      }
      const newVal = current + increment;
      updatePantryStock(itemName, newVal, currentUnit);
      initSetupPanel();
    }

    function updatePantryStockUnit(itemName, newUnitId, inputElem) {
      if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};
      const oldUnitId = window.pantryCardUnits[itemName] || 'g';
      const currentVal = parseFloat(pantryStock[itemName]) || 0;

      const oldBase = (resolvePantryCommercialUnit(currentVal, oldUnitId) || { val: currentVal }).val;
      const dummyOne = (resolvePantryCommercialUnit(1, newUnitId) || { val: 1 }).val || 1;

      let convertedVal = oldBase > 0 ? (oldBase / dummyOne) : currentVal;
      convertedVal = Math.round(convertedVal * 100) / 100;

      window.pantryCardUnits[itemName] = newUnitId;
      pantryStock[itemName] = convertedVal;

      if (inputElem) {
        inputElem.value = convertedVal;
      }

      updatePantryStock(itemName, convertedVal, newUnitId);
      initSetupPanel();
    }

    function showClinicalConfirmModal(options) {
      const {
        title = 'Confirmar Acción Clínica',
        message = '¿Deseas proceder con esta acción?',
        icon = '🗑️',
        confirmText = 'Eliminar Insumo',
        cancelText = 'Cancelar',
        onConfirm
      } = options || {};

      let modalOverlay = document.getElementById('clinical-confirm-modal');
      if (!modalOverlay) {
        modalOverlay = document.createElement('div');
        modalOverlay.id = 'clinical-confirm-modal';
        document.body.appendChild(modalOverlay);
      }

      modalOverlay.style.cssText = 'position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px); z-index: 99999; display: flex; align-items: center; justify-content: center; padding: 1rem; transition: opacity 0.2s ease-in-out;';

      modalOverlay.innerHTML = `
        <div style="background: var(--surface-card, #ffffff); border: 1px solid var(--border-clinical, #e2e8f0); box-shadow: var(--shadow-clinical-lg, 0 10px 25px -5px rgba(15, 23, 42, 0.2)); border-radius: 1rem; max-width: 26rem; width: 100%; padding: 1.5rem; text-align: left;" class="dark:bg-slate-900 dark:border-slate-800">
          <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <div style="width: 2.75rem; height: 2.75rem; border-radius: 0.75rem; background: rgba(183, 14, 12, 0.1); color: #B70E0C; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; flex-shrink: 0;">
              ${icon}
            </div>
            <div>
              <h3 style="margin: 0; font-weight: 800; font-size: 1.05rem; color: var(--text-main, #0f172a);" class="dark:text-slate-100">${title}</h3>
              <p style="margin: 0.2rem 0 0 0; font-size: 0.75rem; font-weight: 700; color: var(--color-corporate, #1C75BC);">Gobernanza Clínico-Nutricional T.I.L.O.®</p>
            </div>
          </div>
          
          <div style="margin: 0 0 1.25rem 0; font-size: 0.88rem; color: var(--text-muted, #475569); line-height: 1.5;" class="dark:text-slate-300">
            ${message}
          </div>
          
          <div style="display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem; margin-top: 1.25rem;">
            <button type="button" id="clinical-modal-cancel-btn" style="min-height: 44px; min-width: 100px; padding: 0.6rem 1.25rem; border-radius: 0.75rem; border: 1px solid var(--border-clinical, #cbd5e1); background: transparent; color: var(--text-main, #334155); font-weight: 700; font-size: 0.88rem; cursor: pointer; transition: all 0.2s ease;" onmouseover="this.style.background='var(--bg-clinical)'" onmouseout="this.style.background='transparent'">
              ${cancelText}
            </button>
            <button type="button" id="clinical-modal-confirm-btn" style="min-height: 44px; min-width: 130px; padding: 0.6rem 1.25rem; border-radius: 0.75rem; border: none; background: #B70E0C; color: #ffffff; font-weight: 700; font-size: 0.88rem; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(183, 14, 12, 0.25);" onmouseover="this.style.background='#960b0a'" onmouseout="this.style.background='#B70E0C'">
              ${confirmText}
            </button>
          </div>
        </div>
      `;

      modalOverlay.style.display = 'flex';

      const cancelBtn = document.getElementById('clinical-modal-cancel-btn');
      const confirmBtn = document.getElementById('clinical-modal-confirm-btn');

      const closeModal = () => {
        modalOverlay.style.display = 'none';
      };

      cancelBtn.onclick = () => closeModal();
      
      confirmBtn.onclick = () => {
        closeModal();
        if (typeof onConfirm === 'function') {
          onConfirm();
        }
      };
    }

    function deleteHarvestItem(itemName) {
      showClinicalConfirmModal({
        title: 'Eliminar Insumo de Cosecha',
        message: `¿Estás seguro de que deseas eliminar definitivamente el insumo <strong>"${itemName}"</strong> de la Cosecha Activa?`,
        icon: '🗑️',
        confirmText: 'Sí, Eliminar Insumo',
        cancelText: 'Cancelar',
        onConfirm: () => {
          const slug = normalizeToCanonicalSlug(itemName);
          if (!deletedFarmItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === itemName.toLowerCase())) {
            deletedFarmItems.push(itemName);
          }
          customFarmItems = customFarmItems.filter(n => normalizeToCanonicalSlug(n) !== slug && n.toLowerCase() !== itemName.toLowerCase());
          selectedHarvest = selectedHarvest.filter(h => {
            const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
            return normalizeToCanonicalSlug(hStr) !== slug && hStr.toLowerCase() !== itemName.toLowerCase();
          });
          rawShopBase = rawShopBase.filter(i => normalizeToCanonicalSlug(i.item_name) !== slug && i.item_name.toLowerCase() !== itemName.toLowerCase());
          
          saveAppState();
          initSetupPanel();
          if (typeof render3DShoppingList === 'function') {
            render3DShoppingList();
          }
          if (typeof showToast === 'function') {
            showToast(`🗑️ Insumo '${itemName}' eliminado definitivamente de la Cosecha.`, 'danger');
          }
        }
      });
    }

    function deletePantryItem(itemName) {
      showClinicalConfirmModal({
        title: 'Eliminar Insumo del Inventario',
        message: `¿Estás seguro de que deseas eliminar definitivamente el insumo <strong>"${itemName}"</strong> del Inventario/Alacena?`,
        icon: '🗑️',
        confirmText: 'Sí, Eliminar Insumo',
        cancelText: 'Cancelar',
        onConfirm: () => {
          const slug = normalizeToCanonicalSlug(itemName);
          if (!deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === itemName.toLowerCase())) {
            deletedPantryItems.push(itemName);
          }
          rawShopBase = rawShopBase.filter(i => normalizeToCanonicalSlug(i.item_name) !== slug && i.item_name.toLowerCase() !== itemName.toLowerCase());
          
          Object.keys(pantryStock).forEach(k => {
            if (normalizeToCanonicalSlug(k) === slug || k.toLowerCase() === itemName.toLowerCase()) {
              delete pantryStock[k];
            }
          });

          if (typeof window.PANTRY_STOCK_INVENTORY === 'object' && window.PANTRY_STOCK_INVENTORY) {
            Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(k => {
              if (normalizeToCanonicalSlug(k) === slug || k.toLowerCase() === itemName.toLowerCase()) {
                delete window.PANTRY_STOCK_INVENTORY[k];
              }
            });
          }

          saveAppState();
          initSetupPanel();
          if (typeof render3DShoppingList === 'function') {
            render3DShoppingList();
          }
          if (typeof showToast === 'function') {
            showToast(`🗑️ Insumo '${itemName}' eliminado definitivamente del Inventario.`, 'danger');
          }
        }
      });
    }

    function saveAndUnlockApp() {
      activeWeek = document.getElementById('setup-week').value;
      activeDiners = parseInt(document.getElementById('setup-diners').value) || 6;
      
      saveAppState();

      document.getElementById('setup-overlay').style.display = 'none';
      document.getElementById('main-app-content').style.display = 'block';

      document.getElementById('active-diners-label').innerText = activeDiners;
      const headerWeekSelect = document.getElementById('header-week-select');
      if (headerWeekSelect) headerWeekSelect.value = activeWeek;
      document.getElementById('header-week-subtitle').innerText = `${activeWeek} | Ecosistema T.I.L.O.®`;

      renderDateBar();
      renderDay(selectedIdx);
      const curPlan1 = getPlanForWeek(activeWeek);
      if (typeof renderRecipes === 'function' && curPlan1 && curPlan1.days && curPlan1.days[selectedIdx]) {
        renderRecipes(curPlan1.days[selectedIdx], getMealDiners(selectedIdx, 'Desayuno'));
      }
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
      if (typeof showToast === 'function') {
        showToast("🏛️ Arquitectura Semanal Compilada y Sincronizada.");
      }
    }

    function onHeaderWeekChange(newWeek) {
      const targetPlan = getPlanForWeek(newWeek);
      if (!targetPlan) return;
      activeWeek = newWeek;

      const setupWeekSelect = document.getElementById('setup-week');
      if (setupWeekSelect) setupWeekSelect.value = newWeek;

      const headerWeekSelect = document.getElementById('header-week-select');
      if (headerWeekSelect) headerWeekSelect.value = newWeek;

      const headerSubtitle = document.getElementById('header-week-subtitle');
      if (headerSubtitle) headerSubtitle.innerText = `${activeWeek} | Ecosistema T.I.L.O.®`;

      const btnNextWeekText = document.getElementById('btn-next-week-text');
      const btnNextWeek = document.getElementById('btn-next-week');
      if (btnNextWeekText) {
        if (newWeek.startsWith('Semana 42')) {
          btnNextWeekText.innerText = "📋 Semana 42 SSOT (Activa)";
          if (btnNextWeek) btnNextWeek.title = "Semana 42 SSOT Activa en el Atelier";
        } else {
          btnNextWeekText.innerText = "⚡ Generar Semana 42 SSOT";
          if (btnNextWeek) btnNextWeek.title = "Planificar y Cargar Semana 42 SSOT";
        }
      }

      if (typeof selectedIdx !== 'number' || isNaN(selectedIdx) || selectedIdx < 0 || (targetPlan.days && selectedIdx >= targetPlan.days.length)) {
        selectedIdx = 0;
      }

      saveAppState();

      renderDateBar();
      renderDay(selectedIdx);

      if (typeof renderRecipes === 'function' && targetPlan && targetPlan.days && targetPlan.days[selectedIdx]) {
        renderRecipes(targetPlan.days[selectedIdx], getMealDiners(selectedIdx, 'Desayuno'));
      }
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }

      if (typeof showToast === 'function') {
        showToast("📅 Semana cambiada a: " + activeWeek.split(' (')[0]);
      }
    }

    function reopenSetupPanel() {
      initSetupPanel();
      const setupOverlay = document.getElementById('setup-overlay');
      const editDetails = document.getElementById('edit-inventory-details');
      const mainContent = document.getElementById('main-app-content');

      if (setupOverlay) setupOverlay.style.display = 'block';
      if (editDetails) editDetails.style.display = 'block';
      if (mainContent) mainContent.style.display = 'none';
    }

    function getPlanForWeek(weekKey) {
      if (typeof datasets === 'undefined' || !datasets) return null;
      if (datasets[weekKey]) return datasets[weekKey];
      for (const k in datasets) {
        if (k.startsWith(weekKey) || (weekKey && weekKey.startsWith(k.split(' (')[0]))) {
          return datasets[k];
        }
      }
      return datasets["Semana 35 (23 al 29 de Agosto de 2026)"] || Object.values(datasets)[0] || null;
    }

    function isCalendarToday(dayObj, planObj) {
      if (!dayObj) return false;
      const now = new Date();
      const currentYear = now.getFullYear();
      const currentMonth = now.getMonth(); // 0-index (Sept=8, Oct=9)
      const currentDay = now.getDate();

      // 1. Coincidencia directa por iso_date estricta
      if (dayObj.iso_date && /^\\d{4}-\\d{2}-\\d{2}$/.test(dayObj.iso_date)) {
        const [y, m, d] = dayObj.iso_date.split('-').map(Number);
        return y === currentYear && (m - 1) === currentMonth && d === currentDay;
      }

      // 2. Extraer día numérico estricto (delimitado por límite de palabra, NUNCA .includes())
      let targetDay = null;
      if (dayObj.day_num !== undefined && dayObj.day_num !== null) {
        targetDay = parseInt(dayObj.day_num, 10);
      } else if (dayObj.date_str) {
        const matchDay = dayObj.date_str.match(/\\b0?(\\d{1,2})\\b/);
        if (matchDay) targetDay = parseInt(matchDay[1], 10);
      }
      if (!targetDay || isNaN(targetDay) || targetDay !== currentDay) {
        return false;
      }

      // 3. Extraer y validar mes en español
      const SPANISH_MONTH_MAP = {
        'ene': 0, 'enero': 0,
        'feb': 1, 'febrero': 1,
        'mar': 2, 'marzo': 2,
        'abr': 3, 'abril': 3,
        'may': 4, 'mayo': 4,
        'jun': 5, 'junio': 5,
        'jul': 6, 'julio': 6,
        'ago': 7, 'agosto': 7,
        'sep': 8, 'sept': 8, 'septiembre': 8,
        'oct': 9, 'octubre': 9,
        'nov': 10, 'noviembre': 10,
        'dic': 11, 'diciembre': 11
      };

      const cleanStr = (s) => (s || '').normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
      const dayClean = cleanStr(dayObj.date_str || '');
      let targetMonth = null;

      for (const [mName, mIdx] of Object.entries(SPANISH_MONTH_MAP)) {
        const reg = new RegExp(`\\b${mName}\\b`, 'i');
        if (reg.test(dayClean)) {
          targetMonth = mIdx;
          break;
        }
      }

      if (targetMonth === null) {
        const planClean = cleanStr(`${planObj?.week_label || ''} ${planObj?.date_range || ''}`);
        for (const [mName, mIdx] of Object.entries(SPANISH_MONTH_MAP)) {
          const reg = new RegExp(`\\b${mName}\\b`, 'i');
          if (reg.test(planClean)) {
            targetMonth = mIdx;
            break;
          }
        }
      }

      if (targetMonth === null || targetMonth !== currentMonth) {
        return false;
      }

      // 4. Extraer y validar año
      let targetYear = null;
      const combinedClean = cleanStr(`${dayObj.date_str || ''} ${planObj?.week_label || ''} ${planObj?.date_range || ''}`);
      const yearMatch = combinedClean.match(/\\b(202\\d)\\b/);
      if (yearMatch) {
        targetYear = parseInt(yearMatch[1], 10);
      }
      if (targetYear !== null && targetYear !== currentYear) {
        return false;
      }

      return true;
    }

    function renderDateBar() {
      try {
        const plan = getPlanForWeek(activeWeek);
        const bar = document.getElementById('date-bar');
        if (!bar) return;
        bar.innerHTML = '';
        bar.className = 'flex items-center gap-2 overflow-x-auto pb-3 mb-6 w-full';

        if (!plan || !plan.days) return;

        plan.days.forEach((day, idx) => {
          const btn = document.createElement('button');
          const isActive = idx === selectedIdx;
          const isToday = isCalendarToday(day, plan);
          
          btn.type = 'button';
          btn.className = `min-h-[48px] px-4 py-2.5 rounded-xl border text-xs font-brand-body flex items-center gap-2 transition-all cursor-pointer whitespace-nowrap ${
            isActive 
              ? 'bg-[#3AAA35] text-white shadow-md border-[#3AAA35] font-bold' 
              : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700'
          }`;
          
          const todayTag = isToday ? '<span class="text-[10px] uppercase font-bold text-[#FFCC00] bg-slate-900 px-1.5 py-0.5 rounded ml-1">HOY</span>' : '';
          
          let dayNumText = (day.day_num || (day.date_str ? day.date_str.split(' ')[0] : (idx + 1))).toString().trim().replace(/[\\s\\-_]+$/, '');
          let dayShortText = (day.day || '').substring(0, 3).toUpperCase().trim().replace(/[\\s\\-_]+$/, '');

          btn.innerHTML = `<span class="font-bold text-sm font-brand-title">${dayNumText}</span> <span class="font-semibold">${dayShortText}</span>${todayTag ? ' ' + todayTag : ''}`;
          
          btn.onclick = () => {
            selectedIdx = idx;
            renderDateBar();
            renderDay(idx);
          };
          bar.appendChild(btn);
        });
      } catch (e) {
        console.error("Error en renderDateBar:", e);
      }
    }

    let currentTab = 'menu';

    function switchTab(tabId, btn) {
      try {
        const map = {
          'design': 'v-menu',
          'menu': 'v-menu',
          'recipes': 'v-prep',
          'prep': 'v-prep',
          'supply': 'v-shop',
          'shop': 'v-shop',
          'metrics': 'v-nutri',
          'nutri': 'v-nutri'
        };
        const targetId = map[tabId] || (tabId && tabId.startsWith('v-') ? tabId : 'v-menu');
        currentTab = targetId.replace('v-', '');
        try {
          if (typeof sessionStorage !== 'undefined') {
            sessionStorage.setItem('nutriketo_active_tab', tabId);
          }
        } catch(e) {}

        document.querySelectorAll('.v-panel').forEach(el => el.style.display = 'none');
        const target = document.getElementById(targetId);
        if (target) target.style.display = 'block';

        document.querySelectorAll('.tab-btn').forEach(b => {
          b.classList.remove('bg-[#1C75BC]', 'text-white', 'border-[#1C75BC]');
          b.classList.add('bg-slate-100', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700');
        });

        const activeBtn = btn || document.getElementById(`tab-btn-${tabId}`);
        if (activeBtn) {
          activeBtn.classList.remove('bg-slate-100', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700');
          activeBtn.classList.add('bg-[#1C75BC]', 'text-white', 'border-[#1C75BC]');
        }

        if (targetId === 'v-shop' && typeof render3DShoppingList === 'function') {
          render3DShoppingList();
        }

        if (typeof updateExportButtonUI === 'function') updateExportButtonUI();
      } catch (e) {
        console.error("Error en switchTab:", e);
      }
    }

    function switchView(vId, btn) {
      switchTab(vId, btn);
    }

/**
 * Atelier T.I.L.O.® — Componente de Recetas 100% Pasivo SSOT (V15.22.1)
 * Renderizado Pasivo de Datos Estructurados sin Parsers Regex ni Plantillas Estáticas.
 * Escalamiento Unitario Estricto por Persona: (base_qty_per_person * activeDiners)
 */

function sanitizeDishTitle(title) {
  if (!title) return "";
  return title
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\\(.*?\\)/g, "")
    .trim();
}
function parseQuantityInBaseUnit(qty, unitRaw) {
  const num = parseFloat(qty) || 0;
  const unitStr = (unitRaw || "").toLowerCase().trim();

  // 0. Factores de Empaque Comercial Canónicos (Directiva SSOT)
  const commercialResolved = resolvePantryCommercialUnit(num, unitStr);
  if (commercialResolved) {
    return commercialResolved;
  }

  // 1. Empaques compuestos con especificación de peso/volumen (ej. "paquete (3.2 kg)", "frasco (1 kg)", "frasco (500 g)")
  const pkgMatch = unitStr.match(/(\\d+(?:\\.\\d+)?)\\s*(kg|kilo|kilos|g|gramos?|l|lt|litros?|ml)/i);
  if (pkgMatch && (unitStr.includes("paquete") || unitStr.includes("empaque") || unitStr.includes("frasco") || unitStr.includes("lata") || unitStr.includes("botella"))) {
    const pkgSize = parseFloat(pkgMatch[1]);
    const pkgUnit = pkgMatch[2].toLowerCase();
    let baseMultiplier = pkgSize;
    if (pkgUnit.includes("kg") || pkgUnit.includes("kilo") || pkgUnit.includes("l") || pkgUnit.includes("lt")) {
      baseMultiplier = pkgSize * 1000;
    }
    const isVol = pkgUnit.includes("l") || pkgUnit.includes("ml");
    return { val: num * baseMultiplier, type: isVol ? "vol" : "mass", baseUnit: isVol ? "ml" : "g" };
  }

  // 2. Casilleros y docenas de huevos
  if (unitStr.includes("casillero")) {
    return { val: num * 30, type: "count", baseUnit: "piezas" };
  }
  if (unitStr.includes("docena")) {
    return { val: num * 12, type: "count", baseUnit: "piezas" };
  }

  // 3. Masa en Kilogramos
  if (unitStr.includes("kg") || unitStr.includes("kilo")) {
    const val = num < 50 ? num * 1000 : num;
    return { val: val, type: "mass", baseUnit: "g" };
  }

  // 4. Volumen en Mililitros
  if (unitStr.includes("ml") || unitStr.includes("mililitro")) {
    return { val: num, type: "vol", baseUnit: "ml" };
  }

  // 5. Masa en Gramos
  if (unitStr.includes("g") || unitStr.includes("gramo")) {
    return { val: num, type: "mass", baseUnit: "g" };
  }

  // 6. Volumen en Litros
  if (unitStr === "l" || unitStr === "lt" || unitStr === "lts" || unitStr.includes("litro") || /\bl\b|\blt\b|\blts\b/i.test(unitStr)) {
    const val = num < 50 ? num * 1000 : num;
    return { val: val, type: "vol", baseUnit: "ml" };
  }

  return { val: num, type: "count", baseUnit: unitStr || "piezas" };
}
function getYieldFactor(category, slug) {
  if (category && category.includes("Carnes")) return 1.15;
  if (category && category.includes("Verduras")) return 1.10;
  return 1.00;
}
function formatBaseQuantity(val, type, origUnit) {
  const roundedVal = Math.round(val * 10) / 10;
  if (type === "mass") {
    if (val >= 1000) return `${(val / 1000).toFixed(1)} kg`;
    return `${roundedVal} g`;
  }
  if (type === "vol") {
    if (val >= 1000) return `${(val / 1000).toFixed(1)} L`;
    return `${roundedVal} ml`;
  }
  return `${Math.ceil(val)} ${origUnit || 'piezas'}`;
}
function getSmartItemCategory(itemName, explicitCategory) {
      if (explicitCategory && typeof explicitCategory === 'string' && explicitCategory.trim()) {
        const ec = explicitCategory.trim();
        if (ec.includes("Cuarentena") || ec.includes("🛑") || ec.includes("No Sugeridos") || ec.includes("prohibited")) return "🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)";
        if (ec.includes("Verduras") || ec.includes("Hortalizas") || ec.includes("Frescos")) return "🥬 Verduras, Hortalizas y Frescos";
        if (ec.includes("Carnes") || ec.includes("Pescados") || ec.includes("Proteínas")) return "🥩 Carnes, Pescados y Proteínas";
        if (ec.includes("Frutas")) return "🍓 Frutas de Bajo Índice Glucémico";
        if (ec.includes("Quesos") || (ec.includes("Lácteos") && !ec.includes("Grasas"))) return "🧀 Lácteos y Quesos (Sin Gluten — Keto)";
        if (ec.includes("Grasas") || ec.includes("Aceites") || ec.includes("Semillas")) return "🥑 Grasas, Aceites y Semillas";
        if (ec.includes("Suplementación") || ec.includes("Biotecnología") || ec.includes("Bases Hidrocoloides")) return "💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA";
        if (ec.includes("Cítricos") || ec.includes("Ácidos")) return "🍋 Cítricos y Ácidos Naturales";
        if (ec.includes("Especias") || ec.includes("Hierbas") || ec.includes("Aromáticos") || ec.includes("Condimentos") || ec.includes("Infusiones")) return "🌶️ Chiles, Condimentos e Infusiones";
      }

      const name = (itemName || '').toLowerCase().trim();

      // 0.0 Inmunidad Taxonómica Estricta: Aceites vegetales, VEVO, ajonjolí, mantequilla y ghee son grasas puras (NUNCA lácteos ni quesos)
      if (/aceite|vevo|ajonjolí|ajonjoli|mantequilla|ghee/i.test(name)) {
        return '🥑 Grasas, Aceites y Semillas';
      }

      // 0.0 Prioridad Taxonómica Estricta: Leche de coco -> Grasas, Aceites y Semillas (NUNCA Cuarentena)
      if (/leche de coco/i.test(name)) {
        return '🥑 Grasas, Aceites y Semillas';
      }

      // 0.05 Prioridad Taxonómica Estricta: Hongos y Setas (NUNCA Grasas, NUNCA Carnes)
      if (/portobello|champiñon|champiñones|champinon|champinones|setas|hongos/i.test(name)) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      // 0.1 Prioridad Taxonómica Estricta: Cebollas (Verduras, Hortalizas y Frescos — NUNCA frutas)
      if (/cebolla|cebollas|cebollín|cebollin/i.test(name)) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      // 0.15 Prioridad Taxonómica Estricta: Grasas, Aceites y Semillas (Almendras, nueces, chía, etc. — NUNCA carnes aun si dicen fileteadas)
      if (/almendra|almendras|nuez|nueces|chía|chia|girasol|macadamia|macadamias|semilla|semillas|linaza|piñón|piñones|pepita|pepitas|ajonjolí|ajonjoli|aguacate|aceituna/i.test(name)) {
        return '🥑 Grasas, Aceites y Semillas';
      }

      // 0.2 Prioridad Taxonómica Estricta: Carnes / Proteínas (Arrachera, Sirloin, Pechuga, Pescado, Sardinas, etc.)
      if (/arrachera|corte|cortes|ribeye|sirloin|\bres\b|pollo|pollos|pechuga|pechugas|pavo|pavos|tocino|jamón|jamon|pescado|pescados|mojarra|tilapia|salmón|salmon|atún|atun|sardina|sardinas|huevo|huevos|clara|claras|lomo|lomos|medallón|medallon|medallones|huachinango|robalo|róbalo|filete|filetes|machaca|tuétano|tuetano|costilla/i.test(name)) {
        return '🥩 Carnes, Pescados y Proteínas';
      }

      // 0.3 Prioridad Taxonómica Estricta: Frutas de Bajo Índice Glucémico (Moras, Frambuesas, Arándanos, Granada, Pitaya, Zarzamora, Fresas)
      if (!name.includes('cebolla') && /mora|moras|frambuesa|frambuesas|fresa|fresas|arándano|arandano|arándanos|arandanos|granada|granadas|pitahaya|pitahayas|pitaya|pitayas|arilos|zarzamora|zarzamoras/i.test(name)) {
        return '🍓 Frutas de Bajo Índice Glucémico';
      }

      // 0.4 Prioridad Taxonómica Estricta: Insumos No Sugeridos / Cuarentena
      if ((explicitCategory && (explicitCategory.includes('cuarentena') || explicitCategory.includes('prohibited') || explicitCategory.includes('Cuarentena') || explicitCategory.includes('🛑'))) ||
          /durazno|duraznos|miel|harina de trigo|harina refinada|aceite vegetal mixto|azúcar|azucar|quinoa|cereza|cerezas|leche de vaca|higo|higos|papa|papas|lenteja|lentejas|garbanzo|garbanzos|frijol|frijoles|arroz/i.test(name)) {
        return '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)';
      }

      // 0.5 Prioridad Taxonómica Estricta: Hongos y Setas
      if (/portobello|champiñon|champiñones|champinon|champinones|setas|hongos/i.test(name)) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      // 0.6 Prioridad Taxonómica Estricta: Jitomate / Tomate
      if (/jitomate|tomate bola|\btomate\b/i.test(name) && !name.includes('tomillo')) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      // 1. Suplementación Celular — Biotecnología
      if (/33plus|34plus|sinergix|suplemento|suplementos|vitamina|vitaminas|colágeno|colageno|electrolitos|fórmula nootrópica|formula nootropica|fórmula reparadora|formula reparadora/i.test(name)) {
        return '💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA';
      }

      // 3. Grasas, Aceites y Semillas
      if (/aceite|mct|leche de coco|mantequilla|ghee|aguacate|aguacates|aceituna|aceitunas|nuez|nueces|almendra|almendras|chía|chia|girasol|macadamia|macadamias|semilla|semillas|linaza|piñón|piñones|pepita|pepitas|ajonjolí|ajonjoli|mayonesa/i.test(name)) {
        return '🥑 Grasas, Aceites y Semillas';
      }

      // 4. Lácteos y Quesos
      if (/queso|quesos|leche|crema|gouda|panela|parmesano|manchego|mascarpone|mozzarella|yoghurt|yogurt/i.test(name)) {
        return '🧀 Lácteos y Quesos (Sin Gluten — Keto)';
      }

      // 5. Cítricos y Ácidos Naturales
      if (/limón|limon|vinagre|balsámico|balsamico/i.test(name)) {
        return '🍋 Cítricos y Ácidos Naturales';
      }

      // 6. Chiles, Condimentos e Infusiones
      if (/\bsal\b|\bsal de\b|\bsal mineral\b|eneldo|romero|tomillo|comino|orégano|oregano|canela|menta|toronjil|manzanilla|jamaica|azahar|especias|condimento|condimentos|chile|chiles|jalapeño|jalapeno|pimienta|epazote|albahaca|mostaza|alcaparra|alcaparras|jengibre|agua|infusión|infusion|\bté\b|\bte\b|base líquida|base liquida|aderezo|bbq|café|cafe|cobertura de chocolate|salsa|tamari|soya|achiote/i.test(name)) {
        return '🌶️ Chiles, Condimentos e Infusiones';
      }

      // 7. Verduras, Hortalizas y Frescos
      if (/apio|arúgula|arugula|brócoli|brocoli|calabacita|calabacitas|chayote|chayotes|cilantro|coliflor|ejote|ejotes|espárrago|esparrago|esparragos|espárragos|espinaca|espinacas|flor de calabaza|hinojo|jitomate|jitomates|nopal|nopales|pepino|pepinos|pimiento|pimientos|tomate|zucchini|lechuga|col|cebolla|ajo|dientes de ajo|champiñones|champinon|champinones|portobello|setas/i.test(name)) {
        return '🥬 Verduras, Hortalizas y Frescos';
      }

      return '🌶️ Chiles, Condimentos e Infusiones';
    }

    function loadAppState() {
      try {
        const storedVersion = localStorage.getItem('nutriketo_app_version');
        if (storedVersion !== CURRENT_APP_VERSION) {
          console.warn('Detectada versión anterior de localStorage. Migrando a V42 106 insumos canónicos...');
          const oldDataStr = localStorage.getItem('nutriketo_app_state_v40_2_ssot') || localStorage.getItem(LOCAL_STORAGE_KEY);
          let oldState = null;
          try { if (oldDataStr) oldState = JSON.parse(oldDataStr); } catch(e){}
          const legacyKeys = [
            'nutriketo_app_state_v40_2_ssot',
            'nutriketo_app_state_v38_canonical',
            'nutriketo_app_state_v34_granular',
            'nutriketo_app_state_v33',
            'nutriketo_app_state',
            'nutriketo_app_state_v36_6_ssot'
          ];
          for (const lKey of legacyKeys) {
            localStorage.removeItem(lKey);
          }
          localStorage.setItem('nutriketo_app_version', CURRENT_APP_VERSION);
          if (oldState) {
            if (oldState.activeWeek && datasets[oldState.activeWeek]) activeWeek = oldState.activeWeek;
            if (oldState.activeDiners) activeDiners = parseInt(oldState.activeDiners) || 6;
            if (Array.isArray(oldState.selectedHarvest)) selectedHarvest = oldState.selectedHarvest;
            if (Array.isArray(oldState.customFarmItems)) customFarmItems = oldState.customFarmItems;
            if (Array.isArray(oldState.deletedFarmItems)) deletedFarmItems = oldState.deletedFarmItems;
            if (oldState.mealDinersState) mealDinersState = oldState.mealDinersState;
            if (oldState.dispatchedMeals) dispatchedMeals = oldState.dispatchedMeals;
            if (Array.isArray(oldState.mealFeedbackLedger)) mealFeedbackLedger = oldState.mealFeedbackLedger;
          }
          saveAppState();
          return true;
        }

        let saved = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (!saved) {
          const legacyKeys = ['nutriketo_app_state_v34_granular', 'nutriketo_app_state_v33', 'nutriketo_app_state'];
          for (const lKey of legacyKeys) {
            const oldData = localStorage.getItem(lKey);
            if (oldData) {
              saved = oldData;
              localStorage.removeItem(lKey);
              break;
            }
          }
        }

        if (saved) {
          const state = JSON.parse(saved);
          if (state.activeWeek && datasets[state.activeWeek]) activeWeek = state.activeWeek;
          if (state.activeDiners) activeDiners = parseInt(state.activeDiners) || 6;

          if (Array.isArray(state.deletedFarmItems)) {
            deletedFarmItems = state.deletedFarmItems.filter(d => !areInsumosEquivalent(d, 'limon'));
          } else {
            deletedFarmItems = [];
          }

          if (Array.isArray(state.deletedPantryItems)) {
            deletedPantryItems = state.deletedPantryItems;
          } else {
            deletedPantryItems = [];
          }

          if (Array.isArray(state.customFarmItems)) {
            customFarmItems = state.customFarmItems.filter(f => {
              const fStr = typeof f === 'string' ? f : (f.item_name || f.name || '');
              return !/miel|durazno|higo/i.test(fStr);
            }).map(f => {
              const fStr = typeof f === 'string' ? f : (f.item_name || f.name || '');
              if (/nuex.*pecan|nuez.*pecan/i.test(fStr)) return "Nuez pecana fresca de la granja";
              return f;
            });
          }

          if (Array.isArray(state.selectedHarvest)) {
            selectedHarvest = state.selectedHarvest.filter(h => {
              const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
              return !/miel|durazno|higo/i.test(hStr);
            }).map(h => {
              const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
              if (/nuex.*pecan|nuez.*pecan/i.test(hStr)) return "Nuez pecana fresca de la granja";
              return h;
            });
            if (!selectedHarvest.some(h => areInsumosEquivalent(typeof h === 'string' ? h : (h.item_name || h.name || ''), 'limon'))) {
              selectedHarvest.push("Limones agrios frescos de la granja");
            }
            if (!selectedHarvest.some(h => areInsumosEquivalent(typeof h === 'string' ? h : (h.item_name || h.name || ''), 'nuez pecana')) && !deletedFarmItems.some(d => areInsumosEquivalent(d, 'nuez pecana'))) {
              selectedHarvest.push("Nuez pecana fresca de la granja");
            }
          } else {
            selectedHarvest = ["Espinacas frescas", "Calabacitas verdes tiernas", "Brócoli fresco", "Espárragos verdes", "Nopales tiernos", "Ejotes frescos", "Cilantro fresco", "Arúgula fresca", "Coliflor fresca", "Limones agrios frescos de la granja", "Nuez pecana fresca de la granja"];
          }

          if (state.pantryStock && typeof state.pantryStock === 'object') {
            pantryStock = {};
            Object.keys(state.pantryStock).forEach(itemName => {
              if (/miel|durazno|higo/i.test(itemName)) return;
              pantryStock[itemName] = state.pantryStock[itemName];
            });
          }

          if (state.pantryCardUnits && typeof state.pantryCardUnits === 'object') {
            window.pantryCardUnits = state.pantryCardUnits;
          } else {
            window.pantryCardUnits = {};
          }
          if (window.pantryCardUnits) {
            Object.keys(window.pantryCardUnits).forEach(k => {
              if (/aguacate/i.test(k) && (window.pantryCardUnits[k] === 'litros' || window.pantryCardUnits[k] === 'l' || window.pantryCardUnits[k] === 'ml' || window.pantryCardUnits[k] === 'botellas (355 ml)')) {
                window.pantryCardUnits[k] = 'piezas';
              }
            });
          }

          if (state.pantryStockInventory && typeof state.pantryStockInventory === 'object') {
            delete state.pantryStockInventory['miel-pura'];
            delete state.pantryStockInventory['duraznos-frescos'];
            delete state.pantryStockInventory['higos-frescos'];

            // Comprobante Sam's Club 03/10/2026 reemplazado por inventario físico canónico de 106 insumos

            window.PANTRY_STOCK_INVENTORY = Object.assign(window.PANTRY_STOCK_INVENTORY || {}, state.pantryStockInventory);
          }

          if (state.checkedRows) checkedRows = state.checkedRows;
          if (state.mealDinersState) mealDinersState = state.mealDinersState;
          if (state.dispatchedMeals && typeof state.dispatchedMeals === 'object') {
            dispatchedMeals = state.dispatchedMeals;
          } else {
            dispatchedMeals = {};
          }
          window.DISPATCHED_MEALS = dispatchedMeals;
          if (Array.isArray(state.mealFeedbackLedger)) {
            mealFeedbackLedger = state.mealFeedbackLedger;
          } else {
            mealFeedbackLedger = [];
          }
          if (state.customDishesState) {
            customDishesState = state.customDishesState;
            delete customDishesState['Semana 41 (04 al 10 de Octubre de 2026)_day_1_Comida'];
            delete customDishesState['Semana 41 (04 al 10 de Octubre de 2026)_day_3_Comida'];
            delete customDishesState['Semana 41_day_1_Comida'];
            delete customDishesState['Semana 41_day_3_Comida'];
          }
          if (window.MEAL_DISH_OVERRIDES) {
            delete window.MEAL_DISH_OVERRIDES['Semana 41 (04 al 10 de Octubre de 2026)_day_1_Comida'];
            delete window.MEAL_DISH_OVERRIDES['Semana 41 (04 al 10 de Octubre de 2026)_day_3_Comida'];
            delete window.MEAL_DISH_OVERRIDES['Semana 41_day_1_Comida'];
            delete window.MEAL_DISH_OVERRIDES['Semana 41_day_3_Comida'];
          }
          if (state.selectedIdx !== undefined && !isNaN(parseInt(state.selectedIdx))) {
            selectedIdx = parseInt(state.selectedIdx);
          } else {
            selectedIdx = currentDayNum;
          }

          if (Array.isArray(state.customShopItems)) {
            state.customShopItems.forEach(cItem => {
              if (!cItem || !cItem.item_name || /miel|durazno/i.test(cItem.item_name)) return;
              const smartCat = getSmartItemCategory(cItem.item_name, cItem.category);
              const cSlug = normalizeToCanonicalSlug(cItem.item_name);
              const existing = rawShopBase.find(r => normalizeToCanonicalSlug(r.item_name) === cSlug);
              if (existing) {
                existing.category = smartCat;
              } else {
                cItem.category = smartCat;
                rawShopBase.push(cItem);
              }
            });
          }

          // Sanitizar y deduplicar rawShopBase por slug canónico
          const cleanedShopBase = [];
          const seenShopSlugs = new Set();

          rawShopBase.forEach(item => {
            if (!item || !item.item_name) return;
            const cleanName = item.item_name.replace(/\\s*\\/\\s*/g, ' \u2014 ').replace(/\\//g, ' \u2014 ').trim();
            if (!cleanName) return;
            const slug = normalizeToCanonicalSlug(cleanName);
            if (deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === cleanName.toLowerCase())) return;
            if (deletedFarmItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === cleanName.toLowerCase())) return;

            const smartCat = getSmartItemCategory(cleanName, item.category);

            if (!seenShopSlugs.has(slug)) {
              seenShopSlugs.add(slug);
              cleanedShopBase.push({
                ...item,
                item_name: cleanName,
                category: smartCat
              });
            }
          });
          rawShopBase = cleanedShopBase;

          saveAppState();
          return true;
        }
      } catch(e) {
        console.error("Error al cargar localStorage:", e);
      }
      return false;
    }

    function saveAppState() {
      try {
        const customShopItems = rawShopBase.filter(i => i.id > 100);
        const state = {
          activeWeek,
          activeDiners,
          selectedHarvest,
          customFarmItems,
          deletedFarmItems,
          deletedPantryItems,
          pantryStock,
          pantryCardUnits: window.pantryCardUnits || {},
          pantryStockInventory: window.PANTRY_STOCK_INVENTORY || {},
          samsReceiptProcessed_20261003: true,
          checkedRows,
          customShopItems,
          selectedIdx,
          mealDinersState,
          customDishesState,
          dispatchedMeals,
          mealFeedbackLedger: window.MEAL_FEEDBACK_LEDGER || mealFeedbackLedger
        };
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(state));
        localStorage.setItem('nutriketo_app_version', CURRENT_APP_VERSION);
      } catch(e) {
        console.error("Error al guardar localStorage:", e);
      }
    }

    function getMealDiners(dayIdx, mealType) {
      const key = `${activeWeek}_day_${dayIdx}_${mealType}`;
      return (mealDinersState[key] !== undefined) ? parseInt(mealDinersState[key]) : activeDiners;
    }

    function updateMealDiners(dayIdx, mealType, val) {
      const parsed = Math.min(12, Math.max(1, parseInt(val) || activeDiners));
      const key = `${activeWeek}_day_${dayIdx}_${mealType}`;
      mealDinersState[key] = parsed;
      saveAppState();
      renderDay(selectedIdx);
      if (typeof render3DShoppingList === "function") {
        render3DShoppingList();
      }
    }

    function validateNoDuplicateBroths(mObj) {
      const st = (mObj.starter_name || '').toLowerCase();
      const main = (mObj.main_dish_name || mObj.dish_name || '').toLowerCase();
      if ((st.includes('caldo') || st.includes('consomé') || st.includes('sopa')) && (main.includes('caldo') || main.includes('consomé') || main.includes('sopa'))) {
        mObj.starter_name = "Ensalada de Hojas Verdes de la Granja";
      }
      return mObj;
    }

    function enforceFatSourceUniqueness(mObj) {
      const st = (mObj.starter_name || '').toLowerCase();
      const main = (mObj.main_dish_name || mObj.dish_name || '').toLowerCase();
      const side = (mObj.side_dish_name || '').toLowerCase();

      if ((st.includes('aguacate') || st.includes('guacamole') || main.includes('aguacate') || main.includes('guacamole')) && (side.includes('aguacate') || side.includes('guacamole'))) {
        mObj.side_dish_name = "Bastones de Pepino Fresco con Sal de Mar";
      }
      return mObj;
    }

    function validateNoFruitDairyMix(mObj) {
      let st = (mObj.starter_name || '');
      const stLower = st.toLowerCase();
      if ((stLower.includes('pitahaya') || stLower.includes('pitaya') || stLower.includes('higos') || stLower.includes('durazno')) && (stLower.includes('cottage') || stLower.includes('yogur') || stLower.includes('yogurth'))) {
        if (stLower.includes('fresas')) {
          mObj.starter_name = "Fresas Frescas de la Granja con Queso Cottage";
        } else if (stLower.includes('higos')) {
          mObj.starter_name = "Arilos de Granada Fresca con Semillas de Chía y Nueces Pecana";
        } else if (stLower.includes('pitahaya') || stLower.includes('pitaya')) {
          mObj.starter_name = "Pitahaya Fresca de la Granja con Semillas de Chía y Nueces Pecana";
        } else {
          mObj.starter_name = "Duraznos Frescos con Semillas de Chía y Coco Rayado Sin Azúcar";
        }
      }
      return mObj;
    }

    function enforceIngredientDiversityPerMeal(mObj) {
      const st = (mObj.starter_name || '').toLowerCase();
      const main = (mObj.main_dish_name || mObj.dish_name || '').toLowerCase();
      let side = (mObj.side_dish_name || '').toLowerCase();

      const vegRules = [
        { key: 'coliflor', alt: 'Ejotes Tiernos Salteados a la Mantequilla' },
        { key: 'brócoli', alt: 'Espárragos Verdes Asados al Limón' },
        { key: 'brocoli', alt: 'Espárragos Verdes Asados al Limón' },
        { key: 'calabacita', alt: 'Nopales Tiernos Gratinados con Queso Panela' },
        { key: 'espinaca', alt: 'Ensalada Mix de Hojas Verdes de la Granja' },
        { key: 'nopales', alt: 'Ejotes Salteados con Almendras Fileteadas' },
        { key: 'nopal', alt: 'Ejotes Salteados con Almendras Fileteadas' },
        { key: 'aguacate', alt: 'Bastones de Pepino y Apio con Sal de Mar' }
      ];

      vegRules.forEach(v => {
        const inSt = st.includes(v.key);
        const inMain = main.includes(v.key);
        const inSide = side.includes(v.key);

        if ((inSt && inSide) || (inMain && inSide)) {
          mObj.side_dish_name = v.alt;
        } else if (inSt && inMain) {
          mObj.starter_name = "Ensalada Mix de Hojas Verdes de la Granja";
        }
      });

      return mObj;
    }

    
    function getDishRecipeFromPool(dishName, category, mealType) {
      if (!dishName || !window.DISH_EXCHANGE_POOL) return null;
      const list = category === 'starter' ? window.DISH_EXCHANGE_POOL.starters : (category === 'side' ? window.DISH_EXCHANGE_POOL.sides : window.DISH_EXCHANGE_POOL.mains);
      const found = (list || []).find(item => item.name === dishName || item.name.toLowerCase() === dishName.toLowerCase());
      if (found && found.recipe) return found.recipe;
      return null;
    }

    function getMealObj(dayIdx, rawMeal) {
      if (!rawMeal) return {};
      const weekSlug = typeof activeWeek !== 'undefined' ? (activeWeek === 'Semana 38' ? 'semana_38' : activeWeek.toLowerCase().replace(/ /g, '_')) : 'semana_38';
      const key1 = `${weekSlug}_${dayIdx}_${rawMeal.meal_type}`;
      const key2 = `${activeWeek}_day_${dayIdx}_${rawMeal.meal_type}`;
      
      const override = (window.MEAL_DISH_OVERRIDES && window.MEAL_DISH_OVERRIDES[key1]) ||
                       (window.MEAL_DISH_OVERRIDES && window.MEAL_DISH_OVERRIDES[key2]) ||
                       (typeof customDishesState !== 'undefined' && (customDishesState[key1] || customDishesState[key2]));

      let mObj = { ...rawMeal };
      if (override) {
        mObj.starter_name = override.starter_name || rawMeal.starter_name;
        mObj.main_dish_name = override.main_dish_name || rawMeal.main_dish_name || rawMeal.dish_name;
        mObj.side_dish_name = override.side_dish_name || rawMeal.side_dish_name;
        mObj.is_negotiated = true;

        if (override.macros) {
          mObj.calories_kcal = override.macros.kcal;
          mObj.fat_g = override.macros.fat_g;
          mObj.protein_g = override.macros.protein_g;
          mObj.net_carbs_g = override.macros.net_carbs_g;
        }
        if (override.starter_recipe) mObj.starter_recipe = override.starter_recipe;
        if (override.main_recipe) mObj.main_recipe = override.main_recipe;
        if (override.side_recipe) mObj.side_recipe = override.side_recipe;
      }
      
      validateNoDuplicateBroths(mObj);
      enforceFatSourceUniqueness(mObj);
      validateNoFruitDairyMix(mObj);
      enforceIngredientDiversityPerMeal(mObj);
      enforceMetabolicLoadBalance(mObj);
      return mObj;
    }

    function classifyDishDensity(dishName) {
      if (!dishName) return 'LIGERO';
      const d = dishName.toLowerCase();
      if (d.includes('enchilada') || d.includes('mole') || d.includes('queso') || d.includes('ribeye') || d.includes('sirloin') || d.includes('tocino') || d.includes('gratinado') || d.includes('albóndiga') || d.includes('albondiga') || d.includes('waffle') || d.includes('crepa') || d.includes('parrillada') || d.includes('chiles rellenos')) {
        return 'DENSO';
      }
      if (d.includes('pollo') || d.includes('pavo') || d.includes('pescado') || d.includes('salmón') || d.includes('salmon') || d.includes('omelette') || d.includes('frittata') || d.includes('shakshuka')) {
        return 'MEDIO';
      }
      return 'LIGERO';
    }

    function enforceMetabolicLoadBalance(mObj) {
      if (!mObj) return mObj;
      const mainDensity = classifyDishDensity(mObj.main_dish_name || mObj.dish_name);

      if (mainDensity === 'DENSO') {
        const stLower = (mObj.starter_name || '').toLowerCase();
        const stDensity = classifyDishDensity(mObj.starter_name);
        if (stDensity !== 'LIGERO' || stLower.includes('aguacate') || stLower.includes('queso')) {
          mObj.starter_name = "Ensalada Verde de Arúgula y Espinaca Baby a la Vinagreta de Manzana";
        }

        const sdLower = (mObj.side_dish_name || '').toLowerCase();
        const sdDensity = classifyDishDensity(mObj.side_dish_name);
        if (sdDensity !== 'LIGERO' || sdLower.includes('puré') || sdLower.includes('pure') || sdLower.includes('queso')) {
          mObj.side_dish_name = "Gelatina Artesanal elaborada con Grenetina Natural y Fruta Fresca de la Granja Sin Azúcar";
        }
      }
      return mObj;
    }

    function resolveKetoDishAlias(dishName) {
      let name = dishName || '';
      if (!name) return name;
      let lower = name.toLowerCase();

      if (lower.includes('frijol') || lower.includes('frijoles')) {
        return 'Consomé Claro de Nopales y Hortalizas Tiernas';
      }
      if (lower.includes('chipotle')) {
        name = name.replace(/chipotle/gi, 'Ajo y Tomillo');
      }
      if (lower.includes('arroz') && !lower.includes('coliflor')) {
        name = name.replace(/arroz/gi, 'Cuscús de Coliflor y Ejotes');
      }

      // PATCH V13.2 & V13.3: NOMENCLATURA GASTRONÓMICA Y DEPURACIÓN SENSORIAL (SUPRESIÓN DE "KETO" Y "SIN AZÚCAR")
      name = name.replace(/\\s*Keto\\b/gi, '');
      name = name.replace(/\\s*Cetogénico\\b/gi, '');
      name = name.replace(/\\s*Cetogénica\\b/gi, '');
      name = name.replace(/\\s*Low-Carb\\b/gi, '');
      name = name.replace(/\\(Fideos Keto\\)/gi, '');
      name = name.replace(/\\(Keto\\)/gi, '');
      name = name.replace(/\\s*Sin Azúcar\\b/gi, '');
      name = name.replace(/\\s*Sin Azucar\\b/gi, '');
      name = name.replace(/\\s*Zero\\b/gi, '');
      name = name.replace(/\\s*Dietético\\b/gi, '');
      name = name.replace(/\\s*Dietética\\b/gi, '');
      name = name.replace(/de Grenetina con/gi, 'de');
      name = name.replace(/\\s+/g, ' ').trim();

      return name;
    }

    const compiledPhasesCache = {};

    async function fetchDayPrepPhasesJIT(dayIdx) {
      const day = (getPlanForWeek(activeWeek) && getPlanForWeek(activeWeek).days) ? getPlanForWeek(activeWeek).days[dayIdx] : null;
      if (!day || !day.meals) return;

      const itemsToCompile = [];
      day.meals.forEach(rawM => {
        const m = getMealObj(dayIdx, rawM);
        const diners = getMealDiners(dayIdx, m.meal_type);

        [m.starter_name, m.main_dish_name || m.dish_name, m.side_dish_name].forEach(name => {
          if (name && !compiledPhasesCache[name]) {
            itemsToCompile.push({
              dish_name: name,
              approved_ingredients: m.ingredients || [],
              diners_count: diners
            });
          }
        });
      });

      if (itemsToCompile.length === 0) return;

      try {
        const res = await fetch('/api/menu/compile-phases', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items: itemsToCompile })
        });
        if (res.ok) {
          const data = await res.json();
          if (data.compiled_phases) {
            Object.assign(compiledPhasesCache, data.compiled_phases);
            renderDay(dayIdx);
          }
        }
      } catch(e) {
        console.warn("JIT Phase compilation offline or fallback:", e);
      }
    }

    function renderDynamicPrepPhases(dishName, diners, ingredients) {
      const name = resolveKetoDishAlias(dishName);
      const phases = compiledPhasesCache[name] || compiledPhasesCache[dishName];
      if (phases) {
        const f1 = phases.fase_1_mise_en_place || phases.f1 || `Fase 1 (Mise en Place): Pesar insumos para ${diners} comensales.`;
        const f2 = phases.fase_2_acondicionamiento || phases.f2 || `Fase 2 (Acondicionamiento): Porcionado e higienización.`;
        const f3 = phases.fase_3_termodinamica || phases.f3 || `Fase 3 (Termodinámica): Cocción regulada a temperatura óptima.`;
        const f4 = phases.fase_4_servicio || phases.f4 || `Fase 4 (Servicio): Emplatado para ${diners} personas a 65°C.`;
        return `
          <ul>
            <li><span class="green-bullet">✦</span> <strong>Fase 1 (Mise en Place):</strong> ${f1}</li>
            <li><span class="green-bullet">✦</span> <strong>Fase 2 (Acondicionamiento):</strong> ${f2}</li>
            <li><span class="green-bullet">✦</span> <strong>Fase 3 (Termodinámica):</strong> ${f3}</li>
            <li><span class="green-bullet">✦</span> <strong>Fase 4 (Servicio):</strong> ${f4}</li>
          </ul>
        `;
      }
      
      const n = parseInt(diners) || 6;
      const dLower = (name || '').toLowerCase();
      
      function resolveTechniqueJS(dishName) {
        const nm = (dishName || '').toLowerCase();
        if (['infusión', 'infusion', 'té ', 'te ', 'tisana', 'café', 'cafe'].some(k => nm.includes(k))) return 'steep_beverage';
        if (['crema', 'sopa', 'caldo', 'consomé', 'consome'].some(k => nm.includes(k))) return 'boil_and_blend';
        if (['gelatina', 'mousse', 'panna cotta'].some(k => nm.includes(k))) return 'gelatin_molding';
        if (['çılbır', 'cilbir', 'turcos', 'pochado', 'pochados', 'benedict'].some(k => nm.includes(k))) return 'poach_and_emulsion';
        if (['omelette', 'huevo', 'revuelto', 'frittata', 'shakshuka'].some(k => nm.includes(k))) return 'pan_fry_egg';
        if (['higos', 'granada', 'fruta', 'ensalada', 'bastones', 'pepino', 'tartar'].some(k => nm.includes(k))) return 'raw_assembly';
        if (['salmón', 'salmon', 'pechuga', 'pavo', 'pollo', 'carne', 'corte'].some(k => nm.includes(k))) return 'saute_and_sear';
        return 'raw_assembly'; // Default seguro NUNCA debe ser infusión
      }

      const tech = resolveTechniqueJS(name);

      let f1, f2, f3, f4, techBadge;
      if (tech === 'steep_beverage') {
        techBadge = "🍵 Infusión Herbal & Bebida";
        f1 = `Fase 1 (Mise en Place de Bebidas):\n* Insumos base para ${n} personas: Sobres o mezcla de ${name}.\n* Agua purificada: ${n * 250} ml de agua de manantial.`;
        f2 = `Fase 2 (Calentamiento de Agua):\n* Llevar ${n * 250} ml de agua purificada a ebullición suave (95°C) en tetera.`;
        f3 = `Fase 3 (Infusión Herbal):\n* Verter el agua hirviendo sobre ${name} e infundir 5 a 6 minutos.`;
        f4 = `Fase 4 (Servicio):\n* Colar y servir caliente a 70°C en tazas térmicas.`;
      } else if (tech === 'boil_and_blend') {
        techBadge = "🍲 Crema / Sopa (Licuado & Cremado Lácteo)";
        f1 = `Fase 1 (Mise en Place y Gramajes de Crema):\n* Insumos base para ${n} personas: Vegetales e insumos de ${name}.\n* Base líquida: ${n * 125} ml de caldo tibio y mantequilla de pastoreo.`;
        f2 = `Fase 2 (Base Sofrito Aromático):\n* En cacerola a fuego medio, sofrito de cebolla, ajo y mantequilla por 4 minutos hasta acitronar sin quemar.`;
        f3 = `Fase 3 (Cocción en Caldo, Licuado & Cremado):\n* Verter el caldo y vegetales. Hervir suavemente (95°C) durante 8-10 minutos hasta ternura.\n* Licuar a alta velocidad por 2 minutos hasta lograr textura aterciopelada.\n* Regresar a fuego muy bajo, integrar crema/queso rallado agitando suavemente sin dejar hervir.`;
        f4 = `Fase 4 (Servicio Gourmet):\n* Servir en tazones hondos precalentados a 68°C con láminas de queso, pimienta negra y un hilo de aceite VEVO.`;
      } else if (tech === 'gelatin_molding') {
        techBadge = "🍮 Gelatina Artesanal & Moldeo a 4°C";
        f1 = `Fase 1 (Mise en Place y Gramajes):\n* Jugo fresco o base de ${name} para ${n} personas con grenetina natural e insumos de la granja.`;
        f2 = `Fase 2 (Hidratación & Disolución):\n* Hidratar grenetina en agua fría 5 minutos; disolver a 60°C mezclando con el jugo caliente.`;
        f3 = `Fase 3 (Moldeo & Refrigeración):\n* Integrar el resto del líquido fresco y verter en moldes individuales a 4°C por 3 horas.`;
        f4 = `Fase 4 (Servicio en Frío):\n* Servir frío a 4°C firmemente cuajado.`;
      } else if (tech === 'poach_and_emulsion') {
        techBadge = "🍳 Huevos Pochados Çılbır (Base de Yogur & Mantequilla Especiada)";
        f1 = `Fase 1 (Mise en Place y Gramajes):\n* 12 huevos frescos, 750 g (3 tazas) yogur griego natural a temp. ambiente, 3 dientes de ajo rallados, 135 g mantequilla de pastoreo, 45 ml aceite VEVO, 1 cda paprika dulce/orégano, 1.5 cditas comino molido, 3 cdas vinagre.`;
        f2 = `Fase 2 (Base de Yogur & Mantequilla Especiada):\n* Batir yogur con ajo y sal en tazón formando cama en 6 platos. Derretir mantequilla con aceite de oliva a fuego medio-bajo hasta dorar (avellanada); retirar e incorporar paprika dulce y comino.`;
        f3 = `Fase 3 (Pochado Regulado a 85-90°C):\n* Hervir agua con vinagre a 85-90°C. Cuelar clara líquida y pochar 3-4 huevos por tanda exactamente 3 minutos para yema líquida. Escurrir en papel absorbente.`;
        f4 = `Fase 4 (Montaje Gourmet por Capas):\n* Colocar 2 huevos pochados sobre cama de yogur en cada plato, bañar con mantequilla especiada tibia, eneldo fresco y pimienta negra. Servir a 55-60°C.`;
      } else if (tech === 'pan_fry_egg') {
        techBadge = "🍳 Huevos Revueltos / Omelette en Sartén";
        f1 = `Fase 1 (Mise en Place y Gramajes):\n* Huevos frescos (${n * 2} piezas), mantequilla de pastoreo, aromáticos y sal de mar.`;
        f2 = `Fase 2 (Batido e Integración):\n* Batir huevos energéticamente con globo homogenizando clara y yema.`;
        f3 = `Fase 3 (Cocción Regulada en Sartén):\n* Calentar sartén antiadherente a fuego medio-bajo con mantequilla. Cuajar suavemente 3-4 minutos.`;
        f4 = `Fase 4 (Servicio Culinario):\n* Servir de inmediato a 60°C.`;
      } else if (tech === 'saute_and_sear') {
        techBadge = "🔥 Sello Térmico & Reposo Culinario";
        f1 = `Fase 1 (Mise en Place y Gramajes Exactos):\n* Proteína e insumos de ${name} escalados para ${n} personas con grasas saludables y sal de mar.`;
        f2 = `Fase 2 (Acondicionamiento Culinario):\n* Porcionar en cortes uniformes sazonando homogéneamente.`;
        f3 = `Fase 3 (Termodinámica y Sello en Sartén):\n* Calentar sartén de hierro a 180°C con materia grasa. Sellar 4 min por lado hasta costra dorada. Reposar 4 min.`;
        f4 = `Fase 4 (Ensamblaje y Servicio):\n* Trinchar contra la fibra y emplatar repartiendo equitativamente para ${n} personas a 65°C.`;
      } else {
        techBadge = "🥗 Ensamblaje en Frío & Macerado (4°C)";
        f1 = `Fase 1 (Mise en Place en Frío):\n* Pesar hortalizas/insumos frescos de ${name} para ${n} personas.\n* Sazonadores y aceites a 4°C.`;
        f2 = `Fase 2 (Higienización y Corte):\n* Lavar e higienizar en agua helada (4°C). Porcionar en cubos de 1 cm o bastones de 7-8 cm.`;
        f3 = `Fase 3 (Emulsión en Frío):\n* Emulsionar el aderezo frío y marinar/macerar a 4°C por 8 minutos.`;
        f4 = `Fase 4 (Servicio en Frío):\n* Montar en vajilla refrigerada y servir fresco a 4-8°C.`;
      }

      return `
        <div style="font-size:0.75rem; font-weight:800; background:var(--bg-clinical); color:var(--color-corporate); padding:0.2rem 0.5rem; border-radius:6px; margin-bottom:0.4rem; display:inline-block; border:1px solid var(--border-clinical);">${techBadge}</div>
        <ul>
          <li><span class="green-bullet">✦</span> ${f1}</li>
          <li><span class="green-bullet">✦</span> ${f2}</li>
          <li><span class="green-bullet">✦</span> ${f3}</li>
          <li><span class="green-bullet">✦</span> ${f4}</li>
        </ul>
      `;
    }

    function initSetupPanel() {
      // 1. Cosecha Grid (sección editable ordenada A-Z de catálogo maestro + personalizados)
      const hGrid = document.getElementById('harvest-checklist-grid');
      if (hGrid) {
        hGrid.innerHTML = '';
        const activeFarmMaster = FARM_MASTER_CATALOG.filter(name => {
          const slug = normalizeToCanonicalSlug(name);
          return !deletedFarmItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === name.toLowerCase());
        });
        const activeCustomFarm = customFarmItems.filter(name => {
          const slug = normalizeToCanonicalSlug(name);
          return !deletedFarmItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === name.toLowerCase());
        });

        const allFarmNames = [...new Set([...activeFarmMaster, ...activeCustomFarm])];
        allFarmNames.sort((a, b) => a.localeCompare(b));

        allFarmNames.forEach((itemName, idx) => {
          const isCanonical = FARM_MASTER_CATALOG.includes(itemName);
          const slug = normalizeToCanonicalSlug(itemName);
          const isChecked = selectedHarvest.some(h => {
            const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
            return normalizeToCanonicalSlug(hStr) === slug || hStr.toLowerCase() === itemName.toLowerCase();
          });

          const div = document.createElement('div');
          div.className = 'option-row';
          div.style.color = 'var(--text-main)';
          const safeName = itemName.replace(/'/g, "\\'");
          div.style.cssText = 'display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; padding: 0.5rem 0.75rem; border-radius: 10px; background: var(--surface-card); border: 1px solid var(--border-clinical); box-shadow: var(--shadow-clinical-sm);';
          div.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem; flex: 1; min-width: 0;">
              <input type="checkbox" id="h-item-${idx}" value="${safeName}" ${isChecked ? 'checked' : ''} onchange="updateHarvestSelection('${safeName}', this.checked)">
              <label for="h-item-${idx}" style="cursor:pointer; flex: 1; color: var(--text-main); font-weight: 700; font-size: 0.85rem; word-break: break-word;">${itemName}</label>
            </div>
            <button type="button" onclick="deleteHarvestItem('${safeName}')" style="background: none; border: none; color: #ef4444; font-size: 0.95rem; cursor: pointer; padding: 0.1rem 0.3rem; opacity: 0.7; transition: opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.7'" title="Eliminar ${safeName} de la Cosecha">🗑️</button>
          `;
          hGrid.appendChild(div);
        });
      }

      // 2. Alacena Grid (sección editable seccionada por Categoría y ordenada A-Z)
      const pGrid = document.getElementById('pantry-stock-grid');
      if (pGrid) {
        pGrid.innerHTML = '';
        const nonFarm = [];
        const seenPantrySlugs = new Set();
        if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};

        // 2.1 Insumos Físicos de Despensa (window.PANTRY_STOCK_INVENTORY)
        // Regla de Oro: En Reconfigurar Parámetros sólo se muestran los 106 insumos que realmente existen en el inventario físico de la despensa.
        // const isCurrentlyHarvested = selectedHarvest.some(h => areInsumosEquivalent(h, 'test'));
        if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined') {
          Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(k => {
            const pObj = window.PANTRY_STOCK_INVENTORY[k];
            if (!pObj) return;
            // Excluir claves de compatibilidad interna con stock 0 (como frutas de catálogo o ajo-fresco de test)
            if (pObj.stock <= 0 && (!pObj.item_num || pObj.item_num <= 0)) return;
            // Excluir alias duplicados para no repetir el mismo ítem en la pantalla
            if (k === 'multisinergix' || k === 'aminosinergix' || k === '33plus' || k === '34plus' || k === 'zarzamoras-frescas' || k === 'fresas-frescas' || k === 'arilos-granada' || k === 'moras-frescas' || k === 'frambuesas-frescas' || k === 'arandanos-frescos' || k === 'pitaya-fresca' || k === 'ajo-fresco') return;

            const slug = normalizeToCanonicalSlug(pObj.name || k);
            if (deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === pObj.name.toLowerCase())) return;
            const alreadyInList = nonFarm.some(existing => areInsumosEquivalent(existing.item_name, pObj.name));
            if (!alreadyInList) {
              seenPantrySlugs.add(slug);
              const assignedCat = (pObj.status === 'prohibited')
                ? '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)'
                : (pObj.category || getSmartItemCategory(pObj.name));
              nonFarm.push({
                item_name: pObj.name,
                quantity: pObj.stock,
                unit: pObj.unit || 'g',
                category: assignedCat,
                status: pObj.status || 'canonical',
                packaging: pObj.packaging
              });
            }
          });
        }

        // 2.3 Insumos en Cuarentena (extraídos dinámicamente de window.PANTRY_STOCK_INVENTORY)
        const QUARANTINE_PANTRY_ITEMS = [];

        QUARANTINE_PANTRY_ITEMS.forEach(qItem => {
          const slug = normalizeToCanonicalSlug(qItem.item_name);
          if (!deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === qItem.item_name.toLowerCase())) {
            const alreadyInList = nonFarm.some(existing => areInsumosEquivalent(existing.item_name, qItem.item_name));
            if (!alreadyInList) {
              seenPantrySlugs.add(slug);
              nonFarm.push(qItem);
            }
          }
        });

        const categoriesMap = {};
        nonFarm.forEach(i => {
          const cat = i.category || getSmartItemCategory(i.item_name, i.category);
          if (!categoriesMap[cat]) categoriesMap[cat] = [];
          categoriesMap[cat].push(i);
        });

        const sortedCats = Object.keys(categoriesMap).sort((a, b) => getCategoryIndex(a) - getCategoryIndex(b));

        sortedCats.forEach(catName => {
          const isQuarantine = catName.includes('Cuarentena') || catName.includes('🛑');
          const catHeader = document.createElement('div');
          if (isQuarantine) {
            catHeader.style.cssText = 'grid-column: 1 / -1; font-weight: 800; font-size: 0.95rem; color: #dc2626; margin-top: 1.2rem; margin-bottom: 0.5rem; padding: 0.45rem 0.75rem; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #dc2626; border-radius: 8px; display: flex; align-items: center; gap: 0.4rem;';
          } else {
            catHeader.style.cssText = 'grid-column: 1 / -1; font-weight: 800; font-size: 0.92rem; color: var(--color-34plus); margin-top: 0.8rem; margin-bottom: 0.4rem; padding-bottom: 0.3rem; border-bottom: 2px solid var(--border-clinical); display: flex; align-items: center; gap: 0.4rem;';
          }
          catHeader.innerHTML = `<span>${catName}</span>`;
          pGrid.appendChild(catHeader);

          const items = categoriesMap[catName];
          items.sort((a, b) => a.item_name.localeCompare(b.item_name, 'es', { sensitivity: 'base' }));

          items.forEach(i => {
            const slug = normalizeToCanonicalSlug(i.item_name);
            const safeName = i.item_name.replace(/'/g, "\\'");

            const options = getCommercialUnitOptions(i.item_name, i.unit, i.quantity);
            let currentUnit = window.pantryCardUnits[i.item_name];
            if (!currentUnit) {
              if (window.PANTRY_STOCK_INVENTORY) {
                const invKey = Object.keys(window.PANTRY_STOCK_INVENTORY).find(k => areInsumosEquivalent(window.PANTRY_STOCK_INVENTORY[k].name, i.item_name));
                if (invKey && window.PANTRY_STOCK_INVENTORY[invKey].unit) {
                  currentUnit = window.PANTRY_STOCK_INVENTORY[invKey].unit;
                }
              }
            }
            if (!currentUnit && options.length > 0) {
              currentUnit = options[0].id;
            }
            window.pantryCardUnits[i.item_name] = currentUnit;

            let val = pantryStock[i.item_name];
            if (val === undefined) {
              const matchedKey = Object.keys(pantryStock).find(k => areInsumosEquivalent(k, i.item_name));
              if (matchedKey !== undefined) {
                val = pantryStock[matchedKey];
              } else if (window.PANTRY_STOCK_INVENTORY) {
                const invKey = Object.keys(window.PANTRY_STOCK_INVENTORY).find(k => areInsumosEquivalent(window.PANTRY_STOCK_INVENTORY[k].name, i.item_name));
                val = invKey ? window.PANTRY_STOCK_INVENTORY[invKey].stock : 0;
              } else {
                val = 0;
              }
            }

            const isEggItem = /huevo/i.test(i.item_name);
            const eggHelperBtn = isEggItem ? `
              <button type="button" onclick="addPantryCasillero('${safeName}')" style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 4px; padding: 2px 6px; font-size: 0.72rem; font-weight: 700; color: #047857; cursor: pointer; white-space: nowrap; transition: all 0.2s;" onmouseover="this.style.background='rgba(16,185,129,0.25)'" onmouseout="this.style.background='rgba(16,185,129,0.12)'" title="Sumar 1 casillero completo (+30 piezas)">+30 (1 Casillero)</button>
            ` : '';

            const selectHtml = options.length > 0 ? `
              <select style="padding: 0.25rem 0.35rem; font-weight: 700; font-size: 0.78rem; border: 1px solid ${isQuarantine ? 'rgba(239, 68, 68, 0.5)' : 'var(--border-clinical)'}; border-radius: 6px; background: var(--surface-card); color: var(--text-main); cursor: pointer; max-width: 145px;" onchange="updatePantryStockUnit('${safeName}', this.value, this.previousElementSibling)">
                ${options.map(opt => `<option value="${opt.id}" ${opt.id === currentUnit ? 'selected' : ''}>${opt.label}</option>`).join('')}
              </select>
            ` : `<span style="font-size: 0.78rem; font-weight: 600; color: ${isQuarantine ? '#dc2626' : 'var(--text-muted)'};">${i.unit}</span>`;

            const div = document.createElement('div');
            div.className = isQuarantine ? 'option-row quarantine-card-item' : 'option-row';
            div.style.color = 'var(--text-main)';
            if (isQuarantine) {
              div.style.cssText = 'display: flex; flex-direction: column; justify-content: space-between; gap: 0.4rem; padding: 0.55rem 0.75rem; border-radius: 10px; background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.35); box-shadow: var(--shadow-clinical-sm);';
            } else {
              div.style.cssText = 'display: flex; flex-direction: column; justify-content: space-between; gap: 0.4rem; padding: 0.55rem 0.75rem; border-radius: 10px; background: var(--surface-card); border: 1px solid var(--border-clinical); box-shadow: var(--shadow-clinical-sm);';
            }
            div.innerHTML = `
              <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 0.4rem; width: 100%;">
                <span style="font-weight: 700; font-size: 0.88rem; color: ${isQuarantine ? '#dc2626' : 'var(--text-main)'}; word-break: break-word; line-height: 1.25;">${i.item_name}</span>
                <button type="button" onclick="deletePantryItem('${safeName}')" style="background: none; border: none; color: #ef4444; font-size: 0.95rem; cursor: pointer; padding: 0.1rem 0.3rem; border-radius: 4px; opacity: 0.7; transition: opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.7'" title="Eliminar ${safeName} del Inventario">🗑️</button>
              </div>
              <div style="display: flex; align-items: center; justify-content: flex-end; gap: 0.4rem; width: 100%; margin-top: 0.2rem; flex-wrap: wrap;">
                ${eggHelperBtn}
                <input type="number" step="${currentUnit === 'piezas' || currentUnit === 'casillero' ? '1' : '0.1'}" min="0" value="${val}" style="width: 70px; padding: 0.25rem 0.4rem; font-weight: 800; text-align: center; border: 1px solid ${isQuarantine ? 'rgba(239, 68, 68, 0.5)' : 'var(--border-clinical)'}; border-radius: 6px; background: var(--surface-card); color: var(--text-main); font-size: 0.88rem;" onchange="updatePantryStock('${safeName}', this.value, window.pantryCardUnits['${safeName}'])">
                ${selectHtml}
              </div>
            `;
            pGrid.appendChild(div);
          });
        });
      }

      if (document.getElementById('setup-week')) document.getElementById('setup-week').value = activeWeek;
      if (document.getElementById('setup-diners')) document.getElementById('setup-diners').value = activeDiners;
    }

    function toggleEditDetails() {
      const details = document.getElementById('edit-inventory-details');
      if (details) {
        if (details.style.display === 'none' || !details.style.display) {
          details.style.display = 'block';
        } else {
          details.style.display = 'none';
        }
      }
    }

    function addNewHarvestItem() {
      const nameInput = document.getElementById('new-harvest-name');
      let val = nameInput ? nameInput.value.trim() : '';
      if (!val) {
        if (typeof showToast === 'function') {
          showToast('⚠️ Por favor escribe el nombre del insumo para la Cosecha.', 'warning');
        }
        if (nameInput) nameInput.focus();
        return;
      }

      if (/nuex/i.test(val)) {
        val = val.replace(/nuex/gi, 'nuez');
      }
      if (/^nuez\\s+pecana$/i.test(val.trim())) {
        val = "Nuez pecana fresca de la granja";
      }

      const slug = normalizeToCanonicalSlug(val);
      deletedFarmItems = deletedFarmItems.filter(d => normalizeToCanonicalSlug(d) !== slug && d.toLowerCase() !== val.toLowerCase());

      const existsInMaster = FARM_MASTER_CATALOG.some(m => normalizeToCanonicalSlug(m) === slug || m.toLowerCase() === val.toLowerCase());
      if (!existsInMaster) {
        const existsInCustom = customFarmItems.some(c => normalizeToCanonicalSlug(c) === slug || c.toLowerCase() === val.toLowerCase());
        if (!existsInCustom) {
          customFarmItems.push(val);
        }
      }

      const existsInSelected = selectedHarvest.some(h => {
        const hName = typeof h === 'string' ? h : (h.item_name || h.name || '');
        return normalizeToCanonicalSlug(hName) === slug || hName.toLowerCase() === val.toLowerCase();
      });

      if (!existsInSelected) {
        selectedHarvest.push(val);
      }

      const existsInShop = rawShopBase.some(i => normalizeToCanonicalSlug(i.item_name) === slug || i.item_name.toLowerCase() === val.toLowerCase());
      if (!existsInShop) {
        const newId = 100 + rawShopBase.length + 1;
        rawShopBase.push({
          id: newId,
          category: "🌾 Cosecha Directa de la Granja / Huerto",
          item_name: val,
          quantity: 1.0,
          unit: "kg/piezas",
          quantity_str: "1.0 kg/piezas"
        });
      }

      if (nameInput) nameInput.value = '';
      saveAppState();
      initSetupPanel();
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
      if (typeof showToast === 'function') showToast(`🌿 '${val}' añadido a Cosecha Activa.`);
    }

    function updatePantryCatBadge(cat) {
      const badge = document.getElementById('pantry-cat-indicator');
      if (!badge) return;
      if (cat.includes('Cuarentena') || cat.includes('🛑') || cat.includes('prohibited')) {
        badge.textContent = 'Destino: 🛑 Cuarentena (Fuera de Protocolo)';
        badge.style.background = 'rgba(239, 68, 68, 0.15)';
        badge.style.color = '#dc2626';
        badge.style.borderColor = 'rgba(239, 68, 68, 0.4)';
      } else {
        badge.textContent = `Destino: ${cat}`;
        badge.style.background = 'rgba(28,117,188,0.12)';
        badge.style.color = '#1C75BC';
        badge.style.borderColor = 'rgba(28,117,188,0.25)';
      }
    }

    function onNewPantryNameInput(val) {
      const catSelect = document.getElementById('new-pantry-cat');
      const unitSelect = document.getElementById('new-pantry-unit');
      const qBox = document.getElementById('pantry-quarantine-reason-box');
      if (!val || !val.trim()) {
        updatePantryCatBadge('🥬 Verduras, Hortalizas y Frescos');
        if (qBox) qBox.style.display = 'none';
        return;
      }

      // Sugerir categoría automáticamente si el usuario no la ha fijado manualmente
      if (catSelect && catSelect.dataset.userLocked !== 'true') {
        const smartCat = getSmartItemCategory(val, '');
        catSelect.value = smartCat;
        updatePantryCatBadge(smartCat);
        if (qBox) {
          qBox.style.display = (smartCat.includes('Cuarentena') || smartCat.includes('🛑')) ? 'block' : 'none';
        }
      }

      // Sugerir unidad de empaque comercial si el usuario no la ha fijado manualmente
      if (unitSelect && unitSelect.dataset.userLocked !== 'true') {
        const v = val.toLowerCase();
        if (/huevo|huevos/i.test(v)) {
          unitSelect.value = 'casillero';
        } else if (/sardina|sardinas|atún|atun/i.test(v)) {
          unitSelect.value = 'latas';
        } else if (/yogurt|yoghurt/i.test(v)) {
          unitSelect.value = 'bote_900';
        } else if (/leche de coco|leche/i.test(v)) {
          unitSelect.value = 'ml';
        } else if (/mayonesa|ghee|mantequilla|crema/i.test(v)) {
          unitSelect.value = 'frasco_500';
        } else if (/aceite|vinagre/i.test(v)) {
          unitSelect.value = 'botella_vevo';
        } else if (/frijol|arroz/i.test(v)) {
          unitSelect.value = 'bolsa_750';
        } else if (/lenteja|garbanzo/i.test(v)) {
          unitSelect.value = 'bolsa_500';
        } else if (/sal\b|pimienta|orégano|oregano|comino|canela|clavo|epazote|romero|tomillo/i.test(v)) {
          unitSelect.value = 'g';
        } else if (/chayote|pepino|aguacate/i.test(v)) {
          unitSelect.value = 'piezas';
        } else {
          unitSelect.value = 'kg';
        }
      }
    }

    function onNewPantryCatChange(cat) {
      const catSelect = document.getElementById('new-pantry-cat');
      if (catSelect) catSelect.dataset.userLocked = 'true';
      updatePantryCatBadge(cat);
      const qBox = document.getElementById('pantry-quarantine-reason-box');
      if (qBox) {
        qBox.style.display = (cat.includes('Cuarentena') || cat.includes('🛑')) ? 'block' : 'none';
      }
    }

    function addNewPantryItem() {
      const nameInput = document.getElementById('new-pantry-name');
      const catSelect = document.getElementById('new-pantry-cat');
      const qtyInput = document.getElementById('new-pantry-qty');
      const unitSelect = document.getElementById('new-pantry-unit');
      const reasonInput = document.getElementById('new-pantry-reason');

      const val = nameInput ? nameInput.value.trim() : '';
      const chosenCat = catSelect ? catSelect.value : getSmartItemCategory(val);
      const qty = parseFloat(qtyInput ? qtyInput.value : 1.0) || 1.0;
      const unit = (unitSelect ? unitSelect.value.trim() : '') || 'kg';
      const reason = (reasonInput ? reasonInput.value.trim() : '') || '';

      if (!val) {
        if (typeof showToast === 'function') {
          showToast('⚠️ Por favor escribe el nombre del insumo para la Alacena.', 'warning');
        }
        if (nameInput) nameInput.focus();
        return;
      }

      const isQuarantine = chosenCat.includes('Cuarentena') || chosenCat.includes('🛑');
      const itemStatus = isQuarantine ? 'prohibited' : 'canonical';

      const slug = normalizeToCanonicalSlug(val);
      deletedPantryItems = deletedPantryItems.filter(d => normalizeToCanonicalSlug(d) !== slug && d.toLowerCase() !== val.toLowerCase());

      const existingInShop = rawShopBase.find(i => normalizeToCanonicalSlug(i.item_name) === slug || i.item_name.toLowerCase() === val.toLowerCase());
      const canonicalName = existingInShop ? existingInShop.item_name : val;

      pantryStock[canonicalName] = qty;
      if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};
      window.pantryCardUnits[canonicalName] = unit;

      if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined' && window.PANTRY_STOCK_INVENTORY) {
        window.PANTRY_STOCK_INVENTORY[slug] = {
          name: canonicalName,
          stock: qty,
          unit: unit,
          category: chosenCat,
          status: itemStatus,
          reason: isQuarantine ? (reason || 'Insumo fuera de protocolo cetogénico (Cuarentena NOM-004)') : null
        };
      }

      // Si es canónico y no está en rawShopBase, lo registramos para que pueda calcularse amortización si entra al menú
      if (!isQuarantine && !existingInShop) {
        const newId = 200 + rawShopBase.length + 1;
        rawShopBase.push({
          id: newId,
          category: chosenCat,
          item_name: canonicalName,
          quantity: qty,
          unit: unit,
          quantity_str: `${qty} ${unit}`
        });
      }

      // Resetear campos
      if (nameInput) nameInput.value = '';
      if (qtyInput) qtyInput.value = '1';
      if (catSelect) {
        catSelect.dataset.userLocked = '';
        catSelect.value = '🥬 Verduras, Hortalizas y Frescos';
      }
      if (unitSelect) {
        unitSelect.dataset.userLocked = '';
        unitSelect.value = 'kg';
      }
      if (reasonInput) reasonInput.value = '';
      const qBox = document.getElementById('pantry-quarantine-reason-box');
      if (qBox) qBox.style.display = 'none';
      updatePantryCatBadge('🥬 Verduras, Hortalizas y Frescos');

      saveAppState();
      initSetupPanel();
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
      if (typeof showToast === 'function') {
        if (isQuarantine) {
          showToast(`🛑 '${canonicalName}' colocado en Cuarentena (${qty} ${unit}).`, 'warning');
        } else {
          showToast(`📦 '${canonicalName}' registrado en ${chosenCat} (${qty} ${unit}).`, 'success');
        }
      }
    }

    function updateHarvestSelection(itemName, isChecked) {
      const slug = normalizeToCanonicalSlug(itemName);
      if (isChecked) {
        const exists = selectedHarvest.some(h => {
          const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
          return normalizeToCanonicalSlug(hStr) === slug || hStr.toLowerCase() === itemName.toLowerCase();
        });
        if (!exists) {
          selectedHarvest.push(itemName);
        }
      } else {
        selectedHarvest = selectedHarvest.filter(h => {
          const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
          return normalizeToCanonicalSlug(hStr) !== slug && hStr.toLowerCase() !== itemName.toLowerCase();
        });
      }
      saveAppState();
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
    }

    function updatePantryStock(itemName, val, unit) {
      const parsed = parseFloat(val) || 0;
      if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};
      const cardUnit = unit || window.pantryCardUnits[itemName] || 'g';
      window.pantryCardUnits[itemName] = cardUnit;
      pantryStock[itemName] = parsed;

      const slug = normalizeToCanonicalSlug(itemName);
      if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined' && window.PANTRY_STOCK_INVENTORY) {
        const matchedKey = Object.keys(window.PANTRY_STOCK_INVENTORY).find(k => 
          k === slug || areInsumosEquivalent(window.PANTRY_STOCK_INVENTORY[k].name, itemName)
        );
        if (matchedKey) {
          window.PANTRY_STOCK_INVENTORY[matchedKey].stock = parsed;
          window.PANTRY_STOCK_INVENTORY[matchedKey].unit = cardUnit;
        } else {
          window.PANTRY_STOCK_INVENTORY[slug] = {
            name: itemName,
            stock: parsed,
            unit: cardUnit,
            status: 'canonical'
          };
        }
      }
      saveAppState();
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
    }

    function addPantryCasillero(itemName) {
      if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};
      const currentUnit = window.pantryCardUnits[itemName] || 'piezas';
      const current = parseFloat(pantryStock[itemName]) || 0;
      let increment = 30;
      if (currentUnit === 'casillero') {
        increment = 1;
      } else if (currentUnit === 'docena') {
        increment = 2.5;
      }
      const newVal = current + increment;
      updatePantryStock(itemName, newVal, currentUnit);
      initSetupPanel();
    }

    function updatePantryStockUnit(itemName, newUnitId, inputElem) {
      if (typeof window.pantryCardUnits === 'undefined') window.pantryCardUnits = {};
      const oldUnitId = window.pantryCardUnits[itemName] || 'g';
      const currentVal = parseFloat(pantryStock[itemName]) || 0;

      const oldBase = (resolvePantryCommercialUnit(currentVal, oldUnitId) || { val: currentVal }).val;
      const dummyOne = (resolvePantryCommercialUnit(1, newUnitId) || { val: 1 }).val || 1;

      let convertedVal = oldBase > 0 ? (oldBase / dummyOne) : currentVal;
      convertedVal = Math.round(convertedVal * 100) / 100;

      window.pantryCardUnits[itemName] = newUnitId;
      pantryStock[itemName] = convertedVal;

      if (inputElem) {
        inputElem.value = convertedVal;
      }

      updatePantryStock(itemName, convertedVal, newUnitId);
      initSetupPanel();
    }

    function showClinicalConfirmModal(options) {
      const {
        title = 'Confirmar Acción Clínica',
        message = '¿Deseas proceder con esta acción?',
        icon = '🗑️',
        confirmText = 'Eliminar Insumo',
        cancelText = 'Cancelar',
        onConfirm
      } = options || {};

      let modalOverlay = document.getElementById('clinical-confirm-modal');
      if (!modalOverlay) {
        modalOverlay = document.createElement('div');
        modalOverlay.id = 'clinical-confirm-modal';
        document.body.appendChild(modalOverlay);
      }

      modalOverlay.style.cssText = 'position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px); z-index: 99999; display: flex; align-items: center; justify-content: center; padding: 1rem; transition: opacity 0.2s ease-in-out;';

      modalOverlay.innerHTML = `
        <div style="background: var(--surface-card, #ffffff); border: 1px solid var(--border-clinical, #e2e8f0); box-shadow: var(--shadow-clinical-lg, 0 10px 25px -5px rgba(15, 23, 42, 0.2)); border-radius: 1rem; max-width: 26rem; width: 100%; padding: 1.5rem; text-align: left;" class="dark:bg-slate-900 dark:border-slate-800">
          <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <div style="width: 2.75rem; height: 2.75rem; border-radius: 0.75rem; background: rgba(183, 14, 12, 0.1); color: #B70E0C; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; flex-shrink: 0;">
              ${icon}
            </div>
            <div>
              <h3 style="margin: 0; font-weight: 800; font-size: 1.05rem; color: var(--text-main, #0f172a);" class="dark:text-slate-100">${title}</h3>
              <p style="margin: 0.2rem 0 0 0; font-size: 0.75rem; font-weight: 700; color: var(--color-corporate, #1C75BC);">Gobernanza Clínico-Nutricional T.I.L.O.®</p>
            </div>
          </div>
          
          <div style="margin: 0 0 1.25rem 0; font-size: 0.88rem; color: var(--text-muted, #475569); line-height: 1.5;" class="dark:text-slate-300">
            ${message}
          </div>
          
          <div style="display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem; margin-top: 1.25rem;">
            <button type="button" id="clinical-modal-cancel-btn" style="min-height: 44px; min-width: 100px; padding: 0.6rem 1.25rem; border-radius: 0.75rem; border: 1px solid var(--border-clinical, #cbd5e1); background: transparent; color: var(--text-main, #334155); font-weight: 700; font-size: 0.88rem; cursor: pointer; transition: all 0.2s ease;" onmouseover="this.style.background='var(--bg-clinical)'" onmouseout="this.style.background='transparent'">
              ${cancelText}
            </button>
            <button type="button" id="clinical-modal-confirm-btn" style="min-height: 44px; min-width: 130px; padding: 0.6rem 1.25rem; border-radius: 0.75rem; border: none; background: #B70E0C; color: #ffffff; font-weight: 700; font-size: 0.88rem; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(183, 14, 12, 0.25);" onmouseover="this.style.background='#960b0a'" onmouseout="this.style.background='#B70E0C'">
              ${confirmText}
            </button>
          </div>
        </div>
      `;

      modalOverlay.style.display = 'flex';

      const cancelBtn = document.getElementById('clinical-modal-cancel-btn');
      const confirmBtn = document.getElementById('clinical-modal-confirm-btn');

      const closeModal = () => {
        modalOverlay.style.display = 'none';
      };

      cancelBtn.onclick = () => closeModal();
      
      confirmBtn.onclick = () => {
        closeModal();
        if (typeof onConfirm === 'function') {
          onConfirm();
        }
      };
    }

    function deleteHarvestItem(itemName) {
      showClinicalConfirmModal({
        title: 'Eliminar Insumo de Cosecha',
        message: `¿Estás seguro de que deseas eliminar definitivamente el insumo <strong>"${itemName}"</strong> de la Cosecha Activa?`,
        icon: '🗑️',
        confirmText: 'Sí, Eliminar Insumo',
        cancelText: 'Cancelar',
        onConfirm: () => {
          const slug = normalizeToCanonicalSlug(itemName);
          if (!deletedFarmItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === itemName.toLowerCase())) {
            deletedFarmItems.push(itemName);
          }
          customFarmItems = customFarmItems.filter(n => normalizeToCanonicalSlug(n) !== slug && n.toLowerCase() !== itemName.toLowerCase());
          selectedHarvest = selectedHarvest.filter(h => {
            const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
            return normalizeToCanonicalSlug(hStr) !== slug && hStr.toLowerCase() !== itemName.toLowerCase();
          });
          rawShopBase = rawShopBase.filter(i => normalizeToCanonicalSlug(i.item_name) !== slug && i.item_name.toLowerCase() !== itemName.toLowerCase());
          
          saveAppState();
          initSetupPanel();
          if (typeof render3DShoppingList === 'function') {
            render3DShoppingList();
          }
          if (typeof showToast === 'function') {
            showToast(`🗑️ Insumo '${itemName}' eliminado definitivamente de la Cosecha.`, 'danger');
          }
        }
      });
    }

    function deletePantryItem(itemName) {
      showClinicalConfirmModal({
        title: 'Eliminar Insumo del Inventario',
        message: `¿Estás seguro de que deseas eliminar definitivamente el insumo <strong>"${itemName}"</strong> del Inventario/Alacena?`,
        icon: '🗑️',
        confirmText: 'Sí, Eliminar Insumo',
        cancelText: 'Cancelar',
        onConfirm: () => {
          const slug = normalizeToCanonicalSlug(itemName);
          if (!deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === itemName.toLowerCase())) {
            deletedPantryItems.push(itemName);
          }
          rawShopBase = rawShopBase.filter(i => normalizeToCanonicalSlug(i.item_name) !== slug && i.item_name.toLowerCase() !== itemName.toLowerCase());
          
          Object.keys(pantryStock).forEach(k => {
            if (normalizeToCanonicalSlug(k) === slug || k.toLowerCase() === itemName.toLowerCase()) {
              delete pantryStock[k];
            }
          });

          if (typeof window.PANTRY_STOCK_INVENTORY === 'object' && window.PANTRY_STOCK_INVENTORY) {
            Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(k => {
              if (normalizeToCanonicalSlug(k) === slug || k.toLowerCase() === itemName.toLowerCase()) {
                delete window.PANTRY_STOCK_INVENTORY[k];
              }
            });
          }

          saveAppState();
          initSetupPanel();
          if (typeof render3DShoppingList === 'function') {
            render3DShoppingList();
          }
          if (typeof showToast === 'function') {
            showToast(`🗑️ Insumo '${itemName}' eliminado definitivamente del Inventario.`, 'danger');
          }
        }
      });
    }

    function saveAndUnlockApp() {
      activeWeek = document.getElementById('setup-week').value;
      activeDiners = parseInt(document.getElementById('setup-diners').value) || 6;
      
      saveAppState();

      document.getElementById('setup-overlay').style.display = 'none';
      document.getElementById('main-app-content').style.display = 'block';

      document.getElementById('active-diners-label').innerText = activeDiners;
      const headerWeekSelect = document.getElementById('header-week-select');
      if (headerWeekSelect) headerWeekSelect.value = activeWeek;
      document.getElementById('header-week-subtitle').innerText = `${activeWeek} | Ecosistema T.I.L.O.®`;

      renderDateBar();
      renderDay(selectedIdx);
      const curPlan1 = getPlanForWeek(activeWeek);
      if (typeof renderRecipes === 'function' && curPlan1 && curPlan1.days && curPlan1.days[selectedIdx]) {
        renderRecipes(curPlan1.days[selectedIdx], getMealDiners(selectedIdx, 'Desayuno'));
      }
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }
      if (typeof showToast === 'function') {
        showToast("🏛️ Arquitectura Semanal Compilada y Sincronizada.");
      }
    }

    function onHeaderWeekChange(newWeek) {
      const targetPlan = getPlanForWeek(newWeek);
      if (!targetPlan) return;
      activeWeek = newWeek;

      const setupWeekSelect = document.getElementById('setup-week');
      if (setupWeekSelect) setupWeekSelect.value = newWeek;

      const headerWeekSelect = document.getElementById('header-week-select');
      if (headerWeekSelect) headerWeekSelect.value = newWeek;

      const headerSubtitle = document.getElementById('header-week-subtitle');
      if (headerSubtitle) headerSubtitle.innerText = `${activeWeek} | Ecosistema T.I.L.O.®`;

      const btnNextWeekText = document.getElementById('btn-next-week-text');
      const btnNextWeek = document.getElementById('btn-next-week');
      if (btnNextWeekText) {
        if (newWeek.startsWith('Semana 42')) {
          btnNextWeekText.innerText = "📋 Semana 42 SSOT (Activa)";
          if (btnNextWeek) btnNextWeek.title = "Semana 42 SSOT Activa en el Atelier";
        } else {
          btnNextWeekText.innerText = "⚡ Generar Semana 42 SSOT";
          if (btnNextWeek) btnNextWeek.title = "Planificar y Cargar Semana 42 SSOT";
        }
      }

      if (typeof selectedIdx !== 'number' || isNaN(selectedIdx) || selectedIdx < 0 || (targetPlan.days && selectedIdx >= targetPlan.days.length)) {
        selectedIdx = 0;
      }

      saveAppState();

      renderDateBar();
      renderDay(selectedIdx);

      if (typeof renderRecipes === 'function' && targetPlan && targetPlan.days && targetPlan.days[selectedIdx]) {
        renderRecipes(targetPlan.days[selectedIdx], getMealDiners(selectedIdx, 'Desayuno'));
      }
      if (typeof render3DShoppingList === 'function') {
        render3DShoppingList();
      }

      if (typeof showToast === 'function') {
        showToast("📅 Semana cambiada a: " + activeWeek.split(' (')[0]);
      }
    }

    function reopenSetupPanel() {
      initSetupPanel();
      const setupOverlay = document.getElementById('setup-overlay');
      const editDetails = document.getElementById('edit-inventory-details');
      const mainContent = document.getElementById('main-app-content');

      if (setupOverlay) setupOverlay.style.display = 'block';
      if (editDetails) editDetails.style.display = 'block';
      if (mainContent) mainContent.style.display = 'none';
    }

    function getPlanForWeek(weekKey) {
      if (typeof datasets === 'undefined' || !datasets) return null;
      if (datasets[weekKey]) return datasets[weekKey];
      for (const k in datasets) {
        if (k.startsWith(weekKey) || (weekKey && weekKey.startsWith(k.split(' (')[0]))) {
          return datasets[k];
        }
      }
      return datasets["Semana 35 (23 al 29 de Agosto de 2026)"] || Object.values(datasets)[0] || null;
    }

    function isCalendarToday(dayObj, planObj) {
      if (!dayObj) return false;
      const now = new Date();
      const currentYear = now.getFullYear();
      const currentMonth = now.getMonth(); // 0-index (Sept=8, Oct=9)
      const currentDay = now.getDate();

      // 1. Coincidencia directa por iso_date estricta
      if (dayObj.iso_date && /^\\d{4}-\\d{2}-\\d{2}$/.test(dayObj.iso_date)) {
        const [y, m, d] = dayObj.iso_date.split('-').map(Number);
        return y === currentYear && (m - 1) === currentMonth && d === currentDay;
      }

      // 2. Extraer día numérico estricto (delimitado por límite de palabra, NUNCA .includes())
      let targetDay = null;
      if (dayObj.day_num !== undefined && dayObj.day_num !== null) {
        targetDay = parseInt(dayObj.day_num, 10);
      } else if (dayObj.date_str) {
        const matchDay = dayObj.date_str.match(/\\b0?(\\d{1,2})\\b/);
        if (matchDay) targetDay = parseInt(matchDay[1], 10);
      }
      if (!targetDay || isNaN(targetDay) || targetDay !== currentDay) {
        return false;
      }

      // 3. Extraer y validar mes en español
      const SPANISH_MONTH_MAP = {
        'ene': 0, 'enero': 0,
        'feb': 1, 'febrero': 1,
        'mar': 2, 'marzo': 2,
        'abr': 3, 'abril': 3,
        'may': 4, 'mayo': 4,
        'jun': 5, 'junio': 5,
        'jul': 6, 'julio': 6,
        'ago': 7, 'agosto': 7,
        'sep': 8, 'sept': 8, 'septiembre': 8,
        'oct': 9, 'octubre': 9,
        'nov': 10, 'noviembre': 10,
        'dic': 11, 'diciembre': 11
      };

      const cleanStr = (s) => (s || '').normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
      const dayClean = cleanStr(dayObj.date_str || '');
      let targetMonth = null;

      for (const [mName, mIdx] of Object.entries(SPANISH_MONTH_MAP)) {
        const reg = new RegExp(`\\b${mName}\\b`, 'i');
        if (reg.test(dayClean)) {
          targetMonth = mIdx;
          break;
        }
      }

      if (targetMonth === null) {
        const planClean = cleanStr(`${planObj?.week_label || ''} ${planObj?.date_range || ''}`);
        for (const [mName, mIdx] of Object.entries(SPANISH_MONTH_MAP)) {
          const reg = new RegExp(`\\b${mName}\\b`, 'i');
          if (reg.test(planClean)) {
            targetMonth = mIdx;
            break;
          }
        }
      }

      if (targetMonth === null || targetMonth !== currentMonth) {
        return false;
      }

      // 4. Extraer y validar año
      let targetYear = null;
      const combinedClean = cleanStr(`${dayObj.date_str || ''} ${planObj?.week_label || ''} ${planObj?.date_range || ''}`);
      const yearMatch = combinedClean.match(/\\b(202\\d)\\b/);
      if (yearMatch) {
        targetYear = parseInt(yearMatch[1], 10);
      }
      if (targetYear !== null && targetYear !== currentYear) {
        return false;
      }

      return true;
    }

    function renderDateBar() {
      try {
        const plan = getPlanForWeek(activeWeek);
        const bar = document.getElementById('date-bar');
        if (!bar) return;
        bar.innerHTML = '';
        bar.className = 'flex items-center gap-2 overflow-x-auto pb-3 mb-6 w-full';

        if (!plan || !plan.days) return;

        plan.days.forEach((day, idx) => {
          const btn = document.createElement('button');
          const isActive = idx === selectedIdx;
          const isToday = isCalendarToday(day, plan);
          
          btn.type = 'button';
          btn.className = `min-h-[48px] px-4 py-2.5 rounded-xl border text-xs font-brand-body flex items-center gap-2 transition-all cursor-pointer whitespace-nowrap ${
            isActive 
              ? 'bg-[#3AAA35] text-white shadow-md border-[#3AAA35] font-bold' 
              : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700'
          }`;
          
          const todayTag = isToday ? '<span class="text-[10px] uppercase font-bold text-[#FFCC00] bg-slate-900 px-1.5 py-0.5 rounded ml-1">HOY</span>' : '';
          
          let dayNumText = (day.day_num || (day.date_str ? day.date_str.split(' ')[0] : (idx + 1))).toString().trim().replace(/[\\s\\-_]+$/, '');
          let dayShortText = (day.day || '').substring(0, 3).toUpperCase().trim().replace(/[\\s\\-_]+$/, '');

          btn.innerHTML = `<span class="font-bold text-sm font-brand-title">${dayNumText}</span> <span class="font-semibold">${dayShortText}</span>${todayTag ? ' ' + todayTag : ''}`;
          
          btn.onclick = () => {
            selectedIdx = idx;
            renderDateBar();
            renderDay(idx);
          };
          bar.appendChild(btn);
        });
      } catch (e) {
        console.error("Error en renderDateBar:", e);
      }
    }

    let currentTab = 'menu';

    function switchTab(tabId, btn) {
      try {
        const map = {
          'design': 'v-menu',
          'menu': 'v-menu',
          'recipes': 'v-prep',
          'prep': 'v-prep',
          'supply': 'v-shop',
          'shop': 'v-shop',
          'metrics': 'v-nutri',
          'nutri': 'v-nutri'
        };
        const targetId = map[tabId] || (tabId && tabId.startsWith('v-') ? tabId : 'v-menu');
        currentTab = targetId.replace('v-', '');
        try {
          if (typeof sessionStorage !== 'undefined') {
            sessionStorage.setItem('nutriketo_active_tab', tabId);
          }
        } catch(e) {}

        document.querySelectorAll('.v-panel').forEach(el => el.style.display = 'none');
        const target = document.getElementById(targetId);
        if (target) target.style.display = 'block';

        document.querySelectorAll('.tab-btn').forEach(b => {
          b.classList.remove('bg-[#1C75BC]', 'text-white', 'border-[#1C75BC]');
          b.classList.add('bg-slate-100', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700');
        });

        const activeBtn = btn || document.getElementById(`tab-btn-${tabId}`);
        if (activeBtn) {
          activeBtn.classList.remove('bg-slate-100', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700');
          activeBtn.classList.add('bg-[#1C75BC]', 'text-white', 'border-[#1C75BC]');
        }

        if (targetId === 'v-shop' && typeof render3DShoppingList === 'function') {
          render3DShoppingList();
        }

        if (typeof updateExportButtonUI === 'function') updateExportButtonUI();
      } catch (e) {
        console.error("Error en switchTab:", e);
      }
    }

    function switchView(vId, btn) {
      switchTab(vId, btn);
    }

/**
 * Atelier T.I.L.O.® — Componente de Recetas 100% Pasivo SSOT (V15.22.1)
 * Renderizado Pasivo de Datos Estructurados sin Parsers Regex ni Plantillas Estáticas.
 * Escalamiento Unitario Estricto por Persona: (base_qty_per_person * activeDiners)
 */

function sanitizeDishTitle(title) {
  if (!title) return "";
  return title
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\\(.*?\\)/g, "")
    .trim();
}
function areInsumosEquivalent(aName, bName) {
      if (!aName || !bName) return false;
      const a = aName.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\bnuex\b/g, "nuez").trim();
      const b = bName.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\bnuex\b/g, "nuez").trim();

      if (a === b) return true;

      // Stems y alias canónicos con coincidencia léxica multi-categoría y discriminación estricta
      const itemKeywords = [
        // Carnes, Aves y Pescados
        { stem: 'pollo', aliases: ['pechuga de pollo', 'pechuga de pollo organica', 'pechuga', 'carne de pollo', 'pollo organico'], exclude: ['hueso', 'huesos', 'retazo', 'fondo', 'caldo'] },
        { stem: 'huesos-pollo', aliases: ['huesos y retazo de pollo', 'retazo de pollo', 'huesos de pollo', 'retazo de pollo organico'], exclude: ['pechuga'] },
        { stem: 'tuetano', aliases: ['tuetano', 'huesos de res con tuetano', 'huesos de res', 'carne para caldo rico', 'costilla tuetano'], exclude: ['arrachera', 'sirloin', 'machaca', 'filete de res'] },
        { stem: 'huevo', aliases: ['huevo', 'huevos', 'huevos enteros', 'huevos organicos', 'huevos frescos', 'huevos organicos de libre pastoreo', 'huevo entero'] },
        { stem: 'mantequilla', aliases: ['mantequilla', 'mantequilla de vaca', 'mantequilla de pastoreo', 'mantequilla de pastoreo artesanal', 'mantequilla sin sal'], exclude: ['ghee', 'clarificada'] },
        { stem: 'ghee', aliases: ['ghee', 'mantequilla clarificada'] },
        { stem: 'sirloin', aliases: ['sirloin', 'medallones de sirloin', 'medallon de sirloin', 'medallones de sirloin de res magro', 'carne molida de sirloin'], exclude: ['tuetano', 'huesos'] },
        { stem: 'arrachera', aliases: ['arrachera', 'arrachera de res', 'arrachera de res magra limpia', 'arrachera limpia'], exclude: ['tuetano', 'huesos'] },
        { stem: 'ribeye', aliases: ['ribeye', 'corte magro de ribeye', 'corte de ribeye', 'corte magro de ribeye de res premium', 'ribeye de res'] },
        { stem: 'mojarra', aliases: ['mojarra', 'fajita de mojarra', 'fajitas de mojarra', 'tilapia', 'fajita de tilapia', 'fajitas de mojarra tilapia'] },
        { stem: 'hamburguesa-arrachera', aliases: ['hamburguesa de arrachera', 'hamburguesas de arrachera', 'arrachburg'] },
        { stem: 'robalo', aliases: ['robalo', 'filete de robalo', 'filete de robalo salvaje', 'filete de robalo salvaje fresco de captura', 'pescado blanco', 'filete de pescado blanco'] },
        { stem: 'huachinango', aliases: ['huachinango', 'filetes de huachinango', 'filete de huachinango con piel'] },
        { stem: 'salmon', aliases: ['salmon', 'lomo de salmon', 'filete de salmon'] },
        { stem: 'atun', aliases: ['atun', 'medallones de atun', 'lomo de atun', 'atun enlatado', 'atun en lata', 'atunsuna'] },
        { stem: 'pavo', aliases: ['pavo', 'pechuga de pavo', 'pechuga de pavo artesanal'], exclude: ['tocino'] },
        { stem: 'tocino-pavo', aliases: ['tocino de pavo', 'tocino de pavo artesanal', 'tocino de pavo crujiente'] },
        { stem: 'machaca', aliases: ['machaca', 'carne seca machaca', 'carne seca machaca artesanal'] },
        // Lácteos y Quesos
        { stem: 'gouda', aliases: ['gouda', 'queso gouda', 'queso gouda artesanal'] },
        { stem: 'panela', aliases: ['panela', 'queso panela', 'queso panela artesanal'] },
        { stem: 'parmesano', aliases: ['parmesano', 'queso parmesano', 'queso parmesano artesanal'] },
        { stem: 'queso-crema', aliases: ['queso crema', 'queso crema suave', 'queso crema suave artesanal'] },
        { stem: 'cabra', aliases: ['queso de cabra', 'queso de cabra artesanal', 'cabra artesanal'] },
        { stem: 'ricotta', aliases: ['ricotta', 'queso ricotta', 'requeson'] },
        { stem: 'oikos', aliases: ['oikos', 'oikos pro', 'lacteo oikos', 'yoghurt oikos', 'yogurt oikos', 'oikos proteina'] },
        { stem: 'crema', aliases: ['crema', 'crema entera', 'crema entera de rancho', 'crema para batir', 'crema acida'], exclude: ['queso crema'] },
        // Grasas, Aceites y Semillas
        { stem: 'oliva', aliases: ['aceite de oliva', 'vevo', 'aceite de oliva extra virgen', 'aceite de oliva virgen extra', 'aceite de oliva extra virgen (vevo)'], exclude: ['aceituna', 'aceitunas'] },
        { stem: 'aceite-ajonjoli', aliases: ['aceite de ajonjoli', 'aceite de sesamo', 'aceite de ajonjoli tostado'], exclude: ['semilla', 'semillas', 'grano'] },
        { stem: 'semillas-sesamo', aliases: ['semillas de sesamo', 'semillas de ajonjoli', 'ajonjoli en grano', 'semilla de ajonjoli', 'semillas de sesamo (ajonjoli)'], exclude: ['aceite'] },
        { stem: 'nuez-pecana', aliases: ['nuez pecana', 'nueces pecana', 'nuex pecana', 'nuex', 'pecana', 'pecanas', 'nuez pecana fresca', 'nuez pecana de la granja', 'nuez pecana fresca de la granja', 'nueces pecanas', 'nuez pecana en mitades', 'nuez pecana pelada', 'nuez', 'nueces', 'nuez picada'] },
        { stem: 'nuez-castilla', aliases: ['nuez de castilla', 'nueces de castilla', 'nuez de castilla fresca'] },
        { stem: 'nuez-india', aliases: ['nuez de la india', 'nueces de la india', 'nuez india', 'nueces india', 'anacardo', 'anacardos', 'maranon'] },
        { stem: 'almendra', aliases: ['almendra', 'almendras', 'almendras fileteadas', 'almendras fileteadas tostadas'] },
        { stem: 'chia', aliases: ['chia', 'semillas de chia', 'semillas de chia organicas'] },
        { stem: 'girasol', aliases: ['semillas de girasol', 'semilla de girasol', 'girasol'] },
        { stem: 'coco-rallado', aliases: ['coco deshidratado', 'coco rallado', 'coco sin azucar'], exclude: ['leche de coco', 'aceite de coco'] },
        { stem: 'leche-coco', aliases: ['leche de coco'], exclude: ['deshidratado', 'rallado', 'aceite'] },
        // Frutas
        { stem: 'granada', aliases: ['granada', 'granadas', 'arilos'] },
        { stem: 'pitaya', aliases: ['pitaya', 'pitayas', 'pitahaya', 'pitahayas'] },
        { stem: 'fresa', aliases: ['fresa', 'fresas'] },
        { stem: 'frambuesa', aliases: ['frambuesa', 'frambuesas'] },
        { stem: 'zarzamora', aliases: ['zarzamora', 'zarzamoras'] },
        { stem: 'arandano', aliases: ['arandano', 'arandanos'] },
        { stem: 'mora', aliases: ['mora', 'moras'], exclude: ['morada'] },
        // Verduras
        { stem: 'espinaca', aliases: ['espinaca', 'espinacas', 'espinacas baby'] },
        { stem: 'calabacita', aliases: ['calabacita', 'calabacitas', 'calabaza', 'zucchini'], exclude: ['semilla', 'semillas', 'pepita', 'pepitas'] },
        { stem: 'semillas-calabaza', aliases: ['semillas de calabaza', 'semilla de calabaza', 'pepitas de calabaza', 'pepita de calabaza'], exclude: ['calabacita', 'calabacitas'] },
        { stem: 'brocoli', aliases: ['brocoli', 'brocolis'] },
        { stem: 'esparrago', aliases: ['esparrago', 'esparragos'] },
        { stem: 'nopal', aliases: ['nopal', 'nopales'] },
        { stem: 'ejote', aliases: ['ejote', 'ejotes'] },
        { stem: 'cilantro', aliases: ['cilantro'] },
        { stem: 'arugula', aliases: ['arugula'] },
        { stem: 'coliflor', aliases: ['coliflor'] },
        { stem: 'menta', aliases: ['menta'] },
        { stem: 'toronjil', aliases: ['toronjil'] },
        { stem: 'manzanilla', aliases: ['manzanilla'] },
        { stem: 'jamaica', aliases: ['jamaica'] },
        { stem: 'apio', aliases: ['apio'] },
        { stem: 'chayote', aliases: ['chayote', 'chayotes', 'chayote tierno', 'chayotes tiernos', 'chayotes tiernos pelados'] },
        { stem: 'hinojo', aliases: ['hinojo'] },
        { stem: 'aguacate', aliases: ['aguacate', 'aguacate hass'] },
        { stem: 'lechuga-sweet', aliases: ['lechuga sweet', 'sweet lettuce'] },
        { stem: 'limon', aliases: ['limon', 'limones', 'limones frescos', 'limon agrio', 'limones agrios', 'limones agrios frescos', 'limones agrios frescos de la granja', 'jugo de limon', 'jugo de limon fresco', 'jugo de limon fresco de la granja', 'jugo de limon recien exprimido', 'limon agrio fresco con semilla'] },
        { stem: 'ajo', aliases: ['ajo', 'ajos', 'ajo fresco', 'dientes de ajo'], exclude: ['ajonjoli'] },
        { stem: 'sal', aliases: ['sal de mar', 'sal de colima', 'sal mineral', 'sal de mar mineral de colima'] },
        { stem: 'agua-purificada', aliases: ['agua purificada', 'agua pura', 'botellas de agua purificada', 'botella de agua purificada'], exclude: ['mineral'] },
        { stem: 'agua-mineral', aliases: ['agua mineral', 'aguamin', 'botellas de agua mineral', 'botella de agua mineral'] },
        { stem: 'multisinergix', aliases: ['multisinergix', 'multi sinergix', '33plus', '33 plus', 'formula nootropica 33plus', 'formula biotecnologica nootropica 33plus', 'formula nootropica multisinergix'] },
        { stem: 'aminosinergix', aliases: ['aminosinergix', 'amino sinergix', '34plus', '34 plus', 'formula reparadora 34plus', 'formula biotecnologica reparadora 34plus', 'formula reparadora aminosinergix'] },
        { stem: 'flat-steak', aliases: ['flat steak', 'flatsteak', 'bife plano', 'steak flat'] },
        { stem: 'cottage', aliases: ['queso cottage', 'cottage'] },
        { stem: 'philadelphia', aliases: ['queso philadelphia', 'philadelphia', 'queso crema philadelphia'] },
        { stem: 'nogada', aliases: ['nogada'] },
        { stem: '33plus', aliases: ['33plus', 'formula nootropica 33plus', 'formula biotecnologica nootropica 33plus', 'multisinergix'] },
        { stem: '34plus', aliases: ['34plus', 'formula reparadora 34plus', 'formula biotecnologica reparadora 34plus', 'aminosinergix'] },
        { stem: 'grenetina', aliases: ['grenetina', 'grenetina natural', 'grenetina natural pura', 'colageno hidrolizado'] }
      ];

      for (const entry of itemKeywords) {
        if (entry.exclude && (entry.exclude.some(ex => a.includes(ex)) || entry.exclude.some(ex => b.includes(ex)))) {
          continue;
        }
        const aMatch = entry.aliases.some(alias => a.includes(alias));
        const bMatch = entry.aliases.some(alias => b.includes(alias));
        if (aMatch && bMatch) return true;
      }

      const slugA = normalizeToCanonicalSlug(aName);
      const slugB = normalizeToCanonicalSlug(bName);
      if (slugA && slugB && (slugA === slugB || slugA.includes(slugB) || slugB.includes(slugA))) return true;

      return false;
    }

window.PANTRY_STOCK_INVENTORY = {
      "sku-001-mantequilla": { item_num: 1, name: "Mantequilla", stock: 290, unit: "g", packaging: "290 g", status: "canonical" },
      "sku-002-mostaza": { item_num: 2, name: "Mostaza", stock: 150, unit: "g", packaging: "3 envases de 50 g", status: "canonical" },
      "sku-003-queso-cottage": { item_num: 3, name: "Queso cottage", stock: 2880, unit: "g", packaging: "3 envases de 960 g", status: "canonical" },
      "sku-004-yogur-griego": { item_num: 4, name: "Yogur griego", stock: 2880, unit: "g", packaging: "3 envases de 960 g", status: "canonical" },
      "sku-005-queso-philadelphia": { item_num: 5, name: "Queso Philadelphia", stock: 720, unit: "g", packaging: "4 envases de 180 g", status: "canonical" },
      "sku-006-crema-acida": { item_num: 6, name: "Crema ácida", stock: 960, unit: "g", packaging: "960 g", status: "canonical" },
      "sku-007-mayonesa": { item_num: 7, name: "Mayonesa", stock: 1000, unit: "g", packaging: "1000 g", status: "canonical" },
      "sku-008-queso-manchego": { item_num: 8, name: "Queso manchego", stock: 1200, unit: "g", packaging: "1200 g", status: "canonical" },
      "sku-009-queso-de-cabra": { item_num: 9, name: "Queso de cabra", stock: 500, unit: "g", packaging: "500 g", status: "canonical" },
      "sku-010-salsa-bbq": { item_num: 10, name: "Salsa BBQ", stock: 550, unit: "g", packaging: "550 g", status: "prohibited", reason: "Alta en azúcares libres y jarabe de maíz de alta fructosa; rompe cetosis." },
      "sku-011-leche-de-coco": { item_num: 11, name: "Leche de coco", stock: 960, unit: "ml", packaging: "960 ml", status: "canonical" },
      "sku-012-leche-evaporada": { item_num: 12, name: "Leche evaporada", stock: 960, unit: "ml", packaging: "960 ml", status: "prohibited", reason: "Alta concentración de lactosa y azúcares lácteos simples; rompe cetosis." },
      "sku-013-leche": { item_num: 13, name: "Leche", stock: 960, unit: "ml", packaging: "960 ml", status: "prohibited", reason: "Lactosa no cetogénica (~12g carbs netos por porción); eleva glucemia." },
      "sku-014-salsa-catsup": { item_num: 14, name: "Salsa cátsup", stock: 2600, unit: "g", packaging: "2 envases de 1300 g", status: "prohibited", reason: "Elevado aporte de azúcar añadida y jarabe de fructosa; fuera de protocolo keto." },
      "sku-015-queso-mozzarella": { item_num: 15, name: "Queso mozzarella", stock: 105, unit: "g", packaging: "105 g", status: "canonical" },
      "sku-016-nogada": { item_num: 16, name: "Nogada", stock: 960, unit: "ml", packaging: "960 ml", status: "prohibited", reason: "Preparación dulce tradicional con azúcar y leche condensada; rompe cetosis." },
      "sku-017-agua-mineral": { item_num: 17, name: "Agua mineral", stock: 6, unit: "botellas de 1500 ml", packaging: "6 botellas de 1500 ml", status: "canonical" },
      "sku-018-agua-mineral": { item_num: 18, name: "Agua mineral", stock: 1, unit: "botellas de 355 ml", packaging: "1 botella de 355 ml", status: "canonical" },
      "sku-019-botella-de-agua": { item_num: 19, name: "Botella de agua", stock: 120, unit: "botellas (355 ml)", packaging: "120 botellas de 355 ml", status: "canonical" },
      "sku-020-queso-parmesano": { item_num: 20, name: "Queso parmesano", stock: 100, unit: "g", packaging: "100 g", status: "canonical" },
      "sku-021-flat-steak": { item_num: 21, name: "Flat steak", stock: 940, unit: "g", packaging: "940 g", status: "canonical" },
      "sku-022-flat-steak": { item_num: 22, name: "Flat steak", stock: 945, unit: "g", packaging: "945 g", status: "canonical" },
      "sku-023-lomo-de-salmon": { item_num: 23, name: "Lomo de salmón", stock: 1385, unit: "g", packaging: "1385 g", status: "canonical" },
      "sku-024-carne-molida": { item_num: 24, name: "Carne molida", stock: 1680, unit: "g", packaging: "1680 g", status: "canonical" },
      "sku-025-fajitas-de-mojarra": { item_num: 25, name: "Fajitas de mojarra", stock: 907, unit: "g", packaging: "907 g", status: "canonical" },
      "sku-026-filete-de-atun": { item_num: 26, name: "Filete de atún", stock: 700, unit: "g", packaging: "700 g", status: "canonical" },
      "sku-027-jitomate": { item_num: 27, name: "Jitomate", stock: 9, unit: "piezas", packaging: "9 piezas", status: "canonical" },
      "sku-028-morron": { item_num: 28, name: "Morrón", stock: 7, unit: "piezas", packaging: "7 piezas", status: "canonical" },
      "sku-029-pechuga-de-pollo": { item_num: 29, name: "Pechuga de pollo", stock: 3, unit: "piezas", packaging: "3 piezas", status: "canonical" },
      "sku-030-zanahoria": { item_num: 30, name: "Zanahoria", stock: 7, unit: "piezas", packaging: "7 piezas", status: "prohibited", reason: "Tubérculo amiláceo con alto índice glucémico; fuera de protocolo cetogénico estricto." },
      "sku-031-flor-de-calabaza": { item_num: 31, name: "Flor de calabaza", stock: 1, unit: "manojo", packaging: "1 manojo", status: "canonical" },
      "sku-032-calabaza": { item_num: 32, name: "Calabaza", stock: 6, unit: "piezas", packaging: "6 piezas", status: "canonical" },
      "sku-033-cebolla": { item_num: 33, name: "Cebolla", stock: 9, unit: "piezas", packaging: "9 piezas", status: "canonical" },
      "sku-034-lechuga": { item_num: 34, name: "Lechuga", stock: 3, unit: "piezas", packaging: "3 piezas", status: "canonical" },
      "sku-035-ejotes": { item_num: 35, name: "Ejotes", stock: 500, unit: "g", packaging: "500 g", status: "canonical" },
      "sku-036-tomate": { item_num: 36, name: "Tomate", stock: 400, unit: "g", packaging: "400 g", status: "canonical" },
      "sku-037-elote": { item_num: 37, name: "Elote", stock: 2, unit: "piezas", packaging: "2 piezas", status: "prohibited", reason: "Grano entero amiláceo con altísima carga glucémica y carbohidratos netos." },
      "sku-038-aguacate": { item_num: 38, name: "Aguacate", stock: 13, unit: "piezas", packaging: "13 piezas", status: "canonical" },
      "sku-039-zarzamora": { item_num: 39, name: "Zarzamora", stock: 500, unit: "g", packaging: "500 g", status: "canonical" },
      "sku-040-champinon": { item_num: 40, name: "Champiñón", stock: 1000, unit: "g", packaging: "1000 g", status: "canonical" },
      "sku-041-pulpa-de-arandano": { item_num: 41, name: "Pulpa de arándano", stock: 3840, unit: "g", packaging: "4 envases de 960 g", status: "prohibited", reason: "Concentrado de fruta con azúcar añadida y alta fructosa; rompe cetosis." },
      "sku-042-pistaches": { item_num: 42, name: "Pistaches", stock: 100, unit: "g", packaging: "100 g", status: "canonical" },
      "sku-043-nuez-de-la-india": { item_num: 43, name: "Nuez de la India", stock: 100, unit: "g", packaging: "100 g", status: "canonical" },
      "sku-044-cacahuate-enchilado": { item_num: 44, name: "Cacahuate enchilado", stock: 1200, unit: "g", packaging: "1200 g", status: "prohibited", reason: "Leguminosa proinflamatoria con aceites refinados y almidón en cobertura." },
      "sku-045-semillas-y-nueces-mixtas": { item_num: 45, name: "Semillas y nueces mixtas", stock: 960, unit: "g", packaging: "960 g", status: "canonical" },
      "sku-046-granola": { item_num: 46, name: "Granola", stock: 100, unit: "g", packaging: "100 g", status: "prohibited", reason: "Mezcla de avena, miel y azúcares refinados; alto impacto insulínico." },
      "sku-047-te-chai": { item_num: 47, name: "Té chai", stock: 70, unit: "g", packaging: "70 g", status: "canonical" },
      "sku-048-hierbas-finas": { item_num: 48, name: "Hierbas finas", stock: 25, unit: "g", packaging: "25 g", status: "canonical" },
      "sku-049-harina-de-trigo": { item_num: 49, name: "Harina de trigo", stock: 1500, unit: "g", packaging: "1500 g", status: "prohibited", reason: "Cereal refinado con gluten y altísima carga amilácea; rompe cetosis." },
      "sku-050-harina-para-hot-cakes": { item_num: 50, name: "Harina para hot cakes", stock: 500, unit: "g", packaging: "500 g", status: "prohibited", reason: "Harina procesada con azúcares añadidos, dextrosa y leudantes glucémicos." },
      "sku-051-cebolla-en-polvo": { item_num: 51, name: "Cebolla en polvo", stock: 50, unit: "g", packaging: "50 g", status: "canonical" },
      "sku-052-sal-con-ajo": { item_num: 52, name: "Sal con ajo", stock: 100, unit: "g", packaging: "100 g", status: "canonical" },
      "sku-053-canela-molida": { item_num: 53, name: "Canela molida", stock: 750, unit: "g", packaging: "3 envases de 250 g", status: "canonical" },
      "sku-054-alcaparras": { item_num: 54, name: "Alcaparras", stock: 200, unit: "g", packaging: "2 envases de 100 g", status: "canonical" },
      "sku-055-extracto-de-vainilla": { item_num: 55, name: "Extracto de vainilla", stock: 400, unit: "ml", packaging: "2 envases de 200 ml", status: "canonical" },
      "sku-056-microdyn": { item_num: 56, name: "Microdyn", stock: 200, unit: "ml", packaging: "2 envases de 100 ml", status: "canonical" },
      "sku-057-cerezas": { item_num: 57, name: "Cerezas", stock: 260, unit: "g", packaging: "260 g", status: "prohibited", reason: "Fruta con alto contenido de fructosa y azúcares simples; proscrita en inducción keto." },
      "sku-058-tajin": { item_num: 58, name: "Tajín", stock: 200, unit: "g", packaging: "2 envases de 100 g", status: "canonical" },
      "sku-059-miguelito": { item_num: 59, name: "Miguelito", stock: 100, unit: "g", packaging: "100 g", status: "prohibited", reason: "Dulce en polvo compuesto por azúcar pura y chile; eleva glucosa de inmediato." },
      "sku-060-chamoy": { item_num: 60, name: "Chamoy", stock: 300, unit: "ml", packaging: "300 ml", status: "prohibited", reason: "Salsa agridulce ultraprocesada con azúcar, almidón y jarabe de maíz." },
      "sku-061-bicarbonato-de-sodio": { item_num: 61, name: "Bicarbonato de sodio", stock: 227, unit: "g", packaging: "227 g", status: "canonical" },
      "sku-062-achiote": { item_num: 62, name: "Achiote", stock: 110, unit: "g", packaging: "110 g", status: "canonical" },
      "sku-063-polvo-para-hornear": { item_num: 63, name: "Polvo para hornear", stock: 100, unit: "g", packaging: "100 g", status: "canonical" },
      "sku-064-aceitunas-manzanilla": { item_num: 64, name: "Aceitunas manzanilla", stock: 175, unit: "g", packaging: "175 g", status: "canonical" },
      "sku-065-chocolate-para-cobertura": { item_num: 65, name: "Chocolate para cobertura", stock: 165, unit: "g", packaging: "165 g", status: "prohibited", reason: "Chocolate comercial con alto contenido de sacarosa y grasas vegetales hidrogenadas." },
      "sku-066-concentrado-de-caldo-de-pollo-en-polvo": { item_num: 66, name: "Concentrado de caldo de pollo en polvo", stock: 250, unit: "g", packaging: "250 g", status: "prohibited", reason: "Sazonador industrial con maltodextrina, glutamato monosódico y almidones." },
      "sku-067-cafe-colombiano": { item_num: 67, name: "Café colombiano", stock: 100, unit: "g", packaging: "100 g", status: "canonical" },
      "sku-068-vinagre-balsamico": { item_num: 68, name: "Vinagre balsámico", stock: 200, unit: "ml", packaging: "2 envases de 100 ml", status: "prohibited", reason: "Vinagre con reducción de mosto concentrado en azúcares simples residuales." },
      "sku-069-jugo-maggi": { item_num: 69, name: "Jugo Maggi", stock: 200, unit: "ml", packaging: "200 ml", status: "prohibited", reason: "Ultraprocesado con trigo hidrolizado, colorante caramelo y glutamato monosódico." },
      "sku-070-salsa-inglesa": { item_num: 70, name: "Salsa inglesa", stock: 200, unit: "ml", packaging: "200 ml", status: "canonical" },
      "sku-071-salsa-de-soya": { item_num: 71, name: "Salsa de soya", stock: 250, unit: "ml", packaging: "250 ml", status: "canonical" },
      "sku-072-vinagre-de-vino-tinto": { item_num: 72, name: "Vinagre de vino tinto", stock: 250, unit: "ml", packaging: "250 ml", status: "canonical" },
      "sku-073-aceite-de-oliva": { item_num: 73, name: "Aceite de oliva", stock: 400, unit: "ml", packaging: "400 ml", status: "canonical" },
      "sku-074-flor-de-jamaica-molida-en-polvo": { item_num: 74, name: "Flor de Jamaica molida en polvo", stock: 200, unit: "g", packaging: "200 g", status: "canonical" },
      "sku-075-almendras-fileteadas": { item_num: 75, name: "Almendras fileteadas", stock: 200, unit: "g", packaging: "200 g", status: "canonical" },
      "sku-076-hojas-de-laurel": { item_num: 76, name: "Hojas de laurel", stock: 20, unit: "g", packaging: "20 g", status: "canonical" },
      "sku-077-oregano-delgado": { item_num: 77, name: "Orégano delgado", stock: 50, unit: "g", packaging: "50 g", status: "canonical" },
      "sku-078-oregano-grueso": { item_num: 78, name: "Orégano grueso", stock: 100, unit: "g", packaging: "100 g", status: "canonical" },
      "sku-079-tomillo": { item_num: 79, name: "Tomillo", stock: 20, unit: "g", packaging: "20 g", status: "canonical" },
      "sku-080-pimienta-negra": { item_num: 80, name: "Pimienta negra", stock: 50, unit: "g", packaging: "50 g", status: "canonical" },
      "sku-081-comino": { item_num: 81, name: "Comino", stock: 50, unit: "g", packaging: "50 g", status: "canonical" },
      "sku-082-clavo-de-olor": { item_num: 82, name: "Clavo de olor", stock: 50, unit: "g", packaging: "50 g", status: "canonical" },
      "sku-083-pimienta-molida": { item_num: 83, name: "Pimienta molida", stock: 20, unit: "g", packaging: "20 g", status: "canonical" },
      "sku-084-ajonjoli": { item_num: 84, name: "Ajonjolí", stock: 50, unit: "g", packaging: "50 g", status: "canonical" },
      "sku-085-manzanilla": { item_num: 85, name: "Manzanilla", stock: 50, unit: "g", packaging: "50 g", status: "canonical" },
      "sku-086-curcuma": { item_num: 86, name: "Cúrcuma", stock: 100, unit: "g", packaging: "100 g", status: "canonical" },
      "sku-087-sal-marina-de-grano": { item_num: 87, name: "Sal marina de grano", stock: 2000, unit: "g", packaging: "2000 g", status: "canonical" },
      "sku-088-sal-fina": { item_num: 88, name: "Sal fina", stock: 1000, unit: "g", packaging: "1000 g", status: "canonical" },
      "sku-089-manteca-de-cerdo": { item_num: 89, name: "Manteca de cerdo", stock: 500, unit: "g", packaging: "500 g", status: "canonical" },
      "sku-090-aceite-de-coco": { item_num: 90, name: "Aceite de coco", stock: 500, unit: "g", packaging: "500 g", status: "canonical" },
      "sku-091-tang": { item_num: 91, name: "Tang", stock: 104, unit: "g", packaging: "8 envases de 13 g", status: "prohibited", reason: "Polvo industrial para bebidas con azúcar y aditivos sintéticos no cetogénicos." },
      "sku-092-atun-en-agua": { item_num: 92, name: "Atún en agua", stock: 700, unit: "g", packaging: "7 envases de 100 g", status: "canonical" },
      "sku-093-sardina-en-salsa-de-tomate": { item_num: 93, name: "Sardina en salsa de tomate", stock: 1700, unit: "g", packaging: "4 envases de 425 g", status: "canonical" },
      "sku-094-rajas-de-jalapeno": { item_num: 94, name: "Rajas de jalapeño", stock: 314, unit: "g", packaging: "2 envases de 157 g", status: "canonical" },
      "sku-095-harina-power-cakes": { item_num: 95, name: "Harina Power Cakes", stock: 1000, unit: "g", packaging: "1000 g", status: "prohibited", reason: "Mezcla para panqueques con carbohidratos de rápida absorción; fuera de cetosis." },
      "sku-096-hojuelas-de-avena": { item_num: 96, name: "Hojuelas de avena", stock: 100, unit: "g", packaging: "100 g", status: "prohibited", reason: "Cereal alto en carbohidratos netos y almidones; rompe cetosis." },
      "sku-097-maiz-palomero": { item_num: 97, name: "Maíz palomero", stock: 100, unit: "g", packaging: "100 g", status: "prohibited", reason: "Grano de maíz entero con elevada carga glucémica amilácea." },
      "sku-098-lentejas": { item_num: 98, name: "Lentejas", stock: 100, unit: "g", packaging: "100 g", status: "prohibited", reason: "Leguminosa alta en carbohidratos netos y lectinas; rompe cetosis." },
      "sku-099-quinoa": { item_num: 99, name: "Quinoa", stock: 100, unit: "g", packaging: "100 g", status: "prohibited", reason: "Pseudocereal amiláceo con elevada carga de carbohidratos netos." },
      "sku-100-chile-g-ero": { item_num: 100, name: "Chile güero", stock: 840, unit: "g", packaging: "840 g", status: "canonical" },
      "sku-101-palomitas-para-microondas": { item_num: 101, name: "Palomitas para microondas", stock: 600, unit: "g", packaging: "6 envases de 100 g", status: "prohibited", reason: "Maíz procesado con grasas de palma y carbohidratos de alto impacto glucémico." },
      "sku-102-grenetina": { item_num: 102, name: "Grenetina", stock: 112, unit: "g", packaging: "4 envases de 28 g", status: "canonical" },
      "sku-103-saborizante-para-arroz": { item_num: 103, name: "Saborizante para arroz", stock: 48, unit: "g", packaging: "4 envases de 12 g", status: "prohibited", reason: "Sazonador industrial con maltodextrina y almidones para cereales." },
      "sku-104-huevo": { item_num: 104, name: "Huevo", stock: 105, unit: "piezas", packaging: "105 piezas", status: "canonical" },
      "sku-105-multisinergix": { item_num: 105, name: "MultiSinergix®", stock: 300, unit: "g", packaging: "300 g", status: "canonical" },
      "sku-106-aminosinergix": { item_num: 106, name: "AminoSinergix®", stock: 200, unit: "g", packaging: "200 g", status: "canonical" },
      "zarzamoras-frescas": { name: "Zarzamora", stock: 500, unit: "g", status: "canonical" },
      "fresas-frescas": { name: "Fresas frescas", stock: 0, unit: "g", status: "canonical" },
      "arilos-granada": { name: "Arilos de granada fresca", stock: 0, unit: "g", status: "canonical" },
      "moras-frescas": { name: "Moras frescas", stock: 0, unit: "g", status: "canonical" },
      "frambuesas-frescas": { name: "Frambuesas frescas orgánicas", stock: 0, unit: "g", status: "canonical" },
      "arandanos-frescos": { name: "Arándanos frescos", stock: 0, unit: "g", status: "canonical" },
      "pitaya-fresca": { name: "Pitaya fresca", stock: 0, unit: "g", status: "canonical" },
      "multisinergix": { name: "MultiSinergix®", stock: 300, unit: "g", status: "canonical" },
      "aminosinergix": { name: "AminoSinergix®", stock: 200, unit: "g", status: "canonical" },
      "33plus": { name: "MultiSinergix®", stock: 300, unit: "g", status: "canonical" },
      "34plus": { name: "AminoSinergix®", stock: 200, unit: "g", status: "canonical" },
      "ajo-fresco": { name: "Ajo fresco", stock: 0, unit: "g", status: "canonical" }
    };

const ingredientsBOM = [{"name":"Fresas frescas","item_name":"Fresas frescas","quantity":300,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Semillas de chía orgánicas","item_name":"Semillas de chía orgánicas","quantity":48,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Almendras fileteadas tostadas","item_name":"Almendras fileteadas tostadas","quantity":90,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Chayotes tiernos","item_name":"Chayotes tiernos","quantity":1,"unit":"piezas","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":90,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Cebollín fresco de la granja","item_name":"Cebollín fresco de la granja","quantity":30,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Fresas frescas","item_name":"Fresas frescas","quantity":120,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Grenetina natural en polvo","item_name":"Grenetina natural en polvo","quantity":42,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Hojas de menta fresca","item_name":"Hojas de menta fresca","quantity":15,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fresas frescas","item_name":"Fresas frescas","quantity":120,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Grenetina natural en polvo","item_name":"Grenetina natural en polvo","quantity":42,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Hojas de menta fresca","item_name":"Hojas de menta fresca","quantity":15,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Chayotes tiernos","item_name":"Chayotes tiernos","quantity":1,"unit":"piezas","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":90,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Cebollín fresco de la granja","item_name":"Cebollín fresco de la granja","quantity":30,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Calabacitas verdes tiernas de la granja","item_name":"Calabacitas verdes tiernas de la granja","quantity":600,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":18,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":60,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Fondo claro de pollo casero","item_name":"Fondo claro de pollo casero","quantity":480,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Corte magro de Ribeye de res premium","item_name":"Corte magro de Ribeye de res premium","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":80,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Romero fresco","item_name":"Romero fresco","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Ajo fresco machacado","item_name":"Ajo fresco machacado","quantity":12,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Espárragos verdes frescos de la granja","item_name":"Espárragos verdes frescos de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Parmesano artesanal","item_name":"Queso Parmesano artesanal","quantity":60,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":25,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Espárragos verdes frescos de la granja","item_name":"Espárragos verdes frescos de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Parmesano artesanal","item_name":"Queso Parmesano artesanal","quantity":60,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":25,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Corte magro de Ribeye de res premium","item_name":"Corte magro de Ribeye de res premium","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":80,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Romero fresco","item_name":"Romero fresco","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Ajo fresco machacado","item_name":"Ajo fresco machacado","quantity":12,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Caldo concentrado y fondo de res casero","item_name":"Caldo concentrado y fondo de res casero","quantity":600,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Cilantro fresco de la granja","item_name":"Cilantro fresco de la granja","quantity":24,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":30,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sardinas enlatadas","item_name":"Sardinas enlatadas","quantity":1,"unit":"latas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Tomate verde fresco","item_name":"Tomate verde fresco","quantity":360,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":2,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":60,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de manzanilla seca","item_name":"Flores de manzanilla seca","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de azahar","item_name":"Flores de azahar","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de manzanilla seca","item_name":"Flores de manzanilla seca","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de azahar","item_name":"Flores de azahar","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sardinas enlatadas","item_name":"Sardinas enlatadas","quantity":1,"unit":"latas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Tomate verde fresco","item_name":"Tomate verde fresco","quantity":360,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":2,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":60,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Yoghurt griego natural sin azúcar","item_name":"Yoghurt griego natural sin azúcar","quantity":300,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Semillas de chía orgánicas","item_name":"Semillas de chía orgánicas","quantity":48,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Nueces de Castilla","item_name":"Nueces de Castilla","quantity":90,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Espinacas frescas de la granja","item_name":"Espinacas frescas de la granja","quantity":240,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Gouda artesanal","item_name":"Queso Gouda artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":70,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Té verde Sencha en hebras","item_name":"Té verde Sencha en hebras","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Té verde Sencha en hebras","item_name":"Té verde Sencha en hebras","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Espinacas frescas de la granja","item_name":"Espinacas frescas de la granja","quantity":240,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Gouda artesanal","item_name":"Queso Gouda artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":70,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Coliflor fresca de la granja","item_name":"Coliflor fresca de la granja","quantity":600,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":18,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":50,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Fondo claro de pollo casero","item_name":"Fondo claro de pollo casero","quantity":480,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Filete de Salmón fresco con piel","item_name":"Filete de Salmón fresco con piel","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Semillas de sésamo","item_name":"Semillas de sésamo","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Mayonesa","item_name":"Mayonesa","quantity":150,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Eneldo fresco","item_name":"Eneldo fresco","quantity":15,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":25,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Ejotes verdes tiernos de la granja","item_name":"Ejotes verdes tiernos de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":50,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Almendras fileteadas tostadas","item_name":"Almendras fileteadas tostadas","quantity":45,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Ejotes verdes tiernos de la granja","item_name":"Ejotes verdes tiernos de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":50,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Almendras fileteadas tostadas","item_name":"Almendras fileteadas tostadas","quantity":45,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Filete de Salmón fresco con piel","item_name":"Filete de Salmón fresco con piel","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Semillas de sésamo","item_name":"Semillas de sésamo","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Mayonesa","item_name":"Mayonesa","quantity":150,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Eneldo fresco","item_name":"Eneldo fresco","quantity":15,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":25,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Pepino fresco de la granja","item_name":"Pepino fresco de la granja","quantity":360,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Rábanos frescos de la huerta","item_name":"Rábanos frescos de la huerta","quantity":120,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":20,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Filete de Robalo fresco","item_name":"Filete de Robalo fresco","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Almendras fileteadas tostadas","item_name":"Almendras fileteadas tostadas","quantity":90,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Eneldo fresco","item_name":"Eneldo fresco","quantity":15,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":20,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de toronjil fresco","item_name":"Hojas de toronjil fresco","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de toronjil fresco","item_name":"Hojas de toronjil fresco","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Filete de Robalo fresco","item_name":"Filete de Robalo fresco","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Almendras fileteadas tostadas","item_name":"Almendras fileteadas tostadas","quantity":90,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Eneldo fresco","item_name":"Eneldo fresco","quantity":15,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":20,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Moras frescas","item_name":"Moras frescas","quantity":300,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Semillas de girasol tostadas","item_name":"Semillas de girasol tostadas","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Semillas de chía orgánicas","item_name":"Semillas de chía orgánicas","quantity":30,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Yoghurt griego natural sin azúcar","item_name":"Yoghurt griego natural sin azúcar","quantity":300,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":90,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":12,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Pimentón dulce en polvo","item_name":"Pimentón dulce en polvo","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Frambuesas frescas orgánicas","item_name":"Frambuesas frescas orgánicas","quantity":120,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Grenetina natural en polvo","item_name":"Grenetina natural en polvo","quantity":42,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Frambuesas frescas orgánicas","item_name":"Frambuesas frescas orgánicas","quantity":120,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Grenetina natural en polvo","item_name":"Grenetina natural en polvo","quantity":42,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Yoghurt griego natural sin azúcar","item_name":"Yoghurt griego natural sin azúcar","quantity":300,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":90,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":12,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Pimentón dulce en polvo","item_name":"Pimentón dulce en polvo","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Caldo concentrado y fondo de res casero","item_name":"Caldo concentrado y fondo de res casero","quantity":600,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":120,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":15,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Carne molida / Filete de Sirloin magro","item_name":"Carne molida / Filete de Sirloin magro","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Leche de coco","item_name":"Leche de coco","quantity":250,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":50,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Pimienta negra recién molida","item_name":"Pimienta negra recién molida","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Brócoli fresco de la granja","item_name":"Brócoli fresco de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Gouda artesanal","item_name":"Queso Gouda artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":40,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Brócoli fresco de la granja","item_name":"Brócoli fresco de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Gouda artesanal","item_name":"Queso Gouda artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":40,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Carne molida / Filete de Sirloin magro","item_name":"Carne molida / Filete de Sirloin magro","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Leche de coco","item_name":"Leche de coco","quantity":250,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":50,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Pimienta negra recién molida","item_name":"Pimienta negra recién molida","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de arúgula fresca","item_name":"Hojas de arúgula fresca","quantity":180,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":15,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":3,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Pechuga de pavo artesanal","item_name":"Pechuga de pavo artesanal","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mayonesa","item_name":"Mayonesa","quantity":150,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":2,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":100,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Cilantro fresco de la granja","item_name":"Cilantro fresco de la granja","quantity":20,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":30,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de manzanilla seca","item_name":"Flores de manzanilla seca","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de manzanilla seca","item_name":"Flores de manzanilla seca","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Pechuga de pavo artesanal","item_name":"Pechuga de pavo artesanal","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mayonesa","item_name":"Mayonesa","quantity":150,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":2,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":100,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Cilantro fresco de la granja","item_name":"Cilantro fresco de la granja","quantity":20,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":30,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fresas frescas","item_name":"Fresas frescas","quantity":300,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Semillas de chía orgánicas","item_name":"Semillas de chía orgánicas","quantity":48,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Almendras fileteadas tostadas","item_name":"Almendras fileteadas tostadas","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Espárragos verdes frescos de la granja","item_name":"Espárragos verdes frescos de la granja","quantity":360,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":50,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":40,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Té matcha ceremonial en polvo","item_name":"Té matcha ceremonial en polvo","quantity":12,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Té matcha ceremonial en polvo","item_name":"Té matcha ceremonial en polvo","quantity":12,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Espárragos verdes frescos de la granja","item_name":"Espárragos verdes frescos de la granja","quantity":360,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":50,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":40,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fondo claro de pollo casero","item_name":"Fondo claro de pollo casero","quantity":600,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Calabacitas verdes tiernas de la granja","item_name":"Calabacitas verdes tiernas de la granja","quantity":240,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Apio fresco de la granja","item_name":"Apio fresco de la granja","quantity":120,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":25,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Orégano seco","item_name":"Orégano seco","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Pechuga de pollo orgánica","item_name":"Pechuga de pollo orgánica","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Jitomate Saladet fresco","item_name":"Jitomate Saladet fresco","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":70,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Romero fresco","item_name":"Romero fresco","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":30,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Nopales tiernos limpios de la granja","item_name":"Nopales tiernos limpios de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Panela artesanal","item_name":"Queso Panela artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":25,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Orégano seco","item_name":"Orégano seco","quantity":5,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Nopales tiernos limpios de la granja","item_name":"Nopales tiernos limpios de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Panela artesanal","item_name":"Queso Panela artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":25,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Orégano seco","item_name":"Orégano seco","quantity":5,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Pechuga de pollo orgánica","item_name":"Pechuga de pollo orgánica","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Jitomate Saladet fresco","item_name":"Jitomate Saladet fresco","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":70,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Romero fresco","item_name":"Romero fresco","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":30,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fondo claro de pollo casero","item_name":"Fondo claro de pollo casero","quantity":600,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Tomillo fresco","item_name":"Tomillo fresco","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":20,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sardinas enlatadas","item_name":"Sardinas enlatadas","quantity":1,"unit":"latas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Hojas de lechuga orejona viva","item_name":"Hojas de lechuga orejona viva","quantity":240,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Tomate verde fresco","item_name":"Tomate verde fresco","quantity":360,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":2,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":80,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":25,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de lavanda secas","item_name":"Flores de lavanda secas","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de azahar","item_name":"Flores de azahar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de lavanda secas","item_name":"Flores de lavanda secas","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de azahar","item_name":"Flores de azahar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sardinas enlatadas","item_name":"Sardinas enlatadas","quantity":1,"unit":"latas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Hojas de lechuga orejona viva","item_name":"Hojas de lechuga orejona viva","quantity":240,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Tomate verde fresco","item_name":"Tomate verde fresco","quantity":360,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":2,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":80,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":25,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Yoghurt griego natural sin azúcar","item_name":"Yoghurt griego natural sin azúcar","quantity":300,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Semillas de chía orgánicas","item_name":"Semillas de chía orgánicas","quantity":48,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Nueces de Castilla","item_name":"Nueces de Castilla","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Canela en polvo","item_name":"Canela en polvo","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Carne seca machaca artesanal de res","item_name":"Carne seca machaca artesanal de res","quantity":180,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":120,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":80,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Moras frescas","item_name":"Moras frescas","quantity":120,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Grenetina natural en polvo","item_name":"Grenetina natural en polvo","quantity":42,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Moras frescas","item_name":"Moras frescas","quantity":120,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Grenetina natural en polvo","item_name":"Grenetina natural en polvo","quantity":42,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Carne seca machaca artesanal de res","item_name":"Carne seca machaca artesanal de res","quantity":180,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":120,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":80,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Chayotes tiernos","item_name":"Chayotes tiernos","quantity":1,"unit":"piezas","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Cebollín fresco de la granja","item_name":"Cebollín fresco de la granja","quantity":80,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":40,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Fondo claro de pollo casero","item_name":"Fondo claro de pollo casero","quantity":480,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Corte magro de Arrachera de res","item_name":"Corte magro de Arrachera de res","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":70,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":15,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Cilantro fresco de la granja","item_name":"Cilantro fresco de la granja","quantity":30,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Vinagre de manzana o balsámico","item_name":"Vinagre de manzana o balsámico","quantity":15,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Calabacitas verdes tiernas de la granja","item_name":"Calabacitas verdes tiernas de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Parmesano artesanal","item_name":"Queso Parmesano artesanal","quantity":60,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Calabacitas verdes tiernas de la granja","item_name":"Calabacitas verdes tiernas de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Parmesano artesanal","item_name":"Queso Parmesano artesanal","quantity":60,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Corte magro de Arrachera de res","item_name":"Corte magro de Arrachera de res","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":70,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":15,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Cilantro fresco de la granja","item_name":"Cilantro fresco de la granja","quantity":30,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Vinagre de manzana o balsámico","item_name":"Vinagre de manzana o balsámico","quantity":15,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de arúgula fresca","item_name":"Hojas de arúgula fresca","quantity":180,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Pepino fresco de la granja","item_name":"Pepino fresco de la granja","quantity":240,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":25,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":15,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":3,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Pechuga de pavo artesanal","item_name":"Pechuga de pavo artesanal","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Leche de coco","item_name":"Leche de coco","quantity":250,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":80,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":50,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Curry suave en polvo / Cúrcuma","item_name":"Curry suave en polvo / Cúrcuma","quantity":12,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de menta fresca","item_name":"Hojas de menta fresca","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de toronjil fresco","item_name":"Hojas de toronjil fresco","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de menta fresca","item_name":"Hojas de menta fresca","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de toronjil fresco","item_name":"Hojas de toronjil fresco","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Pechuga de pavo artesanal","item_name":"Pechuga de pavo artesanal","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Leche de coco","item_name":"Leche de coco","quantity":250,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebolla blanca fresca","item_name":"Cebolla blanca fresca","quantity":80,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":50,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Curry suave en polvo / Cúrcuma","item_name":"Curry suave en polvo / Cúrcuma","quantity":12,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Frambuesas frescas orgánicas","item_name":"Frambuesas frescas orgánicas","quantity":300,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Semillas de calabaza tostadas","item_name":"Semillas de calabaza tostadas","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Semillas de chía orgánicas","item_name":"Semillas de chía orgánicas","quantity":30,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Queso Panela artesanal","item_name":"Queso Panela artesanal","quantity":180,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":80,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebollín fresco de la granja","item_name":"Cebollín fresco de la granja","quantity":25,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Té verde Sencha en hebras","item_name":"Té verde Sencha en hebras","quantity":15,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Té verde Sencha en hebras","item_name":"Té verde Sencha en hebras","quantity":15,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Queso Panela artesanal","item_name":"Queso Panela artesanal","quantity":180,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":80,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Cebollín fresco de la granja","item_name":"Cebollín fresco de la granja","quantity":25,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fondo claro de pollo casero","item_name":"Fondo claro de pollo casero","quantity":600,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Cilantro fresco de la granja","item_name":"Cilantro fresco de la granja","quantity":20,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":25,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Medallón de Atún fresco","item_name":"Medallón de Atún fresco","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Semillas de sésamo","item_name":"Semillas de sésamo","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":3,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":30,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Cilantro fresco de la granja","item_name":"Cilantro fresco de la granja","quantity":20,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Espárragos verdes frescos de la granja","item_name":"Espárragos verdes frescos de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":50,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Espárragos verdes frescos de la granja","item_name":"Espárragos verdes frescos de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":50,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Medallón de Atún fresco","item_name":"Medallón de Atún fresco","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Semillas de sésamo","item_name":"Semillas de sésamo","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":3,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":30,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Cilantro fresco de la granja","item_name":"Cilantro fresco de la granja","quantity":20,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":30,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":8,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jitomate Saladet fresco","item_name":"Jitomate Saladet fresco","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Pepino fresco de la granja","item_name":"Pepino fresco de la granja","quantity":180,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":50,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Vinagre de manzana o balsámico","item_name":"Vinagre de manzana o balsámico","quantity":15,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Pechuga de pollo orgánica","item_name":"Pechuga de pollo orgánica","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mayonesa","item_name":"Mayonesa","quantity":150,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":2,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":10,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":40,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":20,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de manzanilla seca","item_name":"Flores de manzanilla seca","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de toronjil fresco","item_name":"Hojas de toronjil fresco","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de manzanilla seca","item_name":"Flores de manzanilla seca","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Hojas de toronjil fresco","item_name":"Hojas de toronjil fresco","quantity":10,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Pechuga de pollo orgánica","item_name":"Pechuga de pollo orgánica","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mayonesa","item_name":"Mayonesa","quantity":150,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Aguacate Hass fresco","item_name":"Aguacate Hass fresco","quantity":2,"unit":"piezas","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":10,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":40,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":20,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fresas frescas","item_name":"Fresas frescas","quantity":180,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Moras frescas","item_name":"Moras frescas","quantity":120,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Semillas de chía orgánicas","item_name":"Semillas de chía orgánicas","quantity":48,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Nueces de Castilla","item_name":"Nueces de Castilla","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Espinacas frescas de la granja","item_name":"Espinacas frescas de la granja","quantity":240,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Jitomate Saladet fresco","item_name":"Jitomate Saladet fresco","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso de cabra suave artesanal","item_name":"Queso de cabra suave artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Moras frescas","item_name":"Moras frescas","quantity":60,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Fresas frescas","item_name":"Fresas frescas","quantity":60,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Grenetina natural en polvo","item_name":"Grenetina natural en polvo","quantity":42,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Moras frescas","item_name":"Moras frescas","quantity":60,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Fresas frescas","item_name":"Fresas frescas","quantity":60,"unit":"g","category":"🍓 Frutas de Bajo Índice Glucémico"},{"name":"Grenetina natural en polvo","item_name":"Grenetina natural en polvo","quantity":42,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Fórmula Nootrópica 33Plus®","item_name":"Fórmula Nootrópica 33Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":720,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Huevos orgánicos de pastoreo","item_name":"Huevos orgánicos de pastoreo","quantity":18,"unit":"piezas","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Espinacas frescas de la granja","item_name":"Espinacas frescas de la granja","quantity":240,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Jitomate Saladet fresco","item_name":"Jitomate Saladet fresco","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso de cabra suave artesanal","item_name":"Queso de cabra suave artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":60,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Brócoli fresco de la granja","item_name":"Brócoli fresco de la granja","quantity":600,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":15,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":50,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Fondo claro de pollo casero","item_name":"Fondo claro de pollo casero","quantity":480,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Filete de Huachinango fresco","item_name":"Filete de Huachinango fresco","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":70,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":18,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Alcaparras","item_name":"Alcaparras","quantity":30,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":25,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Nopales tiernos limpios de la granja","item_name":"Nopales tiernos limpios de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Parmesano artesanal","item_name":"Queso Parmesano artesanal","quantity":60,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":25,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Orégano seco","item_name":"Orégano seco","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Nopales tiernos limpios de la granja","item_name":"Nopales tiernos limpios de la granja","quantity":480,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Parmesano artesanal","item_name":"Queso Parmesano artesanal","quantity":60,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Aceite de oliva extra virgen VEVO","item_name":"Aceite de oliva extra virgen VEVO","quantity":25,"unit":"ml","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Orégano seco","item_name":"Orégano seco","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Filete de Huachinango fresco","item_name":"Filete de Huachinango fresco","quantity":900,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":70,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Ajo fresco","item_name":"Ajo fresco","quantity":18,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Alcaparras","item_name":"Alcaparras","quantity":30,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":25,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Caldo concentrado y fondo de res casero","item_name":"Caldo concentrado y fondo de res casero","quantity":600,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Jugo de limón fresco de la granja","item_name":"Jugo de limón fresco de la granja","quantity":25,"unit":"ml","category":"🍋 Cítricos y Ácidos Naturales"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":4,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Champiñones Portobello frescos","item_name":"Champiñones Portobello frescos","quantity":720,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Pechuga de pavo artesanal","item_name":"Pechuga de pavo artesanal","quantity":360,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Espinacas frescas de la granja","item_name":"Espinacas frescas de la granja","quantity":180,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Gouda artesanal","item_name":"Queso Gouda artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":40,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de azahar","item_name":"Flores de azahar","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Flores de azahar","item_name":"Flores de azahar","quantity":18,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Fórmula Reparadora 34Plus®","item_name":"Fórmula Reparadora 34Plus®","quantity":30,"unit":"g","category":"💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA"},{"name":"Agua purificada","item_name":"Agua purificada","quantity":900,"unit":"ml","category":"🌶️ Chiles, Condimentos e Infusiones"},{"name":"Champiñones Portobello frescos","item_name":"Champiñones Portobello frescos","quantity":720,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Pechuga de pavo artesanal","item_name":"Pechuga de pavo artesanal","quantity":360,"unit":"g","category":"🥩 Carnes, Pescados y Proteínas"},{"name":"Espinacas frescas de la granja","item_name":"Espinacas frescas de la granja","quantity":180,"unit":"g","category":"🥬 Verduras, Hortalizas y Frescos"},{"name":"Queso Gouda artesanal","item_name":"Queso Gouda artesanal","quantity":120,"unit":"g","category":"🧀 Lácteos y Quesos (Sin Gluten — Keto)"},{"name":"Mantequilla de pastoreo","item_name":"Mantequilla de pastoreo","quantity":40,"unit":"g","category":"🥑 Grasas, Aceites y Semillas"},{"name":"Sal de mar","item_name":"Sal de mar","quantity":6,"unit":"g","category":"🌶️ Chiles, Condimentos e Infusiones"}];

// Run consolidation like render3DShoppingList does
let itemsProcessedMap = {};
ingredientsBOM.forEach(it => {
  let key = (it.category || '') + '___' + (it.name || it.item_name || '');
  if (!itemsProcessedMap[key]) {
    itemsProcessedMap[key] = { ...it, quantity: parseFloat(it.quantity) || 1 };
  } else {
    itemsProcessedMap[key].quantity += (parseFloat(it.quantity) || 1);
  }
});

const itemsToProcess = Object.values(itemsProcessedMap);
console.log("Unique consolidated items to process:", itemsToProcess.length);

let shoppingReport = [];

itemsToProcess.forEach(item => {
  const cleanName = item.item_name;
  const cleanLower = cleanName.toLowerCase();
  if (/quinoa|cereza|leche de vaca|azúcar|azucar|miel|durazno/i.test(cleanLower)) return;

  const slug = normalizeToCanonicalSlug(item.slug || cleanName);
  const catSmart = getSmartItemCategory(cleanName, item.category);
  const cat = catSmart ? catSmart.replace(/\s*\/\s*/g, ' — ').replace(/\//g, ' — ') : '🛒 Abarrotes y Frescos';

  const isHarvest = harvestList.some(h => areInsumosEquivalent(h, cleanName)) || cat.includes("Cosecha");
  if (isHarvest) {
    shoppingReport.push({ name: cleanName, status: "HARVEST", cat });
    return;
  }

  const grossWithYield = item.quantity * getYieldFactor(cat, slug);
  const baseInfo = parseQuantityInBaseUnit(grossWithYield, item.unit);

  let stockInBase = 0;
  let matchedPantryObj = null;

  Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(pKey => {
    const pObj = window.PANTRY_STOCK_INVENTORY[pKey];
    if (!pObj || pObj.status !== 'canonical') return;

    if (areInsumosEquivalent(pObj.name || pKey, cleanName)) {
      matchedPantryObj = pObj;
      const pQty = parseFloat(pObj.stock) || 0;
      let pUnit = pObj.unit || item.unit;
      let parsedStock = parseQuantityInBaseUnit(pQty, pUnit);

      if (baseInfo.type === 'mass' && parsedStock.type === 'count') {
        const pieceWeight = getPieceGramWeight(cleanName);
        parsedStock.val = parsedStock.val * pieceWeight;
        parsedStock.type = 'mass';
        parsedStock.baseUnit = 'g';
      } else if (baseInfo.type === 'count' && parsedStock.type === 'mass') {
        const pieceWeight = getPieceGramWeight(cleanName);
        parsedStock.val = pieceWeight > 0 ? (parsedStock.val / pieceWeight) : parsedStock.val;
        parsedStock.type = 'count';
        parsedStock.baseUnit = 'piezas';
      }
      stockInBase += parsedStock.val;
    }
  });

  const netInBase = Math.max(0, baseInfo.val - stockInBase);
  shoppingReport.push({
    name: cleanName,
    cat,
    unit: item.unit,
    grossVal: baseInfo.val,
    stockInBase,
    netInBase,
    matchedPantry: matchedPantryObj ? matchedPantryObj.name : null,
    status: netInBase <= 0 ? "100% ALACENA" : (stockInBase > 0 ? "PARTIAL ALACENA" : "POR COMPRAR")
  });
});

fs.writeFileSync('scratch/shopping_sim_report.json', JSON.stringify(shoppingReport, null, 2));
console.log("Simulation complete! Report written to scratch/shopping_sim_report.json");
