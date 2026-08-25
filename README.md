<div align="center">
  <img src="assets/banner.jpg" alt="Bioinformatics API Banner" width="100%">
  <br><br>
  
  [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
  [![GitHub Codespaces](https://img.shields.io/badge/Codespaces-Ready-24292e.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/features/codespaces)
  [![Build Status](https://img.shields.io/github/actions/workflow/status/madhun2319/bioinfo-rest-api/ci.yml?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/madhun2319/bioinfo-rest-api/actions)

  <h3 align="center">Next-Gen Bioinformatics REST API Wrapper</h3>
  <p align="center">
    A blazingly fast, federated API wrapper that seamlessly bridges the RCSB PDB Data API and NCBI E-utilities.
    <br />
    <a href="#-api-endpoints"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>

<hr>

## 🧬 Overview
Welcome to the **Bioinformatics REST API Wrapper**. Designed from the ground up to be resilient, memory-efficient, and developer-friendly. This API aggregates critical genomic and structural metadata into a single, federated endpoint. 

Whether you're building a massive bioinformatics dashboard or running quick CLI scripts, this API delivers clean, typed, and cached JSON instantly.

---

## ✨ Features
- 🚀 **Federated Search Engine:** Query both the **RCSB Protein Data Bank (PDB)** and **NCBI Gene** databases concurrently with a single HTTP request.
- 🧠 **Smart Caching:** Built-in asynchronous LRU caching (`async-lru`) ensuring lightning-fast subsequent queries and respecting upstream rate limits.
- 🛡️ **Resilient Connection Pooling:** A global singleton `httpx.AsyncClient` handles high-throughput requests without leaking connections or exhausting memory.
- 💻 **Zero-Config Environments:** Launch a fully configured IDE right in your browser via GitHub Codespaces with our built-in `.devcontainer`.

---

## 🚀 Quick Start (GitHub Codespaces)

The easiest way to experience this project is via GitHub Codespaces. No local setup required!

1. Click the **Code** button at the top of this repository.
2. Select the **Codespaces** tab.
3. Click **Create codespace on master**.

Your browser will instantly transform into a VS Code environment. The server will start, dependencies will install, and the Pytest suite will auto-configure.

### Run locally

```bash
# 1. Clone the repository
git clone https://github.com/madhun2319/bioinfo-rest-api.git
cd bioinfo-rest-api

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn app.main:app --reload
```
Navigate to `http://localhost:8000/docs` to view the beautiful interactive Swagger UI.

---

## 📡 API Endpoints

### 1. `GET /api/aggregate?term={query}`
The crown jewel of the API. Fetches federated data concurrently.
```json
{
  "query": "BRCA1",
  "pdb_result": null,
  "ncbi_result": {
    "gene_id": "672",
    "name": "BRCA1",
    "description": "BRCA1 DNA repair associated",
    "organism": "Homo sapiens"
  }
}
```

### 2. `GET /api/pdb/{pdb_id}`
Returns strictly-typed structural metadata for a specific Protein Data Bank ID.

### 3. `GET /api/ncbi/gene/{gene_id}`
Returns detailed gene summaries using the NCBI E-utilities `esearch` and `esummary` pipelines.

---

## 🧪 Testing & Architecture
This project boasts a **100% offline test suite**. Using `pytest-mock`, all network calls are seamlessly intercepted, ensuring tests run in milliseconds without hitting rate limits. 

Simply run:
```bash
pytest tests/
```

---

<div align="center">
  <sub>Built with ❤️ for the Bioinformatics Community.</sub>
</div>
