import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY


class OpenAIRepository:
    """
    Handles interactions with the OpenAI API for the CinemaAI assistant.
    """

    def __init__(self):
        self.model = settings.OPENAI_MODEL

    async def get_streamed_response(self, conversation, tools):
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

        except Exception as e:
            yield f"Error: {str(e)}"
