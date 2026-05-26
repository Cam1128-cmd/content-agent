# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose of this directory

This directory contains two unrelated file types that should not be confused:

| File | Purpose |
|---|---|
| `index.html` | Flask Jinja2 template — part of the Python web app (see `../CLAUDE.md`) |
| `*.agent.md` | AI agent persona definitions — standalone instruction files, not Python |

## Agent Definition Files (`*.agent.md`)

These files define specialized "Elite Email Marketing Strategist" agent personas for specific email platforms. They are AI instruction files, not code.

### Files
- `.agent.md` — base/generic agent (platform-agnostic)
- `activecampaign.agent.md`, `convertkit.agent.md`, `klaviyo.agent.md`, `mailchimp.agent.md`, `gohighlevel.agent.md` — platform-specific variants

### Required structure

Every agent file must follow this exact format:

```
---
name: <agent name>
summary: <one-line description>
---

## Purpose
## Role
## When to use
## Behavior rules
## Recommended questions
## Notes
```

### Core rule shared by all agents

**Never write email copy until complete business context is collected.** Every agent must ask for: business name, offer, target audience, pain points, campaign goal, and brand voice before generating any output.

### Platform-specific additions

Each platform variant extends the base questions with platform-specific context:
- **ActiveCampaign** — lists, tags, automation stages
- **ConvertKit** — tags, segments, sequence length
- **Klaviyo** — lists, flow types, A/B subject line testing
- **Mailchimp** — audience tags, journey type
- **GoHighLevel** — pipeline stage, triggers, appointment funnel context

### Adding a new platform variant

Copy an existing `*.agent.md`, update the frontmatter `name` and `summary`, keep all base behavior rules intact, and add platform-specific questions under `## Recommended questions`.
