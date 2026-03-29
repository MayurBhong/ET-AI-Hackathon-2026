from fastapi import APIRouter
from pydantic import BaseModel
from integrations.gmail_integration import fetch_emails, send_email

router = APIRouter()


class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str


@router.get("/emails")
def list_email_threads():
    return {"threads": fetch_emails()}


@router.get("/emails/{thread_id}")
def get_thread(thread_id: str):
    threads = fetch_emails(thread_id)
    if not threads:
        return {"error": "Thread not found"}
    return threads[0]


@router.post("/emails/send")
def send_email_endpoint(request: SendEmailRequest):
    result = send_email(to=request.to, subject=request.subject, body=request.body)
    return result
