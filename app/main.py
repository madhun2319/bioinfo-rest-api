from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import pdb, ncbi, aggregate
from app.core.http_client import get_client, close_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the global HTTP client pool
    get_client()
    yield
    # Cleanup on shutdown
    await close_client()

app = FastAPI(title="BioInfo REST API", lifespan=lifespan)

app.include_router(pdb.router, prefix="/api/pdb", tags=["PDB"])
app.include_router(ncbi.router, prefix="/api/ncbi", tags=["NCBI"])
app.include_router(aggregate.router, prefix="/api", tags=["Aggregate"])
