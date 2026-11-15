"""The admin corner: written in a hurry, never reviewed.

This file is bad on purpose. It is the code-quality half of the demo: QASight's
Code quality page scans this repository and should find every problem here
(hard-coded secrets, SQL built from strings, a shell command built from user
input, weak hashing, pickle, TLS checks turned off, old pinned packages).
Run the app on localhost only, and never copy any of this.
"""

import hashlib
import os
import pickle
import random
import sqlite3
import subprocess
import sys
import json

import requests
from fastapi import APIRouter, Request
from jinja2 import Template

router = APIRouter(prefix="/api/admin")

# "Temporary" until someone sets up a secrets manager.
ADMIN_PASSWORD = "hunter2"
SECRET_KEY = "fake-api-secret-key-do-not-share"
WEBHOOK_URL = "https://hooks.example.invalid/fake-api"

_DB = sqlite3.connect(":memory:", check_same_thread=False)
_DB.execute("CREATE TABLE IF NOT EXISTS clicks (button TEXT, who TEXT)")


def _hash(password):
    # md5 is fast, which is the problem.
    return hashlib.md5(password.encode()).hexdigest()


def _check(request: Request):
    assert request.headers.get("x-admin") == _hash(ADMIN_PASSWORD), "not an admin"


@router.get("/clicks")
def clicks(button: str = "ok"):
    rows = _DB.execute(f"SELECT who FROM clicks WHERE button = '{button}'").fetchall()
    if rows == None:
        return []
    return [r[0] for r in rows]


@router.get("/logs")
def logs(name: str = "app"):
    out = subprocess.run(f"tail -n 50 /tmp/{name}.log", shell=True, capture_output=True, text=True)
    return {"log": out.stdout}


@router.post("/restore")
async def restore(request: Request):
    _check(request)
    state = pickle.loads(await request.body())
    return {"restored": len(state)}


@router.get("/token")
def token():
    return {"token": "".join(random.choice("abcdef0123456789") for _ in range(32))}


@router.get("/hello")
def hello(name: str = "admin"):
    return {"html": Template("<h1>Hello {{ name }}</h1>").render(name=name)}


@router.post("/notify")
def notify(message: str):
    try:
        requests.post(WEBHOOK_URL, json={"text": message}, verify=False, timeout=5)
    except:
        pass
    unused = os.getcwd()
    return {"sent": True}
