from pydantic import BaseModel, Field, field_validator
from app.enums.booking import BookingStatus
from datetime import datetime, UTC

class BookingCreate(BaseModel):
    status: BookingStatus
    starts_at: datetime

    @field_validator("starts_at")
    @classmethod
    def utc_whole_hour(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("A time zone is required")
        value = value.astimezone(UTC)
        if value.second or value.microsecond:
            raise ValueError("Seconds and microseconds must be zero")
        if value.minute % 5 != 0:
            raise ValueError("Booking must start at a 5-minute boundary")
        return value


class BookingUpdate(BaseModel):
    status: BookingStatus | None = Field(default=None)
    starts_at: datetime | None = None

    @field_validator("starts_at")
    @classmethod
    def utc_whole_hour(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("A time zone is required")
        value = value.astimezone(UTC)
        if value.second or value.microsecond:
            raise ValueError("Seconds and microseconds must be zero")
        if value.minute % 5 != 0:
            raise ValueError("Booking must start at a 5-minute boundary")
        return value


class BookingRequest(BaseModel):
    id: int
    user_id: int
    status: BookingStatus
    starts_at: datetime
    ends_at: datetime
    created_at: datetime
    model_config = {
        "from_attributes": True
    }
