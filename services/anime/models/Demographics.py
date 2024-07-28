from typing import Union

from pydantic import BaseModel


class Demographics(BaseModel):
    type: str | None
    source: str | None
    genres: Union[list[str] | str | None]