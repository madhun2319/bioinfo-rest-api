import asyncio
import json
from app.services.pdb_service import fetch_pdb_metadata
from app.services.ncbi_service import fetch_gene_summary
from app.services.uniprot_service import fetch_uniprot_metadata
from app.core.http_client import get_client, close_client
import app.core.redis_client as rc
from unittest.mock import AsyncMock

async def main():
    # Mock Redis to avoid needing a local Redis server
    mock = AsyncMock()
    mock.get.return_value = None
    rc._redis_client = mock
    
    # Initialize HTTP client
    get_client()
    
    print("--- PDB Result (JSON) ---")
    pdb = await fetch_pdb_metadata('1CRN')
    print(pdb.model_dump_json(indent=2))
    
    print("\n--- NCBI Result (JSON) ---")
    ncbi = await fetch_gene_summary('BRCA1')
    print(ncbi.model_dump_json(indent=2))
    
    print("\n--- UniProt Result (JSON) ---")
    uniprot = await fetch_uniprot_metadata('P01308')
    print(uniprot.model_dump_json(indent=2))
    
    await close_client()

if __name__ == '__main__':
    asyncio.run(main())
