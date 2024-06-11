from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import StreamingResponse
import uuid
from app.models.requests.chat_request import ChatRequest
from app.services.chat_service import CinemaAIChat
from pydantic import BaseModel

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(request_body: ChatRequest):
    """
    Endpoint to handle chat messages and return a streaming response from OpenAI.
    """
    try:
        # Extract context_id and message
        context_id = request_body.context_id
        message = request_body.message

        # Create an instance of CinemaAIChat
        ai_chat = CinemaAIChat(context_id)

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
