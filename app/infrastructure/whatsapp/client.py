import requests

from app.core.config import settings


class WhatsAppClient:

    BASE_URL = "https://graph.facebook.com/v22.0"

    def send(
        self,
        phone: str,
        message: str,
    ):

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