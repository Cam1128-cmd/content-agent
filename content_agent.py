import os
from typing import Optional

import openai

PROMPT_TEMPLATE = """You are a content strategy agent tasked with creating a 7-day social media content gameplan for an AI education Skool community.

Community details:
- The community teaches everyday business owners how to use AI practically and profitably.
- Two audience segments: complete beginners (zero AI experience) and intermediate learners (general AI knowledge, ready to build websites, ebooks, AI agents, and other business tools).
- Tone: encouraging, jargon-free, and results-focused. Make AI feel accessible, not intimidating.

Requirements:
- Provide 7 daily themes that speak directly to business owners curious about or learning AI.
- For each day, include 3 cross-post captions or short scripts for Instagram, TikTok, Threads, and Facebook.
- Include 1 YouTube content idea per day with a title and short description.
- Each post must have a strong hook, clear value, and a CTA that drives people to join the Skool community.
- Mix content for both audience segments across the week (some posts for total beginners, some for those ready to build).
- Include real, relatable examples of what members learn: AI agents, websites, ebooks, automations, and other business tools.

Input:
Niche: {niche}
Primary goal: {goal}

Output format:
- Day 1: Theme
  - Post 1: Hook, value, CTA
  - Post 2: Hook, value, CTA
  - Post 3: Hook, value, CTA
  - YouTube: Title, Description, CTA
  - Audience note: (beginner / intermediate / both)

Write output in Markdown.
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
        max_tokens=1500,
    )
    return response.choices[0].message.content.strip()
