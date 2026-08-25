from pydantic import BaseModel
from typing import Optional
from app.schemas.pdb import PdbMetadata
from app.schemas.ncbi import GeneSummary

class AggregateResponse(BaseModel):
    query: str
    pdb_result: Optional[PdbMetadata] = None
    ncbi_result: Optional[GeneSummary] = None
