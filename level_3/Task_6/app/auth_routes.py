from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from auth_schemas import (
    RegisterUserRequest,
    LoginUserRequest,
    AuthResponse,
    UserModel,
)
from auth_utils import (
    HashPassword,
    VerifyPassword,
    CreateAccessToken,
    DecodeAccessToken,
)
from mongo_config import get_user_collection
from pymongo.errors import DuplicateKeyError
from datetime import timedelta
from mail_utils import SendRecoveryEmail
from fastapi import HTTPException
from auth_schemas import PasswordResetRequest
from auth_schemas import NewPasswordRequest



authRouter = APIRouter(prefix="/auth", tags=["Authentication"])

# Register a new user
@authRouter.post("/register", response_model=AuthResponse)
async def RegisterUser(user: RegisterUserRequest, UserCollection=Depends(get_user_collection)):
    # Check if passwords match
    if user.Password != user.ConfirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check if user already exists
    existing = await UserCollection.find_one({"Email": user.Email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # Prepare user data with hashed password
    user_data = {
        "Username": user.Username,
        "Email": user.Email,
        "HashedPassword": HashPassword(user.Password)
    }

    try:
        # Insert new user into database
        await UserCollection.insert_one(user_data)
        # Create access token for the new user
        token = CreateAccessToken(data={"sub": user.Email, "name": user.Username})
        return AuthResponse(Message="User registered successfully", AccessToken=token)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already in use")


# Login route
@authRouter.post("/login", response_model=AuthResponse)
async def LoginUser(user: LoginUserRequest, UserCollection=Depends(get_user_collection)):
    # Find user by email
    existing = await UserCollection.find_one({"Email": user.Email})
    # Check if user exists and password is correct
    if not existing or not VerifyPassword(user.Password, existing["HashedPassword"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create access token for successful login
    token = CreateAccessToken(data={"sub": user.Email, "name": existing["Username"]})
    return AuthResponse(Message="Login successful", AccessToken=token)



# Password recovery via email (now using request body)
@authRouter.post("/reset-password")
async def RequestPasswordReset(payload: PasswordResetRequest, UserCollection=Depends(get_user_collection)):
    # Get email from request
    email = payload.Email
    # Check if user exists
    user = await UserCollection.find_one({"Email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create reset token with 15 minute expiry
    token = CreateAccessToken(data={"sub": email}, expires_delta=timedelta(minutes=15))
    # Send recovery email with reset link
    await SendRecoveryEmail(email_to=email, token=token)
    return {"Message": "Password reset link has been sent to your email."}


# Reset password with new one (front-end calls this with token)
@authRouter.post("/confirm-reset")
async def ConfirmPasswordReset(payload: NewPasswordRequest, UserCollection=Depends(get_user_collection)):
    # Check if new passwords match
    if payload.NewPassword != payload.ConfirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Decode and verify the reset token
    payload_data = DecodeAccessToken(payload.Token)
    if not payload_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Get email from token and hash new password
    email = payload_data.get("sub")
    hashed_password = HashPassword(payload.NewPassword)

    # Update user's password in database
    result = await UserCollection.update_one(
        {"Email": email},
        {"$set": {"HashedPassword": hashed_password}}
    )

    # Check if password was actually updated
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or password not changed")

    return {"Message": "Password has been successfully reset."}


# Protected example
@authRouter.get("/me")
async def GetCurrentUser(token: str):
    # Decode and verify the access token
    user_data = DecodeAccessToken(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    # Return user email from token
    return {"Email": user_data["sub"]}
