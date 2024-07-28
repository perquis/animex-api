from pydantic import BaseModel


class UrlsSchema(BaseModel):
    poster: str | None
    trailer: str | None