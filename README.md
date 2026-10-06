# Fake API

A deliberately silly API with a deliberately silly UI, built to be tested.
It is the demo target for [testosterone](https://github.com/taltal-beep/testosterone):
some parts work, some fail on purpose, so a test run always has something to show.

| Route | Button | Behaviour |
|-------|--------|-----------|
| `GET /api/ok` | Do nothing | Always works |
| `GET /api/flaky` | Do nothing, maybe | Fails about a third of the time (`FAKE_FLAKY_FAIL_RATE`) |
| `GET /api/broken` | Do nothing, badly | Always returns 500 |
| `GET /api/slow` | Do nothing, slowly | Works, but takes 1.5 s (`FAKE_SLOW_SECONDS`) |

`GET /` serves the **Fake Doing Bullshit** page, one button per route.

## Run it

```bash
pip install -r requirements.txt
uvicorn fake_api.app:app --reload        # http://127.0.0.1:8000
```

## Test it

The tests describe how the app *should* behave, so the broken parts fail them honestly.
Nothing in the tests is rigged; the failures come from the app.

| Layer | Where | Expected result |
|-------|-------|-----------------|
| Unit | `tests/unit` | All pass |
| API | `tests/api` | `broken` and `slow` fail; `flaky` fails some runs |
| Behave | `features/buttons.feature` | "Do nothing, badly" fails; "maybe" fails some runs |
| Browser | `tests/e2e` | "Do nothing, badly" fails; "maybe" fails some runs |

```bash
python -m playwright install chromium      # once, for the browser tests
pytest
behave features/buttons.feature
```

With testosterone installed, `testo run --cycle fake-api` runs all four layers as one
cycle (see `testosterone.yaml`) and puts the results in its dashboard.
