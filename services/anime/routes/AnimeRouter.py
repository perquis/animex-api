import random
from typing import Annotated

from controllers.AnimeController import fetch_data, get_top_anime_list
from enums.TopAnimeType import TopAnimeType
from fastapi import APIRouter, Depends, Path, Query
from fastapi_limiter.depends import RateLimiter
from models import AnimeModel, TopAnimeItem
from responses.AnimeResponse import responses
from utils.cache import use_redis_cache

anime_router = APIRouter()


@anime_router.get("/anime/top", tags=["Anime"], summary="Get top anime information", description="Get top anime information from **myanimelist**.", responses=responses)
def get_top_anime_info(anime_type: Annotated[TopAnimeType | None, Query(title="Anime Type", description="The type of anime from the **myanimelist**.")] = None, page: Annotated[int, Query(min=1, example=1)] = 1) -> list[TopAnimeItem]:
    return get_top_anime_list(anime_type, page)


@anime_router.get("/anime/random", response_model=AnimeModel, tags=["Anime"], summary="Get random anime information", description="Get random anime information from **myanimelist**.", responses=responses)
def get_random_anime_info() -> AnimeModel:
    random_anime_id = random.randint(1, 48_000)
    return fetch_data(random_anime_id)


@anime_router.get("/anime/{anime_id}", response_model=AnimeModel, tags=["Anime"], summary="Get anime information", description="Get anime information from **myanimelist**.", responses=responses, dependencies=[Depends(RateLimiter(times=100, seconds=10))])
def get_anime_info(
    anime_id: Annotated[int, Path(title="Anime ID", description="The `ID` of the anime from the **myanimelist**.", ge=1, le=100_000, example=20)]
) -> AnimeModel:
    def callback():
        return fetch_data(anime_id)
    return use_redis_cache(f"get_anime_info:{anime_id}", callback)
