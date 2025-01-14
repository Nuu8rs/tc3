from sqlalchemy import Column, Integer, String, Float

from database.models.base import Base


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(256), nullable=False)
    features: str = Column(String(256))
    price: float = Column(Float)
