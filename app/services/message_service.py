from datetime import datetime, timezone
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

    async def _add_message(self, message: dict):
        """
        Internal method to add a message to the database.
        """
        await self.db_repository.update_one(
            {"_id": self.context_id},
            {
                "$push": {"messages": message},
                "$set": {"updated_at": datetime.now(timezone.utc).isoformat()},
            },
            upsert=True,
        )

    async def add_system_message(self, content: str):
        """
        Add a system message.
        """
        message = {"role": Roles.SYSTEM.value, "content": content}
        await self._add_message(message)

    async def add_user_message(self, content: str):
        """
        Add a user message.
        """
        message = {"role": Roles.USER.value, "content": content}
        await self._add_message(message)

    async def add_assistant_message(self, content: str):
        """
        Add an assistant message.
        """
        message = {"role": Roles.ASSISTANT.value, "content": content}
        await self._add_message(message)

    async def add_assistant_tool_call(self, tool_call: dict):
        """
        Add a tool call message from the assistant.
        """
        message = {
            "role": Roles.ASSISTANT.value,
            "tool_calls": [tool_call],
        }
        await self._add_message(message)

    async def add_tool_result(self, tool_call_id: str, content: str):
        """
        Add the result of a tool call.
        """
        message = {
            "role": Roles.TOOL.value,
            "tool_call_id": tool_call_id,
            "content": content,
        }
        await self._add_message(message)
