import re

with open('scratch/pantry_inventory_block.js', 'r', encoding='utf-8') as f:
    new_pantry_inventory = f.read().strip()

with open('scratch/pantry_stock_block.js', 'r', encoding='utf-8') as f:
    new_pantry_stock = f.read().strip()

with open('generate_standalone_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace PANTRY_STOCK_INVENTORY
pattern_inventory = r'    window\.PANTRY_STOCK_INVENTORY = \{.*?\n    \};'
assert re.search(pattern_inventory, content, re.DOTALL), "Could not find window.PANTRY_STOCK_INVENTORY block"
content = re.sub(pattern_inventory, new_pantry_inventory, content, count=1, flags=re.DOTALL)

# 2. Replace pantryStock
pattern_stock = r'    let pantryStock = \{.*?\n    \};'
assert re.search(pattern_stock, content, re.DOTALL), "Could not find pantryStock block"
content = re.sub(pattern_stock, new_pantry_stock, content, count=1, flags=re.DOTALL)

# 3. Version bump
content = content.replace(
    "const CURRENT_APP_VERSION = 'v40_2_ssot_canonical_skus';",
    "const CURRENT_APP_VERSION = 'v42_pantry_106_canonical_skus';"
)
content = content.replace(
    "const LOCAL_STORAGE_KEY = 'nutriketo_app_state_v40_2_ssot';",
    "const LOCAL_STORAGE_KEY = 'nutriketo_app_state_v42_106_canonical';"
)

# 4. Canonical name replacement
content = content.replace(
    "if (/multi sinergix|fórmula nootrópica|formula nootropica/i.test(lower)) return 'Fórmula Nootrópica 33Plus®';",
    "if (/multi sinergix|multisinergix|33plus|fórmula nootrópica|formula nootropica/i.test(lower)) return 'MultiSinergix®';"
)
content = content.replace(
    "if (/amino sinergix|fórmula reparadora|formula reparadora/i.test(lower)) return 'Fórmula Reparadora 34Plus®';",
    "if (/amino sinergix|aminosinergix|34plus|fórmula reparadora|formula reparadora/i.test(lower)) return 'AminoSinergix®';"
)

# 5. Stems in areInsumosEquivalent
old_stem = "{ stem: '33plus', aliases: ['33plus', 'formula nootropica 33plus', 'formula biotecnologica nootropica 33plus'] },"
new_stem = """{ stem: 'multisinergix', aliases: ['multisinergix', 'multi sinergix', '33plus', '33 plus', 'formula nootropica 33plus', 'formula biotecnologica nootropica 33plus', 'formula nootropica multisinergix'] },
        { stem: 'aminosinergix', aliases: ['aminosinergix', 'amino sinergix', '34plus', '34 plus', 'formula reparadora 34plus', 'formula biotecnologica reparadora 34plus', 'formula reparadora aminosinergix'] },
        { stem: 'flat-steak', aliases: ['flat steak', 'flatsteak', 'bife plano', 'steak flat'] },
        { stem: 'cottage', aliases: ['queso cottage', 'cottage'] },
        { stem: 'philadelphia', aliases: ['queso philadelphia', 'philadelphia', 'queso crema philadelphia'] },
        { stem: 'nogada', aliases: ['nogada'] },
        { stem: '33plus', aliases: ['33plus', 'formula nootropica 33plus', 'formula biotecnologica nootropica 33plus', 'multisinergix'] },"""
content = content.replace(old_stem, new_stem)

old_34plus_stem = "{ stem: '34plus', aliases: ['34plus', 'formula reparadora 34plus', 'formula biotecnologica reparadora 34plus'] },"
new_34plus_stem = "{ stem: '34plus', aliases: ['34plus', 'formula reparadora 34plus', 'formula biotecnologica reparadora 34plus', 'aminosinergix'] },"
content = content.replace(old_34plus_stem, new_34plus_stem)

# 6. Commercial unit options for MultiSinergix / AminoSinergix
old_unit_options = """      // 13. Suplementos 33Plus / 34Plus
      if (/33plus|34plus/i.test(name)) {
        return [
          { id: 'frasco_120', label: 'Frasco Lote (120 g)', multiplier: 120, unit: 'g', type: 'mass' },
          { id: 'g', label: 'Gramos (g)', multiplier: 1, unit: 'g', type: 'mass' }
        ];
      }"""
new_unit_options = """      // 13. Suplementos MultiSinergix® / AminoSinergix® (33Plus / 34Plus)
      if (/multisinergix|aminosinergix|33plus|34plus/i.test(name)) {
        return [
          { id: 'g', label: 'Gramos (g)', multiplier: 1, unit: 'g', type: 'mass' },
          { id: 'frasco_300', label: 'Envase (300 g)', multiplier: 300, unit: 'g', type: 'mass' },
          { id: 'frasco_200', label: 'Envase (200 g)', multiplier: 200, unit: 'g', type: 'mass' },
          { id: 'frasco_120', label: 'Frasco Lote (120 g)', multiplier: 120, unit: 'g', type: 'mass' }
        ];
      }"""
content = content.replace(old_unit_options, new_unit_options)

# 7. INGREDIENT_CANONICAL_MAP_JS
old_canon_map = """  "33plus": ["33plus", "33 plus", "fórmula 33plus", "elixir 33plus"],
  "34plus": ["34plus", "34 plus", "fórmula 34plus", "tisana 34plus"]"""
new_canon_map = """  "multisinergix": ["multisinergix", "multi sinergix", "33plus", "33 plus", "fórmula 33plus", "elixir 33plus"],
  "aminosinergix": ["aminosinergix", "amino sinergix", "34plus", "34 plus", "fórmula 34plus", "tisana 34plus"],
  "33plus": ["33plus", "33 plus", "fórmula 33plus", "elixir 33plus", "multisinergix"],
  "34plus": ["34plus", "34 plus", "fórmula 34plus", "tisana 34plus", "aminosinergix"]"""
content = content.replace(old_canon_map, new_canon_map)

# 8. loadAppState version purge and migration
old_load_version = """        const storedVersion = localStorage.getItem('nutriketo_app_version');
        if (storedVersion !== CURRENT_APP_VERSION) {
          console.warn('Detectada versión obsoleta/corrupta de localStorage. Purgando claves de versiones anteriores e inicializando SSOT V36.6 canónico.');
          const legacyKeys = [
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
          return false;
        }"""

new_load_version = """        const storedVersion = localStorage.getItem('nutriketo_app_version');
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
        }"""
content = content.replace(old_load_version, new_load_version)

# 9. Disable SAMS_TICKET_KEYS in loadAppState
old_sams_block = """            // Garantizar ingesta del comprobante Sam's Club Periférico Cuautitlán (03/10/2026)
            const SAMS_TICKET_KEYS = [
              'sardinas', 'atun-latas', 'salmon-lomo', 'ribeye-corte', 'fajita-mojarra',
              'hamburguesa-arrachera', 'queso-ricotta', 'crema-acida', 'oikos-prot',
              'nuez-india', 'lechuga-sweet', 'agua-mineral', 'agua-purificada'
            ];
            if (!state.samsReceiptProcessed_20261003) {
              if (state.pantryStockInventory['sardinas']) {
                state.pantryStockInventory['sardinas'].stock = Math.max(state.pantryStockInventory['sardinas'].stock || 0, 8);
              }
              SAMS_TICKET_KEYS.forEach(k => {
                if (window.PANTRY_STOCK_INVENTORY[k]) {
                  state.pantryStockInventory[k] = Object.assign({}, window.PANTRY_STOCK_INVENTORY[k]);
                }
              });
              state.samsReceiptProcessed_20261003 = true;
            }"""

new_sams_block = """            // Comprobante Sam's Club 03/10/2026 reemplazado por inventario físico canónico de 106 insumos"""
content = content.replace(old_sams_block, new_sams_block)

# 10. Quarantine items in initSetupPanel
old_quarantine_items = """        // 2.3 Insumos en Cuarentena (siempre presentes en su bloque al fondo)
        const QUARANTINE_PANTRY_ITEMS = [
          { item_name: 'Papa fresca', unit: 'kg', category: '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)' },
          { item_name: 'Lentejas', unit: 'g', category: '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)' },
          { item_name: 'Garbanzo', unit: 'g', category: '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)' },
          { item_name: 'Frijol', unit: 'g', category: '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)' },
          { item_name: 'Arroz tradicional', unit: 'g', category: '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)' },
          { item_name: 'Harina de trigo tradicional', unit: 'g', category: '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)' },
          { item_name: 'Aceite vegetal mixto comercial', unit: 'ml', category: '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)' }
        ];"""

new_quarantine_items = """        // 2.3 Insumos en Cuarentena (extraídos dinámicamente de window.PANTRY_STOCK_INVENTORY)
        const QUARANTINE_PANTRY_ITEMS = [];"""
content = content.replace(old_quarantine_items, new_quarantine_items)

# 11. WhatsApp schedule text
old_wa_text = """      text += "  • ☀️ TOMA 1 (Al Despertar): Fórmula Nootrópica 33Plus® (CoQ10/PQQ ayunas)\\n";
      text += "  • 🍳 TOMA 2 (Desayuno): Fórmula Nootrópica 33Plus® (Soporte enzimático)\\n";
      text += "  • 🥗 TOMA 3 (Cena): Fórmula Reparadora 34Plus® (Péptidos y electrolitos)\\n";
      text += "  • 🌙 TOMA 4 (Al Dormir): Fórmula Reparadora 34Plus® (Cross-linking & Mg)\\n\\n";"""

new_wa_text = """      text += "  • ☀️ TOMA 1 (Al Despertar): MultiSinergix® (CoQ10/PQQ ayunas - antes Fórmula 33Plus®)\\n";
      text += "  • 🍳 TOMA 2 (Desayuno): MultiSinergix® (Soporte enzimático)\\n";
      text += "  • 🥗 TOMA 3 (Cena): AminoSinergix® (Péptidos y electrolitos - antes Fórmula 34Plus®)\\n";
      text += "  • 🌙 TOMA 4 (Al Dormir): AminoSinergix® (Cross-linking & Mg)\\n\\n";"""
content = content.replace(old_wa_text, new_wa_text)

# 12. Modal label
content = content.replace(
    "🌿 3. Acompañamiento / Elixir Bioactivo (33Plus® Desayuno / 34Plus® Cena):",
    "🌿 3. Acompañamiento / Elixir Bioactivo (MultiSinergix® Desayuno / AminoSinergix® Cena):"
)

# 13. Service Worker version in registration
content = content.replace(
    "navigator.serviceWorker.register('./sw.js?v=nutriketo-v36-6-rev4-s41-service-checkin-v28')",
    "navigator.serviceWorker.register('./sw.js?v=nutriketo-v36-6-rev4-s41-service-checkin-v29')"
)

with open('generate_standalone_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied pantry update to generate_standalone_html.py successfully!")
