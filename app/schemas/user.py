from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr):
        return value.lower()


class UserEmailUpdate(BaseModel):
    current_email: str
    new_email: EmailStr = Field(max_length=255)

    @field_validator("current_email", "new_email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> EmailStr:
        return value.lower()


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=255)


class FirstNameUpdate(BaseModel):
    new_first_name: str = Field(max_length=50)


class LastNameUpdate(BaseModel):
    new_last_name: str = Field(max_digits=50)

class UserRecovery(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)

    @field_validator("new_email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> EmailStr:
        return value.lower()


class UserResponse(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    created_at: datetime
    model_config = {
        'from_attributes': True
    }