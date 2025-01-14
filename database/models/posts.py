from datetime import datetime, timezone
from sqlalchemy import Column, Enum, Integer, String, ForeignKey, DateTime, Boolean, BigInteger

from app.constants import DEFAULT_THUMBNAIL
from database.models.constans import PostStatusEnum, MediaTypeEnum
from database.models.base import Base, utcnow


class Post(Base):
    __tablename__ = 'posts'

    id: int = Column(Integer, primary_key=True, index=True)
    chat_id: int = Column(BigInteger, ForeignKey('chats.chat_id', ondelete="cascade"))
    message_id: int | None = Column(Integer, nullable=True) # if will be added website parsing
    text: str | None = Column(String(4096), nullable=True) # if post is a photo without caption
    creation_date: datetime = Column(DateTime, server_default=utcnow())
    project_id: int | None = Column(
        Integer,
        ForeignKey(
            'projects.id',
            ondelete="cascade",
            name="fc_custom_post_project_id"
        ),
        nullable=True,
        default=None
    )
    was_changed: str = Column(Enum(PostStatusEnum), nullable=False, default=PostStatusEnum.NOT_CHANGED)
    thumbnail_url: str = Column(String(256), default=DEFAULT_THUMBNAIL)


class Media(Base):
    __tablename__ = 'medias'

    id: int = Column(Integer, primary_key=True, index=True)
    post_id: int = Column(Integer, ForeignKey('posts.id', ondelete="cascade"))
    file_url: str = Column(String(256), nullable=False)
    file_type: str = Column(Enum(MediaTypeEnum), nullable=False, default=MediaTypeEnum.PHOTO)


class Views(Base):
    __tablename__ = 'views'
    
    id: int = Column(Integer, primary_key=True, index=True)
    chat_id: int = Column(BigInteger, ForeignKey('chats.chat_id', ondelete="cascade"))
    message_id: int = Column(Integer)
    views: int = Column(Integer, nullable=False)
    tracking_time: datetime = Column(DateTime, server_default=utcnow())


class Subscribers(Base):
    __tablename__ = 'subscribers'
    
    id: int = Column(Integer, primary_key=True, index=True)
    chat_id: int = Column(BigInteger, ForeignKey('chats.chat_id', ondelete="cascade"))
    subscribers: int = Column(Integer, nullable=False)
    tracking_time: datetime = Column(DateTime, server_default=utcnow())
