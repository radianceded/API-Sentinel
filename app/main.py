from fastapi import FastAPI
app=FastAPI(
    title="API_Sentinel",
    description="A lightweight API monitoring and alerting platform.",
    version="0.1.0"
)
@app.get("/health")
def health_check():
    return {
        "status":"ok",
        "service":"API-sentinel",
        "version":"0.1.0",
    }

