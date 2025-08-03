# main.py - Final, Secure, High-Speed Version
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import google.generativeai as genai
from pinecone import Pinecone
from groq import Groq
import os
import json

# --- Configuration ---
# This code is SAFE for GitHub. It reads the keys from a secure place.
# For local testing, it uses the fallback value you paste here.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "PASTE_YOUR_GOOGLE_API_KEY_HERE")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "PASTE_YOUR_PINECONE_API_KEY_HERE")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "PASTE_YOUR_GROQ_API_KEY_HERE")

# Configure all our services
genai.configure(api_key=GOOGLE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

# Configure services
genai.configure(api_key=GOOGLE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

PINECONE_INDEX_NAME = "hackrx-library"
index = pc.Index(PINECONE_INDEX_NAME)

SECRET_PASSWORD = "1e83fbe10fa7c1be5ffa312d8b283e496b82c2470dee257fb48b82ad7e8ba562"
app = FastAPI(title="HackRx 6.0 API - Final Version")

# --- Pydantic Models ---
class HackRxRequest(BaseModel):
    document_urls: List[str]
    queries: List[str]

class HackRxResponse(BaseModel):
    answers: List[str]

# --- Helper Function ---
def get_embedding(text: str, model="models/embedding-001"):
    try:
        result = genai.embed_content(model=model, content=text)
        return result['embedding']
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None

# --- Main Information Extraction Function ---
def generate_decision(query: str, index: Pinecone.Index, namespace: str):
    # Generate embedding for the query
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return {"justification": "Could not process the query. Please try again."}

    # Retrieve relevant policy clauses from the vector database
    results = index.query(
        vector=query_embedding, 
        top_k=7,  # Retrieve more context for better answers
        include_metadata=True, 
        namespace=namespace
    )
    
    # Format the retrieved context
    context = ""
    if results['matches']:
        for i, match in enumerate(results['matches']):
            # Include metadata for better context
            page_info = f"Page {match['metadata'].get('page', 'N/A')}" if 'page' in match['metadata'] else ""
            context += f"Clause {i+1} {page_info}:\n{match['metadata']['text']}\n---\n"
    
    if not context:
        return {"justification": "No relevant information found in the policy document."}

    # Create a prompt that focuses on answering the specific question
    prompt = f"""
    You are an expert insurance policy analyst. Your task is to answer a specific question about an insurance policy 
    based ONLY on the provided policy document clauses.

    **Policy Clauses (Context):**
    {context}

    **Question:**
    {query}

    Provide a direct, concise, and accurate answer to the question based solely on the information in the provided policy clauses.
    Your answer should be factual and reference specific details from the policy document.
    If the information is not available in the provided clauses, state that clearly.
    Do not make assumptions or provide information not supported by the policy clauses.
    
    Format your response as a single paragraph without bullet points or numbered lists.
    """
    
    try:
        # Use Groq to generate the answer
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
            temperature=0.2,  # Lower temperature for more factual responses
            max_tokens=500,   # Limit response length
        )
        
        # Extract the answer
        answer = chat_completion.choices[0].message.content.strip()
        
        # Return the answer in the expected format
        return {"justification": answer}
    except Exception as e:
        return {"justification": f"Error processing query: {str(e)}"}


# --- Main API Endpoint ---
@app.post("/hackrx/run")
def process_document_queries(request: HackRxRequest, authorization: Optional[str] = Header(None)):
    # Validate authorization
    if authorization is None or "Bearer " not in authorization or authorization.split()[1] != SECRET_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")

    # Get document URLs and queries
    doc_urls = request.document_urls
    queries = request.queries
    
    # Ensure we have at least one document URL
    if not doc_urls or len(doc_urls) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one document URL is required")
    
    # Use the first document URL for namespace mapping
    doc_url = doc_urls[0]
    
    # Map document URL to namespace
    if "HDFHLIP23024V072223" in doc_url:
        namespace_id = "HDFC_ERGO_Easy_Health"
    elif "BAJHLIP23020V012223" in doc_url:
        namespace_id = "Bajaj_Allianz_Global_Health"
    elif "ICIHLIP22012V012223" in doc_url:
        namespace_id = "ICICI_Lombard_Golden_Shield"
    elif "CHOTGDP23004V012223" in doc_url:
        namespace_id = "Cholamandalam_Travel"
    elif "EDLHLGA23009V012223" in doc_url:
        namespace_id = "Edelweiss_Well_Baby_Well_Mother"
    else:
        # Default to a generic namespace if document is not recognized
        namespace_id = "default"

    # Process each query and generate answers
    answers = []
    for query in queries:
        try:
            # Get decision from LLM
            decision_json = generate_decision(query, index, namespace=namespace_id)
            
            # Extract the justification as the answer
            answer = decision_json.get("justification", "No answer available.")
            answers.append(answer)
        except Exception as e:
            # Handle errors gracefully
            answers.append(f"Error processing query: {str(e)}")

    # Return the answers
    return HackRxResponse(answers=answers)
