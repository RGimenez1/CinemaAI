from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models.cinema import CinemaPreference


class CinemaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_preference(self, preference: CinemaPreference):
        self.session.add(preference)
        await self.session.commit()
        await self.session.refresh(preference)
        return preference

    async def get_preferences_by_user_id(self, user_id: str):
        result = await self.session.execute(
            select(CinemaPreference).where(CinemaPreference.user_id == user_id)
        )
        return result.scalars().all()
