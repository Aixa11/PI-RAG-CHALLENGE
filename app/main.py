from fastapi import FastAPI
from app.api.v1.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API RAG para challenge tecnico de PI."
)

app.include_router(router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "environment": settings.app_env}
