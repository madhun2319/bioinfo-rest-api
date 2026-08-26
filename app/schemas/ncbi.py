from pydantic import BaseModel
from typing import Optional


class GeneSummary(BaseModel):
    gene_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    organism: Optional[str] = None
    maplocation: Optional[str] = None
    summary: Optional[str] = None
    aliases: Optional[str] = None
    exoncount: Optional[int] = None
