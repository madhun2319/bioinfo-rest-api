from fastapi import APIRouter
import asyncio
from typing import List
from app.schemas.aggregate import AggregateResponse, BatchAggregateRequest, BatchAggregateResponse
from app.services.pdb_service import fetch_pdb_metadata
from app.services.ncbi_service import fetch_gene_summary
from app.services.uniprot_service import fetch_uniprot_metadata

router = APIRouter()

async def _process_single_term(term: str) -> AggregateResponse:
    pdb_task = fetch_pdb_metadata(term)
    ncbi_task = fetch_gene_summary(term)
    uniprot_task = fetch_uniprot_metadata(term)

    results = await asyncio.gather(pdb_task, ncbi_task, uniprot_task, return_exceptions=True)

    return AggregateResponse(
        query=term, 
        pdb_result=results[0] if not isinstance(results[0], Exception) else None, 
        ncbi_result=results[1] if not isinstance(results[1], Exception) else None,
        uniprot_result=results[2] if not isinstance(results[2], Exception) else None
    )

@router.get("/aggregate", response_model=AggregateResponse)
async def get_aggregate(term: str):
    """Fetch federated data for a single term."""
    return await _process_single_term(term)

@router.post("/aggregate/batch", response_model=BatchAggregateResponse)
async def get_aggregate_batch(request: BatchAggregateRequest):
    """
    High-Throughput Batch Processing:
    Fetch federated data for up to 50 terms concurrently. 
    Uses a semaphore to prevent overwhelming upstream servers.
    """
    semaphore = asyncio.Semaphore(10) # Max 10 concurrent requests
    
    async def _sem_process(term):
        async with semaphore:
            return await _process_single_term(term)

    tasks = [_sem_process(term) for term in request.terms]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful_results = []
    failed_terms = []
    
    for term, res in zip(request.terms, results):
        if isinstance(res, Exception):
            failed_terms.append(term)
        else:
            successful_results.append(res)
            
    return BatchAggregateResponse(results=successful_results, failed_terms=failed_terms)
