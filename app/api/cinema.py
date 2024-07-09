from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.session import get_session
from app.services.cinema_service import CinemaService
from app.domain.models.cinema import CinemaPreferenceCreate
from typing import List
from uuid import UUID

router = APIRouter()


@router.post(
    "/cinema_preferences",
    response_model=CinemaPreferenceCreate,
    summary="Posts a new entry to cinema preferences by user id",
    description="Add movie or series to user cinema preferences",
)
async def create_cinema_preference(
    preference: CinemaPreferenceCreate, session: AsyncSession = Depends(get_session)
):
    cinema_service = CinemaService(session)
    return await cinema_service.create_cinema_preference(preference)


@router.get(
    "/cinema_preferences/{user_id}",
    response_model=List[CinemaPreferenceCreate],
    summary="Get cinema preferences by user id",
    description="Gets movies and series user cinema preferences",
)
async def get_cinema_preferences(
    user_id: UUID, session: AsyncSession = Depends(get_session)
):
    cinema_service = CinemaService(session)
    return await cinema_service.get_cinema_preferences(user_id)
