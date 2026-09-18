import json
import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch_s38_canonical.json', 'r', encoding='utf-8') as f:
    canonical_data = json.load(f)

test_js = '''
const canonicalData = ''' + json.dumps(canonical_data, ensure_ascii=False) + ''';

function normalizeToCanonicalSlug(name) {
  if (!name) return '';
  const cleanNoAcc = name.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
  return cleanNoAcc.replace(/[^a-z0-9\\s-]/g, '').trim().replace(/\\s+/g, '-');
}

let selectedHarvest = [
  "Espinacas frescas",
  "Calabacitas verdes tiernas",
  "Brócoli fresco",
  "Espárragos verdes",
  "Nopales tiernos",
  "Ejotes frescos",
  "Cilantro fresco",
  "Arúgula fresca",
  "Coliflor fresca"
  // Note: "Higos frescos" and "Granada fresca" are NOT selected!
];

function calcShopping(numDiners, harvestList) {
  let totalCount = 0;
  let farmCount = 0;
  let marketNetCount = 0;

  let allItems = [];
  for (const catKey in canonicalData.bom) {
    allItems = allItems.concat(canonicalData.bom[catKey]);
  }

  totalCount = allItems.length;

  const farmItems = [];
  const marketItems = [];

  allItems.forEach(item => {
    const cat = item.category;
    const name = item.name || item.item_name;
    const itemSlug = normalizeToCanonicalSlug(item.canonical_id || name);
    const cleanLower = name.toLowerCase();

    const isHarvest = harvestList.some(h => {
      if (!h) return false;
      const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
      const hSlug = normalizeToCanonicalSlug(hStr);
      const hLower = hStr.toLowerCase();
      return (hSlug && itemSlug && (hSlug === itemSlug || itemSlug.includes(hSlug) || hSlug.includes(itemSlug))) ||
             (hLower && cleanLower && (hLower === cleanLower || cleanLower.includes(hLower) || hLower.includes(cleanLower)));
    });

    if (isHarvest) {
      farmCount++;
      farmItems.push(name);
    } else {
      marketNetCount++;
      marketItems.push({ name, cat });
    }
  });

  return { totalCount, farmCount, marketNetCount, farmItems, marketItems };
}

console.log("=== TEST 1: Higos frescos UNCHECKED ===");
let res1 = calcShopping(6, selectedHarvest);
console.log("Farm count:", res1.farmCount);
console.log("Market count:", res1.marketNetCount);
console.log("Higos in Farm?", res1.farmItems.includes("Higos frescos de la granja"));
console.log("Higos in Market?", res1.marketItems.some(i => i.name.includes("Higos")));

console.log("=== TEST 2: Higos frescos CHECKED ===");
selectedHarvest.push("Higos frescos");
let res2 = calcShopping(6, selectedHarvest);
console.log("Farm count:", res2.farmCount);
console.log("Market count:", res2.marketNetCount);
console.log("Higos in Farm?", res2.farmItems.includes("Higos frescos de la granja"));
console.log("Higos in Market?", res2.marketItems.some(i => i.name.includes("Higos")));
'''

with open('temp_test_harvest.js', 'w', encoding='utf-8') as f:
    f.write(test_js)

res = subprocess.run(['node', 'temp_test_harvest.js'], capture_output=True, text=True, encoding='utf-8')
print("STDOUT:", res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)

if os.path.exists('temp_test_harvest.js'):
    os.remove('temp_test_harvest.js')
