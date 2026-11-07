from app.db.base import Base
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint

from sqlalchemy import Integer, String, DateTime, ForeignKey, TEXT, DECIMAL, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Service(Base):
    """Service offered by a provider with a specified price and duration."""

    __tablename__="services"

    __table_args__=(
        CheckConstraint(
            "duration_minutes > 0",
            name="ck_services_duration_positive"
        ),
        CheckConstraint(
            "price >= 0",
            name="ck_services_price_nonnegative"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    provider_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("providers.id")
    )

    name: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        TEXT,
        nullable=True
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        index=True,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
        onupdate=lambda:datetime.now(timezone.utc),
        nullable=False
    )

    provider = relationship(
        "Provider",
        back_populates="services"
    )

    bookings = relationship(
        "Booking",
        back_populates="service"
    )
