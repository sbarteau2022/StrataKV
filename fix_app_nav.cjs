const fs = require('fs');
let code = fs.readFileSync('src/App.tsx', 'utf-8');

// Add the import
code = code.replace(
  "import { BenchmarkTelemetryBoard } from './components/BenchmarkTelemetryBoard';",
  "import { BenchmarkTelemetryBoard } from './components/BenchmarkTelemetryBoard';\nimport { AgenticRunbook } from './components/AgenticRunbook';"
);

// Update nav buttons
const oldNav = `<button
              onClick={() => setActiveTier('tier1')}
              className={\`nav-pill \${activeTier === 'tier1' ? 'active' : ''}\`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTier('tier2')}
              className={\`nav-pill \${activeTier === 'tier2' ? 'active' : ''}\`}
            >
              Benchmarks
            </button>`;

const newNav = `<button
              onClick={() => setActiveTier('tier1')}
              className={\`nav-pill \${activeTier === 'tier1' ? 'active' : ''}\`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTier('runbook')}
              className={\`nav-pill \${activeTier === 'runbook' ? 'active' : ''}\`}
            >
              Runbook
            </button>
            <button
              onClick={() => setActiveTier('tier2')}
              className={\`nav-pill \${activeTier === 'tier2' ? 'active' : ''}\`}
            >
              Benchmarks
            </button>`;

code = code.replace(oldNav, newNav);

// Add the component section
const oldTier2Section = `{/* ======================================================================= */}
        {/* TIER 2: 14 BENCHMARK DEEP DIVES */}`;

const newRunbookSection = `{/* ======================================================================= */}
        {/* RUNBOOK: AGENTIC LIFECYCLE */}
        {/* ======================================================================= */}
        {activeTier === 'runbook' && (
          <AgenticRunbook />
        )}

        {/* ======================================================================= */}
        {/* TIER 2: 14 BENCHMARK DEEP DIVES */}`;

code = code.replace(oldTier2Section, newRunbookSection);

fs.writeFileSync('src/App.tsx', code);
console.log('App.tsx navigation updated successfully');
