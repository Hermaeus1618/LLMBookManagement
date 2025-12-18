from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID, uuid4

from app.db.session import get_db
from app.db.models.review import Review
from app.db.models.book import Book
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewSummary
from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()


#
# Add a review for a book
#
@router.post("/{book_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def add_review(book_id: UUID, review_in: ReviewCreate, db: AsyncSession = Depends(get_db)):
    # Ensure book exists
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    # TODO: replace with authenticated user
    user_id = uuid4()  # placeholder
    user_id="9589e349-05ec-4171-a933-c00c03cf69fc"

    review = Review(book_id=book_id, user_id=user_id, **review_in.dict())
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


#
# Get all reviews for a book
#
@router.get("/{book_id}/reviews", response_model=list[ReviewResponse])
async def get_reviews(book_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    reviews = result.scalars().all()
    return reviews


#
# Get aggregated review summary
#
@router.get("/{book_id}/summary", response_model=ReviewSummary)
async def get_review_summary(book_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    reviews = result.scalars().all()
    if not reviews:
        return ReviewSummary(average_rating=0, total_reviews=0, summary_text="No reviews yet.")

    avg_rating = sum(r.rating for r in reviews) / len(reviews)
    total_reviews = len(reviews)

    # Generate aggregated summary via LLM
    combined_text = "\n".join(r.review_text or "" for r in reviews)
    summary_text = await llm_service.generate_summary(combined_text)

    return ReviewSummary(average_rating=avg_rating, total_reviews=total_reviews, summary_text=summary_text)
