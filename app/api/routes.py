from fastapi import APIRouter, Query
from app.services.movie_service import get_movies_by_title
from typing import List, Optional
from app.models.movie import Movie

router = APIRouter()


@router.get("/movies", response_model=List[Movie])
async def read_movies(
    title: Optional[str] = Query(None, description="Title of the movie to search")
):
    return await get_movies_by_title(title)
