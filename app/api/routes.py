from fastapi import APIRouter, Query
from app.services.movie_service import search_movies
from typing import List, Optional
from app.models.movie import Movie

router = APIRouter()


@router.get("/movies", response_model=List[Movie])
async def read_movies(
    title: Optional[str] = Query(None, description="Title of the movie to search"),
    genres: Optional[List[str]] = Query(None, description="Genres to search for"),
    year: Optional[int] = Query(None, description="Year of release to search"),
    director: Optional[str] = Query(None, description="Director to search for"),
    cast_member: Optional[str] = Query(None, description="Cast member to search for"),
):
    return await search_movies(title, genres, year, director, cast_member)
