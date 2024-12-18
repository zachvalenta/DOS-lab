import requests
import concurrent.futures
import time

def make_request():
    data = {
        'id': str(time.time()),
        'payload': 'x' * 1000000  # Large payload
    }
    try:
        response = requests.post(
            'http://localhost:5000/api/process',
            json=data,
            timeout=30
        )
        return response.status_code
    except requests.exceptions.RequestException as e:
        return str(e)

# Create 100 concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(make_request) for _ in range(100)]
    
    for future in concurrent.futures.as_completed(futures):
        print(f"Request completed with status: {future.result()}")
