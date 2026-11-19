from pydantic import BaseModel, Field, EmailStr

class LoginRequest(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=6, max_length=255)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
