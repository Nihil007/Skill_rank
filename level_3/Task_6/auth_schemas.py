from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Schema for user registration request
class RegisterUserRequest(BaseModel):
    Username: str = Field(..., min_length=3, max_length=30)
    Email: EmailStr
    Password: str = Field(..., min_length=6)
    ConfirmPassword: str = Field(..., min_length=6)


# Schema for user login request
class LoginUserRequest(BaseModel):
    Email: EmailStr
    Password: str


# Schema for password reset request
class PasswordResetRequest(BaseModel):
    Email: EmailStr


# Schema for setting a new password
class NewPasswordRequest(BaseModel):
    Token: str
    NewPassword: str = Field(..., min_length=6)
    ConfirmPassword: str = Field(..., min_length=6)


# Response schema after login/registration
class AuthResponse(BaseModel):
    Message: str
    AccessToken: Optional[str] = None
    TokenType: Optional[str] = "bearer"


# Schema for internal user model stored in DB
class UserModel(BaseModel):
    Id: Optional[str]
    Username: str
    Email: EmailStr
    HashedPassword: str
