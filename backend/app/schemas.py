from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ── Auth ────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise ValueError("A senha deve conter ao menos uma letra maiúscula.")
        if not any(char.isdigit() for char in value):
            raise ValueError("A senha deve conter ao menos um número.")
        if not any(not char.isalnum() for char in value):
            raise ValueError("A senha deve conter ao menos um caractere especial.")
        return value


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Game ─────────────────────────────────────────────────────────────────────

class AttemptIn(BaseModel):
    guess: str = Field(..., min_length=4, max_length=4, description="4-letter guess using A-F")


class AttemptResult(BaseModel):
    guess: str
    correct_position: int   # pegs in right position
    correct_color: int      # right color, wrong position


class GameOut(BaseModel):
    id: str
    user_id: str
    attempts: List[AttemptResult]
    attempt_count: int
    max_attempts: int = 10
    score: Optional[int]
    duration_seconds: Optional[float]
    started_at: datetime
    finished_at: Optional[datetime]
    is_won: Optional[bool]
    is_finished: bool

    model_config = {"from_attributes": True}


class GameStart(BaseModel):
    id: str
    user_id: str
    started_at: datetime
    max_attempts: int = 10

    model_config = {"from_attributes": True}


# ── Ranking ───────────────────────────────────────────────────────────────────

class RankingEntry(BaseModel):
    rank: int
    user_id: str
    username: str
    best_score: int
    total_games: int
    wins: int
