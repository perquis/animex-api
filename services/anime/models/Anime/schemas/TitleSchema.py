from pydantic import BaseModel


class TitleSchema(BaseModel):
    english: str | None
    japanese: str | None
    synonyms: str | None