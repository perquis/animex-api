from fastapi import FastAPI, HTTPException
from requests.exceptions import HTTPError

from models.Anime import get_anime_object
from utils.process_data import process_data

app = FastAPI()


@app.get("/api/v1/anime/{anime_id}")
async def get_anime_info(anime_id: int):
    try:
        url = f"https://myanimelist.net/anime/{anime_id}"
        anime_instance = get_anime_object(url)

        process_data(anime_instance['production'])
        process_data(anime_instance['demographics'])
        
        return anime_instance
    except Exception as e:
        if "404" in str(e):
            raise HTTPException(status_code=404, detail="Anime not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
