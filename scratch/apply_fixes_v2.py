import re

with open('generate_standalone_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update window.PANTRY_STOCK_INVENTORY for Item 17 Agua mineral
old_item_17 = '"sku-017-agua-mineral": { item_num: 17, name: "Agua mineral", stock: 9000, unit: "ml", packaging: "6 envases de 1500 ml", status: "canonical" },'
new_item_17 = '"sku-017-agua-mineral": { item_num: 17, name: "Agua mineral", stock: 6, unit: "botellas de 1500 ml", packaging: "6 botellas de 1500 ml", status: "canonical" },'
assert old_item_17 in content, "old_item_17 not found"
content = content.replace(old_item_17, new_item_17)

old_item_18 = '"sku-018-agua-mineral": { item_num: 18, name: "Agua mineral", stock: 355, unit: "ml", packaging: "355 ml", status: "canonical" },'
new_item_18 = '"sku-018-agua-mineral": { item_num: 18, name: "Agua mineral", stock: 1, unit: "botellas de 355 ml", packaging: "1 botella de 355 ml", status: "canonical" },'
assert old_item_18 in content, "old_item_18 not found"
content = content.replace(old_item_18, new_item_18)

# 2. Add getPieceGramWeight function before parseQuantityInBaseUnit
piece_weight_fn = """function getPieceGramWeight(itemName) {
  const n = (itemName || '').toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").trim();
  if (/morron|pimiento/i.test(n)) return 160; // 1 pimiento morrón ~160 g
  if (/pechuga|pollo/i.test(n)) return 500; // 1 pechuga de pollo entera ~500 g
  if (/calabacita|calabaza/i.test(n)) return 180; // 1 calabacita tierna ~180 g
  if (/flor de calabaza/i.test(n)) return 180; // 1 manojo de flor de calabaza ~180 g
  if (/lechuga/i.test(n)) return 380; // 1 pieza de lechuga ~380 g
  if (/jitomate|tomate saladet/i.test(n)) return 120; // 1 jitomate ~120 g
  if (/tomate verde|tomatillo/i.test(n)) return 60; // 1 tomate verde ~60 g
  if (/cebolla/i.test(n)) return 160; // 1 cebolla ~160 g
  if (/aguacate/i.test(n)) return 180; // 1 aguacate Hass ~180 g
  if (/zanahoria/i.test(n)) return 120; // 1 zanahoria ~120 g
  if (/elote/i.test(n)) return 250; // 1 elote ~250 g
  if (/huevo/i.test(n)) return 55; // 1 huevo ~55 g
  if (/chayote/i.test(n)) return 200; // 1 chayote ~200 g
  if (/pepino/i.test(n)) return 200; // 1 pepino ~200 g
  if (/limon/i.test(n)) return 40; // 1 limón ~40 g
  if (/ajo/i.test(n)) return 50; // 1 cabeza de ajo ~50 g
  return 100;
}

function parseQuantityInBaseUnit(qty, unitRaw) {"""

assert "function parseQuantityInBaseUnit(qty, unitRaw) {" in content
content = content.replace("function parseQuantityInBaseUnit(qty, unitRaw) {", piece_weight_fn)

# 3. Update getCommercialUnitOptions for pimientos, pollo, lechuga, calabaza, agua mineral
old_unit_options = """      // 6. Pollo y aves
      if (/pechuga.*pollo|carne.*pollo|pollo/i.test(name) && !/hueso|retazo|fondo|caldo/i.test(name)) {
        return [
          { id: 'paquete_3_2', label: 'Paquete Familiar (3.2 kg)', multiplier: 3200, unit: 'g', type: 'mass' },
          { id: 'kg', label: 'Kilo (1,000 g)', multiplier: 1000, unit: 'g', type: 'mass' },
          { id: 'g', label: 'Gramos (g)', multiplier: 1, unit: 'g', type: 'mass' }
        ];
      }"""

new_unit_options = """      // 5b. Pimientos morrones / Morrón (Canónico en Piezas o Gramos)
      if (/morron|pimiento/i.test(name)) {
        return [
          { id: 'piezas', label: 'Piezas (pzas ~160g)', multiplier: 1, unit: 'piezas', type: 'count' },
          { id: 'kg', label: 'Kilo (1,000 g)', multiplier: 1000, unit: 'g', type: 'mass' },
          { id: 'g', label: 'Gramos (g)', multiplier: 1, unit: 'g', type: 'mass' }
        ];
      }

      // 5c. Flor de calabaza y Lechugas
      if (/flor de calabaza/i.test(name)) {
        return [
          { id: 'manojo', label: 'Manojo (~180 g)', multiplier: 1, unit: 'manojo', type: 'count' },
          { id: 'g', label: 'Gramos (g)', multiplier: 1, unit: 'g', type: 'mass' }
        ];
      }
      if (/lechuga/i.test(name)) {
        return [
          { id: 'piezas', label: 'Piezas (pzas ~380g)', multiplier: 1, unit: 'piezas', type: 'count' },
          { id: 'kg', label: 'Kilo (1,000 g)', multiplier: 1000, unit: 'g', type: 'mass' },
          { id: 'g', label: 'Gramos (g)', multiplier: 1, unit: 'g', type: 'mass' }
        ];
      }
      if (/calabaza|calabacita/i.test(name)) {
        return [
          { id: 'piezas', label: 'Piezas (pzas ~180g)', multiplier: 1, unit: 'piezas', type: 'count' },
          { id: 'kg', label: 'Kilo (1,000 g)', multiplier: 1000, unit: 'g', type: 'mass' },
          { id: 'g', label: 'Gramos (g)', multiplier: 1, unit: 'g', type: 'mass' }
        ];
      }

      // 6. Pollo y aves
      if (/pechuga.*pollo|carne.*pollo|pollo/i.test(name) && !/hueso|retazo|fondo|caldo/i.test(name)) {
        return [
          { id: 'piezas', label: 'Piezas (pzas ~500g)', multiplier: 1, unit: 'piezas', type: 'count' },
          { id: 'paquete_3_2', label: 'Paquete Familiar (3.2 kg)', multiplier: 3200, unit: 'g', type: 'mass' },
          { id: 'kg', label: 'Kilo (1,000 g)', multiplier: 1000, unit: 'g', type: 'mass' },
          { id: 'g', label: 'Gramos (g)', multiplier: 1, unit: 'g', type: 'mass' }
        ];
      }"""

assert old_unit_options in content, "old_unit_options not found"
content = content.replace(old_unit_options, new_unit_options)

# 4. Update water in getCommercialUnitOptions
old_water_opt = """      // 8b. Agua purificada e hidratación
      if (/\\bagua\\b/i.test(name) && !/aguacate/i.test(name)) {
        return [
          { id: 'litros', label: 'Litros (L)', multiplier: 1000, unit: 'ml', type: 'vol' },
          { id: 'botellas (355 ml)', label: 'Botella (355 ml)', multiplier: 355, unit: 'ml', type: 'vol' },
          { id: 'ml', label: 'Mililitros (ml)', multiplier: 1, unit: 'ml', type: 'vol' }
        ];
      }"""

new_water_opt = """      // 8b. Agua mineral y agua purificada
      if (/agua mineral/i.test(name)) {
        return [
          { id: 'botellas de 1500 ml', label: 'Botella (1,500 ml / 1.5 L)', multiplier: 1500, unit: 'ml', type: 'vol' },
          { id: 'botellas de 355 ml', label: 'Botella / Lata (355 ml)', multiplier: 355, unit: 'ml', type: 'vol' },
          { id: 'litros', label: 'Litros (L)', multiplier: 1000, unit: 'ml', type: 'vol' },
          { id: 'ml', label: 'Mililitros (ml)', multiplier: 1, unit: 'ml', type: 'vol' }
        ];
      }
      if (/\\bagua\\b/i.test(name) && !/aguacate/i.test(name)) {
        return [
          { id: 'botellas de 355 ml', label: 'Botella (355 ml)', multiplier: 355, unit: 'ml', type: 'vol' },
          { id: 'litros', label: 'Litros (L)', multiplier: 1000, unit: 'ml', type: 'vol' },
          { id: 'ml', label: 'Mililitros (ml)', multiplier: 1, unit: 'ml', type: 'vol' }
        ];
      }"""

assert old_water_opt in content, "old_water_opt not found"
content = content.replace(old_water_opt, new_water_opt)

# 5. Update resolvePantryCommercialUnit
old_resolve_switch = "        case 'casillero':"
new_resolve_switch = """        case 'botellas de 1500 ml':
        case 'botellas (1500 ml)':
        case 'botella_1500':
          return { val: num * 1500, type: 'vol', baseUnit: 'ml' };
        case 'botellas de 355 ml':
        case 'botellas (355 ml)':
        case 'botella_355':
          return { val: num * 355, type: 'vol', baseUnit: 'ml' };
        case 'manojo':
          return { val: num, type: 'count', baseUnit: 'manojo' };
        case 'casillero':"""

assert old_resolve_switch in content, "old_resolve_switch not found"
content = content.replace(old_resolve_switch, new_resolve_switch, 1)

# 6. Update Alacena card rendering to display item.packaging cleanly
old_canon_render = """    canonicalPantry.forEach(k => {
      const item = pantryMap[k];
      let displayUnit = item.unit || '';
      if (displayUnit === 'bolsa_sal') displayUnit = 'bolsa (1 kg)';
      else if (displayUnit === 'botella_vevo') displayUnit = 'botella (750 ml)';
      html += `
        <div class="bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800 p-3 rounded-lg flex justify-between items-center">
          <div>
            <div class="font-bold text-xs text-slate-900 dark:text-slate-100">${item.name}</div>
            <div class="text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold mt-0.5">🟢 Apto / Canónico</div>
          </div>
          <div class="font-bold text-xs text-[#3AAA35] font-mono">${item.stock} ${displayUnit}</div>
        </div>
      `;
    });"""

new_canon_render = """    canonicalPantry.forEach(k => {
      const item = pantryMap[k];
      let displayQty = item.packaging ? item.packaging : `${item.stock} ${item.unit || ''}`;
      html += `
        <div class="bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800 p-3 rounded-lg flex justify-between items-center">
          <div>
            <div class="font-bold text-xs text-slate-900 dark:text-slate-100">${item.name}</div>
            <div class="text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold mt-0.5">🟢 Apto / Canónico</div>
          </div>
          <div class="font-bold text-xs text-[#3AAA35] font-mono">${displayQty}</div>
        </div>
      `;
    });"""

assert old_canon_render in content, "old_canon_render not found"
content = content.replace(old_canon_render, new_canon_render)

old_prohib_render = """    prohibitedPantry.forEach(k => {
      const item = pantryMap[k];
      html += `
        <div class="bg-rose-50/60 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800 p-3 rounded-lg flex justify-between items-center">
          <div>
            <div class="font-bold text-xs text-slate-900 dark:text-slate-100">${item.name}</div>
            <div class="text-[10px] text-rose-600 dark:text-rose-400 font-semibold mt-0.5">⚠️ Motivo: ${item.reason}</div>
          </div>
          <div class="font-bold text-xs text-rose-700 dark:text-rose-300 font-mono">${item.stock} ${item.unit}</div>
        </div>
      `;
    });"""

new_prohib_render = """    prohibitedPantry.forEach(k => {
      const item = pantryMap[k];
      let displayQty = item.packaging ? item.packaging : `${item.stock} ${item.unit || ''}`;
      html += `
        <div class="bg-rose-50/60 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800 p-3 rounded-lg flex justify-between items-center">
          <div>
            <div class="font-bold text-xs text-slate-900 dark:text-slate-100">${item.name}</div>
            <div class="text-[10px] text-rose-600 dark:text-rose-400 font-semibold mt-0.5">⚠️ Motivo: ${item.reason}</div>
          </div>
          <div class="font-bold text-xs text-rose-700 dark:text-rose-300 font-mono">${displayQty}</div>
        </div>
      `;
    });"""

assert old_prohib_render in content, "old_prohib_render not found"
content = content.replace(old_prohib_render, new_prohib_render)

# 7. Update Alacena deduction in render3DShoppingList
old_deduction_block = """    let stockInBase = 0;
    if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined' && window.PANTRY_STOCK_INVENTORY) {
      Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(pKey => {
        const pObj = window.PANTRY_STOCK_INVENTORY[pKey];
        if (!pObj || pObj.status !== 'canonical') return;

        if (areInsumosEquivalent(pObj.name || pKey, cleanName)) {
          const pQty = parseFloat(pObj.stock) || 0;
          let pUnit = (typeof window.pantryCardUnits !== 'undefined' && (window.pantryCardUnits[pObj.name] || window.pantryCardUnits[pKey])) || pObj.unit;
          if (!pUnit && typeof window.pantryCardUnits !== 'undefined') {
            const matchedUnitKey = Object.keys(window.pantryCardUnits).find(k => areInsumosEquivalent(k, cleanName));
            if (matchedUnitKey) pUnit = window.pantryCardUnits[matchedUnitKey];
          }
          if (!pUnit) pUnit = item.unit;
          let parsedStock = parseQuantityInBaseUnit(pQty, pUnit);
          // Clinical Safety Net: si la demanda es > 200g y pQty < 20 para carnes/pescados, interpretar como kg (a menos que ya sea empaque comercial)
          if (parsedStock.type === 'mass' && parsedStock.val < 20 && baseInfo.val > 200 && (cat.includes('Carne') || cat.includes('Proteína') || cat.includes('Pescado')) && !pUnit.includes('paquete') && !pUnit.includes('bolsa')) {
            parsedStock.val *= 1000;
          }
          stockInBase += parsedStock.val;
        }
      });
    }

    if (stockInBase === 0 && typeof pantryStock !== 'undefined' && pantryStock) {
      Object.keys(pantryStock).forEach(pName => {
        const pVal = parseFloat(pantryStock[pName]) || 0;
        if (pVal <= 0) return;
        if (areInsumosEquivalent(pName, cleanName)) {
          let pUnit = (typeof window.pantryCardUnits !== 'undefined' && window.pantryCardUnits[pName]) || null;
          if (!pUnit && typeof window.pantryCardUnits !== 'undefined') {
            const matchedUnitKey = Object.keys(window.pantryCardUnits).find(k => areInsumosEquivalent(k, cleanName));
            if (matchedUnitKey) pUnit = window.pantryCardUnits[matchedUnitKey];
          }
          if (!pUnit) pUnit = item.unit;
          let parsedStock = parseQuantityInBaseUnit(pVal, pUnit);
          // Clinical Safety Net: si la demanda es > 200g y pVal < 20 para carnes/pescados, interpretar como kg (a menos que ya sea empaque comercial)
          if (parsedStock.type === 'mass' && parsedStock.val < 20 && baseInfo.val > 200 && (cat.includes('Carne') || cat.includes('Proteína') || cat.includes('Pescado')) && !pUnit.includes('paquete') && !pUnit.includes('bolsa')) {
            parsedStock.val *= 1000;
          }
          stockInBase += parsedStock.val;
        }
      });
    }

    const netInBase = Math.max(0, baseInfo.val - stockInBase);

    if (netInBase <= 0) {
      pantryFullyCoveredCount++;
      pantryCoveredItems.push({
        name: item.item_name,
        slug: slug,
        reason: `🧀 Cubierto por Alacena (${formatBaseQuantity(stockInBase, baseInfo.type, item.unit)} disponibles)`,
        category: cat
      });
    } else {
      marketNetCount++;
      const netStr = formatBaseQuantity(netInBase, baseInfo.type, item.unit);
      const grossStr = formatBaseQuantity(baseInfo.val, baseInfo.type, item.unit);
      const pantryStr = formatBaseQuantity(stockInBase, baseInfo.type, item.unit);

      let note = "";
      if (slug === '33plus' || slug === '34plus') {
        note = "(Lote Interno Granja — Laboratorio $0 Mercado)";
      } else if (stockInBase > 0) {
        note = `(Bruto: ${grossStr} | Alacena: ${pantryStr})`;
      }"""

new_deduction_block = """    let stockInBase = 0;
    let matchedPantryObj = null;

    if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined' && window.PANTRY_STOCK_INVENTORY) {
      Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(pKey => {
        const pObj = window.PANTRY_STOCK_INVENTORY[pKey];
        if (!pObj || pObj.status !== 'canonical') return;

        if (areInsumosEquivalent(pObj.name || pKey, cleanName)) {
          matchedPantryObj = pObj;
          const pQty = parseFloat(pObj.stock) || 0;
          let pUnit = (typeof window.pantryCardUnits !== 'undefined' && (window.pantryCardUnits[pObj.name] || window.pantryCardUnits[pKey])) || pObj.unit;
          if (!pUnit && typeof window.pantryCardUnits !== 'undefined') {
            const matchedUnitKey = Object.keys(window.pantryCardUnits).find(k => areInsumosEquivalent(k, cleanName));
            if (matchedUnitKey) pUnit = window.pantryCardUnits[matchedUnitKey];
          }
          if (!pUnit) pUnit = item.unit;
          let parsedStock = parseQuantityInBaseUnit(pQty, pUnit);

          // Conversión Canónica de Conteos Físicos (piezas/manojo) a Masa (g) cuando la demanda BOM está en masa
          if (baseInfo.type === 'mass' && parsedStock.type === 'count') {
            const pieceWeight = getPieceGramWeight(cleanName);
            parsedStock.val = parsedStock.val * pieceWeight;
            parsedStock.type = 'mass';
            parsedStock.baseUnit = 'g';
            parsedStock.isPieceConversion = true;
            parsedStock.origPieces = pQty;
            parsedStock.origUnit = pUnit;
          } else if (baseInfo.type === 'count' && parsedStock.type === 'mass') {
            const pieceWeight = getPieceGramWeight(cleanName);
            parsedStock.val = pieceWeight > 0 ? (parsedStock.val / pieceWeight) : parsedStock.val;
            parsedStock.type = 'count';
            parsedStock.baseUnit = 'piezas';
          }

          // Clinical Safety Net: si la demanda es > 200g y pQty < 20 para carnes/pescados, interpretar como kg (a menos que ya sea empaque comercial o conteo de piezas)
          if (parsedStock.type === 'mass' && !parsedStock.isPieceConversion && parsedStock.val < 20 && baseInfo.val > 200 && (cat.includes('Carne') || cat.includes('Proteína') || cat.includes('Pescado')) && !pUnit.includes('paquete') && !pUnit.includes('bolsa')) {
            parsedStock.val *= 1000;
          }
          stockInBase += parsedStock.val;
        }
      });
    }

    if (stockInBase === 0 && typeof pantryStock !== 'undefined' && pantryStock) {
      Object.keys(pantryStock).forEach(pName => {
        const pVal = parseFloat(pantryStock[pName]) || 0;
        if (pVal <= 0) return;
        if (areInsumosEquivalent(pName, cleanName)) {
          let pUnit = (typeof window.pantryCardUnits !== 'undefined' && window.pantryCardUnits[pName]) || null;
          if (!pUnit && typeof window.pantryCardUnits !== 'undefined') {
            const matchedUnitKey = Object.keys(window.pantryCardUnits).find(k => areInsumosEquivalent(k, cleanName));
            if (matchedUnitKey) pUnit = window.pantryCardUnits[matchedUnitKey];
          }
          if (!pUnit) pUnit = item.unit;
          let parsedStock = parseQuantityInBaseUnit(pVal, pUnit);

          // Conversión Canónica de Conteos Físicos (piezas/manojo) a Masa (g) cuando la demanda BOM está en masa
          if (baseInfo.type === 'mass' && parsedStock.type === 'count') {
            const pieceWeight = getPieceGramWeight(cleanName);
            parsedStock.val = parsedStock.val * pieceWeight;
            parsedStock.type = 'mass';
            parsedStock.baseUnit = 'g';
            parsedStock.isPieceConversion = true;
            parsedStock.origPieces = pVal;
            parsedStock.origUnit = pUnit;
          } else if (baseInfo.type === 'count' && parsedStock.type === 'mass') {
            const pieceWeight = getPieceGramWeight(cleanName);
            parsedStock.val = pieceWeight > 0 ? (parsedStock.val / pieceWeight) : parsedStock.val;
            parsedStock.type = 'count';
            parsedStock.baseUnit = 'piezas';
          }

          // Clinical Safety Net: si la demanda es > 200g y pVal < 20 para carnes/pescados, interpretar como kg (a menos que ya sea empaque comercial o conteo de piezas)
          if (parsedStock.type === 'mass' && !parsedStock.isPieceConversion && parsedStock.val < 20 && baseInfo.val > 200 && (cat.includes('Carne') || cat.includes('Proteína') || cat.includes('Pescado')) && !pUnit.includes('paquete') && !pUnit.includes('bolsa')) {
            parsedStock.val *= 1000;
          }
          stockInBase += parsedStock.val;
        }
      });
    }

    const netInBase = Math.max(0, baseInfo.val - stockInBase);

    if (netInBase <= 0) {
      pantryFullyCoveredCount++;
      let coveredReason = `🧀 Cubierto por Alacena (${formatBaseQuantity(stockInBase, baseInfo.type, item.unit)} disponibles)`;
      if (matchedPantryObj && matchedPantryObj.packaging) {
        coveredReason = `🧀 Cubierto por Alacena (${matchedPantryObj.packaging} / ~${formatBaseQuantity(stockInBase, baseInfo.type, item.unit)} disponibles)`;
      } else if (matchedPantryObj && (matchedPantryObj.unit === 'piezas' || matchedPantryObj.unit === 'manojo')) {
        coveredReason = `🧀 Cubierto por Alacena (${matchedPantryObj.stock} ${matchedPantryObj.unit} / ~${formatBaseQuantity(stockInBase, baseInfo.type, item.unit)} disponibles)`;
      }
      pantryCoveredItems.push({
        name: item.item_name,
        slug: slug,
        reason: coveredReason,
        category: cat
      });
    } else {
      marketNetCount++;
      const netStr = formatBaseQuantity(netInBase, baseInfo.type, item.unit);
      const grossStr = formatBaseQuantity(baseInfo.val, baseInfo.type, item.unit);
      let pantryStr = formatBaseQuantity(stockInBase, baseInfo.type, item.unit);
      if (matchedPantryObj && matchedPantryObj.packaging) {
        pantryStr = `${matchedPantryObj.packaging} (~${formatBaseQuantity(stockInBase, baseInfo.type, item.unit)})`;
      } else if (matchedPantryObj && (matchedPantryObj.unit === 'piezas' || matchedPantryObj.unit === 'manojo')) {
        pantryStr = `${matchedPantryObj.stock} ${matchedPantryObj.unit} (~${formatBaseQuantity(stockInBase, baseInfo.type, item.unit)})`;
      }

      let note = "";
      if (slug === '33plus' || slug === '34plus' || slug.includes('multisinergix') || slug.includes('aminosinergix')) {
        note = "(Lote Interno Granja — Laboratorio $0 Mercado)";
      } else if (stockInBase > 0) {
        note = `(Bruto: ${grossStr} | Alacena: ${pantryStr})`;
      }"""

assert old_deduction_block in content, "old_deduction_block not found"
content = content.replace(old_deduction_block, new_deduction_block)

# 8. Update initSetupPanel to ONLY list physical items from PANTRY_STOCK_INVENTORY (no BOM ghost items)
old_setup_panel_loop = """        // 2.1 Insumos del BOM Canónico del Menú Activo (Semana 40)
        const activeBom = (typeof ACTIVE_WEEK_40_CANONICAL_BOM !== 'undefined' && Array.isArray(ACTIVE_WEEK_40_CANONICAL_BOM) && ACTIVE_WEEK_40_CANONICAL_BOM.length > 0)
          ? ACTIVE_WEEK_40_CANONICAL_BOM
          : (typeof rawShopBase !== 'undefined' ? rawShopBase : []);

        activeBom.forEach(bItem => {
          const bName = bItem.name || bItem.item_name;
          if (!bName) return;
          const cat = getSmartItemCategory(bName, bItem.category);
          // Proyección Reflexiva Total del BOM a la Alacena (Directiva SSOT):
          // Un insumo sólo se excluye de la Alacena si está actualmente marcado en Cosecha (selectedHarvest).
          // Si no está en Cosecha, TIENE que estar en Alacena para posibilitar su amortización física.
          const isCurrentlyHarvested = selectedHarvest.some(h => {
            const hStr = typeof h === 'string' ? h : (h.item_name || h.name || '');
            return areInsumosEquivalent(hStr, bName);
          });
          if (isCurrentlyHarvested) return;

          const slug = normalizeToCanonicalSlug(bName);
          if (deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === bName.toLowerCase())) return;

          // Deduplicación estricta por equivalencia léxica
          const alreadyInList = nonFarm.some(existing => areInsumosEquivalent(existing.item_name, bName));
          if (!alreadyInList) {
            seenPantrySlugs.add(slug);
            nonFarm.push({
              item_name: bName,
              quantity: bItem.quantity || bItem.amount || 0,
              unit: bItem.unit || 'g',
              category: cat
            });
          }
        });

        // 2.2 Insumos Canónicos y Registrados Activos en Inventario Físico de Alacena (con stock declarado)
        if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined') {
          Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(k => {
            const pObj = window.PANTRY_STOCK_INVENTORY[k];
            if (!pObj) return;
            const slug = normalizeToCanonicalSlug(pObj.name || k);
            if (deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === pObj.name.toLowerCase())) return;
            const alreadyInList = nonFarm.some(existing => areInsumosEquivalent(existing.item_name, pObj.name));
            if (!alreadyInList) {
              seenPantrySlugs.add(slug);
              const assignedCat = (pObj.status === 'prohibited')
                ? '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)'
                : (pObj.category || getSmartItemCategory(pObj.name));
              nonFarm.push({
                item_name: pObj.name,
                quantity: 0,
                unit: pObj.unit || 'g',
                category: assignedCat,
                status: pObj.status || 'canonical'
              });
            }
          });
        }"""

new_setup_panel_loop = """        // 2.1 Insumos Físicos de Despensa (window.PANTRY_STOCK_INVENTORY)
        // Regla de Oro: En Reconfigurar Parámetros sólo se muestran los 106 insumos que realmente existen en el inventario físico de la despensa.
        // const isCurrentlyHarvested = selectedHarvest.some(h => areInsumosEquivalent(h, 'test'));
        if (typeof window.PANTRY_STOCK_INVENTORY !== 'undefined') {
          Object.keys(window.PANTRY_STOCK_INVENTORY).forEach(k => {
            const pObj = window.PANTRY_STOCK_INVENTORY[k];
            if (!pObj) return;
            // Excluir claves de compatibilidad interna con stock 0 (como frutas de catálogo o ajo-fresco de test)
            if (pObj.stock <= 0 && (!pObj.item_num || pObj.item_num <= 0)) return;
            // Excluir alias duplicados para no repetir el mismo ítem en la pantalla
            if (k === 'multisinergix' || k === 'aminosinergix' || k === '33plus' || k === '34plus' || k === 'zarzamoras-frescas' || k === 'fresas-frescas' || k === 'arilos-granada' || k === 'moras-frescas' || k === 'frambuesas-frescas' || k === 'arandanos-frescos' || k === 'pitaya-fresca' || k === 'ajo-fresco') return;

            const slug = normalizeToCanonicalSlug(pObj.name || k);
            if (deletedPantryItems.some(d => normalizeToCanonicalSlug(d) === slug || d.toLowerCase() === pObj.name.toLowerCase())) return;
            const alreadyInList = nonFarm.some(existing => areInsumosEquivalent(existing.item_name, pObj.name));
            if (!alreadyInList) {
              seenPantrySlugs.add(slug);
              const assignedCat = (pObj.status === 'prohibited')
                ? '🛑 Insumos No Sugeridos / Cuarentena (No usar en Protocolo Cetogénico)'
                : (pObj.category || getSmartItemCategory(pObj.name));
              nonFarm.push({
                item_name: pObj.name,
                quantity: pObj.stock,
                unit: pObj.unit || 'g',
                category: assignedCat,
                status: pObj.status || 'canonical',
                packaging: pObj.packaging
              });
            }
          });
        }"""

assert old_setup_panel_loop in content, "old_setup_panel_loop not found"
content = content.replace(old_setup_panel_loop, new_setup_panel_loop)

# 9. Bump version to force fresh load in client browsers
content = content.replace(
    "const CURRENT_APP_VERSION = 'v42_pantry_106_canonical_skus';",
    "const CURRENT_APP_VERSION = 'v42_2_pantry_exact_packaging_units';"
)
content = content.replace(
    "const LOCAL_STORAGE_KEY = 'nutriketo_app_state_v42_106_canonical';",
    "const LOCAL_STORAGE_KEY = 'nutriketo_app_state_v42_2_exact_units';"
)

with open('generate_standalone_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied fixes v2 successfully!")
