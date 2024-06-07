from pydantic import ValidationError
from app.repository.database import movies_collection, build_search_query
from app.models.movie import Movie
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)


async def search_movies(
    title: Optional[str] = None,
    genres: Optional[List[str]] = None,
    year: Optional[int] = None,
    director: Optional[str] = None,
    cast_member: Optional[str] = None,
) -> List[Movie]:
    query = build_search_query(title, genres, year, director, cast_member)

    try:
        movies = await movies_collection.find(query).to_list(20)
    except Exception as e:
        logging.error(f"Error fetching movies from the database: {e}")
        return []  # Return an empty list if the database query fails

    results = []
    for movie in movies:
        # Convert ObjectId to string
        if "_id" in movie and isinstance(movie["_id"], ObjectId):
            movie["_id"] = str(movie["_id"])

        # Convert datetime fields to ISO format strings
        if "released" in movie and isinstance(movie["released"], datetime):
            movie["released"] = movie["released"].isoformat()

        try:
            # Append the movie to results after conversion
            results.append(Movie(**movie))
        except ValidationError as e:
            logging.error(
                f"Error converting movie {movie.get('title', 'unknown')}: {e}"
            )

    return results
