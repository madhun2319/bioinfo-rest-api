import json
import httpx
from fastapi import HTTPException
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from app.core.http_client import get_client
from app.core.redis_client import get_redis
from app.core.config import settings
from app.schemas.ncbi import GeneSummary

NCBI_TOOL = "BioAPIWrapper"
NCBI_EMAIL = "developer@example.com"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
)
async def _fetch_ncbi_api(url: str, params: dict) -> dict:
    client = get_client()
    if settings.NCBI_API_KEY:
        params["api_key"] = settings.NCBI_API_KEY
    response = await client.get(url, params=params)
    response.raise_for_status()
    return response.json()


async def fetch_gene_summary(gene_id: str) -> GeneSummary:
    redis = get_redis()
    cache_key = f"ncbi_gene:{gene_id.upper()}"
    cached_data = await redis.get(cache_key)

    if cached_data:
        return GeneSummary(**json.loads(cached_data))

    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "gene",
        "term": gene_id,
        "retmode": "json",
        "tool": NCBI_TOOL,
        "email": NCBI_EMAIL,
    }

    try:
        search_data = await _fetch_ncbi_api(search_url, search_params)

        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            raise HTTPException(status_code=404, detail="Gene not found")

        actual_id = id_list[0]

        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        summary_params = {
            "db": "gene",
            "id": actual_id,
            "retmode": "json",
            "tool": NCBI_TOOL,
            "email": NCBI_EMAIL,
        }

        summary_data = await _fetch_ncbi_api(summary_url, summary_params)
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (429, 503):
            raise HTTPException(
                status_code=503, detail="Upstream service unavailable or rate limited"
            )
        raise HTTPException(status_code=502, detail="Bad gateway")
    except httpx.RequestError:
        raise HTTPException(
            status_code=504, detail="Upstream service timeout or network error"
        )

    result = summary_data.get("result", {}).get(actual_id, {})
    if not result:
        raise HTTPException(status_code=404, detail="Gene summary not found")

    summary = GeneSummary(
        gene_id=actual_id,
        name=result.get("name"),
        description=result.get("description"),
        organism=result.get("organism", {}).get("scientificname"),
    )

    await redis.setex(cache_key, 3600, summary.model_dump_json())
    return summary
