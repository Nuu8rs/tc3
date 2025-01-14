from dependency_injector import containers, providers
from pyaml_env import parse_config #type: ignore

from app.components.api.service import ApiService
from app.components.auth.repo import AuthRepository
from app.components.auth.service import AuthService
from app.components.chats.repo import ChatRepository
from app.components.chats.service import ChatService
from app.components.jinja2.templates import CustomJinja
from app.components.media.repo import MediaRepository
from app.components.media.service import MediaService
from app.components.posts.repo import PostRepository
from app.components.posts.service import PostService
from app.components.projects.repo import ProjectRepository
from app.components.projects.service import ProjectService
from app.components.users.repo import UserRepository
from app.components.users.service import UserService
from app.configs import AppConfig
from app.constants import CONFIG_FILE
from app.database import DB


class Container(containers.DeclarativeContainer):
    config: providers.Provider = providers.Singleton(
        AppConfig, **parse_config(CONFIG_FILE)
    )

    db: providers.Provider = providers.Singleton(
        DB, config=config.provided.db, debug=config.provided.env.debug
    )
    db_session: providers.Provider = providers.Factory(db.provided.get_session)

    api_service: providers.Provider = providers.Singleton(
        ApiService,
        config=config
    )

    user_repository: providers.Provider = providers.Singleton(UserRepository)
    user_service: providers.Provider = providers.Singleton(
        UserService,
        user_repository=user_repository,
        config=config.provided.auth
    )

    auth_repository: providers.Provider = providers.Singleton(AuthRepository)
    auth_service: providers.Provider = providers.Singleton(
        AuthService,
        auth_repository=auth_repository,
        user_repository=user_repository,
        config=config.provided.auth
    )
    
    project_repository: providers.Provider = providers.Singleton(ProjectRepository)
    project_service: providers.Provider = providers.Singleton(
        ProjectService,
        project_repository=project_repository,
    )

    chat_repository: providers.Provider = providers.Singleton(ChatRepository)
    chat_service: providers.Provider = providers.Singleton(
        ChatService,
        chat_repository=chat_repository,
        project_service=project_service
    )

    post_repository: providers.Provider = providers.Singleton(PostRepository)
    post_service: providers.Provider = providers.Singleton(
        PostService,
        post_repository=post_repository,
        chat_service=chat_service
    )

    media_repository: providers.Provider = providers.Singleton(MediaRepository)
    media_service: providers.Provider = providers.Singleton(
        MediaService,
        media_repository=media_repository
    )

    templates: providers.Provider = providers.Singleton(
        CustomJinja,
        directory="app/templates",
    )

container = Container()
