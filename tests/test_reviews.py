import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from uuid import UUID

from app.main import app
from app.db.session import init_db


@pytest.mark.asyncio
async def test_reviews():
    # Initialize DB
    await init_db()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://0.0.0.0:8000") as client:
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
        # Create a book first
        #
        book_data = {
            "title": "The Great Gatsby",
            "author": "Nick Carraway",
            "genre": "Fantasy",
            "year_published": 2012
        }
        book_resp = await client.post("/api/v1/books/", json=book_data, params={"token": token})
        book_id = book_resp.json()["id"]

        #
        # Add a review
        #
        review_data = {"review_text": "Great book!", "rating": 5}
        review_resp = await client.post(f"/api/v1/books/{book_id}/reviews", json=review_data, params={"token": token})
        assert review_resp.status_code == status.HTTP_201_CREATED
        review = review_resp.json()
        assert review["review_text"] == "Great book!"
        assert review["rating"] == 5

        #
        # Retrieve reviews
        #
        response = await client.get(f"/api/v1/books/{book_id}/reviews", params={"token": token})
        assert response.status_code == status.HTTP_200_OK
        reviews = response.json()
        assert any(r["id"] == review["id"] for r in reviews)
