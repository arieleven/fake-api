"""API tests. They describe how the API *should* behave, so the broken parts fail them."""

from __future__ import annotations

import time

from fastapi.testclient import TestClient

from fake_api.app import app

client = TestClient(app)


def test_index_serves_the_ui() -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Fake Doing Bullshit" in resp.text


def test_ok_does_nothing_successfully() -> None:
    resp = client.get("/api/ok")
    assert resp.status_code == 200
    assert resp.json() == {"result": "did nothing, successfully"}


def test_unknown_route_is_404() -> None:
    assert client.get("/api/nope").status_code == 404


def test_flaky_works() -> None:
    # Fails whenever the route flakes (about a third of the time by default).
    assert client.get("/api/flaky").status_code == 200


def test_broken_works() -> None:
    # Always fails: /api/broken is broken on purpose.
    assert client.get("/api/broken").status_code == 200


def test_slow_answers_within_a_second() -> None:
    # Fails while /api/slow takes longer than its one-second budget.
    started = time.monotonic()
    resp = client.get("/api/slow")
    elapsed = time.monotonic() - started
    assert resp.status_code == 200
    assert elapsed < 1.0, f"took {elapsed:.2f}s"
