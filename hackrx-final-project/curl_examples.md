# API Testing with cURL

This document provides examples of how to test the HackRx API using cURL commands.

## Prerequisites

- The API server is running (`python main.py`)
- You have set up your API key in the `.env` file

## Testing the HackRx API

### Basic Query

```bash
curl -X POST "http://localhost:8000/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "document_urls": ["https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"],
    "queries": ["What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"]
  }'
```

### Multiple Queries

```bash
curl -X POST "http://localhost:8000/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "document_urls": ["https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"],
    "queries": [
      "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
      "What is the waiting period for pre-existing diseases (PED) to be covered?",
      "Does this policy cover maternity expenses, and what are the conditions?"
    ]
  }'
```

### Using a Different Document URL

```bash
curl -X POST "http://localhost:8000/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "document_urls": ["https://example.com/your-policy-document.pdf"],
    "queries": ["What is the grace period for premium payment?"]
  }'
```

## Testing the Document Processor API

```bash
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
    "document_path": "docs/HDFHLIP23024V072223.pdf"
  }'
```

## Windows PowerShell Examples

For Windows PowerShell, you need to escape the quotes differently:

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/hackrx/run" `
  -Headers @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer your_api_key"
  } `
  -Body '{"document_urls":["https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"],"queries":["What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"]}'
```