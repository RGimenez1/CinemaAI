from datetime import datetime, timezone
from app.repository.database import database
from app.models.enums.roles import Roles


class MessageService:
    def __init__(self, context_id: str):
        self.db_repository = database.get_collection("messages")
        self.context_id = context_id
        self.messages = self.db_repository.find({"context_id": self.context_id})
        self.messages = []

    async def commit(self):
        for message in self.messages:
            await self.db_repository.insert_one(message)
        self.messages = []

    def add_message(self, role: Roles, content: str):
        self.messages.append(
            {
                "role": role.value,
                "content": content,
                "created_at": datetime.now(timezone.utc),
                "context_id": self.context_id,
            }
        )

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
