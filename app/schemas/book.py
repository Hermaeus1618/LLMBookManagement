from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    genre: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = None
    year_published: Optional[int] = None

class BookCreate(BookBase):
    user_id: Optional[UUID] = None

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    content: Optional[str] = None
    year_published: Optional[int] = None

class BookResponse(BookBase):
    id: UUID
    content: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
