from pydantic import BaseModel, HttpUrl


class TopAnimeItem(BaseModel):
    anime_id: int
    rank: int
    score: float | None
    title: str
    poster_url: HttpUrl
    link_url: HttpUrl
