import re

with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update areInsumosEquivalent
are_equiv_target = """    function areInsumosEquivalent(aName, bName) {
      if (!aName || !bName) return false;
      const a = aName.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").replace(/\\bnuex\\b/g, "nuez").trim();
      const b = bName.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").replace(/\\bnuex\\b/g, "nuez").trim();

      if (a === b) return true;

      // Stems y alias canónicos con coincidencia léxica multi-categoría y discriminación estricta
      const itemKeywords = [
        // Carnes, Aves y Pescados
        { stem: 'pollo', aliases: ['pechuga de pollo', 'pechuga de pollo organica', 'pechuga de pollo fresca', 'pollo organico', 'pollo fresco', 'carne de pollo'], exclude: ['hueso', 'huesos', 'retazo', 'fondo', 'caldo', 'pavo'] },
        { stem: 'huesos-pollo', aliases: ['huesos y retazo de pollo', 'retazo de pollo', 'huesos de pollo', 'retazo de pollo organico'], exclude: ['pechuga'] },
        { stem: 'tuetano', aliases: ['tuetano', 'huesos de res con tuetano', 'huesos de res', 'carne para caldo rico', 'costilla tuetano'], exclude: ['arrachera', 'sirloin', 'machaca', 'filete de res'] },
        { stem: 'huevo', aliases: ['huevo', 'huevos', 'huevos enteros', 'huevos organicos', 'huevos frescos', 'huevos organicos de libre pastoreo', 'huevos organicos de pastoreo', 'huevo entero'] },
        { stem: 'mantequilla', aliases: ['mantequilla', 'mantequilla de vaca', 'mantequilla de pastoreo', 'mantequilla de pastoreo artesanal', 'mantequilla sin sal'], exclude: ['ghee', 'clarificada'] },
        { stem: 'ghee', aliases: ['ghee', 'mantequilla clarificada'] },
        { stem: 'sirloin', aliases: ['sirloin', 'medallones de sirloin', 'medallon de sirloin', 'medallones de sirloin de res magro', 'carne molida de sirloin'], exclude: ['tuetano', 'huesos'] },
        { stem: 'arrachera', aliases: ['arrachera', 'arrachera de res', 'arrachera de res magra limpia', 'arrachera limpia', 'corte magro de arrachera'], exclude: ['tuetano', 'huesos', 'hamburguesa'] },
        { stem: 'ribeye', aliases: ['ribeye', 'corte magro de ribeye', 'corte de ribeye', 'corte magro de ribeye de res premium', 'ribeye de res'] },
        { stem: 'mojarra', aliases: ['mojarra', 'fajita de mojarra', 'fajitas de mojarra', 'tilapia', 'fajita de tilapia', 'fajitas de mojarra tilapia'] },
        { stem: 'hamburguesa-arrachera', aliases: ['hamburguesa de arrachera', 'hamburguesas de arrachera', 'arrachburg'] },
        { stem: 'robalo', aliases: ['robalo', 'filete de robalo', 'filete de robalo salvaje', 'filete de robalo salvaje fresco de captura', 'pescado blanco', 'filete de pescado blanco'] },
        { stem: 'huachinango', aliases: ['huachinango', 'filetes de huachinango', 'filete de huachinango con piel'] },
        { stem: 'salmon', aliases: ['salmon', 'lomo de salmon', 'filete de salmon', 'salmon fresco', 'salmon salvaje'], exclude: ['salsa'] },
        { stem: 'sardina', aliases: ['sardina', 'sardinas', 'sardina enlatada', 'sardinas enlatadas', 'sardina en salsa de tomate', 'sardinas en salsa de tomate', 'sardinas en tomate', 'lata de sardinas', 'latas de sardinas'] },
        { stem: 'atun-fresco', aliases: ['medallon de atun', 'medallones de atun', 'filete de atun', 'atun fresco', 'lomo de atun', 'medallon de atun fresco'], exclude: ['enlatado', 'en agua', 'en lata', 'lata'] },
        { stem: 'atun-lata', aliases: ['atun enlatado', 'atun en agua', 'atun en lata', 'lata de atun'], exclude: ['fresco', 'medallon', 'filete'] },
        { stem: 'pavo', aliases: ['pavo', 'pechuga de pavo', 'pechuga de pavo artesanal', 'jamon de pavo'], exclude: ['tocino', 'pollo'] },
        { stem: 'tocino-pavo', aliases: ['tocino de pavo', 'tocino de pavo artesanal', 'tocino de pavo crujiente'], exclude: ['pollo'] },
        { stem: 'machaca', aliases: ['machaca', 'carne seca machaca', 'carne seca machaca artesanal'] },
        { stem: 'flat-steak', aliases: ['flat steak', 'flatsteak', 'bife plano', 'steak flat'] },
        { stem: 'carne-molida', aliases: ['carne molida', 'carne molida de res', 'carne molida de sirloin'] },
        // Lácteos y Quesos
        { stem: 'gouda', aliases: ['gouda', 'queso gouda', 'queso gouda artesanal'] },
        { stem: 'panela', aliases: ['panela', 'queso panela', 'queso panela artesanal'] },
        { stem: 'parmesano', aliases: ['parmesano', 'queso parmesano', 'queso parmesano artesanal'] },
        { stem: 'queso-crema', aliases: ['queso crema', 'queso crema suave', 'queso crema suave artesanal'] },
        { stem: 'cabra', aliases: ['queso de cabra', 'queso de cabra artesanal', 'cabra artesanal', 'queso de cabra suave artesanal'] },
        { stem: 'ricotta', aliases: ['ricotta', 'queso ricotta', 'requeson'] },
        { stem: 'oikos', aliases: ['oikos', 'oikos pro', 'lacteo oikos', 'yoghurt oikos', 'yogurt oikos', 'oikos proteina', 'yogur griego', 'yoghurt griego'] },
        { stem: 'crema', aliases: ['crema', 'crema entera', 'crema entera de rancho', 'crema para batir', 'crema acida'], exclude: ['queso crema'] },
        { stem: 'cottage', aliases: ['queso cottage', 'cottage'] },
        { stem: 'philadelphia', aliases: ['queso philadelphia', 'philadelphia', 'queso crema philadelphia'] },
        { stem: 'mozzarella', aliases: ['queso mozzarella', 'mozzarella'] },
        // Grasas, Aceites y Semillas
        { stem: 'oliva', aliases: ['aceite de oliva', 'vevo', 'aceite de oliva extra virgen', 'aceite de oliva virgen extra', 'aceite de oliva extra virgen (vevo)'], exclude: ['aceituna', 'aceitunas'] },
        { stem: 'aceite-ajonjoli', aliases: ['aceite de ajonjoli', 'aceite de sesamo', 'aceite de ajonjoli tostado'], exclude: ['semilla', 'semillas', 'grano'] },
        { stem: 'semillas-sesamo', aliases: ['semillas de sesamo', 'semillas de ajonjoli', 'ajonjoli en grano', 'semilla de ajonjoli', 'ajonjoli', 'semillas de sesamo (ajonjoli)'], exclude: ['aceite'] },
        { stem: 'nuez-pecana', aliases: ['nuez pecana', 'nueces pecana', 'nuex pecana', 'nuex', 'pecana', 'pecanas', 'nuez pecana fresca', 'nuez pecana de la granja', 'nuez pecana fresca de la granja', 'nueces pecanas', 'nuez pecana en mitades', 'nuez pecana pelada', 'nuez', 'nueces', 'nuez picada'] },
        { stem: 'nuez-castilla', aliases: ['nuez de castilla', 'nueces de castilla', 'nuez de castilla fresca'] },
        { stem: 'nuez-india', aliases: ['nuez de la india', 'nueces de la india', 'nuez india', 'nueces india', 'anacardo', 'anacardos', 'maranon'] },
        { stem: 'almendra', aliases: ['almendra', 'almendras', 'almendras fileteadas', 'almendras fileteadas tostadas'] },
        { stem: 'chia', aliases: ['chia', 'semillas de chia', 'semillas de chia organicas'] },
        { stem: 'girasol', aliases: ['semillas de girasol', 'semilla de girasol', 'girasol', 'semillas de girasol tostadas'] },
        { stem: 'coco-rallado', aliases: ['coco deshidratado', 'coco rallado', 'coco sin azucar'], exclude: ['leche de coco', 'aceite de coco'] },
        { stem: 'leche-coco', aliases: ['leche de coco', 'leche de coco sin azucar'], exclude: ['deshidratado', 'rallado', 'aceite'] },
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
        { stem: 'calabacita', aliases: ['calabacita', 'calabacitas', 'calabaza', 'zucchini', 'calabacitas verdes tiernas'], exclude: ['semilla', 'semillas', 'pepita', 'pepitas', 'flor'] },
        { stem: 'flor-calabaza', aliases: ['flor de calabaza', 'flores de calabaza'] },
        { stem: 'semillas-calabaza', aliases: ['semillas de calabaza', 'semilla de calabaza', 'pepitas de calabaza', 'pepita de calabaza', 'pepitas'], exclude: ['calabacita', 'calabacitas'] },
        { stem: 'brocoli', aliases: ['brocoli', 'brocolis'] },
        { stem: 'esparrago', aliases: ['esparrago', 'esparragos'] },
        { stem: 'nopal', aliases: ['nopal', 'nopales'] },
        { stem: 'ejote', aliases: ['ejote', 'ejotes', 'ejotes verdes', 'ejotes verdes tiernos'] },
        { stem: 'cilantro', aliases: ['cilantro'] },
        { stem: 'arugula', aliases: ['arugula'] },
        { stem: 'coliflor', aliases: ['coliflor'] },
        { stem: 'menta', aliases: ['menta'] },
        { stem: 'toronjil', aliases: ['toronjil'] },
        { stem: 'manzanilla-te', aliases: ['manzanilla', 'flores de manzanilla', 'flores de manzanilla seca', 'te de manzanilla'], exclude: ['aceituna', 'aceitunas'] },
        { stem: 'aceitunas', aliases: ['aceitunas manzanilla', 'aceitunas', 'aceituna'] },
        { stem: 'jamaica', aliases: ['jamaica', 'flor de jamaica', 'flor de jamaica molida en polvo'] },
        { stem: 'apio', aliases: ['apio'] },
        { stem: 'chayote', aliases: ['chayote', 'chayotes', 'chayote tierno', 'chayotes tiernos', 'chayotes tiernos pelados'] },
        { stem: 'hinojo', aliases: ['hinojo'] },
        { stem: 'aguacate', aliases: ['aguacate', 'aguacates', 'aguacate hass', 'aguacate hass fresco'] },
        { stem: 'morron', aliases: ['morron', 'morrones', 'pimiento morron', 'pimientos morrones', 'pimientos morrones dulces', 'pimiento morron dulce'] },
        { stem: 'cebolla-fresca', aliases: ['cebolla blanca', 'cebolla blanca fresca', 'cebolla', 'cebollas', 'cebolla morada'], exclude: ['en polvo'] },
        { stem: 'cebolla-polvo', aliases: ['cebolla en polvo'] },
        { stem: 'jitomate', aliases: ['jitomate', 'jitomates', 'saladet', 'jitomate saladet', 'jitomate saladet fresco', 'jitomate bola'], exclude: ['tomate verde', 'tomatillo'] },
        { stem: 'tomate-verde', aliases: ['tomate verde', 'tomate verde fresco', 'tomatillo', 'tomate'], exclude: ['jitomate', 'saladet', 'salsa'] },
        { stem: 'champinon', aliases: ['champinon', 'champinones', 'portobello', 'champinones portobello', 'champinones portobello frescos'] },
        { stem: 'lechuga-sweet', aliases: ['lechuga sweet', 'sweet lettuce', 'lechuga', 'lechugas', 'lechuga orejona', 'hojas de lechuga', 'hojas de lechuga orejona viva'] },
        { stem: 'limon', aliases: ['limon', 'limones', 'limones frescos', 'limon agrio', 'limones agrios', 'limones agrios frescos', 'limones agrios frescos de la granja', 'jugo de limon', 'jugo de limon fresco', 'jugo de limon fresco de la granja', 'jugo de limon recien exprimido', 'limon agrio fresco con semilla'] },
        { stem: 'ajo-fresco', aliases: ['ajo', 'ajos', 'ajo fresco', 'dientes de ajo', 'ajo picado', 'ajo machacado'], exclude: ['ajonjoli', 'sal con ajo'] },
        { stem: 'sal-con-ajo', aliases: ['sal con ajo'] },
        { stem: 'sal', aliases: ['sal de mar', 'sal de colima', 'sal mineral', 'sal de mar mineral de colima', 'sal marina de grano', 'sal fina'], exclude: ['salsa', 'ajo', 'salmon', 'apio'] },
        { stem: 'canela', aliases: ['canela', 'canela molida', 'canela en polvo'] },
        { stem: 'oregano', aliases: ['oregano', 'oregano seco', 'oregano delgado', 'oregano grueso'] },
        { stem: 'tomillo', aliases: ['tomillo', 'tomillo fresco', 'tomillo seco'] },
        { stem: 'pimienta-negra', aliases: ['pimienta negra', 'pimienta negra molida', 'pimienta negra recien molida'] },
        { stem: 'curcuma', aliases: ['curcuma', 'curcuma en polvo', 'curry suave en polvo / curcuma'] },
        { stem: 'alcaparras', aliases: ['alcaparras', 'alcaparra'] },
        { stem: 'agua-purificada', aliases: ['agua purificada', 'agua pura', 'botellas de agua purificada', 'botella de agua purificada', 'botella de agua', 'botellas de agua'], exclude: ['mineral'] },
        { stem: 'agua-mineral', aliases: ['agua mineral', 'aguamin', 'botellas de agua mineral', 'botella de agua mineral'] },
        { stem: 'multisinergix', aliases: ['multisinergix', 'multi sinergix', '33plus', '33 plus', 'formula nootropica 33plus', 'formula biotecnologica nootropica 33plus', 'formula nootropica multisinergix'] },
        { stem: 'aminosinergix', aliases: ['aminosinergix', 'amino sinergix', '34plus', '34 plus', 'formula reparadora 34plus', 'formula biotecnologica reparadora 34plus', 'formula reparadora aminosinergix'] },
        { stem: 'nogada', aliases: ['nogada'] },
        { stem: 'grenetina', aliases: ['grenetina', 'grenetina natural', 'grenetina natural pura', 'grenetina natural en polvo', 'colageno hidrolizado'] }
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
      if (slugA && slugB && slugA === slugB) return true;

      return false;
    }"""

old_are_equiv_regex = r"    function areInsumosEquivalent\(aName, bName\) \{[\s\S]*?^    \}"
content = re.sub(old_are_equiv_regex, lambda m: are_equiv_target, content, flags=re.M)
print("1. Replaced areInsumosEquivalent successfully.")

# 2. Update INGREDIENT_CANONICAL_MAP_JS & normalizeToCanonicalSlug & getPieceGramWeight
canonical_block_target = """const INGREDIENT_CANONICAL_MAP_JS = {
  "aceite-oliva": ["aceite de oliva", "aceite de oliva extra virgen", "aceite vevo", "aceite de oliva extra virgen vevo", "aceite de oliva virgen extra"],
  "te-verde": ["té verde", "te verde", "té verde orgánico", "matcha ceremonial", "te verde sencha"],
  "huevo-organico": ["huevo", "huevos", "huevos frescos", "huevos orgánicos", "huevos frescos orgánicos", "huevos frescos orgánicos de pastoreo", "huevos enteros", "huevos orgánicos de pastoreo"],
  "pechuga-pavo": ["pechuga de pavo", "pavo artesanal", "pechuga de pavo artesanal", "jamón de pavo"],
  "pechuga-pollo": ["pechuga de pollo", "pollo fresco", "pechuga de pollo fresca", "pechuga de pollo orgánica", "pollo orgánico", "muslos de pollo"],
  "sirloin-magro": ["carne molida de sirloin", "sirloin magro", "carne molida de sirloin magra"],
  "filete-res": ["filete de res", "filete de res magro", "ribeye", "sirloin", "medallones de mignon"],
  "huachinango-fresco": ["huachinango", "filete de huachinango", "filete de huachinango fresco", "filete de huachinango al horno"],
  "robalo-fresco": ["róbalo", "robalo", "filete de róbalo", "filete de robalo fresco", "filete de róbalo a la plancha"],
  "salmon-salvaje": ["salmón", "salmon", "salmón salvaje", "filete de salmón fresco", "filete de salmón salvaje", "filete de salmón fresco con piel", "lomo de salmón"],
  "pescado-blanco": ["pescado blanco", "filete de pescado blanco", "filete de pescado blanco fresco"],
  "atun-fresco": ["atún fresco", "atun fresco", "medallón de atún", "medallon de atun", "medallones de atun", "filete de atún", "filete de atun", "lomo de atún", "lomo de atun", "medallón de atún fresco"],
  "atun-enlatado": ["atún enlatado", "atun enlatado", "atún en agua", "atun en agua", "atún en lata", "atun en lata", "lata de atún", "lata de atun"],
  "sardinas": ["sardinas enlatadas", "sardina enlatada", "sardina en salsa de tomate", "sardinas en salsa de tomate", "sardina", "sardinas", "lata de sardinas", "latas de sardinas"],
  "queso-parmesano": ["queso parmesano", "parmesano maduro", "queso parmesano maduro", "queso parmesano artesanal"],
  "queso-manchego": ["queso manchego", "manchego maduro", "queso manchego maduro"],
  "queso-gouda": ["queso gouda", "gouda maduro", "queso gouda maduro", "queso gouda artesanal"],
  "queso-panela": ["queso panela", "panela fresco", "queso panela fresco", "queso panela artesanal"],
  "queso-cabra": ["queso de cabra", "cabra artesanal", "queso de cabra artesanal", "queso de cabra suave artesanal"],
  "queso-crema": ["queso crema", "queso crema artesanal"],
  "queso-philadelphia": ["queso philadelphia", "philadelphia"],
  "queso-cottage": ["queso cottage", "cottage"],
  "queso-mozzarella": ["queso mozzarella", "mozzarella"],
  "mantequilla-pastoreo": ["mantequilla", "mantequilla de vaca", "mantequilla de pastoreo", "mantequilla sin sal"],
  "jitomate-bola": ["jitomate", "jitomates", "jitomate bola", "jitomate bola jugoso", "jitomate saladet", "jitomate saladet fresco", "saladet"],
  "tomate-verde": ["tomate verde", "tomate verde fresco", "tomatillo", "tomates verdes", "tomate"],
  "morron": ["morrón", "morron", "morrones", "pimiento morrón", "pimiento morron", "pimientos morrones", "pimientos morrones dulces"],
  "flor-calabaza": ["flor de calabaza", "flores de calabaza"],
  "calabaza": ["calabaza", "calabazas", "calabacita", "calabacitas", "calabacitas verdes tiernas"],
  "almendras-fileteadas": ["almendras fileteadas tostadas", "almendras fileteadas", "almendras tostadas", "almendras enteras", "almendra", "almendras"],
  "semillas-chia": ["semillas de chía orgánicas", "semillas de chia organicas", "semillas de chía", "semillas de chia", "chía", "chia"],
  "semillas-ajonjoli": ["semillas de sésamo", "semillas de sesamo", "semillas de ajonjolí", "semillas de ajonjoli", "ajonjolí", "ajonjoli"],
  "ajo-fresco": ["ajo fresco", "dientes de ajo fresco", "dientes de ajo", "ajo picado", "ajo machacado"],
  "sal-con-ajo": ["sal con ajo"],
  "limon-fresco": ["jugo de limón fresco recién exprimido", "jugo de limon fresco recien exprimido", "jugo de limón fresco", "limón fresco recién exprimido", "limones frescos", "limón", "limon", "limon agrio"],
  "pimienta-negra": ["pimienta negra recién molida", "pimienta negra recien molida", "pimienta negra molida", "pimienta negra"],
  "cebolla-blanca": ["cebolla blanca fresca", "cebolla blanca", "cebolla", "cebollas"],
  "cebolla-polvo": ["cebolla en polvo"],
  "sal-mar": ["sal de mar", "sal de colima", "sal mineral", "sal de mar mineral de colima", "sal marina de grano", "sal fina"],
  "manzanilla-te": ["manzanilla", "flores de manzanilla", "flores de manzanilla seca", "té de manzanilla", "te de manzanilla"],
  "aceitunas-manzanilla": ["aceitunas manzanilla", "aceitunas", "aceituna"],
  "yoghurt-griego": ["yoghurt griego natural sin azúcar", "yoghurt griego", "yogurt griego", "yoghurt griego natural", "yogur griego"],
  "mayonesa": ["mayonesa", "mayonesa casera", "mayonesa keto"],
  "leche-coco": ["leche de coco", "leche de coco sin azúcar", "leche de coco sin azucar"],
  "multisinergix": ["multisinergix", "multi sinergix", "33plus", "33 plus", "fórmula 33plus", "formula nootropica 33plus", "formula nootropica multisinergix"],
  "aminosinergix": ["aminosinergix", "amino sinergix", "34plus", "34 plus", "fórmula 34plus", "formula reparadora 34plus", "formula reparadora aminosinergix"],
  "flat-steak": ["flat steak", "flatsteak", "bife plano"],
  "carne-molida": ["carne molida", "carne molida de res"],
  "fajitas-mojarra": ["fajitas de mojarra", "fajita de mojarra", "fajitas de mojarra tilapia", "tilapia"]
};

function normalizeToCanonicalSlug(rawName) {
  if (!rawName) return "";
  const clean = rawName.trim().toLowerCase();
  const cleanNoAcc = stripAccents(clean);

  // 1. Coincidencia exacta
  for (const slug in INGREDIENT_CANONICAL_MAP_JS) {
    const aliases = INGREDIENT_CANONICAL_MAP_JS[slug];
    for (const alias of aliases) {
      const aliasClean = stripAccents(alias.trim().toLowerCase());
      if (cleanNoAcc === aliasClean) {
        return slug;
      }
    }
  }

  // 2. Coincidencia con frase multi-palabra o límite de palabra estricto
  for (const slug in INGREDIENT_CANONICAL_MAP_JS) {
    const aliases = INGREDIENT_CANONICAL_MAP_JS[slug];
    for (const alias of aliases) {
      const aliasClean = stripAccents(alias.trim().toLowerCase());
      if (aliasClean.includes(" ")) {
        if (cleanNoAcc.includes(aliasClean) || aliasClean.includes(cleanNoAcc)) {
          return slug;
        }
      } else {
        const wordRegex = new RegExp('(?:^|\\\\s|_)' + aliasClean.replace(/[-\\\\/\\\\^$*+?.()|[\\]{}]/g, '\\\\$&') + '(?:\\\\s|_|$)', 'i');
        if (wordRegex.test(cleanNoAcc)) {
          return slug;
        }
      }
    }
  }

  const sanitized = cleanNoAcc.replace(/[^a-z0-9\\\\s-]/g, '').replace(/\\\\s+/g, '-').replace(/^-+|-+$/g, '');
  return sanitized || "insumo-general";
}

function getPieceGramWeight(itemName) {
  const n = (itemName || '').toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").trim();
  if (/morron|pimiento/i.test(n)) return 160; // 1 pimiento morrón ~160 g
  if (/pechuga.*pollo|pollo.*pechuga|\\bpollo\\b/i.test(n) && !/pavo/i.test(n)) return 500; // 1 pechuga de pollo ~500 g
  if (/calabacita|calabaza/i.test(n) && !/flor/i.test(n)) return 180; // 1 calabacita tierna ~180 g
  if (/flor de calabaza/i.test(n)) return 180; // 1 manojo de flor de calabaza ~180 g
  if (/lechuga/i.test(n)) return 380; // 1 pieza de lechuga ~380 g
  if (/jitomate|tomate saladet/i.test(n)) return 120; // 1 jitomate ~120 g
  if (/tomate verde|tomatillo/i.test(n)) return 60; // 1 tomate verde ~60 g
  if (/cebolla/i.test(n) && !/polvo/i.test(n)) return 160; // 1 cebolla ~160 g
  if (/aguacate/i.test(n)) return 180; // 1 aguacate Hass ~180 g
  if (/zanahoria/i.test(n)) return 120; // 1 zanahoria ~120 g
  if (/elote/i.test(n)) return 250; // 1 elote ~250 g
  if (/huevo/i.test(n)) return 55; // 1 huevo ~55 g
  if (/chayote/i.test(n)) return 200; // 1 chayote ~200 g
  if (/pepino/i.test(n)) return 200; // 1 pepino ~200 g
  if (/limon/i.test(n)) return 40; // 1 limón ~40 g
  if (/ajo/i.test(n) && !/ajonjoli/i.test(n)) return 50; // 1 cabeza de ajo ~50 g
  if (/sardina/i.test(n)) return 425; // 1 lata/envase de sardinas en salsa de tomate ~425 g
  if (/atun/i.test(n)) return 100; // 1 lata de atún ~100 g
  return 100;
}"""

old_canonical_block_regex = r"const INGREDIENT_CANONICAL_MAP_JS = \{[\s\S]*?^function getPieceGramWeight[\s\S]*?^\}"
content = re.sub(old_canonical_block_regex, lambda m: canonical_block_target, content, flags=re.M)
print("2. Replaced INGREDIENT_CANONICAL_MAP_JS and getPieceGramWeight successfully.")

# 3. Update getYieldFactor
old_yield_regex = r"function getYieldFactor\(category, slug\) \{[\s\S]*?^\}"
new_yield_func = """function getYieldFactor(category, slug) {
  if (/sardina|atun-enlatado|enlatad|lata/i.test(slug)) return 1.00;
  if (category && category.includes("Carnes")) return 1.15;
  if (category && category.includes("Verduras")) return 1.10;
  return 1.00;
}"""
content = re.sub(old_yield_regex, lambda m: new_yield_func, content, flags=re.M)
print("3. Replaced getYieldFactor successfully.")

# 4. Update Paso 3 in initSetupPanel
new_paso3_pantry_loop = """        // 2.1 Insumos Físicos de Despensa (window.PANTRY_STOCK_INVENTORY)
        // Regla de Oro: En Reconfigurar Parámetros se muestran exactamente los 106 insumos del inventario físico
        if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined') {
          Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(k => {
            const pObj = window.PANTRY_STOCK_INVENTORY[k];
            if (!pObj) return;
            if (pObj.stock <= 0 && (!pObj.item_num || pObj.item_num <= 0)) return;
            if (k === 'multisinergix' || k === 'aminosinergix' || k === '33plus' || k === '34plus' || k === 'zarzamoras-frescas' || k === 'fresas-frescas' || k === 'arilos-granada' || k === 'moras-frescas' || k === 'frambuesas-frescas' || k === 'arandanos-frescos' || k === 'pitaya-fresca' || k === 'ajo-fresco') return;

            const slug = normalizeToCanonicalSlug(pObj.name || k);
            if (deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === pObj.name.toLowerCase())) return;

            const alreadyInList = nonFarm.some(existing => (existing.item_num && pObj.item_num ? existing.item_num === pObj.item_num : existing.item_name === pObj.name));
            if (!alreadyInList) {
              seenPantrySlugs.add(slug);
              let displayName = pObj.name;
              if (pObj.item_num === 17) displayName = "Agua mineral (6 botellas de 1500 ml)";
              if (pObj.item_num === 18) displayName = "Agua mineral (1 botella de 355 ml)";
              if (pObj.item_num === 21) displayName = "Flat steak (Paquete 1)";
              if (pObj.item_num === 22) displayName = "Flat steak (Paquete 2)";
              if (pObj.item_num === 77) displayName = "Orégano delgado";
              if (pObj.item_num === 78) displayName = "Orégano grueso";
              if (pObj.item_num === 87) displayName = "Sal marina de grano";
              if (pObj.item_num === 88) displayName = "Sal fina";

              const assignedCat = (pObj.status === 'prohibited')
                ? '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)'
                : (pObj.category || getSmartItemCategory(pObj.name));
              nonFarm.push({
                sku: k,
                item_num: pObj.item_num,
                item_name: displayName,
                raw_name: pObj.name,
                quantity: pObj.stock,
                unit: pObj.unit || 'g',
                category: assignedCat,
                status: pObj.status || 'canonical',
                packaging: pObj.packaging
              });
            }
          });
        }"""
old_paso3_pantry_loop = r"        // 2\.1 Insumos Físicos de Despensa \(window\.PANTRY_STOCK_INVENTORY\)[\s\S]*?nonFarm\.push\(\{[\s\S]*?\}\);\s*\}\s*\}\);\s*\}"
content = re.sub(old_paso3_pantry_loop, lambda m: new_paso3_pantry_loop, content)
print("4. Updated Paso 3 in initSetupPanel successfully.")

# 5. Update render3DShoppingList dynamic stock deduction
new_shopping_pantry_block = """    let stockInBase = 0;
    let matchedPantryObj = null;

    if (typeof dynamicPantryStock !== 'undefined' && dynamicPantryStock) {
      Object.keys(dynamicPantryStock).forEach(pKey => {
        const pObj = dynamicPantryStock[pKey];
        if (!pObj || pObj.stock <= 0) return;

        if (areInsumosEquivalent(pObj.name || pKey, cleanName)) {
          matchedPantryObj = pObj;
          const pQty = pObj.stock;
          let pUnit = pObj.unit || item.unit;
          let parsedStock = parseQuantityInBaseUnit(pQty, pUnit);

          // Conversión Canónica de Conteos Físicos (piezas/manojo/latas) a Masa (g) cuando la demanda BOM está en masa
          if (baseInfo.type === 'mass' && parsedStock.type === 'count') {
            const pieceWeight = getPieceGramWeight(cleanName);
            parsedStock.val = parsedStock.val * pieceWeight;
            parsedStock.type = 'mass';
            parsedStock.baseUnit = 'g';
            parsedStock.isPieceConversion = true;
          } else if (baseInfo.type === 'count' && parsedStock.type === 'mass') {
            const pieceWeight = getPieceGramWeight(cleanName);
            parsedStock.val = pieceWeight > 0 ? (parsedStock.val / pieceWeight) : parsedStock.val;
            parsedStock.type = 'count';
            parsedStock.baseUnit = item.unit || 'piezas';
          }

          // Clinical Safety Net: si la demanda es > 200g y pQty < 20 para carnes/pescados, interpretar como kg (a menos que ya sea empaque comercial o conteo de piezas)
          if (parsedStock.type === 'mass' && !parsedStock.isPieceConversion && parsedStock.val < 20 && baseInfo.val > 200 && (cat.includes('Carne') || cat.includes('Proteína') || cat.includes('Pescado')) && !pUnit.includes('paquete') && !pUnit.includes('bolsa')) {
            parsedStock.val *= 1000;
          }

          const neededFromThis = Math.max(0, baseInfo.val - stockInBase);
          const deductVal = Math.min(parsedStock.val, neededFromThis);
          stockInBase += deductVal;

          // Descontar del inventario dinámico restante (Anti-doble amortización)
          if (parsedStock.val > 0) {
            const ratio = deductVal / parsedStock.val;
            pObj.stock = Math.max(0, pObj.stock - (pQty * ratio));
          }
        }
      });
    }"""

old_shopping_pantry_block = r"    let stockInBase = 0;\s*let matchedPantryObj = null;\s*if \(typeof window\.PANTRY_STOCK_INVENTORY !== 'undefined'[\s\S]*?stockInBase \+= parsedStock\.val;\s*\}\s*\}\);\s*\}\s*\}\);\s*\}\s*if \(stockInBase === 0 && typeof pantryStock !== 'undefined'[\s\S]*?stockInBase \+= parsedStock\.val;\s*\}\s*\}\);\s*\}"

if "const dynamicPantryStock = {};" not in content:
    init_dynamic = """  // Inicializar inventario dinámico de alacena para amortización estricta sin duplicación
  const dynamicPantryStock = {};
  if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined' && window.PANTRY_STOCK_INVENTORY) {
    Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(k => {
      const p = window.PANTRY_STOCK_INVENTORY[k];
      if (p && p.status === 'canonical') {
        dynamicPantryStock[k] = {
          stock: parseFloat(p.stock) || 0,
          unit: (typeof window.pantryCardUnits !== 'undefined' && (window.pantryCardUnits[p.name] || window.pantryCardUnits[k])) || p.unit,
          packaging: p.packaging,
          name: p.name,
          item_num: p.item_num
        };
      }
    });
  }

  itemsToProcess.forEach(item => {"""
    content = content.replace("itemsToProcess.forEach(item => {", init_dynamic, 1)

content = re.sub(old_shopping_pantry_block, lambda m: new_shopping_pantry_block, content)
print("5. Updated render3DShoppingList stock deduction successfully.")

with open("generate_standalone_html.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Saved updated generate_standalone_html.py successfully!")
