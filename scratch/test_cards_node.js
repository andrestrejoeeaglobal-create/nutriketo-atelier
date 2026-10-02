const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');

// Extract getSmartItemCategory definition and calculateActiveMenuBOM or calculateNetShoppingList
// Or evaluate with minimal sandbox
const vm = require('vm');

const sandbox = {
  console: console,
  window: {},
  navigator: { userAgent: 'node' },
  tailwind: { config: {} },
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  matchMedia: () => ({ matches: false, addEventListener: () => {} }),
  document: {
    addEventListener: () => {},
    documentElement: { classList: { add: () => {}, remove: () => {}, toggle: () => {} } },
    getElementById: () => ({ style: {}, classList: { add: () => {}, remove: () => {} }, innerHTML: '', textContent: '', appendChild: () => {}, addEventListener: () => {} }),
    createElement: () => ({ style: {}, classList: { add: () => {}, remove: () => {} }, innerHTML: '', textContent: '', appendChild: () => {}, setAttribute: () => {} }),
    querySelector: () => null,
    querySelectorAll: () => []
  }
};
sandbox.window = sandbox;
vm.createContext(sandbox);

// Extract scripts from html
const scriptMatches = [...html.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi)];
let allCode = '';
for (const m of scriptMatches) {
  allCode += m[1] + '\n;';
}

// Let's run in sandbox
try {
  vm.runInContext(allCode, sandbox);
  console.log('App code executed successfully in sandbox.');

  if (typeof sandbox.calculateNetShoppingList === 'function') {
    const res = sandbox.calculateNetShoppingList(6);
    console.log('\n=== CARDS GENERATED ===');
    for (const cat of Object.keys(res.categories || {})) {
      console.log(`\nCard: [${cat}] (${res.categories[cat].length} items):`);
      for (const it of res.categories[cat]) {
        console.log(`  - ${it.name}: ${it.displayQty} ${it.note || ''}`);
      }
    }
  } else {
    console.log('calculateNetShoppingList not found directly in sandbox');
  }
} catch (e) {
  console.error('Error running sandbox:', e.message);
}
