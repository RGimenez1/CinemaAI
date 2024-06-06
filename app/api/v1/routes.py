
from fastapi import APIRouter
from app.services.movie_service import get_all_movies
from typing import List
from app.models.movie import Movie

router = APIRouter()

@router.get("/movies", response_model=List[Movie])
async def read_movies():
    return await get_all_movies()
