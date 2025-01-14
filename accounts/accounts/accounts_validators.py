import asyncio

from .account import Account
from .account_manager import AccountManager
from .account_factory import AccountFactory

from accounts.logger.logger import logger

from tenacity import retry, stop_after_attempt, wait_fixed
from telethon.errors import SessionPasswordNeededError, RPCError

class AccountValidator:
    CHECK_INTERVAL = 1800 
    MAX_RETRY_ATTEMPTS_RELOAD_ACCOUNT = 3

        
    async def start_validation(self) -> None:        
        while True:
            await asyncio.sleep(self.CHECK_INTERVAL)
            await self.validation_accounts()
            
    
    async def validation_accounts(self):
        for _, account in AccountManager.accounts.items():
            await self.check_account_status(account)
    
    async def check_account_status(self, account: Account) -> None:
        try:
            if not account.client.is_connected():
                logger.warning(f"Аккаунт {account.account_info.session_name} не подключён, восстанавливаем...")
                await self.try_to_restore_account()

            elif not await account.client.is_user_authorized():
                logger.warning(f"Аккаунт {account.account_info.session_name} не авторизован, требуется повторная авторизация...")
                await self.try_to_restore_account(requires_authorization=True)

            else:
                logger.info(f"Аккаунт {account.account_info.session_name} работает нормально.")

        except RPCError as rpc_error:
            logger.error(f"RPC ошибка для аккаунта {account.account_info.session_name}: {rpc_error}")
            await AccountManager.delete_account_from_pool(account)


        except Exception as e:
            logger.error(f"Непредвиденная ошибка для аккаунта {account.account_info.session_name}: {e}")
            await AccountManager.delete_account_from_pool(account)

    @retry(stop=stop_after_attempt(MAX_RETRY_ATTEMPTS_RELOAD_ACCOUNT), wait=wait_fixed(10))
    async def try_to_restore_account(self, account: Account, requires_authorization=False) -> None:
        try:
            await account.client.connect()
            
            if requires_authorization:
                if not await account.client.is_user_authorized():
                    logger.warning(f"Требуется повторная авторизация для аккаунта {account.account_info.session_name}.")
                    await AccountFactory.authorize_account(account.client, account.account_info)

            logger.info(f"Аккаунт {account.account_info.session_name} успешно восстановлен.")

        except SessionPasswordNeededError:
            logger.error(f"Для аккаунта {account.account_info.session_name} требуется пароль двухфакторной аутентификации.")
            password = input(f"Введите пароль для двухэтапной аутентификации для {account.account_info.phone}: ")
            await account.client.sign_in(password=password)

        except RPCError as rpc_error:
            logger.error(f"RPC ошибка во время восстановления аккаунта {account.account_info.session_name}: {rpc_error}")
            raise  

        except Exception as e:
            logger.error(f"Не удалось восстановить аккаунт {account.account_info.session_name}: {e}")
            await AccountManager.delete_account_from_pool(account)
        