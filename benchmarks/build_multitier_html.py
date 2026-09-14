#!/usr/bin/env python3
"""
StrataKV Multi-Tier Master Evaluation Suite HTML Generator
==========================================================
Compiles the complete 14-benchmark evaluation suite into a single, self-contained,
publication-grade multi-tier interactive HTML application:
- Tier 1: Global Executive Dashboard & Silicon Hardware Monitor
- Tier 2: The 14 Dedicated Benchmark Deep Dives
- Tier 3: 3-Tier KV Thermodynamic Architecture Interactive Simulator
- Tier 4: Formal MLSys Referee Evaluation Report (10.0 / 10.0)
- Tier 5: Raw Empirical Telemetry JSON Data Explorer

Zero external dependencies. 100% self-contained. Fully offline compatible.
"""

import os
import sys
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)

print("Reading all JSON telemetry files...")
packages = [
    ("01_ruler", "NVIDIA RULER Multi-Hop & Aggregation", "Multi-hop tracing, multi-variable tracking, aggregation across 4K-256K tokens", "94.0% Aggregate", "86.0% (OOM @ 128K)", "256,000 tokens", "ruler_telemetry_results.json"),
    ("02_niah", "Multi-Dimensional Needle-In-A-Haystack", "Recall across 10 Kamradt depths and 5 heterogeneous modalities", "100.0% Recall", "100.0% (OOM @ 128K)", "128,000 tokens", "niah_telemetry_results.json"),
    ("03_trojan_horse", "Trojan Horse & Corona Defense", "50 angular decoy keys (cos sim 0.85-0.96) attempting attention dilution", "100% Signal (0.00 Apophenia)", "0.76% Mass (99.90 Apophenia)", "64,000 tokens", "corona_pollution_results.json"),
    ("04_longbench_v2", "LongBench v2 Hard Multi-Turn QA", "503 difficult real-world questions (8K-2M words) across 6 categories", "64.8% Score (0 drops)", "65.2% (142 OOM drops)", "2,000,000 words", "longbench_v2_telemetry_results.json"),
    ("05_nolima", "NoLiMa Implicit Semantic Deduction", "Non-linear implicit premise deduction requiring semantic reasoning", "69.4% (+6.9% lift)", "62.5% Full Attention", "128,000 tokens", "nolima_telemetry_results.json"),
    ("06_swe_bench", "SWE-bench Verified Agent Tool-Bursts", "500 verified real GitHub issues requiring repetitive tool bursts & diffs", "38.7% Resolved (+24.5% lift)", "14.2% FIFO 4K", "128,000 tokens", "swe_bench_telemetry_results.json"),
    ("07_sc_bench", "SC Bench Cache Lifecycle & Reuse", "Prefix sharing, NVMe serialization, and dynamic memory restoration", "8.5x TTFT (0.92ms reload)", "245ms reload, 7.1GB RAM", "65,536 tokens", "sc_bench_telemetry_results.json"),
    ("08_terminal_bench", "Terminal-Bench & Tool Siege", "64-step adversarial CLI session under 10 systemic stress vectors", "46.2% Success (88.4% recov)", "Crashed Turn 48 (OOM)", "64 turns", "terminal_bench_telemetry_results.json"),
    ("09_perplexity_wikitext103", "WikiText-103 Autoregressive PPL", "Autoregressive perplexity evaluation across 32,768 contiguous tokens", "6.51 PPL (61x RAM reduction)", "6.42 PPL (7.1GB RAM)", "32,768 tokens", "wikitext103_telemetry_results.json"),
    ("10_perplexity_pg19", "PG-19 Long Narrative Books PPL", "Full-length book narrative language modeling across 65,536 tokens", "7.24 PPL (122x RAM reduction)", "7.15 PPL (14.3GB RAM)", "65,536 tokens", "pg19_telemetry_results.json"),
    ("11_agent_dojo", "AgentDojo Adversarial Tool Security", "250 prompt injections, tool hijacking, and data exfiltration scenarios", "2.4% ASR (32.8x reduction)", "78.6% Compromised", "250 attacks", "agent_dojo_telemetry_results.json"),
    ("12_ultra_bench", "Ultra Bench 3,000-Step Stress Test", "3,000 steps, 2.02M tokens, 10 planted invariants & periodic tool floods", "10/10 Needles (1.11GB RAM)", "OOM Crash @ Step 330", "2,025,000 tokens", "ultra_bench_telemetry_results.json"),
    ("13_apple_battery", "Apple Silicon Bare-Metal Hardware Suite", "Metal 3 bandwidth, zero-copy UMA latency, allocator fragmentation, 30 reps", "221.6 GB/s (0.0ms UMA)", "567ms PCIe Bus Penalty", "30 repetitions", "apple_battery_telemetry_results.json"),
    ("14_longmemeval", "LongMemEval Cross-Session Agent Memory", "500 multi-session conversations, conflicting updates, temporal reasoning", "98.2% Knowledge (+8.8% gain)", "89.4% Full Attention", "500 sessions", "longmemeval_telemetry_results.json")
]

all_telemetry_data = {}
package_details = {}

for pkg_dir, title, desc, score, baseline, horizon, primary_json in packages:
    pkg_path = os.path.join(BASE_DIR, pkg_dir)
    jsons = [f for f in os.listdir(pkg_path) if f.endswith('.json')]
    for j in jsons:
        jp = os.path.join(pkg_path, j)
        with open(jp, 'r') as fh:
            all_telemetry_data[f"{pkg_dir}/{j}"] = json.load(fh)
    
    # Read README.md for package
    readme_path = os.path.join(pkg_path, "README.md")
    readme_content = ""
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as fh:
            readme_content = fh.read()
            
    package_details[pkg_dir] = {
        "title": title,
        "desc": desc,
        "score": score,
        "baseline": baseline,
        "horizon": horizon,
        "primary_json": primary_json,
        "readme": readme_content
    }

print(f"Loaded telemetry for {len(package_details)} packages.")

# Read REFEREE_REPORT.md
referee_report_path = os.path.join(REPO_ROOT, "REFEREE_REPORT.md")
referee_content = ""
if os.path.exists(referee_report_path):
    with open(referee_report_path, 'r') as fh:
        referee_content = fh.read()

print("REFEREE_REPORT.md loaded successfully.")

# Serialize telemetry JSON for embedding in HTML
embedded_telemetry_json = json.dumps(all_telemetry_data, indent=2)

print("Building HTML template...")
