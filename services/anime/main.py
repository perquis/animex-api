from typing import Annotated

from controllers.AnimeController import get_anime_object
from fastapi import FastAPI, Path
from models import Anime
from utils.process_data import process_data

app = FastAPI(swagger_ui_parameters={
    "syntaxHighlight": {
        "theme": "arta"
    }
})


@app.get("/api/v1/anime/{anime_id}")
def get_anime_info(
    anime_id: Annotated[int, Path(title="Anime ID", description="The ID of the anime", ge=1, le=100_000)]
) -> Anime:
    url = f"https://myanimelist.net/anime/{anime_id}"
    anime_instance = get_anime_object(url)

    process_data(anime_instance['production'])
    process_data(anime_instance['demographics'])
    
    return anime_instance
