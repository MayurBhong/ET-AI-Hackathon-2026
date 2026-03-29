"""
Gmail Integration — Mock + Real API skeleton

In production: use google-auth + googleapiclient
For demo: returns mock email data matching seed threads
"""
import base64

# ✅ Correct relative import
from ..recovery_email.mock_data.seed import EMAIL_THREADS


def fetch_emails(thread_id: str = None) -> list:
    """Fetch email threads — mock implementation."""
    if thread_id:
        thread = next((t for t in EMAIL_THREADS if t["id"] == thread_id), None)
        return [thread] if thread else []
    return EMAIL_THREADS


def send_email(to: str, subject: str, body: str, from_email: str = "ae@revagent.ai") -> dict:
    """
    Send email via Gmail API.
    """
    # Mock: simulate successful send
    import uuid
    return {
        "message_id": f"mock_{uuid.uuid4().hex[:8]}",
        "to": to,
        "subject": subject,
        "status": "sent",
        "timestamp": "2025-03-29T10:00:00Z",
        "mock": True,
    }


def parse_thread_sentiment(thread: dict) -> str:
    """Basic keyword sentiment from email thread."""
    all_text = " ".join(m["body"].lower() for m in thread.get("messages", []))

    positive = ["great", "love", "excited", "interested", "yes", "proceed"]
    negative = ["concern", "issue", "problem", "delay", "other vendor", "competitor", "not sure"]

    pos = sum(1 for w in positive if w in all_text)
    neg = sum(1 for w in negative if w in all_text)

    if pos > neg + 1:
        return "positive"
    if neg > pos + 1:
        return "negative"
    return "neutral"