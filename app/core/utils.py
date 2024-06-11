# utils.py
from pymongo import MongoClient
from app.core.config import settings

# Initialize MongoDB client using the configured URI
client = MongoClient(settings.MONGO_URI)
db = client.get_database(settings.MONGO_DB_NAME)
system_prompt_collection = db.get_collection("system_prompt")
tools_collection = db.get_collection("tools")


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


def get_tool(version: int):
    """
    Fetches the tool information from the MongoDB collection based on the version.

    Args:
        version (int): The version of the tool to fetch.

    Returns:
        dict: The details of the tool.
    """
    tool = tools_collection.find_one({"version": version})
    if tool:
        # Convert ObjectId to string
        tool["_id"] = str(tool["_id"])
        return tool
    return {"error": "Tool not found"}  # Fallback if no tool is found
