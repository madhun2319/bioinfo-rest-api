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
from app.schemas.uniprot import UniprotMetadata


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
)
async def _fetch_uniprot_api(url: str) -> dict:
    client = get_client()
    response = await client.get(url, headers={"Accept": "application/json"})
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="UniProt entry not found")
    response.raise_for_status()
    return response.json()


async def fetch_uniprot_metadata(accession: str) -> UniprotMetadata:
    redis = get_redis()
    cache_key = f"uniprot:{accession.upper()}"
    cached_data = await redis.get(cache_key)

    if cached_data:
        return UniprotMetadata(**json.loads(cached_data))

    url = f"https://rest.uniprot.org/uniprotkb/{accession.upper()}"

    try:
        data = await _fetch_uniprot_api(url)
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

    # Extract relevant data
    primaryAccession = data.get("primaryAccession", accession)
    entryAudit = data.get("entryAudit", {})
    entry_id = data.get("uniProtkbId", primaryAccession)
    
    proteinDescription = data.get("proteinDescription", {})
    recommendedName = proteinDescription.get("recommendedName", {})
    fullName = recommendedName.get("fullName", {}).get("value")
    
    genes = data.get("genes", [])
    gene_name = genes[0].get("geneName", {}).get("value") if genes else None
    
    organism = data.get("organism", {}).get("scientificName")
    
    sequence_data = data.get("sequence", {})
    sequence = sequence_data.get("value")
    sequence_length = sequence_data.get("length")

    metadata = UniprotMetadata(
        entry_id=entry_id,
        primary_accession=primaryAccession,
        protein_name=fullName,
        gene_name=gene_name,
        organism=organism,
        sequence=sequence,
        sequence_length=sequence_length
    )

    await redis.setex(cache_key, 3600, metadata.model_dump_json())
    return metadata
