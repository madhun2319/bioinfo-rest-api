from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers (unchanged)
from app.routers import pdb, ncbi, aggregate, uniprot

app = FastAPI(title="BioInfo REST API")  # ponytail: minimal config

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ponytail: dev permissive CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdb.router, prefix="/api/pdb", tags=["PDB"])
app.include_router(ncbi.router, prefix="/api/ncbi", tags=["NCBI"])
app.include_router(uniprot.router, prefix="/api/uniprot", tags=["UniProt"])
app.include_router(aggregate.router, prefix="/api", tags=["Aggregate"])
