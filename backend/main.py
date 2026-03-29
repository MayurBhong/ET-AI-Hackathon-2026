from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import leads, deals
from .recovery_email.mock_data.seed import LEADS, DEALS, COMPETITOR_SIGNALS

app = FastAPI(title="RevAgent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads.router, prefix="/api", tags=["leads"])
app.include_router(deals.router, prefix="/api", tags=["deals"])


@app.get("/")
def root():
    return {"status": "RevAgent running", "version": "1.0.0"}


@app.get("/api/dashboard")
def dashboard():
    return {
        "total_leads": len(LEADS),
        "total_deals": len(DEALS),
        "pipeline_value": sum(d["value"] for d in DEALS),
        "at_risk_deals": sum(1 for d in DEALS if d.get("risk_score", 0) > 65),
        "competitor_signals": len(COMPETITOR_SIGNALS),
        "conversion_rate": 0.34,
        "avg_deal_cycle_days": 42,
    }