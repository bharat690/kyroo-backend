import json
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import PlainTextResponse
from app.api.dependencies.database import get_db
from app.core.config import settings
from app.engine.orchestrator import Orchestrator
from app.infrastructure.whatsapp.client import WhatsAppClient
from app.brain.kyroo_brain import validate_response

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
async def webhook(request: Request, db=Depends(get_db)):
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

    try:
        reply = Orchestrator(db).process(phone, text)
        bubbles = validate_response(reply)
        WhatsAppClient().send(phone, bubbles)
    except Exception as e:
        print(f"[webhook] Error: {e}")

    return {"status": "ok"}
