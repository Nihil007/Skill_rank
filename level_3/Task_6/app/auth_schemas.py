from pydantic import BaseModel, EmailStr, Field, constr, validator
from typing import Optional, Annotated


# Schema for user registration request
class RegisterUserRequest(BaseModel):
    Username: Annotated[str, constr(min_length=3, max_length=30, regex=r"^[a-zA-Z0-9_.-]+$")]
    Email: EmailStr
    Password: str
    ConfirmPassword: str

    @validator("Password")
    def password_policy(cls, v):
        import re
        if len(v) < 8 or not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", v):
            raise ValueError("Password does not meet complexity requirements")
        return v


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
    NewPassword: str
    ConfirmPassword: str

    @validator("NewPassword")
    def password_policy(cls, v):
        import re
        if len(v) < 8 or not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", v):
            raise ValueError("Password does not meet complexity requirements")
        return v


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
