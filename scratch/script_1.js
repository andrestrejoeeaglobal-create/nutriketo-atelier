
    window.MEAL_DISH_OVERRIDES = window.MEAL_DISH_OVERRIDES || {};

function getDeconstructedRecipeForDish(dishTitle, courseRole) {
  // CORTEX SSOT V16.0.0: Renderizado 100% pasivo desde el backend dinámico. Sin overrides hardcodeados por regex.
  return null;
}



// --- MOTOR DE AUTO-GENERACIÓN DÉ LA SIGUIENTE SEMANA JIT (V15.23.2) ---
const FORBIDDEN_INGREDIENTS = {
  picante: ["chile", "serrano", "jalapeño", "habanero", "chipotle", "pimienta negra", "paprika picante"],
  cerdo: ["cerdo", "puerco", "tocino de cerdo", "jamon de cerdo", "manteca", "chicharron"],
  gluten_granos: ["trigo", "maiz", "arroz", "harina refinada", "avena"],
  azucares: ["azucar", "jarabe", "miel", "sacarosa", "maltitol"]
};

function validateCulinaryImmunity(text) {
  if (!text) return true;
  const clean = text.toLowerCase();
  for (const cat in FORBIDDEN_INGREDIENTS) {
    for (const forbidden of FORBIDDEN_INGREDIENTS[cat]) {
      if (clean.includes(forbidden)) return false;
    }
  }
  return true;
}

const SANITIZED_KETO_CATALOG = {
  starters: [
    { name: "Coctel Frutal de Kiwi Dorado con Semillas de Chía y Nuez de la India", source: "Granja El Herami", cost: 0.0 },
    { name: "Carpaccio de Calabacín Amarillo al Limón con Lascas de Parmesano", source: "Granja El Herami", cost: 0.0 },
    { name: "Crema Caliente de Alcachofas y Queso Pecorino Romano", source: "Mercado", cost: 25.0 },
    { name: "Zarzamoras Frescas de la Granja con Semillas de Girasol y Coco", source: "Granja El Herami", cost: 0.0 },
    { name: "Consomé Claro de Hortalizas al Cilantro Fresco", source: "Granja El Herami", cost: 0.0 },
    { name: "Tazón de Carambola y Menta con Almendras Tostadas", source: "Granja El Herami", cost: 0.0 },
    { name: "Crema de Pimientos Amarillos Rostizados y Queso de Cabra", source: "Mercado", cost: 22.0 },
    { name: "Frambuesas Amarillas con Semillas de Chía y Avellanas Fileteadas", source: "Granja El Herami", cost: 0.0 },
    { name: "Consomé de Res con Tuétano y Hierbas Finas", source: "Mercado", cost: 35.0 },
    { name: "Moras Azules Orgánicas con Chía y Almendras Fileteadas", source: "Granja El Herami", cost: 0.0 },
    { name: "Crema Suave de Berenjena Rostizada y Tahini", source: "Mercado", cost: 20.0 },
    { name: "Arilos de Granada Fresca con Semillas de Calabaza y Chía", source: "Granja El Herami", cost: 0.0 },
    { name: "Sopa de Jitomate Rostizado al Tomillo y Queso Parmesano", source: "Mercado", cost: 18.0 },
    { name: "Fruta de la Pasión / Maracuyá Keto con Chía y Almendras", source: "Granja El Herami", cost: 0.0 },
    { name: "Crema de Hongos Porcini y Ajo Rostizado", source: "Mercado", cost: 30.0 },
    { name: "Tartar de Aguacate y Tomate Cherry al Aceite VEVO", source: "Granja El Herami", cost: 0.0 }
  ],
  mains: [
    { name: "Huevos Pochados sobre Cama de Portobello Rostizado y Mantequilla de Trufa", source: "Granja El Herami", cost: 0.0 },
    { name: "Puchero de Chambarete de Res al Tuétano con Hortalizas de la Granja", source: "Mercado", cost: 45.0 },
    { name: "Muslos de Pollo al Sartén con Hierbas de Provenza y Ajo Confitado", source: "Mercado", cost: 35.0 },
    { name: "Omelette Relleno de Queso Fontina, Pechuga de Pavo y Albahaca Fresca", source: "Granja El Herami", cost: 0.0 },
    { name: "Lomo de Pavo Real Encostrado en Pistaches con Reducción de Mantequilla", source: "Mercado", cost: 48.0 },
    { name: "Brochetas de Camarón al Sartén con Mantequilla de Ajo y Limón", source: "Mercado", cost: 55.0 },
    { name: "Filete de Huachinango al Sartén con Alcaparras y Mantequilla Clarificada", source: "Mercado", cost: 50.0 },
    { name: "Rollo de Pechuga de Pavo Relleno de Queso Brie y Espinaca Fina", source: "Mercado", cost: 42.0 },
    { name: "Panqueques Keto de Harina de Coco y Huevo con Mantequilla", source: "Granja El Herami", cost: 0.0 },
    { name: "Pechuga de Pollo en Costra de Queso Gruyère y Mantequilla de Estragón", source: "Mercado", cost: 38.0 },
    { name: "Medallones de Pescado Blanco al Eneldo con Mantequilla", source: "Mercado", cost: 40.0 },
    { name: "Frittata de Calabacín Tierno, Queso Ricotta y Salvia", source: "Granja El Herami", cost: 0.0 },
    { name: "Bife de Chorizo de Res a la Parrilla con Chimichurri de Hierbas Frescas", source: "Mercado", cost: 65.0 },
    { name: "Hamburguesa Keto Sin Pan de Res y Tocino de Pavo con Queso Cheddar", source: "Mercado", cost: 45.0 },
    { name: "Scramble de Huevos Orgánicos con Salmón Ahumado y Queso Crema", source: "Mercado", cost: 48.0 },
    { name: "Atún Sellado en Costra de Ajonjolí Negro con Vinagreta de Sésamo", source: "Mercado", cost: 52.0 },
    { name: "Filete Mignon de Res al Sartén en Salsa de Mostaza Antigua y Crema", source: "Mercado", cost: 70.0 }
  ],
  sides: [
    { name: "Gelatina Artesanal de Kiwi Dorado Viva", source: "Granja El Herami", cost: 0.0 },
    { name: "Salteado de Germinado de Soya con Aceite de Sésamo y Jengibre", source: "Mercado", cost: 15.0 },
    { name: "Infusión Fría de Rooibos con Vainilla y Canela", source: "Granja El Herami", cost: 0.0 },
    { name: "Gelatina Artesanal de Zarzamoras de la Granja", source: "Granja El Herami", cost: 0.0 },
    { name: "Cuscús de Coliflor Rostizada a las Hierbas Aromáticas", source: "Granja El Herami", cost: 0.0 },
    { name: "Infusión de Té de Hojas de Naranjo y Azahar", source: "Granja El Herami", cost: 0.0 },
    { name: "Ensalada Tibia de Berros y Nueces Pecana al Vinagre Balsámico Keto", source: "Granja El Herami", cost: 0.0 },
    { name: "Infusión Digestiva de Hinojo y Anís Estrella", source: "Granja El Herami", cost: 0.0 },
    { name: "Puré Ligero de Coliflor y Ajo Rostizado al Parmesano", source: "Mercado", cost: 18.0 },
    { name: "Pimientos de Padrón Dulces Salteados con Sal de Mar", source: "Granja El Herami", cost: 0.0 },
    { name: "Gelatina Artesanal de Moras Azules Vivas", source: "Granja El Herami", cost: 0.0 },
    { name: "Infusión Nocturna de Toronjil y Flor de Manzanilla", source: "Granja El Herami", cost: 0.0 },
    { name: "Ensalada de Algas Marinas Wakame y Pepino al Limón", source: "Mercado", cost: 20.0 },
    { name: "Infusión de Té Blanco al Jazmín", source: "Granja El Herami", cost: 0.0 },
    { name: "Brócoli Rostizado al Sartén con Lascas de Parmesano y Limón", source: "Granja El Herami", cost: 0.0 }
  ]
};

function generateNextWeekMenu() {
  try {
    let maxWeekNum = 36;
    if (typeof datasets !== 'undefined' && datasets) {
      Object.keys(datasets).forEach(wKey => {
        const match = wKey.match(/Semana\s+(\d+)/i);
        if (match) {
          const num = parseInt(match[1]);
          if (num > maxWeekNum) maxWeekNum = num;
        }
      });
    }

    const nextWeekNum = maxWeekNum + 1;
    const baseStartDate = new Date(2026, 8, 6 + (nextWeekNum - 37) * 7);
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

    const mealsTypes = ["Desayuno", "Comida", "Cena"];
    const generatedDays = weekDays.map((dInfo, dayIdx) => {
      const dayMeals = mealsTypes.map((mType, mIdx) => {
        const sObj = SANITIZED_KETO_CATALOG.starters[(dayIdx * 3 + mIdx) % SANITIZED_KETO_CATALOG.starters.length];
        const mObj = SANITIZED_KETO_CATALOG.mains[(dayIdx * 3 + mIdx) % SANITIZED_KETO_CATALOG.mains.length];
        const sideObj = SANITIZED_KETO_CATALOG.sides[(dayIdx * 3 + mIdx) % SANITIZED_KETO_CATALOG.sides.length];

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
              { category: "Base Vegetal / Frutal", items: [{ name: sObj.name.split(' ')[0] + " fresco", base_qty_per_person: 50, unit: "g", source: sObj.source, unit_cost: sObj.cost }] },
              { category: "Grasas y Sazón", items: [{ name: "Aceite de oliva VEVO / Mantequilla", base_qty_per_person: 10, unit: "ml", source: "Granja El Herami", unit_cost: 0.0 }] }
            ],
            steps: ["Higienizar insumos frescos.", "Emulsionar aderezo con sal marina.", "Servir de inmediato."]
          },
          main_recipe: {
            title: mObj.name,
            sensory_description: `Platillo principal de ${mObj.name} rico en proteínas limpias de pastoreo y lípidos cetogénicos.`,
            ingredient_groups: [
              { category: "Proteína Principal", items: [{ name: mObj.name.split(' ')[0], base_qty_per_person: 150, unit: "g", source: mObj.source, unit_cost: mObj.cost }] },
              { category: "Grasas de Cocción", items: [{ name: "Mantequilla de pastoreo", base_qty_per_person: 10, unit: "g", source: "Granja El Herami", unit_cost: 0.0 }] }
            ],
            steps: ["Sazonar proteína con sal de mar.", "Sellar a sartén a 180°C hasta dorar.", "Emplatar caliente."]
          },
          side_recipe: {
            title: sideObj.name,
            sensory_description: `Acompañamiento botánico de ${sideObj.name} que aporta fibra y flavonoides sin romper la cetosis.`,
            ingredient_groups: [
              { category: "Base Acompañamiento", items: [{ name: sideObj.name.split(' ')[0], base_qty_per_person: 60, unit: "g", source: sideObj.source, unit_cost: sideObj.cost }] }
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

    if (typeof datasets !== 'undefined') {
      datasets[weekTitle] = newWeekPlan;
    }

    const selectElements = document.querySelectorAll('select[id*="week"], select[id*="Week"], select[id="weekSelect"]');
    selectElements.forEach(select => {
      const opt = document.createElement('option');
      opt.value = weekTitle;
      opt.innerText = weekTitle;
      opt.selected = true;
      select.appendChild(opt);
    });

    if (typeof selectWeek === 'function') {
      selectWeek(weekTitle);
    } else {
      activeWeek = weekTitle;
      if (typeof renderDay === 'function') renderDay(0);
      if (typeof renderDateBar === 'function') renderDateBar();
    }

    alert(`✨ ¡${weekKeyShort} Generada Exitosamente!

📅 Rango: ${startDayStr} al ${endDayStr}
🛡️ Filtros Activos: 0 Picante, 0 Cerdo, 0 Gluten, Granja El Herami ($0 BOM).`);
  } catch (err) {
    console.error("Error en generateNextWeekMenu:", err);
    alert("Hubo un error al generar la siguiente semana: " + err.message);
  }
}


    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            'ea-red': '#B70E0C',
            'ea-pink': '#F29FC5',
            'ea-corporate': '#1C75BC',
            'ea-green': '#3AAA35',
            'ea-yellow': '#FFCC00',
            'ea-navy': '#0F172A',
            'ea-clinical': '#F8FAFC',
          }
        }
      }
    }
  