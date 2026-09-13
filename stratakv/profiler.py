"""
Intake Coherence Profiler (Kappa) for StrataKV
==============================================
Evaluates token-stream coherence curvature kappa in (0, 1) using
goal alignment, semantic persistence, and surprisal signals.
"""

import math
from typing import Optional
import numpy as np

# Mathematical Constants
PHI = (1.0 + math.sqrt(5.0)) / 2.0         # Golden ratio: 1.6180339887...
TWISTOR_C = 1.0 / math.pi                   # Tier 3 boundary: ~0.318309886...
KAPPA_CORE = 0.75                           # Tier 1 boundary: 0.750000000...

def sigmoid(z: float) -> float:
    """Safe logistic sigmoid function clamped to avoid overflow."""
    return 1.0 / (1.0 + math.exp(-max(min(z, 20.0), -20.0)))

class KappaProfiler:
    """
    Computes coherence metric kappa = sigma(z) for incoming token representations.
    """
    def __init__(self, goal_vector: Optional[np.ndarray] = None):
        self.goal_vector = goal_vector # Optional semantic goal anchor vector

    def compute_distance(self, k: np.ndarray) -> float:
        """
        Computes hyperbolic geodesic distance d from the root goal vector.
        """
        if self.goal_vector is None or k.size == 0:
            return 0.0
        k_mean = k.mean(axis=(0, 1))
        g_norm = float(np.linalg.norm(self.goal_vector))
        k_norm = float(np.linalg.norm(k_mean))
        if g_norm < 1e-8 or k_norm < 1e-8:
            return 2.5
        cos_sim = float(np.clip(np.dot(k_mean, self.goal_vector) / (k_norm * g_norm), -1.0, 1.0))
        # Hyperbolic distance d_H = arccosh(2 - cos_sim)
        delta = max(2.0 - cos_sim, 1.0)
        return float(math.log(delta + math.sqrt(delta**2 - 1.0)))

    def profile_step(
        self,
        k: np.ndarray,
        source_tag: str,
        is_needle: bool = False,
        surprisal: Optional[float] = None
    ) -> Tuple[float, float]:
        """
        Profiles both coherence curvature kappa and hyperbolic distance d.
        Returns:
            Tuple[float, float]: (kappa, distance)
        """
        kappa = self.profile_kappa(k, source_tag, is_needle, surprisal)
        d = self.compute_distance(k)
        return kappa, d

    def profile_kappa(
        self,
        k: np.ndarray,
        source_tag: str,
        is_needle: bool = False,
        surprisal: Optional[float] = None
    ) -> float:
        """
        Profiles the instantaneous coherence curvature score kappa.
        If goal_vector is present, computes continuous vector alignment:
            cos_sim = <k_mean, g> / (|k_mean| * |g|)
            z = 3.2 * cos_sim - 1.8 * surprisal - 1.2 * var_penalty
            kappa = sigmoid(z)
        Otherwise falls back to structural priors.
        """
        # CORDIS Silo & Provenance Quarantine:
        # Silos 8-12 (Tool outputs, compiler dumps, ephemeral stdout/stderr, decoys)
        # can NEVER be promoted to Tier 1 Invariant Core, regardless of embedding cosine similarity.
        if "decoy" in source_tag:
            return 0.45  # Decoys land in Tier 2; subject to phi-pooling & dissolution leak
        elif "noise" in source_tag or "tool_flood" in source_tag or "stderr" in source_tag or "dump" in source_tag or "stack" in source_tag or "stdout" in source_tag:
            return 0.14  # Tier 3: Transient Fringe, dissolved on next exhale
        elif "speculative" in source_tag or "churn" in source_tag or "dead_end" in source_tag:
            return 0.22  # Tier 3: Transient Fringe

        # Verified Invariant Anchors (Silos 1-3: System Invariants, Root Goals, Key Checkpoints)
        if is_needle or source_tag.startswith("needle_") or "root" in source_tag or source_tag == "critical_checkpoint":
            return 0.96  # Tier 1: Invariant Core, permanent lossless preservation

        # Continuous vector alignment for agent reasoning / planning (Silos 4-7)
        if self.goal_vector is not None and k.size > 0:
            k_mean = k.mean(axis=(0, 1))
            g_norm = float(np.linalg.norm(self.goal_vector))
            k_norm = float(np.linalg.norm(k_mean))
            cos_sim = float(np.dot(k_mean, self.goal_vector) / (k_norm * g_norm)) if (g_norm > 1e-8 and k_norm > 1e-8) else 0.0
            var_feat = float(np.var(k))
            var_penalty = min(var_feat / 4.0, 1.0)
            s_val = float(surprisal) if surprisal is not None else 0.0

            z = 3.2 * cos_sim - 1.8 * s_val - 1.2 * var_penalty
            # Cap intermediate unverified reasoning in Tier 2 (harmonic basin) so it breathes
            return min(sigmoid(z), 0.72)

        # Structural prior lookup for internal agent cognition
        if "plan" in source_tag or "reasoning" in source_tag:
            return 0.68
        elif "derivation" in source_tag or "code" in source_tag:
            return 0.58
        else:
            return 0.50

    def classify_tier(self, kappa: float) -> int:
        """
        Maps a coherence curvature score kappa to its corresponding memory tier.

        Returns:
            int: 1 (Invariant Core), 2 (Harmonic Basin), 3 (Transient Fringe).
        """
        if kappa >= KAPPA_CORE:
            return 1
        elif kappa >= TWISTOR_C:
            return 2
        else:
            return 3
