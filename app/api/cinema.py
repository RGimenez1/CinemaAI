from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.cinema import CinemaPreference, StatusEnum
from app.repositories.cinema_repository import CinemaRepository
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal
from uuid import UUID

router = APIRouter()


class CinemaPreferenceCreate(BaseModel):
    user_id: UUID
    title: str
    year: int
    type: Literal["movie", "series"]
    genre: List[str]
    status: str = Field(...)

    @field_validator("status")
    def validate_status(cls, v):
        if v not in [status.value for status in StatusEnum]:
            raise ValueError(f"Invalid status: {v}")
        return v


@router.post(
    "/cinema_preferences",
    response_model=CinemaPreferenceCreate,
    summary="Posts a new entry to cinema preferences by user id",
    description="Add movie or serie to user cinema preferences",
)
async def create_cinema_preference(
    preference: CinemaPreferenceCreate, session: AsyncSession = Depends(get_session)
):
    cinema_repository = CinemaRepository(session)
    preference = CinemaPreference(**preference.model_dump())
    return await cinema_repository.add_preference(preference)


@router.get(
    "/cinema_preferences/{user_id}",
    response_model=List[CinemaPreferenceCreate],
    summary="Get cinema preferences by user id",
    description="Gets movies and series user cinema preferences",
)
async def get_cinema_preferences(
    user_id: UUID, session: AsyncSession = Depends(get_session)
):
    cinema_repository = CinemaRepository(session)
    return await cinema_repository.get_preferences_by_user_id(user_id)
