from fastapi.testclient import TestClient
import time
from app.main import app
import app.core.redis_client as rc
from unittest.mock import AsyncMock

mock_redis = AsyncMock()
mock_redis.ping.return_value = True
mock_redis.get.return_value = None
rc._redis_client = mock_redis

def run_stress_test():
    with TestClient(app) as client:
        # Reduced to 25 items for faster demonstration (prevents NCBI IP-ban on free tier)
        terms = ["1CRN"] + [f"TEST_TARGET_{i}" for i in range(1, 25)]
        
        payload = {"terms": terms}
        headers = {"X-API-Key": "my_secure_api_key_123"}
        
        start_time = time.time()
        batch_resp = client.post("/api/aggregate/batch", json=payload, headers=headers)
        end_time = time.time()
        
        if batch_resp.status_code == 200:
            data = batch_resp.json()
            results = data.get('results', [])
            print(f"Time Taken: {end_time - start_time:.2f} seconds")
            print(f"Successfully processed: {len(results)} items out of {len(terms)}")
            print(f"\nSnippet of Result #1 (Real Data):")
            print(results[0])
            print(f"\nSnippet of Result #25 (Handled 404 gracefully):")
            print(results[-1])
        else:
            print("Error:", batch_resp.text)

if __name__ == "__main__":
    run_stress_test()
