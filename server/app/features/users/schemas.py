from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        strict=True,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        strict=True,
    )
