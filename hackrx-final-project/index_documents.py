# index_documents.py

import os
import argparse
import glob
from typing import List, Dict, Any
import google.generativeai as genai
from pinecone import Pinecone
import re
from pypdf import PdfReader

# --- Configuration ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "PASTE_YOUR_GOOGLE_API_KEY_HERE")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "PASTE_YOUR_PINECONE_API_KEY_HERE")

# Configure services
genai.configure(api_key=GOOGLE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

PINECONE_INDEX_NAME = "hackrx-library"

def get_embedding(text: str, model="models/embedding-001"):
    """Generate embeddings for the given text using Google's embedding model."""
    try:
        result = genai.embed_content(model=model, content=text)
        return result['embedding']
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None

def extract_pdf_text(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract text from a PDF file and split it into chunks."""
    try:
        reader = PdfReader(pdf_path)
        chunks = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                # Split text into smaller chunks (paragraphs or sections)
                paragraphs = re.split(r'\n\s*\n', text)
                for j, paragraph in enumerate(paragraphs):
                    if paragraph.strip():
                        chunks.append({
                            "text": paragraph.strip(),
                            "metadata": {
                                "page": i + 1,
                                "chunk": j + 1,
                                "source": os.path.basename(pdf_path)
                            }
                        })
        return chunks
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return []

def index_document(pdf_path: str, namespace: str):
    """Index a document into the Pinecone vector database."""
    print(f"Indexing document: {pdf_path} into namespace: {namespace}")
    
    # Extract text chunks from the PDF
    chunks = extract_pdf_text(pdf_path)
    print(f"Extracted {len(chunks)} chunks from the document.")
    
    if not chunks:
        print("No text chunks extracted. Skipping indexing.")
        return
    
    # Connect to the Pinecone index
    try:
        index = pc.Index(PINECONE_INDEX_NAME)
    except Exception as e:
        print(f"Error connecting to Pinecone index: {e}")
        return
    
    # Create embeddings and index the chunks
    vectors_to_upsert = []
    for i, chunk in enumerate(chunks):
        # Generate embedding for the chunk
        embedding = get_embedding(chunk["text"])
        if embedding is None:
            print(f"Failed to generate embedding for chunk {i+1}. Skipping.")
            continue
        
        # Prepare the vector for upserting
        vector = {
            "id": f"{os.path.basename(pdf_path)}_chunk_{i+1}",
            "values": embedding,
            "metadata": {
                "text": chunk["text"],
                "page": chunk["metadata"]["page"],
                "chunk": chunk["metadata"]["chunk"],
                "source": chunk["metadata"]["source"]
            }
        }
        vectors_to_upsert.append(vector)
        
        # Upsert in batches of 100 to avoid hitting API limits
        if len(vectors_to_upsert) >= 100:
            try:
                index.upsert(vectors=vectors_to_upsert, namespace=namespace)
                print(f"Indexed batch of {len(vectors_to_upsert)} chunks.")
                vectors_to_upsert = []
            except Exception as e:
                print(f"Error upserting vectors to Pinecone: {e}")
                return
    
    # Upsert any remaining vectors
    if vectors_to_upsert:
        try:
            index.upsert(vectors=vectors_to_upsert, namespace=namespace)
            print(f"Indexed remaining {len(vectors_to_upsert)} chunks.")
        except Exception as e:
            print(f"Error upserting vectors to Pinecone: {e}")
            return
    
    print(f"Successfully indexed document: {pdf_path} into namespace: {namespace}")

def main():
    parser = argparse.ArgumentParser(description="Index insurance policy documents into the vector database.")
    parser.add_argument(
        "--document", "-d",
        type=str,
        help="Path to a specific document to index."
    )
    parser.add_argument(
        "--directory", "-dir",
        type=str,
        default="./docs",
        help="Directory containing documents to index (default: ./docs)."
    )
    parser.add_argument(
        "--namespace", "-n",
        type=str,
        required=True,
        help="Namespace to use for indexing (e.g., 'HDFC_ERGO_Easy_Health')."
    )
    
    args = parser.parse_args()
    
    # Check if Pinecone API key is set
    if PINECONE_API_KEY == "PASTE_YOUR_PINECONE_API_KEY_HERE":
        print("Error: Pinecone API key not set. Please set the PINECONE_API_KEY environment variable.")
        return
    
    # Check if Google API key is set
    if GOOGLE_API_KEY == "PASTE_YOUR_GOOGLE_API_KEY_HERE":
        print("Error: Google API key not set. Please set the GOOGLE_API_KEY environment variable.")
        return
    
    # Index a specific document if provided
    if args.document:
        if not os.path.exists(args.document):
            print(f"Error: Document not found: {args.document}")
            return
        
        index_document(args.document, args.namespace)
    else:
        # Index all PDF documents in the specified directory
        if not os.path.exists(args.directory):
            print(f"Error: Directory not found: {args.directory}")
            return
        
        pdf_files = glob.glob(os.path.join(args.directory, "*.pdf"))
        if not pdf_files:
            print(f"No PDF files found in directory: {args.directory}")
            return
        
        print(f"Found {len(pdf_files)} PDF files to index.")
        for pdf_file in pdf_files:
            index_document(pdf_file, args.namespace)

if __name__ == "__main__":
    main()