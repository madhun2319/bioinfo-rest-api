import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
def clear_caches():
    from app.services.pdb_service import fetch_pdb_metadata
    from app.services.ncbi_service import fetch_gene_summary
    fetch_pdb_metadata.cache_clear()
    fetch_gene_summary.cache_clear()
