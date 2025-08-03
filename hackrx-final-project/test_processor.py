# test_processor.py

import os
import json
from document_processor import process_document_query

def test_document_processor():
    """
    Test the document processor with a sample query.
    
    Before running this test, make sure:
    1. You have set the required API keys as environment variables
    2. You have indexed at least one document into the vector database
    """
    # Sample query
    query = "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
    
    # List of available document namespaces to test
    documents = [
        "HDFC_ERGO_Easy_Health",
        "Bajaj_Allianz_Global_Health",
        "ICICI_Lombard_Golden_Shield",
        "Cholamandalam_Travel",
        "Edelweiss_Well_Baby_Well_Mother"
    ]
    
    # Test with each document namespace
    for doc in documents:
        print(f"\n===== Testing with document: {doc} =====")
        try:
            # Process the query
            result = process_document_query(query, doc)
            
            # Print the result
            print(f"Decision: {result['decision']}")
            if result['amount'] is not None:
                print(f"Amount: {result['amount']}")
            print(f"Justification: {result['justification']}")
            
            print("\nRelevant Clauses:")
            for clause in result['clauses']:
                print(f"\nClause {clause['clause_id']}:")
                print(f"Relevance Score: {clause.get('relevance_score', 'N/A')}")
                print(f"Text: {clause['text']}")
        except Exception as e:
            print(f"Error processing query with document {doc}: {str(e)}")

def test_with_variations():
    """
    Test the document processor with variations of the same query to evaluate robustness.
    """
    # Sample document to test with
    document = "HDFC_ERGO_Easy_Health"
    
    # Query variations
    query_variations = [
        "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
        "46M, knee surgery, Pune, 3-month policy",
        "Male, 46, needs knee operation in Pune, policy is 3 months old",
        "Is knee surgery covered for a 46-year-old man in Pune with a 3-month policy?",
        "Coverage for knee procedure, 46M, Pune, policy age 3 months"
    ]
    
    print(f"\n===== Testing query variations with document: {document} =====")
    
    for i, query in enumerate(query_variations):
        print(f"\n----- Variation {i+1}: {query} -----")
        try:
            # Process the query
            result = process_document_query(query, document)
            
            # Print the result
            print(f"Decision: {result['decision']}")
            if result['amount'] is not None:
                print(f"Amount: {result['amount']}")
            print(f"Justification: {result['justification']}")
        except Exception as e:
            print(f"Error processing query: {str(e)}")

if __name__ == "__main__":
    # Check if API keys are set
    required_keys = ["GOOGLE_API_KEY", "PINECONE_API_KEY", "GROQ_API_KEY"]
    missing_keys = [key for key in required_keys if os.environ.get(key, "") in ["", "PASTE_YOUR_GOOGLE_API_KEY_HERE", "PASTE_YOUR_PINECONE_API_KEY_HERE", "PASTE_YOUR_GROQ_API_KEY_HERE"]]
    
    if missing_keys:
        print("Error: The following API keys are not set:")
        for key in missing_keys:
            print(f"  - {key}")
        print("\nPlease set these environment variables before running the tests.")
    else:
        print("===== Testing Document Processor =====")
        print("Note: This test assumes you have already indexed documents into the vector database.")
        
        # Run the tests
        test_document_processor()
        test_with_variations()