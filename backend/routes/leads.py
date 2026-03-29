from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# ✅ Correct relative imports
from ..recovery_email.mock_data.seed import LEADS
from ..agents.prospect_agent import score_lead, generate_outreach_email
from ..integrations.linkedin_integration import enrich_lead

router = APIRouter()


class LeadScoreRequest(BaseModel):
    lead_id: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None


# ✅ Get all leads
@router.get("/leads")
async def list_leads():
    return {"leads": LEADS, "total": len(LEADS)}


# ✅ Get single lead + enrichment
@router.get("/leads/{lead_id}")
async def get_lead(lead_id: str):
    lead = next((l for l in LEADS if l["id"] == lead_id), None)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    enriched = enrich_lead(lead)
    return enriched


# ✅ Score single lead (existing or adhoc)
@router.post("/score-lead")
async def score_lead_endpoint(request: LeadScoreRequest):

    if request.lead_id:
        lead = next((l for l in LEADS if l["id"] == request.lead_id), None)

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

    else:
        # Ad-hoc lead
        lead = {
            "id": "adhoc",
            "name": "Unknown",
            "title": request.role or "Unknown",
            "company": request.company or "Unknown",
            "industry": "Unknown",
            "employees": 100,
            "revenue_usd": 1000000,
            "intent_signals": [],
            "last_activity": "2025-03-01",
        }

    score_data = await score_lead(lead)
    email_data = await generate_outreach_email(lead, score_data)
    enriched = enrich_lead(lead)

    return {
        "lead": lead,
        "score": score_data,
        "outreach_email": email_data,
        "linkedin_enrichment": enriched.get("linkedin_profile"),
        "enrichment_signals": enriched.get("enrichment_signals", []),
    }


# ✅ Score all leads
@router.post("/score-all-leads")
async def score_all_leads():
    results = []

    for lead in LEADS:
        score_data = await score_lead(lead)
        email_data = await generate_outreach_email(lead, score_data)

        results.append({
            "lead_id": lead["id"],
            "name": lead["name"],
            "company": lead["company"],
            "score": score_data,
            "email_preview": email_data.get("subject"),
        })

    return {
        "results": results,
        "total_scored": len(results)
    }