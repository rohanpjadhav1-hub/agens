# test_api.py

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
API_URL = "http://localhost:8000/hackrx/run"
API_KEY = os.environ.get("API_KEY", "1e83fbe10fa7c1be5ffa312d8b283e496b82c2470dee257fb48b82ad7e8ba562")

# Sample questions from the problem statement
sample_questions = [
    "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
    "What is the waiting period for pre-existing diseases (PED) to be covered?",
    "Does this policy cover maternity expenses, and what are the conditions?",
    "What is the waiting period for cataract surgery?",
    "Are the medical expenses for an organ donor covered under this policy?",
    "What is the No Claim Discount (NCD) offered in this policy?",
    "Is there a benefit for preventive health check-ups?",
    "How does the policy define a 'Hospital'?",
    "What is the extent of coverage for AYUSH treatments?",
    "Are there any sub-limits on room rent and ICU charges for Plan A?"
]

# Sample document URL from the problem statement
sample_document_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"

def test_api():
    """Test the API with the sample questions and document URL."""
    # Prepare the request payload
    payload = {
        "document_urls": [sample_document_url],
        "queries": sample_questions
    }
    
    # Set the headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print("Sending request to API...")
    try:
        # Send the request
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            # Parse the response
            response_data = response.json()
            
            # Print the answers
            print("\nAnswers:")
            for i, answer in enumerate(response_data.get("answers", [])):
                print(f"\nQuestion {i+1}: {sample_questions[i]}")
                print(f"Answer: {answer}")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_with_specific_document(document_url, questions=None):
    """Test the API with a specific document URL and questions."""
    if questions is None:
        questions = sample_questions[:2]  # Use first two sample questions by default
    
    # Prepare the request payload
    payload = {
        "document_urls": [document_url],
        "queries": questions
    }
    
    # Set the headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print(f"Testing with document: {document_url}")
    print(f"Number of questions: {len(questions)}")
    
    try:
        # Send the request
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            # Parse the response
            response_data = response.json()
            
            # Print the answers
            print("\nAnswers:")
            for i, answer in enumerate(response_data.get("answers", [])):
                print(f"\nQuestion {i+1}: {questions[i]}")
                print(f"Answer: {answer}")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the HackRx API with sample or custom queries.")
    parser.add_argument(
        "--document", "-d",
        type=str,
        default=sample_document_url,
        help="Document URL to query (default: sample document URL)."
    )
    parser.add_argument(
        "--questions", "-q",
        type=str,
        help="Comma-separated list of questions to ask (default: first two sample questions)."
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Use all sample questions (overrides --questions)."
    )
    
    args = parser.parse_args()
    
    if args.all:
        # Test with all sample questions
        test_with_specific_document(args.document, sample_questions)
    elif args.questions:
        # Test with custom questions
        custom_questions = [q.strip() for q in args.questions.split(",")]
        test_with_specific_document(args.document, custom_questions)
    else:
        # Test with default (first two sample questions)
        test_with_specific_document(args.document)