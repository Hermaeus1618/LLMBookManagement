from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.db.session import get_db
from app.db.models.book import Book
from app.schemas.book import BookResponse
from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()


#
# Get book recommendations
#
@router.get("/", response_model=list[BookResponse])
async def get_recommendations(user_id: UUID | None = None, db: AsyncSession = Depends(get_db)):
    """
    Returns recommended books for a user.
    Currently uses placeholder logic: returns first 5 books.
    Can be replaced with LLM-based personalized recommendations.
    """
    result = await db.execute(select(Book).limit(5))
    books = result.scalars().all()
    return books
