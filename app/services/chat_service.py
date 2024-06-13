import uuid
import openai
from app.core.config import settings
from app.core.utils import get_system_prompt, get_tool
from app.services.message_service import MessageService
from app.services.callable_functions import CallableFunctions
from app.models.enums.roles import Roles  # Ensure Roles is correctly imported

openai.api_key = settings.OPENAI_API_KEY


class CinemaAIChat:
    """
    A class to handle interactions with OpenAI for the CinemaAI assistant.
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

    async def process_tool_calls(self, tool_calls):
        """
        Process tool calls by making the appropriate function calls and gathering results.
        """
        tool_results = []
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            # Dynamically call the appropriate function
            if function_name == "movie_searcher":
                tool_result = await self.callable_functions.movie_searcher(arguments)
            else:
                tool_result = {"error": "Unknown tool call"}

            ### this is what should be passed back to the AI model as a new message: tool + result
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
            # Add the tool call as an assistant message using the new method
            await self.message_service.add_assistant_tool_call(
                {
                    "id": tool_call["id"],
                    "type": tool_call["type"],
                    "function": {
                        "name": tool_call["function"]["name"],
                        "arguments": tool_call["function"][
                            "arguments"
                        ],  # Pass as dictionary
                    },
                }
            )

    async def save_tool_results(self, tool_results):
        """
        Save the results of the tool call using the MessageService.
        """
        for result in tool_results:
            # Add the tool result as a tool message using the new method
            await self.message_service.add_tool_result(
                tool_call_id=result["id"], content=str(result["result"])
            )
            # await self.message_service.commit()

    async def stream_response(self, user_message: str):
        """
        Streams the response from OpenAI's chat model and manages tool calls.
        """
        try:
            messages = await self.message_service.get_messages()
            if not messages:
                await self.message_service.add_system_message(
                    self.system_message["content"]
                )
                messages = [
                    {
                        "role": self.system_message["role"],
                        "content": self.system_message["content"],
                    }
                ]

            await self.message_service.add_user_message(user_message)
            messages = (
                await self.message_service.get_messages()
            )
            
            print(messages)
            response = openai.chat.completions.create(
                model=self.model,
                tool_choice="auto",
                tools=self.tools,
                messages=messages,
                max_tokens=150,
                stream=True,
            )

            assistant_message = ""
            finish_reason = ""
            tool_calls = {}

            for chunk in response:
                choice = chunk.choices[0]
                delta = choice.delta
                finish_reason = choice.finish_reason

                # Check if delta has content and yield it
                if hasattr(delta, "content") and delta.content:
                    assistant_message += delta.content
                    yield delta.content

                # Handle tool calls within the chunks
                self.handle_chunk_tool_calls(tool_calls, delta)

                if finish_reason == "tool_calls":
                    # Save the assistant's decision to call a tool
                    print(f"Tool calls: {tool_calls}")
                    await self.save_tool_call(tool_calls)

                    # Process the tool calls
                    tool_results = await self.process_tool_calls(tool_calls.values())

                    # Save the tool call results
                    await self.save_tool_results(tool_results)

                    ### TODO: resend to model to get the final response
                    # # Generate the final assistant response using the tool results
                    # for result in tool_results:
                    #     assistant_response = (
                    #         f"Here is what I found:\n{result['result']}"
                    #     )
                    #     await self.message_service.add_assistant_message(
                    #         assistant_response
                    #     )

                    # End processing here to avoid infinite loop
                    return

                if finish_reason == "stop":
                    break

            await self.message_service.add_assistant_message(assistant_message)

        except Exception as e:
            yield f"Error: {str(e)}"
