import os
from typing import Any, Optional
from dotenv import find_dotenv, load_dotenv
from app.utils.exceptions import ThirdPartyAPIConnectionError
from app.utils.third_party_api import EXTERNAL_SOURCES_CONFIG, API_COLLECTION
from app.utils.news_call import RequestClient


class QueryManager:
    def __init__(self, query: Optional[str] = None, limit: int = 10) -> None:
        """Initialization values."""
        self.query: str = query
        self.limit: int = limit
        self.response_data: list = []
        self.response_status: bool = False
        self.news_api_key: str = os.getenv("NEWS_API_KEY")
        self.error = None

    def search_news_query(self) -> list[dict[str, Any]]:
        """function to get search results for a given QUERY from all registered APIs (in API_COLLECTION)."""
        all_data_list: list = []
        reddit_list = []
        news_api_list = []

        for api_sources in API_COLLECTION:
            try:
                request_client = RequestClient("NewsList")
                response = request_client.request(
                    method="get",
                    url=EXTERNAL_SOURCES_CONFIG[api_sources]["search_url"].format(
                        query=self.query, limit=self.limit
                    ),
                    headers={
                        "x-api-key": EXTERNAL_SOURCES_CONFIG[api_sources]["access_key"],
                        "Content-Type": "application/json",
                        "User-agent": "your bot 0.1",
                    },
                )

                # if the source of data is new_api and response.response_data["articles"] is not None
                if (
                    EXTERNAL_SOURCES_CONFIG[api_sources]["source"] == "newsapi"
                    and response.response_data["articles"] is not None
                ):
                    for data in response.response_data["articles"]:
                        news_api_list.append(
                            {
                                "title": data["title"],
                                "link": data["url"],
                                "source": EXTERNAL_SOURCES_CONFIG[api_sources][
                                    "source"
                                ],
                            }
                        )
                    all_data_list += news_api_list

                # if the source of data is reddit esponse.response_data["data"]["children"] is not None
                elif (
                    EXTERNAL_SOURCES_CONFIG[api_sources]["source"] == "reddit"
                    and response.response_data["data"]["children"] is not None
                ):
                    for data in response.response_data["data"]["children"]:
                        reddit_list.append(
                            {
                                "title": data["data"]["title"],
                                "link": data["data"]["url"],
                                "source": EXTERNAL_SOURCES_CONFIG[api_sources][
                                    "source"
                                ],
                            }
                        )
                    all_data_list += reddit_list
                else:
                    all_data_list = []
            except ThirdPartyAPIConnectionError as error:
                # return error.response_data
                pass

        self.response_data += all_data_list
        return self.response_data

    def get_news_query(self) -> list[dict[str, Any]]:
        """For fetching list of data from any Reddit and News_Api endpoints"""
        all_data_list: list = []
        reddit_list = []
        news_api_list = []

        for api_sources in API_COLLECTION:
            try:
                request_client = RequestClient("NewsList")
                response = request_client.request(
                    method="get",
                    url=EXTERNAL_SOURCES_CONFIG[api_sources]["listing_url"].format(
                        limit=self.limit
                    ),
                    headers={
                        "x-api-key": EXTERNAL_SOURCES_CONFIG[api_sources]["access_key"],
                        "Content-Type": "application/json",
                        "User-agent": "your bot 0.1",
                    },
                )

                # if the source of data is new_api and response is not None
                if (
                    EXTERNAL_SOURCES_CONFIG[api_sources]["source"] == "newsapi"
                    and response.response_data["articles"] is not None
                ):
                    for data in response.response_data["articles"]:
                        news_api_list.append(
                            {
                                "title": data["title"],
                                "link": data["url"],
                                "source": EXTERNAL_SOURCES_CONFIG[api_sources][
                                    "source"
                                ],
                            }
                        )
                    all_data_list += news_api_list

                # if the source of data is reddit esponse.response_data["data"]["children"] is not None
                elif (
                    EXTERNAL_SOURCES_CONFIG[api_sources]["source"] == "reddit"
                    and response.response_data["data"]["children"] is not None
                ):
                    for data in response.response_data["data"]["children"]:
                        reddit_list.append(
                            {
                                "title": data["data"]["title"],
                                "link": data["data"]["url"],
                                "source": EXTERNAL_SOURCES_CONFIG[api_sources][
                                    "source"
                                ],
                            }
                        )
                    all_data_list += reddit_list
                else:
                    all_data_list = []
            except ThirdPartyAPIConnectionError as error:
                # return error.response_data
                pass

        self.response_data += all_data_list
        return self.response_data