from fastapi import APIRouter
from mock_data.seed import DEALS
from integrations.news_integration import fetch_competitor_news, assess_competitive_threat

router = APIRouter()


@router.get("/competitor-signals")
def get_competitor_signals():
    signals = fetch_competitor_news()
    threats = [assess_competitive_threat(s, DEALS) for s in signals]
    return {
        "signals": signals,
        "threat_assessments": threats,
        "total_revenue_at_risk": sum(t["revenue_at_risk"] for t in threats),
    }
