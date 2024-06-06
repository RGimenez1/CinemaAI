from app.repository.database import database
from app.models.movie import Movie
from typing import List, Optional


async def get_movies_by_title(title: Optional[str]) -> List[Movie]:
    movies_collection = database.get_collection("movies")
    query = {}
    if title:
        query["title"] = {
            "$regex": title,
            "$options": "i",
        }  # Case-insensitive regex search
    movies = await movies_collection.find(query).to_list(100)
    return [Movie(**movie) for movie in movies]
