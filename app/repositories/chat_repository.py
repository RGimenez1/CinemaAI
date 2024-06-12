import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY


class OpenAIRepository:
    """
    Handles interactions with the OpenAI API for the CinemaAI assistant.
    """

    def __init__(self):
        self.model = settings.OPENAI_MODEL

    def get_streamed_response(self, conversation, tools):
        """
        Streams the response from OpenAI's chat model.
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=conversation,
                max_tokens=150,
                stream=True,
                tools=tools,
                tool_choice="auto",
            )

            return response  # Return the response object for iteration

        except Exception as e:
            raise RuntimeError(f"Error fetching OpenAI response: {str(e)}")
