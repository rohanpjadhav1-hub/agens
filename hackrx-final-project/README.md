# LLM Document Processing System

This project is an AI-powered system that uses Large Language Models (LLMs) to process natural language queries and retrieve relevant information from large unstructured documents such as policy documents, contracts, and emails.

## 🤖 How It Works

The system uses a Retrieval-Augmented Generation (RAG) architecture:
1. It parses and structures natural language queries to identify key details such as age, procedure, location, and policy duration.
2. It searches and retrieves relevant clauses or rules from the provided documents using semantic understanding rather than simple keyword matching.
3. It evaluates the retrieved information to determine the correct decision, such as approval status or payout amount, based on the logic defined in the clauses.
4. It returns a structured response containing: Decision (e.g., approved or rejected), Amount (if applicable), and Justification, including mapping of each decision to the specific clause(s) it was based on.

## 🚀 Components

### Document Processor

The main component of the system is the document processor, which handles the entire pipeline from query parsing to decision generation.

```python
from document_processor import process_document_query

# Process a query
result = process_document_query(
    query="46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
    document_path="docs/HDFHLIP23024V072223.pdf"
)

print(result)
```

### Command-Line Interface

The system includes a command-line interface for easy access:

```bash
# Process a query with text output
python cli.py "46-year-old male, knee surgery in Pune, 3-month-old insurance policy" -d "HDFHLIP23024V072223"

# Process a query with JSON output
python cli.py "46-year-old male, knee surgery in Pune, 3-month-old insurance policy" -d "HDFHLIP23024V072223" -o json
```

### Document Indexing

Before processing queries, documents need to be indexed into the vector database:

```bash
# Index a specific document
python index_documents.py -d "docs/HDFHLIP23024V072223.pdf" -n "HDFC_ERGO_Easy_Health"

# Index all documents in a directory
python index_documents.py -dir "docs" -n "HDFC_ERGO_Easy_Health"
```

### API Endpoints

The system provides two API endpoints for integration with other applications:

#### Document Processor API

```bash
# Start the Document Processor API server
python document_processor.py
```

Send a POST request to `/process` with the following JSON body:

```json
{
  "query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
  "document_path": "docs/HDFHLIP23024V072223.pdf"
}
```

#### HackRx API

```bash
# Start the HackRx API server
python main.py
```

Send a POST request to `/hackrx/run` with the following JSON body:

```json
{
  "document_urls": ["https://example.com/policy.pdf"],
  "queries": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

The API requires authentication with a Bearer token in the Authorization header:

```
Authorization: Bearer your_api_key
```

The response will be in the following format:

```json
{
  "answers": [
    "The grace period for premium payment under the National Parivar Mediclaim Plus Policy is 30 days from the due date.",
    "The waiting period for pre-existing diseases (PED) to be covered is 48 months (4 years) from the date of inception of the policy."
  ]
}
```

### Mock Server

For testing purposes, a mock server is provided that simulates the API responses without requiring actual API keys. To use the mock server:

1. Install dependencies:
   ```
   pip install fastapi uvicorn
   ```
2. Run the mock server:
   ```
   python mock_server.py
   ```

The mock server will run on `http://localhost:8000` and provide predefined answers to common questions about insurance policies.

### API Demo

An interactive HTML demo is available in `api_demo.html` that allows you to test the API with a user-friendly interface. Simply open the file in a web browser and ensure the API server is running.

### Python Example

A Python example script is provided in `python_example.py` that demonstrates how to use the API programmatically:

```json
{
  "answers": [
    "The grace period for premium payment is 30 days from the due date.",
    "The waiting period for pre-existing diseases is 36 months of continuous coverage."
  ]
}
```

#### Testing the API

You can test the HackRx API using the provided test script:

```bash
# Test with default sample questions
python test_api.py

# Test with all sample questions
python test_api.py --all

# Test with custom questions
python test_api.py --questions "Question 1, Question 2"

# Test with a specific document URL
python test_api.py --document "https://example.com/policy.pdf"
```

## 🛠️ Tech Stack

- Backend: FastAPI
- LLM & Embeddings: Google Gemini API, Groq API
- Vector Database: Pinecone
- PDF Processing: PyPDF

## 📚 Documentation

For detailed documentation, please refer to the [DOCUMENTATION.md](DOCUMENTATION.md) file.

## 📝 Examples

The repository includes example scripts and interfaces to help you test the API:

- [test_api.html](test_api.html): A browser-based interface for testing the API (open in your browser)
- [curl_examples.md](curl_examples.md): Examples of how to test the API using cURL commands
- [python_examples.md](python_examples.md): Examples of how to test the API using Python's `requests` library
- [javascript_examples.md](javascript_examples.md): Examples of how to test the API using JavaScript's `fetch` API
- [test_api.py](test_api.py): A Python script to test the API with sample questions

## 🚢 Deployment

### Deploying to Render

This project is configured for easy deployment to Render. Follow these steps:

1. Create a Render account at [render.com](https://render.com) if you don't have one
2. Fork or clone this repository to your GitHub account
3. In the Render dashboard, click "New" and select "Blueprint"
4. Connect your GitHub account and select this repository
5. Render will automatically detect the `render.yaml` configuration
6. Click "Apply" to deploy the service

Alternatively, you can use the deployment script that helps you deploy the API to various platforms:

```bash
python deploy.py <platform>
```

Where `<platform>` can be one of the following:
- `heroku`: Deploy to Heroku
- `vercel`: Deploy to Vercel
- `railway`: Deploy to Railway
- `render`: Deploy to Render
- `docker`: Create Docker deployment files
- `all`: Create deployment files for all platforms

For detailed deployment instructions, see the [Deployment section in the documentation](DOCUMENTATION.md#deployment).

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- API keys for Google Generative AI, Pinecone, and Groq

### Quick Start

For Windows users:
```bash
.\run.ps1
```

For Linux/Mac users:
```bash
chmod +x run.sh
./run.sh
```

These scripts will:
1. Create a virtual environment if it doesn't exist
2. Install dependencies
3. Create a `.env` file from `.env.example` if it doesn't exist
4. Start the API server

### Verify Setup

To verify that all components are working correctly, run:

```bash
python verify_setup.py
```

This script will check:
- Required environment variables
- Required dependencies
- Required files
- API connectivity to Google Generative AI, Pinecone, and Groq

### Manual Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file:

```
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX=hackrx-library
API_KEY=your_api_key_for_authorization
```

## 📝 Sample Query

```
"46M, knee surgery, Pune, 3-month policy"
```

## 📝 Sample Response

```json
{
  "decision": "Approved",
  "amount": 50000,
  "justification": "The policy covers knee surgery for a 46-year-old male in Pune with a 3-month-old policy as per Clause 2.1 of the policy document.",
  "clauses": [
    {
      "clause_id": 1,
      "text": "Clause 2.1: Surgical procedures are covered after a waiting period of 30 days from the policy inception date.",
      "relevance_score": 0.89,
      "metadata": {
        "page": 12,
        "chunk": 3,
        "source": "HDFHLIP23024V072223.pdf"
      }
    }
  ]
}
```

## 🔍 Applications

This system can be applied in domains such as:
- Insurance claim processing
- Legal compliance verification
- Human resources policy enforcement
- Contract management and analysis
