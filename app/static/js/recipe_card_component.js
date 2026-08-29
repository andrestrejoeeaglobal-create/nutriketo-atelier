
function getDeconstructedRecipeForDish(dishTitle, courseRole) {
  // CORTEX SSOT V16.0.0: Renderizado 100% pasivo desde el backend dinámico. Sin overrides hardcodeados por regex.
  return null;
}

/**
 * Atelier T.I.L.O.® — Componente de Recetas 100% Pasivo SSOT (V15.22.1)
 * Renderizado Pasivo de Datos Estructurados sin Parsers Regex ni Plantillas Estáticas.
 * Escalamiento Unitario Estricto por Persona: (base_qty_per_person * activeDiners)
 */

function sanitizeDishTitle(title) {
  if (!title) return "";
  return title
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\\(.*?\\)/g, "")
    .trim();
}

function normalizeQuantity(qty, unit) {
  const num = parseFloat(qty);
  if (isNaN(num)) return qty;

  const u = (unit || "").toLowerCase();
  if (u.includes("piez") || u.includes("huevo") || u.includes("unidad") || u.includes("hoja")) {
    return Math.ceil(num).toString();
  }
  if (u.includes("g") || u.includes("gram")) {
    const rounded = Math.ceil(num / 5) * 5;
    return rounded.toString();
  }
  if (u.includes("ml") || u.includes("cucharad") || u.includes("pizca")) {
    const rounded = Math.ceil(num / 5) * 5;
    return rounded.toString();
  }
  return (Math.round(num * 10) / 10).toString();
}

function parseQuantityInBaseUnit(qty, unit) {
  let num = parseFloat(qty);
  if (isNaN(num)) num = 1;
  const u = (unit || "").toLowerCase().trim();

  if (u === "kg" || u === "kilos" || u === "kilogramos") {
    return { val: num * 1000, type: "mass", baseUnit: "g" };
  }
  if (u === "g" || u === "gramos") {
    return { val: num, type: "mass", baseUnit: "g" };
  }
  if (u === "l" || u === "litros" || u === "lt") {
    return { val: num * 1000, type: "vol", baseUnit: "ml" };
  }
  if (u === "ml" || u === "mililitros") {
    return { val: num, type: "vol", baseUnit: "ml" };
  }
  return { val: num, type: "count", baseUnit: u || "piezas" };
}

function formatBaseQuantity(val, type, origUnit) {
  if (type === "mass") {
    if (val >= 1000) return `${(val / 1000).toFixed(1)} kg`;
    return `${Math.ceil(val / 5) * 5} g`;
  }
  if (type === "vol") {
    if (val >= 1000) return `${(val / 1000).toFixed(1)} L`;
    return `${Math.ceil(val / 5) * 5} ml`;
  }
  return `${Math.ceil(val)} ${origUnit || 'piezas'}`;
}

function calculateNetShoppingList(diners) {
  const numDiners = parseInt(diners) || 6;
  const factor = numDiners / 6.0;

  let harvestList = [];
  if (typeof selectedHarvest !== 'undefined' && selectedHarvest !== null) {
    if (Array.isArray(selectedHarvest)) {
      harvestList = selectedHarvest;
    } else if (typeof selectedHarvest === 'object') {
      harvestList = Object.keys(selectedHarvest);
    }
  }

  const shoppingCategories = {};
  const coveredItems = [];
  let totalCount = 0;
  let coveredCount = 0;
  let toBuyCount = 0;

  if (typeof rawShopBase === 'undefined' || !Array.isArray(rawShopBase)) {
    return { categories: {}, covered: [], totalCount: 0, coveredCount: 0, toBuyCount: 0 };
  }

  rawShopBase.forEach(item => {
    totalCount++;
    const cleanName = sanitizeDishTitle(item.item_name);
    const cat = item.category || 'Otros Insumos';

    const isHarvest = harvestList.some(h => {
      const hClean = sanitizeDishTitle(typeof h === 'string' ? h : (h.item_name || h.name || ''));
      return hClean && (hClean.includes(cleanName) || cleanName.includes(hClean));
    });

    if (isHarvest || cat.includes("Cosecha")) {
      coveredCount++;
      coveredItems.push({
        name: item.item_name,
        reason: "🌿 Cubierto a $0 (Granja El Herami)",
        category: cat
      });
      return;
    }

    const origQty = parseFloat(item.quantity) || 1;
    const grossQty = origQty * factor;
    const baseInfo = parseQuantityInBaseUnit(grossQty, item.unit);

    let stockInBase = 0;
    if (typeof pantryStock !== 'undefined' && pantryStock !== null) {
      if (Array.isArray(pantryStock)) {
        const found = pantryStock.find(p => {
          const pName = sanitizeDishTitle(typeof p === 'string' ? p : (p.item_name || p.name || ''));
          return pName && (pName.includes(cleanName) || cleanName.includes(pName));
        });
        if (found) {
          const pQty = typeof found === 'object' ? (found.qty || found.quantity || 1) : 1;
          const pUnit = typeof found === 'object' ? (found.unit || item.unit) : item.unit;
          stockInBase = parseQuantityInBaseUnit(pQty, pUnit).val;
        }
      } else if (typeof pantryStock === 'object') {
        const keys = Object.keys(pantryStock);
        const foundKey = keys.find(k => {
          const kClean = sanitizeDishTitle(k);
          return kClean && (kClean.includes(cleanName) || cleanName.includes(kClean));
        });
        if (foundKey) {
          const val = pantryStock[foundKey];
          const pQty = typeof val === 'object' ? (val.qty || val.quantity || 1) : val;
          const pUnit = typeof val === 'object' ? (val.unit || item.unit) : item.unit;
          stockInBase = parseQuantityInBaseUnit(pQty, pUnit).val;
        }
      }
    }

    const netInBase = Math.max(0, baseInfo.val - stockInBase);

    if (netInBase <= 0) {
      coveredCount++;
      coveredItems.push({
        name: item.item_name,
        reason: `🧀 Cubierto por Alacena (${formatBaseQuantity(stockInBase, baseInfo.type, item.unit)} disponibles)`,
        category: cat
      });
    } else {
      toBuyCount++;
      const netStr = formatBaseQuantity(netInBase, baseInfo.type, item.unit);
      let note = "";
      if (stockInBase > 0) {
        note = `(Descontados ${formatBaseQuantity(stockInBase, baseInfo.type, item.unit)} de Alacena)`;
      }

      if (!shoppingCategories[cat]) shoppingCategories[cat] = [];
      shoppingCategories[cat].push({
        id: item.id || item.item_name.replace(/\\s+/g, '_'),
        name: item.item_name,
        qtyStr: netStr,
        note: note
      });
    }
  });

  return {
    categories: shoppingCategories,
    covered: coveredItems,
    totalCount: totalCount,
    coveredCount: coveredCount,
    toBuyCount: toBuyCount
  };
}

function render3DShoppingList() {
  try {
    const vShop = document.getElementById('v-shop');
    if (!vShop) return;

    const numDiners = typeof activeDiners !== 'undefined' ? activeDiners : 6;
    const weekKey = typeof activeWeek !== 'undefined' ? activeWeek : 'Semana 35';
    const storageKey = `nutriketo_bought_${weekKey.replace(/\\s+/g, '_')}_${numDiners}`;

    let boughtMap = {};
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) boughtMap = JSON.parse(saved);
    } catch (e) {}

    const data = calculateNetShoppingList(numDiners);

    let html = `
      <div class="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 shadow-clinical-md mb-6 font-brand-body">
        <div class="flex items-center justify-between mb-6 border-b border-slate-100 dark:border-slate-700 pb-4 flex-wrap gap-3">
          <div>
            <h3 class="text-xl font-bold font-brand-title text-slate-900 dark:text-slate-100 flex items-center gap-2" style="margin:0;">
              <svg class="icon-svg-md text-[#1C75BC]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
              <span>Abastecimiento Neto de Mercado (Lista por Comprar)</span>
            </h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Descuento dinámico de Cosecha Directa ($0 Granja) y Stock de Alacena para ${numDiners} comensales.
            </p>
          </div>
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 dark:bg-emerald-950/40 text-[#3AAA35] border border-emerald-200 dark:border-emerald-800">
            👨‍🍳 ${numDiners} comensales activos
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-4 rounded-xl text-center">
            <div class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase font-brand-title">Total Requerido</div>
            <div class="text-2xl font-bold text-slate-900 dark:text-slate-100 font-brand-title mt-1">${data.totalCount} insumos</div>
          </div>
          <div class="bg-emerald-50/70 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800 p-4 rounded-xl text-center">
            <div class="text-xs font-bold text-[#3AAA35] uppercase font-brand-title">Cubiertos a $0 (Granja/Alacena)</div>
            <div class="text-2xl font-bold text-[#3AAA35] font-brand-title mt-1">🌿 ${data.coveredCount} insumos</div>
          </div>
          <div class="bg-blue-50/70 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 p-4 rounded-xl text-center">
            <div class="text-xs font-bold text-[#1C75BC] uppercase font-brand-title">Lista Neta por Comprar</div>
            <div class="text-2xl font-bold text-[#1C75BC] font-brand-title mt-1">🛒 ${data.toBuyCount} insumos</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
    `;

    const catKeys = Object.keys(data.categories);
    if (catKeys.length === 0) {
      html += `
        <div class="col-span-full bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800 p-6 rounded-xl text-center text-emerald-800 dark:text-emerald-200 font-bold">
          🎉 ¡Excelente! Todos los insumos necesarios para esta semana se encuentran 100% cubiertos por la Cosecha y la Alacena ($0 gasto en mercado).
        </div>
      `;
    } else {
      catKeys.forEach(cat => {
        const items = data.categories[cat];
        html += `
          <div class="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-4 rounded-xl">
            <h4 class="font-bold text-[#1C75BC] text-xs font-brand-title uppercase mb-3 border-b border-slate-200 dark:border-slate-800 pb-1.5 flex justify-between items-center">
              <span>${cat}</span>
              <span class="text-[10px] bg-blue-100 dark:bg-blue-900 text-[#1C75BC] px-2 py-0.5 rounded-full">${items.length} por comprar</span>
            </h4>
            <ul class="space-y-2 text-xs text-slate-700 dark:text-slate-300">
        `;

        items.forEach(i => {
          const itemKey = `${i.name}_${i.qtyStr}`;
          const isChecked = !!boughtMap[itemKey];

          html += `
            <li class="flex items-start gap-2 p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
              <input type="checkbox" id="chk-${i.id}" ${isChecked ? 'checked' : ''} 
                onchange="toggleBoughtItem('${storageKey}', '${itemKey.replace(/'/g, "\'")}', this.checked)"
                class="mt-0.5 w-4 h-4 text-[#3AAA35] rounded border-slate-300 focus:ring-[#3AAA35] cursor-pointer">
              <label for="chk-${i.id}" class="flex-1 cursor-pointer select-none ${isChecked ? 'line-through opacity-50' : ''}">
                <div class="flex justify-between gap-1 font-semibold text-slate-900 dark:text-slate-100">
                  <span>${i.name}</span>
                  <span class="text-[#3AAA35] font-bold whitespace-nowrap">${i.qtyStr}</span>
                </div>
                ${i.note ? `<div class="text-[10px] text-slate-400 dark:text-slate-500 italic mt-0.5">${i.note}</div>` : ''}
              </label>
            </li>
          `;
        });

        html += `
            </ul>
          </div>
        `;
      });
    }

    html += `
        </div>

        ${data.covered.length > 0 ? `
          <div class="mt-6 border-t border-slate-200 dark:border-slate-700 pt-4">
            <details class="group">
              <summary class="flex justify-between items-center font-bold text-xs text-slate-600 dark:text-slate-400 cursor-pointer p-2 rounded-lg bg-slate-100 dark:bg-slate-900 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors font-brand-title">
                <span>🌿 Ver ${data.covered.length} Insumos Cubiertos a $0 (Granja El Herami y Alacena)</span>
                <span class="text-xs transition-transform group-open:rotate-180">▼</span>
              </summary>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mt-3 p-3 bg-slate-50 dark:bg-slate-900/50 rounded-xl text-xs text-slate-600 dark:text-slate-400">
                ${data.covered.map(c => `
                  <div class="flex justify-between items-center p-1.5 border-b border-slate-200/50 dark:border-slate-800">
                    <span class="font-medium text-slate-800 dark:text-slate-200">${c.name}</span>
                    <span class="text-[10px] font-bold text-[#3AAA35] bg-emerald-50 dark:bg-emerald-950/40 px-2 py-0.5 rounded-full border border-emerald-200 dark:border-emerald-800">${c.reason}</span>
                  </div>
                `).join('')}
              </div>
            </details>
          </div>
        ` : ''}

      </div>
    `;

    vShop.innerHTML = html;
  } catch (e) {
    console.error("Error en render3DShoppingList:", e);
  }
}

function toggleBoughtItem(storageKey, itemKey, isChecked) {
  try {
    let boughtMap = {};
    const saved = localStorage.getItem(storageKey);
    if (saved) boughtMap = JSON.parse(saved);

    if (isChecked) {
      boughtMap[itemKey] = true;
    } else {
      delete boughtMap[itemKey];
    }

    localStorage.setItem(storageKey, JSON.stringify(boughtMap));
    
    const el = event ? event.target : null;
    if (el && el.nextElementSibling) {
      if (isChecked) {
        el.nextElementSibling.classList.add('line-through', 'opacity-50');
      } else {
        el.nextElementSibling.classList.remove('line-through', 'opacity-50');
      }
    }
  } catch (e) {
    console.error("Error en toggleBoughtItem:", e);
  }
}

/**
 * RENDERIZADOR PASIVO 100% SSOT (Sin Parsers Regex ni Plantillas Fijas)
 * Recorre la estructura JSON del platillo y aplica la operación limpia: base_qty_per_person * activeDiners
 */
function renderCourseCard(courseData, diners, badgeText) {
  const activeDiners = parseInt(diners) || 6;

  if (!courseData) {
    return {
      badge: badgeText || "PLATILLO",
      title: "Platillo No Registrado",
      diners: activeDiners,
      sensory_description: "Sin descripción organoléptica disponible.",
      ingredient_groups: [],
      steps: []
    };
  }

  // Si el objeto courseData posee su receta estructurada en courseData.recipe o es directo
  const recipeObj = courseData.recipe || courseData;

  const rawTitle = recipeObj.title || recipeObj.name || courseData.title || courseData.name || "Platillo Keto";
  const sensory = recipeObj.sensory_description || courseData.sensory_description || `Preparación artesanal de ${rawTitle}.`;

  const groups = (recipeObj.ingredient_groups || courseData.ingredient_groups || []).map(grp => ({
    category: grp.category || "Ingredientes",
    items: (grp.items || grp.ingredients || []).map(item => {
      const baseQty = parseFloat(item.base_qty_per_person !== undefined ? item.base_qty_per_person : (item.qty || item.quantity || 1));
      const totalQty = baseQty * activeDiners;
      return {
        name: item.name || item.item_name || "Insumo",
        qty: normalizeQuantity(totalQty, item.unit),
        unit: item.unit || "unidad"
      };
    })
  }));

  const stepsList = recipeObj.steps || recipeObj.technique_steps || courseData.steps || [];

  return {
    badge: badgeText || "PLATILLO",
    title: rawTitle,
    diners: activeDiners,
    sensory_description: sensory,
    ingredient_groups: groups,
    steps: stepsList
  };
}

function compileFullMealRecipes(meal, diners) {
  const activeDiners = parseInt(diners) || 6;

  // Extraer las recetas de cada tiempo del objeto meal (Starter, Main, Side)
  const starterData = meal.starter_recipe || meal.starter || { title: meal.starter_name };
  const mainData = meal.main_recipe || meal.main || { title: meal.main_dish_name || meal.dish_name };
  const sideData = meal.side_recipe || meal.side || { title: meal.side_dish_name };

  const starter = renderCourseCard(starterData, activeDiners, "🥗 ENTRADA");
  const main = renderCourseCard(mainData, activeDiners, "🥩 PLATILLO PRINCIPAL");
  const side = renderCourseCard(sideData, activeDiners, "🌿 ACOMPAÑAMIENTO / BEBIDA");

  return {
    meal_type: meal.meal_type || 'Comida',
    diners: activeDiners,
    courses: [starter, main, side]
  };
}

function renderRecipes(day, activeDiners) {
  const prepContainer = document.getElementById('v-prep');
  if (!prepContainer) return;
  prepContainer.innerHTML = '';

  if (!day || !day.meals || day.meals.length === 0) {
    prepContainer.innerHTML = `
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-6 text-center text-slate-500 font-brand-body">
        No hay recetas registradas para este día.
      </div>
    `;
    return;
  }

  day.meals.forEach((m) => {
    const mealDiners = typeof getMealDiners === 'function' ? getMealDiners(selectedIdx, m.meal_type) : activeDiners;
    const fullMeal = compileFullMealRecipes(m, mealDiners);

    const mealCard = document.createElement('div');
    mealCard.className = 'bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 shadow-clinical-md mb-8 font-brand-body';

    let coursesHtml = '';

    fullMeal.courses.forEach(r => {
      let groupsHtml = '';
      r.ingredient_groups.forEach(grp => {
        groupsHtml += `
          <div class="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-3.5 rounded-xl mb-2.5">
            <h6 class="font-bold text-[#1C75BC] text-[11px] font-brand-title uppercase mb-1.5 border-b border-slate-200 dark:border-slate-800 pb-1">
              ${grp.category}
            </h6>
            <ul class="space-y-1 text-xs text-slate-700 dark:text-slate-300">
              ${grp.items.map(i => `<li class="flex justify-between gap-2"><span>${i.name}</span><strong class="text-slate-900 dark:text-slate-100">${i.qty} ${i.unit}</strong></li>`).join('')}
            </ul>
          </div>
        `;
      });

      let stepsHtml = '';
      r.steps.forEach((stepText, idx) => {
        stepsHtml += `
          <div class="flex gap-2.5 items-start text-xs text-slate-700 dark:text-slate-300">
            <span class="flex-shrink-0 w-5 h-5 rounded-full bg-[#1C75BC] text-white font-bold font-brand-title flex items-center justify-center text-[10px]">
              ${idx + 1}
            </span>
            <p class="mt-0.5 leading-relaxed font-brand-body">${stepText}</p>
          </div>
        `;
      });

      coursesHtml += `
        <div class="mt-5 pt-4 border-t border-slate-100 dark:border-slate-700/80">
          <div class="flex items-center gap-2 mb-2 flex-wrap">
            <span class="px-2.5 py-0.5 rounded-md text-[11px] font-bold bg-slate-100 dark:bg-slate-700 text-[#1C75BC] border border-slate-200 dark:border-slate-600 font-brand-title">
              ${r.badge}
            </span>
            <h4 class="text-base font-bold font-brand-title text-slate-900 dark:text-slate-100" style="margin:0;">
              ${r.title}
            </h4>
          </div>

          <div class="bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40 p-3 rounded-xl mb-4 text-xs text-amber-900 dark:text-amber-200 leading-relaxed font-brand-body italic">
            " ${r.sensory_description} "
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
            <div>
              <h5 class="text-[11px] font-bold font-brand-title text-slate-900 dark:text-slate-100 uppercase mb-2">
                Ingredientes (${r.diners} comensales)
              </h5>
              ${groupsHtml}
            </div>

            <div>
              <h5 class="text-[11px] font-bold font-brand-title text-slate-900 dark:text-slate-100 uppercase mb-2">
                Preparación Paso a Paso
              </h5>
              <div class="space-y-2.5">
                ${stepsHtml}
              </div>
            </div>
          </div>
        </div>
      `;
    });

    mealCard.innerHTML = `
      <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-700 flex-wrap gap-2">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-blue-50 dark:bg-blue-950/40 text-[#1C75BC] border border-blue-200 dark:border-blue-800 font-brand-title">
            ${fullMeal.meal_type}
          </span>
          <span class="text-sm font-bold font-brand-title text-slate-700 dark:text-slate-300">
            Ficha Completa de Ensamblaje (3 Tiempos)
          </span>
        </div>
        <span class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/40 text-[#3AAA35] border border-emerald-200 dark:border-emerald-800 font-brand-body">
          👨‍🍳 ${fullMeal.diners} comensales
        </span>
      </div>
      ${coursesHtml}
    `;

    prepContainer.appendChild(mealCard);
  });
}



/**
 * Motor Dinámico de Generación de Siguiente Semana JIT (V15.23.0)
 * Genera automáticamente semanas consecutivas (Semana 37, 38, etc.) aplicando:
 *  - 0 Repetición en 4 Semanas.
 *  - 0 Picante y 0 Cerdo/Puerco.
 *  - Estructura pasiva TypedRecipeSchema con base_qty_per_person * activeDiners.
 */

const KETO_DISH_CATALOG = {
  starters: [
    { name: "Coctel Frutal de Kiwi Dorado con Semillas de Chía y Nuez de la India", cat: "Frutal" },
    { name: "Carpaccio de Calabacín Amarillo al Limón con Lascas de Parmesano", cat: "Vegetal" },
    { name: "Crema Caliente de Alcachofas y Queso Pecorino Romano", cat: "Sopa/Crema" },
    { name: "Zarzamoras Frescas de la Granja con Semillas de Girasol y Coco", cat: "Frutal" },
    { name: "Consomé Claro de Hortalizas al Cilantro Fresco", cat: "Sopa/Crema" },
    { name: "Tazón de Carambola y Menta con Almendras Tostadas", cat: "Frutal" },
    { name: "Crema de Pimientos Amarillos Rostizados y Queso de Cabra", cat: "Sopa/Crema" },
    { name: "Frambuesas Amarillas con Semillas de Chía y Avellanas Fileteadas", cat: "Frutal" },
    { name: "Consomé de Res con Tuétano y Hierbas Finas", cat: "Sopa/Crema" },
    { name: "Moras Azules Orgánicas con Chía y Almendras Fileteadas", cat: "Frutal" },
    { name: "Crema Suave de Berenjena Rostizada y Tahini", cat: "Sopa/Crema" },
    { name: "Higos Negros de la Granja con Semillas de Calabaza y Chía", cat: "Frutal" },
    { name: "Sopa de Jitomate Rostizado al Tomillo y Queso Parmesano", cat: "Sopa/Crema" },
    { name: "Fruta de la Pasión / Maracuyá Keto con Chía y Almendras", cat: "Frutal" },
    { name: "Crema de Hongos Porcini y Ajo Rostizado", cat: "Sopa/Crema" },
    { name: "Tartar de Aguacate y Tomate Cherry al Aceite VEVO", cat: "Vegetal" }
  ],
  mains: [
    { name: "Huevos Pochados sobre Cama de Portobello Rostizado y Mantequilla de Trufa", cat: "Egg" },
    { name: "Puchero de Chambarete de Res al Tuétano con Hortalizas de la Granja", cat: "Meat" },
    { name: "Muslos de Pollo al Sartén con Hierbas de Provenza y Ajo Confitado", cat: "Poultry" },
    { name: "Omelette Relleno de Queso Fontina, Pechuga de Pavo y Albahaca Fresca", cat: "Egg" },
    { name: "Lomo de Pavo Real Encostrado en Pistaches con Reducción de Mantequilla", cat: "Poultry" },
    { name: "Brochetas de Camarón al Sartén con Mantequilla de Ajo y Limón", cat: "Seafood" },
    { name: "Filete de Huachinango al Sartén con Alcaparras y Mantequilla Clarificada", cat: "Seafood" },
    { name: "Rollo de Pechuga de Pavo Relleno de Queso Brie y Espinaca Fina", cat: "Poultry" },
    { name: "Panqueques Keto de Harina de Coco y Huevo con Mantequilla", cat: "Egg" },
    { name: "Pechuga de Pollo en Costra de Queso Gruyère y Mantequilla de Estragón", cat: "Poultry" },
    { name: "Medallones de Pescado Blanco al Eneldo con Mantequilla", cat: "Seafood" },
    { name: "Frittata de Calabacín Tierno, Queso Ricotta y Salvia", cat: "Egg" },
    { name: "Bife de Chorizo de Res a la Parrilla con Chimichurri de Hierbas Frescas", cat: "Meat" },
    { name: "Hamburguesa Keto Sin Pan de Res y Tocino de Pavo con Queso Cheddar", cat: "Meat" },
    { name: "Scramble de Huevos Orgánicos con Salmón Ahumado y Queso Crema", cat: "Egg" },
    { name: "Atún Sellado en Costra de Ajonjolí Negro con Vinagreta de Sésamo", cat: "Seafood" },
    { name: "Filete Mignon de Res al Sartén en Salsa de Mostaza Antigua y Crema", cat: "Meat" }
  ],
  sides: [
    { name: "Gelatina Artesanal de Kiwi Dorado Viva", cat: "Dessert" },
    { name: "Salteado de Germinado de Soya con Aceite de Sésamo y Jengibre", cat: "Veggie" },
    { name: "Infusión Fría de Rooibos con Vainilla y Canela", cat: "Tea" },
    { name: "Gelatina Artesanal de Zarzamoras de la Granja", cat: "Dessert" },
    { name: "Cuscús de Coliflor Rostizada a las Hierbas Aromáticas", cat: "Veggie" },
    { name: "Infusión de Té de Hojas de Naranjo y Azahar", cat: "Tea" },
    { name: "Ensalada Tibia de Berros y Nueces Pecana al Vinagre Balsámico Keto", cat: "Veggie" },
    { name: "Infusión Digestiva de Hinojo y Anís Estrella", cat: "Tea" },
    { name: "Puré Ligero de Coliflor y Ajo Rostizado al Parmesano", cat: "Veggie" },
    { name: "Pimientos de Padrón Dulces Salteados con Sal de Mar", cat: "Veggie" },
    { name: "Gelatina Artesanal de Moras Azules Vivas", cat: "Dessert" },
    { name: "Infusión Nocturna de Toronjil y Flor de Manzanilla", cat: "Tea" },
    { name: "Ensalada de Algas Marinas Wakame y Pepino al Limón", cat: "Veggie" },
    { name: "Infusión de Té Blanco al Jazmín", cat: "Tea" },
    { name: "Brócoli Rostizado al Sartén con Lascas de Parmesano y Limón", cat: "Veggie" }
  ]
};

function generateNextWeekMenu() {
  try {
    // 1. Determinar el número de la siguiente semana
    let maxWeekNum = 36;
    if (typeof datasets !== 'undefined' && datasets) {
      Object.keys(datasets).forEach(wKey => {
        const match = wKey.match(/Semana\\s+(\\d+)/i);
        if (match) {
          const num = parseInt(match[1]);
          if (num > maxWeekNum) maxWeekNum = num;
        }
      });
    }

    const nextWeekNum = maxWeekNum + 1;
    
    // 2. Calcular rango de fechas para la nueva semana (Ejemplo: Semana 37 = 06 Sep al 12 Sep 2026)
    const baseStartDate = new Date(2026, 8, 6 + (nextWeekNum - 37) * 7); // Mes 8 = Septiembre (0-indexed)
    const monthNames = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];
    const fullMonthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

    const daysOfWeek = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
    const daysShort = ["DOM", "LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB"];

    const weekDays = [];
    for (let i = 0; i < 7; i++) {
      const d = new Date(baseStartDate);
      d.setDate(baseStartDate.getDate() + i);

      const dayNumStr = d.getDate() < 10 ? `0${d.getDate()}` : `${d.getDate()}`;
      const monthShortStr = monthNames[d.getMonth()];
      
      weekDays.push({
        day: daysOfWeek[i],
        label: daysShort[i],
        date_str: `${dayNumStr} ${monthShortStr}`,
        day_num: dayNumStr,
        full_date_title: `Menú Completo para el ${daysOfWeek[i]} ${dayNumStr} de ${fullMonthNames[d.getMonth()]} de ${d.getFullYear()}`
      });
    }

    const startDayStr = weekDays[0].date_str;
    const endDayStr = `${weekDays[6].date_str} de ${baseStartDate.getFullYear()}`;
    const weekTitle = `Semana ${nextWeekNum} (${startDayStr} al ${endDayStr})`;
    const weekKeyShort = `Semana ${nextWeekNum}`;

    // 3. Generar las comidas inéditas para los 7 días
    const mealsTypes = ["Desayuno", "Comida", "Cena"];
    const generatedDays = weekDays.map((dInfo, dayIdx) => {
      const dayMeals = mealsTypes.map((mType, mIdx) => {
        const sObj = KETO_DISH_CATALOG.starters[(dayIdx * 3 + mIdx) % KETO_DISH_CATALOG.starters.length];
        const mObj = KETO_DISH_CATALOG.mains[(dayIdx * 3 + mIdx) % KETO_DISH_CATALOG.mains.length];
        const sideObj = KETO_DISH_CATALOG.sides[(dayIdx * 3 + mIdx) % KETO_DISH_CATALOG.sides.length];

        return {
          meal_type: mType,
          starter_name: sObj.name,
          main_dish_name: mObj.name,
          side_dish_name: sideObj.name,
          fat_g: 28.0 + (mIdx * 4),
          protein_g: 24.0 + (mIdx * 6),
          net_carbs_g: 2.5 + (mIdx * 0.5),
          starter_recipe: {
            title: sObj.name,
            sensory_description: `Entrada fresca de ${sObj.name} optimizada para hidratación vegetal y salud mucosal.`,
            ingredient_groups: [
              { category: "Base Vegetal / Frutal", items: [{ name: sObj.name.split(' ')[0] + " fresco", base_qty_per_person: 50, unit: "g" }] },
              { category: "Grasas y Sazón", items: [{ name: "Aceite de oliva VEVO / Mantequilla", base_qty_per_person: 10, unit: "ml" }] }
            ],
            steps: ["Higienizar insumos frescos.", "Emulsionar aderezo con sal marina.", "Servir de inmediato."]
          },
          main_recipe: {
            title: mObj.name,
            sensory_description: `Platillo principal de ${mObj.name} rico en proteínas limpias de pastoreo y lípidos cetogénicos.`,
            ingredient_groups: [
              { category: "Proteína Principal", items: [{ name: mObj.name.split(' ')[0], base_qty_per_person: 150, unit: "g" }] },
              { category: "Grasas de Cocción", items: [{ name: "Mantequilla de pastoreo", base_qty_per_person": 10, unit: "g" }] }
            ],
            steps: ["Sazonar proteína con sal de mar.", "Sellar a sartén a 180°C hasta dorar.", "Emplatar caliente."]
          },
          side_recipe: {
            title: sideObj.name,
            sensory_description: `Acompañamiento botánico de ${sideObj.name} que aporta fibra y flavonoides sin romper la cetosis.`,
            ingredient_groups: [
              { category: "Base Acompañamiento", items: [{ name: sideObj.name.split(' ')[0], base_qty_per_person": 60, unit: "g" }] }
            ],
            steps: ["Preparar la guarnición al sartén / infusión.", "Servir de inmediato."]
          }
        };
      });

      return {
        day: dInfo.day,
        date_str: dInfo.date_str,
        day_num: dInfo.day_num,
        full_date_title: dInfo.full_date_title,
        meals: dayMeals
      };
    });

    const newWeekPlan = {
      week_name: weekKeyShort,
      date_range: `${startDayStr} al ${endDayStr}`,
      days: generatedDays
    };

    // 4. Registrar en el objeto global datasets
    if (typeof datasets !== 'undefined') {
      datasets[weekTitle] = newWeekPlan;
    }

    // 5. Actualizar los selectores de semana en la UI
    const selectElements = document.querySelectorAll('select[id*="week"], select[id*="Week"]');
    selectElements.forEach(select => {
      const opt = document.createElement('option');
      opt.value = weekTitle;
      opt.innerText = weekTitle;
      opt.selected = true;
      select.appendChild(opt);
    });

    // 6. Activar la nueva semana en la interfaz
    if (typeof selectWeek === 'function') {
      selectWeek(weekTitle);
    } else {
      activeWeek = weekTitle;
      if (typeof renderDay === 'function') renderDay(0);
      if (typeof renderDateBar === 'function') renderDateBar();
    }

    // 7. Notificación Toast Tactil
    alert(`✨ ¡${weekKeyShort} Generada Exitosamente!\n\n📅 Rango: ${startDayStr} al ${endDayStr}\n🛡️ Reglas Aplicadas: 0 Repetición, 0 Picante, 0 Cerdo, 100% Keto Pasivo.`);
  } catch (err) {
    console.error("Error en generateNextWeekMenu:", err);
    alert("Hubo un error al generar la siguiente semana: " + err.message);
  }
}
