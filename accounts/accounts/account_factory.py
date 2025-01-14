import os
import traceback

from .account import Account

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from database.models.account_info import AccountInfo

from accounts.proxy.proxy_checker import ProxyChecker
from accounts.services.proxy_service import ProxyService

from accounts.logger.logger import logger


    
class AccountFactory:
    patch_to_session_folder = "accounts/sessions"
    
    async def create_account(self, account_info: AccountInfo) -> Account | None:
        try:
            logger.info(f"START CHECK PROXY FROM ACCOUNT {account_info.session_name}")
            proxy = await ProxyService.get_proxy(proxy_id=account_info.proxy_id)
            proxy_is_working = await ProxyChecker.check_proxy(
                proxy=proxy)
            
            if not proxy_is_working:
                logger.warning(f"Не смог создать аккаунт {account_info.session_name} , не работает прокси")
                return None
            
            logger.info(f"START CREATE ACCOUNT {account_info.session_name}")
            
        
            session_path = os.path.join(self.patch_to_session_folder, account_info.session_name)
            client = TelegramClient(session_path, account_info.api_id, 
                                    account_info.hash_id, proxy=proxy.socks_proxy) # 
            client.parse_mode = "html"
            await client.connect()
            if not await client.is_user_authorized():
                await self.authorize_account(client, account_info)
            
            if await client.is_user_authorized():
                logger.info(f"Аккаунт {account_info.session_name} успешно авторизован")
            else:
                logger.error(f"Не удалось авторизовать аккаунт {account_info.session_name}")
                return

            return Account(client=client,account_info=account_info)
        except Exception as E:
            logger.error(f"Ошибка в процессе работы с аккаунтом {account_info.session_name}: {E}")
            logger.error("Полная информация об ошибке: ")
            logger.error(traceback.format_exc())
    @staticmethod
    async def authorize_account(client: TelegramClient, account_info: AccountInfo) -> None:
        try:
            await client.send_code_request(phone = account_info.phone)
            code = input("enrty code: ")
            await client.sign_in(account_info.phone, code)
        except SessionPasswordNeededError:
            password = input("enter password code: ")
            await client.sign_in(password=password)
        except Exception as e:
            logger.error(f"DONT SIGIN IN ACCOUNT e: {e}")
            

