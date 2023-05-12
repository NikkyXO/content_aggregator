from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.settings.database import Base, engine


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(15), nullable=False)
    first_name = Column(String(30), nullable=False, default="firstname")
    last_name = Column(String(30), nullable=False, default="lastname")
    email = Column(String(100), nullable=False, unique=True)
    description = Column(String(400), nullable=True)
    password = Column(String(400), nullable=False)
    image_url = Column(String(300), default="default.jpg")
    location = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


Base.metadata.create_all(bind=engine)