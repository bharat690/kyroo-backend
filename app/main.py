from fastapi import FastAPI

from app.api.routes.user import router as user_router

app = FastAPI(
    title="Kyroo API",
    version="1.0.0",
)

app.include_router(user_router)


@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "kyroo-backend",
    }