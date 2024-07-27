import logging
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

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

def get_anime_object(url: str) -> Dict[str, Optional[str]]:
    """Compile all anime information into a dictionary."""
    html_doc = fetch_html(url)
    soup = create_soup_instance(html_doc)
    if not soup:
        return {}

    data_from_left_sidebar = get_details_list_from_left_sidebar(soup)

    return {
        "title": {
            "synonyms": data_from_left_sidebar.get("synonyms", None),
            "english": data_from_left_sidebar.get("english", None),
            "japanese": data_from_left_sidebar.get("japanese", None),
        },
        "urls": {
            "poster": get_anime_poster(soup),
            "trailer": get_anime_trailer(soup),
        },
        "broadcast": {
            "type": data_from_left_sidebar.get("type", None),
            "duration_per_episode": data_from_left_sidebar.get("duration", None),
            "episodes": data_from_left_sidebar.get("episodes", None),
            "transmission": data_from_left_sidebar.get("broadcast", None),
            "status": data_from_left_sidebar.get("status", None),
            "premiered": data_from_left_sidebar.get("premiered", None),
            "rating": data_from_left_sidebar.get("rating", None),
            "aired": data_from_left_sidebar.get("aired", None),
        },
        "stats": {
            "popularity": data_from_left_sidebar.get("popularity", None),
            "ranked": data_from_left_sidebar.get("ranked", None),
            "score": data_from_left_sidebar.get("score", None),
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
