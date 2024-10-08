from typing import Union

from pydantic import BaseModel


class ProductionSchema(BaseModel):
    studios: Union[list[str] | str | None]
    producers: Union[list[str] | str | None]
    licensors: Union[list[str] | str | None]