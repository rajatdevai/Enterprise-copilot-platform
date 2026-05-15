from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter
import httpx
import os
import shutil
import uuid
import json
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI(title="Document Service")

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Upstash QStash Configuration
QSTASH_TOKEN = os.getenv("QSTASH_TOKEN")
QSTASH_URL = os.getenv("QSTASH_URL", "https://qstash.upstash.io")

EMBEDDING_SERVICE_URL = os.getenv("EMBEDDING_SERVICE_URL", "http://embedding-service:8004")
RETRIEVAL_SERVICE_URL = os.getenv("RETRIEVAL_SERVICE_URL", "http://retrieval-service:8003")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
)

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    tenant_id: str = Form(...),
    user_id: str = Form(...)
):
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOADS_DIR, f"{file_id}_{file.filename}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Simple text extraction (placeholder for OCR)
        # For now, let's assume it's a text file or we just use the filename
        content = f"Content of {file.filename}. This is a placeholder for actual extraction logic."
        
        # Chunking
        chunks = text_splitter.split_text(content)
        
        # Get embeddings
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{EMBEDDING_SERVICE_URL}/embed/batch", json={"texts": chunks})
            resp.raise_for_status()
            embeddings = resp.json()["embeddings"]
            
            # Notify via QStash (Replacement for Kafka)
            if QSTASH_TOKEN:
                async with httpx.AsyncClient() as qclient:
                    await qclient.post(
                        f"{QSTASH_URL}/v2/publish/http://worker-service:8007/process",
                        headers={"Authorization": f"Bearer {QSTASH_TOKEN}"},
                        json={
                            "file_id": file_id,
                            "tenant_id": tenant_id,
                            "chunks": len(chunks)
                        }
                    )
        
        return {"status": "completed", "file_id": file_id, "chunks": len(chunks), "async": "QStash triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
