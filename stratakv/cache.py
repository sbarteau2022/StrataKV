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

FIBONACCI_CHECKPOINTS = {8, 13, 21, 34, 55, 89, 144}

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
        goal_vector: Optional[np.ndarray] = None
    ):
        self.max_active_budget = max_active_budget
        self.head_dim = head_dim
        self.num_heads = num_heads
        self.leak_rate = dissolution_leak_rate
        self.profiler = KappaProfiler(goal_vector=goal_vector)
        
        self.blocks: List[StrataBlock] = []
        self.total_tokens_seen = 0
        self.breath_state = "HOLD" # "INHALE", "HOLD", "EXHALE"
        self.inhale_events = 0
        self.exhale_events = 0
        self.total_tokens_exhaled = 0

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
        """
        self.breath_state = "EXHALE"
        self.exhale_events += 1
        tokens_before = self.active_tokens

        # Sort blocks descending by kappa
        self.blocks.sort(key=lambda b: b.kappa, reverse=True)
        surviving_blocks: List[StrataBlock] = []

        for block in self.blocks:
            if block.tier == 1 or block.kappa >= KAPPA_CORE:
                # Tier 1: Invariant Core is NEVER evicted or compressed
                surviving_blocks.append(block)

            elif block.tier == 2 or (block.kappa >= TWISTOR_C and block.kappa < KAPPA_CORE):
                # Tier 2: Harmonic Basin undergoes phi-wound consolidation for older turns
                age_turns = turn_id - block.turn_id
                if age_turns > 2:
                    block.scale_n += 1
                    # Stride scales with phi^scale_n
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

                            # Crucial: Select median sequence position to preserve RoPE geometric phase
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

        # Apply 2% Milankovitch Dissolution Leak: S_{t+1} = 0.98 * S_t + 0.02 * S_prior
        # In latent representations, this continuously relaxes non-core components toward zero
        for b in surviving_blocks:
            if b.tier != 1:
                b.k = (1.0 - self.leak_rate) * b.k
                b.v = (1.0 - self.leak_rate) * b.v

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

        Args:
            q (np.ndarray): Query vector of shape [num_heads, head_dim].
            q_pos (int): Query sequence position.
            target_needle_tag (str): Origin tag of invariant needle to track.

        Returns:
            Tuple[np.ndarray, float, float]:
                - Mean attention distribution across active tokens [total_active].
                - Attention mass focused on invariant needle tokens.
                - Attention entropy in nats.
        """
        if not self.blocks:
            return np.zeros((1,)), 0.0, 0.0

        all_k = np.concatenate([b.k for b in self.blocks], axis=0)
        all_pos = np.concatenate([b.positions for b in self.blocks], axis=0)
        all_tags = []
        for b in self.blocks:
            all_tags.extend(b.token_sources)

        # Apply explicit non-contiguous Rotary Position Embeddings
        q_rot = compute_rope_embeddings(q[None, ...], np.array([q_pos]))[0] # [num_heads, head_dim]
        k_rot = compute_rope_embeddings(all_k, all_pos)                      # [total_active, num_heads, head_dim]

        # Scaled dot-product attention
        scores = np.einsum('hd,shd->hs', q_rot, k_rot) / math.sqrt(self.head_dim)
        scores_max = np.max(scores, axis=-1, keepdims=True)
        exp_scores = np.exp(scores - scores_max)
        attn_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)

        mean_attn = np.mean(attn_weights, axis=0) # Average over attention heads

        # Compute invariant needle attention mass
        needle_mask = np.array([t == target_needle_tag for t in all_tags], dtype=bool)
        needle_mass = float(np.sum(mean_attn[needle_mask])) if np.any(needle_mask) else 0.0

        # Compute attention entropy H(alpha) = - sum alpha * ln(alpha)
        p = np.clip(mean_attn, 1e-12, 1.0)
        entropy = -float(np.sum(p * np.log(p)))

        return mean_attn, needle_mass, entropy
