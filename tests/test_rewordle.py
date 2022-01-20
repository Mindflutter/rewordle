import pytest
from httpx import AsyncClient

from asgi import app

pytestmark = [pytest.mark.usefixtures("db_tables", "db_app", "db_data"), pytest.mark.asyncio]


async def test_start_game():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/rewordle/start")
    assert response.status_code == 201
    assert response.json() == {"game_id": 2}


async def test_word_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/rewordle/guess/1", json={"guess_word": "abcde"})
    assert response.status_code == 404
    assert response.json() == {"message": "Word abcde not found"}


async def test_game_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/rewordle/guess/2", json={"guess_word": "audio"})
    assert response.status_code == 404
    assert response.json() == {"message": "Game id 2 not found"}


async def test_payload_missing():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/rewordle/guess/1")
    assert response.status_code == 422
    assert response.json() == {"detail": [{"loc": ["body"], "msg": "field required", "type": "value_error.missing"}]}


async def test_wrong_game_id():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/rewordle/guess/WRONG", json={"guess_word": "audio"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{"loc": ["path", "game_id"], "msg": "value is not a valid integer", "type": "type_error.integer"}]
    }


async def test_guess_ok():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/rewordle/guess/1", json={"guess_word": "adieu"})
    assert response.status_code == 200
    assert response.json() == {"a": "green", "d": "yellow", "e": "gray", "i": "yellow", "u": "yellow"}
