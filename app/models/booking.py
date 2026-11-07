from app.db.base import Base

from sqlalchemy import Integer, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone
from sqlalchemy import CheckConstraint

from app.enums.booking import BookingStatus

class Booking(Base):
    __tablename__="bookings"

    __table_args__=(
        CheckConstraint(
            "ends_at > starts_at",
            name="ck_bookings_time_orders",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"),
        nullable=False
    )

    status: Mapped[BookingStatus] = mapped_column(
        SAEnum(
            BookingStatus,
            name="booking_status",
            values_callable=lambda items: [item.value for item in items],
        ),
        default=BookingStatus.COMPLETED,
        nullable=False
    )

    starts_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    ends_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="bookings"
    )

    service = relationship(
        "Service",
        back_populates="bookings"
    )