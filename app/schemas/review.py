from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, conint, ConfigDict


class ReviewBase(BaseModel):
    review_text: Optional[str] = Field(None, max_length=2000)
    rating: conint(ge=1, le=5)  # Ensures rating between 1 and 5


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: UUID
    book_id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewSummary(BaseModel):
    average_rating: float
    total_reviews: int
    summary_text: Optional[str] = None
