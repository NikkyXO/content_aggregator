import os
from typing import Any, Dict

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

NEWS_API_CONFIG = 1
REDDIT_API_CONFIG = 2

EXTERNAL_SOURCES_CONFIG: Dict[int, Dict[str, Any]] = {
    NEWS_API_CONFIG: {
        "api_name": "newsapi",
        "source": "newsapi",
        "listing_url": "http://newsapi.org/v2/top-headlines?category=general&pageSize={limit}&page=1",
        "search_url": "http://newsapi.org/v2/everything?q='{query}'&pageSize='{limit}'&page=1",
        "access_key": os.getenv("NEWS_API_KEY"),
    },
    REDDIT_API_CONFIG: {
        "api_name": "reddit",
        "source": "reddit",
        "listing_url": ("https://www.reddit.com/r/news/top.json?" "limit={limit}"),
        "search_url": "https://www.reddit.com/r/news/search.json?"
        "q={query}&"
        "limit={limit}",
        "access_key": "",
    },
}

API_COLLECTION = [NEWS_API_CONFIG, REDDIT_API_CONFIG]