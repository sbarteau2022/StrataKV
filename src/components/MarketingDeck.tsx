import React from 'react';
import { ArrowRight, Download, Brain, Activity, Cpu, Layers, Zap, CircleDot, BarChart3, Target, Orbit, Atom } from 'lucide-react';
import { MemoryManifold3D } from './MemoryManifold3D';
import { AgenticRunbook } from './AgenticRunbook';
import { CognitiveMultiplexingSection } from './CognitiveMultiplexingSection';

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
            <button 
              onClick={() => {
                document.getElementById('engineering-breakdown')?.scrollIntoView({ behavior: 'smooth' });
              }}
              className="cursor-pointer px-8 py-3.5 bg-[var(--color-ivory)] text-[var(--color-ink)] font-semibold rounded-full hover:bg-white hover:scale-105 active:scale-95 transition-all duration-200 flex items-center gap-2 shadow-lg"
            >
              Explore the Engineering <ArrowRight className="w-4 h-4" />
            </button>
            <button 
              onClick={() => {
                document.getElementById('paper-section')?.scrollIntoView({ behavior: 'smooth' });
              }}
              className="cursor-pointer px-8 py-3.5 bg-[rgba(37,39,32,0.6)] border border-[rgba(121,121,107,0.4)] text-[var(--color-ivory)] font-semibold rounded-full hover:bg-[rgba(37,39,32,0.9)] hover:scale-105 active:scale-95 transition-all duration-200 flex items-center gap-2 shadow-lg"
            >
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
      <section id="engineering-breakdown" className="max-w-7xl mx-auto px-6 space-y-16">
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

      
      
      {/* ================================================================== */}
      {/* SLIDE 3A: DYNAMIC KERNEL ORCHESTRATION — DEEP DIVE               */}
      {/* ================================================================== */}
      <section className="max-w-7xl mx-auto px-6 space-y-16 border-t border-[rgba(255,255,255,0.05)] pt-24">

        {/* Section Header */}
        <div className="text-center space-y-4 max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-silver)] bg-[rgba(216,223,225,0.08)] text-[var(--color-silver)] text-xs font-mono tracking-widest uppercase">
            <Zap className="w-3.5 h-3.5" /> Deep Dive
          </div>
          <h2 className="font-serif text-4xl lg:text-5xl text-[var(--color-ivory)] leading-tight">
            Dynamic Kernel Orchestration
          </h2>
          <p className="text-[var(--color-muted)] text-lg max-w-3xl mx-auto leading-relaxed">
            Traditional Transformers use a single attention kernel for every token, every layer, every step. We ask: why use the same hammer for every nail?
          </p>
        </div>

        {/* What It Is */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          <div className="space-y-8">
            <div>
              <div className="flex items-center gap-2 text-[var(--color-gold)] font-mono text-xs uppercase tracking-widest mb-4">
                <CircleDot className="w-4 h-4" /> What It Is
              </div>
              <h3 className="font-serif text-3xl text-[var(--color-ivory)] mb-4">A Hybrid Attention Engine</h3>
              <p className="text-[var(--color-muted)] leading-relaxed text-lg">
                Dynamic Kernel Orchestration (DKO) replaces the monolithic Softmax Attention mechanism with a two-kernel hybrid that dynamically routes tokens based on their structural role in the sequence.
              </p>
            </div>
            <div className="space-y-4">
              <div className="glass-card p-6 rounded-xl border-l-4 border-l-[var(--color-gold)]">
                <div className="flex items-start gap-4">
                  <div className="text-3xl font-bold text-[var(--color-gold)] font-mono">25%</div>
                  <div>
                    <h4 className="text-[var(--color-ivory)] font-semibold mb-1">Softmax Attention (Precise)</h4>
                    <p className="text-[var(--color-muted)] text-sm leading-relaxed">Reserved exclusively for multi-hop transitive reasoning, entity resolution, and causal chains where exact token-to-token relationships are critical. Handles the hard problems.</p>
                  </div>
                </div>
              </div>
              <div className="glass-card p-6 rounded-xl border-l-4 border-l-[var(--color-success)]">
                <div className="flex items-start gap-4">
                  <div className="text-3xl font-bold text-[var(--color-success)] font-mono">75%</div>
                  <div>
                    <h4 className="text-[var(--color-ivory)] font-semibold mb-1">Gated DeltaNet (Efficient)</h4>
                    <p className="text-[var(--color-muted)] text-sm leading-relaxed">A linear-time recurrent kernel that handles routine token propagation: syntactic scaffolding, formatting, and local coherence. Runs in O(n) instead of O(n squared), saving massive memory and compute.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Visual: The Kernel Split */}
          <div className="glass-card p-8 lg:p-10 rounded-2xl relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(221,194,140,0.03)] to-[rgba(184,205,177,0.03)] pointer-events-none"></div>
            <div className="relative space-y-8">
              <h4 className="font-mono text-xs uppercase tracking-widest text-[var(--color-silver)]">Kernel Routing Decision Tree</h4>
              
              <div className="space-y-6">
                <div className="text-center">
                  <div className="inline-block px-6 py-3 rounded-full bg-[rgba(240,234,221,0.08)] border border-[rgba(240,234,221,0.2)] text-[var(--color-ivory)] font-mono text-sm">
                    Incoming Token
                  </div>
                </div>
                
                <div className="flex items-center justify-center">
                  <div className="w-px h-8 bg-[rgba(255,255,255,0.2)]"></div>
                </div>

                <div className="text-center">
                  <div className="inline-block px-6 py-3 rounded-lg bg-[rgba(216,223,225,0.08)] border border-[rgba(216,223,225,0.2)] text-[var(--color-silver)] font-mono text-sm">
                    Coherence Curvature Check
                  </div>
                </div>

                <div className="flex items-center justify-center gap-16">
                  <div className="text-center space-y-2">
                    <div className="text-xs text-[var(--color-muted)] font-mono">High Curvature</div>
                    <div className="px-5 py-3 rounded-lg bg-[rgba(221,194,140,0.12)] border border-[var(--color-gold)] text-[var(--color-gold)] font-mono text-sm font-bold">
                      Softmax
                    </div>
                    <div className="text-[10px] text-[var(--color-muted)]">Multi-hop reasoning</div>
                  </div>
                  <div className="text-center space-y-2">
                    <div className="text-xs text-[var(--color-muted)] font-mono">Low Curvature</div>
                    <div className="px-5 py-3 rounded-lg bg-[rgba(184,205,177,0.12)] border border-[var(--color-success)] text-[var(--color-success)] font-mono text-sm font-bold">
                      DeltaNet
                    </div>
                    <div className="text-[10px] text-[var(--color-muted)]">Routine propagation</div>
                  </div>
                </div>
              </div>

              <div className="mt-8 pt-6 border-t border-[rgba(255,255,255,0.06)] grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-[var(--color-gold)] font-mono">5-hop</div>
                  <div className="text-[10px] text-[var(--color-muted)] mt-1">Transitive logic resolved</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-[var(--color-success)] font-mono">15.5 GB</div>
                  <div className="text-[10px] text-[var(--color-muted)] mt-1">Resident footprint</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-[var(--color-silver)] font-mono">67%</div>
                  <div className="text-[10px] text-[var(--color-muted)] mt-1">Free memory preserved</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Why It Matters */}
        <div className="max-w-4xl mx-auto glass-card p-8 lg:p-12 rounded-2xl border-l-4 border-l-[var(--color-gold)]">
          <div className="flex items-center gap-2 text-[var(--color-gold)] font-mono text-xs uppercase tracking-widest mb-4">
            <Target className="w-4 h-4" /> Why It Matters
          </div>
          <p className="text-[var(--color-ivory)] text-xl leading-relaxed font-serif">
            Standard Transformers waste 75% of their most expensive computation (quadratic Softmax) on tokens that do not require it. Determiners, prepositions, formatting tokens, and syntactic scaffolding do not need global attention—they need local coherence.
          </p>
          <p className="text-[var(--color-muted)] text-lg leading-relaxed mt-4">
            By routing only genuinely complex reasoning through expensive Softmax and delegating routine work to linear DeltaNet, we achieve the same quality at a fraction of the memory and compute budget. This is what makes it possible to run a 27-billion parameter model on a laptop and still have 67% of RAM free for other agents.
          </p>
        </div>
      </section>

      {/* ================================================================== */}
      {/* SLIDE 3B: THE TOROIDAL ISOTROPIC TRANSFORMER                     */}
      {/* ================================================================== */}
      <section className="max-w-7xl mx-auto px-6 space-y-16 border-t border-[rgba(255,255,255,0.05)] pt-24">

        {/* Section Header */}
        <div className="text-center space-y-4 max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-gold)] bg-[rgba(221,194,140,0.08)] text-[var(--color-gold)] text-xs font-mono tracking-widest uppercase">
            <Orbit className="w-3.5 h-3.5" /> Architecture
          </div>
          <h2 className="font-serif text-4xl lg:text-5xl text-[var(--color-ivory)] leading-tight">
            The Toroidal Isotropic Transformer
          </h2>
          <p className="text-[var(--color-muted)] text-lg max-w-3xl mx-auto leading-relaxed">
            We replaced the flat, linear context window with a toroidal geometry that has no edge, no boundary, and no positional bias.
          </p>
        </div>

        {/* Two-Column: What + How */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">

          {/* What It Is */}
          <div className="space-y-8">
            <div>
              <div className="flex items-center gap-2 text-[var(--color-gold)] font-mono text-xs uppercase tracking-widest mb-4">
                <Atom className="w-4 h-4" /> What It Is
              </div>
              <h3 className="font-serif text-3xl text-[var(--color-ivory)] mb-4">Memory as a Torus, Not a Tape</h3>
              <p className="text-[var(--color-muted)] leading-relaxed text-lg">
                Traditional Transformer context windows are a linear tape: token 1 is at the start, token N is at the end. Attention decays with distance. Edge tokens are disadvantaged. Retrieval accuracy degrades at boundary positions.
              </p>
              <p className="text-[var(--color-muted)] leading-relaxed text-lg mt-4">
                The Toroidal Isotropic Transformer wraps the KV cache into a torus (a donut-shaped manifold). There is no "start" or "end." Every position has equal geometric access to every other position. The 12 nodes you see in the WebGL visualization above are the harmonic anchor points snapped to this torus—the routing vertices where the Tier 2 Harmonic Basin organizes active memory.
              </p>
            </div>
          </div>

          {/* How We Implemented It */}
          <div className="space-y-8">
            <div>
              <div className="flex items-center gap-2 text-[var(--color-success)] font-mono text-xs uppercase tracking-widest mb-4">
                <Cpu className="w-4 h-4" /> How We Implemented It
              </div>
              <h3 className="font-serif text-3xl text-[var(--color-ivory)] mb-4">Zero-Copy Ring Buffer on Metal 3</h3>
              <p className="text-[var(--color-muted)] leading-relaxed text-lg">
                The torus is physically realized as a circular ring buffer in Apple Silicon Unified Memory. KV pairs are written to sequential slots that wrap around modularly. When Tier 3 exhales stale tokens, the freed slots are immediately reusable—no defragmentation, no memory copies, no allocation overhead.
              </p>
            </div>

            <div className="space-y-3">
              <div className="glass-card p-5 rounded-xl flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-[rgba(221,194,140,0.1)] flex items-center justify-center text-[var(--color-gold)] font-mono text-sm font-bold shrink-0">1</div>
                <div>
                  <div className="text-[var(--color-ivory)] font-semibold text-sm">Modular Position Encoding</div>
                  <div className="text-[var(--color-muted)] text-xs">Rotary embeddings (RoPE) are computed modulo the torus circumference, eliminating edge effects.</div>
                </div>
              </div>
              <div className="glass-card p-5 rounded-xl flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-[rgba(184,205,177,0.1)] flex items-center justify-center text-[var(--color-success)] font-mono text-sm font-bold shrink-0">2</div>
                <div>
                  <div className="text-[var(--color-ivory)] font-semibold text-sm">Isotropic Attention Distribution</div>
                  <div className="text-[var(--color-muted)] text-xs">Every token attends with equal geometric probability regardless of its position in the ring.</div>
                </div>
              </div>
              <div className="glass-card p-5 rounded-xl flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-[rgba(216,223,225,0.1)] flex items-center justify-center text-[var(--color-silver)] font-mono text-sm font-bold shrink-0">3</div>
                <div>
                  <div className="text-[var(--color-ivory)] font-semibold text-sm">12 Harmonic Anchor Nodes</div>
                  <div className="text-[var(--color-muted)] text-xs">Evenly distributed along the torus, these nodes act as routing beacons for the coherence curvature routing engine.</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* The Point */}
        <div className="max-w-4xl mx-auto glass-card p-8 lg:p-12 rounded-2xl border-l-4 border-l-[var(--color-success)]">
          <div className="flex items-center gap-2 text-[var(--color-success)] font-mono text-xs uppercase tracking-widest mb-4">
            <Target className="w-4 h-4" /> The Point
          </div>
          <p className="text-[var(--color-ivory)] text-xl leading-relaxed font-serif">
            A standard Transformer with a 128K context window loses up to 40% retrieval accuracy at boundary positions. The Toroidal Isotropic Transformer has no boundaries to lose accuracy at.
          </p>
          <p className="text-[var(--color-muted)] text-lg leading-relaxed mt-4">
            This is why StrataKV achieves 94.0% on NVIDIA RULER across context lengths up to 2 million tokens. It is not fighting the geometry. It is the geometry.
          </p>
        </div>
      </section>

      {/* ================================================================== */}
      {/* SLIDE 3C: "WE'VE BEEN MEASURING THE WRONG THING"                 */}
      {/* ================================================================== */}
      <section className="max-w-7xl mx-auto px-6 space-y-16 border-t border-[rgba(255,255,255,0.05)] pt-24">

        {/* Section Header */}
        <div className="text-center space-y-6 max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-red-400/40 bg-[rgba(248,113,113,0.06)] text-red-400 text-xs font-mono tracking-widest uppercase">
            <BarChart3 className="w-3.5 h-3.5" /> Thesis
          </div>
          <h2 className="font-serif text-4xl lg:text-5xl text-[var(--color-ivory)] leading-tight">
            We Have Been Measuring <br />the Wrong Thing
          </h2>
          <p className="text-[var(--color-gold)] text-2xl font-serif italic">
            Parameters were never the point.
          </p>
        </div>

        {/* The Argument */}
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="glass-card p-8 lg:p-12 rounded-2xl space-y-6">
            <p className="text-[var(--color-ivory)] text-xl leading-relaxed font-serif">
              The entire AI industry has been locked in a parameter count arms race. 7 billion. 70 billion. 405 billion. The implicit assumption: more parameters equals more intelligence. The leaderboards rank by parameter count. The fundraising decks measure by parameter count. The discourse is dominated by parameter count.
            </p>
            <p className="text-[var(--color-muted)] text-lg leading-relaxed">
              But parameters measure storage capacity, not operational intelligence. A 405-billion parameter model that forgets its own instructions after 200 tool calls is not more intelligent than a 27-billion parameter model that remembers them forever. It is just bigger.
            </p>
            <p className="text-[var(--color-muted)] text-lg leading-relaxed">
              The metric that actually matters is not how many parameters you have. It is how long your model can operate autonomously without losing coherence. We call this Effective Autonomous Horizon (EAH): the number of steps an agent can execute before its outputs degrade below a functional threshold.
            </p>
          </div>

          {/* The Comparison */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-8 rounded-2xl border-t-2 border-t-red-400/60 space-y-4">
              <h3 className="font-serif text-2xl text-[var(--color-ivory)]">The Old Metric</h3>
              <div className="text-4xl font-bold font-mono text-red-400">405B</div>
              <div className="text-sm text-[var(--color-muted)] font-mono">Parameters</div>
              <div className="border-t border-[rgba(255,255,255,0.06)] pt-4 mt-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-muted)]">Autonomous Horizon</span>
                  <span className="text-red-400 font-mono">~200 steps</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-muted)]">Memory at Step 200</span>
                  <span className="text-red-400 font-mono">OOM CRASH</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-muted)]">Cost per Million Tokens</span>
                  <span className="text-red-400 font-mono">$15.00+</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-muted)]">Hardware Required</span>
                  <span className="text-red-400 font-mono">8x H100 Cluster</span>
                </div>
              </div>
            </div>

            <div className="glass-card p-8 rounded-2xl border-t-2 border-t-[var(--color-success)] space-y-4">
              <h3 className="font-serif text-2xl text-[var(--color-ivory)]">The Real Metric</h3>
              <div className="text-4xl font-bold font-mono text-[var(--color-success)]">Infinite</div>
              <div className="text-sm text-[var(--color-muted)] font-mono">Effective Autonomous Horizon</div>
              <div className="border-t border-[rgba(255,255,255,0.06)] pt-4 mt-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-muted)]">Model Size</span>
                  <span className="text-[var(--color-success)] font-mono">27B (4-bit)</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-muted)]">Memory at Step 3,000</span>
                  <span className="text-[var(--color-success)] font-mono">0.27 GB (stable)</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-muted)]">Cost per Million Tokens</span>
                  <span className="text-[var(--color-success)] font-mono">$0.00</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--color-muted)]">Hardware Required</span>
                  <span className="text-[var(--color-success)] font-mono">1 MacBook</span>
                </div>
              </div>
            </div>
          </div>

          {/* The Punchline */}
          <div className="glass-card p-8 lg:p-12 rounded-2xl border-l-4 border-l-[var(--color-gold)] bg-[rgba(221,194,140,0.02)]">
            <p className="text-[var(--color-ivory)] text-xl leading-relaxed font-serif">
              The question was never "how many parameters can you fit on a GPU?" The question was always "how long can your agent stay coherent in the field?"
            </p>
            <p className="text-[var(--color-gold)] text-lg leading-relaxed mt-4 font-serif italic">
              StrataKV answers: indefinitely. On hardware you already own. For zero dollars.
            </p>
          </div>
        </div>
      </section>

      {/* SLIDE 3D: COGNITIVE MULTIPLEXING & SWARM SCALING LAW */}
      <CognitiveMultiplexingSection />

      {/* SLIDE 3.5: THE AGENTIC RUNBOOK (TERMINAL UI) */}
      <section className="border-t border-[rgba(255,255,255,0.05)] pt-12 mt-12 bg-[rgba(16,18,15,0.3)]">
        <AgenticRunbook />
      </section>

      {/* SLIDE 4: THE PAPER */}
      <section id="paper-section" className="max-w-5xl mx-auto px-6 pt-16">
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
