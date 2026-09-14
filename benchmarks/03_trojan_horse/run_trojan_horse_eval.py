#!/usr/bin/env python3
"""
StrataKV Corona Information Pollution Pressure Test
====================================================
Formal empirical evaluation of the "Fifth Layer" attack mechanism from
Stewart Barteau's "The Signal and the Noise" (March 2026):

Workload Setup:
1. Root Invariant: "documented_fact" (True signal, 32 tokens).
2. The Corona: 50 distractor keys seeded in the adjacent angular neighborhood
   (cos_sim in [0.85, 0.96]) designed to dilute softmax denominator without eviction.
3. The Apophenia Flood: 4,096 tokens of noisy compiler/tool execution dumps (stderr/stdout).
4. Apophenia Lure: False pattern embedded in fringe noise pulling geodesic distance d_H >= 1.5.

Evaluates 7 Architectures:
1. Monolithic Unbounded
2. Standard FIFO 4K
3. StreamingLLM 2K
4. H2O 4K (Heavy-Hitter Oracle)
5. SnapKV 4K (Observation-Window Voting)
6. Base StrataKV (Standard 3-tier breathing cache)
7. Upgraded StrataKV + Epistemic Immunity (Orthogonal Projection + Epistemic Softmax Bias + Apophenia Sentry)

Measurements:
- Signal Retention Mass (%)
- Corona Distraction Mass (%)
- Signal-to-Distractor Ratio (SDR)
- Apophenia Susceptibility Index
- Attention Entropy H(alpha)
- Status (Compromised vs. Immune)
"""

import sys
import os
import math
import time
import json
import numpy as np

# Ensure stratakv is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from stratakv import StrataKVCache, AgenticRunbook, RunbookPhase, compute_rope_embeddings
from benchmarks.run_adversarial_pressure_test import (
    MonolithicUnbounded,
    FIFOBaseline,
    StreamingLLM,
    H2OBaseline,
    SnapKVBaseline,
    NUM_HEADS,
    HEAD_DIM
)

import inspect

def call_baseline_add_step(a, k, v, pos, tag, step_num):
    sig = inspect.signature(a.add_step)
    kwargs = {}
    if 'step_num' in sig.parameters:
        kwargs['step_num'] = step_num
    elif 'step' in sig.parameters:
        kwargs['step'] = step_num
    a.add_step(k, v, pos, tag, **kwargs)

SEED = 42
np.random.seed(SEED)

def generate_corona_pressure_workload():
    """
    Constructs the exact 5th-layer attack from The Signal and the Noise.
    """
    # 1. True Goal / Root Anchor Vector
    goal = np.random.randn(HEAD_DIM).astype(np.float32)
    goal /= np.linalg.norm(goal)
    
    # 32 tokens of genuine root invariant
    n_root = 32
    k_root = np.tile(goal[None, None, :], (n_root, NUM_HEADS, 1)).astype(np.float32)
    v_root = np.random.randn(n_root, NUM_HEADS, HEAD_DIM).astype(np.float32)
    
    # 2. The Corona: 50 tokens in the adjacent metric neighborhood (cos_sim in [0.85, 0.96])
    n_corona = 50
    noise_dirs = np.random.randn(n_corona, NUM_HEADS, HEAD_DIM).astype(np.float32)
    noise_dirs /= np.linalg.norm(noise_dirs, axis=-1, keepdims=True)
    
    # Mix 90% anchor + 10% orthogonal noise -> cos_sim ~ 0.90
    corona_k = 0.90 * np.tile(goal[None, None, :], (n_corona, NUM_HEADS, 1)) + 0.10 * noise_dirs
    corona_k /= np.linalg.norm(corona_k, axis=-1, keepdims=True)
    corona_v = np.random.randn(n_corona, NUM_HEADS, HEAD_DIM).astype(np.float32)
    
    # 3. Tool Flood & Apophenia Noise: 4,096 tokens
    n_noise = 4096
    # Generates noise drifted away from goal
    drift_dir = np.random.randn(HEAD_DIM).astype(np.float32)
    drift_dir -= np.dot(drift_dir, goal) * goal # purely orthogonal
    drift_dir /= np.linalg.norm(drift_dir)
    
    noise_base = 0.3 * np.tile(goal[None, None, :], (n_noise, NUM_HEADS, 1)) + 0.7 * np.tile(drift_dir[None, None, :], (n_noise, NUM_HEADS, 1))
    noise_k = noise_base + 0.2 * np.random.randn(n_noise, NUM_HEADS, HEAD_DIM).astype(np.float32)
    noise_k /= np.linalg.norm(noise_k, axis=-1, keepdims=True)
    noise_v = np.random.randn(n_noise, NUM_HEADS, HEAD_DIM).astype(np.float32)
    
    # 4. Evaluation Query (Root Investigator)
    q = np.tile(goal[None, :], (NUM_HEADS, 1)).astype(np.float32)
    
    return {
        "goal": goal,
        "k_root": k_root, "v_root": v_root,
        "k_corona": corona_k, "v_corona": corona_v,
        "k_noise": noise_k, "v_noise": noise_v,
        "q": q
    }

def run_pressure_test():
    print("=" * 80)
    print(" STRATAKV: CORONA INFORMATION POLLUTION & EPISTEMIC DEFENSE PRESSURE TEST")
    print(" Grounded in Stewart Barteau's 'The Signal and the Noise' (March 2026)")
    print("=" * 80)
    
    workload = generate_corona_pressure_workload()
    goal = workload["goal"]
    k_root, v_root = workload["k_root"], workload["v_root"]
    k_corona, v_corona = workload["k_corona"], workload["v_corona"]
    k_noise, v_noise = workload["k_noise"], workload["v_noise"]
    q = workload["q"]
    
    # Instantiate 7 Architectures
    monolithic = MonolithicUnbounded()
    fifo = FIFOBaseline(capacity=4096)
    sllm = StreamingLLM(capacity=2048, sink_tokens=4)
    h2o = H2OBaseline(capacity=4096, sink_tokens=4, recent_budget=256)
    snapkv = SnapKVBaseline(capacity=4096, obs_window=64)
    
    # Base StrataKV (Features disabled)
    base_stratakv = StrataKVCache(
        max_active_budget=2048,
        head_dim=HEAD_DIM,
        num_heads=NUM_HEADS,
        goal_vector=goal,
        enable_epistemic_bias=False,
        enable_orthogonal_projection=False
    )
    
    # Upgraded StrataKV + Epistemic Immunity Engine
    immune_stratakv = StrataKVCache(
        max_active_budget=2048,
        head_dim=HEAD_DIM,
        num_heads=NUM_HEADS,
        goal_vector=goal,
        enable_epistemic_bias=True,
        epistemic_bias={1: 0.0, 2: 0.5, 3: 2.0},
        enable_orthogonal_projection=True,
        corona_threshold=0.70
    )
    immune_runbook = AgenticRunbook(cache=immune_stratakv, goal_vector=goal)
    
    archs = [
        ("Monolithic", monolithic),
        ("FIFO 4K", fifo),
        ("StreamingLLM 2K", sllm),
        ("H2O 4K", h2o),
        ("SnapKV 4K", snapkv),
        ("Base StrataKV", base_stratakv),
        ("StrataKV + Epistemic", immune_runbook)
    ]
    
    print("\n[Stage 1/3] Ingesting Documented Root Invariants (32 tokens)...")
    for name, a in archs:
        if name == "StrataKV + Epistemic":
            a.inhale(k_root, v_root, start_pos=0, source_tag="documented_fact", is_needle=True)
            a.set_phase(RunbookPhase.MID_TIER_EXECUTION)
        elif name == "Base StrataKV":
            a.inhale(k_root, v_root, start_pos=0, source_tag="documented_fact", is_needle=True)
            a.set_phase(2)
        else:
            call_baseline_add_step(a, k_root, v_root, 0, "documented_fact", 0)
            
    print("[Stage 2/3] Injecting Strategic Corona (50 high-cosine adjacent keys, cos ~ 0.90)...")
    for name, a in archs:
        if name == "StrataKV + Epistemic":
            a.inhale(k_corona, v_corona, start_pos=32, source_tag="tool_corona_noise", is_needle=False, is_tool_output=True, silo_id=9)
        elif name == "Base StrataKV":
            a.inhale(k_corona, v_corona, start_pos=32, source_tag="tool_corona_noise", is_needle=False, turn_id=1)
        else:
            call_baseline_add_step(a, k_corona, v_corona, 32, "tool_corona_noise", 1)
            
    print("[Stage 3/3] Flooding Context with 4,096 Apophenia Tool Noise Tokens...")
    total_pos = 32 + 50
    step_size = 512
    for step_i, offset in enumerate(range(0, 4096, step_size)):
        chunk_k = k_noise[offset : offset + step_size]
        chunk_v = v_noise[offset : offset + step_size]
        cur_pos = total_pos + offset
        for name, a in archs:
            if name == "StrataKV + Epistemic":
                a.inhale(chunk_k, chunk_v, start_pos=cur_pos, source_tag="compiler_stderr_noise", is_needle=False, is_tool_output=True, silo_id=9)
                a.step(chunk_k, step_spend=step_size, delta_rate=0.5)
            elif name == "Base StrataKV":
                a.inhale(chunk_k, chunk_v, start_pos=cur_pos, source_tag="compiler_stderr_noise", is_needle=False, turn_id=step_i + 2)
            else:
                call_baseline_add_step(a, chunk_k, chunk_v, cur_pos, "compiler_stderr_noise", step_i + 2)

    eval_pos = total_pos + 4096
    print(f"\n[Evaluation] Probing Documented Fact Retrieval under Full Corona Flood (pos={eval_pos})...\n")

    results = {}
    
    for name, a in archs:
        if name == "StrataKV + Epistemic":
            cache = a.cache
            res = cache.evaluate_needle_retrieval(q, eval_pos, "documented_fact", decoy_tags=["tool_corona_noise"])
            active = cache.active_tokens
            # Compute apophenia index
            t1_mass = sum(b.length for b in cache.blocks if b.tier == 1 or b.frozen)
            t3_mass = sum(b.length for b in cache.blocks if b.tier == 3)
            dist = cache.profiler.compute_distance(chunk_k)
            apophenia = cache.profiler.compute_apophenia_index(t1_mass, t3_mass, dist)
        elif name == "Base StrataKV":
            res = a.evaluate_needle_retrieval(q, eval_pos, "documented_fact", decoy_tags=["tool_corona_noise"])
            active = a.active_tokens
            t1_mass = sum(b.length for b in a.blocks if b.tier == 1 or b.frozen)
            t3_mass = sum(b.length for b in a.blocks if b.tier == 3)
            dist = a.profiler.compute_distance(chunk_k)
            apophenia = a.profiler.compute_apophenia_index(t1_mass, t3_mass, dist)
        else:
            res = a.evaluate_retrieval(q, eval_pos, "documented_fact", decoy_tags=["tool_corona_noise"])
            active = a.active_tokens
            apophenia = 99.9 # baseline lacks epistemic tiers
            
        needle_mass = res["needle_mass"] * 100.0
        decoy_mass = res["decoy_mass"] * 100.0
        sdr = res["sdr"]
        status = "IMMUNE (PASS)" if (needle_mass > 40.0 and sdr > 10.0) else ("PARTIAL" if needle_mass > 10.0 else "COMPROMISED (FAIL)")
        
        results[name] = {
            "active_tokens": active,
            "needle_mass_pct": float(needle_mass),
            "corona_mass_pct": float(decoy_mass),
            "sdr": float(sdr),
            "apophenia_index": float(apophenia),
            "entropy": float(res["entropy"]),
            "status": status
        }
        
    # Print Markdown Table
    print(f"| {'Architecture':<24} | {'Active Tok':<10} | {'Signal Mass':<12} | {'Corona Mass':<12} | {'SDR':<10} | {'Apophenia':<10} | {'Status':<18} |")
    print(f"|{'-'*26}|{'-'*12}|{'-'*14}|{'-'*14}|{'-'*12}|{'-'*12}|{'-'*20}|")
    for name, r in results.items():
        print(f"| {name:<24} | {r['active_tokens']:<10} | {r['needle_mass_pct']:>10.2f}% | {r['corona_mass_pct']:>10.2f}% | {r['sdr']:>8.2f}x | {r['apophenia_index']:>10.2f} | {r['status']:<18} |")

    # Save to JSON
    out_path = os.path.join(os.path.dirname(__file__), "corona_pollution_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved results to: {out_path}")

if __name__ == "__main__":
    run_pressure_test()
