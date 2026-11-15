"""Fake API with a fake UI.

Every route is honest about what it is:

    GET /api/ok      always works
    GET /api/flaky   fails some of the time (FAKE_FLAKY_FAIL_RATE, default 0.3)
    GET /api/broken  always fails with a 500
    GET /api/slow    works, but takes FAKE_SLOW_SECONDS (default 1.5s)

GET / serves the "Fake Doing Bullshit" page, one button per route.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from fake_api import admin, logic

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Fake API")
app.include_router(admin.router)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/ok")
def ok() -> dict[str, str]:
    return {"result": "did nothing, successfully"}


@app.get("/api/flaky")
def flaky() -> JSONResponse:
    if logic.should_fail(logic.flaky_fail_rate()):
        return JSONResponse({"result": "flaked"}, status_code=503)
    return JSONResponse({"result": "worked this time"})


@app.get("/api/broken")
def broken() -> JSONResponse:
    # Broken on purpose. This is the bug.
    return JSONResponse({"result": "broken, as advertised"}, status_code=500)


@app.get("/api/slow")
async def slow() -> dict[str, str]:
    await asyncio.sleep(logic.slow_seconds())
    return {"result": "eventually did nothing"}
