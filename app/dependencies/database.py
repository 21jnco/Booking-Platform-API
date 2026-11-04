from collections.abc import AsyncGenerator
from app.db.session import session
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session() as db:
        yield db