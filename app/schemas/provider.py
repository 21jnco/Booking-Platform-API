from pydantic import BaseModel, Field, field_validator
from app.enums.provider import MedicalSpecialty
from datetime import datetime

class ProdiverCreate(BaseModel):
    profile_description: str | None = None
    specialty: MedicalSpecialty


class ProdiverUpdate(BaseModel):
    profile_description: str | None = None
    specialty: MedicalSpecialty | None = Field(default=None)

    @field_validator("specialty")
    @classmethod
    def specialty_cannot_be_null(cls, value: MedicalSpecialty) -> MedicalSpecialty:
        if value is None:
            raise ValueError("Specialty cannot be null")
        return value


class ProviderResponce(BaseModel):
    id: int
    user_id: int
    profile_description: str | None
    specialty: MedicalSpecialty
    created_at: datetime
    model_config = {
        "from_attributes": True
    }