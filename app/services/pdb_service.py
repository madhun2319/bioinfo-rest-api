import json
import httpx
from fastapi import HTTPException
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.http_client import get_client
from app.core.redis_client import get_redis
from app.schemas.pdb import PdbMetadata

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError))
)
async def _fetch_pdb_api(url: str) -> dict:
    client = get_client()
    response = await client.get(url)
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="PDB entry not found")
    response.raise_for_status()
    return response.json()

async def fetch_pdb_metadata(pdb_id: str) -> PdbMetadata:
    redis = get_redis()
    cache_key = f"pdb:{pdb_id.upper()}"
    cached_data = await redis.get(cache_key)
    
    if cached_data:
        return PdbMetadata(**json.loads(cached_data))

    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id.upper()}"
    
    try:
        data = await _fetch_pdb_api(url)
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (429, 503):
            raise HTTPException(status_code=503, detail="Upstream service unavailable or rate limited")
        raise HTTPException(status_code=502, detail="Bad gateway")
    except httpx.RequestError:
        raise HTTPException(status_code=504, detail="Upstream service timeout or network error")
    
    rcsb_id = data.get("rcsb_id", pdb_id)
    struct = data.get("struct", {})
    title = struct.get("title")
    
    accession_info = data.get("rcsb_accession_info", {})
    deposition_date = accession_info.get("deposit_date")
    release_date = accession_info.get("initial_release_date")
    
    entry_info = data.get("rcsb_entry_info", {})
    resolution_combined = entry_info.get("resolution_combined")
    polymer_entity_count = entry_info.get("polymer_entity_count")
    molecular_weight = entry_info.get("molecular_weight")
    
    exptl = data.get("exptl", [])
    experimental_method = [e.get("method") for e in exptl if "method" in e] if exptl else None

    metadata = PdbMetadata(
        entry_id=rcsb_id,
        title=title,
        deposition_date=deposition_date,
        release_date=release_date,
        resolution_combined=resolution_combined,
        experimental_method=experimental_method,
        polymer_entity_count=polymer_entity_count,
        molecular_weight=molecular_weight
    )
    
    await redis.setex(cache_key, 3600, metadata.model_dump_json())
    return metadata
