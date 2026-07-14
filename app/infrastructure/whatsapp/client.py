# app/infrastructure/whatsapp/client.py
import random
import time

import requests

from app.core.config import settings


class WhatsAppClient:

    BASE_URL = "https://graph.facebook.com/v22.0"

    DEFAULT_DELAY_RANGE = (0.8, 2.0)

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