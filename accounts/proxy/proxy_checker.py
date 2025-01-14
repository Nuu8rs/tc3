from database.models.proxy import Proxy
from accounts.api.client import Client

from accounts.logger.logger import logger

class ProxyChecker:
    api_url = 'https://ipinfo.io/json'
    
    @classmethod
    async def check_proxy(cls, proxy: Proxy) -> bool:
            if not proxy.is_active:
                return False
            
            response_check_proxy = await Client.send_request(
                url=cls.api_url,
                proxy= proxy.url_proxy
            )
            
            if response_check_proxy.get('error', False):
                #TODO send error message
                return False
            
            if response_check_proxy['ip'] != proxy.ip or response_check_proxy['country'] != proxy.country:
                #TODO send error message
                return False
            logger.info(response_check_proxy)
            return True 