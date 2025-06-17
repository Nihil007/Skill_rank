import pytest
from httpx import AsyncClient, ASGITransport
from main import app  # Replace with your actual FastAPI app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register a user
        register_payload = {
            "Username": "TestUser",
            "Email": "testuser@example.com",
            "Password": "TestPass123",
            "ConfirmPassword": "TestPass123"
        }
        register_response = await client.post("/auth/register", json=register_payload)
        assert register_response.status_code == 200
        assert "AccessToken" in register_response.json()

        # Login with the same credentials
        login_payload = {
            "Email": "testuser@example.com",
            "Password": "TestPass123"
        }
        login_response = await client.post("/auth/login", json=login_payload)
        assert login_response.status_code == 200
        assert "AccessToken" in login_response.json()
