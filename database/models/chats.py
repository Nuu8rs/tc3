from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, BigInteger, DateTime

from database.models.base import Base, utcnow


class Chat(Base):
    __tablename__ = 'chats'

    chat_id: int = Column(BigInteger, nullable=False, index=True, unique=True, primary_key=True)
    chat_link: str = Column(String(64), nullable=False)
    chat_name: str = Column(String(128), nullable=False)
    chat_type: str = Column(Enum("CHAT", "CHANNEL", name="type_chat"), nullable=False)


class ProjectChatAssociation(Base):
    __tablename__ = "project_сhat_associations"
    
    id: int                 = Column(Integer, primary_key=True, index=True)
    project_id: int         = Column(Integer, ForeignKey('projects.id', name="fc_project_chat_association_PROJECT_ID", ondelete="cascade"))
    chat_id: int            = Column(BigInteger, ForeignKey("chats.chat_id", name="fc_project_chat_association_CHAT_ID", ondelete="cascade"), nullable=False)
    auto_post: bool         = Column(Boolean, nullable=False, default=False, server_default="0")
    creation_date: datetime = Column(DateTime, server_default=utcnow())

    pinned: bool            = Column(Boolean, default=False, server_default="0")
