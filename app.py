from flask import Flask, request, Response
import time
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
# Creating a thread pool with no limit - first vulnerability
executor = ThreadPoolExecutor()

# In-memory storage without limits - second vulnerability
cache = {}

@app.route('/')
def root():
    return Response("at the index", 200)

@app.route('/api/process', methods=['POST'])
def process_data():
    """
    This endpoint demonstrates multiple ways to accidentally DOS your own server:
    1. No input size validation
    2. Unbounded in-memory storage
    3. Computationally expensive operation without timeouts
    4. Unlimited concurrent processing
    """
    # Accepting arbitrary-sized input without validation
    data = request.get_json()
    
    if not data or 'id' not in data:
        return {'error': 'Invalid input'}, 400
    
    # Storing in cache without size limits or eviction
    cache[data['id']] = data
    
    def expensive_operation():
        # Simulating CPU-intensive work without timeout
        time.sleep(10)  # Blocking operation
        return {'processed': True}
    
    # Spawning new thread for each request without limits
    future = executor.submit(expensive_operation)
    
    try:
        # No timeout on result retrieval
        result = future.result()
        return result
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/memory_leak', methods=['POST'])
def memory_leak():
    """
    This endpoint demonstrates memory exhaustion through unbounded data storage
    """
    # Accepting large files without size validation
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400
        
    file = request.files['file']
    
    # Reading entire file into memory without size checks
    content = file.read()
    
    # Storing in memory without limits
    cache[file.filename] = content
    
    return {'status': 'stored'}, 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True)  # Running in threaded mode compounds the issues
