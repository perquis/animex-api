from models.Broadcast import Broadcast
from models.Demographics import Demographics
from models.Production import Production
from models.Stats import Stats
from models.Title import Title
from models.Urls import Urls
from pydantic import BaseModel


class Anime(BaseModel):
    title: Title
    urls: Urls
    broadcast: Broadcast
    stats: Stats
    demographics: Demographics
    production: Production
