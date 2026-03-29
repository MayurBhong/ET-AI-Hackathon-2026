from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# ✅ Correct relative imports
from ..recovery_email.mock_data.seed import DEALS
from ..agents.deal_agent import analyze_deal
from ..integrations.gmail_integration import fetch_emails, send_email
from ..integrations.news_integration import (
    fetch_competitor_news,
    detect_competitor_mentions,
    assess_competitive_threat
)

router = APIRouter()


class DealAnalyzeRequest(BaseModel):
    deal_id: str
    include_thread: bool = True


class SendRecoveryEmailRequest(BaseModel):
    deal_id: str
    to_email: str
    subject: Optional[str] = None
    body: Optional[str] = None


@router.get("/deals")
async def list_deals():
    return {"deals": DEALS, "total": len(DEALS)}


@router.get("/deals/{deal_id}")
async def get_deal(deal_id: str):
    deal = next((d for d in DEALS if d["id"] == deal_id), None)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.post("/analyze-deal")
async def analyze_deal_endpoint(request: DealAnalyzeRequest):
    deal = next((d for d in DEALS if d["id"] == request.deal_id), None)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    thread = None
    if request.include_thread and deal.get("email_thread_id"):
        threads = fetch_emails(deal["email_thread_id"])
        thread = threads[0] if threads else None

    analysis = await analyze_deal(deal, thread)

    competitor_news = fetch_competitor_news()
    relevant_signals = [
        s for s in competitor_news if deal["id"] in s.get("affected_deals", [])
    ]
    competitive_threats = [
        assess_competitive_threat(s, DEALS) for s in relevant_signals
    ]

    return {
        "deal": deal,
        "analysis": analysis,
        "email_thread": thread,
        "competitor_threats": competitive_threats,
    }


@router.post("/analyze-all-deals")
async def analyze_all_deals():
    results = []

    for deal in DEALS:
        thread = None
        if deal.get("email_thread_id"):
            threads = fetch_emails(deal["email_thread_id"])
            thread = threads[0] if threads else None

        analysis = await analyze_deal(deal, thread)

        results.append({
            "deal_id": deal["id"],
            "deal_name": deal["name"],
            "value": deal["value"],
            "risk_score": analysis.get("risk_score"),
            "risk_level": analysis.get("risk_level"),
            "deal_health": analysis.get("deal_health"),
            "top_risk": analysis.get("risk_reasons", [""])[0] if analysis.get("risk_reasons") else "",
        })

    results.sort(key=lambda x: x.get("risk_score", 0) or 0, reverse=True)

    total_at_risk = sum(
        d["value"] for d in DEALS if any(
            r["deal_id"] == d["id"] and (r.get("risk_score") or 0) > 60
            for r in results
        )
    )

    return {
        "results": results,
        "total_deals": len(results),
        "high_risk_count": sum(1 for r in results if (r.get("risk_score") or 0) > 60),
        "total_value_at_risk": total_at_risk,
    }


@router.post("/send-recovery-email")
async def send_recovery_email(request: SendRecoveryEmailRequest):
    deal = next((d for d in DEALS if d["id"] == request.deal_id), None)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    thread = None
    if deal.get("email_thread_id"):
        threads = fetch_emails(deal["email_thread_id"])
        thread = threads[0] if threads else None

    if not request.subject or not request.body:
        analysis = await analyze_deal(deal, thread)
        subject = request.subject or analysis.get(
            "suggested_email_subject", f"Following up on {deal['name']}"
        )
        body = request.body or analysis.get(
            "suggested_email_body", "Hi, just following up..."
        )
    else:
        subject = request.subject
        body = request.body

    result = send_email(to=request.to_email, subject=subject, body=body)

    return {
        "status": "sent",
        "email_result": result,
        "deal_id": request.deal_id,
    }