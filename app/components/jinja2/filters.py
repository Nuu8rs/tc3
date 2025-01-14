import bleach

from datetime import datetime
from typing import Any

from app.constants import DEFAULT_THUMBNAIL
from database.models.constans import PostStatusEnum, MediaTypeEnum
from database.models.posts import Media


def format_datetime(value: Any, format:str='%Y-%m-%d %H:%M') -> str:
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

def post_status(value: PostStatusEnum) -> str:
    if value == PostStatusEnum.NOT_CHANGED:
        return _("NOT CHANGED")
    elif value == PostStatusEnum.EDITED:
        return _("EDITED")
    elif value == PostStatusEnum.DELETED:
        return _("DELETED")
    return _("UNKNOWN")

def format_media(value: Media) -> str:
    if value.file_type == MediaTypeEnum.PHOTO:
        return f"""<img src="{value.file_url}" alt="Image">"""
    if value.file_type == MediaTypeEnum.VIDEO:
        return f"""<video controls src="{value.file_url}"></video>"""
    else:
        return f"""<a href="{value.file_url}"><img src="{DEFAULT_THUMBNAIL}" alt="Image"></a>"""

def replace_to_br_tag(value: str | None) -> str | None:
    return value.replace("\n", "<br>")

def format_html(value: str | None) -> str | None:
    if value is None:
        return value
    value = value.replace("&nbsp;", "")
    allowed_tags = ["b", "strong", "u", "i", "em", "code", "strike", "s", "del", "pre", "a"]
    allowed_attrs = {
        "a": ["href"],
        "pre": ["language"]
    }
    return bleach.clean(value, tags=allowed_tags, attributes=allowed_attrs, strip=False)

def format_html_news_feed(value: str | None) -> str | None:
    if value is None:
        return value
    value = value.replace("&nbsp;", "")
    allowed_tags = []
    return bleach.clean(value, tags=allowed_tags, attributes={}, strip=True)
