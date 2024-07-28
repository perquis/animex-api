from pydantic import BaseModel, HttpUrl


class UrlsSchema(BaseModel):
    poster: HttpUrl | None
    trailer: HttpUrl | None