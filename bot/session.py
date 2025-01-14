from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from bot.config import config
from typing import Generator

connection_string = config.database_config.master_key_connect
engine = create_async_engine(connection_string, pool_size=10, max_overflow=0)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> Generator[AsyncSession,None,None]: #type: ignore
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
        finally:
            await session.close()
