import httpx
import json

headers = {'X-API-Key': 'my_secure_api_key_123'}
try:
    response = httpx.get('http://localhost:8000/api/aggregate?term=KRAS', headers=headers, timeout=10.0)
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print('Error:', e)
