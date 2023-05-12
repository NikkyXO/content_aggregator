from bs4 import BeautifulSoup
import requests
import os
from sqlalchemy.orm import Session
from app.settings.database import get_db
from app.models.articles import Article
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request


router = APIRouter(
    prefix='/articles',
    tags=['Article']
)

@router.post('/create')
async def create_article(url: str, db: Session = Depends(get_db)):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('title').get_text()
    db_article = Article(title=title, url=url)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return {'id': db_article.id, 'title': db_article.title, 'url': db_article.url}


@router.post('/{article_id}')
async def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail='Article not found')

    return {'id': article.id, 'title': article.title, 'url': article.url}