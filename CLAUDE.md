# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python app that generates 7-day social content gameplans (Instagram, TikTok, Threads, Facebook, YouTube) via OpenAI. Exposes both a CLI and a Flask web UI.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_key"
```

## Running the App

**CLI:**
```bash
python agent.py "fitness coaching" "grow your AI-powered brand"
python agent.py "fitness coaching" -o gameplan.md
```

**Web app** (Flask, port 5000):
```bash
python web_app.py
# open http://localhost:5000
```

There is no test suite.

## Architecture

- **`content_agent.py`** — sole OpenAI integration point. Builds `PROMPT_TEMPLATE` and calls `gpt-4o-mini`. All prompt logic lives here.
- **`agent.py`** — CLI wrapper (`argparse`) that calls `create_gameplan()`.
- **`web_app.py`** — Flask wrapper with two routes: `GET/POST /` (generate + render) and `POST /download` (stream Markdown). Renders `templates/index.html`.
- **`templates/index.html`** — only frontend file (Jinja2). Template variables: `{{ plan }}`, `{{ niche }}`, `{{ goal }}`, `{{ error }}`.

> **Known issue:** `content_agent.py` uses the legacy `openai.ChatCompletion.create()` syntax (v0), but `requirements.txt` pins `openai>=1.0.0` (v1+). The v1 equivalent is `openai.OpenAI().chat.completions.create()`.

## templates/ Directory

The `templates/` directory serves two unrelated purposes:
1. `index.html` — Flask Jinja2 template (part of this app)
2. `*.agent.md` — AI agent definition files (see `templates/CLAUDE.md` for details)
