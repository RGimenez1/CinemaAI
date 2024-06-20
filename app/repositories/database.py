from typing import List, Dict
from app.models.movie import Movie
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.MONGO_DB_NAME]


async def get_movies_from_db(query_params: Dict) -> List[Movie]:
    try:
        query = {}

        if query_params.get("title"):
            query["title"] = {"$regex": query_params["title"], "$options": "i"}

        if query_params.get("genres"):
            query["genres"] = {"$in": query_params["genres"]}

        if query_params.get("year"):
            query["year"] = query_params["year"]

        if query_params.get("directors"):
            query["directors"] = {"$regex": query_params["directors"], "$options": "i"}

        if query_params.get("cast_member"):
            query["cast"] = {
                "$regex": query_params["cast_member"],
                "$options": "i",
            }  # Correct the field name to match your database schema

        # Apply pagination
        offset = (query_params["page"] - 1) * query_params["size"]
        limit = query_params["size"]
        print(query)

        movies_collection = database["movies"]
        cursor = movies_collection.find(query).skip(offset).limit(limit)
        results = await cursor.to_list(length=limit)

        # Convert MongoDB ObjectId to string and return as Pydantic models
        movies = []
        for movie in results:
            if "_id" in movie:
                movie["_id"] = str(movie["_id"])  # Convert ObjectId to string
            movies.append(Movie(**movie))

        return movies

    except Exception as e:
        # Log or handle the error as needed
        raise Exception(f"Database Error: {e}")
