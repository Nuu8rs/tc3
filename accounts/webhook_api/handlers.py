from aiohttp.web import Request, Response
from accounts.accounts.account_manager import AccountManager
from accounts.accounts.types import ResultJoinToChat, ResultJoin

from database.models.account_info import AccountInfo
from accounts.services.chat_association_service import ChatAssociationService

from .base_endpoint import EndPoint, HTTPMethod
from .schemas import JoinToChatSchema, DeleteChatFromPool

from accounts.accounts.account import Account
from accounts.logger.logger import logger

class JoinToChat(EndPoint):
    schema = JoinToChatSchema
    method = HTTPMethod.POST
    data: JoinToChatSchema = None
    
    async def handle_request(self) -> Response:
        #TODO СДЕЛАТЬ ПРОВЕРКУ С АККАУНТ ЧАТ АСОЦ. НЕ БЫЛ ЛИ ДАННЫЙ ЧАТ УЖЕ ПОДКЛЮЧЕН СЮДА
        account: AccountInfo      = await ChatAssociationService.get_account_with_fewest_associations()
        result_join:  ResultJoinToChat = await AccountManager.account_join_to_chat(
            account_id = account.id,
            chat_link  = self.data.chat_link,
            project_id = self.data.project_id
        )
        if result_join.join_status in [ResultJoin.ALREADY_JOIN, ResultJoin.SUCCES_JOIN]:
            return self.OK(
                    message_join_result = result_join.message_answer,
                    chat_id    = result_join.chat_id,
                    project_id = self.data.project_id
            )
        return self.BAD(
            status  = 422,
            message_join_result = result_join.message_answer,
        )
        
class DeleteChatViews(EndPoint):
    schema = DeleteChatFromPool
    method = HTTPMethod.DELETE
    data: DeleteChatFromPool = None
    
    async def handle_request(self) -> Response:
        try:
            accounts: list[Account] = AccountManager.get_all_accounts()        
            for account in accounts:
                if self.data.chat_id in account.chat_account_manager.chats_views:
                    account.chat_account_manager.chats_views.remove(self.data.chat_id)
            
            return self.OK()
        except Exception as E:
            return self.BAD(status=500, message_error = E)