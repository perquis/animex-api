from pydantic import BaseModel


class Demographics(BaseModel):
    type: str | None
    source: str | None
    genres: list[str] | None