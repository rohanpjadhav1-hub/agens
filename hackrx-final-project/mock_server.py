# mock_server.py

from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
SECRET_PASSWORD = os.environ.get("API_KEY", "1e83fbe10fa7c1be5ffa312d8b283e496b82c2470dee257fb48b82ad7e8ba562")

# Create FastAPI app
app = FastAPI(title="HackRx 6.0 API - Mock Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# --- Pydantic Models ---
class HackRxRequest(BaseModel):
    document_urls: List[str]
    queries: List[str]

class HackRxResponse(BaseModel):
    answers: List[str]

# --- Mock Data ---
mock_answers = {
    "What is the grace period for premium payment?": 
        "The grace period for premium payment under the National Parivar Mediclaim Plus Policy is 30 days from the due date.",
    
    "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?": 
        "The grace period for premium payment under the National Parivar Mediclaim Plus Policy is 30 days from the due date.",
    
    "What is the waiting period for pre-existing diseases?":
        "The waiting period for pre-existing diseases (PED) to be covered is 48 months (4 years) from the date of inception of the policy.",
        
    "What is the waiting period for pre-existing diseases (PED) to be covered?":
        "The waiting period for pre-existing diseases (PED) to be covered is 48 months (4 years) from the date of inception of the policy.",
    
    "Does this policy cover maternity expenses, and what are the conditions?":
        "Yes, the policy covers maternity expenses after a waiting period of 9 months. The coverage includes pre and post-natal expenses up to the sum insured, with a sub-limit of Rs. 50,000 for normal delivery and Rs. 75,000 for cesarean section.",
    
    "What is the waiting period for cataract surgery?":
        "The waiting period for cataract surgery under this policy is 24 months (2 years) from the date of inception of the policy.",
    
    "Are the medical expenses for an organ donor covered under this policy?":
        "Yes, medical expenses for an organ donor are covered under this policy. This includes pre-hospitalization, surgery, and post-hospitalization expenses for the donor, subject to the availability of the overall sum insured of the insured person.",
    
    "What is the No Claim Discount (NCD) offered in this policy?":
        "The policy offers a No Claim Discount (NCD) of 5% on the premium for each claim-free year, up to a maximum of 15% if no claims are made for three consecutive years.",
    
    "Is there a benefit for preventive health check-ups?":
        "Yes, the policy provides a benefit for preventive health check-ups. After every four claim-free policy years, the insured is entitled to a free health check-up at designated network hospitals, up to 1% of the sum insured.",
    
    "How does the policy define a 'Hospital'?":
        "The policy defines a 'Hospital' as an institution established for in-patient care and day care treatment of illness and/or injuries and which has been registered as a hospital with the local authorities. It must have at least 10 in-patient beds in towns with a population less than 10 lakhs and 15 in-patient beds in all other places, with qualified medical practitioners and nursing staff available round the clock.",
    
    "What is the extent of coverage for AYUSH treatments?":
        "AYUSH treatments (Ayurveda, Yoga and Naturopathy, Unani, Siddha, and Homeopathy) are covered up to 25% of the sum insured per policy year. The treatment must be taken at a government hospital or an institute recognized by the government and/or accredited by Quality Council of India or National Accreditation Board for Health.",
    
    "Are there any sub-limits on room rent and ICU charges for Plan A?":
        "Yes, there are sub-limits on room rent and ICU charges for Plan A. Room rent is limited to 2% of the sum insured per day, and ICU charges are limited to 4% of the sum insured per day."
}

# --- Default answer for unknown questions ---
default_answer = "Based on the provided policy document, I cannot find specific information to answer this question accurately. Please refer to the complete policy document or contact the insurance provider for more details."

# --- API Endpoint ---
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
    
    # Process each query and generate answers
    answers = []
    for query in queries:
        # Get answer from mock data or use default answer
        answer = mock_answers.get(query, default_answer)
        answers.append(answer)

    # Return the answers
    return HackRxResponse(answers=answers)

# --- Run the server ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)