# document_processor.py

from typing import List, Dict, Any, Optional
import re
import json
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import google.generativeai as genai
from pinecone import Pinecone
from groq import Groq
import os
from pypdf import PdfReader

# --- Configuration ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "PASTE_YOUR_GOOGLE_API_KEY_HERE")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "PASTE_YOUR_PINECONE_API_KEY_HERE")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "PASTE_YOUR_GROQ_API_KEY_HERE")

# Configure services
genai.configure(api_key=GOOGLE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

PINECONE_INDEX_NAME = "hackrx-library"
index = pc.Index(PINECONE_INDEX_NAME)

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    query: str
    document_path: Optional[str] = None

class QueryResponse(BaseModel):
    decision: str
    amount: Optional[float] = None
    justification: str
    clauses: List[Dict[str, Any]]

# --- Helper Functions ---
def get_embedding(text: str, model="models/embedding-001"):
    """Generate embeddings for the given text using Google's embedding model."""
    try:
        result = genai.embed_content(model=model, content=text)
        return result['embedding']
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None

def extract_pdf_text(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract text from a PDF file and split it into chunks."""
    try:
        reader = PdfReader(pdf_path)
        chunks = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                # Split text into smaller chunks (paragraphs or sections)
                paragraphs = re.split(r'\n\s*\n', text)
                for j, paragraph in enumerate(paragraphs):
                    if paragraph.strip():
                        chunks.append({
                            "text": paragraph.strip(),
                            "metadata": {
                                "page": i + 1,
                                "chunk": j + 1,
                                "source": pdf_path
                            }
                        })
        return chunks
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return []

def parse_query(query: str) -> Dict[str, Any]:
    """Parse the natural language query to extract structured information."""
    prompt = f"""
    You are an expert insurance query parser. Extract structured information from the following query:
    
    Query: {query}
    
    Extract the following information (if available):
    1. Age and gender of the person
    2. Medical procedure or condition
    3. Location
    4. Policy duration or age
    5. Any other relevant details
    
    Return ONLY a valid JSON object with these fields (use null for missing information).
    """
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
            response_format={"type": "json_object"},
        )
        parsed_data = json.loads(chat_completion.choices[0].message.content)
        return parsed_data
    except Exception as e:
        print(f"Error parsing query: {e}")
        return {
            "age": None,
            "gender": None,
            "procedure": None,
            "location": None,
            "policy_duration": None,
            "other_details": None
        }

def retrieve_relevant_clauses(structured_query: Dict[str, Any], namespace: str) -> List[Dict[str, Any]]:
    """Retrieve relevant clauses from the vector database based on the structured query."""
    # Create a more specific search query based on the structured information
    search_query = ""
    if structured_query.get("procedure"):
        search_query += f"Coverage for {structured_query['procedure']} "
    if structured_query.get("age"):
        search_query += f"for a {structured_query['age']} year old "
    if structured_query.get("gender"):
        search_query += f"{structured_query['gender']} "
    if structured_query.get("location"):
        search_query += f"in {structured_query['location']} "
    if structured_query.get("policy_duration"):
        search_query += f"with a {structured_query['policy_duration']} policy "
    
    # If we couldn't extract structured information, use the original query
    if not search_query.strip():
        search_query = "insurance coverage policy details"
    
    # Get embedding for the search query
    query_embedding = get_embedding(search_query)
    if query_embedding is None:
        return []
    
    # Retrieve relevant clauses from the vector database
    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True,
        namespace=namespace
    )
    
    relevant_clauses = []
    if results['matches']:
        for i, match in enumerate(results['matches']):
            relevant_clauses.append({
                "clause_id": i + 1,
                "text": match['metadata']['text'],
                "relevance_score": match['score'],
                "metadata": match['metadata']
            })
    
    return relevant_clauses

def generate_decision(query: str, structured_query: Dict[str, Any], relevant_clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a decision based on the query and relevant clauses."""
    if not relevant_clauses:
        return {
            "decision": "Insufficient Information",
            "amount": None,
            "justification": "Could not find relevant policy clauses to make a determination.",
            "clauses": []
        }
    
    # Format the clauses for the prompt
    clauses_text = ""
    for clause in relevant_clauses:
        clauses_text += f"Clause {clause['clause_id']}:\n{clause['text']}\n---\n"
    
    # Create a detailed prompt for the decision generation
    prompt = f"""
    You are an expert insurance claims processor. Your task is to evaluate a claim based ONLY on the provided policy document clauses.
    
    **Query Details:**
    - Original Query: {query}
    - Age: {structured_query.get('age', 'Not specified')}
    - Gender: {structured_query.get('gender', 'Not specified')}
    - Procedure/Condition: {structured_query.get('procedure', 'Not specified')}
    - Location: {structured_query.get('location', 'Not specified')}
    - Policy Duration: {structured_query.get('policy_duration', 'Not specified')}
    - Other Details: {structured_query.get('other_details', 'None')}
    
    **Policy Clauses:**
    {clauses_text}
    
    Based strictly on the query details and the policy clauses, provide a decision. Your response MUST be a single, valid JSON object with these keys:
    1. "decision": Either "Approved", "Rejected", or "Needs More Information"
    2. "amount": The coverage amount if applicable (null if not applicable)
    3. "justification": A clear explanation of your decision, referencing specific clauses
    4. "clause_references": An array of clause IDs that support your decision
    
    Be specific and precise in your justification, citing the exact clauses that led to your decision.
    """
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
            response_format={"type": "json_object"},
        )
        decision_data = json.loads(chat_completion.choices[0].message.content)
        
        # Format the response
        referenced_clauses = []
        if "clause_references" in decision_data:
            for clause_id in decision_data["clause_references"]:
                for clause in relevant_clauses:
                    if clause["clause_id"] == clause_id:
                        referenced_clauses.append(clause)
                        break
        
        return {
            "decision": decision_data.get("decision", "Undetermined"),
            "amount": decision_data.get("amount"),
            "justification": decision_data.get("justification", "No justification provided."),
            "clauses": referenced_clauses or relevant_clauses
        }
    except Exception as e:
        print(f"Error generating decision: {e}")
        return {
            "decision": "Error",
            "amount": None,
            "justification": f"An error occurred while processing the decision: {str(e)}",
            "clauses": relevant_clauses
        }

# --- Main Processing Function ---
def process_document_query(query: str, document_path: Optional[str] = None) -> Dict[str, Any]:
    """Process a natural language query against document(s) and return a structured response."""
    # Step 1: Parse the query to extract structured information
    structured_query = parse_query(query)
    
    # Step 2: Determine the namespace based on the document path
    namespace = "default"
    if document_path:
        if "HDFHLIP23024V072223" in document_path:
            namespace = "HDFC_ERGO_Easy_Health"
        elif "BAJHLIP23020V012223" in document_path:
            namespace = "Bajaj_Allianz_Global_Health"
        elif "ICIHLIP22012V012223" in document_path:
            namespace = "ICICI_Lombard_Golden_Shield"
        elif "CHOTGDP23004V012223" in document_path:
            namespace = "Cholamandalam_Travel"
        elif "EDLHLGA23009V012223" in document_path:
            namespace = "Edelweiss_Well_Baby_Well_Mother"
    
    # Step 3: Retrieve relevant clauses from the vector database
    relevant_clauses = retrieve_relevant_clauses(structured_query, namespace)
    
    # Step 4: Generate a decision based on the query and relevant clauses
    decision = generate_decision(query, structured_query, relevant_clauses)
    
    return decision

# --- API Endpoint ---
app = FastAPI(title="Document Processing API")

@app.post("/process", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a natural language query against document(s) and return a structured response."""
    try:
        result = process_document_query(request.query, request.document_path)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the query: {str(e)}"
        )

# For direct script execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)