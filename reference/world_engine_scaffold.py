"""Illustrative World Engine interfaces.

This dependency-free scaffold is not a trained model or production code. It
implements a small, inspectable version of candidate-conditioned transition and
multi-objective trajectory scoring described in the research paper.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Iterable, Mapping


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


@dataclass(frozen=True)
class Signal:
    """A predictive event-field pattern with explicit uncertainty."""

    name: str
    strength: float
    persistence: float
    specificity: float
    confidence: float

    @property
    def effective_strength(self) -> float:
        return _clip(
            self.strength
            * self.persistence
            * self.specificity
            * self.confidence
        )


@dataclass(frozen=True)
class MindState:
    """A compact example of typed, behaviorally relevant state."""

    attention: float = 0.5
    novelty: float = 0.5
    value: float = 0.5
    goal_activation: float = 0.5
    context_fit: float = 0.5
    saturation: float = 0.0
    uncertainty: float = 0.5


@dataclass(frozen=True)
class Candidate:
    """A candidate item represented by its possible state effects."""

    identifier: str
    signal: Signal
    effects: Mapping[str, float]
    diversity: float = 0.0
    risk: float = 0.0


@dataclass(frozen=True)
class WorldState:
    """A minimal population-level context used during scoring."""

    interaction_potential: float = 0.5
    exposure_concentration: float = 0.0


@dataclass(frozen=True)
class TrajectoryValue:
    immediate_relevance: float
    delayed_value: float
    information_gain: float
    diversity: float
    ecosystem_value: float
    risk_penalty: float

    @property
    def total(self) -> float:
        return (
            0.30 * self.immediate_relevance
            + 0.25 * self.delayed_value
            + 0.15 * self.information_gain
            + 0.10 * self.diversity
            + 0.20 * self.ecosystem_value
            - 0.30 * self.risk_penalty
        )


def transition(state: MindState, candidate: Candidate) -> MindState:
    """Apply one uncertainty-gated, candidate-conditioned state transition."""

    evidence = candidate.signal.effective_strength
    gate = evidence * (1.0 - 0.5 * state.uncertainty)
    values = {field.name: getattr(state, field.name) for field in fields(state)}

    for dimension, effect in candidate.effects.items():
        if dimension not in values or dimension == "uncertainty":
            raise ValueError(f"Unknown or protected state dimension: {dimension}")
        values[dimension] = _clip(values[dimension] + gate * effect)

    values["uncertainty"] = _clip(state.uncertainty * (1.0 - 0.35 * evidence))
    return MindState(**values)


def evaluate_trajectory(
    before: MindState,
    after: MindState,
    candidate: Candidate,
    world: WorldState,
) -> TrajectoryValue:
    """Score a possible successor state under an explicit objective."""

    immediate = (
        0.35 * after.attention
        + 0.35 * after.value
        + 0.30 * after.context_fit
    )
    delayed = (
        0.40 * after.goal_activation
        + 0.30 * after.novelty
        + 0.30 * (1.0 - after.saturation)
    )
    information_gain = _clip(before.uncertainty - after.uncertainty)
    ecosystem = _clip(
        world.interaction_potential
        * (1.0 - 0.5 * world.exposure_concentration)
    )
    return TrajectoryValue(
        immediate_relevance=immediate,
        delayed_value=delayed,
        information_gain=information_gain,
        diversity=_clip(candidate.diversity),
        ecosystem_value=ecosystem,
        risk_penalty=_clip(candidate.risk),
    )


def rank_candidates(
    state: MindState,
    world: WorldState,
    candidates: Iterable[Candidate],
) -> list[tuple[Candidate, MindState, TrajectoryValue]]:
    """Rank candidates by expected trajectory value."""

    evaluated = []
    for candidate in candidates:
        successor = transition(state, candidate)
        value = evaluate_trajectory(state, successor, candidate, world)
        evaluated.append((candidate, successor, value))
    return sorted(evaluated, key=lambda item: item[2].total, reverse=True)


def example() -> None:
    state = MindState(attention=0.42, novelty=0.65, saturation=0.72)
    world = WorldState(interaction_potential=0.61, exposure_concentration=0.34)
    candidates = [
        Candidate(
            identifier="semantic-repetition",
            signal=Signal("topic affinity", 0.80, 0.75, 0.60, 0.80),
            effects={"attention": 0.05, "value": 0.06, "saturation": 0.18},
            diversity=0.10,
        ),
        Candidate(
            identifier="state-compatible-discovery",
            signal=Signal("contextual novelty", 0.82, 0.68, 0.78, 0.76),
            effects={
                "attention": 0.18,
                "novelty": 0.12,
                "context_fit": 0.16,
                "saturation": -0.22,
            },
            diversity=0.72,
        ),
    ]

    for candidate, successor, value in rank_candidates(state, world, candidates):
        print(
            f"{candidate.identifier}: score={value.total:.3f}, "
            f"attention={successor.attention:.3f}, "
            f"saturation={successor.saturation:.3f}"
        )


if __name__ == "__main__":
    example()
