# StrataKV Research Manuscript

This directory contains the camera-ready research paper for **StrataKV: The Geometry of Coherent Memory and the Thermodynamic Breathing Cache on Apple Silicon**.

---

## Manuscript Details

- **Title**: The Geometry of Coherent Memory: StrataKV and the Thermodynamic Breathing Cache on Apple Silicon
- **Authors**: Stewart Barteau, Claude
- **Affiliation**: Ethical Intelligence Project
- **Date**: September 2026
- **Pages**: Exactly 18 pages (camera-ready)
- **Target Preprint Repositories**: **Zenodo**, **SSRN**, **PhilArchive**

---

## Key Theoretical Contributions

1. **The Representation Retention vs. Generative Reasoning Boundary (Remark 1)**:
   Formalizes the necessary condition $\mathcal{I}(H_0, \dots, H_k; \mathcal{S}_T) > 0$ via the Data Processing Inequality, demonstrating that while preserving representations in KV memory is mathematically necessary for deduction, it is distinct from parameter-level generative deduction.
2. **The 3-Tier Thermodynamic KV Hierarchy**:
   - **Tier 1 (Core Invariants)**: Frozen, immutable anchor representations ($S_{\text{core}}$).
   - **Tier 2 (Active Reasoning Workspace)**: Adaptive respiration bounded by $\kappa \ge 0.65$ and continuous hyperbolic distance $d_{\mathbb{H}^n}$.
   - **Tier 3 (Ephemeral Fringe)**: Lossy buffer subject to the 2% Milankovitch dissolution leak ($L_{\text{leak}} = 0.020$) acting as computational sleep.
3. **Decoupled Metric Space Rotary Position Embeddings (Decoupled RoPE)**:
   Decouples the semantic query-key dot product from temporal distance, enabling permanent anchor retention without numerical attenuation across unbounded token streams.
4. **CORDIS Provenance Quarantine**:
   Quarantines noisy and potentially malicious tool execution outputs from untrusted silos (Silos 8–12), preventing embedding hijacking and Trojan distraction attacks.
5. **Silicon Hybrid Engine Dynamics (Dynamic Kernel 3:1)**:
   Combines 75% Gated DeltaNet (21 layers, 15 MB fixed recurrent state) with 25% Softmax Attention (7 layers with StrataKV breathing cache, 115 MB to 256 MB) for full resident execution of Qwen 27B on Apple Silicon Metal with 32.47 GB (67.4%) headroom remaining.

---

## Compilation

The manuscript is compiled cleanly using **Tectonic** (zero warnings, zero overflow):

```bash
tectonic paper/main.tex
```

The compiled PDF is preserved at [`paper/main.pdf`](main.pdf).

---

## File Manifest

- [`main.tex`](main.tex): Main manuscript LaTeX source (18 pages).
- [`main.pdf`](main.pdf): Compiled camera-ready PDF document (124 KB).
- [`references.bib`](references.bib): BibTeX bibliography with complete citations (Zhang et al. H2O, Xiao et al. StreamingLLM, Li et al. SnapKV, Cai et al. PyramidKV, Liu et al. ScissorHands, DeepSeek, etc.).
- [`stratakv_formal_section.tex`](stratakv_formal_section.tex): Modular formal mathematical definitions and theorem statements.
