# ponytail: simplified FastAPI bootstrap with API‑key auth and rate limiting

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse

from app.routers import pdb, ncbi, aggregate, uniprot

# ------------------------------------------------------------------
# 1️⃣ Configuration – replace hard‑coded keys with vault‑stored secrets in production
# ------------------------------------------------------------------
VALID_API_KEYS = {
    "demo-key-123": "internal-team",
    # add more keys as needed
}
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(key: str = Depends(api_key_header)):
    if key in VALID_API_KEYS:
        return VALID_API_KEYS[key]
    raise HTTPException(status_code=403, detail="Invalid API Key")

# ------------------------------------------------------------------
# 2️⃣ Rate limiter – 100 requests per minute per IP (adjust as needed)
# ------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def rate_limit_exceeded(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

# ------------------------------------------------------------------
# 3️⃣ FastAPI app definition
# ------------------------------------------------------------------
app = FastAPI(title="BioInfo REST API", dependencies=[Depends(get_api_key)])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ponytail: permissive CORS for dev; replace in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# 4️⃣ Register routers
# ------------------------------------------------------------------
app.include_router(pdb.router, prefix="/api/pdb", tags=["PDB"])
app.include_router(ncbi.router, prefix="/api/ncbi", tags=["NCBI"])
app.include_router(uniprot.router, prefix="/api/uniprot", tags=["UniProt"])
app.include_router(aggregate.router, prefix="/api", tags=["Aggregate"])
