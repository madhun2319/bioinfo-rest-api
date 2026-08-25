import httpx
from fastapi import HTTPException
from async_lru import alru_cache
from app.core.http_client import get_client
from app.schemas.ncbi import GeneSummary

NCBI_TOOL = "BioAPIWrapper"
NCBI_EMAIL = "developer@example.com"

@alru_cache(maxsize=200, ttl=3600)
async def fetch_gene_summary(gene_id: str) -> GeneSummary:
    client = get_client()
    
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "gene",
        "term": gene_id,
        "retmode": "json",
        "tool": NCBI_TOOL,
        "email": NCBI_EMAIL
    }
    
    try:
        search_resp = await client.get(search_url, params=search_params)
        search_resp.raise_for_status()
        search_data = search_resp.json()
        
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
            "email": NCBI_EMAIL
        }
        
        summary_resp = await client.get(summary_url, params=summary_params)
        summary_resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (429, 503):
            raise HTTPException(status_code=503, detail="Upstream service unavailable or rate limited")
        raise HTTPException(status_code=502, detail="Bad gateway")
    except httpx.RequestError:
        raise HTTPException(status_code=504, detail="Upstream service timeout or network error")
        
    summary_data = summary_resp.json()
    
    result = summary_data.get("result", {}).get(actual_id, {})
    if not result:
        raise HTTPException(status_code=404, detail="Gene summary not found")
        
    return GeneSummary(
        gene_id=actual_id,
        name=result.get("name"),
        description=result.get("description"),
        organism=result.get("organism", {}).get("scientificname")
    )
