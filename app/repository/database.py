from typing import Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.MONGO_DB_NAME]
movies_collection = database.get_collection("movies")


def build_search_query(
    title: Optional[str] = None,
    genres: Optional[List[str]] = None,
    year: Optional[int] = None,
    director: Optional[str] = None,
    cast_member: Optional[str] = None,
) -> Dict:
    query = {}
    if title:
        query["title"] = {
            "$regex": title,
            "$options": "i",
        }  # Case-insensitive regex search
    if genres:
        query["genres"] = {"$in": genres}
    if year:
        query["year"] = year
    if director:
        query["directors"] = {"$regex": director, "$options": "i"}
    if cast_member:
        query["cast"] = {"$regex": cast_member, "$options": "i"}
    return query
