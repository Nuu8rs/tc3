def get_base():
    from database.models.base import Base
    from database.models.auth import Auth
    from database.models.chats import Chat, ProjectChatAssociation
    from database.models.posts import Media, Post, Views, Subscribers
    from database.models.subscriptions import Subscription
    from database.models.users import User
    from database.models.account_info import AccountInfo
    from database.models.account_chat_association import AccountChatAssociation
    from database.models.invoice_pending_chat import InvoicePendingChat
    from database.models.proxy import Proxy
    from database.models.projects import Project
    
    return Base