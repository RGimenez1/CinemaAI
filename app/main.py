from fastapi import FastAPI
from app.api.routes import router as movie_router

app = FastAPI()

app.include_router(movie_router, prefix="/api")
