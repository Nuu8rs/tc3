import socks

from datetime import datetime
from database.models.base import Base
from sqlalchemy import Column, String, DateTime, Integer


class Proxy(Base):
    __tablename__ = "proxys"
    
    id         = Column(Integer, primary_key=True, index=True)
    
    ip         = Column(String(256), nullable=False)
    port       = Column(String(256), nullable=False)
    password   = Column(String(256), nullable=False)
    login      = Column(String(256), nullable=False)
    country    = Column(String(256), nullable=False)
    
    active_to = Column(DateTime, nullable=False)
    
    @property
    def is_active(self) -> bool:
        return self.active_to > datetime.now()
    
    @property
    def url_proxy(self) -> str:
        return f"socks5://{self.login}:{self.password}@{self.ip}:{self.port}"

    @property
    def socks_proxy(self) -> tuple:
        return (socks.SOCKS5, self.ip, int(self.port), True, self.login, self.password)
