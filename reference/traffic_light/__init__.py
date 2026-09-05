"""Reference belief-state control package for the World Engine research note.

The package is a deliberately bounded, dependency-free POMDP-style toy model.
It is not a traffic-control product, autonomous-driving system, or model of
human behaviour.
"""

from .evaluation import ExperimentConfig, compare_policies
from .model import Observation, PhasePolicy
from .policies import BeliefStatePolicy, HistoryReplayPolicy

__all__ = [
    "BeliefStatePolicy",
    "ExperimentConfig",
    "HistoryReplayPolicy",
    "Observation",
    "PhasePolicy",
    "compare_policies",
]
