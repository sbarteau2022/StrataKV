"""
Unit Tests for StrataKV Agentic AI Runbook (AI_KV + CORDIS)
============================================================
Verifies:
  1. Phase transitions and progressive tier freezing.
  2. CORDIS Provenance Quarantine against tool flooding and adversarial decoys.
  3. Active inference tripartite intervention policy (CONTINUE, NUDGE, KILL).
  4. Superposition Holding Engine under low kappa, high d ambiguity.
  5. Fibonacci computational sleep cycles with 2% Milankovitch leak.
  6. Master Atlas Distillation (H^n x T^n).
  7. Full telemetry and audit trail.
"""

import unittest
import numpy as np
import math

from stratakv import (
    StrataKVCache,
    AgenticRunbook,
    RunbookPhase,
    Intervention,
    ProvenanceQuarantine,
    KAPPA_CORE,
    TWISTOR_C,
    PHI
)


class TestAgenticRunbook(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        self.head_dim = 64
        self.num_heads = 4
        self.goal_vec = np.random.randn(self.head_dim).astype(np.float32)
        self.goal_vec /= np.linalg.norm(self.goal_vec)

        self.cache = StrataKVCache(
            max_active_budget=1024,
            head_dim=self.head_dim,
            num_heads=self.num_heads,
            goal_vector=self.goal_vec,
            dissolution_leak_rate=0.020
        )
        self.runbook = AgenticRunbook(
            cache=self.cache,
            goal_vector=self.goal_vec,
            leak_rate=0.020
        )

    def test_initial_state_phase_1(self):
        """Verify Runbook starts in Phase 1 Intake."""
        self.assertEqual(self.runbook.phase, RunbookPhase.FOUNDATION_INTAKE)
        self.assertEqual(self.runbook.step_count, 0)
        self.assertEqual(self.runbook.quarantine.quarantined_count, 0)

    def test_phase_transitions_and_tier_freezing(self):
        """Verify progressive freezing policy across phases."""
        # Inhale root invariant in Phase 1
        k_root = np.random.randn(64, self.num_heads, self.head_dim).astype(np.float32)
        v_root = np.random.randn(64, self.num_heads, self.head_dim).astype(np.float32)
        self.runbook.inhale(k_root, v_root, start_pos=0, source_tag="root_prompt", is_needle=True)

        # In Phase 1, block is not yet frozen
        self.assertTrue(len(self.cache.blocks) > 0)
        self.assertFalse(self.cache.blocks[0].frozen)

        # Transition to Phase 2: Mid-Tier Execution
        self.runbook.set_phase(RunbookPhase.MID_TIER_EXECUTION)
        self.assertEqual(self.runbook.phase, RunbookPhase.MID_TIER_EXECUTION)
        # Tier 1 blocks must now be frozen!
        self.assertTrue(self.cache.blocks[0].frozen)

        # Transition to Phase 3: High-Tier Reasoning
        self.runbook.set_phase(RunbookPhase.HIGH_TIER_REASONING)
        self.assertEqual(self.runbook.phase, RunbookPhase.HIGH_TIER_REASONING)

    def test_cordis_provenance_quarantine(self):
        """Verify that compiler stderr and tool outputs are quarantined from Tier 1."""
        self.runbook.set_phase(RunbookPhase.MID_TIER_EXECUTION)

        # 1. Benign tool output with compiler_stderr tag
        k_tool = np.random.randn(128, self.num_heads, self.head_dim).astype(np.float32)
        v_tool = np.random.randn(128, self.num_heads, self.head_dim).astype(np.float32)

        # Even if someone claims is_needle=True, quarantine must intercept it!
        self.runbook.inhale(
            k=k_tool,
            v=v_tool,
            start_pos=64,
            source_tag="compiler_stderr_dump",
            is_needle=True,
            is_tool_output=True
        )

        self.assertGreater(self.runbook.quarantine.quarantined_count, 0)
        # Verify the quarantined block was NOT assigned to Tier 1
        tool_block = self.cache.blocks[-1]
        self.assertNotEqual(tool_block.tier, 1)
        self.assertIn(tool_block.tier, [2, 3])

        # 2. Inhale from Silo 9 (Silos 8-12 are quarantine silos)
        k_silo = np.random.randn(64, self.num_heads, self.head_dim).astype(np.float32)
        v_silo = np.random.randn(64, self.num_heads, self.head_dim).astype(np.float32)
        self.runbook.inhale(
            k=k_silo,
            v=v_silo,
            start_pos=192,
            source_tag="api_response",
            silo_id=9
        )
        self.assertEqual(self.runbook.quarantine.quarantined_count, 2)

    def test_active_inference_intervention_policy(self):
        """Verify CONTINUE, NUDGE, and KILL decisions."""
        self.runbook.set_phase(RunbookPhase.HIGH_TIER_REASONING)

        # 1. Coherent step: aligned with goal vector
        k_aligned = np.tile(self.goal_vec, (16, self.num_heads, 1)).astype(np.float32)
        iv1 = self.runbook.step(k_aligned, step_spend=16, delta_rate=1.0)
        self.assertEqual(iv1.action, "CONTINUE")
        self.assertFalse(iv1.superposition_active)
        self.assertGreater(iv1.confidence, 0.0)

        # 2. Drifting step: orthogonal/opposed to goal (low kappa, high distance)
        k_drift = -np.tile(self.goal_vec, (16, self.num_heads, 1)).astype(np.float32)
        iv2 = self.runbook.step(k_drift, step_spend=16, delta_rate=0.2)
        self.assertEqual(iv2.action, "NUDGE")
        self.assertTrue(iv2.superposition_active)
        self.assertIn("drift", iv2.reason.lower())

        # 3. Budget exhaustion with stalled progress: KILL
        # Artificially push spend way above predicted ceiling
        self.runbook.cumulative_tokens_spent = 50000
        iv3 = self.runbook.step(k_drift, step_spend=100, delta_rate=-0.5, token_budget=40000)
        self.assertEqual(iv3.action, "KILL")
        self.assertIn("budget exceeded", iv3.reason.lower())

    def test_superposition_holding_engine(self):
        """Verify holding candidate hypotheses in superposition and collapsing upon alignment."""
        # Generate 3 candidate trajectory heads
        cand1 = np.random.randn(16, self.num_heads, self.head_dim).astype(np.float32)
        cand2 = np.random.randn(16, self.num_heads, self.head_dim).astype(np.float32)
        cand3 = np.tile(self.goal_vec, (16, self.num_heads, 1)).astype(np.float32) # Aligned!

        # When candidates have high drift (exclude cand3)
        bundle_drift = self.runbook.hold_superposition([cand1, cand2])
        self.assertEqual(bundle_drift.status, "HOLDING_SUPERPOSITION")
        self.assertTrue(bundle_drift.active)
        self.assertEqual(bundle_drift.num_hypotheses, 2)
        self.assertEqual(len(bundle_drift.branch_distribution), 2)

        # When candidate 3 (aligned) is introduced, it should trigger collapse
        bundle_resolve = self.runbook.hold_superposition([cand1, cand2, cand3])
        self.assertEqual(bundle_resolve.status, "COLLAPSED")
        self.assertFalse(bundle_resolve.active)
        self.assertEqual(bundle_resolve.collapsed_branch_id, 2) # cand3 had highest alignment

    def test_fibonacci_computational_sleep(self):
        """Verify that step counts matching Fibonacci numbers trigger sleep consolidation."""
        # Add transient noise tokens
        k_noise = np.random.randn(512, self.num_heads, self.head_dim).astype(np.float32)
        v_noise = np.random.randn(512, self.num_heads, self.head_dim).astype(np.float32)
        self.runbook.inhale(k_noise, v_noise, start_pos=0, source_tag="compiler_noise")

        # Explicitly run sleep
        report = self.runbook.execute_computational_sleep(step=8)
        self.assertEqual(report["status"], "CONSOLIDATED_SLOW_WAVE_SLEEP")
        self.assertEqual(report["leak_rate"], 0.020)
        self.assertGreaterEqual(report["tokens_before"], report["tokens_after"])

    def test_master_atlas_distillation(self):
        """Verify Phase 5 Master Atlas distillation output."""
        # Inhale an invariant
        k_inv = np.random.randn(32, self.num_heads, self.head_dim).astype(np.float32)
        v_inv = np.random.randn(32, self.num_heads, self.head_dim).astype(np.float32)
        self.runbook.inhale(k_inv, v_inv, start_pos=0, source_tag="system_spec", is_needle=True)

        failures = [{"task": "compile_c", "error": "Undefined symbol _main", "barrier_curvature": -1.5}]
        distilled = self.runbook.distill(failure_branches=failures)

        self.assertEqual(self.runbook.phase, RunbookPhase.ATLAS_DISTILLATION)
        self.assertEqual(distilled["manifold"], "H^n x T^n")
        self.assertEqual(distilled["status"], "CONSOLIDATED")
        self.assertGreater(len(distilled["crystallized_invariants"]), 0)
        self.assertEqual(len(distilled["negative_curvature_barriers"]), 1)

    def test_telemetry_ledger(self):
        """Verify telemetry ledger contains accurate audit data."""
        k = np.random.randn(16, self.num_heads, self.head_dim).astype(np.float32)
        self.runbook.step(k, step_spend=16, delta_rate=1.0)
        self.runbook.step(k, step_spend=16, delta_rate=1.0)

        telem = self.runbook.get_telemetry()
        self.assertEqual(telem["total_steps"], 2)
        self.assertEqual(telem["current_phase"], "FOUNDATION_INTAKE")
        self.assertIn("CONTINUE", telem["intervention_counts"])
        self.assertGreaterEqual(len(telem["phase_transitions"]), 1)


if __name__ == "__main__":
    unittest.main()
