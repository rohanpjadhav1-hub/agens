# This script helps deploy the HackRx API to Render

Write-Host "Preparing for deployment to Render..." -ForegroundColor Cyan

# Create Procfile if it doesn't exist
if (-not (Test-Path -Path "Procfile")) {
    Write-Host "Creating Procfile..." -ForegroundColor Yellow
    "web: uvicorn mock_server:app --host=0.0.0.0 --port=${PORT:-8000}" | Out-File -FilePath "Procfile" -Encoding utf8
    Write-Host "Procfile created." -ForegroundColor Green
}

# Create render.yaml if it doesn't exist
if (-not (Test-Path -Path "render.yaml")) {
    Write-Host "Creating render.yaml..." -ForegroundColor Yellow
    @"
services:
  - type: web
    name: hackrx-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn mock_server:app --host 0.0.0.0 --port `$PORT
    envVars:
      - key: API_KEY
        value: 1e83fbe10fa7c1be5ffa312d8b283e496b82c2470dee257fb48b82ad7e8ba562
    plan: free
"@ | Out-File -FilePath "render.yaml" -Encoding utf8
    Write-Host "render.yaml created." -ForegroundColor Green
}

Write-Host ""
Write-Host "Deployment files created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To deploy to Render:" -ForegroundColor Cyan
Write-Host "1. Create a Render account at https://render.com" -ForegroundColor White
Write-Host "2. Push this repository to GitHub" -ForegroundColor White
Write-Host "3. In the Render dashboard, click 'New' and select 'Blueprint'" -ForegroundColor White
Write-Host "4. Connect your GitHub account and select this repository" -ForegroundColor White
Write-Host "5. Render will automatically detect the render.yaml configuration" -ForegroundColor White
Write-Host "6. Click 'Apply' to deploy the service" -ForegroundColor White
Write-Host ""
Write-Host "After deployment, update the API URL in the example files to your Render URL." -ForegroundColor Yellow
Write-Host ""

Read-Host -Prompt "Press Enter to exit"