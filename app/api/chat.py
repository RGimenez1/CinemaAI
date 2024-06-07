from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.services.chat_service import get_openai_response

router = APIRouter()


@router.get("/chat")
async def chat_endpoint(
    message: str = Query(..., description="Message to send to OpenAI")
):
    """
    Endpoint to handle chat messages and return a streaming response from OpenAI.
    """
    try:
        if not message:
            raise HTTPException(status_code=400, detail="Message content is required")

        # Define the async generator
        async def response_generator():
            async for chunk in get_openai_response(message):
                yield chunk

        # Return the streaming response
        return StreamingResponse(
            response_generator(),
            media_type="text/plain",
            headers={"Transfer-Encoding": "chunked"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
