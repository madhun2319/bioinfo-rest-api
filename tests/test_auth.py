import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_auth_bypassed_if_no_key_set(async_client: AsyncClient, mocker):
    mocker.patch("app.core.config.settings.APP_API_KEY", None)
    response = await async_client.get("/api/pdb/1CRN")
    # Should not return 401 because auth is bypassed when APP_API_KEY is None
    assert response.status_code != 401

@pytest.mark.asyncio
async def test_auth_fails_if_key_missing(async_client: AsyncClient, mocker):
    mocker.patch("app.core.config.settings.APP_API_KEY", "secret")
    response = await async_client.get("/api/pdb/1CRN")
    # Should return 401 Unauthorized
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_auth_succeeds_with_correct_key(async_client: AsyncClient, mocker):
    mocker.patch("app.core.config.settings.APP_API_KEY", "secret")
    # we need to also mock the actual PDB call or rely on the other mocks
    mock_get = mocker.patch("httpx.AsyncClient.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rcsb_id": "1CRN"}

    response = await async_client.get("/api/pdb/1CRN", headers={"X-API-Key": "secret"})
    assert response.status_code == 200
