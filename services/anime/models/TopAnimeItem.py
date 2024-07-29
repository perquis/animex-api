from pydantic import BaseModel, HttpUrl


class TopAnimeItem(BaseModel):
    anime_id: int
    rank: int
    score: float
    title: str
    poster_url: HttpUrl
    link_url: HttpUrl
