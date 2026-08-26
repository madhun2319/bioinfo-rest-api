import pytest
from httpx import Response

import httpx

original_get = httpx.AsyncClient.get

@pytest.mark.asyncio
async def test_get_uniprot(async_client, mocker):
    mock_get = mocker.patch("httpx.AsyncClient.get")

    async def side_effect(*args, **kwargs):
        url = kwargs.get("url") or args[0]
        url_str = str(url)
        if url_str.startswith("/") or url_str.startswith("http://test"):
            return await original_get(async_client, *args, **kwargs)
        return Response(
            200,
            json={
                "primaryAccession": "P01308",
                "uniProtkbId": "INS_HUMAN",
                "proteinDescription": {
                    "recommendedName": {
                        "fullName": {"value": "Insulin"}
                    }
                },
                "genes": [{"geneName": {"value": "INS"}}],
                "organism": {"scientificName": "Homo sapiens"},
                "sequence": {"value": "MALWMRLLPLLALLALWGPDPAAAF", "length": 25}
            },
            request=mocker.Mock(),
        )

    mock_get.side_effect = side_effect

    response = await async_client.get("/api/uniprot/P01308")
    assert response.status_code == 200
    data = response.json()
    assert data["primary_accession"] == "P01308"
    assert data["protein_name"] == "Insulin"
    assert data["gene_name"] == "INS"
    assert data["organism"] == "Homo sapiens"

@pytest.mark.asyncio
async def test_get_uniprot_not_found(async_client, mocker):
    mock_get = mocker.patch("httpx.AsyncClient.get")
    async def side_effect(*args, **kwargs):
        url = kwargs.get("url") or args[0]
        url_str = str(url)
        if url_str.startswith("/") or url_str.startswith("http://test"):
            return await original_get(async_client, *args, **kwargs)
        return Response(404, json={}, request=mocker.Mock())

    mock_get.side_effect = side_effect

    response = await async_client.get("/api/uniprot/INVALID")
    assert response.status_code == 404
