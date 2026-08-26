import asyncio
from app.services.ncbi_service import fetch_gene_summary
from app.core.http_client import _client
from app.core.redis_client import _redis_client
import httpx
from unittest.mock import AsyncMock
import app.core.http_client as hc
import app.core.redis_client as rc

async def debug_ncbi():
    hc._client = httpx.AsyncClient()
    rc._redis_client = AsyncMock()
    rc._redis_client.get.return_value = None
    
    try:
        res = await fetch_gene_summary("BRCA1")
        print("RESULT:", res)
    except Exception as e:
        print("ERROR:", e)
    finally:
        await hc._client.aclose()

if __name__ == "__main__":
    asyncio.run(debug_ncbi())
