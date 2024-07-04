from typing import List, Optional
from fastapi import HTTPException
from app.domain.models.movie import Movie
from app.infrastructure.repositories.movie_repository import get_movies_from_db


async def search_movies(
    title: Optional[str],
    genres: Optional[List[str]],
    year: Optional[str],
    director: Optional[str],
    cast_member: Optional[str],
    countries: Optional[List[str]],
    imdb_rating: Optional[float],
    oscars: Optional[bool],
    size: int = 999999,
) -> List[Movie]:
    try:
        # Build query parameters dictionary
        query_params = {
            "title": title,
            "genres": genres,
            "year": year,
            "directors": director,
            "cast_member": cast_member,
            "countries": countries,
            "imdb_rating": imdb_rating,
            "oscars": oscars,
            "size": size,
        }

        # Fetch movies using the repository layer
        movies = await get_movies_from_db(query_params, size)

        if not movies:
            # Raise a 404 exception if no movies are found
            raise HTTPException(
                status_code=404, detail="No movies found with the given filters"
            )

        return movies

    except HTTPException as e:
        # Re-raise the HTTPException for proper status code handling
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service Error: {e}")
