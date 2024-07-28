from pydantic import BaseModel


class BroadcastSchema(BaseModel):
    type: str | None
    duration_per_episode: str | None
    episodes: str | None
    transmission: str | None
    status: str | None
    premiered: str | None
    rating: str | None
    aired: str | None