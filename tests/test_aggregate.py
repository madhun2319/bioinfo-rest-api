import pytest
from httpx import Response

@pytest.mark.asyncio
async def test_aggregate_success(async_client, mocker):
    mock_get = mocker.patch("httpx.AsyncClient.get")
    
    def side_effect(url, *args, **kwargs):
        if "rcsb.org" in url:
            return Response(200, json={"rcsb_id": "1XYZ", "struct": {"title": "Test"}}, request=mocker.Mock())
        elif "esearch" in url:
            return Response(200, json={"esearchresult": {"idlist": ["1234"]}}, request=mocker.Mock())
        elif "esummary" in url:
            return Response(200, json={"result": {"1234": {"name": "GeneX"}}}, request=mocker.Mock())
        return Response(404, request=mocker.Mock())
        
    mock_get.side_effect = side_effect
    
    response = await async_client.get("/api/aggregate?term=1XYZ")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "1XYZ"
    assert data["pdb_result"]["entry_id"] == "1XYZ"
    assert data["ncbi_result"]["gene_id"] == "1234"

@pytest.mark.asyncio
async def test_aggregate_partial_failure(async_client, mocker):
    mock_get = mocker.patch("httpx.AsyncClient.get")
    
    def side_effect(url, *args, **kwargs):
        if "rcsb.org" in url:
            return Response(404, json={}, request=mocker.Mock())
        elif "esearch" in url:
            return Response(200, json={"esearchresult": {"idlist": ["1234"]}}, request=mocker.Mock())
        elif "esummary" in url:
            return Response(200, json={"result": {"1234": {"name": "GeneX"}}}, request=mocker.Mock())
        return Response(404, request=mocker.Mock())
        
    mock_get.side_effect = side_effect
    
    response = await async_client.get("/api/aggregate?term=1XYZ")
    assert response.status_code == 200
    data = response.json()
    assert data["pdb_result"] is None
    assert data["ncbi_result"]["gene_id"] == "1234"
