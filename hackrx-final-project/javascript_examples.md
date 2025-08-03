# API Testing with JavaScript Fetch

This document provides examples of how to test the HackRx API using JavaScript's `fetch` API.

## Prerequisites

- The API server is running (`python main.py`)
- You have set up your API key in the `.env` file
- You have a JavaScript environment (browser or Node.js)

## Testing the HackRx API

### Browser Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HackRx API Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        pre {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        button {
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input {
            padding: 8px;
            width: 100%;
            margin-bottom: 10px;
        }
        textarea {
            width: 100%;
            height: 100px;
            padding: 8px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>HackRx API Test</h1>
    
    <div>
        <h2>API Key</h2>
        <input type="text" id="apiKey" placeholder="Enter your API key">
    </div>
    
    <div>
        <h2>Document URL</h2>
        <input type="text" id="documentUrl" value="https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D">
    </div>
    
    <div>
        <h2>Queries</h2>
        <textarea id="queries">What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?
What is the waiting period for pre-existing diseases (PED) to be covered?</textarea>
        <p><small>Enter one query per line</small></p>
    </div>
    
    <button onclick="sendRequest()">Send Request</button>
    
    <div>
        <h2>Response</h2>
        <pre id="response">Response will appear here...</pre>
    </div>
    
    <script>
        async function sendRequest() {
            const apiKey = document.getElementById('apiKey').value;
            const documentUrl = document.getElementById('documentUrl').value;
            const queriesText = document.getElementById('queries').value;
            const queries = queriesText.split('\n').filter(q => q.trim() !== '');
            
            const url = 'http://localhost:8000/hackrx/run';
            
            const data = {
                document_urls: [documentUrl],
                queries: queries
            };
            
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${apiKey}`
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                document.getElementById('response').textContent = JSON.stringify(result, null, 2);
            } catch (error) {
                document.getElementById('response').textContent = `Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
```

### Node.js Example

```javascript
const fetch = require('node-fetch');
require('dotenv').config();

async function testHackRxApi() {
    // Get API key from environment variables
    const apiKey = process.env.API_KEY;
    
    // API endpoint
    const url = 'http://localhost:8000/hackrx/run';
    
    // Request body
    const data = {
        document_urls: ['https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D'],
        queries: [
            'What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?',
            'What is the waiting period for pre-existing diseases (PED) to be covered?'
        ]
    };
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        console.log('Status Code:', response.status);
        console.log('Response:', JSON.stringify(result, null, 2));
    } catch (error) {
        console.error('Error:', error.message);
    }
}

testHackRxApi();
```

## Testing the Document Processor API

```javascript
const fetch = require('node-fetch');

async function testDocumentProcessorApi() {
    // API endpoint
    const url = 'http://localhost:8000/process';
    
    // Request body
    const data = {
        query: '46-year-old male, knee surgery in Pune, 3-month-old insurance policy',
        document_path: 'docs/HDFHLIP23024V072223.pdf'
    };
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        console.log('Status Code:', response.status);
        console.log('Response:', JSON.stringify(result, null, 2));
    } catch (error) {
        console.error('Error:', error.message);
    }
}

testDocumentProcessorApi();
```