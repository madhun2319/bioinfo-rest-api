from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse

from app.core.config import settings
from app.routers import pdb, ncbi, aggregate, uniprot
from app.core.http_client import get_client, close_client
from app.core.redis_client import get_redis, close_redis

# ------------------------------------------------------------------
# OpenAPI Documentation Metadata
# ------------------------------------------------------------------
tags_metadata = [
    {
        "name": "Aggregate",
        "description": "Federated endpoints that combine data from multiple biological databases in a single request.",
    },
    {
        "name": "NCBI",
        "description": "Direct endpoints for the National Center for Biotechnology Information.",
    },
    {
        "name": "PDB",
        "description": "Direct endpoints for the Protein Data Bank.",
    },
    {
        "name": "UniProt",
        "description": "Direct endpoints for the Universal Protein Resource.",
    },
    {
        "name": "System",
        "description": "Enterprise health and readiness probes.",
    },
]

# ------------------------------------------------------------------
# 1️⃣ Configuration
# ------------------------------------------------------------------
from app.core.auth import get_api_key

# ------------------------------------------------------------------
# 2️⃣ Rate limiter – 100 requests per minute per IP
# ------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def rate_limit_exceeded(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

# ------------------------------------------------------------------
# 3️⃣ Lifespan Events (Resource Management)
# ------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the global HTTP client pool and Redis
    get_client()
    get_redis()
    yield
    # Cleanup on shutdown
    await close_client()
    await close_redis()

# ------------------------------------------------------------------
# 4️⃣ FastAPI app definition
# ------------------------------------------------------------------
description = """
**BioInfo REST API** provides federated, high-throughput access to biological databases.

### Core Features
* 🚀 **Federated Search:** Query NCBI, UniProt, and PDB simultaneously.
* ⚡ **High Throughput:** Use `/api/aggregate/batch` for concurrent batch processing.
* 🔒 **Secure:** Rate-limited and protected via `X-API-Key`.
"""

app = FastAPI(
    title="BioInfo REST API",
    description=description,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "BioInfo API Support",
        "url": "https://github.com/madhun2319/bioinfo-rest-api",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
    dependencies=[Depends(get_api_key)], 
    lifespan=lifespan
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Use secure origins from config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# 5️⃣ Register routers
# ------------------------------------------------------------------
app.include_router(pdb.router, prefix="/api/pdb", tags=["PDB"])
app.include_router(ncbi.router, prefix="/api/ncbi", tags=["NCBI"])
app.include_router(uniprot.router, prefix="/api/uniprot", tags=["UniProt"])
app.include_router(aggregate.router, prefix="/api", tags=["Aggregate"])

# ------------------------------------------------------------------
# 6️⃣ Enterprise Health & Readiness Probes
# ------------------------------------------------------------------
@app.get("/health", tags=["System"])
async def health_check():
    """Kubernetes Readiness Probe. Checks if application and Redis are up."""
    redis_status = "down"
    try:
        redis_client = get_redis()
        if await redis_client.ping():
            redis_status = "up"
    except Exception:
        pass

    return {
        "status": "healthy" if redis_status == "up" else "degraded",
        "redis": redis_status,
        "version": "1.0.0"
    }
