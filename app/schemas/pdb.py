from pydantic import BaseModel
from typing import Optional, List


class PdbMetadata(BaseModel):
    entry_id: str
    title: Optional[str] = None
    deposition_date: Optional[str] = None
    release_date: Optional[str] = None
    resolution_combined: Optional[List[float]] = None
    experimental_method: Optional[List[str]] = None
    polymer_entity_count: Optional[int] = None
    molecular_weight: Optional[float] = None
