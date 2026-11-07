from datetime import timezone, datetime

from app.db.base import Base


from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    """User account with bookings and an optional provider profile."""

    __tablename__="users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        index=True,
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate= lambda: datetime.now(timezone.utc),
        nullable=False
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True
    )

    bookings = relationship(
        "Booking",
        back_populates="user"
    )

    provider = relationship(
        "Provider",
        back_populates="user",
        uselist=False
    )
