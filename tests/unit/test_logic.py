"""Unit tests for fake_api.logic. These are expected to pass: the logic itself is fine."""

from __future__ import annotations

import random

import pytest

from fake_api import logic


class _FixedRng(random.Random):
    def __init__(self, value: float) -> None:
        super().__init__()
        self._value = value

    def random(self) -> float:
        return self._value


@pytest.mark.parametrize(
    ("roll", "rate", "expected"),
    [(0.1, 0.3, True), (0.5, 0.3, False), (0.0, 0.0, False), (0.99, 1.0, True), (0.3, 0.3, False)],
)
def test_should_fail_compares_roll_to_rate(roll: float, rate: float, expected: bool) -> None:
    assert logic.should_fail(rate, _FixedRng(roll)) is expected


@pytest.mark.parametrize(("status", "expected"), [(200, "✅"), (204, "✅"), (500, "💥"), (503, "💥"), (404, "💥")])
def test_verdict(status: int, expected: str) -> None:
    assert logic.verdict(status) == expected


@pytest.mark.parametrize(
    ("clicks", "expected"),
    [(0, "none yet"), (1, "mild"), (2, "mild"), (3, "considerable"), (9, "considerable"), (10, "maximum")],
)
def test_bullshit_level(clicks: int, expected: str) -> None:
    assert logic.bullshit_level(clicks) == expected


def test_flaky_fail_rate_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FAKE_FLAKY_FAIL_RATE", raising=False)
    assert logic.flaky_fail_rate() == logic.DEFAULT_FLAKY_FAIL_RATE


@pytest.mark.parametrize(("raw", "expected"), [("0.5", 0.5), ("2", 1.0), ("-1", 0.0), ("nonsense", 0.3)])
def test_flaky_fail_rate_is_clamped(monkeypatch: pytest.MonkeyPatch, raw: str, expected: float) -> None:
    monkeypatch.setenv("FAKE_FLAKY_FAIL_RATE", raw)
    assert logic.flaky_fail_rate() == expected


@pytest.mark.parametrize(("raw", "expected"), [("", 1.5), ("0.2", 0.2), ("-3", 0.0), ("soon", 1.5)])
def test_slow_seconds(monkeypatch: pytest.MonkeyPatch, raw: str, expected: float) -> None:
    monkeypatch.setenv("FAKE_SLOW_SECONDS", raw)
    assert logic.slow_seconds() == expected
