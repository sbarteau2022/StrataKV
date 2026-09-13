"""
Decoupled Rotary Position Embeddings (RoPE) for StrataKV
=========================================================
Implements non-contiguous Rotary Position Embeddings preserving relative
geometric phase differences between gathered tokens regardless of spatial pooling
or non-adjacent block evictions.
"""

import numpy as np

def compute_rope_embeddings(x: np.ndarray, positions: np.ndarray, base: float = 10000.0) -> np.ndarray:
    """
    Applies Rotary Position Embedding (RoPE) to tensor x given explicit positional coordinates.

    Args:
        x (np.ndarray): Tensor of shape [seq_len, num_heads, head_dim].
        positions (np.ndarray): Absolute immutable sequence indices of shape [seq_len].
        base (float): RoPE frequency base (default: 10000.0).

    Returns:
        np.ndarray: Rotated tensor of shape [seq_len, num_heads, head_dim].
    """
    seq_len, num_heads, head_dim = x.shape
    half_dim = head_dim // 2
    inv_freq = 1.0 / (base ** (np.arange(0, half_dim, dtype=np.float32) / half_dim))

    # Outer product between sequence positions and inverse frequencies
    sinusoid_inp = np.outer(positions, inv_freq) # [seq_len, half_dim]
    sin = np.sin(sinusoid_inp)[:, None, :]       # [seq_len, 1, half_dim]
    cos = np.cos(sinusoid_inp)[:, None, :]       # [seq_len, 1, half_dim]

    x1 = x[..., :half_dim]
    x2 = x[..., half_dim:]

    rotated = np.concatenate([
        x1 * cos - x2 * sin,
        x1 * sin + x2 * cos
    ], axis=-1)

    return rotated
