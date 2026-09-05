"""Deterministic-seed synthetic crossing environment for paired evaluation."""

from __future__ import annotations

from random import Random

from .model import CarResponse, Episode, LatentCrossingState, Observation, PhasePolicy, RiderResponse


def designed_cost(action: PhasePolicy, state: LatentCrossingState) -> float:
    """Fixed loss table: conflict is expensive; clearance has delay cost.

    These values encode the research note's toy assumptions.  They have no
    physical units and must not be interpreted as accident likelihoods.
    """

    conflict = state.car is CarResponse.PROCEED and state.rider is RiderResponse.LAUNCH_EARLY
    if action is PhasePolicy.SWITCH_NORMALLY:
        return 10.0 if conflict else 0.4
    if action is PhasePolicy.ADD_CLEARANCE:
        return 2.0 if conflict else 0.8
    if action is PhasePolicy.HOLD_GREEN:
        return 1.0 if state.car is CarResponse.PROCEED else 1.6
    raise ValueError(f"Unknown action: {action}")


class SyntheticCrossing:
    """Reproducible generator of designed latent states and noisy observations."""

    def __init__(self, seed: int) -> None:
        self._rng = Random(seed)

    def sample(self) -> tuple[LatentCrossingState, Observation]:
        state = LatentCrossingState(
            car=CarResponse.PROCEED if self._rng.random() < 0.42 else CarResponse.BRAKE,
            rider=RiderResponse.LAUNCH_EARLY if self._rng.random() < 0.26 else RiderResponse.WAIT,
        )
        observation = Observation(
            approach_speed="high"
            if self._rng.random() < (0.82 if state.car is CarResponse.PROCEED else 0.18)
            else "low",
            launch_cue=self._rng.random() < (0.78 if state.rider is RiderResponse.LAUNCH_EARLY else 0.22),
        )
        return state, observation

    def realise(self, action: PhasePolicy) -> Episode:
        state, observation = self.sample()
        return Episode(state, observation, action, designed_cost(action, state))
