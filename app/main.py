from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="healthbeat", version="0.1.0")

@app.get("/healthz/ready")
def readiness_probe():
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
