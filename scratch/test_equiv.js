
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

console.log("Equivalent('Sardinas enlatadas', 'Sardina en salsa de tomate'):", areInsumosEquivalent('Sardinas enlatadas', 'Sardina en salsa de tomate'));
console.log("Equivalent('Sardina en salsa de tomate', 'Sardinas enlatadas'):", areInsumosEquivalent('Sardina en salsa de tomate', 'Sardinas enlatadas'));
console.log("Equivalent('Pechuga de pollo', 'Pechuga de pavo artesanal'):", areInsumosEquivalent('Pechuga de pollo', 'Pechuga de pavo artesanal'));
console.log("Equivalent('Pechuga de pollo orgánica', 'Pechuga de pollo'):", areInsumosEquivalent('Pechuga de pollo orgánica', 'Pechuga de pollo'));
console.log("slug Sardinas enlatadas:", normalizeToCanonicalSlug("Sardinas enlatadas"));
console.log("slug Sardina en salsa de tomate:", normalizeToCanonicalSlug("Sardina en salsa de tomate"));
