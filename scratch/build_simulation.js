const fs = require('fs');

const htmlGen = fs.readFileSync('generate_standalone_html.py', 'utf8');

// Extract the required functions and variables
const extractVar = (name) => {
  const m = htmlGen.match(new RegExp(`(?:let|const|var)\\s+${name}\\s*=\\s*([\\s\\S]*?);\\n`));
  return m ? m[0] : '';
};

// Write a standalone node runner that runs the shopping list calculation for Week 41
const s41 = JSON.parse(fs.readFileSync('semana_41_master.json', 'utf8'));

// Build list of ingredients from s41
let ingredientsBOM = [];
s41.days.forEach(d => {
  d.meals.forEach(m => {
    ['starter', 'main_dish', 'dessert', 'side_dish', 'side', 'drink', 'main'].forEach(c => {
      if (m[c] && m[c].ingredients) {
        m[c].ingredients.forEach(ing => {
          ingredientsBOM.push({
            name: ing.name,
            item_name: ing.name,
            quantity: ing.amount,
            unit: ing.unit,
            category: ing.category
          });
        });
      }
    });
  });
});

console.log("Total raw BOM ingredients:", ingredientsBOM.length);

const testScript = `
const fs = require('fs');

// We need DOM stubs or variables
let harvestList = ["Espinacas frescas", "Calabacitas verdes tiernas", "Brócoli fresco", "Espárragos verdes", "Nopales tiernos", "Ejotes frescos", "Cilantro fresco", "Arúgula fresca", "Coliflor fresca", "Limones agrios frescos de la granja", "Nuez pecana fresca de la granja"];

${htmlGen.match(/function stripAccents[\s\S]*?^\}/m)[0]}
${htmlGen.match(/const INGREDIENT_CANONICAL_MAP_JS = \{[\s\S]*?\};/m)[0]}
${htmlGen.match(/function normalizeToCanonicalSlug[\s\S]*?^function /m)[0].replace(/^function $/m, '')}
${htmlGen.match(/function getPieceGramWeight[\s\S]*?^\}/m)[0]}
${htmlGen.match(/function resolvePantryCommercialUnit[\s\S]*?^\}/m)[0]}
${htmlGen.match(/function parseQuantityInBaseUnit[\s\S]*?^\}/m)[0]}
${htmlGen.match(/function getYieldFactor[\s\S]*?^\}/m)[0]}
${htmlGen.match(/function formatBaseQuantity[\s\S]*?^\}/m)[0]}
${htmlGen.match(/function getSmartItemCategory[\s\S]*?^\}/m)[0]}
${htmlGen.match(/function areInsumosEquivalent[\s\S]*?^    \}/m)[0]}

${htmlGen.match(/window\.PANTRY_STOCK_INVENTORY = \{[\s\S]*?\};/m)[0]}

const ingredientsBOM = ${JSON.stringify(ingredientsBOM)};

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
  const cat = catSmart ? catSmart.replace(/\\s*\\/\\s*/g, ' — ').replace(/\\//g, ' — ') : '🛒 Abarrotes y Frescos';

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
`;

fs.writeFileSync('scratch/simulate_shopping.js', testScript);
console.log("Wrote scratch/simulate_shopping.js");
