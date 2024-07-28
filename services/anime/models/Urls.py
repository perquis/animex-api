from pydantic import BaseModel


class Urls(BaseModel):
    poster: str | None
    trailer: str | None