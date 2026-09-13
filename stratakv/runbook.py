"""
StrataKV Agentic AI Runbook Engine (AI_KV + CORDIS)
===================================================
Realizes the complete 5-Phase Agentic AI Runbook architecture:
  Phase 1: Foundation Intake (Zero-Shot / Low-Rank, Coordinator only)
  Phase 2: Mid-Tier Execution (Freeze Tier 1 KV, Sub-Atlas Isolation, Provenance Quarantine)
  Phase 3: High-Tier Reasoning & Superposition Holding Engine (Active Inference Steering)
  Phase 4: Computational Sleep & Dissolution (Fibonacci Consolidation, 2% Milankovitch Leak)
  Phase 5: Master Atlas Distillation (Riemannian M = H^n x T^n Projection)

Author: Stewart Barteau & Claude (Anthropic)
Date: September 2026
License: Apache-2.0
"""

import math
from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
import numpy as np

from .profiler import KappaProfiler, KAPPA_CORE, TWISTOR_C, PHI
from .predict import PredictionOperator
from .cache import StrataKVCache


class RunbookPhase(IntEnum):
    """The 5 canonical operational phases of the Agentic AI Runbook."""
    FOUNDATION_INTAKE = 1       # Phase 1: Intake root constraints (Tier 1 writeable)
    MID_TIER_EXECUTION = 2      # Phase 2: Freeze Tier 1, sub-agent isolation, CORDIS quarantine
    HIGH_TIER_REASONING = 3     # Phase 3: Active inference steering, superposition holding
    COMPUTATIONAL_SLEEP = 4     # Phase 4: Fibonacci consolidation, 2% Milankovitch leak
    ATLAS_DISTILLATION = 5      # Phase 5: Projection into Master Atlas coordinates (H^n x T^n)


# Canonical Fibonacci Consolidation Milestones
FIBONACCI_SLEEP_STEPS: Set[int] = {
    8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181
}

# CORDIS Quarantine Silos (Tool Execution Streams)
QUARANTINE_SILO_IDS: Set[int] = {8, 9, 10, 11, 12}

# Known noisy tool tags requiring immediate provenance quarantine
QUARANTINE_TOOL_TAGS: Set[str] = {
    "compiler_stderr", "compiler_noise", "tool_stderr", "tool_stdout",
    "terminal_exec", "json_payload", "core_dump", "stack_trace",
    "git_diff", "linter_warning", "ast_dump", "curl_output"
}


@dataclass
class Intervention:
    """Active inference intervention signal for agent execution steering."""
    action: str                 # "CONTINUE", "NUDGE", "KILL"
    kappa: float                # Instantaneous coherence curvature in (0, 1)
    distance: float             # Hyperbolic geodesic distance from root goal
    confidence: float           # Composite confidence: kappa * exp(-min(d, 5.0))
    spend_tokens: int           # Cumulative tokens spent by agent
    predicted_tokens: int       # Predicted token ceiling from PredictionOperator P
    delta_rate: float           # Progress velocity (positive = advancing, <=0 = stalling)
    reason: str                 # Human/agent readable rationale for telemetry
    superposition_active: bool  # True if candidate hypotheses are held in superposition
    step: int = 0               # Step at which intervention was evaluated


@dataclass
class SuperpositionBundle:
    """Uncollapsed superposition bundle holding candidate reasoning branches."""
    status: str
    num_hypotheses: int
    branch_distribution: List[float]
    active: bool
    guidance: str
    collapsed_branch_id: Optional[int] = None
    metrics: Optional[Dict[str, Any]] = None


class ProvenanceQuarantine:
    """
    CORDIS Provenance Quarantine Engine.
    Enforces strict physical boundary protection between external untrusted tool
    execution streams (Silos 8-12) and the immutable Tier 1 Invariant Core.
    Defuses the Embedding Hijacking Attack discovered in multi-turn agent benchmarks.
    """
    def __init__(self, quarantine_silos: Optional[Set[int]] = None):
        self.quarantine_silos = quarantine_silos or QUARANTINE_SILO_IDS
        self.quarantined_count: int = 0
        self.quarantined_tokens: int = 0

    def inspect_and_classify(
        self,
        source_tag: str,
        turn_id: Optional[int] = None,
        silo_id: Optional[int] = None,
        is_tool_output: bool = False,
        requested_tier: int = 3
    ) -> Tuple[int, bool]:
        """
        Inspects provenance tags and enforces quarantine policy.
        Returns:
            Tuple[int, bool]: (assigned_tier, is_quarantined)
        """
        tag_lower = source_tag.lower()
        is_quarantine_tag = any(q in tag_lower for q in QUARANTINE_TOOL_TAGS)
        is_quarantine_silo = silo_id is not None and silo_id in self.quarantine_silos

        if is_tool_output or is_quarantine_tag or is_quarantine_silo:
            self.quarantined_count += 1
            # External tool output is strictly quarantined to Tier 2 or Tier 3.
            # It CANNOT be enrolled into Tier 1 regardless of embedding similarity!
            assigned_tier = max(requested_tier, 2)
            return assigned_tier, True

        return requested_tier, False


class AgenticRunbook:
    """
    The Agentic AI Runbook Controller.
    Orchestrates the 5-phase lifecycle over StrataKVCache, coupling:
      1. Progressive Stratified Freezing
      2. CORDIS Provenance Quarantine
      3. Active Inference Steering (Prediction Operator P + Profiler)
      4. Superposition Holding Engine (Low kappa, High d)
      5. Fibonacci Consolidation Cycles (2% Milankovitch Dissolution Leak)
      6. Master Atlas Distillation (H^n x T^n)
    """
    def __init__(
        self,
        cache: StrataKVCache,
        goal_vector: Optional[np.ndarray] = None,
        coordinator_id: int = 0,
        leak_rate: float = 0.020,
        drift_distance_threshold: float = 1.2,
        drift_kappa_threshold: float = 0.65
    ):
        self.cache = cache
        self.coordinator_id = coordinator_id
        self.leak_rate = leak_rate
        self.drift_distance_threshold = drift_distance_threshold
        self.drift_kappa_threshold = drift_kappa_threshold

        self.phase: RunbookPhase = RunbookPhase.FOUNDATION_INTAKE
        self.step_count: int = 0
        self.cumulative_tokens_spent: int = 0

        # Subsystems
        self.quarantine = ProvenanceQuarantine()
        self.predictor = PredictionOperator()
        self.profiler = KappaProfiler(goal_vector=goal_vector)

        # Audit and telemetry ledger
        self.intervention_history: List[Intervention] = []
        self.phase_transitions: List[Tuple[int, RunbookPhase, str]] = [
            (0, RunbookPhase.FOUNDATION_INTAKE, "Initialized Runbook in Phase 1 Intake")
        ]
        self.superposition_bundle: Optional[SuperpositionBundle] = None

    def set_phase(self, phase: RunbookPhase | int, reason: str = "") -> None:
        """
        Transitions the agent to a new runbook phase and applies tier freezing.
        """
        old_phase = self.phase
        self.phase = RunbookPhase(phase)
        self.cache.set_phase(int(self.phase))
        msg = reason or f"Transitioned from {old_phase.name} to {self.phase.name}"
        self.phase_transitions.append((self.step_count, self.phase, msg))

    def inhale(
        self,
        k: np.ndarray,
        v: np.ndarray,
        start_pos: int,
        source_tag: str,
        is_needle: bool = False,
        turn_id: Optional[int] = None,
        is_tool_output: bool = False,
        silo_id: Optional[int] = None,
        surprisal: Optional[float] = None
    ) -> int:
        """
        Intake token representations under CORDIS Provenance Quarantine.
        Prevents tool noise and adversarial decoys from polluting Tier 1.
        """
        num_tokens = k.shape[0]
        self.cumulative_tokens_spent += num_tokens

        # Enforce quarantine classification
        target_tier = 1 if (is_needle and self.phase == RunbookPhase.FOUNDATION_INTAKE) else 3
        assigned_tier, quarantined = self.quarantine.inspect_and_classify(
            source_tag=source_tag,
            turn_id=turn_id,
            silo_id=silo_id,
            is_tool_output=is_tool_output,
            requested_tier=target_tier
        )

        # If quarantined, is_needle is overridden to False
        effective_needle = is_needle and (not quarantined)

        # Inhale into physical StrataKV Cache
        active_count = self.cache.inhale(
            k=k,
            v=v,
            start_pos=start_pos,
            source_tag=source_tag,
            is_needle=effective_needle,
            turn_id=turn_id,
            surprisal=surprisal
        )

        return active_count

    def step(
        self,
        k: np.ndarray,
        step_spend: int = 0,
        delta_rate: float = 1.0,
        source_tag: str = "agent_step",
        token_budget: Optional[int] = None
    ) -> Intervention:
        """
        Advances the agent runbook by one execution step:
          1. Updates Prediction Operator P to forecast token envelope.
          2. Profiles instantaneous curvature kappa and hyperbolic distance d.
          3. Evaluates Active Inference tripartite policy (CONTINUE, NUDGE, KILL).
          4. Checks Fibonacci consolidation intervals for computational sleep.
        """
        self.step_count += 1
        spend = self.cumulative_tokens_spent + step_spend

        # Predict token spend envelope using PredictionOperator
        pred_res = self.predictor.step(np.array([float(spend)], dtype=np.float32))
        pred_env = pred_res.get("predicted_envelope")
        predicted_ceiling = token_budget if token_budget is not None else (int(pred_env) if pred_env is not None else int(spend * 1.5))

        # Profile curvature kappa and hyperbolic distance d_H
        kappa, dist = self.profiler.profile_step(k, source_tag=source_tag)

        # Active Inference Decision Policy:
        # 1. KILL: Budget exceeded and velocity stagnant or negative
        if spend > predicted_ceiling and delta_rate <= 0.0:
            action = "KILL"
            reason = (
                f"Thermodynamic token budget exceeded ({spend} > {predicted_ceiling}) "
                f"with stalled/negative progress velocity (delta={delta_rate:.2f})."
            )
            superposition_req = False

        # 2. NUDGE: Trajectory drift detected (Low kappa, High d)
        elif kappa < self.drift_kappa_threshold and dist >= self.drift_distance_threshold:
            action = "NUDGE"
            reason = (
                f"Semantic drift detected (kappa={kappa:.3f} < {self.drift_kappa_threshold}, "
                f"distance={dist:.3f} >= {self.drift_distance_threshold}). "
                f"Holding Superposition active; dispatching 2-way scratchboard nudge."
            )
            superposition_req = True

        # 3. CONTINUE: Coherent forward progress
        else:
            action = "CONTINUE"
            reason = f"Stable alignment (kappa={kappa:.3f}, distance={dist:.3f}, progress={delta_rate:.2f})."
            superposition_req = False

        confidence = float(kappa * math.exp(-min(dist, 5.0)))
        intervention = Intervention(
            action=action,
            kappa=kappa,
            distance=dist,
            confidence=confidence,
            spend_tokens=spend,
            predicted_tokens=predicted_ceiling,
            delta_rate=delta_rate,
            reason=reason,
            superposition_active=superposition_req,
            step=self.step_count
        )
        self.intervention_history.append(intervention)

        # Check for automatic Fibonacci computational sleep
        if self.step_count in FIBONACCI_SLEEP_STEPS:
            self.execute_computational_sleep(step=self.step_count)

        return intervention

    def hold_superposition(
        self,
        candidate_trajectories: List[np.ndarray]
    ) -> SuperpositionBundle:
        """
        Superposition Holding Unified Function:
        Holds candidate hypothesis trajectories Psi = sum c_m |h_m> in equilibrium
        under Low kappa, High d ambiguity, preventing premature collapse and
        destructive token thrashing.
        """
        if not candidate_trajectories:
            bundle = SuperpositionBundle(
                status="EMPTY",
                num_hypotheses=0,
                branch_distribution=[],
                active=False,
                guidance="No candidate branches supplied to superposition engine."
            )
            self.superposition_bundle = bundle
            return bundle

        branch_metrics = []
        for idx, cand_k in enumerate(candidate_trajectories):
            k_score, d_score = self.profiler.profile_step(cand_k, source_tag="superposition_branch")
            branch_metrics.append({
                "branch_id": idx,
                "kappa": k_score,
                "distance": d_score,
                "weight": math.exp(-d_score) * k_score
            })

        total_weight = sum(m["weight"] for m in branch_metrics)
        normalized_weights = [m["weight"] / max(total_weight, 1e-12) for m in branch_metrics]
        best_idx = int(np.argmax(normalized_weights))
        best_branch = branch_metrics[best_idx]

        if best_branch["kappa"] >= self.drift_kappa_threshold and best_branch["distance"] < self.drift_distance_threshold:
            bundle = SuperpositionBundle(
                status="COLLAPSED",
                num_hypotheses=len(candidate_trajectories),
                branch_distribution=normalized_weights,
                active=False,
                guidance="Coherence restored. Collapse superposition and resume forward execution.",
                collapsed_branch_id=best_idx,
                metrics=best_branch
            )
        else:
            bundle = SuperpositionBundle(
                status="HOLDING_SUPERPOSITION",
                num_hypotheses=len(candidate_trajectories),
                branch_distribution=normalized_weights,
                active=True,
                guidance="Ambiguity remains. Maintain uncollapsed superposition; await 2-way scratchboard resolution.",
                metrics=best_branch
            )

        self.superposition_bundle = bundle
        return bundle

    def execute_computational_sleep(self, step: Optional[int] = None) -> Dict[str, Any]:
        """
        Phase 4: Computational Sleep & Dissolution.
        Applies the 2% Milankovitch dissolution leak (L_leak = 0.020) and consolidates
        Tier 2 harmonic representations, releasing transient noise into thermodynamic vacuum.
        """
        prev_tokens = self.cache.active_tokens
        # Trigger cache exhale pass
        self.cache.exhale(turn_id=step or self.step_count, force_fibonacci=True)
        now_tokens = self.cache.active_tokens

        report = {
            "step": step or self.step_count,
            "leak_rate": self.leak_rate,
            "tokens_before": prev_tokens,
            "tokens_after": now_tokens,
            "purged_noise_tokens": max(0, prev_tokens - now_tokens),
            "status": "CONSOLIDATED_SLOW_WAVE_SLEEP"
        }
        return report

    def distill(self, failure_branches: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Phase 5: Master Atlas Distillation.
        Projects surviving invariants and negative curvature boundaries into
        Riemannian product manifold M = H^n x T^n.
        """
        self.set_phase(RunbookPhase.ATLAS_DISTILLATION, reason="Final task distillation")
        return self.cache.distill_to_master_atlas(failure_branches=failure_branches)

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns comprehensive telemetry audit logs of the runbook session."""
        interventions_summary = {"CONTINUE": 0, "NUDGE": 0, "KILL": 0}
        for iv in self.intervention_history:
            interventions_summary[iv.action] = interventions_summary.get(iv.action, 0) + 1

        return {
            "current_phase": self.phase.name,
            "total_steps": self.step_count,
            "cumulative_tokens_spent": self.cumulative_tokens_spent,
            "active_retained_tokens": self.cache.active_tokens,
            "quarantined_tool_streams": self.quarantine.quarantined_count,
            "intervention_counts": interventions_summary,
            "phase_transitions": self.phase_transitions,
            "superposition_status": self.superposition_bundle.status if self.superposition_bundle else "INACTIVE"
        }
