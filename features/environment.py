from fastapi.testclient import TestClient

from fake_api.app import app


def before_scenario(context, scenario):
    context.client = TestClient(app)
