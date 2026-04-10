from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=6, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str


class GenreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ReviewOut(BaseModel):
    id: int
    username: str
    rating: int | None = None
    content: str
    created_at: datetime
    updated_at: datetime
    is_mine: bool = False


class GameCardOut(BaseModel):
    id: int
    title: str
    short_description: str
    cover_path: str
    genres: list[str]
    average_rating: float
    reviews_count: int
    my_rating: int | None = None
    recommended_score: int = 0


class GameDetailOut(BaseModel):
    id: int
    title: str
    short_description: str
    description: str
    cover_path: str
    system_requirements: str
    genres: list[str]
    average_rating: float
    ratings_count: int
    reviews_count: int
    my_rating: int | None = None
    my_review: str | None = None
    reviews: list[ReviewOut]


class RatingRequest(BaseModel):
    value: int = Field(ge=1, le=5)


class ReviewRequest(BaseModel):
    content: str = Field(min_length=3, max_length=1200)


class PreferencesResponse(BaseModel):
    favorite_genres: list[str]
    favorite_games: list[GameCardOut]


class PreferencesUpdateRequest(BaseModel):
    genres: list[str]


class ProfileResponse(BaseModel):
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    rated_games_count: int
    reviews_count: int
    favorite_genres_count: int
    favorite_games_count: int
