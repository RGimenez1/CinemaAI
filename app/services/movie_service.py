from app.repository.database import movies_collection, build_search_query
from app.models.movie import Movie
from typing import List, Optional
from bson import ObjectId
from datetime import datetime


async def search_movies(
    title: Optional[str] = None,
    genres: Optional[List[str]] = None,
    year: Optional[int] = None,
    director: Optional[str] = None,
    cast_member: Optional[str] = None,
) -> List[Movie]:
    query = build_search_query(title, genres, year, director, cast_member)
    movies = await movies_collection.find(query).to_list(100)

    results = []
    for movie in movies:
        # Convert ObjectId to string
        if "_id" in movie and isinstance(movie["_id"], ObjectId):
            movie["_id"] = str(movie["_id"])

        # Convert datetime fields to ISO format strings
        if "released" in movie and isinstance(movie["released"], datetime):
            movie["released"] = movie["released"].isoformat()

        results.append(Movie(**movie))
    return results
