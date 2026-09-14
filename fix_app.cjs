const fs = require('fs');
let code = fs.readFileSync('src/App.tsx', 'utf-8');
const lines = code.split('\n');

const tier2Index = lines.findIndex(l => l.includes('TIER 2: 14 BENCHMARK DEEP DIVES'));
const tier1StartIndex = lines.findIndex(l => l.includes('TIER 1: MARKETING HOME PAGE / DECK')) - 1;

if (tier2Index !== -1 && tier1StartIndex !== -1) {
  const newLines = lines.slice(0, tier1StartIndex);
  newLines.push('        {/* ======================================================================= */}');
  newLines.push('        {/* TIER 1: MARKETING HOME PAGE / DECK */}');
  newLines.push('        {/* ======================================================================= */}');
  newLines.push('        {activeTier === "tier1" && (');
  newLines.push('          <MarketingDeck />');
  newLines.push('        )}');
  newLines.push('');
  
  // Add from TIER 2 onwards
  const remainder = lines.slice(tier2Index - 1);
  const result = newLines.concat(remainder).join('\n');
  fs.writeFileSync('src/App.tsx', result);
  console.log('Fixed App.tsx successfully');
} else {
  console.log('Could not find indices', tier1StartIndex, tier2Index);
}
