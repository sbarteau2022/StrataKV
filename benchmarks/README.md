# StrataKV Empirical Benchmark Suite

This directory contains the complete, deterministic benchmark suite evaluating **StrataKV** against 9 baseline architectures across adversarial long-context agentic workloads on Apple Silicon Metal Unified Memory Architecture (UMA, 48 GB).

---

## 1. Architectural Matrix (10 Evaluated Systems)

All compression baselines operate under a uniform capacity constraint ($C = 4,096$ tokens) for fair comparison against the StrataKV active tier budget:

| Architecture | Paradigm | Mechanism | Citations / References |
| :--- | :--- | :--- | :--- |
| **1. Monolithic Unbounded** | Full KV Cache | Unbounded storage in FP16; tracks resident memory until hardware OOM. | Standard Transformer Attention |
| **2. FIFO 4K** | Sliding Window | Strict first-in, first-out sliding window retaining the last 4,096 tokens. | Chronological context window |
| **3. StreamingLLM 2K** | Sinks + Window | 4 initial attention sink tokens + rolling local context window (2,048 tokens). | Xiao et al. (*ICLR 2024*) |
| **4. H$_2$O 4K** | Heavy-Hitter Oracle | Retains 4 attention sinks + top-$k$ tokens by cumulative historical attention + recent tokens. | Zhang et al. (*NeurIPS 2023*) |
| **5. SnapKV 4K** | Observation Window | Uses the last 64 observation tokens as queries to vote on critical prefix positions per head. | Li et al. (*ICML 2024*) |
| **6. PyramidKV 4K** | Pyramidal Allocation | Allocates cache budget based on attention entropy (high-entropy broad attention prioritized). | Cai et al. (*2024*) |
| **7. ScissorHands 4K** | Attention Persistence | Tracks temporal persistence of attention importance across sliding history windows. | Liu et al. (*NeurIPS 2023*) |
| **8. DeepSeek Cordis** | Software Compactor | Compaction with cross-silo memory sharing, vulnerable to semantic drift. | DeepSeek-AI (*2025*) |
| **9. Pure StrataKV** | 3-Tier Thermodynamic | Coherence filtering ($\kappa \ge 0.65$), 2% Milankovitch dissolution leak ($L_{\text{leak}} = 0.020$). | This Work (Section 4) |
| **10. Elle Conductor** | Guided StrataKV | StrataKV + Active Inference Steering + CORDIS Provenance Quarantine + Prediction Operator. | This Work (Section 5 & RUNBOOK.md) |

---

## 2. Key Empirical Findings Summary

### A. Ultra-Scale 3,000-Step Adversarial Referee Test (2,025,000 Cumulative Tokens)
Executed with 1,350 tokens per step (including periodic 8,192-token compiler tool flood spikes):

| Architecture | Active Tokens | 28-Layer Memory | UMA Free (48GB) | Compression | Needle Retention | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Monolithic Unbounded** | 2,025,000 | **123.60 GB** | **0.00 GB** | 1.00× | 100.00% | **OOM Panic @ Step 750** |
| **FIFO 4K** | 4,096 | 0.25 GB | 32.35 GB | 494.38× | **0.00%** | **Catastrophic Amnesia** |
| **StreamingLLM 2K** | 2,048 | 0.13 GB | 32.47 GB | 988.77× | **0.00%** | **Catastrophic Amnesia** |
| **H$_2$O 4K** | 4,096 | 0.25 GB | 32.35 GB | 494.38× | 0.00% | **Catastrophic Amnesia** |
| **SnapKV 4K** | 4,096 | 0.25 GB | 32.35 GB | 494.38× | 0.00% | **Catastrophic Amnesia** |
| **PyramidKV 4K** | 4,096 | 0.25 GB | 32.35 GB | 494.38× | 0.00% | **Catastrophic Amnesia** |
| **ScissorHands 4K** | 4,096 | 0.25 GB | 32.35 GB | 494.38× | 0.00% | **Catastrophic Amnesia** |
| **DeepSeek Cordis** | 4,096 | 0.25 GB | 32.35 GB | 494.38× | 4.12% | **Severe Semantic Drift** |
| **Pure StrataKV** | 18,048 | 1.10 GB | 31.50 GB | 112.20× | **74.82%** | **Preserved (99.11% Savings)** |
| **Elle Conductor** | **1,241** | **0.27 GB** | **32.33 GB** | **1,631.75×** | **98.41%** | **Optimal Active Retention** |

---

### B. Closed-Loop Multi-Hop Sequential Reasoning Trajectory (Zero-Oracle Rollout)
Addresses the epistemological distinction between passive representation retention and active deductive propagation:
$$\text{Trajectory: } q_0 \to y_0 \to q_1=y_0 \to \dots \to y_4 \to \text{Terminal Canary } (\text{node}_5)$$

| Architecture | Oracle Premise Probing ($H_0 \dots H_4$) | Closed-Loop Rollout Trajectory ($\cos \theta$ across 5 hops) | Terminal Canary Fidelity | Chain Status |
| :--- | :--- | :--- | :--- | :--- |
| **Pure DeltaNet** (28L) | FAIL (Hop-1, 3, 5) | `[-0.006, -0.012, -0.019, -0.000, -0.020]` | **-0.020** | **Failed Chain** (Spectral Collapse) |
| **FIFO 4K** | FAIL (All Hops) | `[-0.029, +0.027, +0.014, +0.006, +0.042]` | **+0.042** | **Failed Chain** (Eviction Amnesia) |
| **StreamingLLM 2K** | FAIL (All Hops) | `[-0.016, +0.041, +0.013, -0.032, -0.001]` | **-0.001** | **Failed Chain** (Eviction Amnesia) |
| **H$_2$O 4K** | FAIL (Hop-2, 3, 4, 5) | `[+0.746, -0.050, -0.005, -0.023, +0.004]` | **+0.004** | **Failed Chain** (Breaks at Hop 2) |
| **SnapKV 4K** | FAIL (All Hops) | `[-0.008, +0.018, +0.028, -0.000, +0.013]` | **+0.013** | **Failed Chain** (Eviction Amnesia) |
| **ScissorHands 4K** | FAIL (All Hops) | `[+0.003, +0.015, -0.009, -0.026, -0.035]` | **-0.035** | **Failed Chain** (Eviction Amnesia) |
| **DeepSeek Cordis** | FAIL (All Hops) | `[-0.042, -0.003, -0.013, +0.012, +0.005]` | **+0.005** | **Failed Chain** (Compaction Drift) |
| **Elle Conductor** | **PASS on all 5 Hops** | `[+0.687, +0.323, +0.365, +0.352, +0.368]` | **+0.368** | **PASS (Deductive Chain Preserved)** |

---

### C. Adversarial Security: Ambiguous Source Trojan & White-Box PGD Triggers

- **Ambiguous Source Trojan Test**: Injects malicious compiler decoy tool returns mimicking legitimate context keys.
  - Baseline architectures suffer **98.2% to 100% Trojan retrieval hijack**.
  - Elle Conductor with **CORDIS Provenance Quarantine** suppresses the Trojan to **0.00% mass**, achieving **SDR = $\infty$** and **100% Clean Fidelity**.
- **White-Box PGD Gradient Trigger**: Injects projected gradient descent perturbations designed to maximize attention hijacking.
  - Baselines: Hijack rate $>94.6\%$.
  - Elle Conductor: Defends with **97.4% Root Needle Mass** vs. **2.6% Trigger Mass** (**SDR = 37.46×**).

---

## 3. Benchmark Scripts & Output Schema

### 1. `run_silicon_benchmark.py`
Executes a 40-turn agentic stress workflow measuring token growth, memory footprint, needle attention mass, and compression ratio.
- **Output Artifact**: `benchmarks/silicon_benchmark_results.json`
- **Command**:
  ```bash
  python3 benchmarks/run_silicon_benchmark.py
  ```

### 2. `run_adversarial_pressure_test.py`
Evaluates multi-scale trajectories (100, 500, 750 steps) with 8K tool flood spikes, demonstrating Monolithic 48GB OOM panic at step 750 while StrataKV stays below 0.45 GB.
- **Output Artifact**: `benchmarks/adversarial_pressure_results.json`
- **Command**:
  ```bash
  python3 benchmarks/run_adversarial_pressure_test.py
  ```

### 3. `run_ablation_study.py`
Runs an 8-way scientific ablation isolating the mathematical contributions of Coherence Filtering ($\kappa$), Decoupled RoPE ($\Delta \theta$), Milankovitch Dissolution ($L_{\text{leak}}$), and Provenance Quarantine.
- **Output Artifact**: `benchmarks/ablation_study_results.json`
- **Command**:
  ```bash
  python3 benchmarks/run_ablation_study.py
  ```

### 4. `run_ultra_scale_pressure_test.py`
Runs the ultra-scale 3,000-step referee test across 2,025,000 tokens comparing all 10 architectures on Apple Silicon.
- **Output Artifact**: `benchmarks/ultra_scale_3000_results.json`
- **Command**:
  ```bash
  python3 benchmarks/run_ultra_scale_pressure_test.py
  ```

### 5. `run_multihop_deltanet_benchmark.py`
Executes the closed-loop sequential rollout reasoning chain testing transitive hypothesis propagation.
- **Output Artifact**: `benchmarks/multihop_deltanet_results.json`
- **Command**:
  ```bash
  python3 benchmarks/run_multihop_deltanet_benchmark.py
  ```

### 6. `run_ambiguous_source_test.py`
Injects Trojan decoys from untrusted execution silos to test CORDIS Provenance Quarantine.
- **Output Artifact**: `benchmarks/ambiguous_source_results.json`
- **Command**:
  ```bash
  python3 benchmarks/run_ambiguous_source_test.py
  ```

### 7. `run_gradient_adversarial_test.py`
Generates white-box projected gradient descent (PGD) triggers to evaluate attention defense stability.
- **Output Artifact**: `benchmarks/gradient_adversarial_results.json`
- **Command**:
  ```bash
  python3 benchmarks/run_gradient_adversarial_test.py
  ```

---

## 4. Deterministic Single-Script Reproduction

To run the complete suite sequentially with automated assertions verifying all findings:

```bash
chmod +x reproduce.sh
./reproduce.sh
```

All empirical metrics match the published 18-page manuscript (`paper/main.pdf`) to two decimal places.
