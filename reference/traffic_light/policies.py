"""Baselines and an uncertainty-aware policy for the fixed toy environment."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping

from .environment import designed_cost
from .inference import Belief, entropy, update_belief
from .model import LATENT_STATES, Observation, PhasePolicy


class Policy(ABC):
    """Shared policy interface to keep the evaluation paired and inspectable."""

    name: str

    @abstractmethod
    def choose(self, observation: Observation) -> PhasePolicy:
        """Select a phase action given the currently available observation."""


class HistoryReplayPolicy(Policy):
    """A deliberately weak baseline that overweights one current cue.

    It represents a design that treats a single observable trace as sufficient,
    rather than preserving uncertainty over the response pair.
    """

    name = "single-signal replay"

    def choose(self, observation: Observation) -> PhasePolicy:
        return PhasePolicy.HOLD_GREEN if observation.approach_speed == "high" else PhasePolicy.SWITCH_NORMALLY


class ConservativePolicy(Policy):
    """A policy that always holds green, illustrating the cost of over-caution."""

    name = "always hold green"

    def choose(self, observation: Observation) -> PhasePolicy:  # noqa: ARG002
        return PhasePolicy.HOLD_GREEN


class BeliefStatePolicy(Policy):
    """Minimise expected cost under a posterior over latent response pairs."""

    name = "belief-state control"

    def belief(self, observation: Observation) -> Belief:
        return update_belief(observation)

    def expected_cost(self, action: PhasePolicy, belief: Mapping = None) -> float:
        current = belief if belief is not None else update_belief(Observation("low", False))
        return sum(probability * designed_cost(action, state) for state, probability in current.items())

    def choose(self, observation: Observation) -> PhasePolicy:
        current = self.belief(observation)
        return min(PhasePolicy, key=lambda action: self.expected_cost(action, current))

    def diagnostics(self, observation: Observation) -> dict[str, float | str]:
        current = self.belief(observation)
        return {
            "action": self.choose(observation).value,
            "belief_entropy_bits": round(entropy(current), 4),
            **{f"p_{state.car.value}_{state.rider.value}": round(current[state], 4) for state in LATENT_STATES},
        }
