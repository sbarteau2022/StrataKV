const fs = require('fs');

let content = fs.readFileSync('src/components/MarketingDeck.tsx', 'utf-8');

// Add new icons to import
content = content.replace(
  "import { ArrowRight, Download, Brain, Activity, Cpu, Layers } from 'lucide-react';",
  "import { ArrowRight, Download, Brain, Activity, Cpu, Layers, Zap, CircleDot, BarChart3, Target, Orbit, Atom } from 'lucide-react';"
);

const deepKernelSlide = `
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
`;

// Inject between engineering breakdown and agentic runbook
content = content.replace(
  '{/* SLIDE 3.5: THE AGENTIC RUNBOOK (TERMINAL UI) */}',
  deepKernelSlide + '\n      {/* SLIDE 3.5: THE AGENTIC RUNBOOK (TERMINAL UI) */}'
);

fs.writeFileSync('src/components/MarketingDeck.tsx', content);
console.log('Successfully injected Dynamic Kernel, Toroidal Transformer, and Measuring Wrong Thing sections');
