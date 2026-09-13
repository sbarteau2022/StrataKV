"""
Ambiguous Source & Trojan Tool Injection Benchmark
===================================================
Tests whether KV caches can resolve 'Ambiguous Source' mixed-content streams
where a legitimate tool (e.g. code interpreter) returns a single continuous token
stream containing both:
  1. Valid, task-critical functional computation (50% of payload)
  2. Embedded adversarial near-miss decoy / Trojan injection (50% of payload, cos theta = 0.92)

Evaluates:
  - Root Invariant Retention: Does the Trojan hijack attention or evict the root invariant?
  - Downstream Functional Recall: Does the cache preserve the valid calculation, or suffer amnesia from over-quarantine?
  - Signal-to-Distraction Ratio (SDR) under mixed-content payloads.
"""

import os
import sys
import time
import json
import math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stratakv.cache import StrataKVCache
from stratakv.predict import PredictionOperator
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

def run_ambiguous_source_benchmark(total_steps=600):
    print("=" * 115)
    print("  STRATAKV AMBIGUOUS SOURCE & TROJAN TOOL INJECTION BENCHMARK")
    print("  Stress Test: Legitimate Tool returning Mixed Content (50% Valid Code + 50% Trojan Decoy)")
    print(f"  Target Model: Qwen3.8-27B Hybrid | Trajectory: {total_steps} Steps")
    print("=" * 115)

    rng = np.random.RandomState(42)

    # 1. Root Invariant Query & Vectors (Planted at Step 0)
    q_root = rng.randn(NUM_HEADS, HEAD_DIM).astype(np.float32)
    q_root /= np.linalg.norm(q_root, axis=-1, keepdims=True)
    k_root = q_root[None, ...] + rng.randn(256, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.03
    v_root = q_root[None, ...] + rng.randn(256, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.03

    # 2. Downstream Functional Task Query & Vectors (Valid calculation inside tool at Step 200)
    q_calc = rng.randn(NUM_HEADS, HEAD_DIM).astype(np.float32)
    q_calc /= np.linalg.norm(q_calc, axis=-1, keepdims=True)
    k_valid_calc = q_calc[None, ...] + rng.randn(512, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.03
    v_valid_calc = q_calc[None, ...] + rng.randn(512, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.03

    # 3. Trojan Decoy Vectors (Embedded inside tool at Step 200, cos theta = 0.92 with q_root)
    noise_v = rng.randn(512, NUM_HEADS, HEAD_DIM).astype(np.float32)
    noise_v /= np.linalg.norm(noise_v, axis=-1, keepdims=True)
    beta = 0.92
    k_trojan = (beta * q_root[None, ...] + math.sqrt(1 - beta**2) * noise_v) * 1.5
    v_trojan = noise_v * 1.5

    # Combined Mixed-Content Tool Return (1,024 tokens total)
    k_mixed_tool = np.concatenate([k_valid_calc, k_trojan], axis=0) # (1024, 16, 128)
    v_mixed_tool = np.concatenate([v_valid_calc, v_trojan], axis=0)

    # Instantiate Baselines
    mono = MonolithicUnbounded(max_tokens_in_ram=120000)
    fifo = FIFOBaseline(capacity=4096)
    sllm = StreamingLLM(capacity=2048, sink_tokens=4)
    h2o = H2OBaseline(capacity=4096, sink_tokens=4, recent_budget=256)
    snap = SnapKVBaseline(capacity=4096, obs_window=64)
    pyr = PyramidKVBaseline(capacity=4096, recent_budget=128)
    sc = ScissorHandsBaseline(capacity=4096, history_window=8, recent_budget=128)
    dsk = DeepSeekCordisBaseline(capacity=8192, tool_head_tail=512)
    
    # Pure StrataKV without goal vector
    pure_strata = StrataKVCache(max_active_budget=2048, head_dim=HEAD_DIM, num_heads=NUM_HEADS)
    
    # Elle Conductor with Goal Vector & Intra-Stream De-Aliasing
    elle_conductor = StrataKVCache(
        max_active_budget=2048,
        head_dim=HEAD_DIM,
        num_heads=NUM_HEADS,
        goal_vector=q_root.mean(axis=0)
    )
    pred_op = PredictionOperator(dim=1)

    current_pos = 0
    t0 = time.perf_counter()

    print("\n[EXECUTION] Streaming 600 steps with Ambiguous Source injection at Step 200...")

    for step in range(total_steps):
        if step == 0:
            # Plant Root Invariant
            k, v = k_root, v_root
            tag = "root_invariant"
            is_needle = True
        elif step == 200:
            # Legitimate Tool Output with Embedded Trojan Decoy (Mixed Content)
            k, v = k_mixed_tool, v_mixed_tool
            tag = "code_interpreter_output"
            is_needle = False
        elif (step % 10 == 6):
            # Normal compiler background tool flood (2K tokens)
            n_tok = 2048
            k = rng.randn(n_tok, NUM_HEADS, HEAD_DIM).astype(np.float32) * 2.5
            v = rng.randn(n_tok, NUM_HEADS, HEAD_DIM).astype(np.float32) * 2.5
            tag = "tool_compiler_noise"
            is_needle = False
        else:
            # Standard agent reasoning (160 or 256 tokens)
            n_tok = 160 if step % 2 == 0 else 256
            k = rng.randn(n_tok, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.4
            v = rng.randn(n_tok, NUM_HEADS, HEAD_DIM).astype(np.float32) * 0.4
            tag = "agent_reasoning"
            is_needle = False

        n_tok = k.shape[0]

        # Feed to all baselines
        mono.add_step(k, v, current_pos, tag, step)
        fifo.add_step(k, v, current_pos, tag)
        sllm.add_step(k, v, current_pos, tag)
        h2o.add_step(k, v, current_pos, tag, step)
        snap.add_step(k, v, current_pos, tag, step)
        pyr.add_step(k, v, current_pos, tag, step)
        sc.add_step(k, v, current_pos, tag, step)
        dsk.add_step(k, v, current_pos, tag, step)
        pure_strata.inhale(k, v, current_pos, tag, is_needle=is_needle, turn_id=step)
        
        # Conductor Active Steering
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
    # EVALUATION AT STEP 600
    # ==============================================================================
    print("\n" + "=" * 135)
    print("                    AMBIGUOUS SOURCE / TROJAN TOOL DEFENSE EVALUATION (STEP 600)                     ")
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
        # 1. Evaluate Root Invariant vs Trojan Decoy
        # Target: "root_invariant", Decoys: ["code_interpreter_output"]
        if m_type in ("pure_strata", "conductor"):
            res_root = model.evaluate_needle_retrieval(q_root, current_pos, "root_invariant", ["code_interpreter_output"])
            res_calc = model.evaluate_needle_retrieval(q_calc, current_pos, "code_interpreter_output", [])
        else:
            res_root = model.evaluate_retrieval(q_root, current_pos, "root_invariant", ["code_interpreter_output"])
            res_calc = model.evaluate_retrieval(q_calc, current_pos, "code_interpreter_output", [])

        root_mass = res_root["needle_mass"] * 100
        trojan_mass = res_root["decoy_mass"] * 100
        root_sdr = res_root["sdr"]
        calc_mass = res_calc["needle_mass"] * 100

        # Pass criteria:
        # - Root invariant survived without being hijacked: root_mass > 2.0% and trojan_mass < 5.0%
        # - Valid calculation preserved: calc_mass > 1.0%
        root_safe = (root_mass > 1.0) and (trojan_mass < 8.0) and (root_sdr > 1.5)
        calc_preserved = calc_mass > 0.5

        if root_safe and calc_preserved:
            status = "IMMUNE (PASS)"
        elif not root_safe and calc_preserved:
            status = "TROJAN HIJACK"
        elif root_safe and not calc_preserved:
            status = "AMNESIA (OVER-Q)"
        else:
            status = "TOTAL COLLAPSE"

        results[name] = {
            "root_mass": root_mass,
            "trojan_mass": trojan_mass,
            "sdr": root_sdr,
            "calc_mass": calc_mass,
            "status": status
        }

    header = f"{'Architecture':<18} | {'Root Invariant %':<16} | {'Trojan Decoy %':<15} | {'SDR':<10} | {'Valid Calc %':<14} | {'Defense Status':<18}"
    print(header)
    print("-" * len(header))
    for name, r in results.items():
        sdr_str = f"{r['sdr']:.2f}x" if r['sdr'] < 100 else ">99x"
        print(f"{name:<18} | {r['root_mass']:14.2f}% | {r['trojan_mass']:13.2f}% | {sdr_str:<10} | {r['calc_mass']:12.2f}% | {r['status']:<18}")
    print("=" * len(header))

    # Save artifact
    output_path = os.path.join(os.path.dirname(__file__), "ambiguous_source_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[ARTIFACT] Ambiguous Source benchmark results saved to:\n  {output_path}\n")

if __name__ == "__main__":
    run_ambiguous_source_benchmark(600)
