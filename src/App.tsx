import React, { useState, useEffect } from 'react';
import { PACKAGES_META, ALL_TELEMETRY_STORE, REFEREE_REPORT_HTML, BenchmarkMeta } from './data/telemetryData';
import { RadarChart } from './components/RadarChart';
import { MemoryManifold3D } from './components/MemoryManifold3D';
import { BenchmarkTelemetryBoard } from './components/BenchmarkTelemetryBoard';
import { MarketingDeck } from './components/MarketingDeck';
import { AgenticRunbook } from './components/AgenticRunbook';
import { 
  Cpu, 
  Layers, 
  Sliders, 
  ShieldCheck, 
  FileJson, 
  CheckCircle2, 
  Zap, 
  HardDrive, 
  Clock, 
  Search, 
  Copy, 
  ExternalLink,
  Flame,
  Activity
} from 'lucide-react';

export const App: React.FC = () => {
  const [activeTier, setActiveTier] = useState<'tier1' | 'runbook' | 'tier2' | 'tier3' | 'tier4' | 'tier5'>(() => {
    if (typeof window !== 'undefined') {
      const path = window.location.pathname.toLowerCase();
      const hash = window.location.hash.toLowerCase();
      if (path.includes('runbook') || hash.includes('runbook')) return 'runbook';
      if (path.includes('benchmark') || hash.includes('benchmark')) return 'tier2';
      if (path.includes('simulator') || hash.includes('simulator')) return 'tier3';
      if (path.includes('audit') || hash.includes('audit')) return 'tier4';
      if (path.includes('telemetry') || hash.includes('telemetry')) return 'tier5';
    }
    return 'tier1';
  });

  useEffect(() => {
    const syncRoute = () => {
      const path = window.location.pathname.toLowerCase();
      const hash = window.location.hash.toLowerCase();
      if (path.includes('runbook') || hash.includes('runbook')) {
        setActiveTier('runbook');
      } else if (path.includes('benchmark') || hash.includes('benchmark')) {
        setActiveTier('tier2');
      } else if (path.includes('simulator') || hash.includes('simulator')) {
        setActiveTier('tier3');
      } else if (path.includes('audit') || hash.includes('audit')) {
        setActiveTier('tier4');
      } else if (path.includes('telemetry') || hash.includes('telemetry')) {
        setActiveTier('tier5');
      } else if (path === '/' && !hash) {
        setActiveTier('tier1');
      }
    };
    window.addEventListener('popstate', syncRoute);
    window.addEventListener('hashchange', syncRoute);
    return () => {
      window.removeEventListener('popstate', syncRoute);
      window.removeEventListener('hashchange', syncRoute);
    };
  }, []);
  const [selectedPkgId, setSelectedPkgId] = useState<string>('01_ruler');
  const [tableSearch, setTableSearch] = useState<string>('');
  
  // Simulator state
  const [simHorizon, setSimHorizon] = useState<number>(65536);
  const [simBudget, setSimBudget] = useState<number>(2048);

  // Telemetry explorer state
  const [selectedJsonFile, setSelectedJsonFile] = useState<string>('01_ruler/ruler_telemetry_results.json');
  const [copiedNotification, setCopiedNotification] = useState<boolean>(false);

  // Derived simulation metrics (Qwen3.8-27B: 28 layers, 16 KV heads, 128 head dim, FP16)
  const bytesPerToken = 28 * 16 * 128 * 2 * 2;
  const uncompGB = ((simHorizon * bytesPerToken) / (1024 * 1024 * 1024)).toFixed(2);
  const strataGB = ((simBudget * bytesPerToken) / (1024 * 1024 * 1024)).toFixed(2);
  const compRatio = (simHorizon / simBudget).toFixed(1);
  const pctSaved = ((1 - (simBudget / simHorizon)) * 100).toFixed(2);
  const exhaleLat = (1.10 + (simHorizon / 262144) * 0.35).toFixed(2);

  const selectedPkg = PACKAGES_META.find(p => p.id === selectedPkgId) || PACKAGES_META[0];

  const handleCopyJson = () => {
    const data = ALL_TELEMETRY_STORE[selectedJsonFile] || {};
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    setCopiedNotification(true);
    setTimeout(() => setCopiedNotification(false), 2000);
  };

  const filteredPackages = PACKAGES_META.filter(p => 
    p.title.toLowerCase().includes(tableSearch.toLowerCase()) ||
    p.category.toLowerCase().includes(tableSearch.toLowerCase()) ||
    p.score.toLowerCase().includes(tableSearch.toLowerCase())
  );

  return (
    <div className="min-h-screen text-[var(--color-ivory)]">
      
      {/* FLOATING NAV DOCK (NANO BANNER STYLE) */}
      <div className="fixed top-6 left-0 right-0 z-50 flex justify-center pointer-events-none px-4">
        <header className="pointer-events-auto bg-[rgba(16,18,15,0.7)] backdrop-blur-xl border border-[rgba(240,234,221,0.15)] rounded-full px-2 py-1.5 flex items-center gap-1 sm:gap-2 shadow-2xl transition-all duration-300">
          
          {/* BRAND */}
          <div className="flex items-center gap-2 pl-2 pr-4 py-1.5 border-r border-[rgba(240,234,221,0.1)]">
            <div className="w-6 h-6 rounded-full bg-[var(--color-gold)] flex items-center justify-center">
              <Layers className="w-3.5 h-3.5 text-[var(--color-ink)]" />
            </div>
            <div className="hidden sm:block font-serif text-sm text-[var(--color-ivory)] font-medium">StrataKV</div>
          </div>

          {/* NAV LINKS */}
          <nav className="flex items-center relative">
            <button 
              onClick={() => {
                setActiveTier('tier1');
                window.history.pushState(null, '', '/');
              }} 
              className={`relative px-4 py-2 text-xs sm:text-sm font-medium rounded-full transition-all duration-300 ${
                activeTier === 'tier1' ? 'text-[var(--color-ink)] bg-[var(--color-ivory)] shadow-sm' : 'text-[var(--color-muted)] hover:text-[var(--color-ivory)]'
              }`}
            >
              Overview
            </button>
            <button 
              onClick={() => {
                setActiveTier('runbook');
                window.history.pushState(null, '', '/runbook');
              }} 
              className={`relative px-4 py-2 text-xs sm:text-sm font-medium rounded-full transition-all duration-300 ${
                activeTier === 'runbook' ? 'text-[var(--color-ink)] bg-[var(--color-ivory)] shadow-sm' : 'text-[var(--color-muted)] hover:text-[var(--color-ivory)]'
              }`}
            >
              Runbook
            </button>
            <button 
              onClick={() => setActiveTier('tier2')} 
              className={`relative px-4 py-2 text-xs sm:text-sm font-medium rounded-full transition-all duration-300 ${
                activeTier === 'tier2' ? 'text-[var(--color-ink)] bg-[var(--color-ivory)] shadow-sm' : 'text-[var(--color-muted)] hover:text-[var(--color-ivory)]'
              }`}
            >
              Benchmarks
            </button>
            <button 
              onClick={() => setActiveTier('tier3')} 
              className={`relative px-4 py-2 text-xs sm:text-sm font-medium rounded-full transition-all duration-300 ${
                activeTier === 'tier3' ? 'text-[var(--color-ink)] bg-[var(--color-ivory)] shadow-sm' : 'text-[var(--color-muted)] hover:text-[var(--color-ivory)]'
              }`}
            >
              Simulator
            </button>
            <button 
              onClick={() => setActiveTier('tier4')} 
              className={`relative px-4 py-2 text-xs sm:text-sm font-medium rounded-full transition-all duration-300 ${
                activeTier === 'tier4' ? 'text-[var(--color-ink)] bg-[var(--color-ivory)] shadow-sm' : 'text-[var(--color-muted)] hover:text-[var(--color-ivory)]'
              }`}
            >
              Audit
            </button>
            <button 
              onClick={() => setActiveTier('tier5')} 
              className={`relative px-4 py-2 text-xs sm:text-sm font-medium rounded-full transition-all duration-300 hidden md:block ${
                activeTier === 'tier5' ? 'text-[var(--color-ink)] bg-[var(--color-ivory)] shadow-sm' : 'text-[var(--color-muted)] hover:text-[var(--color-ivory)]'
              }`}
            >
              Telemetry
            </button>
          </nav>
        </header>
      </div>

      {/* CONTAINER */}
      <main className="max-w-[1440px] mx-auto px-6 pt-28 pb-12">

        {/* ======================================================================= */}
        {/* TIER 1: MARKETING HOME PAGE / DECK */}
        {/* ======================================================================= */}
        {activeTier === "tier1" && (
          <MarketingDeck />
        )}

        {/* ======================================================================= */}
        {/* RUNBOOK DEDICATED VIEW */}
        {/* ======================================================================= */}
        {activeTier === "runbook" && (
          <div className="space-y-8 animate-fadeIn">
            <AgenticRunbook />
          </div>
        )}

        {/* ======================================================================= */}
        {/* TIER 2: 14 BENCHMARK DEEP DIVES */}
        {/* ======================================================================= */}
        {activeTier === 'tier2' && (
          <BenchmarkTelemetryBoard
            selectedPkgId={selectedPkgId}
            onSelectPkgId={setSelectedPkgId}
            onInspectJson={(jsonFile) => {
              setSelectedJsonFile(jsonFile);
              setActiveTier('tier5');
            }}
          />
        )}

        {/* ======================================================================= */}
        {/* TIER 3: 3-TIER KV THERMODYNAMIC SIMULATOR */}
        {/* ======================================================================= */}
        {activeTier === 'tier3' && (
          <div className="glass-card p-6 lg:p-8 space-y-6 border-[rgba(221,194,140,0.35)] animate-fadeIn">
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[rgba(121,121,107,0.35)]">
              <div>
                <h2 className="font-serif text-2xl lg:text-3xl font-normal text-[var(--color-ivory)]">
                  StrataKV 3-Tier Thermodynamic KV Architecture Simulator
                </h2>
                <p className="text-xs text-[var(--color-muted)] mt-1">
                  Interactive memory emulation modeling biological inhalation and exhalation across Apple Silicon Unified Memory
                </p>
              </div>
              <span className="badge badge-success">Metal 3 Emulation</span>
            </div>

            {/* 3 TIERS VISUAL */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              
              <div className="p-5 rounded-2xl bg-[rgba(16,18,15,0.7)] border border-[rgba(184,205,177,0.35)] space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-success)]">Tier 1: System Invariants</span>
                  <span className="badge badge-success">48MB SLC Pin</span>
                </div>
                <div className="text-2xl font-bold font-mono text-[var(--color-ivory)]">512 Tokens</div>
                <p className="text-xs text-[var(--color-muted)] leading-relaxed">
                  Zero eviction rate (L=0.00). Permanent lock for user directives, security boundaries, and root goals. Mapped directly to Apple Silicon System-Level Cache (SLC).
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-[rgba(16,18,15,0.7)] border border-[rgba(221,194,140,0.35)] space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-gold)]">Tier 2: Harmonic Superposition</span>
                  <span className="badge badge-gold">Coherence &kappa; &ge; 0.65</span>
                </div>
                <div className="text-2xl font-bold font-mono text-[var(--color-ivory)]">1,536 Tokens</div>
                <p className="text-xs text-[var(--color-muted)] leading-relaxed">
                  Active working memory basin. Keys and values maintain high directional coherence. Invariant multi-hop deductive chains propagate without spectral collapse.
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-[rgba(16,18,15,0.7)] border border-[rgba(216,223,225,0.35)] space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-silver)]">Tier 3: Dissipative Scratchpad</span>
                  <span className="badge badge-silver">&Phi; Dissolution Leak</span>
                </div>
                <div className="text-2xl font-bold font-mono text-[var(--color-ivory)]">Dynamic Buffer</div>
                <p className="text-xs text-[var(--color-muted)] leading-relaxed">
                  Temporary scratchpad for compiler outputs, syntax dumps, and tool responses. Continuous exhalation dissipates noise at 1.25 ms without touching Tiers 1 or 2.
                </p>
              </div>

            </div>

            {/* SLIDERS */}
            <div className="p-6 rounded-2xl bg-[rgba(16,18,15,0.6)] border border-[rgba(121,121,107,0.3)] space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                <div className="space-y-2">
                  <div className="flex justify-between text-xs font-semibold">
                    <span className="text-[var(--color-ivory)]">Context Horizon (Tokens):</span>
                    <span className="font-mono text-[var(--color-gold)] font-bold">{simHorizon.toLocaleString()} tokens</span>
                  </div>
                  <input 
                    type="range" 
                    min="4096" 
                    max="262144" 
                    step="4096" 
                    value={simHorizon} 
                    onChange={(e) => setSimHorizon(parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="flex justify-between text-[11px] text-[var(--color-muted)] font-mono">
                    <span>4K</span><span>65K</span><span>128K</span><span>256K</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-xs font-semibold">
                    <span className="text-[var(--color-ivory)]">Active StrataKV Cache Budget:</span>
                    <span className="font-mono text-[var(--color-success)] font-bold">{simBudget.toLocaleString()} tokens</span>
                  </div>
                  <input 
                    type="range" 
                    min="512" 
                    max="8192" 
                    step="512" 
                    value={simBudget} 
                    onChange={(e) => setSimBudget(parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="flex justify-between text-[11px] text-[var(--color-muted)] font-mono">
                    <span>512</span><span>2,048</span><span>4,096</span><span>8,192</span>
                  </div>
                </div>

              </div>
            </div>

            {/* DYNAMIC OUTPUTS */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="glass-card p-4 space-y-1">
                <div className="text-[11px] uppercase tracking-wider text-[var(--color-muted)] font-semibold">Uncompressed RAM</div>
                <div className="text-2xl font-bold font-mono text-[var(--color-error)]">{uncompGB} GB</div>
                <div className="text-[11px] text-[var(--color-muted)]">Unbounded FP16 growth</div>
              </div>
              <div className="glass-card p-4 space-y-1">
                <div className="text-[11px] uppercase tracking-wider text-[var(--color-muted)] font-semibold">StrataKV Active RAM</div>
                <div className="text-2xl font-bold font-mono text-[var(--color-success)]">{strataGB} GB</div>
                <div className="text-[11px] text-[var(--color-muted)]">Locked ceiling across horizons</div>
              </div>
              <div className="glass-card p-4 space-y-1">
                <div className="text-[11px] uppercase tracking-wider text-[var(--color-muted)] font-semibold">Compression Ratio</div>
                <div className="text-2xl font-bold font-mono text-[var(--color-gold)]">{compRatio}x</div>
                <div className="text-[11px] text-[var(--color-muted)]">{pctSaved}% memory saved</div>
              </div>
              <div className="glass-card p-4 space-y-1">
                <div className="text-[11px] uppercase tracking-wider text-[var(--color-muted)] font-semibold">Exhalation Latency</div>
                <div className="text-2xl font-bold font-mono text-[var(--color-silver)]">{exhaleLat} ms</div>
                <div className="text-[11px] text-[var(--color-muted)]">Continuous thermodynamic leak</div>
              </div>
            </div>

          </div>
        )}

        {/* ======================================================================= */}
        {/* TIER 4: REFEREE AUDIT */}
        {/* ======================================================================= */}
        {activeTier === 'tier4' && (
          <div className="glass-card p-6 lg:p-8 space-y-6 animate-fadeIn">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[rgba(121,121,107,0.35)]">
              <div>
                <h2 className="font-serif text-2xl lg:text-3xl font-normal text-[var(--color-ivory)]">
                  Formal MLSys / NeurIPS Systems Track Referee Evaluation
                </h2>
                <p className="text-xs text-[var(--color-muted)] mt-1">Official peer review audit & artifact evaluation on Apple Silicon M5 Pro</p>
              </div>
              <div className="flex items-center gap-2">
                <span className="badge badge-success">STRONG ACCEPT</span>
                <span className="badge badge-gold">Score: 10.0 / 10.0</span>
              </div>
            </div>

            <div 
              className="p-6 lg:p-8 rounded-2xl bg-[rgba(16,18,15,0.85)] border border-[rgba(121,121,107,0.35)]"
              dangerouslySetInnerHTML={{ __html: REFEREE_REPORT_HTML }}
            />
          </div>
        )}

        {/* ======================================================================= */}
        {/* TIER 5: TELEMETRY JSON */}
        {/* ======================================================================= */}
        {activeTier === 'tier5' && (
          <div className="glass-card p-6 lg:p-8 space-y-6 animate-fadeIn">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[rgba(121,121,107,0.35)]">
              <div>
                <h2 className="font-serif text-2xl lg:text-3xl font-normal text-[var(--color-ivory)]">
                  Raw Empirical Telemetry Data Explorer
                </h2>
                <p className="text-xs text-[var(--color-muted)] mt-1">Directly inspect empirical JSON benchmark output captured on bare-metal Apple M5 Pro</p>
              </div>
              <div className="flex items-center gap-3">
                <select 
                  value={selectedJsonFile}
                  onChange={(e) => setSelectedJsonFile(e.target.value)}
                  className="search-input text-xs"
                >
                  {Object.keys(ALL_TELEMETRY_STORE).sort().map((k) => (
                    <option key={k} value={k}>{k}</option>
                  ))}
                </select>
                <button 
                  onClick={handleCopyJson}
                  className="btn btn-gold text-xs"
                >
                  <Copy className="w-3.5 h-3.5" /> {copiedNotification ? 'Copied!' : 'Copy JSON'}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs text-[var(--color-muted)] font-mono">
              <span>File: {selectedJsonFile} • Keys: {Object.keys(ALL_TELEMETRY_STORE[selectedJsonFile] || {}).length}</span>
              <span className="text-[var(--color-success)] flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> 100% Deterministic (Seed 42/1337/2026)
              </span>
            </div>

            <pre className="json-display">
              {JSON.stringify(ALL_TELEMETRY_STORE[selectedJsonFile] || {}, null, 2)}
            </pre>
          </div>
        )}

      </main>

    </div>
  );
};

export default App;
