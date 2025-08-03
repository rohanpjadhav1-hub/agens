# API Testing with Python Requests

This document provides examples of how to test the HackRx API using Python's `requests` library.

## Prerequisites

- The API server is running (`python main.py`)
- You have set up your API key in the `.env` file
- You have installed the `requests` library (`pip install requests`)

## Testing the HackRx API

### Basic Query

```python
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("API_KEY")

# API endpoint
url = "http://localhost:8000/hackrx/run"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Request body
data = {
    "document_urls": ["https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"],
    "queries": ["What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"]
}

# Send request
response = requests.post(url, headers=headers, json=data)

# Print response
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=2))
```

### Multiple Queries

```python
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("API_KEY")

# API endpoint
url = "http://localhost:8000/hackrx/run"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Request body
data = {
    "document_urls": ["https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"],
    "queries": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?"
    ]
}

# Send request
response = requests.post(url, headers=headers, json=data)

# Print response
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=2))
```

### Using a Different Document URL

```python
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("API_KEY")

# API endpoint
url = "http://localhost:8000/hackrx/run"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Request body
data = {
    "document_urls": ["https://example.com/your-policy-document.pdf"],
    "queries": ["What is the grace period for premium payment?"]
}

# Send request
response = requests.post(url, headers=headers, json=data)

# Print response
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=2))
```

## Testing the Document Processor API

```python
import requests
import json

# API endpoint
url = "http://localhost:8000/process"

# Headers
headers = {
    "Content-Type": "application/json"
}

# Request body
data = {
    "query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
    "document_path": "docs/HDFHLIP23024V072223.pdf"
}

# Send request
response = requests.post(url, headers=headers, json=data)

# Print response
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=2))
```