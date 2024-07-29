from fastapi import FastAPI
from routes.AnimeRouter import anime_router

app = FastAPI(swagger_ui_parameters={
    "syntaxHighlight": {
        "theme": "arta"
    }
})


app.include_router(anime_router, prefix="/api/v1")