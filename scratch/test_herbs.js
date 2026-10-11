const fs = require('fs');
const html = fs.readFileSync('atelier.html', 'utf8');

// Extract areInsumosEquivalent function from HTML
const match = html.match(/function areInsumosEquivalent\(aName, bName\) \{[\s\S]*?\n    \}/);
if (!match) {
  console.error("Function areInsumosEquivalent not found");
  process.exit(1);
}

// We also need normalizeToCanonicalSlug and stripAccents and INGREDIENT_CANONICAL_MAP_JS
const slugMatch = html.match(/function normalizeToCanonicalSlug\(rawName\) \{[\s\S]*?\n\}/);
const stripMatch = html.match(/function stripAccents\(str\) \{[\s\S]*?\n\}/);
const mapMatch = html.match(/const INGREDIENT_CANONICAL_MAP_JS = \{[\s\S]*?\n\};/);

const testCode = `
${stripMatch[0]}
${mapMatch[0]}
${slugMatch[0]}
${match[0]}

console.log("Romero vs Romero fresco:", areInsumosEquivalent("Romero", "Romero fresco"));
console.log("Romero fresco vs Romero:", areInsumosEquivalent("Romero fresco", "Romero"));
console.log("Epazote vs Epazote fresco:", areInsumosEquivalent("Epazote", "Epazote fresco"));
console.log("Eneldo vs Eneldo fresco:", areInsumosEquivalent("Eneldo", "Eneldo fresco"));
console.log("Albahaca vs Albahaca fresca:", areInsumosEquivalent("Albahaca", "Albahaca fresca"));

if (!areInsumosEquivalent("Romero", "Romero fresco")) process.exit(1);
if (!areInsumosEquivalent("Epazote", "Epazote fresco")) process.exit(1);
console.log("ALL HERB EQUIVALENCES PASS!");
`;

eval(testCode);
