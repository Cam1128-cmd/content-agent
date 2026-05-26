import os
from typing import Optional

import openai

PROMPT_TEMPLATE = """You are a content strategy agent creating a 7-day social media content gameplan for an AI education Skool community.

Community details:
- Teaches everyday business owners how to use AI practically and profitably.
- Two segments: complete beginners (zero AI experience) and intermediate learners ready to build websites, ebooks, AI agents, and automations.
- Tone: encouraging, jargon-free, results-focused. Make AI feel accessible, not intimidating.

Requirements:
- 7 daily themes that speak directly to business owners curious about or learning AI.
- Each day: 2 social media posts (Instagram, TikTok, Threads, Facebook) with a Hook, Value, and CTA.
- Each post must include a short-form video script (conversational, 60-90 words, ends with an engagement prompt).
- Mix beginner and intermediate content across the week.
- All CTAs drive people to join the Skool community.

Input:
Niche: {niche}
Primary goal: {goal}

Output format — follow this structure exactly for every day:

# Day [number] — [Theme]

## Post 1

**Hook:**
[one punchy sentence]

**Value:**
[2-3 sentences of useful insight]

**CTA:**
[one clear call to action]

### Video Script

[60-90 word conversational script, no hashtags, ends with an engagement prompt like "Comment AI if you want to learn more."]

---

## Post 2

**Hook:**
[one punchy sentence]

**Value:**
[2-3 sentences of useful insight]

**CTA:**
[one clear call to action]

### Video Script

[60-90 word conversational script, no hashtags, ends with an engagement prompt]

---

Repeat this structure for all 7 days. Do not add any intro or closing text outside of this format.
"""


def build_prompt(niche: str, goal: Optional[str]) -> str:
    if not goal:
        goal = "grow audience, engagement, and AI-driven revenue"
    return PROMPT_TEMPLATE.format(niche=niche.strip(), goal=goal.strip())


def create_gameplan(niche: str, goal: Optional[str] = None) -> str:
    prompt = build_prompt(niche, goal)
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required. Set it in your environment before running the agent.")

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a skilled content strategist and AI automation expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        max_tokens=3500,
    )
    return response.choices[0].message.content.strip()
