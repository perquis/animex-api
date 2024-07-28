from pydantic import BaseModel

from .schemas.BroadcastSchema import BroadcastSchema
from .schemas.DemographicsSchema import DemographicsSchema
from .schemas.ProductionSchema import ProductionSchema
from .schemas.StatsSchema import StatsSchema
from .schemas.TitleSchema import TitleSchema
from .schemas.UrlsSchema import UrlsSchema


class AnimeModel(BaseModel):
    titles: TitleSchema
    urls: UrlsSchema
    synopsis: str
    broadcast: BroadcastSchema
    stats: StatsSchema
    demographics: DemographicsSchema
    production: ProductionSchema
