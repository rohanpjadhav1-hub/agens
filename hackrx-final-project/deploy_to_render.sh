#!/bin/bash

# This script helps deploy the HackRx API to Render

echo "Preparing for deployment to Render..."

# Create Procfile if it doesn't exist
if [ ! -f "Procfile" ]; then
    echo "Creating Procfile..."
    echo "web: uvicorn mock_server:app --host=0.0.0.0 --port=\${PORT:-8000}" > Procfile
    echo "Procfile created."
fi

# Create render.yaml if it doesn't exist
if [ ! -f "render.yaml" ]; then
    echo "Creating render.yaml..."
    cat > render.yaml << EOL
services:
  - type: web
    name: hackrx-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn mock_server:app --host 0.0.0.0 --port \$PORT
    envVars:
      - key: API_KEY
        value: 1e83fbe10fa7c1be5ffa312d8b283e496b82c2470dee257fb48b82ad7e8ba562
    plan: free
EOL
    echo "render.yaml created."
fi

echo ""
echo "Deployment files created successfully!"
echo ""
echo "To deploy to Render:"
echo "1. Create a Render account at https://render.com"
echo "2. Push this repository to GitHub"
echo "3. In the Render dashboard, click 'New' and select 'Blueprint'"
echo "4. Connect your GitHub account and select this repository"
echo "5. Render will automatically detect the render.yaml configuration"
echo "6. Click 'Apply' to deploy the service"
echo ""
echo "After deployment, update the API URL in the example files to your Render URL."
echo ""