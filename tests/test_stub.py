import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import app  # noqa: E402
import brain  # noqa: E402
from app import AskIn  # noqa: E402


def test_stub_ask_never_500s(monkeypatch):
    monkeypatch.setattr(brain, "_try_ollama", lambda q: None)
    for q in ["rice price?", "open?", "", "zzz"]:
        r = app.api_ask(AskIn(q=q))
        assert r["answer"] and r["used_local_model"] is False


def test_health_shape():
    assert app.health() == {"ok": True}
