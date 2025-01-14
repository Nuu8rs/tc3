from sqlalchemy import Column, Integer, String, ForeignKey

from database.models.base import Base


class Auth(Base):
    __tablename__ = 'auth'

    id: int = Column(Integer, primary_key=True, index=True)
    token: str = Column(String(512), nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id', ondelete="cascade"))