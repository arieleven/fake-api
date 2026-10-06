"""The tiny bits of "business logic" the fake app has, kept pure so they unit-test cleanly."""

from __future__ import annotations

import os
import random

# How often /api/flaky fails. Overridable so a run can be made calmer or angrier.
DEFAULT_FLAKY_FAIL_RATE = 0.3
# How long /api/slow sleeps, in seconds.
DEFAULT_SLOW_SECONDS = 1.5


def flaky_fail_rate() -> float:
    raw = os.environ.get("FAKE_FLAKY_FAIL_RATE", "")
    try:
        value = float(raw) if raw else DEFAULT_FLAKY_FAIL_RATE
    except ValueError:
        value = DEFAULT_FLAKY_FAIL_RATE
    return min(1.0, max(0.0, value))


def slow_seconds() -> float:
    raw = os.environ.get("FAKE_SLOW_SECONDS", "")
    try:
        value = float(raw) if raw else DEFAULT_SLOW_SECONDS
    except ValueError:
        value = DEFAULT_SLOW_SECONDS
    return max(0.0, value)


def should_fail(fail_rate: float, rng: random.Random | None = None) -> bool:
    """Roll the dice for the flaky route."""
    roll = (rng or random).random()
    return roll < fail_rate


def verdict(status_code: int) -> str:
    """What the UI shows for a response: a tick for 2xx, an explosion for anything else."""
    return "✅" if 200 <= status_code < 300 else "💥"


def bullshit_level(clicks: int) -> str:
    """The one feature nobody asked for."""
    if clicks <= 0:
        return "none yet"
    if clicks < 3:
        return "mild"
    if clicks < 10:
        return "considerable"
    return "maximum"
