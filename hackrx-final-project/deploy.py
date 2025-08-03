# deploy.py

import os
import argparse
import subprocess
import shutil
import json

def create_heroku_files():
    """Create necessary files for Heroku deployment."""
    print("Creating Heroku deployment files...")
    
    # Create Procfile
    with open("Procfile", "w") as f:
        f.write("web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}")
    print("Created Procfile")
    
    # Create runtime.txt
    with open("runtime.txt", "w") as f:
        f.write("python-3.9.16")
    print("Created runtime.txt")
    
    print("Heroku deployment files created successfully.")

def create_vercel_files():
    """Create necessary files for Vercel deployment."""
    print("Creating Vercel deployment files...")
    
    # Create vercel.json
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "main.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "main.py"
            }
        ]
    }
    
    with open("vercel.json", "w") as f:
        json.dump(vercel_config, f, indent=2)
    print("Created vercel.json")
    
    print("Vercel deployment files created successfully.")

def create_railway_files():
    """Create necessary files for Railway deployment."""
    print("Creating Railway deployment files...")
    
    # Railway uses Procfile similar to Heroku
    with open("Procfile", "w") as f:
        f.write("web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}")
    print("Created Procfile")
    
    print("Railway deployment files created successfully.")

def create_render_files():
    """Create necessary files for Render deployment."""
    print("Creating Render deployment files...")
    
    # Create render.yaml
    render_config = {
        "services": [
            {
                "type": "web",
                "name": "hackrx-api",
                "env": "python",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
                "envVars": [
                    {
                        "key": "GOOGLE_API_KEY",
                        "sync": "false"
                    },
                    {
                        "key": "PINECONE_API_KEY",
                        "sync": "false"
                    },
                    {
                        "key": "GROQ_API_KEY",
                        "sync": "false"
                    }
                ]
            }
        ]
    }
    
    with open("render.yaml", "w") as f:
        json.dump(render_config, f, indent=2)
    print("Created render.yaml")
    
    print("Render deployment files created successfully.")

def create_docker_files():
    """Create necessary files for Docker deployment."""
    print("Creating Docker deployment files...")
    
    # Create Dockerfile
    dockerfile_content = """
    FROM python:3.9-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 8000

    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    """
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content.strip())
    print("Created Dockerfile")
    
    # Create .dockerignore
    dockerignore_content = """
    __pycache__
    *.pyc
    *.pyo
    *.pyd
    .Python
    env/
    venv/
    .env
    .git
    .gitignore
    .vscode
    .idea
    """
    
    with open(".dockerignore", "w") as f:
        f.write(dockerignore_content.strip())
    print("Created .dockerignore")
    
    # Create docker-compose.yml
    docker_compose_content = """
    version: '3'

    services:
      api:
        build: .
        ports:
          - "8000:8000"
        environment:
          - GOOGLE_API_KEY=${GOOGLE_API_KEY}
          - PINECONE_API_KEY=${PINECONE_API_KEY}
          - GROQ_API_KEY=${GROQ_API_KEY}
    """
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content.strip())
    print("Created docker-compose.yml")
    
    print("Docker deployment files created successfully.")

def deploy_to_platform(platform):
    """Deploy the application to the specified platform."""
    if platform == "heroku":
        create_heroku_files()
        print("\nTo deploy to Heroku, run the following commands:")
        print("1. heroku create your-app-name")
        print("2. git push heroku main")
        print("3. heroku config:set GOOGLE_API_KEY=your_google_api_key PINECONE_API_KEY=your_pinecone_api_key GROQ_API_KEY=your_groq_api_key")
    
    elif platform == "vercel":
        create_vercel_files()
        print("\nTo deploy to Vercel, run the following commands:")
        print("1. vercel login")
        print("2. vercel")
        print("3. Set environment variables in the Vercel dashboard")
    
    elif platform == "railway":
        create_railway_files()
        print("\nTo deploy to Railway, run the following commands:")
        print("1. railway login")
        print("2. railway init")
        print("3. railway up")
        print("4. Set environment variables in the Railway dashboard")
    
    elif platform == "render":
        create_render_files()
        print("\nTo deploy to Render:")
        print("1. Create a new Web Service in the Render dashboard")
        print("2. Connect your GitHub repository")
        print("3. Set environment variables in the Render dashboard")
    
    elif platform == "docker":
        create_docker_files()
        print("\nTo deploy using Docker, run the following commands:")
        print("1. docker build -t hackrx-api .")
        print("2. docker run -p 8000:8000 -e GOOGLE_API_KEY=your_google_api_key -e PINECONE_API_KEY=your_pinecone_api_key -e GROQ_API_KEY=your_groq_api_key hackrx-api")
        print("\nOr using Docker Compose:")
        print("1. docker-compose up")
    
    else:
        print(f"Deployment to {platform} is not supported yet.")

def main():
    parser = argparse.ArgumentParser(description="Deploy the HackRx API to various platforms.")
    parser.add_argument(
        "platform",
        type=str,
        choices=["heroku", "vercel", "railway", "render", "docker", "all"],
        help="Platform to deploy to (heroku, vercel, railway, render, docker, or all)."
    )
    
    args = parser.parse_args()
    
    if args.platform == "all":
        platforms = ["heroku", "vercel", "railway", "render", "docker"]
        for platform in platforms:
            deploy_to_platform(platform)
            print("\n" + "-"*50 + "\n")
    else:
        deploy_to_platform(args.platform)

if __name__ == "__main__":
    main()