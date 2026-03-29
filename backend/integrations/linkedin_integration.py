"""
LinkedIn Integration — Mock implementation
Production: use LinkedIn OAuth 2.0 + People API
"""

MOCK_PROFILES = {
    "priya@technova.in": {
        "linkedin_id": "priya-sharma-123",
        "name": "Priya Sharma",
        "headline": "VP of Sales @ TechNova India | SaaS Growth Leader",
        "summary": "10+ years scaling B2B SaaS sales.",
        "skills": ["Sales Leadership", "Revenue Operations", "CRM", "Pipeline Management", "SaaS"],
        "connections": 2400,
        "recent_posts": [
            "Just hit Q1 target early — AI tools are changing sales 🚀",
            "Looking for RevOps platforms integrating with HubSpot",
        ],
        "company_news": "TechNova India raised Series B $8M",
        "mutual_connections": 3,
    },
    "amit@finedge.io": {
        "linkedin_id": "amit-verma-456",
        "name": "Amit Verma",
        "headline": "CTO @ FinEdge Solutions",
        "summary": "Engineering leader in fintech.",
        "skills": ["Engineering Leadership", "Fintech", "API Architecture"],
        "connections": 1800,
        "recent_posts": [
            "Evaluating AI-powered RevOps tools",
        ],
        "company_news": "Top 50 Fintech Startups India",
        "mutual_connections": 1,
    },
}


def get_profile(email: str, name: str = "Unknown") -> dict:
    """Get LinkedIn profile by email (mock)."""

    if email and email in MOCK_PROFILES:
        return MOCK_PROFILES[email]

    # ✅ fallback using name instead of broken email
    base_name = name if name else "Professional"

    return {
        "linkedin_id": f"mock_{base_name.lower().replace(' ', '_')}",
        "name": base_name,
        "headline": "Business Professional",
        "summary": "Experienced professional at a growing company.",
        "skills": ["Leadership", "Strategy", "Operations"],
        "connections": 500,
        "recent_posts": [],
        "company_news": None,
        "mutual_connections": 0,
    }


def enrich_lead(lead: dict) -> dict:
    """Enrich lead data with LinkedIn profile info."""

    profile = get_profile(
        lead.get("email", ""),
        lead.get("name", "Unknown")
    )

    return {
        **lead,
        "linkedin_profile": profile,
        "enrichment_signals": [
            p for p in profile.get("recent_posts", [])
            if any(kw in p.lower() for kw in ["revops", "sales", "crm", "ai", "tool", "platform"])
        ],
    }