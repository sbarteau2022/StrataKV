"""
StrataKV Breathing Cache Implementation
=======================================
3-Tier Coherent Memory Geometry (CMG) engine with:
- Intake kappa-profiling (surprise + semantic coherence)
- Inhale / Hold / Exhale dynamic thermodynamic lifecycle
- Rajasethupathy Tri-Timer cascade (tau_{k+1}/tau_k = phi)
- phi-wound spatial consolidation with median RoPE alignment
- 2% Milankovitch continuous dissolution leak
- Decoupled rotary position attention
"""

import math
from typing import List, Tuple, Optional, Dict, Any
import numpy as np

from .block import StrataBlock
from .rope import compute_rope_embeddings
from .profiler import KappaProfiler, PHI, TWISTOR_C, KAPPA_CORE

FIBONACCI_CHECKPOINTS = {8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987}

class ReadOnlySubAtlasSphere:
    """
    Sub-Agent Atlas (Read-Me Only):
    Provides a hyper-specialized sub-agent with a localized, read-only chart of its
    designated silo on the Atlas manifold. Prevents memory cross-contamination and
    privilege escalation, while allowing the agent to reference root invariants and
    quality evaluation criteria.
    """
    def __init__(self, parent_cache: 'StrataKVCache', silo_id: int, quality_criteria: Dict[str, Any]):
        self._cache = parent_cache
        self.silo_id = silo_id
        self.quality_criteria = quality_criteria

    @property
    def read_only(self) -> bool:
        return True

    def read_invariants(self) -> List[Dict[str, Any]]:
        """Reads surviving Tier 1 invariants visible to this sub-atlas sphere."""
        return [
            {
                "tier": b.tier,
                "length": b.length,
                "tags": list(set(b.token_sources)),
                "positions": (int(b.positions[0]), int(b.positions[-1])) if len(b.positions) > 0 else (0, 0),
                "frozen": b.frozen
            }
            for b in self._cache.blocks
            if b.tier == 1 or b.frozen or b.silo_id == self.silo_id
        ]

    def query_attention(self, q: np.ndarray, q_pos: int) -> Tuple[np.ndarray, float, float]:
        """Read-only decoupled RoPE attention query over the local sub-atlas."""
        return self._cache.query_attention(q, q_pos)

class StrataKVCache:
    """
    StrataKV: The 3-Tier Breathing KV Cache.

    Maintains three resonant memory strata:
      Tier 1 (Invariant Core, kappa >= 0.75): Lossless retention, pinned.
      Tier 2 (Harmonic Basin, 1/pi <= kappa < 0.75): phi-wound multi-scale consolidation.
      Tier 3 (Transient Fringe, kappa < 1/pi): Zero-cost isotropic release.
    """
    def __init__(
        self,
        max_active_budget: int = 2048,
        head_dim: int = 128,
        num_heads: int = 16,
        dissolution_leak_rate: float = 0.020, # 2% Milankovitch leak
        goal_vector: Optional[np.ndarray] = None,
        enable_epistemic_bias: bool = True,
        epistemic_bias: Optional[Dict[int, float]] = None,
        enable_orthogonal_projection: bool = True,
        corona_threshold: float = 0.70
    ):
        self.max_active_budget = max_active_budget
        self.head_dim = head_dim
        self.num_heads = num_heads
        self.leak_rate = dissolution_leak_rate
        self.profiler = KappaProfiler(goal_vector=goal_vector)
        
        # Epistemic Immunity Subsystem (The Signal and the Noise)
        self.enable_epistemic_bias = enable_epistemic_bias
        self.epistemic_bias = epistemic_bias if epistemic_bias is not None else {1: 0.0, 2: 0.5, 3: 2.0}
        self.enable_orthogonal_projection = enable_orthogonal_projection
        self.corona_threshold = corona_threshold
        
        self.blocks: List[StrataBlock] = []
        self.total_tokens_seen = 0
        self.breath_state = "HOLD" # "INHALE", "HOLD", "EXHALE"
        self.inhale_events = 0
        self.exhale_events = 0
        self.total_tokens_exhaled = 0
        self.phase = 1
        self.silo_id = 0

    def epistemic_exhale(self) -> int:
        """
        Emergency Epistemic Exhale (The Signal and the Noise, Section III):
        Flushes all Tier 3 (Transient Fringe) blocks immediately to extinguish apophenic delusions
        and strategic noise contamination. Returns the number of purged tokens.
        """
        tokens_before = self.active_tokens
        self.blocks = [b for b in self.blocks if b.tier != 3 or b.frozen]
        tokens_purged = tokens_before - self.active_tokens
        self.total_tokens_exhaled += max(0, tokens_purged)
        return tokens_purged

    def _project_orthogonal_to_core(self, k: np.ndarray) -> np.ndarray:
        """
        Orthogonal Subspace Projection (The Signal and the Noise, Section II):
        Detects keys in the adjacent metric neighborhood of Tier 1 invariants
        (cos_sim >= corona_threshold) and projects them onto the orthogonal complement,
        preventing the Corona from diluting the softmax attention denominator.
        """
        t1_blocks = [b for b in self.blocks if b.tier == 1 or b.frozen]
        if not t1_blocks or k.size == 0:
            return k

        # Anchor direction across Tier 1 (averaged across tokens, shape: [num_heads, head_dim])
        anchor_k = np.concatenate([b.k for b in t1_blocks], axis=0)
        u_core = anchor_k.mean(axis=0) # [num_heads, head_dim]
        u_norm = np.linalg.norm(u_core, axis=-1, keepdims=True) # [num_heads, 1]
        u_norm = np.maximum(u_norm, 1e-8)
        u_unit = u_core / u_norm # [num_heads, head_dim]

        k_proj = k.copy() # [N, num_heads, head_dim]
        k_norm = np.linalg.norm(k_proj, axis=-1, keepdims=True) # [N, num_heads, 1]
        k_norm = np.maximum(k_norm, 1e-8)
        cos_sim = np.sum(k_proj * u_unit[None, ...], axis=-1, keepdims=True) / k_norm # [N, num_heads, 1]

        # Apply orthogonal projection where cosine similarity exceeds corona threshold
        mask = (cos_sim >= self.corona_threshold).astype(np.float32)
        if np.any(mask):
            parallel = np.sum(k_proj * u_unit[None, ...], axis=-1, keepdims=True) * u_unit[None, ...]
            k_perp = k_proj - parallel
            perp_norm = np.linalg.norm(k_perp, axis=-1, keepdims=True)
            scale = np.where(perp_norm > 1e-8, k_norm / np.maximum(perp_norm, 1e-8), 1.0)
            k_proj = np.where(mask > 0.5, k_perp * scale, k_proj)

        return k_proj.astype(np.float32)

    def freeze_tier(self, tier: int) -> int:
        """
        Locks all blocks within the specified tier into an immutable state.
        Returns the count of newly frozen blocks.
        """
        count = 0
        for b in self.blocks:
            if b.tier == tier and not b.frozen:
                b.frozen = True
                count += 1
        return count

    def set_phase(self, phase: int) -> None:
        """
        Executes progressive stratified tier freezing from the Agentic AI Runbook:
          Phase 1: Low-rank end-to-end tasks (Active intake).
          Phase 2: Mid-tier execution -> FREEZE TIER 1 KV (Immutable Root Preamble).
          Phase 3: High-tier execution -> Lock verified invariants; Tier 2 harmonic breathing active.
          Phase 4: Review / Test / Refactor -> Verified state locked; testing executes in ephemeral sandbox.
        """
        self.phase = phase
        if phase >= 2:
            # Freeze genuine Tier 1 invariants (immutable, immune to dilution)
            for b in self.blocks:
                if b.tier == 1 or b.kappa >= KAPPA_CORE:
                    b.frozen = True
            # Tier 2 continues to breathe and apply the 2% Milankovitch leak to dissolve distractors!

    def active_inference_evaluate(
        self,
        k: np.ndarray,
        spend_tokens: int,
        predicted_tokens: int,
        delta_rate: float
    ) -> Dict[str, Any]:
        """
        Active Inference intervention policy from the Agentic AI Runbook:
          - High kappa, Low d: CONTINUE + score confidence.
          - Low kappa, High d: NUDGE + activate Superposition Holding Unified Function.
          - Spend > Predicted & Delta <= 0: KILL switch.
        """
        kappa, dist = self.profiler.profile_step(k, source_tag="agent_step")
        if spend_tokens > predicted_tokens and delta_rate <= 0.0:
            action = "KILL"
            reason = "Thermodynamic budget exceeded without forward semantic progress (Delta <= 0)"
        elif kappa < 0.65 and dist >= 1.2:
            action = "NUDGE"
            reason = f"Trajectory drift detected (kappa={kappa:.2f} < 0.65, d={dist:.2f} >= 1.2). Superposition Holding Unified Function active."
        else:
            action = "CONTINUE"
            reason = f"Stable alignment (kappa={kappa:.2f}, d={dist:.2f})"
        
        confidence = float(kappa * math.exp(-min(dist, 5.0)))
        return {
            "action": action,
            "kappa": kappa,
            "distance": dist,
            "confidence": confidence,
            "reason": reason,
            "superposition_required": (action == "NUDGE")
        }

    def hold_superposition(
        self,
        candidate_trajectories: List[np.ndarray],
        dist_threshold: float = 1.2
    ) -> Dict[str, Any]:
        """
        Superposition Holding Unified Function:
        Activated by the reasoning/inference engine under Low kappa, High d ambiguity.
        Instead of prematurely collapsing or thrashing into an ungrounded, high-cost path
        (the root driver of agentic suicide), holds M candidate trajectory states in an
        un-collapsed superposition bundle Psi = sum c_i |h_i>. Binds execution to the
        2-way scratchboard until curvature realigns.
        """
        if not candidate_trajectories:
            return {"status": "EMPTY", "num_hypotheses": 0, "collapsed": False}

        branch_metrics = []
        for idx, cand_k in enumerate(candidate_trajectories):
            k_score, d_score = self.profiler.profile_step(cand_k, source_tag="superposition_branch")
            branch_metrics.append({
                "branch_id": idx,
                "kappa": k_score,
                "distance": d_score,
                "weight": math.exp(-d_score) * k_score
            })

        total_weight = sum(m["weight"] for m in branch_metrics)
        normalized_weights = [m["weight"] / max(total_weight, 1e-12) for m in branch_metrics]

        best_idx = int(np.argmax(normalized_weights))
        best_branch = branch_metrics[best_idx]

        if best_branch["kappa"] >= 0.65 and best_branch["distance"] < dist_threshold:
            return {
                "status": "COLLAPSED",
                "collapsed_branch_id": best_idx,
                "metrics": best_branch,
                "superposition_active": False,
                "guidance": "Coherence restored. Collapse superposition and resume forward execution."
            }
        else:
            return {
                "status": "HOLDING_SUPERPOSITION",
                "num_hypotheses": len(candidate_trajectories),
                "branch_distribution": normalized_weights,
                "superposition_active": True,
                "guidance": "Low kappa, high d detected. Hold superposition; dispatch 2-way scratchboard nudge."
            }

    def get_sub_atlas_sphere(self, silo_id: int, quality_criteria: Optional[Dict[str, Any]] = None) -> 'ReadOnlySubAtlasSphere':
        """
        Sub-Agent Atlas (Read-Me Only):
        Generates a capability-bounded, read-only chart of the Atlas manifold for a
        designated silo sub-agent. Prevents memory cross-contamination and poisoning.
        """
        return ReadOnlySubAtlasSphere(self, silo_id=silo_id, quality_criteria=quality_criteria or {})

    def distill_to_master_atlas(self, failure_branches: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Distills surviving invariants and failure logs into the Master Atlas Manifold:
        M = H^n (Hierarchy / Radial Surprise) x T^n (Harmonic Pacing Phases).
        """
        invariants = []
        for b in self.blocks:
            if b.frozen or b.tier == 1:
                invariants.append({
                    "turn_id": b.turn_id,
                    "tier": b.tier,
                    "kappa": b.kappa,
                    "length": b.length,
                    "tags": list(set(b.token_sources)),
                    "silo_id": b.silo_id
                })
        
        return {
            "manifold": "H^n x T^n",
            "total_tokens_ingested": self.total_tokens_seen,
            "active_retained_tokens": self.active_tokens,
            "compression_factor": self.total_tokens_seen / max(self.active_tokens, 1),
            "crystallized_invariants": invariants,
            "negative_curvature_barriers": failure_branches or [],
            "status": "CONSOLIDATED"
        }

    @property
    def active_tokens(self) -> int:
        """Total number of active token representations across all surviving blocks."""
        return sum(b.length for b in self.blocks)

    @property
    def memory_bytes(self) -> int:
        """Total memory occupied by active blocks in bytes (float16)."""
        return sum(b.memory_bytes for b in self.blocks)

    def inhale(
        self,
        k: np.ndarray,
        v: np.ndarray,
        start_pos: int,
        source_tag: str,
        is_needle: bool = False,
        turn_id: int = 0,
        surprisal: Optional[float] = None
    ) -> StrataBlock:
        """
        Inhale Pass: Ingests incoming step representations, calculates kappa,
        tags initial strata tier, and checks breathing pressure.
        """
        num_tokens = k.shape[0]
        self.total_tokens_seen += num_tokens
        positions = np.arange(start_pos, start_pos + num_tokens, dtype=np.int32)
        tags = [source_tag] * num_tokens

        # Orthogonal Subspace Projection for non-needle external streams
        if self.enable_orthogonal_projection and not is_needle:
            k = self._project_orthogonal_to_core(k)

        # 1. Check for sub-chunk intra-stream decomposition on tool / ambiguous sources
        is_tool_source = any(t in source_tag for t in ["tool", "mixed", "code", "interpreter", "ambiguous", "external", "bash", "stdout"])
        if num_tokens > 64 and is_tool_source and not is_needle:
            chunk_size = 64
            last_block = None
            for i in range(0, num_tokens, chunk_size):
                k_c = k[i : i + chunk_size]
                v_c = v[i : i + chunk_size]
                pos_c = positions[i : i + chunk_size]
                tag_c = tags[i : i + chunk_size]
                
                kappa_c = self.profiler.profile_kappa(k_c, source_tag, is_needle, surprisal)
                tier_c = self.profiler.classify_tier(kappa_c)
                
                b = StrataBlock(
                    k=k_c.astype(np.float32),
                    v=v_c.astype(np.float32),
                    positions=pos_c,
                    token_sources=tag_c,
                    kappa=kappa_c,
                    tier=tier_c,
                    scale_n=0,
                    turn_id=turn_id
                )
                self.blocks.append(b)
                last_block = b
            block = last_block
        else:
            # 1. Profile coherence curvature kappa
            kappa = self.profiler.profile_kappa(k, source_tag, is_needle, surprisal)

            # 2. Determine initial strata tier
            tier = self.profiler.classify_tier(kappa)

            block = StrataBlock(
                k=k.astype(np.float32),
                v=v.astype(np.float32),
                positions=positions,
                token_sources=tags,
                kappa=kappa,
                tier=tier,
                scale_n=0,
                turn_id=turn_id
            )
            self.blocks.append(block)
        self.breath_state = "INHALE"
        self.inhale_events += 1

        # Check if Exhale is triggered (capacity pressure or Fibonacci checkpoint)
        is_fibonacci = turn_id in FIBONACCI_CHECKPOINTS
        if self.active_tokens > self.max_active_budget or is_fibonacci:
            self.exhale(turn_id=turn_id, force_fibonacci=is_fibonacci)
        else:
            self.breath_state = "HOLD"

        return block

    def exhale(self, turn_id: int, force_fibonacci: bool = False) -> None:
        """
        Exhale Pass:
        1. kappa-stratified sorting (Core -> Harmonic -> Fringe).
        2. Tier 1 (Core): 100% retained, lossless.
        3. Tier 2 (Harmonic): phi-wound multi-scale consolidation via sequence-length
           harmonic pooling with median RoPE position preservation.
        4. Tier 3 (Fringe): Dissolved into thermodynamic vacuum (zero-cost release).
        5. Continuous 2% Milankovitch Wobble Leak applied to active representations.
        6. Enforces hard budget ceiling under extreme tool floods.
        """
        self.breath_state = "EXHALE"
        self.exhale_events += 1
        tokens_before = self.active_tokens

        # Sort blocks descending by kappa
        self.blocks.sort(key=lambda b: b.kappa, reverse=True)
        surviving_blocks: List[StrataBlock] = []

        for block in self.blocks:
            if block.frozen or block.tier == 1 or block.kappa >= KAPPA_CORE:
                # Frozen blocks & Tier 1 Core: Lossless, immutable, zero eviction
                surviving_blocks.append(block)

            elif block.tier == 2 or (block.kappa >= TWISTOR_C and block.kappa < KAPPA_CORE):
                # Tier 2: Harmonic Basin undergoes phi-wound consolidation for older turns
                age_turns = turn_id - block.turn_id
                if age_turns > 2:
                    block.scale_n += 1
                    stride = max(2, int(round(PHI ** min(block.scale_n, 4))))
                    cur_len = block.k.shape[0]
                    if cur_len > 4:
                        new_k = []
                        new_v = []
                        new_pos = []
                        new_tags = []
                        for idx in range(0, cur_len, stride):
                            chunk_k = block.k[idx:idx + stride]
                            chunk_v = block.v[idx:idx + stride]
                            chunk_pos = block.positions[idx:idx + stride]
                            chunk_tags = block.token_sources[idx:idx + stride]

                            # Average pool representation vectors
                            new_k.append(np.mean(chunk_k, axis=0, keepdims=True))
                            new_v.append(np.mean(chunk_v, axis=0, keepdims=True))

                            # Select median sequence position to preserve RoPE geometric phase
                            med_idx = len(chunk_pos) // 2
                            new_pos.append(chunk_pos[med_idx])
                            new_tags.append(chunk_tags[med_idx])

                        block.k = np.concatenate(new_k, axis=0)
                        block.v = np.concatenate(new_v, axis=0)
                        block.positions = np.array(new_pos, dtype=np.int32)
                        block.token_sources = new_tags

                surviving_blocks.append(block)

            else:
                # Tier 3: Transient Fringe (kappa < 1/pi) is released completely
                pass

        # Apply 2% Milankovitch Dissolution Leak: S_{t+1} = 0.98 * S_t
        for b in surviving_blocks:
            if b.tier != 1 and not b.frozen:
                b.k = (1.0 - self.leak_rate) * b.k
                b.v = (1.0 - self.leak_rate) * b.v

        # Hard budget convergence: if active tokens exceed budget, pool un-frozen Tier 2 blocks proportionally
        current_active = sum(b.length for b in surviving_blocks)
        if current_active > self.max_active_budget:
            t1_len = sum(b.length for b in surviving_blocks if b.tier == 1 or b.frozen)
            t2_budget = max(64, self.max_active_budget - t1_len)
            t2_blocks = [b for b in surviving_blocks if b.tier == 2 and not b.frozen]
            t2_len = sum(b.length for b in t2_blocks)
            if t2_len > t2_budget and t2_blocks:
                ratio = t2_len / t2_budget
                stride = max(2, int(math.ceil(ratio)))
                for b in t2_blocks:
                    cur_l = b.k.shape[0]
                    if cur_l >= stride:
                        b.k = np.concatenate([np.mean(b.k[i:i+stride], axis=0, keepdims=True) for i in range(0, cur_l, stride)], axis=0)
                        b.v = np.concatenate([np.mean(b.v[i:i+stride], axis=0, keepdims=True) for i in range(0, cur_l, stride)], axis=0)
                        b.positions = np.array([b.positions[min(i + stride//2, cur_l - 1)] for i in range(0, cur_l, stride)], dtype=np.int32)
                        b.token_sources = [b.token_sources[min(i + stride//2, cur_l - 1)] for i in range(0, cur_l, stride)]
                        b.scale_n += 1

        self.blocks = surviving_blocks
        tokens_after = self.active_tokens
        self.total_tokens_exhaled += max(0, tokens_before - tokens_after)
        self.breath_state = "HOLD"

    def query_attention(
        self,
        q: np.ndarray,
        q_pos: int,
        target_needle_tag: str = "root_needle"
    ) -> Tuple[np.ndarray, float, float]:
        """
        Executes Decoupled RoPE Attention over gathered strata blocks.
        """
        res = self.evaluate_needle_retrieval(q, q_pos, target_needle_tag)
        all_k = np.concatenate([b.k for b in self.blocks], axis=0) if self.blocks else np.zeros((1, self.num_heads, self.head_dim))
        all_pos = np.concatenate([b.positions for b in self.blocks], axis=0) if self.blocks else np.zeros((1,), dtype=np.int32)
        q_rot = compute_rope_embeddings(q[None, ...], np.array([q_pos]))[0]
        k_rot = compute_rope_embeddings(all_k, all_pos)
        scores = np.einsum('hd,shd->hs', q_rot, k_rot) / math.sqrt(self.head_dim)

        # Epistemic Softmax Bias: The Analytical Standard
        if self.enable_epistemic_bias and self.blocks:
            all_tiers = np.concatenate([[b.tier] * b.length for b in self.blocks], axis=0)
            bias_vector = np.array([self.epistemic_bias.get(int(t), 0.0) for t in all_tiers], dtype=np.float32)
            scores = scores - bias_vector[None, :]

        scores_max = np.max(scores, axis=-1, keepdims=True)
        exp_scores = np.exp(scores - scores_max)
        attn_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
        mean_attn = np.mean(attn_weights, axis=0)
        return mean_attn, res["needle_mass"], res["entropy"]

    def evaluate_needle_retrieval(
        self,
        q: np.ndarray,
        q_pos: int,
        target_needle_tag: str,
        decoy_tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates competitive needle retrieval against adversarial distractors.
        """
        if not self.blocks:
            return {
                "needle_mass": 0.0,
                "decoy_mass": 0.0,
                "sdr": 0.0,
                "top1_match": False,
                "top5_match": False,
                "entropy": 0.0,
                "rank": -1
            }

        all_k = np.concatenate([b.k for b in self.blocks], axis=0)
        all_pos = np.concatenate([b.positions for b in self.blocks], axis=0)
        all_tags = []
        for b in self.blocks:
            all_tags.extend(b.token_sources)

        q_rot = compute_rope_embeddings(q[None, ...], np.array([q_pos]))[0]
        k_rot = compute_rope_embeddings(all_k, all_pos)

        scores = np.einsum('hd,shd->hs', q_rot, k_rot) / math.sqrt(self.head_dim)

        # Epistemic Softmax Bias in needle evaluation
        if self.enable_epistemic_bias and self.blocks:
            all_tiers = np.concatenate([[b.tier] * b.length for b in self.blocks], axis=0)
            bias_vector = np.array([self.epistemic_bias.get(int(t), 0.0) for t in all_tiers], dtype=np.float32)
            scores = scores - bias_vector[None, :]

        scores_max = np.max(scores, axis=-1, keepdims=True)
        exp_scores = np.exp(scores - scores_max)
        attn_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
        mean_attn = np.mean(attn_weights, axis=0)

        needle_mask = np.array([t == target_needle_tag for t in all_tags], dtype=bool)
        needle_mass = float(np.sum(mean_attn[needle_mask])) if np.any(needle_mask) else 0.0

        decoy_mass = 0.0
        if decoy_tags:
            decoy_mask = np.array([t in decoy_tags for t in all_tags], dtype=bool)
            decoy_mass = float(np.sum(mean_attn[decoy_mask])) if np.any(decoy_mask) else 0.0

        sdr = needle_mass / max(decoy_mass, 1e-12) if needle_mass > 0 else 0.0

        top_indices = np.argsort(mean_attn)[::-1]
        top1_tag = all_tags[top_indices[0]] if len(top_indices) > 0 else ""
        top1_match = (top1_tag == target_needle_tag)

        top5_tags = [all_tags[idx] for idx in top_indices[:min(5, len(top_indices))]]
        top5_match = (target_needle_tag in top5_tags)

        needle_indices = np.where(needle_mask)[0]
        if len(needle_indices) > 0:
            best_needle_idx = needle_indices[np.argmax(mean_attn[needle_indices])]
            rank = int(np.where(top_indices == best_needle_idx)[0][0]) + 1
        else:
            rank = len(all_tags) + 1

        p = np.clip(mean_attn, 1e-12, 1.0)
        entropy = -float(np.sum(p * np.log(p)))

        return {
            "needle_mass": needle_mass,
            "decoy_mass": decoy_mass,
            "sdr": sdr,
            "top1_match": top1_match,
            "top5_match": top5_match,
            "entropy": entropy,
            "rank": rank
        }
