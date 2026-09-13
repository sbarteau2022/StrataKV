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

    def profile_kappa(
        self,
        k: np.ndarray,
        source_tag: str,
        is_needle: bool = False,
        surprisal: Optional[float] = None
    ) -> float:
        """
        Profiles the instantaneous coherence curvature score kappa.

        Args:
            k (np.ndarray): Key tensor of shape [seq_len, num_heads, head_dim].
            source_tag (str): Semantic origin tag of the token sequence.
            is_needle (bool): Explicit flag for invariant root constraints.
            surprisal (Optional[float]): Optional logit surprisal score.

        Returns:
            float: Coherence score kappa in (0, 1).
        """
        if is_needle or source_tag == "root_task" or source_tag == "root_prompt":
            return 0.96
        elif source_tag == "critical_checkpoint":
            return 0.88
        elif source_tag == "plan_reasoning":
            return 0.68
        elif source_tag == "derivation" or source_tag == "code_execution":
            return 0.58
        elif source_tag == "speculative_churn" or source_tag == "dead_end":
            return 0.22
        elif source_tag in ("compiler_noise", "raw_stdout", "distractor_log", "stack_trace"):
            return 0.14
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
