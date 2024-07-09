from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Optional
from app.services.movie_service import search_movies
from app.domain.models.movie import Movie
from app.infrastructure.db.mongo import get_mongo_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()


@router.get("/movies", response_model=List[Movie])
async def read_movies(
    title: Optional[str] = Query(None, description="Title of the movie to search"),
    genres: Optional[List[str]] = Query(None, description="Genres to search for"),
    year: Optional[str] = Query(
        None,
        description="Year of release to search (e.g., '2020', '2000-2020', '>2000', '<2000')",
    ),
    director: Optional[str] = Query(None, description="Director to search for"),
    cast_member: Optional[str] = Query(None, description="Cast member to search for"),
    countries: Optional[List[str]] = Query(
        None, description="Countries where the movie was produced"
    ),
    imdb_rating: Optional[float] = Query(
        None, description="Minimum IMDb rating to search for"
    ),
    oscars: Optional[bool] = Query(
        None, description="Filter for movies nominated for or awarded an Oscar"
    ),
    size: int = Query(10, gt=0, le=100, description="Number of movies per search"),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    """
    Search for movies based on various filters. At least one filter must be provided.
    """
    if all(
        param is None
        for param in [
            title,
            genres,
            year,
            director,
            cast_member,
            countries,
            imdb_rating,
            oscars,
        ]
    ):
        raise HTTPException(
            status_code=400, detail="At least one filter must be provided"
        )

    movies = await search_movies(
        db,
        title,
        genres,
        year,
        director,
        cast_member,
        countries,
        imdb_rating,
        oscars,
        size,
    )

    if not movies:
        raise HTTPException(
            status_code=404, detail="No movies found with the given filters"
        )

    return movies
