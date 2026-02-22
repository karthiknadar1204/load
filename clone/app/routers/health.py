"""Health and info endpoints."""
from fastapi import APIRouter

from app.schemas import ApiResponse, HealthData

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiResponse)
def health():
    """Service health and supported export formats."""
    return ApiResponse(success=True, data=HealthData().model_dump())
