import json
import httpx

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"


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
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]


async def predict_churn(account: dict) -> dict:
    system = """You are a customer success AI specializing in churn prediction for SaaS.
Return ONLY valid JSON with no markdown:
{
  "churn_probability": <float 0.0-1.0>,
  "churn_risk": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "key_risk_factors": ["factor1", "factor2", "factor3"],
  "days_to_likely_churn": <integer or null>,
  "revenue_at_risk": <estimated ARR at risk>,
  "intervention_actions": [
    {"type": "<QBR|DISCOUNT|FEATURE_DEMO|EXECUTIVE_CALL|HEALTH_REVIEW>", "urgency": "<IMMEDIATE|THIS_WEEK|THIS_MONTH>", "description": "<specific action>"}
  ],
  "retention_email_subject": "<subject>",
  "retention_email_body": "<personalized retention email>"
}"""

    prompt = f"""Predict churn for this SaaS customer:

Company: {account['company']}
Usage Drop: {account['usage_drop_pct']}% decline in last 30 days
Support Tickets (last 30d): {account['support_tickets']}
NPS Score: {account['nps_score']} (0-100)
Days Since Last Login: {account['last_login_days_ago']}
Customer Sentiment: {account['sentiment']}
Contract Renewal In: {account['contract_renewal_days']} days

Scoring guide:
- Usage drop >50% = very high churn signal
- NPS <30 = promoter disengagement
- Last login >14 days = disengagement
- High support tickets = product friction
- Renewal <60 days + high risk = CRITICAL"""

    raw = await call_claude(prompt, system)
    try:
        return json.loads(raw)
    except Exception:
        usage_drop = account.get("usage_drop_pct", 0)
        nps = account.get("nps_score", 50)
        login_days = account.get("last_login_days_ago", 0)
        
        prob = min(0.95, (usage_drop / 100 * 0.4) + (max(0, 50 - nps) / 100 * 0.3) + (min(login_days, 30) / 30 * 0.3))
        risk = "CRITICAL" if prob > 0.75 else "HIGH" if prob > 0.55 else "MEDIUM" if prob > 0.3 else "LOW"
        
        return {
            "churn_probability": round(prob, 2),
            "churn_risk": risk,
            "key_risk_factors": [
                f"Usage dropped {usage_drop}% in 30 days",
                f"NPS score critically low at {nps}",
                f"No login in {login_days} days",
            ],
            "days_to_likely_churn": account.get("contract_renewal_days", 90) if prob > 0.6 else None,
            "revenue_at_risk": 48000,
            "intervention_actions": [
                {"type": "EXECUTIVE_CALL", "urgency": "IMMEDIATE", "description": "Schedule emergency executive sponsor call to understand blockers"},
                {"type": "QBR", "urgency": "THIS_WEEK", "description": "Run emergency QBR to surface product gaps"},
                {"type": "DISCOUNT", "urgency": "THIS_WEEK", "description": "Prepare retention offer: 20% off renewal + dedicated CSM"},
            ],
            "retention_email_subject": f"Let's make {account['company']} successful — quick chat?",
            "retention_email_body": f"Hi,\n\nI noticed your team's usage has shifted recently. I'd love to understand what's changed and what we can do better.\n\nCan we find 30 minutes this week? I want to make sure you're getting full value — and if something isn't working, let's fix it together.\n\nBest,\nCustomer Success Team",
        }
