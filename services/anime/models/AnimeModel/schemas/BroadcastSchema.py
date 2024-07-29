from typing import Union

from enums.BroadcastType import BroadcastType
from pydantic import BaseModel


class BroadcastSchema(BaseModel):
    type: BroadcastType | None
    duration_per_episode: str | None
    episodes: Union[int | str | None]
    transmission: str | None
    status: str | None
    premiered: str | None
    rating: str | None
    aired: str | None