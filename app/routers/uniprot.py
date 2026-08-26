from fastapi import APIRouter
from app.schemas.uniprot import UniprotMetadata
from app.services.uniprot_service import fetch_uniprot_metadata

router = APIRouter()

@router.get("/{accession}", response_model=UniprotMetadata)
async def get_uniprot_metadata(accession: str):
    """
    Fetch protein metadata from UniProt given a Primary Accession (e.g., P01308 for Insulin)
    """
    return await fetch_uniprot_metadata(accession)
