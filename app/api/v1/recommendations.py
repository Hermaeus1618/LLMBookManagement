from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.db.session import get_db
from app.db.models.book import Book
from app.schemas.book import BookResponse
from app.services.llm_service import LLMService
from app.core.security import get_current_user_from_token

router = APIRouter()
llm_service = LLMService()
vectorizer = TfidfVectorizer(stop_words='english')

#
# Get book recommendations
#
@router.get("/", response_model=list[BookResponse])
async def get_recommendations(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user["id"]
    user_result = await db.execute(select(Book).where(Book.user_id == user_id))
    user_books = user_result.scalars().all()
    total_result = await db.execute(select(Book))
    total_books = total_result.scalars().all()
    
    if not user_books or not total_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendations not found.")

    user_content=[f"{book.title}\n{book.content}" for book in user_books]
    total_content=[f"{book.title}\n{book.content}" for book in total_books]
    user_matrix = vectorizer.fit_transform(user_content)
    total_matrix = vectorizer.transform(total_content)

    user_total_cosine_sim = cosine_similarity(user_matrix, total_matrix)

    score_map = []
    for i, user_similarities in enumerate(user_total_cosine_sim):
        for idx, similarity_score in enumerate(user_similarities):
            if total_content[idx] not in user_content:
                score_map.append({"score": similarity_score, "index": idx})

    sorted_map = sorted(score_map, key=lambda x: x['score'], reverse=True)[:5]

    recommendations = []
    for map in sorted_map:
        recommendations.append(total_books[map["index"]])

    return recommendations
