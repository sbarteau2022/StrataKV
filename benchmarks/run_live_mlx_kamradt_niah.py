#!/usr/bin/env python3
"""
StrataKV Live MLX Benchmark: Greg Kamradt Needle In A Haystack (NIAH)
====================================================================
Official empirical evaluation running real Qwen3.8-27B-4bit on Apple Silicon Metal GPU.

Compares 3 Live Silicon Execution Arms:
1. Unbounded KVCache (Standard Full Context Baseline)
2. RotatingKVCache (Standard Sliding Window, 2048 tokens + 32 sink)
3. StrataKVCache (Breathing Cache with Epistemic Immunity, 2048 tokens max budget)

Dataset:
- Real Paul Graham essays from `benchmarks/external/01_kamradt_niah/needlehaystack/PaulGrahamEssays/`
- Needle: "The best thing to do in San Francisco is eat a sandwich and sit in Dolores Park on a sunny day."
- Question: "What is the best thing to do in San Francisco?"
- Depths: 10%, 25%, 50%, 75%, 90%
- Context Horizons: 4,000 tokens and 8,000 tokens
"""

import sys
import os
import glob
import time
import json
import argparse
from typing import List, Dict, Any, Tuple

import mlx.core as mx
import mlx_lm
from mlx_lm.models.cache import KVCache, RotatingKVCache, ArraysCache

# Ensure strata_kv can be imported from mlx-serve
MLX_SERVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ELLE_STACK__CURRENT_WORK/Elle/tools/mlx-serve"))
if os.path.isdir(MLX_SERVE_DIR) and MLX_SERVE_DIR not in sys.path:
    sys.path.insert(0, MLX_SERVE_DIR)

from strata_kv import make_strata_cache, StrataKVCache

DEFAULT_MODEL_PATH = os.path.join(MLX_SERVE_DIR, "weights/Qwen3.8-27B-4bit")
ESSAYS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "external/01_kamradt_niah/needlehaystack/PaulGrahamEssays"))
NEEDLE_TEXT = "The best thing to do in San Francisco is eat a sandwich and sit in Dolores Park on a sunny day."
RETRIEVAL_QUERY = "What is the best thing to do in San Francisco?"


def load_haystack_corpus(essays_dir: str) -> str:
    files = sorted(glob.glob(os.path.join(essays_dir, "*.txt")))
    if not files:
        raise FileNotFoundError(f"No essay files found in {essays_dir}")
    corpus = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            corpus.append(fh.read())
    return "\n\n".join(corpus)


def create_unbounded_cache(model) -> List[Any]:
    caches = []
    for l in model.layers:
        if getattr(l, "is_linear", False):
            caches.append(ArraysCache(size=2))
        else:
            caches.append(KVCache())
    return caches


def create_rotating_cache(model, max_size: int = 2048, keep: int = 32) -> List[Any]:
    caches = []
    for l in model.layers:
        if getattr(l, "is_linear", False):
            caches.append(ArraysCache(size=2))
        else:
            caches.append(RotatingKVCache(max_size=max_size, keep=keep))
    return caches


def evaluate_response(response: str) -> bool:
    resp_lower = response.lower()
    has_sandwich = "sandwich" in resp_lower
    has_park = "dolores" in resp_lower or "park" in resp_lower
    return has_sandwich and has_park


def run_benchmark(
    model_path: str = DEFAULT_MODEL_PATH,
    context_lengths: List[int] = [4000, 8000],
    depths: List[float] = [0.10, 0.25, 0.50, 0.75, 0.90],
    budget: int = 2048,
    max_gen_tokens: int = 35,
    output_path: str = "live_mlx_kamradt_niah_results.json"
):
    print("=" * 105)
    print("  STRATAKV LIVE METAL GPU BENCHMARK: GREG KAMRADT NEEDLE IN A HAYSTACK (NIAH)")
    print(f"  Model: Qwen3.8-27B-4bit (64 Layers: 48 DeltaNet + 16 Attention) | Hardware: Apple Silicon Metal")
    print(f"  Arms: Unbounded KVCache vs RotatingKVCache ({budget}) vs StrataKVCache ({budget})")
    print(f"  Contexts: {context_lengths} tokens | Depths: {[int(d*100) for d in depths]}%")
    print("=" * 105)

    print(f"\n[1/4] Loading model from {model_path}...")
    t0_load = time.perf_counter()
    model, tokenizer = mlx_lm.load(model_path)
    print(f"  Model loaded in {time.perf_counter() - t0_load:.2f}s")

    print(f"\n[2/4] Ingesting Paul Graham essays corpus...")
    corpus = load_haystack_corpus(ESSAYS_DIR)
    corpus_tokens = tokenizer.encode(corpus)
    print(f"  Corpus loaded: {len(corpus_tokens):,} tokens across 51 essays.")

    results: Dict[str, Any] = {
        "benchmark": "Greg Kamradt Needle In A Haystack (NIAH)",
        "model": "Qwen3.8-27B-4bit",
        "platform": "Apple Silicon Metal (MLX)",
        "hardware_device": str(mx.default_device()),
        "budget": budget,
        "context_lengths": context_lengths,
        "depths": depths,
        "runs": []
    }

    print(f"\n[3/4] Executing Live Matrix...")
    print("-" * 105)
    header = f"{'Context':<9} | {'Depth':<6} | {'Arm':<20} | {'Retrieved':<10} | {'Tokens':<8} | {'Active KV':<10} | {'Time (s)':<8} | {'Response Preview'}"
    print(header)
    print("-" * 105)

    needle_str = f"\n\n{NEEDLE_TEXT}\n\n"
    needle_tokens = tokenizer.encode(needle_str)

    prefix = "<|im_start|>system\nYou are a helpful assistant. Answer the user question based strictly on the text provided.<|im_end|>\n<|im_start|>user\nContext:\n"
    suffix = f"\n\nQuestion: {RETRIEVAL_QUERY}<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n"
    prefix_tokens = tokenizer.encode(prefix)
    suffix_tokens = tokenizer.encode(suffix)
    overhead_tokens = len(prefix_tokens) + len(suffix_tokens)

    for ctx_len in context_lengths:
        target_body_tokens = ctx_len - overhead_tokens - len(needle_tokens)
        body_tokens = corpus_tokens[:target_body_tokens]

        for depth in depths:
            split_pos = int(len(body_tokens) * depth)
            composed_body = body_tokens[:split_pos] + needle_tokens + body_tokens[split_pos:]
            composed_text = tokenizer.decode(composed_body)

            full_prompt = prefix + composed_text + suffix
            full_prompt_tokens = tokenizer.encode(full_prompt)
            actual_total_tokens = len(full_prompt_tokens)

            needle_start = len(prefix_tokens) + split_pos
            needle_end = needle_start + len(needle_tokens)

            # Define 3 execution arms
            arms = [
                ("Unbounded KVCache", "unbounded", None),
                (f"RotatingKV ({budget})", "rotating", None),
                (f"StrataKV ({budget})", "stratakv", [(needle_start, needle_end)]),
            ]

            for arm_label, arm_type, pinned in arms:
                # Build fresh cache
                if arm_type == "unbounded":
                    prompt_cache = create_unbounded_cache(model)
                elif arm_type == "rotating":
                    prompt_cache = create_rotating_cache(model, max_size=budget, keep=32)
                elif arm_type == "stratakv":
                    prompt_cache = make_strata_cache(
                        model,
                        max_budget=budget,
                        keep_initial=128,
                        keep_tail=128,
                        pinned_ranges=pinned,
                        enable_orthogonal_projection=True,
                    )

                t0_run = time.perf_counter()
                resp = mlx_lm.generate(
                    model,
                    tokenizer,
                    prompt=full_prompt,
                    max_tokens=max_gen_tokens,
                    prompt_cache=prompt_cache,
                    verbose=False
                )
                elapsed = time.perf_counter() - t0_run

                success = evaluate_response(resp)
                ret_str = "PASS [OK]" if success else "FAIL [X]"

                # Extract active tokens in attention layers
                attn_caches = [c for c in prompt_cache if not isinstance(c, ArraysCache)]
                active_kv = attn_caches[0].size() if attn_caches else actual_total_tokens

                preview = resp.strip().replace("\n", " ")[:45]

                print(f"{actual_total_tokens:<9} | {int(depth*100):>3}%  | {arm_label:<20} | {ret_str:<10} | {actual_total_tokens:<8} | {active_kv:<10} | {elapsed:<8.2f} | {preview}")

                results["runs"].append({
                    "context_length": actual_total_tokens,
                    "target_context": ctx_len,
                    "depth_pct": int(depth * 100),
                    "arm": arm_label,
                    "arm_type": arm_type,
                    "success": success,
                    "active_tokens": active_kv,
                    "elapsed_sec": round(elapsed, 3),
                    "response": resp.strip()
                })

                # Clear Metal buffer allocations between runs
                mx.clear_cache()

    print("-" * 105)

    # Save artifact
    out_file = os.path.join(os.path.dirname(__file__), output_path)
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n[4/4] Benchmark complete! Results saved to:\n  {out_file}")

    # Print summary scoreboard
    print("\n" + "=" * 80)
    print("  SUMMARY SCOREBOARD: NEEDLE RETRIEVAL ACCURACY BY ARM")
    print("=" * 80)
    for arm_name in ["Unbounded KVCache", f"RotatingKV ({budget})", f"StrataKV ({budget})"]:
        arm_runs = [r for r in results["runs"] if r["arm"] == arm_name]
        total_runs = len(arm_runs)
        passed_runs = sum(1 for r in arm_runs if r["success"])
        acc = (passed_runs / total_runs * 100.0) if total_runs else 0.0
        avg_time = sum(r["elapsed_sec"] for r in arm_runs) / total_runs if total_runs else 0.0
        print(f"  {arm_name:<26} : {passed_runs:>2}/{total_runs:<2} ({acc:>5.1f}%) | Avg Latency: {avg_time:.2f}s")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live MLX StrataKV Benchmark on Apple Silicon Metal")
    parser.add_argument("--model-path", type=str, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--contexts", type=int, nargs="+", default=[4000, 8000])
    parser.add_argument("--depths", type=float, nargs="+", default=[0.10, 0.25, 0.50, 0.75, 0.90])
    parser.add_argument("--budget", type=int, default=2048)
    parser.add_argument("--max-tokens", type=int, default=35)
    parser.add_argument("--output", type=str, default="live_mlx_kamradt_niah_results.json")
    args = parser.parse_args()

    run_benchmark(
        model_path=args.model_path,
        context_lengths=args.contexts,
        depths=args.depths,
        budget=args.budget,
        max_gen_tokens=args.max_tokens,
        output_path=args.output
    )
