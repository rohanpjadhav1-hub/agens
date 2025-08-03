# LLM Document Processing System - Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Components](#components)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Web Interface](#web-interface)
8. [Command Line Interface](#command-line-interface)
9. [Document Indexing](#document-indexing)
10. [Customization](#customization)
11. [Troubleshooting](#troubleshooting)
12. [Performance Considerations](#performance-considerations)
13. [Security Considerations](#security-considerations)
14. [Deployment](#deployment)
15. [Future Improvements](#future-improvements)

## System Overview

The LLM Document Processing System is designed to process natural language queries against large unstructured documents such as policy documents, contracts, and emails. It uses a Retrieval-Augmented Generation (RAG) architecture to extract relevant information from documents and generate structured responses based on the query.

The system can:

- Parse and structure natural language queries
- Search and retrieve relevant clauses from documents using semantic understanding
- Evaluate retrieved information to determine decisions (e.g., approval status, payout amount)
- Return structured JSON responses with decisions, amounts, and justifications

## Architecture

The system follows a Retrieval-Augmented Generation (RAG) architecture with the following components:

1. **Document Processing Pipeline**:
   - Document ingestion and chunking
   - Text extraction from various document formats (PDF, Word, etc.)
   - Embedding generation using Google Gemini API
   - Vector storage in Pinecone database

2. **Query Processing Pipeline**:
   - Query parsing and structuring
   - Semantic search in the vector database
   - Context retrieval and augmentation
   - Decision generation using Groq API

3. **Response Generation**:
   - Structured JSON output
   - Decision justification with reference to specific clauses
   - Amount calculation (if applicable)

## Components

### Document Processor (`document_processor.py`)

The core component that handles:

- Configuration of API clients (Google Generative AI, Pinecone, Groq)
- Embedding generation for queries
- Retrieval of relevant clauses from the vector database
- Decision generation based on the query and retrieved clauses
- Structured response formatting

### CLI Interface (`cli.py`)

A command-line interface that allows users to:

- Process queries against indexed documents
- Specify document identifiers
- Choose output format (JSON or text)

### Document Indexing (`index_documents.py`)

A utility for indexing documents into the vector database:

- Extracts text from PDF files
- Chunks text into manageable segments
- Generates embeddings for each chunk
- Indexes chunks into Pinecone with metadata

### Web Interface (`web_interface.py`)

A user-friendly web interface that provides:

- A form for entering queries
- Document selection dropdown
- Formatted display of results
- Error handling and user feedback

### API Endpoint (`main.py`)

A FastAPI application that exposes:

- RESTful API endpoints for document processing
- Authentication and request validation
- Structured JSON responses

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- API keys for:
  - Google Generative AI
  - Pinecone
  - Groq

### Installation Steps

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the project root with the following variables:

```
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX=your_pinecone_index
```

## Usage

### Indexing Documents

Before using the system, you need to index your documents into the vector database:

```bash
python index_documents.py --document_path ./docs/policy.pdf --namespace HDFC_ERGO_Easy_Health
```

Or index all documents in a directory:

```bash
python index_documents.py --directory ./docs --namespace Bajaj_Allianz_Global_Health
```

### Processing Queries via CLI

Use the command-line interface to process queries:

```bash
python cli.py --query "46-year-old male, knee surgery in Pune, 3-month-old insurance policy" --document HDFC_ERGO_Easy_Health --format json
```

### Using the Web Interface

Start the web interface:

```bash
python web_interface.py
```

Then open your browser and navigate to `http://localhost:8000`.

### Using the API

Start the API server:

```bash
python main.py
```

Send a request to the API endpoint:

```bash
curl -X POST "http://localhost:8000/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{"document_urls":["HDFC_ERGO_Easy_Health"],"queries":["46-year-old male, knee surgery in Pune, 3-month-old insurance policy"]}'
```

## API Reference

### Document Processor API - `/process` Endpoint

**Method**: POST

**Headers**:
- `Content-Type: application/json`

**Request Body**:

```json
{
  "query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
  "document_path": "docs/HDFHLIP23024V072223.pdf"
}
```

**Response**:

```json
{
  "decision": "Approved",
  "amount": 50000,
  "justification": "The policy covers knee surgery for a 46-year-old male in Pune with a 3-month-old policy as per clause 2.1.",
  "clauses": [
    {
      "clause_id": "2.1",
      "text": "The policy covers surgical procedures...",
      "relevance_score": 0.92,
      "metadata": {
        "source": "policy.pdf",
        "page": 5,
        "chunk": 3
      }
    }
  ]
}
```

### HackRx API - `/hackrx/run` Endpoint

**Method**: POST

**Headers**:
- `Content-Type: application/json`
- `Authorization: Bearer <api_key>`

**Request Body**:

```json
{
  "document_urls": ["https://example.com/policy.pdf"],
  "queries": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

**Response**:

```json
{
  "answers": [
    "The grace period for premium payment is 30 days from the due date.",
    "The waiting period for pre-existing diseases is 36 months of continuous coverage."
  ]
}
```

### Testing the API

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

## Web Interface

The web interface provides a user-friendly way to interact with the system. It includes:

- A form for entering queries
- A dropdown for selecting documents
- A results section displaying:
  - Decision (Approved/Rejected)
  - Amount (if applicable)
  - Justification
  - Relevant clauses with their text and metadata

## Command Line Interface

The CLI supports the following arguments:

- `--query`: The natural language query to process
- `--document`: The document namespace to query against (optional)
- `--format`: Output format (json or text, default: text)

## Document Indexing

The document indexing utility supports:

- Indexing individual PDF files
- Indexing all PDFs in a directory
- Specifying a namespace for the indexed documents
- Customizing chunk size and overlap

## Customization

### Modifying Embedding Generation

You can customize the embedding generation process by modifying the `generate_embeddings` function in `document_processor.py`.

### Adjusting Chunking Parameters

You can adjust the chunking parameters in `index_documents.py` to optimize for your specific documents:

```python
chunk_size = 1000  # Number of characters per chunk
chunk_overlap = 200  # Number of overlapping characters between chunks
```

### Customizing Decision Generation

You can modify the prompt template in `document_processor.py` to customize how decisions are generated:

```python
prompt_template = """
Based on the following query and policy clauses, determine if the claim should be approved or rejected.

Query: {query}

Relevant Policy Clauses:
{context}

Provide a JSON response with the following structure:
{{
  "decision": "Approved" or "Rejected",
  "amount": null or a number,
  "justification": "Explanation referencing specific clauses"
}}
"""
```

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Ensure all API keys are correctly set in the `.env` file
   - Check that the API keys have the necessary permissions

2. **Document Indexing Failures**:
   - Verify that the document format is supported
   - Check that the document is readable and not corrupted
   - Ensure sufficient permissions to read the document

3. **Query Processing Errors**:
   - Verify that the document namespace exists in the vector database
   - Check that the query is well-formed and contains sufficient information
   - Ensure the LLM API is accessible and responding

### Debugging

To enable debugging, set the `DEBUG` environment variable to `True`:

```bash
DEBUG=True python cli.py --query "..." --document "..."
```

## Performance Considerations

### Optimizing Document Indexing

- Adjust chunk size based on document complexity
- Use smaller chunks for dense, technical documents
- Use larger chunks for narrative, flowing documents

### Optimizing Query Processing

- Limit the number of retrieved clauses to improve response time
- Adjust relevance thresholds to filter out less relevant clauses
- Cache frequently used embeddings to reduce API calls

## Security Considerations

- API keys should be stored securely and never committed to version control
- Use environment variables or a secure key management system
- Implement proper authentication for the API endpoints
- Validate and sanitize all user inputs
- Consider data privacy regulations when processing sensitive documents

## Deployment

The system includes a deployment script that helps you deploy the API to various platforms:

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

### Heroku Deployment

```bash
python deploy.py heroku
heroku create your-app-name
git push heroku main
heroku config:set GOOGLE_API_KEY=your_google_api_key PINECONE_API_KEY=your_pinecone_api_key GROQ_API_KEY=your_groq_api_key
```

### Docker Deployment

```bash
python deploy.py docker
docker build -t hackrx-api .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_google_api_key -e PINECONE_API_KEY=your_pinecone_api_key -e GROQ_API_KEY=your_groq_api_key hackrx-api
```

Or using Docker Compose:

```bash
docker-compose up
```

## Future Improvements

1. **Multi-Modal Support**:
   - Add support for processing images and diagrams within documents
   - Implement OCR for scanned documents

2. **Advanced Query Understanding**:
   - Implement more sophisticated query parsing
   - Support for complex, multi-part queries

3. **Improved Decision Logic**:
   - Add support for more complex decision rules
   - Implement a rule engine for deterministic decisions

4. **Performance Optimizations**:
   - Implement caching for frequently accessed documents
   - Optimize embedding generation for large documents

5. **User Experience**:
   - Add support for query suggestions
   - Implement a feedback mechanism for improving responses
   - Develop a more sophisticated web interface with user authentication