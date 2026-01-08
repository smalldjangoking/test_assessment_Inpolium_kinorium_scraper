from pydantic import BaseModel

class PlatformRating(BaseModel):
    platform: str
    rating: str

class Person(BaseModel):
    name: str
    image: str | None = None

class RoleGroup(BaseModel):
    role: str
    people: list[Person]

class MovieDetail(BaseModel):
    url: str
    title: str
    description: str
    year: int
    country: str
    duration: str
    budget: str
    poster: str
    age_restriction: str
    logline: str
    production_companies: list[str]
    genres: list[str]
    ratings: list[PlatformRating]
    crew: list[RoleGroup]