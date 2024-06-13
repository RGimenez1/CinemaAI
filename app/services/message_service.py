from datetime import datetime, timezone
import json
from app.repositories.database import database
from app.models.enums.roles import Roles
from pymongo.collection import Collection


class MessageService:
    def __init__(self, context_id: str):
        self.db_repository: Collection = database.get_collection("messages")
        self.context_id = context_id

    async def get_messages(self):
        """
        Retrieve the document for the current context_id from the database.
        """
        document = await self.db_repository.find_one({"_id": self.context_id})
        return document.get("messages", []) if document else []

    async def add_message(self, role: Roles, content: str):
        """
        Add a new message to the database and commit immediately.
        """
        message = {
            "role": role.value,
            "content": content,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        await self.db_repository.update_one(
            {"_id": self.context_id},
            {
                "$push": {
                    "messages": message,
                },
                "$set": {
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                },
            },
            upsert=True,
        )

    async def add_system_message(self, content: str):
        await self.add_message(Roles.SYSTEM, content)

    async def add_user_message(self, content: str):
        await self.add_message(Roles.USER, content)

    async def add_assistant_message(self, content: str):
        await self.add_message(Roles.ASSISTANT, content)

    async def add_assistant_tool_call(self, tool_call: dict):
        """
        Add a tool call message from the assistant and commit immediately.
        """
        tool_call_message = {
            "tool_calls": [tool_call],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        await self.add_message(Roles.ASSISTANT, tool_call_message)

    async def add_tool_result(self, tool_call_id: str, content: str):
        """
        Add the result of a tool call and commit immediately.
        """
        tool_result_message = {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content,
        }

        await self.add_message(Roles.TOOL, tool_result_message)