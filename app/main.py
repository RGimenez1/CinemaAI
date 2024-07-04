from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from pathlib import Path  # Ensure this is imported correctly
from app.api.movies import router as movie_router
from app.api.cinema import router as cinema_router
from app.api.tool_caller import router as tool_caller_router

# Initialize the FastAPI application
app = FastAPI()

# Dynamically set the servers
app.servers = [
    {"url": settings.SERVER_HOST, "description": "API Server"},
    # Add more servers as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Redirect root URL to /docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# Include the movie and chat routers
app.include_router(movie_router, prefix="/movies", tags=["Movies"])
app.include_router(cinema_router, prefix="/cinema", tags=["Cinema"])
app.include_router(tool_caller_router, prefix="/tool", tags=["AI Tools"])

# Setup the templates directory
templates = Jinja2Templates(directory="app/templates")

# Mount static files
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

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
