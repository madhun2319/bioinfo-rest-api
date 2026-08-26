from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar

from app.schemas.pdb import PdbMetadata
from app.schemas.ncbi import GeneSummary
from app.schemas.uniprot import UniprotMetadata

T = TypeVar('T')

class ServiceResponse(BaseModel, Generic[T]):
    status: str  # 'success', 'not_found', 'error'
    data: Optional[T] = None
    error_message: Optional[str] = None

class AggregateResponse(BaseModel):
    query: str
    pdb_result: ServiceResponse[PdbMetadata]
    ncbi_result: ServiceResponse[GeneSummary]
    uniprot_result: ServiceResponse[UniprotMetadata]

class BatchAggregateRequest(BaseModel):
    terms: List[str]

class BatchAggregateResponse(BaseModel):
    results: List[AggregateResponse]
    failed_terms: List[str]
