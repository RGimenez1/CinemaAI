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


def transform_tool(tool_document):
    """
    Transforms a MongoDB tool document into the OpenAI-compatible format.

    Args:
        tool_document (dict): The MongoDB tool document.

    Returns:
        dict: The transformed tool data in OpenAI-compatible format.
    """
    if not tool_document or "function" not in tool_document:
        return {"error": "Invalid tool document format"}

    # Extract the relevant content
    tool_content = tool_document.get("function", {})

    # Ensure the format matches the expected OpenAI function format
    openai_tool_format = {
        "type": "function",
        "function": {
            "name": tool_content.get("name", ""),
            "description": tool_content.get("description", ""),
            "parameters": tool_content.get("parameters", {}),
        },
    }

    return openai_tool_format
