from pydantic import BaseModel


class StatsSchema(BaseModel):
    score: float | None
    ranked: str | None
    popularity: str | None
    members: str | None
    favorites: str | None