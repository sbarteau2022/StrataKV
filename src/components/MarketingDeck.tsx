import React from 'react';
import { ArrowRight, Download, Brain, Activity, Cpu, Layers } from 'lucide-react';
import { MemoryManifold3D } from './MemoryManifold3D';

export const MarketingDeck: React.FC = () => {
  return (
    <div className="w-full text-[var(--color-ivory)] space-y-24 pb-24">
      
      {/* SLIDE 1: HERO */}
      <section className="min-h-[85vh] flex flex-col justify-center relative pt-24">
        <div className="absolute inset-0 z-0 opacity-40 pointer-events-none">
          {/* We can reuse the 3D manifold in the background of the hero */}
          <div className="h-full w-full mask-image-fade">
             <MemoryManifold3D />
          </div>
        </div>
        
        <div className="relative z-10 max-w-5xl mx-auto px-6 text-center space-y-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-gold)] bg-[rgba(221,194,140,0.1)] text-[var(--color-gold)] text-xs font-mono tracking-widest uppercase mb-4">
            <Activity className="w-3.5 h-3.5" /> Breakthrough in Sovereign AI
          </div>
          <h1 className="font-serif text-5xl md:text-7xl lg:text-8xl leading-tight tracking-tight text-[var(--color-ivory)]">
            StrataKV <br/>
            <span className="text-[var(--color-gold)] text-4xl md:text-6xl lg:text-7xl block mt-2">The Autonomous Superposition Engine</span>
          </h1>
          <p className="text-lg md:text-xl text-[var(--color-muted)] max-w-2xl mx-auto leading-relaxed">
            Coherent Memory Geometry, Thermodynamic Exhalation, and Dynamic Kernel Orchestration for Resident Multi-Agent Tool Swarms.
          </p>
          <div className="pt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <button className="px-8 py-3.5 bg-[var(--color-ivory)] text-[var(--color-ink)] font-semibold rounded-full hover:bg-white transition-colors flex items-center gap-2">
              Explore the Engineering <ArrowRight className="w-4 h-4" />
            </button>
            <button className="px-8 py-3.5 bg-[rgba(37,39,32,0.6)] border border-[rgba(121,121,107,0.4)] text-[var(--color-ivory)] font-semibold rounded-full hover:bg-[rgba(37,39,32,0.9)] transition-colors flex items-center gap-2">
              <Download className="w-4 h-4" /> Read the Paper
            </button>
          </div>
        </div>
      </section>

      
      {/* SLIDE 1.5: THE PLAIN LANGUAGE BREAKDOWN */}
      <section className="max-w-6xl mx-auto px-6 py-12 lg:py-24">
        <div className="text-center space-y-4 mb-16">
          <h2 className="font-serif text-3xl md:text-5xl text-[var(--color-ivory)]">The Big Picture</h2>
          <p className="text-[var(--color-muted)] text-lg max-w-2xl mx-auto">
            Breaking down the StrataKV breakthrough in plain English.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="glass-card p-8 rounded-2xl space-y-4 border-t-2 border-t-[var(--color-gold)]">
            <div className="w-12 h-12 rounded-full bg-[rgba(221,194,140,0.1)] flex items-center justify-center text-[var(--color-gold)] font-bold text-xl mb-6">1</div>
            <h3 className="font-serif text-2xl text-[var(--color-ivory)]">What We Did</h3>
            <p className="text-[var(--color-muted)] leading-relaxed">
              We completely redesigned how AI agents remember things. Standard AI models blindly memorize everything until they run out of memory and crash. We built StrataKV—a "breathing" memory engine that permanently pins core instructions while actively exhaling useless noise (like old tool logs).
            </p>
          </div>

          <div className="glass-card p-8 rounded-2xl space-y-4 border-t-2 border-t-[var(--color-success)]">
            <div className="w-12 h-12 rounded-full bg-[rgba(184,205,177,0.1)] flex items-center justify-center text-[var(--color-success)] font-bold text-xl mb-6">2</div>
            <h3 className="font-serif text-2xl text-[var(--color-ivory)]">Why It Matters</h3>
            <p className="text-[var(--color-muted)] leading-relaxed">
              Until now, running autonomous AI agents meant paying massive cloud bills or watching your local computer crash from "Out of Memory" errors. Our breakthrough allows highly complex AI swarms to run forever on consumer hardware securely, privately, and for zero recurring cost.
            </p>
          </div>

          <div className="glass-card p-8 rounded-2xl space-y-4 border-t-2 border-t-[var(--color-silver)]">
            <div className="w-12 h-12 rounded-full bg-[rgba(216,223,225,0.1)] flex items-center justify-center text-[var(--color-silver)] font-bold text-xl mb-6">3</div>
            <h3 className="font-serif text-2xl text-[var(--color-ivory)]">What Comes Next</h3>
            <p className="text-[var(--color-muted)] leading-relaxed">
              We are scaling the system to support entire swarms of collaborative agents orchestrated by the Elle Conductor. Soon, developers will be able to deploy sovereign, uncensorable AI systems that can independently manage codebases, servers, and operations indefinitely.
            </p>
          </div>
        </div>
      </section>

      {/* SLIDE 2: PRINCIPLED INTELLIGENCE */}
      <section className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div className="space-y-6">
          <div className="flex items-center gap-2 text-[var(--color-silver)] font-mono text-xs uppercase tracking-widest">
            <Brain className="w-4 h-4" /> Core Principle
          </div>
          <h2 className="font-serif text-4xl lg:text-5xl text-[var(--color-ivory)] leading-tight">
            Principled Intelligence: <br /> Active Inferencing
          </h2>
          <h3 className="text-xl text-[var(--color-gold)] font-serif italic">
            Minimizing Variational Free Energy Realized.
          </h3>
          <p className="text-[var(--color-muted)] leading-relaxed text-lg">
            True autonomy is not about memorizing noise; it is about epistemic regulation. StrataKV models the agent's interaction loop as Active Inference with an active Markov blanket. 
          </p>
          <p className="text-[var(--color-muted)] leading-relaxed text-lg">
            Internal intentions are pinned to an Invariant Core, while sensory feedback (tool outputs, noisy logs) is assimilated and thermodynamically dissipated to minimize variational free energy—suppressing apophenia and preventing attention hijacking.
          </p>
        </div>
        <div className="glass-card p-8 lg:p-12 relative overflow-hidden flex items-center justify-center min-h-[400px]">
          {/* Abstract Markov Blanket Visualization */}
          <div className="absolute inset-0 bg-gradient-to-br from-[rgba(184,205,177,0.05)] to-[rgba(221,194,140,0.05)] pointer-events-none"></div>
          <div className="relative w-full max-w-sm aspect-square rounded-full border border-[rgba(184,205,177,0.4)] flex items-center justify-center p-8">
            <div className="absolute top-4 text-xs font-mono text-[var(--color-success)] tracking-widest uppercase">Sensory States</div>
            <div className="absolute bottom-4 text-xs font-mono text-[var(--color-success)] tracking-widest uppercase">Active States</div>
            <div className="w-full h-full rounded-full border border-[rgba(221,194,140,0.6)] bg-[rgba(221,194,140,0.1)] flex items-center justify-center relative backdrop-blur-md">
               <div className="text-center">
                 <div className="font-serif text-2xl text-[var(--color-gold)]">Internal States</div>
                 <div className="text-xs text-[var(--color-muted)] font-mono mt-2">Invariant Core</div>
               </div>
            </div>
          </div>
        </div>
      </section>

      {/* SLIDE 3: ENGINEERING BREAKDOWN */}
      <section className="max-w-7xl mx-auto px-6 space-y-16">
        <div className="text-center space-y-4 max-w-3xl mx-auto">
          <h2 className="font-serif text-4xl lg:text-5xl text-[var(--color-ivory)]">
            Engineering Breakdown
          </h2>
          <p className="text-[var(--color-muted)] text-lg">
            A radical departure from monolithic Transformers. The Breathing Cache achieves 1,631x compression by isolating signals from noise on bare-metal silicon.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="glass-card p-8 space-y-6 hover:translate-y-[-4px] transition-transform duration-300 border-t-2 border-t-[var(--color-gold)]">
            <Layers className="w-8 h-8 text-[var(--color-gold)]" />
            <h3 className="font-serif text-2xl text-[var(--color-ivory)]">3-Tier Geometry</h3>
            <p className="text-[var(--color-muted)] leading-relaxed text-sm">
              An architectural topology dividing the context window into an Invariant Core (system prompts), a Harmonic Basin (geometric routing), and a Transient Fringe (scratchpad buffer). This isolates long-term directives from noisy operational loops.
            </p>
          </div>
          
          <div className="glass-card p-8 space-y-6 hover:translate-y-[-4px] transition-transform duration-300 border-t-2 border-t-[var(--color-silver)]">
            <Activity className="w-8 h-8 text-[var(--color-silver)]" />
            <h3 className="font-serif text-2xl text-[var(--color-ivory)]">Thermodynamic Exhalation</h3>
            <p className="text-[var(--color-muted)] leading-relaxed text-sm">
              A continuous 2% Milankovitch dissolution leak. Emulates biological inhalation and exhalation, purging decoy sequences and tool artifacts. Solves the OOM death-spiral without heuristic eviction metrics.
            </p>
          </div>

          <div className="glass-card p-8 space-y-6 hover:translate-y-[-4px] transition-transform duration-300 border-t-2 border-t-[var(--color-success)]">
            <Cpu className="w-8 h-8 text-[var(--color-success)]" />
            <h3 className="font-serif text-2xl text-[var(--color-ivory)]">Apple Silicon UMA</h3>
            <p className="text-[var(--color-muted)] leading-relaxed text-sm">
              Zero-copy Metal 3 integration on Apple M5 Pro. Dynamic Kernel Orchestration (25% Softmax Attention, 75% Gated DeltaNet) resolves 5-hop transitive logic within a 15.5GB resident footprint, leaving 67% free memory.
            </p>
          </div>
        </div>
      </section>

      
      {/* SLIDE 3.5: THE AGENTIC RUNBOOK (TERMINAL UI) */}
      <section className="border-t border-[rgba(255,255,255,0.05)] pt-12 mt-12 bg-[rgba(16,18,15,0.3)]">
        <AgenticRunbook />
      </section>

      {/* SLIDE 4: THE PAPER */}
      <section className="max-w-5xl mx-auto px-6 pt-16">
        <div className="glass-card p-10 lg:p-16 border-[rgba(221,194,140,0.3)] shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-[var(--color-gold)] opacity-5 blur-[100px] rounded-full pointer-events-none"></div>
          
          <div className="space-y-8 relative z-10">
            <div className="flex items-center gap-3">
              <span className="badge badge-gold font-mono uppercase tracking-widest text-xs">Official Whitepaper</span>
              <span className="badge badge-silver font-mono text-[10px]">Barteau & Claude, 2026</span>
            </div>
            
            <h2 className="font-serif text-3xl lg:text-4xl text-[var(--color-ivory)] leading-tight">
              StrataKV: Coherent Memory Geometry, Thermodynamic Exhalation, and Dynamic Kernel Orchestration for Resident Multi-Agent Tool Swarms
            </h2>
            
            <div className="prose prose-invert prose-sm max-w-none text-[var(--color-muted)] space-y-4">
              <p className="leading-relaxed">
                Autonomous multi-agent systems operating over long horizons exhibit a dual failure mode: the quadratic memory wall of standard Key-Value caches, and catastrophic attention hijacking induced by verbose, non-stationary tool feedback. On consumer Unified Memory Architectures (UMA) such as Apple Silicon (48 GB), monolithic transformers trigger fatal GPU command buffer out-of-memory panics within hundreds of turns.
              </p>
              <p className="leading-relaxed">
                We resolve this dilemma by introducing StrataKV (The Breathing Cache) orchestrated by the Elle Conductor. StrataKV establishes a three-tier Coherent Memory Geometry regulated by intake coherence curvature, the neurobiological Rajasethupathy Tri-Timer Law, thermodynamic exhalation, and a continuous 2% dissolution leak that acts as slow-wave computational sleep.
              </p>
              <p className="leading-relaxed">
                Across rigorous benchmarks on Apple Silicon Metal GPU, our architecture achieves definitive results: in an ultra-scale 3,000-step longitudinal siege, StrataKV compresses the active KV cache to 0.27 GB (1,631x compression), preserving all invariants while baselines suffer complete amnesia. StrataKV proves that sovereign, indefinitely stable autonomous multi-agent tool swarms can run permanently on consumer edge hardware.
              </p>
            </div>

            <div className="pt-6">
              <a href="#" className="inline-flex items-center gap-2 px-6 py-3 bg-[var(--color-gold)] text-[var(--color-ink)] font-bold rounded hover:bg-[#e8d0a5] transition-colors">
                <Download className="w-4 h-4" /> Download PDF (4.2 MB)
              </a>
            </div>
          </div>
        </div>
      </section>
      
    </div>
  );
};
