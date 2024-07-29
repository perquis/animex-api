import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from routes.AnimeRouter import anime_router
from Secweb.ContentSecurityPolicy import ContentSecurityPolicy

app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight": {
            "theme": "arta"
        },
    }, 
    title="animex-api",
    version="1.0.0", 
    description="This is unofficial api that shares public data from <a href='https://myanimelist.net/' target='_blank'>myanimelist.net</a> about anime and manga in real time 🎏🀄."
)

@app.on_event("startup")
async def startup():
    redis_connection = redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ContentSecurityPolicy, Option={
    'connect-src': ["'self'"], 
    'frame-src': ["'self'"]
})

app.include_router(anime_router, prefix="/api/v1")