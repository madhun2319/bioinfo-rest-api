import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def mock_redis(mocker):
    import app.core.redis_client as rc
    mock = mocker.AsyncMock()
    mock.get.return_value = None
    rc._redis_client = mock
    yield
    rc._redis_client = None

@pytest.fixture(autouse=True)
def clear_caches():
    pass
