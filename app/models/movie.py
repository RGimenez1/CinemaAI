from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime


class Award(BaseModel):
    wins: Optional[int]
    nominations: Optional[int]
    text: Optional[str]


class IMDb(BaseModel):
    rating: Optional[float]
    votes: Optional[int]
    id: Optional[int]


class Movie(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: Optional[str]
    imdb: Optional[IMDb]
    year: Optional[int]
    directors: Optional[List[str]]
    cast: Optional[List[str]]
    plot: Optional[str]
    genres: Optional[List[str]]
    countries: Optional[List[str]]
    runtime: Optional[int]
    poster: Optional[str]
    languages: Optional[List[str]]
    released: Optional[datetime]
    rated: Optional[str]
    awards: Optional[Award]
    fullplot: Optional[str]
    metacritic: Optional[int]
    tomatoes: Optional[
        Dict[str, Any]
    ]
    num_mflix_comments: Optional[int]
    type: Optional[str]
    writers: Optional[List[str]]
    lastupdated: Optional[str]
