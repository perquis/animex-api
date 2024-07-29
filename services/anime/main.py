from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.AnimeRouter import anime_router
from Secweb.ContentSecurityPolicy import ContentSecurityPolicy
from services.redis import lifespan

app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight": {
            "theme": "arta"
        },
    }, 
    title="animex-api",
    version="1.0.0", 
    description="This is unofficial api that shares public data from <a href='https://myanimelist.net/' target='_blank'>myanimelist.net</a> about anime and manga in real time 🎏🀄.",
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

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