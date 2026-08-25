import httpx
from typing import Optional

_client: Optional[httpx.AsyncClient] = None


def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=10.0)
    return _client


async def close_client():
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
