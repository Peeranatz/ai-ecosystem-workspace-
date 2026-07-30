from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UserProfileResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["1. Authentication & Security Domain"])

@router.post("/register", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    """Register a new user in the AI Ecosystem."""
    return await AuthService.register_user(payload)

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    """Authenticate credentials and return a Stateless JWT Access Token."""
    return await AuthService.login_user(payload)

@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile():
    """Retrieve current authenticated user profile."""
    return UserProfileResponse(id=1, username="sky_admin", email="sky@aiecosystem.io")
