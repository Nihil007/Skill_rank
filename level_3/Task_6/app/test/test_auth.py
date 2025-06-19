import pytest
from httpx import AsyncClient, ASGITransport
from main import app  

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register a user
        register_payload = {
            "Username": "TestUser",
            "Email": "testuser@example.com",
            "Password": "TestPass123!",
            "ConfirmPassword": "TestPass123!"
        }
        register_response = await client.post("/auth/register", json=register_payload)
        if register_response.status_code != 200:
            print("Validation error:", register_response.json())
        assert register_response.status_code == 200
        assert "AccessToken" in register_response.json()

        # Login with the same credentials
        login_payload = {
            "Email": "testuser@example.com",
            "Password": "TestPass123!"
        }
        login_response = await client.post("/auth/login", json=login_payload)
        assert login_response.status_code == 200
        assert "AccessToken" in login_response.json()

@pytest.mark.asyncio
async def test_register_duplicate_email():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "Username": "TestUser2",
            "Email": "testuser@example.com",
            "Password": "TestPass123!",
            "ConfirmPassword": "TestPass123!"
        }
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 400
        assert "already exists" in response.text or "already in use" in response.text

@pytest.mark.asyncio
async def test_register_weak_password():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "Username": "WeakPassUser",
            "Email": "weakpass@example.com",
            "Password": "weak",
            "ConfirmPassword": "weak"
        }
        response = await client.post("/auth/register", json=payload)
        print("DEBUG: status=", response.status_code, "json=", response.json())
        assert response.status_code == 422
        assert "Password" in response.text

@pytest.mark.asyncio
async def test_register_invalid_email():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "Username": "InvalidEmailUser",
            "Email": "not-an-email",
            "Password": "TestPass123!",
            "ConfirmPassword": "TestPass123!"
        }
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 422
        assert "Email" in response.text

@pytest.mark.asyncio
async def test_register_mismatched_passwords():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "Username": "MismatchUser",
            "Email": "mismatch@example.com",
            "Password": "TestPass123!",
            "ConfirmPassword": "TestPass1234!"
        }
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 400
        assert "Passwords do not match" in response.text

@pytest.mark.asyncio
async def test_login_wrong_password():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "Email": "testuser@example.com",
            "Password": "WrongPass123!"
        }
        response = await client.post("/auth/login", json=payload)
        assert response.status_code == 401
        assert "Invalid credentials" in response.text

@pytest.mark.asyncio
async def test_login_nonexistent_email():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "Email": "doesnotexist@example.com",
            "Password": "TestPass123!"
        }
        response = await client.post("/auth/login", json=payload)
        assert response.status_code == 401
        assert "Invalid credentials" in response.text
