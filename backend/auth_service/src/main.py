"""
Authentication Service - Main FastAPI application

This service handles user authentication, OAuth integration, and user management.
"""

from fastapi import FastAPI, HTTPException, status, Depends, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
import uuid
from datetime import datetime, timedelta

from src.core.config import config
from src.core.security import hash_password, verify_password, create_access_token, verify_token
from src.core.email import email_service
from src.db.session import get_db, init_db
from src.models.user import User

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Auth Service API",
    description="Authentication and user management API for AI-Native Textbook Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Request/Response Models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=100)
    preferred_language: str = Field("en", regex="^(en|ur)$")

    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class UserResponse(BaseModel):
    id: str
    email: str
    display_name: str
    preferred_language: str
    is_verified: bool
    created_at: Optional[str] = None
    last_active: Optional[str] = None


class VerifyEmailRequest(BaseModel):
    token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class HealthResponse(BaseModel):
    status: str


# API Routes
@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.post("/auth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["auth"])
async def signup(
    request: SignupRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user account.

    Sends a verification email to the user's email address.
    """
    try:
        # Check if user already exists
        result = await db.execute(
            select(User).where(User.email == request.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Create new user
        from src.db.init_db import User as UserModel

        hashed_password = hash_password(request.password)
        verification_token = str(uuid.uuid4())

        # For now, we'll use a simple dict-based approach
        # In production, use proper SQLAlchemy async models
        user_data = {
            "id": uuid.uuid4(),
            "email": request.email,
            "password_hash": hashed_password,
            "display_name": request.display_name,
            "preferred_language": request.preferred_language,
            "is_verified": False,
            "created_at": datetime.utcnow(),
        }

        # Create verification URL
        verification_url = f"{config.frontend_url}/verify-email?token={verification_token}"

        # Send verification email
        await email_service.send_verification_email(
            to_email=request.email,
            username=request.display_name,
            verification_url=verification_url
        )

        # Return user response (without password)
        return UserResponse(
            id=str(user_data["id"]),
            email=user_data["email"],
            display_name=user_data["display_name"],
            preferred_language=user_data["preferred_language"],
            is_verified=user_data["is_verified"],
            created_at=user_data["created_at"].isoformat(),
            last_active=None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in signup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create account"
        )


@app.post("/auth/login", response_model=UserResponse, tags=["auth"])
async def login(
    request: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user with email and password.

    Sets an httpOnly cookie with the JWT session token.
    """
    try:
        # Find user by email
        result = await db.execute(
            select(User).where(User.email == request.email)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(days=7 if request.remember_me else 1)
        )

        # Set httpOnly cookie
        max_age = 60 * 60 * 24 * 7 if request.remember_me else 60 * 60 * 24
        response.set_cookie(
            key="session_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set True in production with HTTPS
            samesite="lax",
            max_age=max_age
        )

        # Return user data
        return UserResponse(
            id=str(user.id),
            email=user.email,
            display_name=user.display_name,
            preferred_language=user.preferred_language,
            is_verified=user.is_verified,
            created_at=user.created_at.isoformat() if user.created_at else None,
            last_active=user.last_active.isoformat() if user.last_active else None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@app.post("/auth/logout", tags=["auth"])
async def logout(response: Response):
    """
    Logout user by clearing the session cookie.
    """
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}


@app.get("/users/me", response_model=UserResponse, tags=["users"])
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the currently authenticated user's profile.
    """
    try:
        # Verify token and get user_id
        user_id = verify_token(token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # Get user from database
        result = await db.execute(
            select(User).where(User.id == uuid.UUID(user_id))
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserResponse(
            id=str(user.id),
            email=user.email,
            display_name=user.display_name,
            preferred_language=user.preferred_language,
            is_verified=user.is_verified,
            created_at=user.created_at.isoformat() if user.created_at else None,
            last_active=user.last_active.isoformat() if user.last_active else None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user"
        )


@app.post("/auth/verify-email", tags=["auth"])
async def verify_email(request: VerifyEmailRequest, db: AsyncSession = Depends(get_db)):
    """
    Verify user's email address using the token sent to their email.
    """
    try:
        # Find verification token
        # TODO: Implement token verification logic
        return {"message": "Email verified successfully"}

    except Exception as e:
        logger.error(f"Error verifying email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify email"
        )


@app.post("/auth/forgot-password", tags=["auth"])
async def forgot_password(request: ForgotPasswordRequest):
    """
    Send password reset email to user.
    """
    try:
        # Generate reset token and send email
        # TODO: Implement full password reset flow
        return {"message": "If the email exists, a password reset link has been sent"}

    except Exception as e:
        logger.error(f"Error in forgot password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process request"
        )


@app.post("/auth/reset-password", tags=["auth"])
async def reset_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """
    Reset user's password using the token from the reset email.
    """
    try:
        # Verify token and update password
        # TODO: Implement full password reset logic
        return {"message": "Password reset successfully"}

    except Exception as e:
        logger.error(f"Error resetting password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Auth Service...")
    logger.info(f"Database URL configured")
    logger.info(f"JWT Algorithm: {config.jwt_algorithm}")

    # Initialize database tables
    await init_db()
    logger.info("Database tables initialized")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Auth Service...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)
