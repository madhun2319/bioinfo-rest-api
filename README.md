<div align="center">
  <img src="assets/banner.jpg" alt="Bioinformatics API Banner" width="100%">
  <br><br>
  
  [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
  [![GitHub Codespaces](https://img.shields.io/badge/Codespaces-Ready-24292e.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/features/codespaces)
  [![Build Status](https://img.shields.io/github/actions/workflow/status/madhun2319/bioinfo-rest-api/ci.yml?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/madhun2319/bioinfo-rest-api/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

  <h3 align="center">Next-Gen Bioinformatics REST API Wrapper</h3>
  <p align="center">
    A blazingly fast, federated API wrapper that seamlessly bridges the RCSB PDB Data API and NCBI E-utilities.
    <br />
    <a href="#-api-endpoints"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>

<hr>
## 🤝 Get Involved

We’re proud to open‑source this API under the MIT license. You’re welcome to:

- ⭐ Star the repo
- 🐛 Report bugs or request features via GitHub Issues
- 🔀 Submit pull requests (see **CONTRIBUTING.md**)
- 📚 Share use‑cases with the community

Check out the **README** badges for our license, build status, and package version.

## 📦 Docker Image

A pre‑built Docker image is available on Docker Hub. Pull it with:

```bash
docker pull ghcr.io/madhun2319/bioinfo-rest-api:latest
```

Run the container:

```bash
docker run -p 8000:8000 ghcr.io/madhun2319/bioinfo-rest-api:latest
```

The API will be reachable at `http://localhost:8000`.

## 📚 Why Open‑Source?

We open‑source this API under the MIT license to encourage community innovation and rapid adoption in biotech research. The core service remains free to use, while we offer **SaaS hosting**, **premium support**, and **enterprise add‑ons** (e.g., SSO, custom rate limits, on‑prem deployment) for organizations that need guaranteed uptime, compliance, and dedicated assistance. By building a vibrant contributor ecosystem we continuously improve the API, and our commercial services fund further development.

## 💬 GitHub Discussions

Join the conversation, ask questions, and propose new features in the **[GitHub Discussions](https://github.com/madhun2319/bioinfo-rest-api/discussions)** forum.


## 🧬 Overview
Welcome to the **BioInfo Nexus REST API & Dashboard**. Designed from the ground up to be resilient, enterprise-grade, and developer-friendly. This API aggregates critical genomic, structural, and proteomic metadata into a single, federated platform. 

Whether you're building a massive bioinformatics dashboard or running quick CLI scripts, this API delivers clean, typed, and cached JSON instantly.

---

## ✨ Enterprise Features
- 🚀 **Federated Search Engine:** Query the **RCSB PDB**, **NCBI Gene**, and **UniProtKB** databases concurrently with a single HTTP request.
- 🧠 **Resilient Redis Caching:** Built-in asynchronous Redis caching with graceful fallback degradation. If the cache goes down, the API stays up.
- 📊 **React Frontend Dashboard:** Includes a beautiful, glass-morphism Vite/React UI that visually renders the federated data in a dynamic 3-card grid.
- 🏎️ **Batch Processing & Semaphores:** Need 100 results? The `/api/aggregate/batch` endpoint safely throttles concurrent external HTTP requests to prevent IP bans.
- 🛡️ **Fail-Secure Authentication:** Native API-key security (`X-API-Key`) that fails securely in production if misconfigured.
- 🐳 **Multi-Core Dockerization:** Pre-configured Docker images leveraging Gunicorn/Uvicorn workers for high-concurrency cloud scaling.

---

## 🚀 Quick Start (Local & Frontend)

### 1. Start the API (Backend)
```bash
# Clone the repository
git clone https://github.com/madhun2319/bioinfo-rest-api.git
cd bioinfo-rest-api

# Install dependencies and start the multi-core server
pip install -r requirements.txt
uvicorn app.main:app --port 8000 --reload
```
Navigate to `http://localhost:8000/docs` to view the Swagger UI.

### 2. Start the Dashboard (Frontend)
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:5173` to view the BioInfo Nexus dashboard!

---

## 📡 Core Endpoints

### 1. `GET /api/aggregate?term={query}`
The crown jewel of the API. Fetches federated data from PDB, NCBI, and UniProt concurrently.
```json
{
  "query": "BRCA1",
  "pdb_result": { "status": "not_found", "data": null },
  "ncbi_result": { "status": "success", "data": { "gene_id": "147881884", "name": "LOC147881884" } },
  "uniprot_result": { "status": "success", "data": { "primary_accession": "P38398", "protein_name": "Breast cancer type 1 susceptibility protein" } }
}
```

### 2. `POST /api/aggregate/batch`
Submit a list of terms and fetch them concurrently using built-in semaphore rate-limiting.

### 3. Individual Microservices
- `GET /api/pdb/{pdb_id}` - Structural metadata
- `GET /api/ncbi/gene/{gene_id}` - Genetic metadata
- `GET /api/uniprot/{accession}` - Proteomic metadata

---

## 🧪 Testing & CI/CD
This project boasts an **80%+ coverage** test suite. Using `pytest-mock`, all network calls are seamlessly intercepted.
```bash
pytest --cov=app
```
Our GitHub Actions pipeline automatically enforces test coverage and builds our `ghcr.io` Docker images.

---

<div align="center">
  <sub>Built with ❤️ for the Bioinformatics Community.</sub>
</div>
