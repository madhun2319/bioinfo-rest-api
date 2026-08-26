from pydantic import BaseModel
from typing import List, Optional

from app.schemas.pdb import PdbMetadata
from app.schemas.ncbi import GeneSummary
from app.schemas.uniprot import UniprotMetadata

class AggregateResponse(BaseModel):
    query: str
    pdb_result: Optional[PdbMetadata] = None
    ncbi_result: Optional[GeneSummary] = None
    uniprot_result: Optional[UniprotMetadata] = None

class BatchAggregateRequest(BaseModel):
    terms: List[str]

class BatchAggregateResponse(BaseModel):
    results: List[AggregateResponse]
    failed_terms: List[str]
