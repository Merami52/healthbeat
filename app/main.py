from fastapi import FastAPI, HTTPException
from app.dependencies.health import check_postgres, check_redis
import logging
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Настройка Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app, endpoint="/metrics")  # <- здесь /metrics

@app.get("/healthz/live")
async def liveness_check():
    return {"status": "alive"}

@app.get("/healthz/ready")
async def readiness_check():
    results = {"status": "ready"}

    try:
        results.update(await check_postgres("postgresql://postgres:postgres@db:5432/postgres"))
    except HTTPException as e:
        results["status"] = "unhealthy"
        results["postgres"] = str(e.detail)

    try:
        results.update(await check_redis("redis://redis:6379/0"))
    except HTTPException as e:
        results["status"] = "unhealthy"
        results["redis"] = str(e.detail)

    return results

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down.")
