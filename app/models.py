from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # user = Column(String, server_default='nice', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete='CASCADE'), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    joined_at = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)


class Votes(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    vote_value = Column(Integer, nullable=False)
