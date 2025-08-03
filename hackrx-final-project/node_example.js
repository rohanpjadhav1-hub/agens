// node_example.js

// This example demonstrates how to use the HackRx API with Node.js
// To run this example, you need to have Node.js installed and run:
// npm install node-fetch
// node node_example.js

const fetch = require('node-fetch');

// API endpoint
// For local testing, use http://localhost:8000/hackrx/run
// For deployed version, use your Render URL (e.g., https://hackrx-api.onrender.com/hackrx/run)
const API_URL = 'http://localhost:8000/hackrx/run';  // Change this to your deployed URL when needed

// API key (replace with your actual API key)
const API_KEY = '1e83fbe10fa7c1be5ffa312d8b283e496b82c2470dee257fb48b82ad7e8ba562';

// Document URL
const DOCUMENT_URL = 'https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D';

// List of questions
const QUESTIONS = [
  'What is the grace period for premium payment?',
  'What is the waiting period for pre-existing diseases?',
  'Does this policy cover maternity expenses, and what are the conditions?'
];

// Function to query the API
async function queryApi() {
  try {
    console.log('Sending request to API...');
    
    // Prepare request headers
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`
    };
    
    // Prepare request payload
    const payload = {
      document_urls: [DOCUMENT_URL],
      queries: QUESTIONS
    };
    
    // Send POST request to API
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(payload)
    });
    
    // Check if request was successful
    if (response.ok) {
      // Parse JSON response
      const data = await response.json();
      
      // Print formatted results
      console.log('\nAPI Response:');
      console.log(JSON.stringify(data, null, 2));
      
      // Print questions and answers in a more readable format
      console.log('\nQuestions and Answers:');
      QUESTIONS.forEach((question, index) => {
        console.log(`\nQ${index + 1}: ${question}`);
        console.log(`A${index + 1}: ${data.answers[index]}`);
      });
      
    } else {
      console.error(`Error: API returned status code ${response.status}`);
      console.error(`Response: ${await response.text()}`);
    }
    
  } catch (error) {
    console.error(`Error: ${error.message}`);
  }
}

// Call the function
queryApi();