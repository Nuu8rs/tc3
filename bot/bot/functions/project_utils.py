import re

def is_telegram_chat_link(link: str) -> bool:
    pattern = re.compile(
        r'^(https:\/\/t\.me\/(?:\+[a-zA-Z0-9_-]+|[a-zA-Z0-9_-]+)|t\.me\/(?:\+[a-zA-Z0-9_-]+|[a-zA-Z0-9_-]+)|tg:\/\/join\?invite=[a-zA-Z0-9_-]+)$',
        re.IGNORECASE
    )
    
    return bool(pattern.match(link))