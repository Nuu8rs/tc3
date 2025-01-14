import asyncio
import aiohttp

from aiohttp import ClientError, ClientResponseError, ClientConnectorError, ClientTimeout
from typing import Optional

class Client:
    timeout = ClientTimeout(total=20)
    
    @classmethod
    async def send_request(cls, url: str, proxy: Optional[str]):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, proxy=proxy, timeout=cls.timeout) as response:
                    if response.status == 200:
                        return await response.json() 
                    else:
                        return {'error': f"Статус ответа: {response.status}"}
            except ClientResponseError as e:
                return {'error' : f"HTTP ошибка: {e.status} - {e.message}"}
            except ClientConnectorError as e:
                return {'error' : f"Ошибка подключения {e}"}
            except asyncio.TimeoutError as e:
                return {'error' : f"Запрос превысил время ожидания {e}"}
            except ClientError as e:
                return {'error' : f"Клиентская ошибка {e}"}
            except Exception as e:
                return {'error': str(e)}