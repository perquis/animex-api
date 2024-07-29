from pydantic import BaseModel, Field

from .schemas.BroadcastSchema import BroadcastSchema
from .schemas.DemographicsSchema import DemographicsSchema
from .schemas.ProductionSchema import ProductionSchema
from .schemas.StatsSchema import StatsSchema
from .schemas.TitleSchema import TitleSchema
from .schemas.UrlsSchema import UrlsSchema


class AnimeModel(BaseModel):
    anime_id: int
    titles: TitleSchema
    urls: UrlsSchema
    synopsis: str
    broadcast: BroadcastSchema
    stats: StatsSchema
    demographics: DemographicsSchema
    production: ProductionSchema

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "anime_id": 20,
                    "titles": {
                        "english": "Naruto",
                        "japanese": "ナルト",
                        "synonyms": "NARUTO"
                    },
                    "urls": {
                        "poster": "https://cdn.myanimelist.net/images/anime/1141/142503.jpg",
                        "trailer": None
                    },
                    "synopsis": "Moments before Naruto Uzumaki's birth, a huge demon known as the Nine-Tailed Fox attacked Konohagakure, the Hidden Leaf Village, and wreaked havoc. In order to put an end to the demon's rampage, the leader of the village, the Fourth Hokage, sacrificed his life and sealed the monstrous beast inside the newborn Naruto. In the present, Naruto is a hyperactive and knuckle-headed ninja growing up within Konohagakure. Shunned because of the demon inside him, Naruto struggles to find his place in the village. His one burning desire to become the Hokage and be acknowledged by the villagers who despite him. However, while his goal leads him to unbreakable bonds with lifelong friends, it also lands him in the crosshairs of many deadly foes.",
                    "broadcast": {
                        "type": "TV",
                        "duration_per_episode": "23 min. per ep.",
                        "episodes": 220,
                        "transmission": "Thursdays at 19:30 (JST)",
                        "status": "Finished Airing",
                        "premiered": "Fall 2002",
                        "rating": "PG-13 - Teens 13 or older",
                        "aired": "Oct 3, 2002 to Feb 8, 2007"
                    },
                    "stats": {
                        "score": 8,
                        "ranked": "#644",
                        "popularity": "#8",
                        "members": "2,883,979",
                        "favorites": "80,668"
                    },
                    "demographics": {
                        "type": "Shounen",
                        "source": "Manga",
                        "genres": [
                        "Action",
                        "Adventure",
                        "Fantasy"
                        ]
                    },
                    "production": {
                        "studios": "Pierrot",
                        "producers": [
                        "TV Tokyo",
                        "Aniplex",
                        "Shueisha"
                        ],
                        "licensors": "VIZ Media"
                    }
                }
            ]
        }
    }
