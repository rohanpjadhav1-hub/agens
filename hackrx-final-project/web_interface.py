# web_interface.py

import os
import json
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

from document_processor import process_document_query

# Create FastAPI app
app = FastAPI(title="LLM Document Processing System")

# Create templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)

# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

# Create templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create HTML template file
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Document Processing System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        textarea, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
            font-family: inherit;
            font-size: 16px;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #2980b9;
        }
        .result {
            margin-top: 30px;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 4px;
            border-left: 4px solid #3498db;
        }
        .decision {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .approved {
            color: #27ae60;
        }
        .rejected {
            color: #e74c3c;
        }
        .pending {
            color: #f39c12;
        }
        .amount {
            font-size: 16px;
            margin-bottom: 10px;
        }
        .justification {
            margin-bottom: 20px;
        }
        .clauses {
            margin-top: 20px;
        }
        .clause {
            background-color: #fff;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        .clause-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .error {
            color: #e74c3c;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>LLM Document Processing System</h1>
    
    <form method="post" action="/process">
        <div class="form-group">
            <label for="query">Enter your query:</label>
            <textarea id="query" name="query" rows="4" placeholder="Example: 46-year-old male, knee surgery in Pune, 3-month-old insurance policy" required>{{ query }}</textarea>
        </div>
        
        <div class="form-group">
            <label for="document">Select document:</label>
            <select id="document" name="document">
                <option value="HDFC_ERGO_Easy_Health" {% if document == "HDFC_ERGO_Easy_Health" %}selected{% endif %}>HDFC ERGO Easy Health</option>
                <option value="Bajaj_Allianz_Global_Health" {% if document == "Bajaj_Allianz_Global_Health" %}selected{% endif %}>Bajaj Allianz Global Health</option>
                <option value="ICICI_Lombard_Golden_Shield" {% if document == "ICICI_Lombard_Golden_Shield" %}selected{% endif %}>ICICI Lombard Golden Shield</option>
                <option value="Cholamandalam_Travel" {% if document == "Cholamandalam_Travel" %}selected{% endif %}>Cholamandalam Travel</option>
                <option value="Edelweiss_Well_Baby_Well_Mother" {% if document == "Edelweiss_Well_Baby_Well_Mother" %}selected{% endif %}>Edelweiss Well Baby Well Mother</option>
            </select>
        </div>
        
        <button type="submit">Process Query</button>
    </form>
    
    {% if result %}
    <div class="result">
        <h2>Result</h2>
        
        <div class="decision {% if result.decision == 'Approved' %}approved{% elif result.decision == 'Rejected' %}rejected{% else %}pending{% endif %}">
            Decision: {{ result.decision }}
        </div>
        
        {% if result.amount %}
        <div class="amount">
            Amount: {{ result.amount }}
        </div>
        {% endif %}
        
        <div class="justification">
            <strong>Justification:</strong>
            <p>{{ result.justification }}</p>
        </div>
        
        {% if result.clauses %}
        <div class="clauses">
            <h3>Relevant Clauses</h3>
            
            {% for clause in result.clauses %}
            <div class="clause">
                <div class="clause-header">
                    <span>Clause {{ clause.clause_id }}</span>
                    {% if clause.relevance_score %}
                    <span>Relevance: {{ "%.2f"|format(clause.relevance_score) }}</span>
                    {% endif %}
                </div>
                <p>{{ clause.text }}</p>
                
                {% if clause.metadata %}
                <div class="metadata">
                    <small>
                        Source: {{ clause.metadata.source }}, 
                        Page: {{ clause.metadata.page }}, 
                        Chunk: {{ clause.metadata.chunk }}
                    </small>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    {% endif %}
    
    {% if error %}
    <div class="result error">
        <h2>Error</h2>
        <p>{{ error }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

# Write the HTML template to a file
with open(os.path.join("templates", "index.html"), "w") as f:
    f.write(index_html)

# Create CSS file
style_css = """
/* Add any additional styles here */
"""

# Write the CSS file
with open(os.path.join("static", "style.css"), "w") as f:
    f.write(style_css)

# Define routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "query": "", "document": "HDFC_ERGO_Easy_Health"}
    )

@app.post("/process", response_class=HTMLResponse)
async def process(request: Request, query: str = Form(...), document: str = Form(...)):
    try:
        # Check if API keys are set
        required_keys = ["GOOGLE_API_KEY", "PINECONE_API_KEY", "GROQ_API_KEY"]
        missing_keys = [key for key in required_keys if os.environ.get(key, "") in ["", "PASTE_YOUR_GOOGLE_API_KEY_HERE", "PASTE_YOUR_PINECONE_API_KEY_HERE", "PASTE_YOUR_GROQ_API_KEY_HERE"]]
        
        if missing_keys:
            error_message = "Error: The following API keys are not set: " + ", ".join(missing_keys)
            return templates.TemplateResponse(
                "index.html", 
                {"request": request, "query": query, "document": document, "error": error_message}
            )
        
        # Process the query
        result = process_document_query(query, document)
        
        # Return the result
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "query": query, "document": document, "result": result}
        )
    except Exception as e:
        # Return the error
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "query": query, "document": document, "error": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)