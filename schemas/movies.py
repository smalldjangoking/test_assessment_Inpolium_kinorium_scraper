from pydantic import BaseModel

class PlatformRating(BaseModel):
    kinorium: float
    imdb: float
    critics: int

class Actor(BaseModel):
    name: str
    role: str
    image: str

class MovieDetailResponse(BaseModel):
    url: str
    title: str
    description: str
    year: int
    country: str
    genres: list[str]
    duration: str
    budget: str
    age_restriction: str
    production_companies: list[str]
    logline: str
    actors: list[Actor]
    rating: PlatformRating
    poster: str