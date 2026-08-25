import pytest
import httpx
from httpx import Response
from app.services.pdb_service import fetch_pdb_metadata

original_get = httpx.AsyncClient.get

@pytest.mark.asyncio
async def test_get_pdb(async_client, mocker):
    mock_get = mocker.patch("httpx.AsyncClient.get")
    
    async def side_effect(*args, **kwargs):
        url = kwargs.get("url") or args[0]
        url_str = str(url)
        if url_str.startswith("/") or url_str.startswith("http://test"):
            return await original_get(async_client, *args, **kwargs)
        return Response(
            200,
            json={
                "rcsb_id": "1XYZ",
                "struct": {"title": "Test Protein"},
                "rcsb_accession_info": {"deposit_date": "2023-01-01", "initial_release_date": "2023-01-02"},
                "rcsb_entry_info": {"resolution_combined": [1.5], "polymer_entity_count": 1, "molecular_weight": 50000.0},
                "exptl": [{"method": "X-RAY DIFFRACTION"}]
            },
            request=mocker.Mock()
        )
        
    mock_get.side_effect = side_effect
    
    response = await async_client.get("/api/pdb/1XYZ")
    assert response.status_code == 200
    data = response.json()
    assert data["entry_id"] == "1XYZ"
    assert data["title"] == "Test Protein"
    assert data["resolution_combined"] == [1.5]

@pytest.mark.asyncio
async def test_get_pdb_not_found(async_client, mocker):
    mock_get = mocker.patch("httpx.AsyncClient.get")
    
    async def side_effect(*args, **kwargs):
        url = kwargs.get("url") or args[0]
        url_str = str(url)
        if url_str.startswith("/") or url_str.startswith("http://test"):
            return await original_get(async_client, *args, **kwargs)
        return Response(404, json={}, request=mocker.Mock())
        
    mock_get.side_effect = side_effect
    
    response = await async_client.get("/api/pdb/INVALID")
    assert response.status_code == 404
