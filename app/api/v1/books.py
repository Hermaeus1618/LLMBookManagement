from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.db.session import get_db
from app.db.models.book import Book
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.services.llm_service import LLMService
from app.core.security import get_current_user_from_token

router = APIRouter()
llm_service = LLMService()

#
# Add a new book
#
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user["id"]
    book_data = book_in.model_dump()
    book_data["user_id"] = user_id
    new_book = Book(**book_data)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

#
# Retrieve all books
#
@router.get("/", response_model=list[BookResponse])
async def get_books(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user["id"]
    result = await db.execute(select(Book).where(Book.user_id == user_id))
    books = result.scalars().all()
    return books

#
# Retrieve a book by ID
#
@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user["id"]
    result = await db.execute(select(Book).where((Book.id == book_id) & (Book.user_id == user_id)))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    return book

#
# Update a book
#
@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: UUID, book_in: BookUpdate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user["id"]
    result = await db.execute(select(Book).where((Book.id == book_id) & (Book.user_id == user_id)))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")

    for key, value in book_in.model_dump(exclude_unset=True).items():
        setattr(book, key, value)

    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book

#
# Delete a book
#
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user["id"]
    result = await db.execute(select(Book).where((Book.id == book_id) & (Book.user_id == user_id)))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")

    await db.delete(book)
    await db.commit()
    return None

#
# Generate summary for a book
#
@router.post("/{book_id}/summary", response_model=BookResponse)
async def generate_book_summary(book_id: UUID, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user["id"]
    result = await db.execute(select(Book).where((Book.id == book_id) & (Book.user_id == user_id)))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")

    if book.summary:
        return book

    book.summary = await llm_service.generate_summary(book.content)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book
