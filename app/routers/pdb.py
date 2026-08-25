from fastapi import APIRouter
from app.schemas.pdb import PdbMetadata
from app.services.pdb_service import fetch_pdb_metadata

router = APIRouter()


@router.get("/{pdb_id}", response_model=PdbMetadata)
async def get_pdb(pdb_id: str):
    return await fetch_pdb_metadata(pdb_id)
