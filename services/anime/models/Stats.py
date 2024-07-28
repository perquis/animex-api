from pydantic import BaseModel


class Stats(BaseModel):
    score: str | None
    ranked: str | None
    popularity: str | None
    members: str | None
    favorites: str | None