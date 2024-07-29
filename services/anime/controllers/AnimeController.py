import logging
from typing import Dict, Optional
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from enums.TopAnimeType import TopAnimeType
from fastapi import HTTPException
from models import AnimeModel
from utils.process_data import process_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_html(url: str) -> str:
    """Fetch the HTML content from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.HTTPError:
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Anime not found")
        else:
            raise HTTPException(status_code=500, detail=f"Internal server error")
    except requests.RequestException:
        raise HTTPException(status_code=500, detail=f"Internal server error")

def create_soup_instance(html_doc: str) -> Optional[BeautifulSoup]:
    """Create a BeautifulSoup instance from HTML content."""
    if not html_doc:
        return None
    return BeautifulSoup(html_doc, 'html.parser')

def find_left_sidebar(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
    """Find and return the left sidebar element."""
    left_sidebar = soup.find(class_="borderClass")
    if not left_sidebar:
        logger.warning("Left sidebar not found.")
    return left_sidebar

def extract_info_from_detail(detail: str) -> Dict[str, str]:
    """Extract key-value pair from detail text."""
    key, _, value = detail.partition(":")
    if not key or not value:
        logger.warning(f"Invalid detail format: {detail}")
        return {}
    return {key.strip().lower(): value.strip()}

def filter_genre_spans(soup: BeautifulSoup) -> BeautifulSoup:
    """Remove span elements with itemprop="genre" from the BeautifulSoup instance."""
    for span in soup.find_all('span', itemprop="genre"):
        span.decompose()
    return soup

def get_details_list_from_left_sidebar(soup: BeautifulSoup) -> Dict[str, str]:
    """Get a dictionary of details from the left sidebar, excluding genre spans."""
    left_sidebar = find_left_sidebar(soup)
    if not left_sidebar:
        return {}

    left_sidebar = filter_genre_spans(left_sidebar)

    information_details = left_sidebar.find_all(class_="spaceit_pad")
    details = {}

    for detail in information_details:
        detail_text = detail.get_text(separator=" ", strip=True)
        info = extract_info_from_detail(detail_text)
        if info:
            details.update(info)

    return details

def get_anime_poster(soup: BeautifulSoup) -> Optional[str]:
    """Get the URL of the anime poster."""
    poster_img = soup.find("img", {'data-src': True})
    if not poster_img:
        logger.warning("Anime poster not found.")
    return poster_img['data-src'] if poster_img else None

def get_anime_trailer(soup: BeautifulSoup) -> Optional[str]:
    """Get the URL of the anime trailer."""
    trailer = soup.find("a", {"class": "iframe js-fancybox-video video-unit promotion"})
    if not trailer:
        logger.warning("Anime trailer not found.")
    return trailer["href"] if trailer else None

def get_synopsis(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    """Get the synopsis of the anime."""
    synopsis = soup.find("p", itemprop="description")
    if not synopsis:
        logger.warning("Anime synopsis not found.")
    return synopsis.get_text(separator=" ", strip=True).replace(" [Written by MAL Rewrite]", "") if synopsis else None

def get_stats(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    """Get the stats of the anime."""
    stats = {}
    ranked = soup.find("span", {"class": "numbers ranked"}).get_text(separator=" ", strip=True).replace("Ranked ", "")
    score = soup.find("div", {"data-title": "score"}).get_text(separator=" ", strip=True)
    stats["score"] = float(score) if score != "N/A" else None
    stats["ranked"] = ranked

    return stats

def get_anime_object(url: str) -> Dict[str, Optional[str]]:
    """Compile all anime information into a dictionary."""
    html_doc = fetch_html(url)
    soup = create_soup_instance(html_doc)
    if not soup:
        return {}

    data_from_left_sidebar = get_details_list_from_left_sidebar(soup)
    synopsis = get_synopsis(soup)
    episodes = data_from_left_sidebar.get("episodes")

    stats = get_stats(soup)

    return {
        "anime_id": int(url.split("/")[-1]),
        "titles": {
            "synonyms": data_from_left_sidebar.get("synonyms", None),
            "english": data_from_left_sidebar.get("english", None),
            "japanese": data_from_left_sidebar.get("japanese", None),
        },
        "synopsis": synopsis,
        "urls": {
            "poster": get_anime_poster(soup),
            "trailer": get_anime_trailer(soup),
        },
        "broadcast": {
            "type": data_from_left_sidebar.get("type", None),
            "duration_per_episode": data_from_left_sidebar.get("duration", None),
            "episodes": episodes if episodes in "Unknown" else int(episodes) if episodes else None,
            "transmission": data_from_left_sidebar.get("broadcast", None),
            "status": data_from_left_sidebar.get("status", None),
            "premiered": data_from_left_sidebar.get("premiered", None),
            "rating": data_from_left_sidebar.get("rating", None),
            "aired": data_from_left_sidebar.get("aired", None),
        },
        "stats": {
            "popularity": data_from_left_sidebar.get("popularity", None),
            "ranked": stats.get("ranked", None),
            "score": stats.get("score", None),
            "members": data_from_left_sidebar.get("members", None),
            "favorites": data_from_left_sidebar.get("favorites", None),
        },
        "demographics": {
            "type": data_from_left_sidebar.get("demographic", None),
            "source": data_from_left_sidebar.get("source", None),
            "genres": data_from_left_sidebar.get("genres", None),
        },
        "production": {
            "producers": data_from_left_sidebar.get("producers", None),
            "licensors": data_from_left_sidebar.get("licensors", None),
            "studios": data_from_left_sidebar.get("studios", None),
        },
    }

def get_top_anime_list(anime_type: TopAnimeType, page: int):
    top_anime_list_url = "https://myanimelist.net/topanime.php"
    params = {}

    if anime_type:
        params['type'] = anime_type.value
    if page > 1:
        params['limit'] = (page - 1) * 50

    top_anime_list_url += '?' + urlencode(params)

    html_doc = requests.get(top_anime_list_url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    
    items = soup.find_all("tr", class_="ranking-list")
    top_anime_list = []
    
    for item in items:
        rank = item.find("td", class_="rank ac").get_text().strip()
        details = item.find("td", class_="title al va-t word-break")
        link = details.find("a")
        poster_url = link.find("img")["data-src"]
        link_url = link["href"]
        title = details.find("h3").get_text()
        anime_id = int(link_url.split("/")[-2])
        score = item.find("div", class_="js-top-ranking-score-col di-ib al").find("span").get_text().strip()
        
        top_anime_list.append({
            "anime_id": anime_id, 
            "rank": int(rank), 
            "score": float(score) if score != "N/A" else None, 
            "title": title,
            "poster_url": poster_url, 
            "link_url": link_url
        })

    return top_anime_list

def fetch_data(anime_id: int) -> AnimeModel:
    url = f"https://myanimelist.net/anime/{anime_id}"
    anime_instance = get_anime_object(url)

    process_data(anime_instance['production'])
    process_data(anime_instance['demographics'])

    return anime_instance