import openai
from app.core.config import settings

# Set up the OpenAI API key
openai.api_key = settings.OPENAI_API_KEY


async def get_openai_response(message: str):
    """
    Interacts with OpenAI to get a response for a given message.
    Returns a generator to stream the response.
    """
    try:
        # Initiate the API call for chat completion with streaming
        response = openai.chat.completions.create(
            model="gpt-4o",  # Specify the model to use
            messages=[
                {
                    "role": "system",
                    "content": "You are CinemaAI, a knowledgeable and friendly movie assistant.",
                },
                {"role": "user", "content": message},
            ],
            max_tokens=150,
            stream=True,  # Enable streaming
        )

        # Stream the response chunks
        # TODO: handle stop and tools scenarios
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
                return

    except Exception as e:
        yield f"Error: {str(e)}"
