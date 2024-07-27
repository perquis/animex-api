from controllers.AnimeController import get_anime_object
from fastapi import FastAPI
from utils.process_data import process_data

app = FastAPI()


@app.get("/api/v1/anime/{anime_id}")
async def get_anime_info(anime_id: int):
    url = f"https://myanimelist.net/anime/{anime_id}"
    anime_instance = get_anime_object(url)

    process_data(anime_instance['production'])
    process_data(anime_instance['demographics'])
    
    return anime_instance
