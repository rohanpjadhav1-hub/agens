# HackRx API - Render Deployment

## Overview

This repository contains the HackRx API, a system that uses Large Language Models (LLMs) to process natural language queries and retrieve relevant information from large unstructured documents such as policy documents, contracts, and emails.

## Deployment on Render

This project is configured for easy deployment on Render. The deployment is handled through the `render.yaml` file, which defines the service configuration.

### Deployment Steps

1. Fork or clone this repository to your GitHub account
2. Create a Render account at [render.com](https://render.com) if you don't have one
3. In the Render dashboard, click "New" and select "Blueprint"
4. Connect your GitHub account and select this repository
5. Render will automatically detect the `render.yaml` configuration
6. Click "Apply" to deploy the service
7. Wait for the deployment to complete (this may take a few minutes)
8. Once deployed, Render will provide you with a URL for your API (e.g., `https://hackrx-api.onrender.com`)

### Testing the Deployed API

Once your API is deployed, you can test it using the provided examples:

#### Using the API Demo HTML Page

1. Open the `api_demo.html` file in a web browser
2. Update the API URL from `http://localhost:8000/hackrx/run` to your Render URL (e.g., `https://hackrx-api.onrender.com/hackrx/run`)
3. Use the form to test your API

#### Using Python

1. Open the `python_example.py` file in a text editor
2. Update the `API_URL` variable to your Render URL
3. Run the script: `python python_example.py`

#### Using Node.js

1. Open the `node_example.js` file in a text editor
2. Update the `API_URL` variable to your Render URL
3. Install the required package: `npm install node-fetch`
4. Run the script: `node node_example.js`

## API Documentation

### Endpoint

`POST /hackrx/run`

### Request Format

```json
{
  "document_urls": ["https://example.com/policy.pdf"],
  "queries": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

### Authentication

The API requires authentication with a Bearer token in the Authorization header:

```
Authorization: Bearer 1e83fbe10fa7c1be5ffa312d8b283e496b82c2470dee257fb48b82ad7e8ba562
```

### Response Format

```json
{
  "answers": [
    "The grace period for premium payment under the National Parivar Mediclaim Plus Policy is 30 days from the due date.",
    "The waiting period for pre-existing diseases (PED) to be covered is 48 months (4 years) from the date of inception of the policy."
  ]
}
```

## Additional Resources

- For more detailed information, see the main [README.md](README.md) file
- For deployment troubleshooting, see the [DEPLOYMENT.md](DEPLOYMENT.md) file