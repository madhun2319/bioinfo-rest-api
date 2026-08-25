from fastapi import APIRouter
from app.schemas.ncbi import GeneSummary
from app.services.ncbi_service import fetch_gene_summary

router = APIRouter()


@router.get("/gene/{gene_id}", response_model=GeneSummary)
async def get_ncbi_gene(gene_id: str):
    return await fetch_gene_summary(gene_id)
