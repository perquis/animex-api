from pydantic import BaseModel


class Title(BaseModel):
    english: str | None
    japanese: str | None
    synonyms: str | None