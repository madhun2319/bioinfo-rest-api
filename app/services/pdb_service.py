import httpx
from fastapi import HTTPException
from async_lru import alru_cache
from app.core.http_client import get_client
from app.schemas.pdb import PdbMetadata

@alru_cache(maxsize=200, ttl=3600)
async def fetch_pdb_metadata(pdb_id: str) -> PdbMetadata:
    client = get_client()
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id.upper()}"
    
    try:
        response = await client.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="PDB entry not found")
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (429, 503):
            raise HTTPException(status_code=503, detail="Upstream service unavailable or rate limited")
        raise HTTPException(status_code=502, detail="Bad gateway")
    except httpx.RequestError:
        raise HTTPException(status_code=504, detail="Upstream service timeout or network error")
    
    data = response.json()
    
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

    return PdbMetadata(
        entry_id=rcsb_id,
        title=title,
        deposition_date=deposition_date,
        release_date=release_date,
        resolution_combined=resolution_combined,
        experimental_method=experimental_method,
        polymer_entity_count=polymer_entity_count,
        molecular_weight=molecular_weight
    )
