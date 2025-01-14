from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger

from database.models.base import Base, utcnow


class Project(Base):
    __tablename__ = 'projects'

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey('users.id', ondelete="cascade"))
    chat_id: int = Column(BigInteger, nullable=False)
    chat_name: str = Column(String(128), nullable=False)
    creation_date: datetime = Column(DateTime, server_default=utcnow())
    description_text = Column(String(256), nullable=True)
