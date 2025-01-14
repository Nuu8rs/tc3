import asyncio
from .account_factory import AccountFactory
from .account import Account

from accounts.services.account_service import AccountService
from .types import ResultJoinToChat

from accounts.logger.logger import logger

class AccountManager:
    accounts: dict[int, Account] = {}
    account_factory = AccountFactory()
    
    async def starting_accounts(self):
        all_accounts_info = await AccountService.get_all_accounts()
        for account_info in all_accounts_info:
            account = await self.account_factory.create_account(account_info)
            if not account:
                return 
            asyncio.create_task(account.start_listening())
            self.accounts[account.account_info.id] = account
            
            
    @classmethod
    async def delete_account_from_pool(cls, account:  Account):
        await account.disconnect()
        logger.info(f"Аккаунт {account.account_info.session_name} был удален из пула и отключен")
        cls.accounts.pop(account)
        
    @classmethod
    def get_all_accounts(cls) -> list[Account]:
        return cls.accounts.values()
        
    @classmethod
    async def account_join_to_chat(cls, account_id: int, chat_link: str, project_id: int) -> ResultJoinToChat:
        account: Account = cls.accounts.get(account_id, False)
        if not account:
            return
        
        chat_join_result:ResultJoinToChat  = await account.join_to_chat(chat_link, project_id)
        return chat_join_result
    
