import os
import urllib.parse

from contextlib import asynccontextmanager
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.exceptions import ExceptionMiddleware
from typing import AsyncGenerator

from app.babel import configs
from app.components.auth.endpoints import auth_router
from app.components.auth.exceptions import NoTokenException
from app.components.chats.endpoints import chats_router
from app.components.home.endpoints import home_router
from app.components.posts.endpoints import posts_router
from app.components.projects.endpoints import projects_router
from app.components.projects.exceptions import InvalidProjectError
from app.components.home.endpoints import home_router
from app.components.localization.endpoints import localization_router
from app.components.localization.middlewares import MultiLingualMiddleware
from app.components.media.endpoints import media_router
from app.components.users.endpoints import user_router
from app.configs import AppConfig
from app.containers import container, Container
from app.database import DB
from app.components.base.exceptions import LogicError
from database.models.base_accessor import get_base


@inject
def setup_app(
    config: AppConfig = Provide[Container.config],
    db: DB = Provide[Container.db],
    
):
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        
        engine = create_engine(config.db.master_sync)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )
        get_base().metadata.create_all(bind=engine)
        
        await db.init_db()
        yield
        await db.dispose()

    app = FastAPI(debug=config.env.debug, lifespan=lifespan)
    app.add_middleware(MultiLingualMiddleware, babel_configs=configs)
    
    if not os.path.exists("accounts/static/media"):
        os.makedirs("accounts/static/media")
    app.mount("/static/media", StaticFiles(directory="accounts/static/media"), name="media")
    app.mount("/static/css", StaticFiles(directory="app/static/css"), name="styles")
    app.mount("/static/fonts", StaticFiles(directory="app/static/fonts"), name="fonts")
    app.mount("/static/js", StaticFiles(directory="app/static/js"), name="scripts")
    app.mount("/static/img", StaticFiles(directory="app/static/img"), name="images")

    app.include_router(auth_router)
    app.include_router(chats_router)
    app.include_router(home_router)
    app.include_router(media_router)
    app.include_router(localization_router)
    app.include_router(posts_router)
    app.include_router(projects_router)
    app.include_router(user_router)

    if config.env.enable_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.exception_handler(Exception)
    async def debug_exception_handler(
        _: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception(exc)
        return JSONResponse(
            {"error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @app.exception_handler(LogicError)
    async def logic_exception_handler(
        _: Request, exc: LogicError
    ) -> JSONResponse:
        logger.exception(exc)
        return JSONResponse({"error": str(exc)}, status_code=400)

    @app.exception_handler(NoTokenException)
    async def token_exception_handler(
        request: Request, e: NoTokenException
    ) -> RedirectResponse | JSONResponse:
        if request.method == "GET":
            current_url = urllib.parse.quote_plus(str(request.url))
            redirect_url = f"/auth?redirect={current_url}"
            return RedirectResponse(url=redirect_url)
        return JSONResponse(
            {"error": "No token"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    @app.exception_handler(InvalidProjectError)
    async def project_exception_handler(
        _: Request, __: InvalidProjectError
    ) -> RedirectResponse:
        return RedirectResponse(
            url="/projects",
        )

    app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)

    return app

container.wire(modules=[__name__])
