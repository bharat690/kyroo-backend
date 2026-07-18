import json
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import PlainTextResponse
from app.api.dependencies.database import get_db
from app.core.config import settings
from app.engine.orchestrator import Orchestrator
from app.infrastructure.whatsapp.client import WhatsAppClient
from app.brain.kyroo_brain import validate_response, kyroo_brain
from app.brain.debounce import buffer_message
from app.models.message import MessageRole
from app.services.user_service import UserService
from app.services.conversation_service import ConversationService

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
    phone = message["from"]
    msg_type = message.get("type")

    if msg_type == "image":
        # images bypass the text debounce buffer and get a direct reply
        caption = message.get("image", {}).get("caption", "")
        media_id = message.get("image", {}).get("id")
        downloaded = WhatsAppClient().download_media(media_id) if media_id else None
        image_base64, image_media_type = downloaded if downloaded else (None, None)

        try:
            user = UserService(db).get_or_create_user(phone)
            conversation_service = ConversationService(db)

            result = kyroo_brain(user, caption, [], image_base64, image_media_type)

            conversation_service.add_message(
                user=user, role=MessageRole.USER,
                content=caption or "(sent a photo)", module=result.get("module", "general"),
            )
            conversation_service.add_message(
                user=user, role=MessageRole.ASSISTANT,
                content=result["response"], module=result.get("module", "general"),
            )

            bubbles = result.get("bubbles") or validate_response(result["response"])
            WhatsAppClient().send(phone, bubbles)
        except Exception as e:
            print(f"[webhook] Image error: {e}")
        return {"status": "ok"}

    if msg_type != "text":
        return {"status": "ignored"}

    text = message["text"]["body"].strip()

    async def _reply_to_batch(combined_text: str):
        try:
            reply = Orchestrator(db).process(phone, combined_text)
            bubbles = validate_response(reply)
            WhatsAppClient().send(phone, bubbles)
        except Exception as e:
            print(f"[webhook] Error: {e}")

    # buffers rapid consecutive messages (someone splitting one thought
    # across 2-3 texts) into a single reply instead of responding to each
    # fragment separately
    await buffer_message(phone, text, _reply_to_batch)

    return {"status": "ok"}
