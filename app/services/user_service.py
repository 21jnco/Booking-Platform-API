from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.booking import Booking
from app.models.provider import Provider
from app.models.service import Service
from app.core.exceptions import IncorrectData, violates_unique, AlreadyExistsError, NonexistingError
from app.core.security import verify_password, hash_password
from app.schemas.user import (
    UserPasswordUpdate,
    UserEmailUpdate,
    FirstNameUpdate,
    LastNameUpdate,
    UserRecovery
)
from app.enums.booking import BookingStatus

from starlette.concurrency import run_in_threadpool
from datetime import datetime, timezone

class UserService():
    def __init__(self, session: AsyncSession, current_user: User):
        self.session = session
        self.current_user = current_user

    async def update_password(self, user_data: UserPasswordUpdate) -> None:
        async with self.session.begin():
            verify_old_password = await run_in_threadpool(
                verify_password,
                user_data.current_password,
                self.current_user.hashed_password
            )
            if not verify_old_password:
                raise IncorrectData(400, "Incorrect password")
            new_password = await run_in_threadpool(
                hash_password,
                user_data.new_password
            )
            self.current_user.hashed_password = new_password
            await self.session.flush()

    async def update_email(self, user_data: UserEmailUpdate) -> None:
        try:
            async with self.session.begin():
                if self.current_user.email != user_data.current_email:
                    raise IncorrectData(400, "Incorrect email")
                self.current_user.email = user_data.new_email
                await self.session.flush()
        except IntegrityError as error:
            if violates_unique(error, "ix_users_email"):
                raise AlreadyExistsError(
                    409, "Email is already exsist"
                ) from error
            raise

    async def update_fist_name(self, user_data: FirstNameUpdate) -> None:
        async with self.session.begin():
            self.current_user.first_name = user_data.new_first_name
            await self.session.flush()

    async def update_last_name(self, user_data: LastNameUpdate) -> None:
        async with self.session.begin():
            self.current_user.last_name = user_data.new_last_name
            await self.session.flush()

    async def delete_account(self) -> None:
        async with self.session.begin():
            self.current_user.deleted_at = datetime.now(timezone.utc)
            await self._change_booking_status()
            provider = await self._ensure_provider_available()
            if provider is not None:
                provider.deleted_at = datetime.now(timezone.utc)
            await self._ensure_service_available(provider.id)

    async def recovery_account(self, user_data: UserRecovery) -> None:
        async with self.session.begin():
            user = await self._get_deleted_user_by_email(user_data)
            if user is None:
                raise NonexistingError(404, "User not found")
            password = await run_in_threadpool(
                verify_password,
                user_data.password,
                user.hashed_password
            )
            if not password:
                raise IncorrectData(400, "Incorrect password")
            user.deleted_at = None
            await self.session.flush()

    async def _change_booking_status(self) -> None:
        bookings = await self.session.scalars(
            select(Booking)
            .where(Booking.user_id == self.current_user.id)
        )
        for booking in bookings:
            booking.status = BookingStatus.UNAVAILABLE

    async def _ensure_provider_available(self) -> Provider | None:
        return await self.session.scalar(
            select(Provider)
            .where(
                Provider.user_id == self.current_user,
                Provider.deleted_at.is_(None)
            )
        )
    
    async def _change_service_status(self, provider_id: int) -> None:
        services = await self.session.scalars(
            select(Service)
            .where(
                Service.provider_id == provider_id,
                Service.deleted_at.is_(None)
            )
        )
        for service in services:
            service.is_active = False

    async def _get_deleted_user_by_email(self, data: UserRecovery) -> User | None:
        return await self.session.scalar(
            select(User)
            .where(
                User.email == data.email,
                User.deleted_at.is_not(None),
            )
        )