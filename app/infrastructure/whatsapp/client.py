# app/infrastructure/whatsapp/client.py
import base64
import random
import time

import requests

from app.core.config import settings


class WhatsAppClient:

    BASE_URL = "https://graph.facebook.com/v22.0"

    DEFAULT_DELAY_RANGE = (0.8, 2.0)

    def download_media(self, media_id: str) -> tuple[str, str] | None:
        """Fetches a WhatsApp media file (image, etc.) and returns (base64_data, mime_type), or None on failure."""
        try:
            meta_resp = requests.get(
                f"{self.BASE_URL}/{media_id}",
                headers={"Authorization": f"Bearer {settings.whatsapp_token}"},
                timeout=10,
            )
            meta = meta_resp.json()
            media_url = meta.get("url")
            mime_type = meta.get("mime_type", "image/jpeg")
            if not media_url:
                return None

            file_resp = requests.get(
                media_url,
                headers={"Authorization": f"Bearer {settings.whatsapp_token}"},
                timeout=15,
            )
            return base64.b64encode(file_resp.content).decode("utf-8"), mime_type
        except Exception as e:
            print(f"[whatsapp] media download error: {e}")
            return None

    def send(self, phone: str, messages: list[str]):
        for message in messages:
            time.sleep(random.uniform(*self.DEFAULT_DELAY_RANGE))
            self._send_single_message(phone, message)

    def send_bubbles(self, phone: str, bubbles: list[str], bubble_plan=None):
        for i, bubble in enumerate(bubbles):
            if bubble_plan and i < len(bubble_plan.bubbles):
                delay = bubble_plan.bubbles[i].delay
            else:
                delay = random.uniform(*self.DEFAULT_DELAY_RANGE)

            time.sleep(delay)
            self._send_single_message(phone, bubble)

    def _send_single_message(self, phone: str, message: str):
        response = requests.post(
            f"{self.BASE_URL}/{settings.phone_number_id}/messages",
            headers={
                "Authorization": f"Bearer {settings.whatsapp_token}",
                "Content-Type": "application/json",
            },
            json={
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "text",
                "text": {
                    "body": message[:4096]
                },
            },
            timeout=20,
        )

        response.raise_for_status()