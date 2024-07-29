import os
from contextlib import asynccontextmanager

import redis.asyncio as redis
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from redis import Redis

load_dotenv()

redis_client = Redis(host=os.getenv("REDIS_HOSTNAME"), port=int(os.getenv("REDIS_PORT")), db=0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_connection = redis.from_url(os.getenv("REDIS_ORIGIN"), encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    yield