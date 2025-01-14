from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey, Enum

from database.models.constans import RolePermissionsEnum
from database.models.base import Base, utcnow

class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(256), nullable=False)
    login: str = Column(String(256), unique=True, index=True, nullable=True)
    hashed_password: str = Column(String(256), nullable=False, server_default="", default="")
    telegram_id: int = Column(BigInteger, nullable=True, server_default=None, default=None)
    creation_date: datetime = Column(DateTime, server_default=utcnow())
    subscription_id: int = Column(Integer, ForeignKey('subscriptions.id'), nullable=True, default=None)
    scopes: str = Column(Enum(RolePermissionsEnum), nullable=False, default=RolePermissionsEnum.USER)
    language: str = Column(String(5), nullable=False, default="ru", server_default="ru") 
    end_time_subscription = Column(DateTime, nullable=True, default=None)

    current_project = Column(Integer, nullable=True, default=None)