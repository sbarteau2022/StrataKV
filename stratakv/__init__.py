"""
StrataKV: The 3-Tier Breathing KV Cache for Apple Silicon & Autonomous Agents
=============================================================================
"""

from .block import StrataBlock
from .cache import StrataKVCache
from .profiler import KappaProfiler, PHI, TWISTOR_C, KAPPA_CORE
from .rope import compute_rope_embeddings
from .predict import PredictionOperator
from .runbook import AgenticRunbook, RunbookPhase, Intervention, ProvenanceQuarantine

__version__ = "1.0.0"
__all__ = [
    "StrataBlock",
    "StrataKVCache",
    "KappaProfiler",
    "compute_rope_embeddings",
    "PredictionOperator",
    "AgenticRunbook",
    "RunbookPhase",
    "Intervention",
    "ProvenanceQuarantine",
    "PHI",
    "TWISTOR_C",
    "KAPPA_CORE",
]
