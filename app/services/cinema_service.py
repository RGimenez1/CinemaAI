from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.repositories.cinema_repository import CinemaRepository
from app.domain.models.cinema import CinemaPreference, CinemaPreferenceCreate
from typing import List
from uuid import UUID


class CinemaService:
    def __init__(self, session: AsyncSession):
        self.cinema_repository = CinemaRepository(session)

    async def create_cinema_preference(self, preference: CinemaPreferenceCreate):
        preference_model = CinemaPreference(**preference.dict())
        return await self.cinema_repository.add_preference(preference_model)

    async def get_cinema_preferences(
        self, user_id: UUID
    ) -> List[CinemaPreferenceCreate]:
        return await self.cinema_repository.get_preferences_by_user_id(user_id)
