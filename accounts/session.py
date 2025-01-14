from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from accounts.config import DatabaseConfig
from typing import AsyncGenerator


connection_string = DatabaseConfig.get_connection_string()
engine = create_async_engine(connection_string, pool_size=10, max_overflow=0)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
        finally:
            await session.close()
