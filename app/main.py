from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.middleware.request_log import RequestLogMiddleware

app = FastAPI(
    title="API_Sentinel",
    description="A lightweight API monitoring and alerting platform.",
    version="0.1.0",
)

app.add_middleware(RequestLogMiddleware)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}
