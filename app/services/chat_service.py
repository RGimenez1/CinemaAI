import uuid
from app.core.config import settings
from app.core.utils import get_system_prompt, get_tool
from app.services.message_service import MessageService
from app.services.callable_functions import CallableFunctions
from app.repositories.ai_repository import AIRepository
from app.models.enums.roles import Roles
from typing import AsyncGenerator


class ChatService:
    """
    Manages the chat interactions for the CinemaAI assistant.
    """

    def __init__(self, context_id: str = None):
        self.context_id = context_id or str(uuid.uuid1())
        self.message_service = MessageService(self.context_id)
        self.model = settings.OPENAI_MODEL
        self.system_message = {
            "role": "system",
            "content": get_system_prompt(int(settings.SYSTEM_PROMPT_VERSION)),
        }
        self.tools = get_tool(int(settings.TOOL_VERSION))["tools"]
        self.callable_functions = CallableFunctions()
        self.ai_repository = AIRepository(self.model, self.tools)

    async def process_tool_calls(self, tool_calls):
        """
        Process tool calls by making the appropriate function calls and gathering results.
        """
        tool_results = []
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            if function_name == "movie_searcher":
                tool_result = await self.callable_functions.movie_searcher(arguments)
            else:
                tool_result = {"error": "Unknown tool call"}

            tool_results.append({"id": tool_call["id"], "result": tool_result})
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

    async def save_tool_call(self, tool_calls):
        """
        Save the assistant's decision to call a tool using the MessageService.
        """
        for tool_call in tool_calls.values():
            await self.message_service._add_message(
                {
                    "role": Roles.ASSISTANT.value,
                    "tool_calls": [tool_call],
                }
            )

    async def save_tool_results(self, tool_results):
        """
        Save the results of the tool call using the MessageService.
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
            messages = await self.message_service.get_messages()
            if not messages:
                await self.message_service._add_message(
                    {
                        "role": self.system_message["role"],
                        "content": self.system_message["content"],
                    }
                )
                messages = [
                    {
                        "role": self.system_message["role"],
                        "content": self.system_message["content"],
                    }
                ]

            await self.message_service._add_message(
                {"role": Roles.USER.value, "content": user_message}
            )
            messages = await self.message_service.get_messages()

            loop_count = 0
            max_loops = 5

            while loop_count < max_loops:
                loop_count += 1

                response = await self.ai_repository.get_streamed_response(
                    messages, self.tools
                )

                assistant_message = ""
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
                    await self.save_tool_call(tool_calls)
                    tool_results = await self.process_tool_calls(tool_calls.values())
                    await self.save_tool_results(tool_results)
                    messages = await self.message_service.get_messages()
                    continue

                if finish_reason == "stop":
                    break

            await self.message_service._add_message(
                {"role": Roles.ASSISTANT.value, "content": assistant_message}
            )

        except Exception as e:
            yield f"Unexpected Error: {str(e)}"
