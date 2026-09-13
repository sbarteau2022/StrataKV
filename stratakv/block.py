"""
StrataKV Block Data Structure
=============================
Represents a cohesive geometric stratum block within the Breathing KV Cache.
"""

from dataclasses import dataclass
from typing import List, Optional, Any
import numpy as np

@dataclass
class StrataBlock:
    """
    A discrete memory block residing within a StrataKV memory tier.

    Attributes:
        k (np.ndarray): Key tensor of shape [block_len, num_heads, head_dim].
        v (np.ndarray): Value tensor of shape [block_len, num_heads, head_dim].
        positions (np.ndarray): Original immutable 1D RoPE sequence indices [block_len].
        token_sources (List[str]): Semantic lineage tags for each token in the block.
        kappa (float): Coherence curvature score in (0, 1).
        tier (int): Strata tier: 1 (Invariant Core), 2 (Harmonic Basin), 3 (Transient Fringe).
        scale_n (int): Number of phi-wound pooling operations undergone.
        turn_id (int): Conversation turn at which this block was inhaled.
    """
    k: np.ndarray
    v: np.ndarray
    positions: np.ndarray
    token_sources: List[str]
    kappa: float
    tier: int
    scale_n: int = 0
    turn_id: int = 0

    @property
    def length(self) -> int:
        """Returns the number of active token representations in this block."""
        return self.k.shape[0]

    @property
    def memory_bytes(self) -> int:
        """Returns the total memory footprint of the KV representations in bytes (assuming float16)."""
        return (self.k.size + self.v.size) * 2
