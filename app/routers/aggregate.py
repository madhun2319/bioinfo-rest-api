from fastapi import APIRouter
import asyncio
from app.schemas.aggregate import AggregateResponse
from app.services.pdb_service import fetch_pdb_metadata
from app.services.ncbi_service import fetch_gene_summary
from app.services.uniprot_service import fetch_uniprot_metadata

router = APIRouter()


@router.get("/aggregate", response_model=AggregateResponse)
async def get_aggregate(term: str):
    pdb_task = fetch_pdb_metadata(term)
    ncbi_task = fetch_gene_summary(term)
    uniprot_task = fetch_uniprot_metadata(term)

    results = await asyncio.gather(pdb_task, ncbi_task, uniprot_task, return_exceptions=True)

    pdb_result = None
    if not isinstance(results[0], Exception):
        pdb_result = results[0]

    ncbi_result = None
    if not isinstance(results[1], Exception):
        ncbi_result = results[1]

    uniprot_result = None
    if not isinstance(results[2], Exception):
        uniprot_result = results[2]

    return AggregateResponse(
        query=term, 
        pdb_result=pdb_result, 
        ncbi_result=ncbi_result,
        uniprot_result=uniprot_result
    )
