from pydantic import BaseModel, Field

class UniprotMetadata(BaseModel):
    entry_id: str = Field(..., description="UniProt Knowledgebase Entry ID")
    primary_accession: str = Field(..., description="Primary Accession Number")
    protein_name: str | None = Field(None, description="Recommended name of the protein")
    gene_name: str | None = Field(None, description="Primary gene name")
    organism: str | None = Field(None, description="Scientific name of the organism")
    sequence: str | None = Field(None, description="Amino acid sequence")
    sequence_length: int | None = Field(None, description="Length of the sequence")
