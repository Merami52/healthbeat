from fastapi import FastAPI, HTTPException
from app.dependencies.health import check_postgres, check_redis

app = FastAPI()

@app.get("/healthz/live")
async def liveness_check():
    return {"status": "alive"}

@app.get("/healthz/ready")
async def readiness_check():
    results = {"status": "ready"}

    # Проверяем Postgres
    try:
        results.update(await check_postgres("postgresql://postgres:postgres@db:5432/postgres"))
    except HTTPException as e:
        results["status"] = "unhealthy"
        results["postgres"] = str(e.detail)

    # Проверяем Redis
    try:
        results.update(await check_redis("redis://redis:6379/0"))
    except HTTPException as e:
        results["status"] = "unhealthy"
        results["redis"] = str(e.detail)

    return results