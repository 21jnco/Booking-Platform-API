from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.schemas.auth import LoginRequest
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.exceptions import AlreadyExistsError, NonexistingError, IncorrectPassword
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import violates_unique

from starlette.concurrency import run_in_threadpool

class AuthService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def registration(self, user_data: UserCreate) -> User:
        try:
            async with self.session.begin():
                await self._get_existing_user_by_email(user_data)
                hashed_password = await run_in_threadpool(
                    hash_password,
                    user_data.password
                )
                user = User(
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                    email=user_data.email,
                    hashed_password=hashed_password,
                )
                await self.session.flush()
            return user
        except IntegrityError as error:
            if violates_unique(error, "ix_users_email"):
                raise AlreadyExistsError("Email is already registered.")
            raise

    async def login(self, user_data: LoginRequest):
        async with self.session.begin():
            user = await self._get_user(user_data)
            valid = await run_in_threadpool(
                verify_password,
                user_data.password,
                user.hashed_password,
            )
            if valid is False:
                raise IncorrectPassword("Incorrect password.")
            token = create_access_token(user.id)
            return token

    async def _get_existing_user_by_email(self, user_data: UserCreate) -> None:
        query = select(User).where(User.email == user_data.email)
        execute = await self.session.execute(query)
        existing_user = execute.scalar_one_or_none()
        if existing_user is not None:
            raise AlreadyExistsError("Email is already registered.")

    async def _get_user(self, data: LoginRequest) -> User:
        query = select(User).where(User.email == data.email, User.deleted_at.is_(None))
        execute = await self.session.execute(query)
        user = execute.scalar_one_or_none()
        if user is None:
            raise NonexistingError("Deleted or nonexisting user.")
        return user