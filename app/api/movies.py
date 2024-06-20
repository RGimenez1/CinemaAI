from fastapi import APIRouter, Query, HTTPException
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
    page: int = Query(1, gt=0, description="Page number for pagination"),
    size: int = Query(10, gt=0, le=100, description="Number of movies per page"),
):
    """
    Search for movies based on various filters. At least one filter must be provided.
    Pagination is supported through 'page' and 'size' parameters.
    """
    if all(param is None for param in [title, genres, year, director, cast_member]):
        raise HTTPException(
            status_code=400, detail="At least one filter must be provided"
        )

    try:
        movies = await search_movies(
            title, genres, year, director, cast_member, page, size
        )

        if not movies:
            raise HTTPException(
                status_code=404, detail="No movies found with the given filters"
            )

        return movies

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while searching for movies: {e}"
        )
