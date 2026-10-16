"""Dukaan Box shop API. Run: uvicorn app:app --app-dir src"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from brain import ask

app = FastAPI()
_LAST_LOCAL = False


class AskIn(BaseModel):
    q: str = ""


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/")
def index():
    return FileResponse(
        Path(__file__).resolve().parent.parent / "static" / "index.html"
    )


@app.post("/api/ask")
def api_ask(body: AskIn):
    try:
        r = ask(body.q or "")
    except Exception:
        r = {"answer": "Box busy — try again.", "used_local_model": False}
    global _LAST_LOCAL
    _LAST_LOCAL = bool(r.get("used_local_model"))
    return r


@app.get("/api/status")
def api_status():
    return {"used_local_model": _LAST_LOCAL}
