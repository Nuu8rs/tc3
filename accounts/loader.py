from aiohttp import web
from accounts.accounts.account_manager import AccountManager
from accounts.accounts.accounts_validators import AccountValidator

from accounts.webhook_api.handlers import JoinToChat, DeleteChatViews


def add_web_endoints():
    application.router.add_post(path = "/add-chat-to-account", handler=JoinToChat.router)
    application.router.add_delete(path = "/delete-chat-views", handler=DeleteChatViews.router)



        
application = web.Application()
runner = web.AppRunner(application)

add_web_endoints()


account_manager = AccountManager()
account_validator = AccountValidator()
