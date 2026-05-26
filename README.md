# Content Gameplan Agent

A lightweight Python-based agent that generates a 7-day content gameplan with 3 daily cross-posts for Instagram, TikTok, Threads, and Facebook plus 1 YouTube post.

## Features

- 7-day content schedule
- 3 posts per day across Instagram, TikTok, Threads, and Facebook
- 1 daily YouTube content idea
- Strong hooks, CTAs, and value-add messaging
- AI scaling and automation guidance for every day
- CLI and web UI interfaces
- Markdown export support

## Setup

1. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## CLI Usage

```bash
python agent.py "fitness coaching" "grow your AI-powered personal brand"
```

To save output directly to a Markdown file:

```bash
python agent.py "fitness coaching" "grow your AI-powered personal brand" -o gameplan.md
```

## Web App Usage

```bash
python web_app.py
```

Open `http://localhost:5000` in your browser to use the form and download Markdown output.
