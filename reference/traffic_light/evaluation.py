"""Paired, repeatable evaluation for the toy crossing reference package."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Iterable

from .environment import SyntheticCrossing, designed_cost
from .model import CarResponse, PhasePolicy, RiderResponse
from .policies import BeliefStatePolicy, ConservativePolicy, HistoryReplayPolicy, Policy


@dataclass(frozen=True)
class ExperimentConfig:
    seeds: tuple[int, ...] = tuple(range(20))
    episodes_per_seed: int = 1_000

    def __post_init__(self) -> None:
        if not self.seeds:
            raise ValueError("at least one seed is required")
        if self.episodes_per_seed <= 0:
            raise ValueError("episodes_per_seed must be positive")


@dataclass(frozen=True)
class PolicyMetrics:
    policy: str
    mean_designed_cost: float
    mean_high_conflict_rate: float
    mean_clearance_rate: float

    def as_dict(self) -> dict[str, float | str]:
        return asdict(self)


def evaluate_policy(policy: Policy, config: ExperimentConfig) -> PolicyMetrics:
    costs: list[float] = []
    high_conflicts = 0
    clearances = 0
    count = 0
    for seed in config.seeds:
        environment = SyntheticCrossing(seed)
        for _ in range(config.episodes_per_seed):
            state, observation = environment.sample()
            action = policy.choose(observation)
            costs.append(designed_cost(action, state))
            high_conflicts += int(
                action is PhasePolicy.SWITCH_NORMALLY
                and state.car is CarResponse.PROCEED
                and state.rider is RiderResponse.LAUNCH_EARLY
            )
            clearances += int(action is PhasePolicy.ADD_CLEARANCE)
            count += 1
    return PolicyMetrics(
        policy=policy.name,
        mean_designed_cost=mean(costs),
        mean_high_conflict_rate=high_conflicts / count,
        mean_clearance_rate=clearances / count,
    )


def compare_policies(config: ExperimentConfig = ExperimentConfig()) -> list[PolicyMetrics]:
    """Evaluate three fixed policies against identical seeded episode streams."""

    policies: Iterable[Policy] = (HistoryReplayPolicy(), ConservativePolicy(), BeliefStatePolicy())
    return [evaluate_policy(policy, config) for policy in policies]
