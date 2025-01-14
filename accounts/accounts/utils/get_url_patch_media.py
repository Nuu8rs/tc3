import aiofiles
import os
import asyncio
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, Message, TypeMessageMedia


async def url_patch_media(message: Message) -> str:
    base_direcroty = "static"
    
    if hasattr(message.media, "video") and message.media.video:
        type_media = "video"
        mime_type = "mp4"
    
    if hasattr(message.media, "photo") and message.media.photo:
        type_media = "photo"
        mime_type = "jpg"
        date = message.media.photo.date


    
    async with aiofiles.os.scandir(base_direcroty) as entries:
        existing_files = {entry.name for entry in entries}
        
    base_filename =  f"{type_media}_{message.id}.{mime_type}"
        
    if base_filename not in existing_files:
        return os.path.join(base_direcroty, base_filename)
    
    index = 1
    while True:
        new_filename = f"{type_media}_{message.id}_{index}.{mime_type}"
        
        if new_filename not in existing_files:
            return os.path.join(base_direcroty, new_filename)
        
        index += 1