from pydantic import BaseModel


class Production(BaseModel):
    studios: list[str] | None
    producers: list[str] | None
    licensors: list[str] | None