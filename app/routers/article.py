from bs4 import BeautifulSoup
import requests
from sqlalchemy.orm import Session
from app.settings.database import get_db
from app.models.articles import Article
from app.schemas.user_schema import User
from app.settings.oauth import get_current_active_user
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.routers.news_queries import QueryManager
from typing import Optional, Annotated

router = APIRouter(
    prefix='/articles',
    tags=['Article']
)


@router.post('/news')
def list_news(current_user: Annotated[User, Depends(get_current_active_user)],
              q: Optional[str] = None, limit: int = 10):
    """
    This endpoint will serve for both getting the news listings and search functionality.
    :param current_user:
    :param q: search query to be passed to the request url.
    :param limit: Integer number to limit number of results to fetch from each dependent API.
    :return: JSON response of aggregated results.
    """
    manager = QueryManager(q, limit)
    try:
        if q:
            # call search endpoint
            result = manager.search_news_query()
        else:
            # call news listing endpoint
            result = manager.get_news_query()
        return result
    except:
        raise HTTPException(400, "something went wrong/ Bad request")


@router.post('/create')
async def create_article(db: Session = Depends(get_db)):
    url = "https://www.bbc.com/news"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print("name here", soup.name)
    print("soup string", soup.string)

    title = soup.find('title').get_text()

    links = [link.get('href') for link in soup.findAll('a')]
    print("links here", links)

    # print(soup.get_text())
    print("title here", title)

    results = soup.find_all("h3", class_="gs-c-promo-heading__title")
    news = []
    for result in results:
        news.append(result.text.strip())
    return {"news": news}

    # db_article = Article(title=title, url=url)
    # db.add(db_article)
    # db.commit()
    # db.refresh(db_article)
    # return {'id': db_article.id, 'title': db_article.title, 'url': db_article.url}


@router.post('/{article_id}')
async def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail='Article not found')

    return {'id': article.id, 'title': article.title, 'url': article.url}
