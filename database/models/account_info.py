from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Integer

from database.models.base import Base, utcnow


class AccountInfo(Base):
    
    __tablename__ = "account_info"
    
    id = Column(Integer, primary_key=True, index=True)
    
    api_id:int       = Column(BigInteger(), nullable=False)
    hash_id:str      = Column(String(60), nullable=False)
    phone:str        = Column(String(20), nullable=False)
    
    session_name:str     =  Column(String(100), nullable=False)    
    patch_to_session:str = Column(String(100), nullable=True)
    
    created_time:datetime = Column(DateTime, default=utcnow())
    
    proxy_id:int     = Column(Integer, ForeignKey('proxys.id', name="fk_proxy_id"))


    @property
    def prefix_log(self) -> str:
        return f"Account [{self.session_name}]"