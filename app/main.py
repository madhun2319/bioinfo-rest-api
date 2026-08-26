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
app = FastAPI(title="BioInfo REST API", dependencies=[Depends(get_api_key)], lifespan=lifespan)
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
