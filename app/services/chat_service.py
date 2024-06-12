from app.repositories.chat_repository import OpenAIRepository
from app.services.message_service import MessageService
from app.core.utils import get_system_prompt, get_tool
from app.core.config import settings
import uuid


class CinemaAIChat:
    """
    A class to handle chat interactions for the CinemaAI assistant.
    """

    def __init__(self, context_id: str = None):
        self.context_id = context_id or str(uuid.uuid1())
        self.message_service = MessageService(self.context_id)
        self.openai_repository = OpenAIRepository()
        self.system_message = {
            "role": "system",
            "content": get_system_prompt(int(settings.SYSTEM_PROMPT_VERSION)),
        }
        self.tools = get_tool(int(settings.TOOL_VERSION))["tools"]

    async def stream_response(self, user_message: str):
        """
        Handles the chat process, including retrieving and updating the context, and streaming responses.
        """
        try:
            # Retrieve previous messages
            messages = await self.message_service.get_messages()

            # If no previous messages, add the system message
            if not messages:
                self.message_service.add_system_message(self.system_message["content"])

            # Add the user message
            self.message_service.add_user_message(user_message)

            # Prepare the conversation for OpenAI
            conversation = messages + [
                {
                    "role": self.system_message["role"],
                    "content": self.system_message["content"],
                },
                {"role": "user", "content": user_message},
            ]

            # Get the streamed response from OpenAI
            async for response_chunk in self.openai_repository.get_streamed_response(
                conversation, self.tools
            ):
                yield response_chunk

            # Collect the assistant's response for saving
            assistant_message = "".join(
                [
                    chunk
                    async for chunk in self.openai_repository.get_streamed_response(
                        conversation, self.tools
                    )
                ]
            )

            # Save the assistant message
            self.message_service.add_assistant_message(assistant_message)

            # Commit changes
            await self.message_service.commit()

        except Exception as e:
            yield f"Error: {str(e)}"
