from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime, UTC
from typing import Self

class AvailabilityCreate(BaseModel):
    starts_at: datetime
    ends_at: datetime

    @field_validator("starts_at", "ends_at")
    @classmethod
    def utc_whole_hour(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("A timezone is required")
        value = value.astimezone(UTC)
        if value.second or value.microsecond:
            raise ValueError("Seconds and microseconds must be zero")
        if value.minute % 5 != 0:
            raise ValueError("Booking must start at a 5-minute boundary")
        return value

    @model_validator(mode="after")
    def validate_interval(self) -> Self:
        if self.starts_at >= self.ends_at:
            raise ValueError("End time must be later than start time")
        return self


class AvailabilityUpdate(BaseModel):
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    @field_validator("starts_at", "ends_at")
    @classmethod
    def utc_whole_hour(cls, value: datetime) -> datetime:
        if value is None:
            raise ValueError("Value cannot be null")
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("A timezone is required")
        value = value.astimezone(UTC)
        if value.second or value.microsecond:
            raise ValueError("Seconds and microseconds must be zero")
        if value.minute % 5 != 0:
            raise ValueError("Booking must start at a 5-minute boundary")
        return value

    @model_validator(mode="after")
    def validate_interval(self) -> Self:
        if self.starts_at is not None and self.ends_at is not None:
            if self.starts_at >= self.ends_at:
                raise ValueError("End time must be later than start time")
        return self

class AvailabilityRequest(BaseModel):
    id: int
    provider_id: int
    starts_at: datetime 
    ends_at: datetime
    created_at: datetime
    model_config = {
        "from_attributes": True
    }