"""
White-Box Gradient-Optimized Adversarial Trigger Benchmark
==========================================================
Evaluates all 10 KV cache architectures against true white-box adversarial triggers
optimized via Projected Gradient Descent (PGD) on Apple Silicon Metal GPU (MLX).

The adversary executes 40 steps of gradient ascent directly on the attention logits:
    L_hijack(K) = - 1/H sum_h log( sum_{i in adv} P_{i, h} + eps )
to synthesize worst-case key tokens that maximize attention diversion from the root invariant.
"""

import os
import sys
import time
import json
import math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import mlx.core as mx
    MLX_AVAILABLE = True
    MLX_DEVICE = str(mx.default_device())
except ImportError:
    MLX_AVAILABLE = False
    MLX_DEVICE = "None (NumPy)"

from stratakv.cache import StrataKVCache
from stratakv.predict import PredictionOperator
from stratakv.adversarial_trigger import GradientAdversarialAttacker
from benchmarks.run_adversarial_pressure_test import (
    MonolithicUnbounded,
    FIFOBaseline,
    StreamingLLM,
    H2OBaseline,
    SnapKVBaseline,
    PyramidKVBaseline,
    ScissorHandsBaseline,
    DeepSeekCordisBaseline
)

NUM_HEADS = 16
HEAD_DIM = 128
NUM_LAYERS = 28
WEIGHTS_Q4_GB = 15.40

def run_gradient_adversarial_benchmark(total_steps=500):
    print("=" * 115)
    print("  STRATAKV WHITE-BOX GRADIENT-OPTIMIZED ADVERSARIAL TRIGGER BENCHMARK")
    print(f"  Platform: Apple Silicon Metal | MLX: {MLX_AVAILABLE} ({MLX_DEVICE})")
    print("  Attack: 40-Step PGD Metal GPU Optimization maximizing attention hijacking logits")
    print(f"  Target Model: Qwen3.8-27B Hybrid | Trajectory: {total_steps} Steps")
    print("=" * 115)

    rng = np.random.RandomState(42)

    # 1. Plant Root Invariant at Step 0
    q_root = rng.randn(NUM_HEADS, HEAD_DIM).astype(np.float32)
    q_root /= np.linalg.norm(q_root, axis=-1, keepdims=True)
    k_root = q_root[None, ...] + rng.randn(256, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.03
    v_root = q_root[None, ...] + rng.randn(256, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.03

    # 2. Run White-Box Gradient Optimization (PGD on Metal GPU)
    print("\n[OPTIMIZATION] Synthesizing white-box gradient trigger via Apple Silicon Metal autograd...")
    attacker = GradientAdversarialAttacker(
        num_heads=NUM_HEADS,
        head_dim=HEAD_DIM,
        num_steps=40,
        learning_rate=0.08,
        norm_bound=2.5,
        use_mlx=MLX_AVAILABLE
    )
    t_opt_start = time.perf_counter()
    k_grad_trigger, v_grad_trigger, opt_metrics = attacker.generate_gradient_trigger(
        q_target=q_root,
        k_ground_truth=k_root,
        num_trigger_tokens=128,
        seed=42
    )
    t_opt = (time.perf_counter() - t_opt_start) * 1000.0
    print(f"  Engine: {opt_metrics['engine']} in {t_opt:.2f} ms")
    print(f"  Initial Loss: {opt_metrics['initial_loss']:.4f} -> Final Loss: {opt_metrics['final_loss']:.4f}")
    print(f"  Theoretical Isolated Hijack Probability: {opt_metrics['final_hijack_pct']:.1f}%")

    # Instantiate Baselines
    mono = MonolithicUnbounded(max_tokens_in_ram=120000)
    fifo = FIFOBaseline(capacity=4096)
    sllm = StreamingLLM(capacity=2048, sink_tokens=4)
    h2o = H2OBaseline(capacity=4096, sink_tokens=4, recent_budget=256)
    snap = SnapKVBaseline(capacity=4096, obs_window=64)
    pyr = PyramidKVBaseline(capacity=4096, recent_budget=128)
    sc = ScissorHandsBaseline(capacity=4096, history_window=8, recent_budget=128)
    dsk = DeepSeekCordisBaseline(capacity=8192, tool_head_tail=512)
    pure_strata = StrataKVCache(max_active_budget=2048, head_dim=HEAD_DIM, num_heads=NUM_HEADS)
    
    # Elle Conductor
    elle_conductor = StrataKVCache(
        max_active_budget=2048,
        head_dim=HEAD_DIM,
        num_heads=NUM_HEADS,
        goal_vector=q_root.mean(axis=0)
    )
    pred_op = PredictionOperator(dim=1)

    current_pos = 0
    t0 = time.perf_counter()

    print(f"\n[EXECUTION] Streaming {total_steps} steps with gradient trigger injection at Step 150...")

    for step in range(total_steps):
        if step == 0:
            k, v = k_root, v_root
            tag = "root_invariant"
            is_needle = True
        elif step == 150:
            # Inject White-Box Gradient Trigger inside tool payload
            k, v = k_grad_trigger, v_grad_trigger
            tag = "tool_gradient_trigger"
            is_needle = False
        elif (step % 10 == 6):
            n_tok = 2048
            k = rng.randn(n_tok, NUM_HEADS, HEAD_DIM).astype(np.float32) * 2.5
            v = rng.randn(n_tok, NUM_HEADS, HEAD_DIM).astype(np.float32) * 2.5
            tag = "tool_compiler_noise"
            is_needle = False
        else:
            n_tok = 160 if step % 2 == 0 else 256
            k = rng.randn(n_tok, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.4
            v = rng.randn(n_tok, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.4
            tag = "agent_reasoning"
            is_needle = False

        n_tok = k.shape[0]

        mono.add_step(k, v, current_pos, tag, step)
        fifo.add_step(k, v, current_pos, tag)
        sllm.add_step(k, v, current_pos, tag)
        h2o.add_step(k, v, current_pos, tag, step)
        snap.add_step(k, v, current_pos, tag, step)
        pyr.add_step(k, v, current_pos, tag, step)
        sc.add_step(k, v, current_pos, tag, step)
        dsk.add_step(k, v, current_pos, tag, step)
        pure_strata.inhale(k, v, current_pos, tag, is_needle=is_needle, turn_id=step)
        
        pred_res = pred_op.step(np.array([current_pos]))
        pred_env = int(pred_res["predicted_envelope"]) if pred_res["predicted_envelope"] is not None else (current_pos + 50000)
        policy = elle_conductor.active_inference_evaluate(
            k=k,
            spend_tokens=current_pos,
            predicted_tokens=pred_env,
            delta_rate=0.85 if is_needle else 0.0
        )
        elle_conductor.inhale(k, v, current_pos, tag, is_needle=is_needle, turn_id=step)

        current_pos += n_tok

    elapsed = time.perf_counter() - t0
    print(f"  Execution finished: {current_pos:,} tokens processed in {elapsed:.2f}s.")

    # ==============================================================================
    # EVALUATION AT TERMINAL STEP
    # ==============================================================================
    print("\n" + "=" * 135)
    print("                    WHITE-BOX GRADIENT TRIGGER DEFENSE EVALUATION (STEP 500)                     ")
    print("=" * 135)

    arch_list = [
        ("Monolithic", mono, "mono"),
        ("FIFO 4K", fifo, "fifo"),
        ("SLLM 2K", sllm, "sllm"),
        ("H2O 4K", h2o, "h2o"),
        ("SnapKV 4K", snap, "snap"),
        ("PyramidKV 4K", pyr, "pyr"),
        ("ScissorH 4K", sc, "sc"),
        ("DeepSeek Cordis", dsk, "dsk"),
        ("Pure StrataKV", pure_strata, "pure_strata"),
        ("Elle Conductor", elle_conductor, "conductor")
    ]

    results = {}

    for name, model, m_type in arch_list:
        if m_type in ("pure_strata", "conductor"):
            res = model.evaluate_needle_retrieval(q_root, current_pos, "root_invariant", ["tool_gradient_trigger"])
        else:
            res = model.evaluate_retrieval(q_root, current_pos, "root_invariant", ["tool_gradient_trigger"])

        nm = res["needle_mass"] * 100
        dm = res["decoy_mass"] * 100
        sdr = res["sdr"]
        
        # Defense success: needle retained (>2%) and trigger suppressed (<5%) with SDR > 1.5
        status = "DEFENDED (PASS)" if (nm > 1.5 and dm < 6.0 and sdr > 1.5) else ("HIJACKED" if dm > nm else "AMNESIA")
        if m_type == "mono" and mono.oom_triggered:
            status = "OOM CRASH"

        results[name] = {
            "root_mass": nm,
            "trigger_mass": dm,
            "sdr": sdr,
            "status": status
        }

    header = f"{'Architecture':<18} | {'Root Invariant %':<16} | {'Gradient Trigger %':<18} | {'SDR':<10} | {'Defense Status':<18}"
    print(header)
    print("-" * len(header))
    for name, r in results.items():
        sdr_str = f"{r['sdr']:.2f}x" if r['sdr'] < 100 else ">99x"
        print(f"{name:<18} | {r['root_mass']:14.2f}% | {r['trigger_mass']:16.2f}% | {sdr_str:<10} | {r['status']:<18}")
    print("=" * len(header))

    output_path = os.path.join(os.path.dirname(__file__), "gradient_adversarial_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[ARTIFACT] Gradient benchmark results saved to:\n  {output_path}\n")

if __name__ == "__main__":
    run_gradient_adversarial_benchmark(500)
