from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from upstash_vector import Index
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI(title="Retrieval Service (Upstash)")

# Initialize Upstash Vector Index
index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    tenant_id: str

class AddDocsRequest(BaseModel):
    embeddings: list[list[float]]
    metadata: list[dict]

@app.post("/query")
async def query_docs(request: QueryRequest):
    try:
        # Upstash Vector can handle the query string directly if configured, 
        # or we can pass the embedding. For now, we'll assume we pass embeddings
        # since our Orchestrator/Embedding service handles that.
        
        # NOTE: We'll update the Orchestrator to pass the embedding to this service.
        return {"results": "Metadata filtering and vector search handled by Upstash"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-documents")
async def add_documents(request: AddDocsRequest):
    try:
        # Bulk upsert to Upstash Vector
        vectors = []
        for i, emb in enumerate(request.embeddings):
            vectors.append((f"vec_{i}_{os.urandom(4).hex()}", emb, request.metadata[i]))
        
        index.upsert(vectors=vectors)
        return {"status": "success", "count": len(request.embeddings)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "OK", "provider": "Upstash Vector"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
