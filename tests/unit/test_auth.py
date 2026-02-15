import pytest
from fastapi import HTTPException

from src.dependencies import get_current_user
from src.infrastructure.auth import MockAuthenticator


@pytest.mark.asyncio
async def test_get_current_user_valid():
    auth = MockAuthenticator()
    token = "testuser"
    user = await get_current_user(token=token, auth=auth)
    assert user.id == "user_testuser"
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_get_current_user_no_token():
    auth = MockAuthenticator()
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token=None, auth=auth)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    auth = MockAuthenticator()
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token="invalid-token", auth=auth)
    assert exc.value.status_code == 401
