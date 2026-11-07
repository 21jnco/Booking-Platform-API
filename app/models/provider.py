from app.enums.provider import MedicalSpecialty

from app.db.base import Base

from sqlalchemy import Integer, DateTime, ForeignKey, TEXT, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

class Provider(Base):
    __tablename__="providers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    profile_description: Mapped[str | None] = mapped_column(
        TEXT,
        nullable=True
    )

    specialty: Mapped[MedicalSpecialty] = mapped_column(
        SAEnum(
            MedicalSpecialty,
            name="medical_specialty",
            values_callable=lambda items: [item.value for item in items],
        ),
        default=MedicalSpecialty.NOT_SELECTED,
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

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="provider"
    )

    services = relationship(
        "Service",
        back_populates="provider"
    )

    availabilities = relationship(
        "Availability",
        back_populates="provider"
    )