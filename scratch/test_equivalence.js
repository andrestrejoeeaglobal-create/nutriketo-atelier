function normalizeToCanonicalSlug(name) {
  if (!name) return "";
  let cleanNoAcc = name.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();
  const sanitized = cleanNoAcc.replace(/[^a-z0-9\s-]/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '');
  return sanitized || "insumo-general";
}

function areInsumosEquivalent(aName, bName) {
  if (!aName || !bName) return false;
  const a = aName.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();
  const b = bName.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();

  if (a === b) return true;

  const itemKeywords = [
    // Carnes, Aves y Pescados
    { stem: 'pollo', aliases: ['pollo', 'pechuga de pollo', 'pechuga de pollo organica', 'pechuga'] },
    { stem: 'huevo', aliases: ['huevo', 'huevos', 'huevos enteros', 'huevos organicos', 'huevos frescos', 'huevos organicos de libre pastoreo', 'huevo entero'] },
    { stem: 'mantequilla', aliases: ['mantequilla', 'mantequilla de vaca', 'mantequilla de pastoreo', 'mantequilla de pastoreo artesanal', 'mantequilla sin sal'], exclude: ['ghee', 'clarificada'] },
    { stem: 'ghee', aliases: ['ghee', 'mantequilla clarificada'] },
    { stem: 'sirloin', aliases: ['sirloin', 'medallones de sirloin', 'medallon de sirloin', 'medallones de sirloin de res magro', 'carne molida de sirloin'] },
    { stem: 'arrachera', aliases: ['arrachera', 'arrachera de res', 'arrachera de res magra limpia', 'arrachera limpia'] },
    { stem: 'robalo', aliases: ['robalo', 'filete de robalo', 'filete de robalo salvaje', 'filete de robalo salvaje fresco de captura', 'pescado blanco', 'filete de pescado blanco'] },
    { stem: 'huachinango', aliases: ['huachinango', 'filetes de huachinango', 'filete de huachinango con piel'] },
    { stem: 'salmon', aliases: ['salmon', 'lomo de salmon', 'filete de salmon'] },
    { stem: 'atun', aliases: ['atun', 'medallones de atun', 'lomo de atun'] },
    { stem: 'pavo', aliases: ['pavo', 'pechuga de pavo', 'pechuga de pavo artesanal'] },
    { stem: 'tocino-pavo', aliases: ['tocino de pavo', 'tocino de pavo artesanal', 'tocino de pavo crujiente'] },
    { stem: 'machaca', aliases: ['machaca', 'carne seca machaca', 'carne seca machaca artesanal'] },
    { stem: 'tuetano', aliases: ['tuetano', 'huesos de res con tuetano', 'carne para caldo rico', 'costilla tuetano'] },
    { stem: 'huesos-pollo', aliases: ['huesos y retazo de pollo', 'retazo de pollo', 'pollo entero para caldo'] },
    // Lácteos y Quesos
    { stem: 'gouda', aliases: ['gouda', 'queso gouda', 'queso gouda artesanal'] },
    { stem: 'panela', aliases: ['panela', 'queso panela', 'queso panela artesanal'] },
    { stem: 'parmesano', aliases: ['parmesano', 'queso parmesano', 'queso parmesano artesanal'] },
    { stem: 'queso-crema', aliases: ['queso crema', 'queso crema suave', 'queso crema suave artesanal'] },
    { stem: 'cabra', aliases: ['queso de cabra', 'queso de cabra artesanal', 'cabra artesanal'] },
    { stem: 'crema', aliases: ['crema', 'crema entera', 'crema entera de rancho', 'crema para batir'], exclude: ['queso crema'] },
    // Grasas, Aceites y Semillas
    { stem: 'oliva', aliases: ['aceite de oliva', 'vevo', 'aceite de oliva extra virgen', 'aceite de oliva virgen extra', 'aceite de oliva extra virgen (vevo)'] },
    { stem: 'aceite-ajonjoli', aliases: ['aceite de ajonjoli', 'aceite de sesamo', 'aceite de ajonjoli tostado'] },
    { stem: 'nuez-pecana', aliases: ['nuez pecana', 'nueces pecana', 'pecana', 'pecanas'] },
    { stem: 'nuez-castilla', aliases: ['nuez de castilla', 'nueces de castilla', 'nuez de castilla fresca'] },
    { stem: 'almendra', aliases: ['almendra', 'almendras', 'almendras fileteadas'] },
    { stem: 'chia', aliases: ['chia', 'semillas de chia', 'semillas de chia organicas'] },
    { stem: 'girasol', aliases: ['semillas de girasol', 'semilla de girasol', 'girasol'] },
    { stem: 'sesamo', aliases: ['semillas de sesamo', 'semillas de ajonjoli', 'ajonjoli'] },
    { stem: 'coco', aliases: ['coco deshidratado', 'coco rallado', 'coco sin azucar', 'leche de coco'] },
    // Frutas
    { stem: 'granada', aliases: ['granada', 'granadas', 'arilos', 'arilos de granada'] },
    { stem: 'pitaya', aliases: ['pitaya', 'pitayas', 'pitahaya', 'pitahayas'] },
    { stem: 'fresa', aliases: ['fresa', 'fresas'] },
    { stem: 'frambuesa', aliases: ['frambuesa', 'frambuesas'] },
    { stem: 'zarzamora', aliases: ['zarzamora', 'zarzamoras'] },
    { stem: 'arandano', aliases: ['arandano', 'arandanos'] },
    { stem: 'mora', aliases: ['mora', 'moras'], exclude: ['morada'] },
    // Verduras
    { stem: 'espinaca', aliases: ['espinaca', 'espinacas', 'espinacas baby'] },
    { stem: 'calabacita', aliases: ['calabacita', 'calabacitas', 'calabaza'] },
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
    { stem: 'chayote', aliases: ['chayote', 'chayotes'] },
    { stem: 'hinojo', aliases: ['hinojo'] },
    { stem: 'aguacate', aliases: ['aguacate', 'aguacate hass'] },
    { stem: 'limon', aliases: ['limon', 'limones', 'jugo de limon'] },
    { stem: 'ajo', aliases: ['ajo', 'ajos', 'dientes de ajo'] },
    { stem: 'sal', aliases: ['sal de mar', 'sal de colima', 'sal mineral'] },
    { stem: '33plus', aliases: ['33plus', 'formula nootropica 33plus', 'formula biotecnologica nootropica 33plus'] },
    { stem: '34plus', aliases: ['34plus', 'formula reparadora 34plus', 'formula biotecnologica reparadora 34plus'] }
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

const tests = [
  ['Pechuga de pollo', 'Pechuga de pollo orgánica', true],
  ['Huevos enteros', 'Huevos orgánicos de libre pastoreo', true],
  ['Mantequilla de vaca (sin sal)', 'Mantequilla de pastoreo artesanal', true],
  ['Mantequilla de vaca (sin sal)', 'Mantequilla clarificada (Ghee)', false],
  ['Medallones de Sirloin de res magro', 'Carne molida de Sirloin', true],
  ['Filete de pescado blanco', 'Filete de robalo salvaje fresco de captura', true],
  ['Nueces pecana', 'Nuez pecana', true],
  ['Aceite de oliva virgen extra', 'Aceite de oliva extra virgen (VEVO)', true],
  ['Granadas frescas', 'Arilos de granada fresca', true],
  ['Fresas frescas', 'Fresas', true]
];

tests.forEach(([a, b, expected]) => {
  const result = areInsumosEquivalent(a, b);
  console.log(`${a} == ${b} -> ${result} (Expected: ${expected}) -> ${result === expected ? 'PASS' : 'FAIL'}`);
});
