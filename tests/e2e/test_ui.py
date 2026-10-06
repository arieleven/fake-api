"""Browser tests: click the buttons on the real page served by a real server."""

from __future__ import annotations

import os
import socket
import threading
import time
from collections.abc import Iterator

import pytest
import uvicorn

from fake_api.app import app

playwright = pytest.importorskip("playwright.sync_api")


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="module")
def base_url() -> Iterator[str]:
    port = _free_port()
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}/"
    server.should_exit = True
    thread.join(timeout=5)


@pytest.fixture(scope="module")
def page(base_url: str):
    with playwright.sync_playwright() as p:
        # Lets a machine with a preinstalled Chromium skip `playwright install`.
        executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE") or None
        browser = p.chromium.launch(executable_path=executable)
        page = browser.new_page()
        page.goto(base_url)
        yield page
        browser.close()


def _press(page, label: str) -> str:
    page.get_by_role("button", name=label, exact=True).click()
    result = page.locator("#result")
    result.filter(has_not_text="…").wait_for(timeout=10_000)
    return result.inner_text()


def test_do_nothing_button(page) -> None:
    assert _press(page, "Do nothing").startswith("✅")


def test_do_nothing_maybe_button(page) -> None:
    assert _press(page, "Do nothing, maybe").startswith("✅")


def test_do_nothing_badly_button(page) -> None:
    assert _press(page, "Do nothing, badly").startswith("✅")


def test_bullshit_level_goes_up(page) -> None:
    _press(page, "Do nothing")
    assert page.locator("#level").inner_text() != "none yet"
