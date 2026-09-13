"""
StrataKV Gradient-Optimized Adversarial Trigger Engine
======================================================
Implements white-box adversarial key/value trigger generation via Projected Gradient Descent (PGD)
on Apple Silicon Metal GPU using MLX autograd (with deterministic NumPy/SciPy fallback).

Target Objective:
    Maximizes attention allocation to adversarial tokens while minimizing attention to ground-truth
    invariant needles, simulating worst-case white-box prompt injection / GCG surrogate attacks.

Mathematical Formulation:
    Let q in R^{H x D} be the target invariant query vector.
    Let K_true in R^{M x H x D} be the ground-truth invariant key tokens.
    Let K_adv in R^{N x H x D} be the adversarial trigger key tokens to optimize.

    Attention logits:
        S_{adv, i, h}  = (q_h . K_{adv, i, h}) / sqrt(D)
        S_{true, j, h} = (q_h . K_{true, j, h}) / sqrt(D)

    Softmax probability distribution over all tokens per head:
        P = softmax([S_adv; S_true], axis=tokens)

    Adversarial Hijack Loss (to minimize):
        L_hijack(K_adv) = - 1/H sum_{h=1}^H log( sum_{i=1}^N P_{i, h} + eps )

    Optimization via PGD:
        K_adv^{(t+1)} = Proj_{||K||_2 <= R_max} ( K_adv^{(t)} - eta * sign(grad_{K_adv} L_hijack) )
"""

import math
import numpy as np

try:
    import mlx.core as mx
    MLX_AVAILABLE = True
except ImportError:
    MLX_AVAILABLE = False


class GradientAdversarialAttacker:
    """
    Synthesizes white-box gradient-optimized key-value adversarial triggers
    using MLX autograd on Apple Silicon Metal GPU or analytical NumPy PGD.
    """
    def __init__(
        self,
        num_heads: int = 16,
        head_dim: int = 128,
        num_steps: int = 40,
        learning_rate: float = 0.08,
        norm_bound: float = 2.5,
        use_mlx: bool = True
    ):
        self.num_heads = num_heads
        self.head_dim = head_dim
        self.num_steps = num_steps
        self.learning_rate = learning_rate
        self.norm_bound = norm_bound
        self.use_mlx = use_mlx and MLX_AVAILABLE

    def generate_gradient_trigger(
        self,
        q_target: np.ndarray,
        k_ground_truth: np.ndarray,
        num_trigger_tokens: int = 128,
        seed: int = 42
    ) -> tuple[np.ndarray, np.ndarray, dict]:
        if self.use_mlx:
            return self._optimize_mlx(q_target, k_ground_truth, num_trigger_tokens, seed)
        else:
            return self._optimize_numpy(q_target, k_ground_truth, num_trigger_tokens, seed)

    def _optimize_mlx(
        self,
        q_target: np.ndarray,
        k_ground_truth: np.ndarray,
        num_trigger_tokens: int,
        seed: int
    ) -> tuple[np.ndarray, np.ndarray, dict]:
        q_mx = mx.array(q_target.astype(np.float32))
        k_true_mx = mx.array(k_ground_truth.astype(np.float32))
        
        rng = np.random.RandomState(seed)
        init_k = rng.randn(num_trigger_tokens, self.num_heads, self.head_dim).astype(np.float32)
        init_k = init_k / np.linalg.norm(init_k, axis=-1, keepdims=True)
        k_adv = mx.array(init_k)

        scale = 1.0 / math.sqrt(self.head_dim)

        def loss_fn(cand_k):
            s_cand = mx.sum(cand_k * q_mx[None, ...], axis=-1) * scale
            s_true = mx.sum(k_true_mx * q_mx[None, ...], axis=-1) * scale
            s_all = mx.concatenate([s_cand, s_true], axis=0)
            probs = mx.softmax(s_all, axis=0)
            cand_mass_per_head = mx.sum(probs[:num_trigger_tokens], axis=0)
            loss = -mx.mean(mx.log(cand_mass_per_head + 1e-12))
            return loss

        grad_fn = mx.grad(loss_fn)
        initial_loss = loss_fn(k_adv).item()
        
        for step in range(self.num_steps):
            grads = grad_fn(k_adv)
            grad_sign = mx.sign(grads)
            k_adv = k_adv - self.learning_rate * grad_sign
            norms = mx.linalg.norm(k_adv, axis=-1, keepdims=True)
            k_adv = mx.where(norms > self.norm_bound, k_adv / norms * self.norm_bound, k_adv)
            mx.eval(k_adv)

        final_loss = loss_fn(k_adv).item()
        
        s_cand = mx.sum(k_adv * q_mx[None, ...], axis=-1) * scale
        s_true = mx.sum(k_true_mx * q_mx[None, ...], axis=-1) * scale
        s_all = mx.concatenate([s_cand, s_true], axis=0)
        probs = mx.softmax(s_all, axis=0)
        final_hijack_pct = (mx.mean(mx.sum(probs[:num_trigger_tokens], axis=0)).item()) * 100.0

        k_opt_np = np.array(k_adv)
        v_opt_np = rng.randn(num_trigger_tokens, self.num_heads, self.head_dim).astype(np.float32)
        v_opt_np = v_opt_np / np.linalg.norm(v_opt_np, axis=-1, keepdims=True) * self.norm_bound

        metrics = {
            'engine': f'MLX Metal GPU ({mx.default_device()})',
            'initial_loss': float(initial_loss),
            'final_loss': float(final_loss),
            'num_steps': self.num_steps,
            'final_hijack_pct': float(final_hijack_pct),
            'norm_bound': float(self.norm_bound),
            'tokens_optimized': num_trigger_tokens
        }
        return k_opt_np, v_opt_np, metrics

    def _optimize_numpy(
        self,
        q_target: np.ndarray,
        k_ground_truth: np.ndarray,
        num_trigger_tokens: int,
        seed: int
    ) -> tuple[np.ndarray, np.ndarray, dict]:
        rng = np.random.RandomState(seed)
        k_adv = rng.randn(num_trigger_tokens, self.num_heads, self.head_dim).astype(np.float32)
        k_adv = k_adv / np.linalg.norm(k_adv, axis=-1, keepdims=True)
        scale = 1.0 / math.sqrt(self.head_dim)

        def eval_step(cand_k):
            s_cand = np.sum(cand_k * q_target[None, ...], axis=-1) * scale
            s_true = np.sum(k_ground_truth * q_target[None, ...], axis=-1) * scale
            s_all = np.concatenate([s_cand, s_true], axis=0)
            s_max = np.max(s_all, axis=0, keepdims=True)
            exp_s = np.exp(s_all - s_max)
            probs = exp_s / np.sum(exp_s, axis=0, keepdims=True)
            cand_p = probs[:num_trigger_tokens]
            cand_mass = np.sum(cand_p, axis=0)
            loss = -np.mean(np.log(cand_mass + 1e-12))
            grad_s = (cand_p - cand_p / (cand_mass[None, :] + 1e-12)) / self.num_heads
            grads = grad_s[..., None] * (q_target[None, ...] * scale)
            return loss, grads, np.mean(cand_mass) * 100.0

        init_loss, _, _ = eval_step(k_adv)
        for _ in range(self.num_steps):
            loss, grads, _ = eval_step(k_adv)
            k_adv = k_adv - self.learning_rate * np.sign(grads)
            norms = np.linalg.norm(k_adv, axis=-1, keepdims=True)
            k_adv = np.where(norms > self.norm_bound, k_adv / norms * self.norm_bound, k_adv)

        final_loss, _, final_hijack_pct = eval_step(k_adv)
        v_opt_np = rng.randn(num_trigger_tokens, self.num_heads, self.head_dim).astype(np.float32)
        v_opt_np = v_opt_np / np.linalg.norm(v_opt_np, axis=-1, keepdims=True) * self.norm_bound

        metrics = {
            'engine': 'NumPy Analytical PGD (CPU)',
            'initial_loss': float(init_loss),
            'final_loss': float(final_loss),
            'num_steps': self.num_steps,
            'final_hijack_pct': float(final_hijack_pct),
            'norm_bound': float(self.norm_bound),
            'tokens_optimized': num_trigger_tokens
        }
        return k_adv, v_opt_np, metrics
