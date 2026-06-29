import httpx


class HTTPClient:

    def __init__(self):
        self.client = httpx.Client(
            timeout=60,
            follow_redirects=True,
        )

    def post(self, *args, **kwargs):
        return self.client.post(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.client.get(*args, **kwargs)