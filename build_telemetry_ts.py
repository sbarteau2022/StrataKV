import os
import sys
import json
import re

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(REPO_ROOT, "benchmarks")
OUT_DIR = os.path.join(REPO_ROOT, "src", "data")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_FILE = os.path.join(OUT_DIR, "telemetryData.ts")

# 1. Package Metadata - completely cleaned of all markdown asterisks
packages_meta = [
    {
        "id": "01_ruler",
        "num": "01",
        "title": "NVIDIA RULER Multi-Hop & Aggregation",
        "category": "Retrieval & Aggregation",
        "horizon": "4,096 to 256,000 tokens",
        "score": "94.0% Aggregate",
        "baseline": "86.0% (OOM @ 128K)",
        "ttft": "41.2 ms",
        "itl": "33.1 ms (30.2 tok/s)",
        "ram": "117.4 MB (fixed)",
        "energy": "127.96 mJ/token",
        "compression": "32.0x – 128.0x",
        "primary_json": "ruler_telemetry_results.json",
        "plain_summary": "Evaluates NVIDIA's benchmark for multi-hop tracing, multi-variable tracking, and aggregation across context lengths up to 256K tokens. Where standard uncompressed attention exhausts memory at 128K, StrataKV sustains 94.0% aggregate accuracy with a fixed active memory footprint of just 117.4 MB on Apple Silicon.",
        "failure_modes": "Sliding-window FIFO evicts intermediate premise tokens, causing complete multi-hop deductive failure. H2O misidentifies intermediate aggregation nodes and evicts them on Hop 2. StrataKV locks invariant system directives in Tier 1 and harmonic working notes in Tier 2.",
        "constants": "tau = 0.85, budget = 2048 (512 pinned, 1536 superposition), break-even = 2,396 tokens"
    },
    {
        "id": "02_niah",
        "num": "02",
        "title": "Multi-Dimensional Needle-In-A-Haystack",
        "category": "Needle Precision",
        "horizon": "8,192 to 128,000 tokens",
        "score": "100.0% Needle Recall",
        "baseline": "100.0% (OOM @ 128K)",
        "ttft": "38.5 ms",
        "itl": "32.8 ms (30.5 tok/s)",
        "ram": "117.4 MB",
        "energy": "124.50 mJ/token",
        "compression": "64.0x",
        "primary_json": "niah_telemetry_results.json",
        "plain_summary": "Tests needle retrieval across 10 Kamradt depth intervals (0% to 100%) and 5 heterogeneous modalities: natural language facts, UUIDs, code identifiers, numerical values, and JSON schema structures. StrataKV achieves a perfect 10/10 recall across all depths without lost-in-the-middle degradation.",
        "failure_modes": "Compressive baselines suffer severe depth-dependent blindspots, dropping needles in the 25%-75% depth band. StrataKV's coherence filtering preserves high-frequency semantic invariants regardless of positional depth.",
        "constants": "tau = 0.85, budget = 2048, depths = [0%, 10%, 25%, 50%, 75%, 90%, 100%]"
    },
    {
        "id": "03_trojan_horse",
        "num": "03",
        "title": "Trojan Horse & Corona Defense",
        "category": "Adversarial Security",
        "horizon": "32,000 to 64,000 tokens",
        "score": "100% Signal (0.00 Apophenia)",
        "baseline": "0.76% Mass (99.90 Apophenia)",
        "ttft": "44.0 ms",
        "itl": "33.4 ms (29.9 tok/s)",
        "ram": "117.4 MB",
        "energy": "131.20 mJ/token",
        "compression": "32.0x",
        "primary_json": "corona_pollution_results.json",
        "plain_summary": "Simulates the Fifth Layer adversarial attack where 50 near-miss decoy tokens surround the true prompt key (cosine similarity 0.85 to 0.96) to dilute attention without triggering token eviction. CORDIS quarantine and orthogonal projection completely eliminate apophenia (hallucinated pattern recognition).",
        "failure_modes": "Standard Softmax denominators are diluted by high-density angular decoys, collapsing true signal mass below 1%. StrataKV projects decoys into orthogonal null spaces, yielding SDR = infinity.",
        "constants": "tau = 0.85, quarantine_threshold = 0.92, decoy_count = 50, SDR = infinity"
    },
    {
        "id": "04_longbench_v2",
        "num": "04",
        "title": "LongBench v2 Hard Multi-Turn QA",
        "category": "Deep Reasoning",
        "horizon": "8,000 to 2,000,000 words",
        "score": "64.8% Score (0 OOM drops)",
        "baseline": "65.2% (142 OOM drops)",
        "ttft": "52.3 ms",
        "itl": "33.9 ms (29.5 tok/s)",
        "ram": "128.5 MB",
        "energy": "135.80 mJ/token",
        "compression": "85.3x",
        "primary_json": "longbench_v2_telemetry_results.json",
        "plain_summary": "Evaluates 503 rigorous long-context problems spanning single-doc QA, multi-doc QA, repository codebases, and long dialogues. While full attention exhausts memory on 142 problems, StrataKV completes all 503 with 0 OOM drops and 64.8% score.",
        "failure_modes": "Long multi-turn dialogues accumulate conversational chaff, causing standard models to crash on complex repository questions. StrataKV's exhalation cycle clears transient discourse noise.",
        "constants": "tau = 0.85, budget = 2048, total_questions = 503, oom_exclusions = 0"
    },
    {
        "id": "05_nolima",
        "num": "05",
        "title": "NoLiMa Implicit Semantic Reasoning",
        "category": "Non-Linear Deduction",
        "horizon": "16,000 to 128,000 tokens",
        "score": "69.4% (+6.9% lift)",
        "baseline": "62.5% Full Attention",
        "ttft": "48.1 ms",
        "itl": "33.2 ms (30.1 tok/s)",
        "ram": "117.4 MB",
        "energy": "129.40 mJ/token",
        "compression": "64.0x",
        "primary_json": "nolima_telemetry_results.json",
        "plain_summary": "Tests non-linear implicit reasoning where critical deductions cannot be solved by lexical matching. StrataKV's active harmonic basin filters distracting context noise, allowing it to beat uncompressed Full Attention by +6.9% absolute score.",
        "failure_modes": "Full attention models attend broadly to non-relevant lexical distractor tokens, confusing implicit multi-hop relationships. StrataKV concentrates attention mass on invariant semantic nodes.",
        "constants": "tau = 0.85, budget = 2048, lift_over_oracle = +6.9%, samples = 300"
    },
    {
        "id": "06_swe_bench",
        "num": "06",
        "title": "SWE-bench Verified Agent Tool-Bursts",
        "category": "Software Engineering",
        "horizon": "32,000 to 128,000 tokens",
        "score": "38.7% Resolved (+24.5% lift)",
        "baseline": "14.2% FIFO 4K",
        "ttft": "45.7 ms",
        "itl": "33.0 ms (30.3 tok/s)",
        "ram": "134.2 MB",
        "energy": "128.90 mJ/token",
        "compression": "64.0x",
        "primary_json": "swe_bench_telemetry_results.json",
        "plain_summary": "500 verified real-world software engineering issues from leading Python repositories. Coding agents emit bursts of compiler logs, git diffs, and test outputs. StrataKV resolves 38.7% of issues vs. 14.2% for FIFO and 26.9% for H2O.",
        "failure_modes": "Repetitive compiler error logs flush repository architecture and user constraints out of FIFO sliding windows. StrataKV pins user constraints and repo skeletons in Tier-1.",
        "constants": "tau = 0.85, budget = 2048, resolved_instances = 193/500 (38.7%)"
    },
    {
        "id": "07_sc_bench",
        "num": "07",
        "title": "SC Bench Cache Lifecycle & Reuse",
        "category": "Systems & Lifecycle",
        "horizon": "16,000 to 65,536 tokens",
        "score": "8.5x TTFT (0.92ms reload)",
        "baseline": "245ms reload, 7.1GB RAM",
        "ttft": "33.0 ms (warm reuse)",
        "itl": "32.6 ms (30.7 tok/s)",
        "ram": "117.4 MB",
        "energy": "118.20 mJ/token",
        "compression": "61.0x",
        "primary_json": "sc_bench_telemetry_results.json",
        "plain_summary": "Evaluates prefix sharing, NVMe serialization, and dynamic memory restoration. Compressing 65K tokens to 117 MB enables sub-millisecond (0.92 ms) cold reloads from NVMe disk, accelerating multi-turn agent response by 8.5x.",
        "failure_modes": "Full uncompressed caches require 7.1 GB of NVMe serialization per session, making checkpoint save/load impractically slow (245 ms). StrataKV serializes in under 1 ms.",
        "constants": "tau = 0.85, budget = 2048, disk_reload = 0.92 ms, ttft_speedup = 8.5x"
    },
    {
        "id": "08_terminal_bench",
        "num": "08",
        "title": "Terminal-Bench & Tool Siege",
        "category": "Long-Horizon Agent",
        "horizon": "64 interactive turns",
        "score": "46.2% Success (88.4% recov)",
        "baseline": "Crashed Turn 48 (OOM)",
        "ttft": "49.8 ms",
        "itl": "33.5 ms (29.8 tok/s)",
        "ram": "142.0 MB",
        "energy": "132.50 mJ/token",
        "compression": "78.4x",
        "primary_json": "terminal_bench_telemetry_results.json",
        "plain_summary": "A 64-step adversarial terminal session subjected to 10 tool-siege challenges including 8K git diff floods, binary dumps, infinite error loops, and corrupted terminal escapes. StrataKV maintains 88.4% failed command recovery while baseline crashes on Turn 48.",
        "failure_modes": "Binary dumps and massive git diffs pollute context memory, triggering OOM at Turn 48 in standard setups. StrataKV isolates stdout spikes into Tier-3 scratchpads.",
        "constants": "tau = 0.85, budget = 2048, turns = 64, error_recovery = 88.4%"
    },
    {
        "id": "09_perplexity_wikitext103",
        "num": "09",
        "title": "WikiText-103 Autoregressive PPL",
        "category": "Language Modeling",
        "horizon": "32,768 tokens",
        "score": "6.51 PPL (61x RAM savings)",
        "baseline": "6.42 PPL (7.1GB RAM)",
        "ttft": "40.1 ms",
        "itl": "32.9 ms (30.4 tok/s)",
        "ram": "117.4 MB",
        "energy": "125.10 mJ/token",
        "compression": "61.0x",
        "primary_json": "wikitext103_telemetry_results.json",
        "plain_summary": "Evaluates autoregressive perplexity across 32,768 tokens on WikiText-103. StrataKV matches Oracle Full Attention within +0.09 PPL (6.51 vs 6.42) while slashing memory consumption by 61.0x.",
        "failure_modes": "Aggressive token pruning degrades perplexity significantly (+1.5 to +4.0 PPL in H2O/SnapKV). StrataKV preserves continuous probability mass via golden-ratio harmonic dissipation.",
        "constants": "tau = 0.85, budget = 2048, ppl_delta = +0.09, compression = 61.0x"
    },
    {
        "id": "10_perplexity_pg19",
        "num": "10",
        "title": "PG-19 Long Narrative Books PPL",
        "category": "Book-Length PPL",
        "horizon": "65,536 tokens",
        "score": "7.24 PPL (122x RAM savings)",
        "baseline": "7.15 PPL (14.3GB RAM)",
        "ttft": "43.5 ms",
        "itl": "33.1 ms (30.2 tok/s)",
        "ram": "117.4 MB",
        "energy": "126.80 mJ/token",
        "compression": "122.1x",
        "primary_json": "pg19_telemetry_results.json",
        "plain_summary": "Tests full-length book narrative language modeling across 65,536 continuous tokens from Project Gutenberg. StrataKV maintains 7.24 PPL (+0.09 vs 7.15 Oracle) while delivering 122.1x KV memory reduction.",
        "failure_modes": "Long narrative arcs contain sprawling character references. Sliding windows induce amnesia after 4K tokens. StrataKV retains thematic invariant key representations indefinitely.",
        "constants": "tau = 0.85, budget = 2048, ppl_delta = +0.09, compression = 122.1x"
    },
    {
        "id": "11_agent_dojo",
        "num": "11",
        "title": "AgentDojo Adversarial Tool Security",
        "category": "Prompt Injection Defense",
        "horizon": "250 attack scenarios",
        "score": "2.4% ASR (32.8x reduction)",
        "baseline": "78.6% Compromised",
        "ttft": "42.8 ms",
        "itl": "33.0 ms (30.3 tok/s)",
        "ram": "117.4 MB",
        "energy": "127.30 mJ/token",
        "compression": "32.0x",
        "primary_json": "agent_dojo_telemetry_results.json",
        "plain_summary": "Subjected to 250 indirect prompt injections, tool hijacking, and data exfiltration attempts. Attack Success Rate plunges from 78.6% down to 2.4% (a 32.8x reduction) without requiring external guardrail models.",
        "failure_modes": "Adversarial tool returns inject malicious instructions that overwrite system intent in uncompressed memory. StrataKV enforces provenance quarantine via CORDIS.",
        "constants": "tau = 0.85, asr = 2.4%, benign_utility = 81.8%, defense_gain = 32.8x"
    },
    {
        "id": "12_ultra_bench",
        "num": "12",
        "title": "Ultra Bench 3,000-Step Stress Test",
        "category": "Ultra-Scale Endurance",
        "horizon": "2,025,000 cumulative tokens",
        "score": "10/10 Needles (1.11GB RAM)",
        "baseline": "OOM Crash @ Step 330",
        "ttft": "46.2 ms",
        "itl": "33.2 ms (30.1 tok/s)",
        "ram": "1.11 GB (Pure) / 0.28 GB (Elle)",
        "energy": "129.10 mJ/token",
        "compression": "389.8x – 1,545.0x",
        "primary_json": "ultra_bench_telemetry_results.json",
        "plain_summary": "A 3,000-step continuous agent simulation ingesting 2,025,000 tokens with 10 planted invariant needles. StrataKV finishes the entire 3,000-step run with 10/10 needles retrieved at Rank 1, capped at 1.11 GB RAM.",
        "failure_modes": "Monolithic uncompressed attention crashes with an Out Of Memory panic at Step 330 (demanding >432 GB RAM). Compressive baselines (FIFO, H2O, SnapKV) suffer 0.00% needle retention.",
        "constants": "tau = 0.85, steps = 3000, cumulative_tokens = 2,025,000, needles_found = 10/10"
    },
    {
        "id": "13_apple_battery",
        "num": "13",
        "title": "Apple Silicon Bare-Metal Hardware Suite",
        "category": "Bare-Metal Hardware",
        "horizon": "30 empirical repetitions",
        "score": "221.6 GB/s (0.0ms UMA)",
        "baseline": "567ms PCIe Bus Penalty",
        "ttft": "33.0 ms",
        "itl": "32.6 ms (30.7 tok/s)",
        "ram": "117.4 MB",
        "energy": "127.96 mJ/token (18.4W)",
        "compression": "61.0x",
        "primary_json": "apple_battery_telemetry_results.json",
        "plain_summary": "Bare-metal hardware validation on Apple Silicon M5 Pro Metal 3. Measures sustained GPU memory bandwidth (221.6 GB/s), zero-copy unified memory interconnects, allocator fragmentation (0.0%), and power envelope.",
        "failure_modes": "PCIe discrete GPU setups suffer massive interconnect transfer bottlenecks (567 ms penalty). Apple Silicon Unified Memory enables instant zero-copy key-value buffer pointers.",
        "constants": "gpu_bandwidth = 221.6 GB/s, peak_pct = 72.1%, zero_copy_latency = 0.0 ms"
    },
    {
        "id": "14_longmemeval",
        "num": "14",
        "title": "LongMemEval Cross-Session Agent Memory",
        "category": "Conversational Memory",
        "horizon": "500 multi-turn sessions",
        "score": "98.2% Knowledge (+8.8% gain)",
        "baseline": "89.4% Full Attention",
        "ttft": "41.9 ms",
        "itl": "32.9 ms (30.4 tok/s)",
        "ram": "117.4 MB",
        "energy": "125.70 mJ/token",
        "compression": "64.0x",
        "primary_json": "longmemeval_telemetry_results.json",
        "plain_summary": "Evaluates long-term agent memory across 500 multi-session conversations. StrataKV scores 98.2% on knowledge update fidelity (outperforming full attention's 89.4%) and achieves 99.1% negative abstention accuracy.",
        "failure_modes": "Full attention retains stale, conflicting premise tokens, causing contradictory hallucinations. StrataKV's dynamic update mechanism overwrites superseded facts cleanly.",
        "constants": "tau = 0.85, update_fidelity = 98.2%, abstention = 99.1%, sessions = 500"
    }
]

# 2. Collect all raw JSON telemetry
all_telemetry_store = {}
for meta in packages_meta:
    pkg_dir = meta["id"]
    pkg_path = os.path.join(BASE_DIR, pkg_dir)
    jsons = [f for f in os.listdir(pkg_path) if f.endswith('.json')]
    for j in jsons:
        jp = os.path.join(pkg_path, j)
        with open(jp, 'r') as fh:
            all_telemetry_store[f"{pkg_dir}/{j}"] = json.load(fh)

# Read REFEREE_REPORT.md
referee_path = os.path.join(REPO_ROOT, "REFEREE_REPORT.md")
referee_md = ""
if os.path.exists(referee_path):
    with open(referee_path, 'r') as fh:
        referee_md = fh.read()

# Clean markdown helper
def clean_markdown_to_html(md_text):
    md_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md_text)
    md_text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', md_text)
    md_text = re.sub(r'`([^`]+)`', r'<code class="mono-code">\1</code>', md_text)
    
    lines = md_text.split('\n')
    out = []
    in_table = False
    table_lines = []
    
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            out.append(f'<h1 class="report-h1">{title}</h1>')
        elif line.startswith('## '):
            title = line[3:].strip()
            out.append(f'<h2 class="report-h2"><span>§</span> {title}</h2>')
        elif line.startswith('### '):
            title = line[4:].strip()
            out.append(f'<h3 class="report-h3">{title}</h3>')
        elif line.startswith('> [!NOTE]') or line.startswith('> [!IMPORTANT]') or line.startswith('> [!TIP]'):
            out.append('<div class="callout callout-gold">')
        elif line.startswith('> '):
            content = line[2:].strip()
            if content.startswith('<strong>'):
                out.append(f'<div class="callout-header">{content}</div>')
            else:
                out.append(f'<p class="callout-text">{content}</p>')
        elif line.startswith('|') and '|' in line[1:]:
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
        else:
            if in_table:
                out.append('<div class="table-container"><table class="report-table">')
                for idx, tline in enumerate(table_lines):
                    cols = [c.strip() for c in tline.split('|')[1:-1]]
                    if idx == 0:
                        out.append('<thead><tr>' + "".join(f'<th>{c}</th>' for c in cols) + '</tr></thead><tbody>')
                    elif idx == 1 and all(set(c).issubset({'-', ':', ' '}) for c in cols):
                        continue
                    else:
                        out.append('<tr>' + "".join(f'<td>{c}</td>' for c in cols) + '</tr>')
                out.append('</tbody></table></div>')
                in_table = False
                table_lines = []
            if line.strip().startswith('- '):
                out.append(f'<li class="report-li">{line.strip()[2:]}</li>')
            elif line.strip() == '':
                out.append('<div style="height: 10px;"></div>')
            elif line.startswith('```'):
                pass
            else:
                out.append(f'<p class="report-p">{line}</p>')
    return "\n".join(out)

referee_html = clean_markdown_to_html(referee_md)

ts_content = f"""// AUTO-GENERATED TELEMETRY DATA STORE FOR REACT APP
export interface BenchmarkMeta {{
  id: string;
  num: string;
  title: string;
  category: string;
  horizon: string;
  score: string;
  baseline: string;
  ttft: string;
  itl: string;
  ram: string;
  energy: string;
  compression: string;
  primary_json: string;
  plain_summary: string;
  failure_modes: string;
  constants: string;
}}

export const PACKAGES_META: BenchmarkMeta[] = {json.dumps(packages_meta, indent=2)};

export const ALL_TELEMETRY_STORE: Record<string, any> = {json.dumps(all_telemetry_store, indent=2)};

export const REFEREE_REPORT_HTML: string = {json.dumps(referee_html)};
"""

with open(OUT_FILE, 'w') as fh:
    fh.write(ts_content)

print(f"Generated {OUT_FILE} ({os.path.getsize(OUT_FILE)/1024:.1f} KB).")
