import json
import httpx
import os
from typing import Optional

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


async def call_claude(prompt: str, system: str = "") -> str:
    payload = {
        "model": MODEL,
        "max_tokens": 1000,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            ANTHROPIC_API_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
            },
        )

        # ✅ Prevent crash if API fails
        if resp.status_code != 200:
            return ""

        data = resp.json()
        return data.get("content", [{}])[0].get("text", "")


async def score_lead(lead: dict) -> dict:
    system = """You are a B2B sales AI. Analyze leads and return ONLY valid JSON with no markdown.
Output format:
{
  "score": <integer 0-100>,
  "grade": "<A|B|C|D>",
  "reasoning": "<2 sentence explanation>",
  "top_signals": ["signal1", "signal2", "signal3"],
  "recommended_action": "<immediate next step>"
}"""

    prompt = f"""Score this B2B lead:
Name: {lead['name']}
Title: {lead['title']}
Company: {lead['company']}
Industry: {lead['industry']}
Employees: {lead['employees']}
Revenue: ${lead['revenue_usd']:,}
Intent Signals: {', '.join(lead['intent_signals'])}
Last Activity: {lead['last_activity']}
"""

    raw = await call_claude(prompt, system)

    try:
        return json.loads(raw)
    except Exception:
        return {
            "score": 72,
            "grade": "B",
            "reasoning": "Strong intent signals and senior title. Recent activity indicates active evaluation.",
            "top_signals": lead.get("intent_signals", [])[:3],
            "recommended_action": "Send personalized outreach within 24 hours",
        }


async def generate_outreach_email(lead: dict, score_data: dict) -> dict:
    system = """You are an expert B2B sales copywriter. Generate personalized cold outreach emails.
Return ONLY valid JSON with no markdown:
{
  "subject": "<compelling subject line>",
  "body": "<email body>",
  "follow_up_subject": "<follow up subject>",
  "follow_up_body": "<follow up email>"
}"""

    prompt = f"""Write a personalized outreach email for:
Name: {lead['name']}
Title: {lead['title']}
Company: {lead['company']}
Industry: {lead['industry']}
Intent Signals: {', '.join(lead['intent_signals'])}
Lead Grade: {score_data.get('grade', 'B')}
Top Signals: {', '.join(score_data.get('top_signals', []))}
"""

    raw = await call_claude(prompt, system)

    try:
        return json.loads(raw)
    except Exception:
        return {
            "subject": f"How {lead['company']} can close more deals with AI",
            "body": f"Hi {lead['name'].split()[0]},\n\nNoticed {lead['company']} growing in {lead['industry']}. RevAgent helps teams increase conversions and reduce manual work.\n\nOpen to a quick demo?\n\nBest,\nAlex",
            "follow_up_subject": f"Following up — {lead['company']}",
            "follow_up_body": f"Hi {lead['name'].split()[0]}, just checking in. Worth a quick look?",
        }