
from sqlalchemy import Column, ForeignKey, Integer, String

from database.models.base import Base


class InvoicePendingChat(Base):
    __tablename__ = 'invoices_pending_chat'
    
    id: int         = Column(Integer, primary_key=True, index=True)
    project_id: int = Column(Integer, ForeignKey('projects.id', ondelete="cascade"))
    chat_link: str  = Column(String(256), nullable = False)
    chat_name: str  = Column(String(256), nullable = False) 