const fs = require('fs');

let content = fs.readFileSync('src/components/MarketingDeck.tsx', 'utf-8');

// Add import
content = content.replace(
  "import { Brain, Cpu, Layers, Activity, FileText, Download } from 'lucide-react';",
  "import { Brain, Cpu, Layers, Activity, FileText, Download } from 'lucide-react';\nimport { AgenticRunbook } from './AgenticRunbook';"
);

// Add the slide
const newSlide = `
      {/* SLIDE 3.5: THE AGENTIC RUNBOOK (TERMINAL UI) */}
      <section className="border-t border-[rgba(255,255,255,0.05)] pt-12 mt-12 bg-[rgba(16,18,15,0.3)]">
        <AgenticRunbook />
      </section>
`;

content = content.replace('{/* SLIDE 4: THE PAPER */}', newSlide + '\n      {/* SLIDE 4: THE PAPER */}');

fs.writeFileSync('src/components/MarketingDeck.tsx', content);
console.log('Injected AgenticRunbook into MarketingDeck successfully');
