"""Typed model objects for a deliberately small partially observed crossing."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CarResponse(str, Enum):
    BRAKE = "brake"
    PROCEED = "proceed"


class RiderResponse(str, Enum):
    WAIT = "wait"
    LAUNCH_EARLY = "launch_early"


class PhasePolicy(str, Enum):
    """Actions available to the controller in the toy environment."""

    SWITCH_NORMALLY = "switch_normally"
    ADD_CLEARANCE = "add_clearance"
    HOLD_GREEN = "hold_green"


@dataclass(frozen=True)
class LatentCrossingState:
    """Unobserved response pair for one simulator episode."""

    car: CarResponse
    rider: RiderResponse


@dataclass(frozen=True)
class Observation:
    """Noisy signals available before the policy acts.

    They are synthetic features created by the simulator.  They do not model
    visual perception, biometric data, driver traits, or real traffic signals.
    """

    approach_speed: str
    launch_cue: bool

    def __post_init__(self) -> None:
        if self.approach_speed not in {"low", "high"}:
            raise ValueError("approach_speed must be 'low' or 'high'")


@dataclass(frozen=True)
class Episode:
    """One sampled latent state, observation and realised policy outcome."""

    state: LatentCrossingState
    observation: Observation
    action: PhasePolicy
    cost: float


LATENT_STATES: tuple[LatentCrossingState, ...] = tuple(
    LatentCrossingState(car, rider)
    for car in CarResponse
    for rider in RiderResponse
)
