from typing import List, Dict
from app.models.movie import Movie
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.utils.data_preprocess_utils import clean_data

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
            year_query = query_params["year"]
            if "-" in year_query:
                start_year, end_year = map(int, year_query.split("-"))
                query["year"] = {"$gte": start_year, "$lte": end_year}
            elif year_query.startswith(">"):
                year = int(year_query[1:])
                query["year"] = {"$gt": year}
            elif year_query.startswith("<"):
                year = int(year_query[1:])
                query["year"] = {"$lt": year}
            else:
                year = int(year_query)
                query["year"] = year

        if query_params.get("directors"):
            query["directors"] = {"$regex": query_params["directors"], "$options": "i"}

        if query_params.get("cast_member"):
            query["cast"] = {"$regex": query_params["cast_member"], "$options": "i"}

        # Apply pagination
        offset = (query_params["page"] - 1) * query_params["size"]
        limit = query_params["size"]

        movies_collection = database["movies"]
        cursor = movies_collection.find(query).skip(offset).limit(limit)
        results = await cursor.to_list(length=limit)

        # Convert MongoDB ObjectId to string, clean data, and return as Pydantic models
        movies = []
        for movie in results:
            if "_id" in movie:
                movie["_id"] = str(movie["_id"])
            cleaned_movie = clean_data(movie)
            movies.append(Movie(**cleaned_movie))

        return movies

    except Exception as e:
        raise Exception(f"Database Error: {e}")
