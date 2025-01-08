from pydantic import BaseModel
from typing import List

class MovieBase(BaseModel):
    id: int

class Platform(BaseModel):
    name: str
    logo_path: str

class Movie(MovieBase):
    title: str
    release_date: str
    description: str
    poster_path: str

class MovieDetailed(Movie):
    runtime: int
    genres: List[str]
    platforms: List[Platform]
