from app.db.base import Base

from sqlalchemy import Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

class Availability(Base):
    __tablename__="availabilities"

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

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("providers.id"),
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

    provider = relationship(
        "Provider",
        back_populates="availabilities"
    )