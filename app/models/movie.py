from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime


class Award(BaseModel):
    wins: Optional[int]
    nominations: Optional[int]
    text: Optional[str]

    class Config:
        extra = "allow"  # Accept additional fields not defined


class IMDb(BaseModel):
    rating: Optional[float]
    votes: Optional[int]
    id: Optional[int]

    class Config:
        extra = "allow"  # Accept additional fields not defined


class Movie(BaseModel):
    id: Optional[str] = Field(alias="_id")
    plot: Optional[str]
    genres: Optional[List[str]]
    runtime: Optional[int]
    cast: Optional[List[str]]
    num_mflix_comments: Optional[int]
    poster: Optional[str]
    title: Optional[str]
    fullplot: Optional[str]
    countries: Optional[List[str]]
    released: Optional[datetime]
    directors: Optional[List[str]]
    rated: Optional[str]
    awards: Optional[Award]
    year: Optional[int]
    imdb: Optional[IMDb]
    type: Optional[str]
    languages: Optional[List[str]]

    class Config:
        extra = "allow"  # Accept additional fields not defined
