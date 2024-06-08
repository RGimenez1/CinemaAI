from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.services.chat_service import CinemaAIChat

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(
    message: str = Query(..., description="Message to send to OpenAI")
):
    """
    Endpoint to handle chat messages and return a streaming response from OpenAI.
    """
    try:
        if not message:
            raise HTTPException(status_code=400, detail="Message content is required")

        # Create an instance of CinemaAIChat
        ai_chat = CinemaAIChat()

        # Define the async generator for streaming the response
        async def response_generator():
            async for chunk in ai_chat.stream_response(message):
                yield chunk

        # Return the streaming response
        return StreamingResponse(
            response_generator(),
            media_type="text/plain",
            headers={"Transfer-Encoding": "chunked"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
