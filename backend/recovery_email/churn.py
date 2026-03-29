from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from mock_data.seed import CHURN_SIGNALS
from agents.churn_agent import predict_churn

router = APIRouter()


class ChurnRequest(BaseModel):
    account_id: Optional[str] = None
    usage_drop_pct: Optional[float] = None
    support_tickets: Optional[int] = None
    nps_score: Optional[int] = None
    last_login_days_ago: Optional[int] = None
    sentiment: Optional[str] = None
    contract_renewal_days: Optional[int] = None
    company: Optional[str] = None


@router.get("/churn-signals")
async def list_churn_signals():
    return {"signals": CHURN_SIGNALS}


@router.post("/predict-churn")
async def predict_churn_endpoint(request: ChurnRequest):
    if request.account_id:
        account = next((a for a in CHURN_SIGNALS if a["account_id"] == request.account_id), None)
        if not account:
            account = CHURN_SIGNALS[0]
    else:
        account = {
            "account_id": "custom",
            "company": request.company or "Unknown Company",
            "usage_drop_pct": request.usage_drop_pct or 0,
            "support_tickets": request.support_tickets or 0,
            "nps_score": request.nps_score or 50,
            "last_login_days_ago": request.last_login_days_ago or 0,
            "sentiment": request.sentiment or "neutral",
            "contract_renewal_days": request.contract_renewal_days or 90,
        }

    prediction = await predict_churn(account)
    return {"account": account, "prediction": prediction}
