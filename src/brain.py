"""Deterministic stub FAQ matcher + optional Ollama/Gemma path. Lazy imports only."""

import json
import os

_WARNED = False

RATES = {
    "atta 5kg": 240,
    "rice 5kg": 320,
    "milk 1l": 60,
    "chai 250g": 140,
    "sugar 1kg": 45,
    "eggs 12": 84,
}
HOURS = "Open 9am-9pm daily."


def _stub(q: str) -> str:
    ql = (q or "").strip().lower()
    if not ql:
        return "Ask about rates, hours, or tokens."
    if "hour" in ql or "open" in ql or "close" in ql:
        return HOURS
    if "token" in ql or "queue" in ql or "wait" in ql:
        return "Tokens at the counter — ask the shopkeeper."
    for item, price in RATES.items():
        if item.split()[0] in ql or item in ql:
            return f"{item}: Rs {price}."
    if "rate" in ql or "price" in ql:
        top = ", ".join(f"{k} Rs {v}" for k, v in list(RATES.items())[:4])
        return f"Rate card: {top}."
    return "Dukaan Box: ask rates/hours/token. e.g. 'rice price?'."


def _try_ollama(q: str) -> str | None:
    global _WARNED
    import urllib.request  # lazy: no hard dep

    host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    model = os.getenv("GEMMA_MODEL", "gemma3n:e2b")
    prompt = (
        'Shop FAQ bot. Reply ONLY JSON {"answer": "<<=25 words>"}. '
        f"Rates: {json.dumps(RATES)}. Hours: {HOURS}. Q: {q}"
    )
    req = urllib.request.Request(
        f"{host}/api/generate",
        data=json.dumps({"model": model, "prompt": prompt, "stream": False}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            out = json.loads(r.read().decode())
    except Exception:
        if not _WARNED:
            _WARNED = True
            print("[brain] Ollama unreachable, stub fallback (grey dot).")
        return None
    try:
        txt = out.get("response", "")
        ans = json.loads(txt[txt.find("{") : txt.rfind("}") + 1])["answer"]
        return str(ans)[:200] if ans else None
    except Exception:
        return None


def ask(q: str) -> dict:
    """Never raises: Ollama first, stub fallback. Returns answer + flag."""
    try:
        ans = _try_ollama(q)
        if ans:
            return {"answer": ans, "used_local_model": True}
    except Exception:
        pass
    # ponytail: keyword stub caps at exact rate-card words; swap in
    # embeddings only if queries go fuzzy.
    return {"answer": _stub(q), "used_local_model": False}


if __name__ == "__main__":
    for q in ["rice price?", "open hours?", "token?", "xyz"]:
        print(q, "->", ask(q))
