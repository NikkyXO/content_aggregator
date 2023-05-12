from sqlalchemy import Column, Integer, String, DateTime
from app.settings.database import Base


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    name = Column(String(255))
    description = Column(String(255))
    url = Column(String(255))
    pub_date = Column(DateTime)
    # image
