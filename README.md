# Shop Rate Bot (Side Hustle)

Shop FAQ bot: ask rates/hours, get an answer. Open-weight Gemma via Ollama when available, deterministic stub fallback otherwise. Same code runs on laptop/Render.

## Quickstart

Requires Python ≥ 3.12.

```sh
uv sync
uv run uvicorn app:app --app-dir src --reload
# open http://127.0.0.1:8000
```

Real local model (optional): `ollama run gemma4:e2b` (or set `$GEMMA_MODEL`; falls back to `gemma3n:e2b`).
No keys, no DB, no auth, no torch. Without Ollama the stub answers;
`used_local_model` flag shows which path ran.

## API

| Route | Notes |
|---|---|
| `GET /health` | Uptime probe (Render healthcheck) |
| `GET /` | Single-page shop ask box + status dot |
| `POST /api/ask` | `{q}` → `{answer, used_local_model}` |
| `GET /api/status` | `{used_local_model}` |

## Demo script

1. Ask "rice price?" → stub rate answer, dot grey (= stub).
2. Start Ollama → same question, dot green (= Gemma).

## Tests / deploy

```sh
python -m pytest -q
PYTHONPATH=src python src/brain.py  # stub self-check
```

Docker → Render (`Dockerfile`, `render.yaml`).

## License

MIT — see [LICENSE](LICENSE).
