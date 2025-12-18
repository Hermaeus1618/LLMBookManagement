import pytest

from fastapi import status
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import init_db

@pytest.mark.asyncio
async def test_books_crud():
    # Initialize DB for testing
    await init_db()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://0.0.0.0:8000", timeout=30) as client:
        #
        # Generate Token
        #
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "password": "testpass123"},
        )
        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]
        
        #
        # Create a book
        #
        book_data={
            "title": "The Great Gatsby",
            "author": "Nick Carraway",
            "genre": "Fantasy",
            "content": "The Great Gatsby is a novel written by American author F. Scott Fitzgerald. The story is narrated by Nick Carraway, who moves to Long Island in the summer of 1922. He rents a small house next to the mansion of the mysterious Jay Gatsby, a wealthy man known for hosting lavish parties. Nick befriends Gatsby and learns that he is in love with Daisy Buchanan, Nick's cousin, who is married to Tom Buchanan. Gatsby's attempts to win back Daisy ultimately lead to tragedy, as misunderstandings and confrontations lead to death and ruin. The novel explores themes of the American Dream, class, love, and the moral decay of society.",
            "year_published": 2012
        }
        response = await client.post("/api/v1/books/", json=book_data, params={"token": token})
        assert response.status_code == status.HTTP_201_CREATED
        book = response.json()
        book_id = book["id"]
        assert book["title"] == "The Great Gatsby"

        #
        # Get all books
        #
        response = await client.get("/api/v1/books/", params={"token": token})
        assert response.status_code == status.HTTP_200_OK
        books = response.json()
        assert any(b["id"] == book_id for b in books)

        #
        # Get book by ID
        #
        response = await client.get(f"/api/v1/books/{book_id}", params={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "The Great Gatsby"

        #
        # Update book
        #
        update_data = {"title": "Updated The Great Gatsby"}
        response = await client.put(f"/api/v1/books/{book_id}", json=update_data, params={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Updated The Great Gatsby"

        #
        # Generate summary
        #
        response = await client.post(f"/api/v1/books/{book_id}/summary", params={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert "summary" in response.json()

        #
        # Delete book
        #
        response = await client.delete(f"/api/v1/books/{book_id}", params={"token": token})
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Confirm deletion
        response = await client.get(f"/api/v1/books/{book_id}", params={"token": token})
        assert response.status_code == status.HTTP_404_NOT_FOUND
