*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)*

## What I Built

Shop Rate Bot: a one-page shop FAQ bot. A shopkeeper sets 6 rate-card lines; customers ask "rice price?" / "open?" and get an instant answer. A dot shows stub (grey) vs local Gemma (green).

<!-- TODO: one line on who would pay: e.g. my neighbourhood kirana for rate questions after hours -->

## Demo

<!-- TODO: paste Render URL + 30s video/gif -->
- Live: <render-url>
- Try: "rice price?", "open?", "xyz"

## Code

<!-- TODO: paste public GitHub repo URL (new repo, created Oct 12-18) -->

## How I Built It

FastAPI + single HTML page, no DB, no auth. `src/brain.py` tries Ollama (`$GEMMA_MODEL`, default `gemma3n:e2b`) with strict JSON, falls back to a keyword stub — so it never 500s and boots with no keys. Deploys via Dockerfile to Render free tier.

## Why Does Open Innovation Matter?

Runs on-device via Ollama with zero per-query cost, so a ₹499/mo price works; customer rate questions never leave the shop laptop. Stub keeps it working with Wi-Fi off; Gemma makes answers warmer when home.

## Prize Categories

Best Use of Render, Best Use of Gemma
