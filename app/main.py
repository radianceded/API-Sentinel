from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.auth import router as auth_router
app=FastAPI(
    title="API_Sentinel",
    description="A lightweight API monitoring and alerting platform.",
    version="0.1.0"
)
app.include_router(auth_router)
app.include_router(user_router)
@app.get("/health")
def health_check():
    return {
        "status":"ok",
        "service":"API-sentinel",
        "version":"0.1.0",
    }

