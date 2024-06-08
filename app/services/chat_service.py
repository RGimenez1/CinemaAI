from pyexpat import model
import openai
from app.core.config import settings


openai.api_key = settings.OPENAI_API_KEY


class CinemaAIChat:
    """
    A class to handle interactions with OpenAI for the CinemaAI assistant.
    """

    def __init__(self):
        self.model = settings.OPENAI_MODEL
        self.system_message = {
            "role": "system",
            "content": "You are Nico, a knowledgeable and friendly movie assistant of CinemaAI.",
        }

    async def stream_response(self, user_message: str):
        """
        Streams the response from OpenAI's chat model.
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    self.system_message,
                    {"role": "user", "content": user_message},
                ],
                max_tokens=150,
                stream=True,
            )

            # Stream the response chunks
            assistant_message = ""
            finish_reason = ""

            for chunk in response:
                choice = chunk.choices[0]
                delta = choice.delta
                finish_reason = choice.finish_reason

                if delta.content:
                    assistant_message += delta.content
                    yield delta.content
                if finish_reason == "stop":
                    break

        except Exception as e:
            yield f"Error: {str(e)}"
