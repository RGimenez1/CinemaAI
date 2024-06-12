import uuid
import openai
from app.core.config import settings
from app.core.utils import get_system_prompt, get_tool
from app.services.message_service import MessageService

openai.api_key = settings.OPENAI_API_KEY


class CinemaAIChat:
    """
    A class to handle interactions with OpenAI for the CinemaAI assistant.
    """

    def __init__(self, context_id: str = None):
        # Generate a new context_id if one is not provided
        self.context_id = context_id or str(uuid.uuid1())
        self.message_service = MessageService(self.context_id)
        self.model = settings.OPENAI_MODEL
        self.system_message = {
            "role": "system",
            "content": get_system_prompt(int(settings.SYSTEM_PROMPT_VERSION)),
        }
        self.tools = get_tool(int(settings.TOOL_VERSION))["tools"]

    async def stream_response(self, user_message: str):
        """
        Streams the response from OpenAI's chat model.
        """
        try:
            # Retrieve previous messages for the given context_id
            messages = await self.message_service.get_messages()

            # If it's a new context, start with the system message
            if not messages:
                self.message_service.add_system_message(self.system_message["content"])

            # Add the new user message to the local message list
            self.message_service.add_user_message(user_message)

            # Prepare the messages for sending to OpenAI
            conversation = messages + [
                {
                    "role": self.system_message["role"],
                    "content": self.system_message["content"],
                },
                {"role": "user", "content": user_message},
            ]

            # Get the response from OpenAI
            response = openai.chat.completions.create(
                model=self.model,
                tool_choice="auto",
                tools=self.tools,
                messages=conversation,
                max_tokens=150,
                stream=True,
            )

            # Stream the response chunks and gather the full assistant message
            assistant_message = ""
            finish_reason = ""

            for chunk in response:
                choice = chunk.choices[0]
                delta = choice.delta
                finish_reason = choice.finish_reason

                if delta.content:
                    assistant_message += delta.content
                    yield delta.content
                if finish_reason == "stop":  # tool_calls ;
                    break

            # Save the assistant message to the local message list
            self.message_service.add_assistant_message(assistant_message)

            # Commit the new messages to the database
            await self.message_service.commit()

        except Exception as e:
            yield f"Error: {str(e)}"
