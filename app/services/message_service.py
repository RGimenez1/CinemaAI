from datetime import datetime, timezone
from app.repositories.database import database
from app.models.enums.roles import Roles
from pymongo.collection import Collection


class MessageService:
    def __init__(self, context_id: str):
        self.db_repository: Collection = database.get_collection("messages")
        self.context_id = context_id
        self.messages = []

    async def get_messages(self):
        """
        Retrieve the document for the current context_id from the database.
        """
        document = await self.db_repository.find_one({"_id": self.context_id})
        if document:
            self.messages = document.get("messages", [])
        return self.messages

    def add_message(self, role: Roles, content: str):
        """
        Add a new message to the local messages list.
        """
        self.messages.append(
            {
                "role": role.value,
                "content": content,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    async def commit(self):
        """
        Commit the local messages list to the database.
        """
        if not self.messages:
            return

        # Upsert the document: if it exists, update it; if not, create it
        update_result = await self.db_repository.update_one(
            {"_id": self.context_id},
            {
                "$set": {
                    "messages": self.messages,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
            },
            upsert=True,
        )
        # Clear the local messages after committing
        self.messages = []

    def add_system_message(self, content: str):
        self.add_message(Roles.SYSTEM, content)

    def add_user_message(self, content: str):
        self.add_message(Roles.USER, content)

    def add_assistant_message(self, content: str):
        self.add_message(Roles.ASSISTANT, content)

    def add_assistant_tools(self, tool_calls: list):
        for tool_call in tool_calls:
            self.add_message(Roles.TOOL_CALLS, tool_call)

    def add_tool_answer(self, tool_call_id: str, content: str):
        self.add_message(Roles.TOOL, f"{tool_call_id}: {content}")
