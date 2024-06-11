# utils.py
from pymongo import MongoClient
from app.core.config import settings

# Initialize MongoDB client using the configured URI
client = MongoClient(settings.MONGO_URI)
db = client.get_database(settings.MONGO_DB_NAME)
system_prompt_collection = db.get_collection("system_prompt")


def get_system_prompt(version: int):
    """
    Fetches the system prompt from the MongoDB collection based on the version.

    Args:
        version (int): The version of the system prompt to fetch.

    Returns:
        str: The content of the system prompt.
    """
    prompt = system_prompt_collection.find_one({"version": version})
    if prompt:
        return prompt.get("content", "")
    return "You are Nico, a knowledgeable and friendly movie assistant of CinemaAI."  # Fallback content if no prompt is found
