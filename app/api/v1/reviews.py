from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID, uuid4

from app.db.session import get_db
from app.db.models.review import Review
from app.db.models.book import Book
from app.core.security import get_current_user_from_token
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

#
# Add a review for a book
#
@router.post("/{book_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def add_review(book_id: UUID, review_in: ReviewCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user_from_token)):
    # Ensure book exists
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    user_id=current_user["id"]

    review = Review(book_id=book_id, user_id=user_id, **review_in.model_dump())
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

#
# Get all reviews for a book
#
@router.get("/{book_id}/reviews", response_model=list[ReviewResponse])
async def get_reviews(book_id: UUID, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user_from_token)):
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    reviews = result.scalars().all()
    return reviews
