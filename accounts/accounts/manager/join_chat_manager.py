from telethon import TelegramClient 

from telethon.errors.rpcerrorlist import (
    InviteHashEmptyError,
    InviteHashExpiredError,
    InviteHashInvalidError,
    InviteRequestSentError,
    UserAlreadyParticipantError
    ) 
from database.models.account_info import AccountInfo 
from telethon.tl.functions.channels import JoinChannelRequest  
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import Channel, Chat, ChatInvite
from telethon.tl.functions.messages import CheckChatInviteRequest

from accounts.accounts.types import ResultJoinToChat, ResultJoin

from accounts.services.chat_service import ChatService
from accounts.services.invoice_pending_chat_service import InvoicePendingChatService

from typing import Optional

from accounts.logger.logger import logger


class JoinChatManager:
    def __init__(self, client: TelegramClient, account_info: AccountInfo):
        self.client:TelegramClient = client
        self.account_info: AccountInfo = account_info
        self.logger_prefix: str = f"[Аккаунт {account_info.session_name}] "

    def _is_invite_link(self, chat_link: str) -> bool:
        invite_indicators = ['+', 'joinchat']
        return any(indicator in chat_link for indicator in invite_indicators)        

    def _extract_invite_hash(self, chat_link: str) -> str | None:
        try:
            hash_part = chat_link.rstrip('/').split('/')[-1]
            invite_hash = ''.join(filter(lambda x: x.isalnum() or x in '-_', hash_part))
            return invite_hash if invite_hash else None
        except IndexError:
            return None

    async def _already_join(
        self, 
        chat_link: str,
    ) -> ResultJoinToChat:
        success_msg = "Успешно подключён к публичному чату: {chat_link}"

        chat_entity = await self.client.get_entity(chat_link)
           
        type_chat = await self._get_type_chat(
            entity = chat_entity
        )
        return ResultJoinToChat(
            message_answer=success_msg,
            join_status=ResultJoin.ALREADY_JOIN,
            chat=chat_entity,
            type_chat=type_chat
                )

    async def _get_type_chat(self, chat_id: int = None, entity = None) -> str:
        if not entity: 
            entity = await self.client.get_entity(chat_id)
        if isinstance(entity, Channel):
            if entity.megagroup:
                type_chat = "CHAT"    #ГРУППА
            else:
                type_chat = "CHANNEL" #КАНАЛ
        elif isinstance(entity, Chat):
            type_chat = "CHAT"        #ГРУППА
        else:
            raise Exception("Неверный тип чата")
        return type_chat

    async def join_to_chat(self, chat_link: str, project_id: int) -> ResultJoinToChat:
        
        if self._is_invite_link(chat_link):
            logger.info("INVITE")
            return await self.__join_by_invite(chat_link, project_id)
        else:
            logger.info("PUBLIC")
            return await self.__join_to_public_chat(chat_link)
    

    async def __join_to_public_chat(self, chat_link: str) -> ResultJoinToChat:
        try:
            result = await self.client(JoinChannelRequest(chat_link)) #type: ignore
            logger.info(result)
            type_chat = await self._get_type_chat(chat_id = result.chats[0].id) #type: ignore
            success_msg = "Успешно подключён к публичному чату: {chat_link}"
            logger.info(self.logger_prefix + success_msg.format(chat_link=chat_link))
            
            chat = await ChatService.get_chat(
                chat_id = result.chats[0].id
            )
            
            if not chat:
                join_status = ResultJoin.SUCCES_JOIN
            
            else:
                join_status = ResultJoin.ALREADY_JOIN
            
            return ResultJoinToChat(
                message_answer = success_msg,
                join_status    = join_status,
                chat           = result,
                type_chat      = type_chat
                    )

        except UserAlreadyParticipantError as E:
            return await self._already_join(
                chat_link = chat_link
            )

        except Exception as e:
            return await self._handle_exception(e, chat_link)

    async def __join_by_invite(self, chat_link: str, project_id: int) -> ResultJoinToChat:
        invite_hash = None
        success_msg = "Успешно подключён к чату/группе: {chat_link}"
        try:
            invite_hash = self._extract_invite_hash(chat_link)
            if not invite_hash:
                error_msg = "Неверная форма ссылки-приглашения: {chat_link}"
                logger.error(self.logger_prefix  + error_msg.format(chat_link=chat_link))
                raise InviteHashInvalidError#type: ignore
                
            result = await self.client(ImportChatInviteRequest(hash = invite_hash))
            
            logger.info(success_msg.format(chat_link=chat_link))
            type_chat = await self._get_type_chat(chat_id = result.chats[0].id)


            return ResultJoinToChat(
                message_answer=success_msg,
                join_status=ResultJoin.SUCCES_JOIN,
                chat=result,
                type_chat=type_chat
                    )
            
        except UserAlreadyParticipantError as E:
            return await self._already_join(
                chat_link   = chat_link,
            )

        except InviteRequestSentError as E:
            return await self.add_to_pool_wait_join_chat(
                invite_hash = invite_hash,
                project_id = project_id,
                chat_link = chat_link
            )
            

        except Exception as e:
            return await self._handle_exception(e, chat_link)
        
    async def _handle_exception(self, e:Exception, chat_link:str) -> ResultJoinToChat:
        default_error_msg = "Ошибка при подключении к чату {chat_link}: {e}"
    
        error_messages = {
            InviteHashEmptyError:        "Пустая ссылка-приглашение: {chat_link}",
            InviteHashExpiredError:      "Ссылка-приглашение истекла: {chat_link}",
            InviteHashInvalidError:      "Неверная ссылка-приглашение: {chat_link}",
        }
        error_msg = error_messages.get(type(e), default_error_msg)
        
        logger.error(
            self.logger_prefix + error_msg.format(chat_link = chat_link, e=e)
        )
        return ResultJoinToChat(
                message_answer = error_msg,
                join_status    = ResultJoin.FAILED_JOIN,
                    )
            
    async def add_to_pool_wait_join_chat(
            self, 
            chat_link:str, 
            invite_hash: Optional[str], 
            project_id: int
                    ) -> ResultJoinToChat:
        invite = await self.client(CheckChatInviteRequest(hash = invite_hash))
        chat_name = None
        result_join = ResultJoinToChat(
                        message_answer = "Ошибка отправки подключению к чату",
                        join_status = ResultJoin.FAILED_JOIN,
                    )
        
        if not isinstance(invite, ChatInvite):
            return result_join
        
        chat_name = invite.title
        
        if not chat_name:
            return result_join
        
        invoice = await InvoicePendingChatService.add_new_invoice(
            project_id = project_id,
            chat_name  = chat_name,
            chat_link  = chat_link
        )
        if not invoice:
            return result_join

        return ResultJoinToChat(
                        message_answer = (
                        "Аккаунт подал заявку в канал. "
                        "Ожидайте, пока администратор группы примет вашу заявку: {chat_link}"
                                        ),
                        join_status = ResultJoin.FAILED_JOIN,
                    )