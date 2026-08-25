from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import pdb, ncbi, aggregate
from app.core.http_client import get_client, close_client
from app.core.redis_client import get_redis, close_redis
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the global HTTP client pool and Redis
    get_client()
    get_redis()
    yield
    # Cleanup on shutdown
    await close_client()
    await close_redis()


app = FastAPI(title="BioInfo REST API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(pdb.router, prefix="/api/pdb", tags=["PDB"])
app.include_router(ncbi.router, prefix="/api/ncbi", tags=["NCBI"])
app.include_router(aggregate.router, prefix="/api", tags=["Aggregate"])
