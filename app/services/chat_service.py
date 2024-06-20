import uuid
from app.core.config import settings
from app.core.utils import get_system_prompt, get_tool
from app.services.message_service import MessageService
from app.services.callable_functions import CallableFunctions
from app.repositories.ai_repository import AIRepository
from app.models.enums.roles import Roles
from typing import AsyncGenerator, Dict, Any


class ChatService:
    """
    Manages the chat interactions for the CinemaAI assistant.
    """

    def __init__(self, context_id: str = None):
        self.context_id = context_id or str(uuid.uuid1())
        self.message_service = MessageService(self.context_id)
        self.system_message = self._create_system_message()
        self.model = settings.OPENAI_MODEL
        self.tools = get_tool(int(settings.TOOL_VERSION))["tools"]
        self.ai_repository = AIRepository(self.model, self.tools)
        self.callable_functions = CallableFunctions()

    def _create_system_message(self) -> Dict[str, str]:
        """
        Create the initial system message based on configuration.
        """
        return {
            "role": "system",
            "content": get_system_prompt(int(settings.SYSTEM_PROMPT_VERSION)),
        }

    async def _initialize_messages(self) -> None:
        """
        Initialize the conversation with the system message if no messages exist.
        """
        if not await self.message_service.get_messages():
            await self.message_service._add_message(self.system_message)

    async def process_tool_calls(self, tool_calls) -> list:
        """
        Process tool calls by making the appropriate function calls and gathering results.
        """
        tool_results = []
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]
            result = await self.callable_functions.execute_tool(
                function_name, arguments
            )
            tool_results.append({"id": tool_call["id"], "result": result})
        return tool_results

    def handle_chunk_tool_calls(self, tool_calls, delta):
        """
        Handles the chunk tool calls by updating the tool_calls dictionary based on the provided delta.
        """
        if not hasattr(delta, "tool_calls") or not delta.tool_calls:
            return

        for chunk_tool in delta.tool_calls:
            index = chunk_tool.index
            if index in tool_calls:
                tool_calls[index]["function"][
                    "arguments"
                ] += chunk_tool.function.arguments
            else:
                tool_calls[index] = {
                    "id": chunk_tool.id,
                    "type": chunk_tool.type,
                    "function": {
                        "name": chunk_tool.function.name,
                        "arguments": chunk_tool.function.arguments,
                    },
                }

    async def _add_tool_messages(self, tool_calls: Dict[int, Any]) -> None:
        """
        Add tool call messages to the message service.
        """
        for tool_call in tool_calls.values():
            await self.message_service._add_message(
                {
                    "role": Roles.ASSISTANT.value,
                    "tool_calls": [tool_call],
                }
            )

    async def _add_tool_results(self, tool_results: list) -> None:
        """
        Add tool results to the message service.
        """
        for result in tool_results:
            await self.message_service._add_message(
                {
                    "role": Roles.TOOL.value,
                    "tool_call_id": result["id"],
                    "content": str(result["result"]),
                }
            )

    async def stream_response(self, user_message: str) -> AsyncGenerator[str, None]:
        """
        Streams the response from OpenAI's chat model and manages tool calls.
        """
        try:
            await self._initialize_messages()

            # Add the user message
            await self.message_service._add_message(
                {"role": Roles.USER.value, "content": user_message}
            )
            messages = await self.message_service.get_messages()

            loop_count = 0
            max_loops = 5

            assistant_message = ""  # To accumulate the assistant's message

            while loop_count < max_loops:
                loop_count += 1

                # Get the streamed response from AI
                response = await self.ai_repository.get_streamed_response(
                    messages, self.tools
                )

                finish_reason = ""
                tool_calls = {}

                for chunk in response:
                    choice = chunk.choices[0]
                    delta = choice.delta
                    finish_reason = choice.finish_reason

                    if hasattr(delta, "content") and delta.content:
                        assistant_message += delta.content
                        yield delta.content

                    self.handle_chunk_tool_calls(tool_calls, delta)

                if finish_reason == "tool_calls":
                    # Save and process tool calls
                    await self._add_tool_messages(tool_calls)
                    tool_results = await self.process_tool_calls(tool_calls.values())
                    await self._add_tool_results(tool_results)
                    messages = await self.message_service.get_messages()
                    continue

                if finish_reason == "stop":
                    break

            # Save the complete assistant message
            await self.message_service._add_message(
                {"role": Roles.ASSISTANT.value, "content": assistant_message}
            )

        except Exception as e:
            yield f"Unexpected Error: {str(e)}"
