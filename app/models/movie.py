from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime


class Award(BaseModel):
    wins: Optional[int] = None
    nominations: Optional[int] = None
    text: Optional[str] = None


class IMDb(BaseModel):
    rating: Optional[float] = None
    votes: Optional[int] = None
    id: Optional[int] = None


class Movie(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: Optional[str] = None
    imdb: Optional[IMDb] = None
    year: Optional[int] = None
    directors: Optional[List[str]] = None
    cast: Optional[List[str]] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    countries: Optional[List[str]] = None
    runtime: Optional[int] = None
    poster: Optional[str] = None
    languages: Optional[List[str]] = None
    released: Optional[datetime] = None
    rated: Optional[str] = None
    awards: Optional[Award] = None
    fullplot: Optional[str] = None
    metacritic: Optional[int] = None
    tomatoes: Optional[Dict[str, Any]] = None
    num_mflix_comments: Optional[int] = None
    type: Optional[str] = None
    writers: Optional[List[str]] = None
    lastupdated: Optional[str] = None
