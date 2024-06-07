from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.api.routes import router as movie_router
from pydantic import BaseModel, ValidationError
import logging

# Initialize the FastAPI application
app = FastAPI()

# Include the movie router
app.include_router(movie_router, prefix="/api")

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Define a standard error response model
class ErrorResponse(BaseModel):
    message: str
    errors: Optional[list] = None


# Custom handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"HTTP Exception at {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(message=f"HTTP Exception: {exc.detail}").dict(),
    )


# Custom handler for general exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled Exception at {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500, content=ErrorResponse(message="Internal Server Error").dict()
    )


# Custom handler for Pydantic validation errors
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logging.error(f"Validation Error at {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(message="Validation Error", errors=exc.errors()).dict(),
    )


# Example endpoint to test error handling (remove or replace in production)
# @app.get("/cause-error")
# async def cause_error():
#     raise HTTPException(status_code=400, detail="This is a bad request error")
