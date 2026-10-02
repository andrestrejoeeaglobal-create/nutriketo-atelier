function areInsumosEquivalent(aName, bName) {
  if (!aName || !bName) return false;
  const a = aName.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();
  const b = bName.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();

  if (a === b) return true;

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
    { stem: 'robalo', aliases: ['robalo', 'filete de robalo', 'filete de robalo salvaje', 'filete de robalo salvaje fresco de captura', 'pescado blanco', 'filete de pescado blanco'] },
    { stem: 'huachinango', aliases: ['huachinango', 'filetes de huachinango', 'filete de huachinango con piel'] },
    { stem: 'salmon', aliases: ['salmon', 'lomo de salmon', 'filete de salmon'] },
    { stem: 'atun', aliases: ['atun', 'medallones de atun', 'lomo de atun'] },
    { stem: 'pavo', aliases: ['pavo', 'pechuga de pavo', 'pechuga de pavo artesanal'], exclude: ['tocino'] },
    { stem: 'tocino-pavo', aliases: ['tocino de pavo', 'tocino de pavo artesanal', 'tocino de pavo crujiente'] },
    { stem: 'machaca', aliases: ['machaca', 'carne seca machaca', 'carne seca machaca artesanal'] },
    // Lácteos y Quesos
    { stem: 'gouda', aliases: ['gouda', 'queso gouda', 'queso gouda artesanal'] },
    { stem: 'panela', aliases: ['panela', 'queso panela', 'queso panela artesanal'] },
    { stem: 'parmesano', aliases: ['parmesano', 'queso parmesano', 'queso parmesano artesanal'] },
    { stem: 'queso-crema', aliases: ['queso crema', 'queso crema suave', 'queso crema suave artesanal'] },
    { stem: 'cabra', aliases: ['queso de cabra', 'queso de cabra artesanal', 'cabra artesanal'] },
    { stem: 'crema', aliases: ['crema', 'crema entera', 'crema entera de rancho', 'crema para batir'], exclude: ['queso crema'] },
    // Grasas, Aceites y Semillas
    { stem: 'oliva', aliases: ['aceite de oliva', 'vevo', 'aceite de oliva extra virgen', 'aceite de oliva virgen extra', 'aceite de oliva extra virgen (vevo)'], exclude: ['aceituna', 'aceitunas'] },
    { stem: 'aceite-ajonjoli', aliases: ['aceite de ajonjoli', 'aceite de sesamo', 'aceite de ajonjoli tostado'], exclude: ['semilla', 'semillas', 'grano'] },
    { stem: 'semillas-sesamo', aliases: ['semillas de sesamo', 'semillas de ajonjoli', 'ajonjoli en grano', 'semilla de ajonjoli', 'semillas de sesamo (ajonjoli)'], exclude: ['aceite'] },
    { stem: 'nuez-pecana', aliases: ['nuez pecana', 'nueces pecana', 'pecana', 'pecanas'] },
    { stem: 'nuez-castilla', aliases: ['nuez de castilla', 'nueces de castilla', 'nuez de castilla fresca'] },
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
    { stem: 'limon', aliases: ['limon', 'limones', 'limones frescos', 'jugo de limon'] },
    { stem: 'ajo', aliases: ['ajo', 'ajos', 'ajo fresco', 'dientes de ajo'], exclude: ['ajonjoli'] },
    { stem: 'sal', aliases: ['sal de mar', 'sal de colima', 'sal mineral', 'sal de mar mineral de colima'] },
    { stem: '33plus', aliases: ['33plus', 'formula nootropica 33plus', 'formula biotecnologica nootropica 33plus'] },
    { stem: '34plus', aliases: ['34plus', 'formula reparadora 34plus', 'formula biotecnologica reparadora 34plus'] },
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

  return false;
}

const tests = [
  // 1. Pollo vs Huesos de Pollo (DEBEN SER DIFERENTES)
  ['Pechuga de pollo orgánica', 'Huesos y retazo de pollo orgánico para fondo', false],
  ['Pechuga de pollo', 'Huesos y retazo de pollo', false],
  // 2. Pollo vs Pollo (DEBEN SER IGUALES)
  ['Pechuga de pollo', 'Pechuga de pollo orgánica', true],
  ['Huesos y retazo de pollo', 'Huesos y retazo de pollo orgánico para fondo', true],
  // 3. Aceite de Ajonjolí vs Semillas de Sésamo (DEBEN SER DIFERENTES)
  ['Aceite de ajonjolí tostado', 'Semillas de sésamo (ajonjolí)', false],
  ['Aceite de ajonjolí', 'Semillas de ajonjolí', false],
  // 4. Aceite de Ajonjolí vs Aceite de Ajonjolí (DEBEN SER IGUALES)
  ['Aceite de ajonjolí', 'Aceite de ajonjolí tostado', true],
  ['Semillas de sésamo', 'Semillas de sésamo (ajonjolí)', true],
  // 5. Tuétano vs Res
  ['Huesos de res con tuétano para fondo', 'Medallones de Sirloin de res magro', false],
  ['Huesos de res con tuétano para fondo', 'Arrachera de res magra limpia', false],
  // 6. Ajo vs Ajonjolí (DEBEN SER DIFERENTES)
  ['Ajo fresco', 'Aceite de ajonjolí tostado', false],
  ['Dientes de ajo fresco', 'Semillas de sésamo (ajonjolí)', false]
];

let allPassed = true;
tests.forEach(([a, b, expected]) => {
  const result = areInsumosEquivalent(a, b);
  const pass = result === expected;
  if (!pass) allPassed = false;
  console.log(`${a} == ${b} -> ${result} (Expected: ${expected}) -> ${pass ? 'PASS' : 'FAIL'}`);
});

console.log('Result:', allPassed ? 'ALL TESTS PASSED 100%' : 'SOME TESTS FAILED');
