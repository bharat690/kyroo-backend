import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.config import settings
from app.engine.orchestrator import Orchestrator
from app.infrastructure.whatsapp.client import WhatsAppClient

router = APIRouter(tags=["WhatsApp"])


@router.get("/webhook")
async def verify(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == settings.verify_token:
        return PlainTextResponse(challenge)

    raise HTTPException(status_code=403)


@router.post("/webhook")
async def webhook(
    request: Request,
    db: Session = Depends(get_db),
):

    body = await request.json()

    print(json.dumps(body, indent=2))

    try:
        value = body["entry"][0]["changes"][0]["value"]
    except Exception:
        return {"status": "ignored"}

    if "messages" not in value:
        return {"status": "ignored"}

    message = value["messages"][0]

    if message["type"] != "text":
        return {"status": "ignored"}

    phone = message["from"]

    text = message["text"]["body"].strip()

    # The orchestrator now returns a list of bubbles
    bubbles = Orchestrator(db).process(
        phone,
        text,
    )

    # Send each bubble with appropriate delay
    WhatsAppClient().send_bubbles(
        phone,
        bubbles,
    )

    return {"status": "ok"}