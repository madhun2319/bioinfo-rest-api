from fastapi.testclient import TestClient
import json
from app.main import app
import app.core.redis_client as rc
from unittest.mock import AsyncMock

# Mock Redis so we don't need a live Redis server running locally for the health check
mock_redis = AsyncMock()
mock_redis.ping.return_value = True
mock_redis.get.return_value = None
rc._redis_client = mock_redis

def run_tests():
    with TestClient(app) as client:
        print("--- 1. Testing K8s Health Probe (/health) ---")
        health_resp = client.get("/health")
        print(f"Status Code: {health_resp.status_code}")
        print(json.dumps(health_resp.json(), indent=2))
        
        print("\n--- 2. Testing High-Throughput Batch Endpoint (/api/aggregate/batch) ---")
        # We will query 3 distinct entities that belong to different databases
        payload = {
            "terms": ["1CRN", "BRCA1", "P01308", "INVALID_TERM_123"]
        }
        headers = {"X-API-Key": "my_secure_api_key_123"}
        
        batch_resp = client.post("/api/aggregate/batch", json=payload, headers=headers)
        print(f"Status Code: {batch_resp.status_code}")
        
        if batch_resp.status_code == 200:
            data = batch_resp.json()
            print(f"Successfully processed: {len(data.get('results', []))} items")
            print(f"Failed terms: {data.get('failed_terms', [])}")
            
            # Print a snippet of the first successful result
            if data.get('results'):
                print("\nSnippet of first successful result:")
                print(json.dumps(data['results'][0], indent=2))
        else:
            print("Error:", batch_resp.text)

if __name__ == "__main__":
    run_tests()
