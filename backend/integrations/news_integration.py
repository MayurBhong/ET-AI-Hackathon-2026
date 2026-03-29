"""
News API Integration — Competitor tracking
Uses newsapi.org in production; mock for demo
"""
import httpx
import os

# ✅ Correct relative import
from ..recovery_email.mock_data.seed import COMPETITOR_SIGNALS

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "demo_key")
TRACKED_COMPETITORS = ["Salesforce", "HubSpot", "Gong", "Outreach", "Clari", "Apollo.io"]


def fetch_competitor_news(competitors: list = None) -> list:
    # Mock: return seed data
    targets = competitors or TRACKED_COMPETITORS
    return [s for s in COMPETITOR_SIGNALS if s["competitor"] in targets]


def detect_competitor_mentions(text: str) -> list:
    """Detect competitor mentions in any text (emails, notes)."""
    text_lower = text.lower()
    return [c for c in TRACKED_COMPETITORS if c.lower() in text_lower]


def assess_competitive_threat(signal: dict, deals: list) -> dict:
    """Map competitor signals to affected deals and assess threat level."""
    affected = signal.get("affected_deals", [])
    total_value = sum(d["value"] for d in deals if d["id"] in affected)
    
    return {
        "signal": signal,
        "affected_deal_count": len(affected),
        "revenue_at_risk": total_value,
        "threat_level": signal.get("impact", "medium").upper(),
        "recommended_response": _get_battle_card(signal["competitor"]),
    }


def _get_battle_card(competitor: str) -> str:
    cards = {
        "Salesforce": "Emphasize RevAgent's 10x faster implementation (2 weeks vs 6 months), no per-seat pricing, and AI-native architecture vs Salesforce's bolt-on AI.",
        "HubSpot": "RevAgent is purpose-built for enterprise RevOps. HubSpot is a CRM first. Highlight our deal risk detection and automated recovery — not available in HubSpot.",
        "Gong": "Gong is conversation intelligence only. RevAgent is end-to-end: prospecting → deal management → churn prevention. More ROI for the same budget.",
        "Outreach": "Outreach automates sequences; RevAgent thinks. Our AI adapts outreach based on real-time deal signals, competitor mentions, and sentiment shifts.",
        "Clari": "Clari does forecasting. RevAgent does forecasting AND automated recovery actions. We don't just predict risk — we fix it.",
        "Apollo.io": "Apollo is a database. RevAgent is an agent. We use enriched data AND AI to take action — scoring, emailing, recovering — not just finding contacts.",
    }
    return cards.get(competitor, f"Highlight RevAgent's unique AI-native advantage over {competitor}.")