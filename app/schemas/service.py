from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from datetime import datetime

class ServiceCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str | None
    duration_minutes: int = Field(gt=0)
    price: Decimal = Field(ge=0)
    is_active: bool


class ServiceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=50)
    description: str | None = None
    duration_minutes: int | None = Field(default=None, gt=0)
    price: Decimal | None = Field(default=None, ge=0)
    is_active: bool | None = None

    @field_validator("name", "duration_minutes", "price", "is_active")
    @classmethod
    def price_cannot_be_null(cls, value: Decimal) -> str | int | bool | Decimal:
        if value is None:
            raise ValueError("Price cannot be null")
        return value


class ServiceResponse(BaseModel):
    name: str
    description: str | None
    duration_minutes: int = Field(gt=0)
    price: Decimal = Field(ge=0)
    is_active: bool
    created_at: datetime
    model_config = {
        'from_attributes': True
    }