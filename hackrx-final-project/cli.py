# cli.py

import argparse
import json
import os
from document_processor import process_document_query

def main():
    parser = argparse.ArgumentParser(description="Process natural language queries against insurance policy documents.")
    parser.add_argument(
        "query",
        type=str,
        help="The natural language query to process (e.g., '46-year-old male, knee surgery in Pune, 3-month-old insurance policy')."
    )
    parser.add_argument(
        "--document", "-d",
        type=str,
        help="Path to the document or document identifier (e.g., 'HDFHLIP23024V072223')."
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        choices=["json", "text"],
        default="text",
        help="Output format (json or text)."
    )
    
    args = parser.parse_args()
    
    # Process the query
    result = process_document_query(args.query, args.document)
    
    # Format and display the output
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print("\n===== QUERY PROCESSING RESULT =====")
        print(f"Query: {args.query}")
        print(f"Document: {args.document or 'Not specified'}")
        print("\n----- DECISION -----")
        print(f"Decision: {result['decision']}")
        if result['amount'] is not None:
            print(f"Amount: {result['amount']}")
        print(f"\nJustification: {result['justification']}")
        
        print("\n----- RELEVANT CLAUSES -----")
        for clause in result['clauses']:
            print(f"\nClause {clause['clause_id']}:")
            print(f"Relevance Score: {clause.get('relevance_score', 'N/A')}")
            print(f"Text: {clause['text']}")

if __name__ == "__main__":
    main()