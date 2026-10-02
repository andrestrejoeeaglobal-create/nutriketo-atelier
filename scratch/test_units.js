function parseQuantityInBaseUnit(qty, unitRaw) {
  const num = parseFloat(qty) || 0;
  const unitStr = (unitRaw || "").toLowerCase().trim();

  // 1. Empaques compuestos con especificación de peso/volumen (ej. "paquete (3.2 kg)", "frasco (1 kg)", "frasco (500 g)")
  const pkgMatch = unitStr.match(/(\d+(?:\.\d+)?)\s*(kg|kilo|kilos|g|gramos?|l|lt|litros?|ml)/i);
  if (pkgMatch && (unitStr.includes("paquete") || unitStr.includes("empaque") || unitStr.includes("frasco") || unitStr.includes("lata") || unitStr.includes("botella"))) {
    const pkgSize = parseFloat(pkgMatch[1]);
    const pkgUnit = pkgMatch[2].toLowerCase();
    let baseMultiplier = pkgSize;
    if (pkgUnit.includes("kg") || pkgUnit.includes("kilo") || pkgUnit.includes("l") || pkgUnit.includes("lt")) {
      baseMultiplier = pkgSize * 1000;
    }
    const isVol = pkgUnit.includes("l") || pkgUnit.includes("ml");
    return { val: num * baseMultiplier, type: isVol ? "vol" : "mass", baseUnit: isVol ? "ml" : "g" };
  }

  // 2. Casilleros y docenas de huevos
  if (unitStr.includes("casillero")) {
    return { val: num * 30, type: "count", baseUnit: "piezas" };
  }
  if (unitStr.includes("docena")) {
    return { val: num * 12, type: "count", baseUnit: "piezas" };
  }

  // 3. Masa en Kilogramos
  if (unitStr.includes("kg") || unitStr.includes("kilo")) {
    const val = num < 50 ? num * 1000 : num;
    return { val: val, type: "mass", baseUnit: "g" };
  }

  // 4. Volumen en Mililitros
  if (unitStr.includes("ml") || unitStr.includes("mililitro")) {
    return { val: num, type: "vol", baseUnit: "ml" };
  }

  // 5. Masa en Gramos
  if (unitStr.includes("g") || unitStr.includes("gramo")) {
    return { val: num, type: "mass", baseUnit: "g" };
  }

  // 6. Volumen en Litros
  if (unitStr === "l" || unitStr === "lt" || unitStr === "lts" || unitStr.includes("litro") || /\bl\b|\blt\b|\blts\b/i.test(unitStr)) {
    const val = num < 50 ? num * 1000 : num;
    return { val: val, type: "vol", baseUnit: "ml" };
  }

  return { val: num, type: "count", baseUnit: unitStr || "piezas" };
}

console.log("Test 1 (1 paquete 3.2 kg):", parseQuantityInBaseUnit(1, "paquete (3.2 kg)"));
console.log("Test 2 (3.2 kg):", parseQuantityInBaseUnit(3.2, "kg"));
console.log("Test 3 (3200 g):", parseQuantityInBaseUnit(3200, "g"));
console.log("Test 4 (2 casilleros):", parseQuantityInBaseUnit(2, "casilleros"));
console.log("Test 5 (60 piezas):", parseQuantityInBaseUnit(60, "piezas"));
console.log("Test 6 (1 frasco 500 g):", parseQuantityInBaseUnit(1, "frasco (500 g)"));
console.log("Test 7 (1 L):", parseQuantityInBaseUnit(1, "litros"));
console.log("Test 8 (750 ml):", parseQuantityInBaseUnit(750, "ml"));
