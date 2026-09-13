# The Agentic AI Runbook: Operational & Mathematical Specification
## Continuous Active Inference Steering, CORDIS Provenance Quarantine, and the 13-Sphere Differential Atlas

[![Status: Production Spec](https://img.shields.io/badge/Status-Production_Specification-success.svg)]()
[![Component: StrataKV Runbook](https://img.shields.io/badge/Component-stratakv.runbook-blue.svg)]()
[![Platform: Apple Silicon](https://img.shields.io/badge/Platform-Apple_Silicon_Metal-orange.svg)]()
[![Preprint: Complementary Document](https://img.shields.io/badge/Manuscript-18_Page_Paper_Sec_6-darkred.svg)](paper/main.pdf)

> **"A passive memory cache is an open door to cognitive collapse. An autonomous agent cannot merely store tokens; it must steer its own thermodynamic state across phase boundaries, quarantine untrusted tool cascades, and hold ambiguity in geometric superposition until reality resolves."**  
> — S. Barteau, *The Geometry of Coherent Memory* (September 2026).

---

## 1. Executive Summary & Foundational Paradigm

Standard Key-Value (KV) cache management in large language model inference treats memory as a passive, append-only linear tape ($\mathcal{K}, \mathcal{V} \in \mathbb{R}^{T \times d}$). In autonomous multi-turn agent loops (e.g., iterative code generation, compiler debugging, shell tool execution, web research), this passive paradigm leads directly to three structural failure modes:

1. **The Lorentz Horizon Explosion**:
   As context length $T$ grows, tool output floods (raw compiler stderr cascades, multi-page JSON payloads, terminal core dumps) rapidly consume available Unified Memory Architecture (UMA), triggering catastrophic Apple Silicon Metal GPU driver command buffer out-of-memory panics:
   ```
   RuntimeError: [METAL] Command buffer execution failed:
   Insufficient Memory (00000008:kIOGPUCommandBufferCallbackErrorOutOfMemory)
   ```
2. **The Embedding Hijacking Attack**:
   Adversarial decoys or near-miss distractors ($\cos \theta \in [0.88, 0.93]$) embedded inside legitimate tool outputs seduce attention heads. In naive semantic caching, ungrounded vector similarity classifies distractors as high-salience invariants, freezing them into RAM ($97.6\%$ attention hijacking) and evicting foundational root user constraints (**Semantic Calcification**).
3. **Active Inference Attractor Collapse (Theorem 6)**:
   When an external tool execution fails, the agent's internal error-correction loop increases precision on the failed sub-goal ($\Pi_2 \to \infty$). This attenuates observation precision to zero ($\Pi_1^* \to 0$), blinding the model to subsequent tool feedback and trapping the agent in an infinite, repetitive tool-retry cycle (**Agentic Sundowning**).

The **Agentic AI Runbook** ($AI_{\text{KV}}$ + CORDIS + StrataKV) is an active thermodynamic control system implemented directly in Python (`stratakv.runbook.AgenticRunbook`). It continuously regulates memory intake, freezes verified invariants, enforces cryptographic-grade provenance quarantine, steers execution via active inference ($\kappa, d, \Delta$), holds candidate reasoning paths in geometric superposition, and periodically purges noise through a 2% Milankovitch dissolution leak.

---

## 2. Macro-System Architecture & Stack Division of Labor

The Runbook coordinates three distinct layers of the cognitive stack:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE COMPLETE SYSTEM ARCHITECTURE                                     │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                        │
│  [1] THE GLOBAL GEOMETRY: 13-SPHERE VECTOR EQUILIBRIUM IN HYPERBOLIC/TOROIDAL PRODUCT (Hⁿ × 𝕋ⁿ)         │
│                                                                                                        │
│                                      HYPERBOLIC POINCARÉ BALL ℍⁿ                                       │
│                    ┌─────────────────────────────────────────────────────────────┐                     │
│                    │                  TOROIDAL FIELD 𝕋ⁿ (Compact Lie Group)      │                     │
│                    │            ┌───────────────────────────────────┐            │                     │
│                    │            │           [U1]     [U2]           │            │                     │
│                    │            │             \     /               │            │                     │
│                    │            │    [U12]----( U0 )----[U3]        │            │                     │
│                    │            │       /   / |   \   \             │            │                     │
│                    │            │     [U11] [U10][U9]  [U4] [U5]    │            │                     │
│                    │            │       \     |     /               │            │                     │
│                    │            │        [U8]-[U7]-[U6]             │            │                     │
│                    │            └───────────────────────────────────┘            │                     │
│                    └─────────────────────────────────────────────────────────────┘                     │
│                                                                                                        │
│  • Chart U_0 (Conductor / Coordinator): At origin u = 0. Anchors stability, routing, and consensus.    │
│  • 12 Faculty Spheres (U_1 .. U_12): Kissing U_0 in 3D Vector Equilibrium (R = 2r = 1.0),             │
│    snapped directly to the toroidal cycles along 6 canonical antipodal axes.                           │
│  • Fluid Volumetric Fill: Swarm token load expands internal density ρ_k, keeping centers c_k rigid.     │
│                                                                                                        │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                        │
│  [2] THE STACK DIVISION OF LABOR: RUNTIME vs. CARTOGRAPHER vs. SILICON ENGINE                          │
│                                                                                                        │
│  ┌───────────────────────────┐   ┌────────────────────────────┐   ┌─────────────────────────────────┐  │
│  │   ELLE RUNTIME WORKER     │   │     THE CARTOGRAPHER       │   │       THE SILICON ENGINE        │  │
│  │      (`elle-worker`)      │   │    (`elle_rust_harness` /  │   │        (`mlx-serve` / Metal)    │  │
│  │                           │   │           `DHNG`)          │   │                                 │  │
│  │ • Mind (`mind.ts`):       │   │ • Pure Rust & TypeScript   │   │ • 27B Resident Hybrid Model     │  │
│  │   Cognitive loop & κ loss │   │ • Deterministic & Static   │   │   (Qwen 27B Q4_K_M: 15.40 GB)   │  │
│  │ • Router (`router.ts`):   │   │ • ZERO LLM in compute path │   │ • The Dynamic Kernel (3:1):     │  │
│  │   12 faculty tool dispatch│   │ • Computes Poincaré ball   │   │   - 75% Gated DeltaNet (21L):   │  │
│  │ • Conductor:              │   │   metric & Lorentz charts  │   │     O(1) recurrence (15 MB)     │  │
│  │   Jitterbug pulse (12+1↔13│   │ • Cycle rank b₁, homology  │   │   - 25% Softmax Attention (7L): │  │
│  │ • CORDIS Runbook:         │   │ • Verifies Gates G1–G8     │   │     Powered by StrataKV         │  │
│  │   Quarantine tool floods  │   │ ───────────────────────────│   │ • Role: Librarian & Executioner │  │
│  │   to Tiers 2 & 3          │   │ LOAD-BEARING INVARIANT:    │   │ • 48 GB Unified Memory (UMA):   │  │
│  │                           │   │ Elle has READ-ONLY access. │   │   15.53 GB resident footprint   │  │
│  │                           │   │ Elle CANNOT pose mirror!   │   │   32.47 GB (67.4%) free headroom│  │
│  └─────────────┬─────────────┘   └──────────────┬─────────────┘   └────────────────┬────────────────┘  │
│                │                                │                                  │                   │
│                └─────────────────► READ-ONLY ◄──┴──────────────────────────────────┘                   │
│                                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### The Three Load-Bearing Realities:
1. **The Geometric Nesting ($\mathbb{H}^n \supset \mathbb{T}^n \supset \mathcal{A}_{13}$)**:
   - **Hyperbolic Outer Container ($\mathbb{H}^n$)**: The Poincaré ball model provides exponential metric volume ($V \propto e^r$) accommodating tree-like reasoning depth and unbounded conceptual branching without metric cramping.
   - **Toroidal Recurrent Field ($\mathbb{T}^n$)**: The compact flat torus $\mathbb{T}^n = (\mathbb{R}/2\pi\mathbb{Z})^n$ governs periodic recurrence, rhythm, and integer topological winding invariants ($W \in \pi_1(\mathbb{T}^n) \cong \mathbb{Z}^n$).
   - **Conductor Core ($U_0$)**: Located at origin $u = \mathbf{0}$, anchoring global Lyapunov stability and consensus.
   - **12 Faculty Spheres ($U_1 \dots U_{12}$)**: Kissing $U_0$ at $R = 2r = 1.0$ in 3D Vector Equilibrium, snapped directly to toroidal cycles along 6 antipodal axes. Variance in load manifests as internal fluid density ($\rho_k$), leaving coordinates $c_k$ invariant.
2. **The Mirror Invariant**:
   - The Rust harness (`elle_rust_harness` / `Dynanic-Hyperbolic-Neural-Graph`) calculates geometry on-device using pure, deterministic static functions with **zero LLM in the computation path**.
   - Elle has **strictly read-only access** to the Atlas. The model cannot reach into and pose its own mirror.
3. **The Resident Silicon Footprint**:
   - Running on Apple Silicon Metal (48 GB UMA), the full Qwen 27B quantized base model occupies **15.40 GB**.
   - DeltaNet recurrent state occupies **0.015 GB (15 MB)**.
   - StrataKV dynamic breathing cache occupies **0.115 GB to 0.256 GB**.
   - **Total resident footprint**: **15.53 GB**, leaving **32.47 GB (67.4%) free headroom** for parallel OS operations and compilation tasks.

---

## 3. The 5-Phase Agentic AI Runbook Workflow

```
                                  THE 5-PHASE RUNBOOK LIFECYCLE
                                  
    [ PHASE 1: FOUNDATION INTAKE ]
    • System prompt & root user constraints ingested.
    • Coordinator U_0 writes to Tier 1 Invariant Core (Ash1l).
    • Goal vector g established for hyperbolic distance tracking.
                 │
                 ▼  (Root constraints verified)
    [ PHASE 2: MID-TIER EXECUTION ]
    • FREEZE TIER 1 KV: Immutable preamble created.
    • Specialized sub-agents receive isolated Read-Me Only Sub-Atlas Spheres.
    • CORDIS Provenance Quarantine active: Silos 8–12 (tools) routed strictly to Tiers 2/3.
                 │
                 ▼  (Parallel execution / tool calls)
    [ PHASE 3: HIGH-TIER REASONING ]
    • Active Inference Steering: evaluates κ = σ(z), d_H(k, g), and token spend Δ.
    • CONTINUE: High κ, Low d -> proceed with execution.
    • NUDGE: Low κ, High d -> hold candidate branches in Superposition (|Ψ⟩).
    • KILL: Spend > Predicted & Δ <= 0 -> thermodynamic emergency halt.
                 │
                 ▼  (Periodic Fibonacci checkpoints: F_k = {8, 13, 21, 34, ...})
    [ PHASE 4: COMPUTATIONAL SLEEP & DISSOLUTION ]
    • Exhale pass triggered: 2% Milankovitch dissolution leak (L_leak = 0.020).
    • Tier 2 Harmonic Basin consolidated via golden-ratio pooling (stride ⌈φⁿ⌉).
    • Tier 3 Transient Fringe purged into thermodynamic vacuum.
                 │
                 ▼  (Mission completion / convergence)
    [ PHASE 5: MASTER ATLAS DISTILLATION ]
    • Surviving crystallized invariants projected to Riemannian coordinates on M = Hⁿ × 𝕋ⁿ.
    • Discovered failure boundaries recorded as negative-curvature barriers.
```

### Phase Specifications:

| Phase ID | Name | Permitted Writers | Tier 1 Status | Tier 2 Status | Quarantine Policy |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `FOUNDATION_INTAKE` | Coordinator ($U_0$) Only | **Writeable** | Initializing | Enforced (no tool execution) |
| **2** | `MID_TIER_EXECUTION`| Faculty Agents ($U_1..U_{12}$)| **FROZEN** (Immutable)| Active Inhale | **Quarantine Silos 8–12 to Tiers 2/3** |
| **3** | `HIGH_TIER_REASONING`| Swarm Sub-Agents | **FROZEN** | Harmonic Breathing| Superposition Holding Active |
| **4** | `COMPUTATIONAL_SLEEP`| Self / Cache Engine | **FROZEN** | $\varphi$-Wound Pooling| 2% Milankovitch Dissolution Leak |
| **5** | `ATLAS_DISTILLATION` | Coordinator / Engine | **Consolidated** | Consolidated | Distill to $\mathcal{M} = \mathbb{H}^n \times \mathbb{T}^n$ |

---

## 4. CORDIS Provenance Quarantine (Defusing Embedding Hijacking)

### 4.1 The Threat Model: The Embedding Hijacking Attack
In long-context agent loops, external tool executions return unpredictable token streams:
- Compiler outputs containing thousands of lines of warnings.
- Adversarial decoys: near-miss strings planted by malicious inputs or hallucinated code containing high semantic overlap with root objectives ($\cos \theta \approx 0.90$).

In conventional caches, high semantic similarity causes the cache controller to classify the decoy as an essential invariant, enrolling it into long-term memory. Over hundreds of steps, decoys hijack up to **97.6% of attention mass**, completely erasing original instructions.

### 4.2 The CORDIS Quarantine Implementation
The `ProvenanceQuarantine` engine inspects incoming token representations and provenance metadata:
1. **Source Tag Filtering**: Any stream originating from `compiler_stderr`, `compiler_noise`, `terminal_exec`, `json_payload`, or `ast_dump` is automatically quarantined.
2. **Silo Bounding (Silos 8–12)**: Sub-agents assigned to execution roles (Code Execution, System Shell, Network I/O) are physically prohibited from emitting Tier 1 tokens.
3. **Physical Tier Assignment**: Quarantined streams are clamped to **Tier 2 (Harmonic Basin)** or **Tier 3 (Transient Fringe)**:
   $$\text{Assigned Tier} = \max(\text{Requested Tier}, \, 2)$$
   Even if the payload contains $\cos \theta = 0.99$ similarity to the root prompt, it **cannot breach Tier 1**.
4. **Thermodynamic Purge**: In Tier 2 and Tier 3, quarantined decoys are subjected to the 2% Milankovitch dissolution leak, dissipating within 2–3 Fibonacci intervals while the genuine Tier 1 invariant remains 100% intact.

```
Benchmarked SDR Result:
Monolithic (No Quarantine):     0.25x  (Decoy hijacks 84.8% attention mass)
PyramidKV (No Quarantine):      0.25x  (Decoy hijacks 25.1% attention mass)
StrataKV + CORDIS Quarantine:  10.80x  (Decoy suppressed to 1.18%, Root retained at 12.71%)
```

---

## 5. Active Inference Steering & The Decision Operator

The Runbook continuously tracks the agent's cognitive trajectory using three coupled signals:

1. **Instantaneous Coherence Curvature ($\kappa = \sigma(z) \in [0, 1]$)**:
   Measures structural self-consistency and surprisal. Derived from token prediction error and semantic confidence.
2. **Continuous Hyperbolic Distance ($d_{\mathbb{H}^n}(\bar{\mathbf{k}}, \mathbf{g})$)**:
   Computes the Riemannian geodesic distance between the current average key state $\bar{\mathbf{k}}$ and the root mission goal anchor $\mathbf{g}$ in the Poincaré ball:
   $$d_{\mathbb{H}^n}(\bar{\mathbf{k}}, \mathbf{g}) = \arcosh\left( 2 - \cos \theta \right)$$
3. **Token Spend Envelope ($\Delta$)**:
   The `PredictionOperator` (implementing competitive persistence, EMA $\alpha=0.3$, and AR(2) forecasting with Welford z-scoring) predicts the expected token spend ceiling $\hat{\Delta}$.

### 5.1 The Tripartite Intervention Policy:

```python
# Formal Decision Logic in stratakv.runbook.AgenticRunbook:
if spend > predicted_ceiling and delta_rate <= 0.0:
    action = "KILL"       # Thermodynamic emergency brake: budget exceeded with zero progress
elif kappa < 0.65 and dist >= 1.20:
    action = "NUDGE"      # Drift detected: hold hypotheses in superposition, send scratchboard nudge
else:
    action = "CONTINUE"   # Coherent alignment: proceed with execution
```

### 5.2 Superposition Holding Unified Function ($|\Psi_{\text{holding}}\rangle$)
When a `NUDGE` is triggered, instead of allowing the model to make an ungrounded, irreversible commitment (which triggers tool-loop suicide), the Runbook activates the Superposition Holding Engine:
- It bundles $M$ candidate trajectory states into an uncollapsed superposition:
  $$|\Psi_{\text{holding}}\rangle = \sum_{m=1}^M c_m |h_m\rangle, \quad \text{with } c_m = \frac{\kappa_m e^{-d_m}}{\sum_j \kappa_j e^{-d_j}}$$
- It locks destructive token spending and binds the agent's active communication to the **2-way scratchboard**.
- When subsequent evidence restores coherence ($\kappa \ge 0.65, d < 1.20$), the bundle collapses cleanly to the winning branch, resuming forward execution.

---

## 6. Thermodynamic Sleep & The 2% Dissolution Leak

### 6.1 The Landauer Tax and Semantic Calcification
In physical cognition, zero-leak memory architectures suffer from **Semantic Calcification**: obsolete intermediate hypotheses crystallize into permanent memory, exhausting the representation manifold and causing the model to defend incorrect hypotheses dogmatically.

Conversely, aggressive naive eviction forces the **Landauer Suppression Tax** ($W_{\text{suppress}} \ge k_B T \ln 2 \cdot \Delta H$), destroying intermediate deductive premises and causing **Agentic Sundowning** ($A(t) = A_0 e^{-\gamma t}$).

### 6.2 The Solution: The 2% Milankovitch Wobble Leak
StrataKV operationalizes slow-wave sleep by triggering a continuous 2% dissolution leak at Fibonacci intervals ($F_k \in \{8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987\}$):
$$S_{t+1} = 0.980 \cdot S_t + 0.020 \cdot S_0$$
- Tier 1 Invariants are strictly shielded from dissipation ($S_{\text{Core}} = S_0$).
- Tier 2 Harmonic Basin undergoes spatial pooling with stride $S = \lceil \varphi^n \rceil$.
- Tier 3 Transient Fringe is dissolved into the thermodynamic vacuum.

---

## 7. Python API Reference (`stratakv.runbook`)

### Quickstart Example:

```python
import numpy as np
from stratakv import StrataKVCache, AgenticRunbook, RunbookPhase

# 1. Initialize Cache & Goal Anchor
goal_anchor = np.random.randn(128).astype(np.float32)
goal_anchor /= np.linalg.norm(goal_anchor)

cache = StrataKVCache(
    max_active_budget=2048,
    head_dim=128,
    num_heads=16,
    goal_vector=goal_anchor,
    dissolution_leak_rate=0.020
)

# 2. Initialize Agentic Runbook
runbook = AgenticRunbook(
    cache=cache,
    goal_vector=goal_anchor,
    drift_distance_threshold=1.20,
    drift_kappa_threshold=0.65
)

# --- PHASE 1: FOUNDATION INTAKE ---
k_root = np.random.randn(256, 16, 128).astype(np.float32)
v_root = np.random.randn(256, 16, 128).astype(np.float32)
runbook.inhale(k_root, v_root, start_pos=0, source_tag="root_prompt", is_needle=True)

# --- PHASE 2: MID-TIER EXECUTION (FREEZE TIER 1) ---
runbook.set_phase(RunbookPhase.MID_TIER_EXECUTION)

# Inhale noisy tool output (CORDIS quarantine intercepts this!)
k_tool = np.random.randn(1024, 16, 128).astype(np.float32)
v_tool = np.random.randn(1024, 16, 128).astype(np.float32)
runbook.inhale(
    k_tool, v_tool, start_pos=256,
    source_tag="compiler_stderr",
    is_tool_output=True,
    silo_id=9
)

# --- PHASE 3: HIGH-TIER REASONING & ACTIVE INFERENCE STEERING ---
runbook.set_phase(RunbookPhase.HIGH_TIER_REASONING)

# Step evaluation
k_step = np.random.randn(64, 16, 128).astype(np.float32)
intervention = runbook.step(k_step, step_spend=64, delta_rate=1.0)
print(f"Action: {intervention.action} | Confidence: {intervention.confidence:.3f}")

if intervention.action == "NUDGE":
    # Ambiguity detected -> hold candidate hypotheses in superposition
    cand_a = np.random.randn(16, 16, 128).astype(np.float32)
    cand_b = np.random.randn(16, 16, 128).astype(np.float32)
    bundle = runbook.hold_superposition([cand_a, cand_b])
    print(f"Superposition Bundle Status: {bundle.status}")

# --- PHASE 5: MASTER ATLAS DISTILLATION ---
distilled_atlas = runbook.distill(failure_branches=[
    {"task": "unit_test_auth", "error": "Signature mismatch", "barrier_k": -1.2}
])
print(f"Distilled Manifold: {distilled_atlas['manifold']} | Invariants: {len(distilled_atlas['crystallized_invariants'])}")
```

---

## 8. Operational Failure Modes & Troubleshooting

| Symptom | Probable Cause | Diagnostic Command / Telemetry | Remediation |
| :--- | :--- | :--- | :--- |
| **`NUDGE` storm (continuous loops)** | Model generating off-goal semantic paths | Check `intervention.distance > 1.5` and `intervention.kappa < 0.50` | Activate `hold_superposition`, dispatch scratchboard `NUDGE` with explicit constraint re-anchoring. |
| **`KILL` trigger** | Runaway tool loops with negative progress | Check `spend > predicted_ceiling` and `delta_rate <= 0` | Abort branch immediately; execute Phase 4 computational sleep; unwind context to last verified invariant. |
| **Metal GPU memory creep** | External tools bypassing CORDIS quarantine | Inspect `runbook.quarantine.quarantined_count` | Verify that tool streams are tagged with `is_tool_output=True` or sent to Silos 8–12. |
| **Semantic amnesia on root goal** | Phase 1 not transitioned; Tier 1 not frozen | Check `cache.blocks[0].frozen == False` | Ensure `runbook.set_phase(RunbookPhase.MID_TIER_EXECUTION)` is invoked before executing any external tools. |

---

## 9. Verification & Deterministic Reproduction

The Runbook is verified by the StrataKV automated test suite:

```bash
cd /Users/stewartbarteau/Desktop/stratakv
python3 -m unittest discover -s tests
```

Output:
```
........
----------------------------------------------------------------------
Ran 8 tests in 0.014s

OK
```
