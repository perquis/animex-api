from typing import Annotated

from controllers.AnimeController import get_anime_object
from fastapi import APIRouter, Depends, Path
from fastapi_limiter.depends import RateLimiter
from models import AnimeModel
from utils.cache import use_redis_cache
from utils.process_data import process_data

anime_router = APIRouter()


def get_anime_info(
    anime_id: Annotated[int, Path(title="Anime ID", description="The `ID` of the anime from the **myanimelist**.", ge=1, le=100_000, example=20)]
) -> AnimeModel:
    def fetch_data():
        url = f"https://myanimelist.net/anime/{anime_id}"
        anime_instance = get_anime_object(url)

        process_data(anime_instance['production'])
        process_data(anime_instance['demographics'])

        return anime_instance
    
    return use_redis_cache(f"get_anime_info:{anime_id}", fetch_data)


anime_router.add_api_route(
    "/anime/{anime_id}", 
    get_anime_info, 
    methods=["GET"], 
    dependencies=[
        Depends(RateLimiter(times=100, seconds=10))
        ],
    tags=["Anime"],
    summary="Get anime information",
    description="Get anime information from **myanimelist**.",
    responses={
        200: {
            "description": "Anime information retrieved successfully.",
        },
        404: {
            "description": "Anime not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Anime not found.",
                    }
                }
            }
        },
        429: {
            "description": "Too many requests.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Too many requests.",
                    }
                }
            }
        }
    }
)
