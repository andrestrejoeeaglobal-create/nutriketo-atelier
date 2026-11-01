const fs = require('fs');

const htmlGen = fs.readFileSync('generate_standalone_html.py', 'utf8');

// Extract areInsumosEquivalent function from htmlGen
const areEqMatch = htmlGen.match(/function areInsumosEquivalent[\s\S]*?^    \}/m);
if (!areEqMatch) {
  console.log("Could not find areInsumosEquivalent");
  process.exit(1);
}

// Let's also check INGREDIENT_CANONICAL_MAP_JS and normalizeToCanonicalSlug
const canonicalMapMatch = htmlGen.match(/const INGREDIENT_CANONICAL_MAP_JS = \{[\s\S]*?\};/m);
const normSlugMatch = htmlGen.match(/function normalizeToCanonicalSlug[\s\S]*?^function /m);
const stripAccMatch = htmlGen.match(/function stripAccents[\s\S]*?^\}/m);

const scriptToRun = `
${stripAccMatch ? stripAccMatch[0] : 'function stripAccents(s){return s;}'}
${canonicalMapMatch ? canonicalMapMatch[0] : 'const INGREDIENT_CANONICAL_MAP_JS={};'}
${normSlugMatch ? normSlugMatch[0].replace(/^function $/m, '') : ''}
${areEqMatch[0]}

console.log("Equivalent('Sardinas enlatadas', 'Sardina en salsa de tomate'):", areInsumosEquivalent('Sardinas enlatadas', 'Sardina en salsa de tomate'));
console.log("Equivalent('Sardina en salsa de tomate', 'Sardinas enlatadas'):", areInsumosEquivalent('Sardina en salsa de tomate', 'Sardinas enlatadas'));
console.log("Equivalent('Pechuga de pollo', 'Pechuga de pavo artesanal'):", areInsumosEquivalent('Pechuga de pollo', 'Pechuga de pavo artesanal'));
console.log("Equivalent('Pechuga de pollo orgánica', 'Pechuga de pollo'):", areInsumosEquivalent('Pechuga de pollo orgánica', 'Pechuga de pollo'));
`;

fs.writeFileSync('scratch/test_equiv.js', scriptToRun);
