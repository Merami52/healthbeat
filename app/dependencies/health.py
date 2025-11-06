import asyncpg
import redis.asyncio as aioredis
from fastapi import HTTPException

async def check_postgres(dsn: str):
    try:
        conn = await asyncpg.connect(dsn)
        await conn.execute("SELECT 1;")
        await conn.close()
        return {"postgres": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Postgres error: {e}")

async def check_redis(url: str):
    try:
        redis = aioredis.from_url(url)
        await redis.ping()
        await redis.close()
        return {"redis": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis unavailable: {str(e)}")
