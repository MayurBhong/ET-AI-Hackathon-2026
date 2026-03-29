import json
import httpx
import os

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

        # ✅ Safe fallback if API fails
        if resp.status_code != 200:
            return ""

        data = resp.json()
        return data.get("content", [{}])[0].get("text", "")


async def analyze_deal(deal: dict, thread: dict = None) -> dict:
    system = """You are an expert sales deal analyst. Detect deal risks and suggest recovery actions.
Return ONLY valid JSON with no markdown:
{
  "risk_score": <integer 0-100>,
  "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "risk_reasons": ["reason1", "reason2", "reason3"],
  "deal_health": "<HEALTHY|AT_RISK|STALLED|LIKELY_LOST>",
  "recovery_actions": [
    {"priority": "HIGH", "action": "<what to do>", "rationale": "<why>"},
    {"priority": "MEDIUM", "action": "<what to do>", "rationale": "<why>"}
  ],
  "suggested_email_subject": "<subject>",
  "suggested_email_body": "<email body under 120 words>"
}"""

    thread_info = ""
    if thread:
        msgs = thread.get("messages", [])
        last_msgs = msgs[-3:] if len(msgs) >= 3 else msgs

        thread_info = f"""
Email Thread Sentiment: {thread.get('sentiment', 'unknown')}
Competitor Mentions: {', '.join(thread.get('competitor_mentions', [])) or 'None'}
Recent Messages:
""" + "\n".join([f"  [{m['from']}] {m['body'][:200]}" for m in last_msgs])

    prompt = f"""Analyze this B2B deal for risks:

Deal: {deal['name']}
Stage: {deal['stage']}
Value: ${deal['value']:,}
Days in Current Stage: {deal['days_in_stage']}
Last Reply: {deal['last_reply_days_ago']} days ago
Close Date: {deal['close_date']}
{thread_info}
"""

    raw = await call_claude(prompt, system)

    try:
        return json.loads(raw)
    except Exception:
        # ✅ fallback logic
        days = deal.get("last_reply_days_ago", 0)
        risk = min(95, 30 + days * 3 + (20 if thread and thread.get("competitor_mentions") else 0))
        level = "CRITICAL" if risk > 80 else "HIGH" if risk > 60 else "MEDIUM" if risk > 35 else "LOW"

        return {
            "risk_score": risk,
            "risk_level": level,
            "risk_reasons": [
                f"No reply for {days} days",
                "Deal stalled in current stage",
                "Competitor evaluation underway" if thread and thread.get("competitor_mentions") else "Close date approaching",
            ],
            "deal_health": "AT_RISK" if risk > 50 else "HEALTHY",
            "recovery_actions": [
                {"priority": "HIGH", "action": "Send re-engagement email", "rationale": "Break silence"},
                {"priority": "HIGH", "action": "Offer call", "rationale": "Rebuild momentum"},
            ],
            "suggested_email_subject": f"Quick follow-up on {deal['name']}",
            "suggested_email_body": "Hi, just checking in—happy to help move things forward.",
        }