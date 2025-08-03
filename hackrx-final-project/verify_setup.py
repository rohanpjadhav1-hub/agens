#!/usr/bin/env python
# verify_setup.py - Script to verify that all components are working correctly

import os
import sys
import json
import importlib.util
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_vars():
    """Check if all required environment variables are set."""
    required_vars = [
        "GOOGLE_API_KEY",
        "PINECONE_API_KEY",
        "GROQ_API_KEY",
        "PINECONE_ENVIRONMENT",
        "PINECONE_INDEX",
        "API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    else:
        print("✅ All required environment variables are set.")
        return True

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        "fastapi",
        "google-generativeai",
        "groq",
        "pinecone-client",
        "pydantic",
        "pypdf",
        "python-dotenv",
        "requests",
        "uvicorn"
    ]
    
    missing_packages = []
    for package in required_packages:
        spec = importlib.util.find_spec(package.replace("-", "_"))
        if spec is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing dependencies:")
        for package in missing_packages:
            print(f"  - {package}")
        return False
    else:
        print("✅ All required dependencies are installed.")
        return True

def check_files():
    """Check if all required files exist."""
    required_files = [
        "main.py",
        "document_processor.py",
        "cli.py",
        "index_documents.py",
        "web_interface.py",
        "test_processor.py",
        "test_api.py",
        "requirements.txt",
        "README.md",
        "DOCUMENTATION.md"
    ]
    
    missing_files = [file for file in required_files if not os.path.exists(file)]
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ All required files exist.")
        return True

def check_api_connectivity():
    """Check if the API keys are valid and can connect to the services."""
    # Check Google API
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        models = genai.list_models()
        if models:
            print("✅ Successfully connected to Google Generative AI API.")
        else:
            print("❌ Failed to list models from Google Generative AI API.")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to Google Generative AI API: {str(e)}")
        return False
    
    # Check Pinecone API
    try:
        import pinecone
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENVIRONMENT")
        )
        indexes = pinecone.list_indexes()
        print(f"✅ Successfully connected to Pinecone API. Available indexes: {indexes}")
    except Exception as e:
        print(f"❌ Failed to connect to Pinecone API: {str(e)}")
        return False
    
    # Check Groq API
    try:
        import groq
        client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
        models = client.models.list()
        if models:
            print("✅ Successfully connected to Groq API.")
        else:
            print("❌ Failed to list models from Groq API.")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to Groq API: {str(e)}")
        return False
    
    return True

def main():
    print("🔍 Verifying setup for HackRx API...\n")
    
    env_check = check_env_vars()
    print()
    
    dep_check = check_dependencies()
    print()
    
    file_check = check_files()
    print()
    
    if env_check and dep_check and file_check:
        print("🔌 Checking API connectivity...\n")
        api_check = check_api_connectivity()
        print()
        
        if api_check:
            print("🎉 All checks passed! Your setup is ready to go.")
            return 0
        else:
            print("⚠️ API connectivity check failed. Please check your API keys and try again.")
            return 1
    else:
        print("⚠️ Some checks failed. Please fix the issues and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())