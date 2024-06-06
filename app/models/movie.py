
from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    director: str
    year: int
    imdb_score: float
