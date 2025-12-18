import pytest

from fastapi import status
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import init_db

@pytest.mark.asyncio
async def test_register_and_login():
    # Initialize DB for testing
    await init_db()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://0.0.0.0:8000") as client:
        #
        # Test Registration
        #
        response = await client.post(
            "/api/v1/auth/register",
            json={"username": "testuser", "password": "testpass123"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "access_token" in data

        #
        # Test Duplicate Registration
        #
        response = await client.post(
            "/api/v1/auth/register",
            json={"username": "testuser", "password": "testpass123"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        #
        # Test Login
        #
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "password": "testpass123"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data

        #
        # Test Invalid Login
        #
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "password": "wrongpass"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
