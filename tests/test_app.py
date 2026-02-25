import pytest
from httpx import AsyncClient
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("name" in activity for activity in data)

@pytest.mark.asyncio
async def test_signup_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First, get an activity name
        activities = (await ac.get("/activities")).json()
        activity_name = activities[0]["name"]
        payload = {"student": "alice"}
        response = await ac.post(f"/activities/{activity_name}/signup", json=payload)
    assert response.status_code == 200
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_signup_duplicate():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        activities = (await ac.get("/activities")).json()
        activity_name = activities[0]["name"]
        payload = {"student": "bob"}
        await ac.post(f"/activities/{activity_name}/signup", json=payload)
        response = await ac.post(f"/activities/{activity_name}/signup", json=payload)
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_signup_nonexistent_activity():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"student": "charlie"}
        response = await ac.post("/activities/NonexistentActivity/signup", json=payload)
    assert response.status_code == 404
    assert "not found" in response.json().get("detail", "")

# Optionally, test full activity logic if capacity is enforced in app.py
