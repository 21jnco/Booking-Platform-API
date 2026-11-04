from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

async_engine = create_async_engine(settings.DATABASE_URL)
session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)