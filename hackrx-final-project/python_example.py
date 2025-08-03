# python_example.py

import requests
import json

# API endpoint
# For local testing, use http://localhost:8000/hackrx/run
# For deployed version, use your Render URL (e.g., https://hackrx-api.onrender.com/hackrx/run)
API_URL = "http://localhost:8000/hackrx/run"  # Change this to your deployed URL when needed

# API key (replace with your actual API key)
API_KEY = "1e83fbe10fa7c1be5ffa312d8b283e496b82c2470dee257fb48b82ad7e8ba562"

# Document URL
DOCUMENT_URL = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"

# List of questions
QUESTIONS = [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?",
    "Does this policy cover maternity expenses, and what are the conditions?",
    "What is the waiting period for cataract surgery?",
    "Are the medical expenses for an organ donor covered under this policy?"
]

def query_api():
    # Prepare request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Prepare request payload
    payload = {
        "document_urls": [DOCUMENT_URL],
        "queries": QUESTIONS
    }
    
    # Send POST request to API
    try:
        print("Sending request to API...")
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            
            # Print formatted results
            print("\nAPI Response:")
            print(json.dumps(data, indent=2))
            
            # Print questions and answers in a more readable format
            print("\nQuestions and Answers:")
            for i, (question, answer) in enumerate(zip(QUESTIONS, data["answers"]), 1):
                print(f"\nQ{i}: {question}")
                print(f"A{i}: {answer}")
                
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    query_api()