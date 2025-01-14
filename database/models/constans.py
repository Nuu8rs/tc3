import enum


class PostStatusEnum(enum.Enum):
    NOT_CHANGED = "NOT_CHANGED"
    EDITED = "EDITED"
    DELETED = "DELETED"
    
class MediaTypeEnum(enum.Enum):
    PHOTO = "PHOTO"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    DOCUMENT = "DOCUMENT"


class EmptyList(list):
    def __init__(self):
        super().__init__()
    
    def __bool__(self):
        return len(self) != 0

    def __repr__(self):
        return "[]"
    

@enum.unique
class ScopeEnum(str, enum.Enum):
    ACCOUNT_GET = "account:get"
    ACCOUNT_UPDATE = "account:update"
    ACCOUNT_DELETE = "account:delete"

    ACCOUNTS_GET = "accounts:get"
    ACCOUNTS_CREATE = "accounts:create"
    ACCOUNTS_UPDATE = "accounts:update"
    ACCOUNTS_DELETE = "accounts:delete"

    CHATS_LIST = "chat:all"
    CHAT_CREATE = "chat:create"
    CHAT_INFO = "chat:info"
    CHAT_DELETE = "chat:delete"

    POSTS_LIST = "post:all"
    POST_INFO = "post:info"
    POST_DELETE = "post:delete"
    POST_UPDATE = "post:update"

    # MODERATORS_LIST = "project:moderators"
    PROJECT_GET = "project:get"
    PROJECT_CREATE = "project:create"
    PROJECT_DELETE = "project:delete"


@enum.unique
class RolePermissionsEnum(str, enum.Enum):
    USER = "account:* project:* chat:* post:*"
    ADMIN = f"accounts:* {USER}"


@enum.unique
class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"