from pydantic import BaseModel, field_validator

class PlatformRating(BaseModel):
    platform: str
    rating: str

class Person(BaseModel):
    name: str
    image: str | None = None

    @field_validator('name', mode='after')
    def clean_name(cls, v: str) -> str:
        return v.strip()

class RoleGroup(BaseModel):
    role: str
    people: list[Person]

class MovieDetail(BaseModel):
    url: str
    title: str
    description: str
    year: int
    country: list[str]
    duration: str
    budget: str
    poster: str
    age_restriction: str
    logline: str
    production_companies: list[str]
    genres: list[str]
    ratings: list[PlatformRating]
    crew: list[RoleGroup]

    @field_validator('logline', mode='after')
    def clean_logline(cls, v: str) -> str:
        return v.replace("»", "").replace("«", "").strip()