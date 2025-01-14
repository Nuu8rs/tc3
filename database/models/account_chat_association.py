from database.models.base import Base, utcnow

from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, Integer

class AccountChatAssociation(Base):
    __tablename__ = "account_chat_association"
    id = Column(Integer, primary_key=True, index=True)
    
    account_id = Column(Integer, ForeignKey('account_info.id', name="fc_account_id_ACA", ondelete="cascade"))
    chat_id = Column(BigInteger, ForeignKey('chats.chat_id', name = "fc_chat_id_ACA", ondelete="cascade"))
    
    joined_time = Column(DateTime, server_default=utcnow())

