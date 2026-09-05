"""Bayesian belief update used by the reference controller."""

from __future__ import annotations

from collections.abc import Mapping

from .model import CarResponse, LATENT_STATES, LatentCrossingState, Observation, RiderResponse

Belief = dict[LatentCrossingState, float]


def uniform_prior() -> Belief:
    """An explicitly uninformative prior over the four designed latent states."""

    return {state: 1.0 / len(LATENT_STATES) for state in LATENT_STATES}


def normalise(weights: Mapping[LatentCrossingState, float]) -> Belief:
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Belief weights must have positive total probability")
    return {state: value / total for state, value in weights.items()}


def observation_likelihood(observation: Observation, state: LatentCrossingState) -> float:
    """Fixed emission model, selected only for the toy experiment.

    The two cues are conditionally independent given the latent response pair.
    This is a modelling assumption, not an empirical claim.
    """

    speed_agrees = (observation.approach_speed == "high") == (state.car is CarResponse.PROCEED)
    launch_agrees = observation.launch_cue == (state.rider is RiderResponse.LAUNCH_EARLY)
    return (0.82 if speed_agrees else 0.18) * (0.78 if launch_agrees else 0.22)


def update_belief(observation: Observation, prior: Mapping[LatentCrossingState, float] | None = None) -> Belief:
    """Return P(z | o) for the current observation under the fixed toy model."""

    starting_belief = uniform_prior() if prior is None else prior
    return normalise(
        {state: starting_belief[state] * observation_likelihood(observation, state) for state in LATENT_STATES}
    )


def entropy(belief: Mapping[LatentCrossingState, float]) -> float:
    """Shannon entropy in bits, included to make residual uncertainty visible."""

    from math import log2

    return -sum(probability * log2(probability) for probability in belief.values() if probability > 0)
