import asyncio
from app.services.pdb_service import fetch_pdb_metadata
from app.services.ncbi_service import fetch_gene_summary
from app.core.http_client import get_client, close_client
import app.core.redis_client as rc
from unittest.mock import AsyncMock

async def main():
    # Mock Redis
    mock = AsyncMock()
    mock.get.return_value = None
    rc._redis_client = mock
    
    # Initialize HTTP client
    get_client()
    
    print('Fetching from PDB API (1CRN)...')
    pdb = await fetch_pdb_metadata('1CRN')
    print('PDB Result:', pdb.title)
    
    print('\nFetching from NCBI API (BRCA1)...')
    ncbi = await fetch_gene_summary('BRCA1')
    print('NCBI Result:', ncbi.description, '-', ncbi.organism)
    
    await close_client()

if __name__ == '__main__':
    asyncio.run(main())
