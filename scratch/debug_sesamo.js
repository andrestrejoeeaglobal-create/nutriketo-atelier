const a = 'aceite de ajonjoli tostado';
const b = 'semillas de sesamo (ajonjoli)';

const itemKeywords = [
  { stem: 'oliva', aliases: ['aceite de oliva', 'vevo', 'aceite de oliva extra virgen', 'aceite de oliva virgen extra', 'aceite de oliva extra virgen (vevo)'], exclude: ['aceituna', 'aceitunas'] },
  { stem: 'aceite-ajonjoli', aliases: ['aceite de ajonjoli', 'aceite de sesamo', 'aceite de ajonjoli tostado'], exclude: ['semilla', 'semillas', 'grano'] },
  { stem: 'semillas-sesamo', aliases: ['semillas de sesamo', 'semillas de ajonjoli', 'ajonjoli en grano', 'semilla de ajonjoli', 'semillas de sesamo (ajonjoli)'], exclude: ['aceite'] }
];

for (const entry of itemKeywords) {
  const aEx = entry.exclude && entry.exclude.some(ex => a.includes(ex));
  const bEx = entry.exclude && entry.exclude.some(ex => b.includes(ex));
  if (aEx || bEx) {
    console.log(entry.stem, 'skipped due to exclude:', { aEx, bEx });
    continue;
  }
  const aMatch = entry.aliases.some(alias => a.includes(alias));
  const bMatch = entry.aliases.some(alias => b.includes(alias));
  console.log(entry.stem, { aMatch, bMatch });
}
