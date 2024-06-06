
from app.repository.database import database
from app.models.movie import Movie
from typing import List

async def get_all_movies() -> List[Movie]:
    movies_collection = database.get_collection("movies")
    movies = await movies_collection.find().to_list(100)
    return [Movie(**movie) for movie in movies]
