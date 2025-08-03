# Deployment Guide

## Deploying to Render

This project is configured for easy deployment to Render, a cloud platform that makes it simple to deploy web services.

### Prerequisites

- A [Render](https://render.com) account
- A GitHub account (for the easiest deployment method)

### Method 1: Using Render Blueprints (Recommended)

1. Fork this repository to your GitHub account
2. Log in to your Render account
3. In the Render dashboard, click "New" and select "Blueprint"
4. Connect your GitHub account if you haven't already
5. Select the forked repository
6. Render will automatically detect the `render.yaml` configuration
7. Click "Apply" to deploy the service
8. Wait for the deployment to complete (this may take a few minutes)
9. Once deployed, Render will provide you with a URL for your API (e.g., `https://hackrx-api.onrender.com`)

### Method 2: Manual Deployment

1. Log in to your Render account
2. In the Render dashboard, click "New" and select "Web Service"
3. Connect your GitHub account and select your repository
4. Configure the service with the following settings:
   - **Name**: hackrx-api (or any name you prefer)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn mock_server:app --host 0.0.0.0 --port $PORT`
5. Add the following environment variable:
   - **Key**: `API_KEY`
   - **Value**: `1e83fbe10fa7c1be5ffa312d8b283e496b82c2470dee257fb48b82ad7e8ba562`
6. Click "Create Web Service"
7. Wait for the deployment to complete

### Method 3: Using the Deployment Script

This repository includes a deployment script that can generate the necessary configuration files for Render:

```bash
python deploy.py render
```

After running this script, follow the instructions provided in the terminal.

## Testing Your Deployed API

Once your API is deployed, you can test it using the provided examples:

### Using the API Demo HTML Page

1. Open the `api_demo.html` file in a text editor
2. Update the API URL from `http://localhost:8000/hackrx/run` to your Render URL (e.g., `https://hackrx-api.onrender.com/hackrx/run`)
3. Save the file and open it in a web browser
4. Use the form to test your API

### Using Python

1. Open the `python_example.py` file in a text editor
2. Update the `API_URL` variable to your Render URL
3. Run the script: `python python_example.py`

### Using Node.js

1. Open the `node_example.js` file in a text editor
2. Update the `API_URL` variable to your Render URL
3. Install the required package: `npm install node-fetch`
4. Run the script: `node node_example.js`

## Troubleshooting

- **API returns 401 Unauthorized**: Make sure you're using the correct API key in your requests
- **API returns 404 Not Found**: Check that you're using the correct endpoint URL
- **Deployment fails**: Check the build logs in the Render dashboard for error messages

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)