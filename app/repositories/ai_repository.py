import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY


class AIRepository:
    """
    Handles interactions with the AI APIs, currently OpenAI, for the CinemaAI assistant.
    """

    def __init__(self, model: str, tools: dict):
        self.model = model
        self.tools = tools

    async def get_streamed_response(self, messages, tools):
        """
        Streams the response from OpenAI's chat model.
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                stream=True,
                tools=tools,
                tool_choice="auto",
            )
            return response

        except Exception as e:
            raise RuntimeError(f"Unexpected Error: {str(e)}")
