import pytest
import httpx
from httpx import Response

original_get = httpx.AsyncClient.get


@pytest.mark.asyncio
async def test_get_ncbi_gene(async_client, mocker):
    mock_get = mocker.patch("httpx.AsyncClient.get")

    async def side_effect(*args, **kwargs):
        url = kwargs.get("url") or args[0]
        url_str = str(url)
        if url_str.startswith("/") or url_str.startswith("http://test"):
            return await original_get(async_client, *args, **kwargs)
        if "esearch" in url_str:
            return Response(
                200, json={"esearchresult": {"idlist": ["1234"]}}, request=mocker.Mock()
            )
        elif "esummary" in url_str:
            return Response(
                200,
                json={
                    "result": {
                        "1234": {
                            "name": "BRCA1",
                            "description": "BRCA1 DNA repair associated",
                            "organism": {"scientificname": "Homo sapiens"},
                        }
                    }
                },
                request=mocker.Mock(),
            )
        return Response(404, request=mocker.Mock())

    mock_get.side_effect = side_effect

    response = await async_client.get("/api/ncbi/gene/BRCA1")
    assert response.status_code == 200
    data = response.json()
    assert data["gene_id"] == "1234"
    assert data["name"] == "BRCA1"


@pytest.mark.asyncio
async def test_get_ncbi_gene_not_found(async_client, mocker):
    mock_get = mocker.patch("httpx.AsyncClient.get")

    async def side_effect(*args, **kwargs):
        url = kwargs.get("url") or args[0]
        url_str = str(url)
        if url_str.startswith("/") or url_str.startswith("http://test"):
            return await original_get(async_client, *args, **kwargs)
        return Response(
            200, json={"esearchresult": {"idlist": []}}, request=mocker.Mock()
        )

    mock_get.side_effect = side_effect

    response = await async_client.get("/api/ncbi/gene/UNKNOWN")
    assert response.status_code == 404
