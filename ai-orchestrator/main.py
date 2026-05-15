from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import httpx
import os
import uuid
from guardrails import Guardrails
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI(title="AI Orchestrator")

AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL", "http://agent-service:8002")
RETRIEVAL_SERVICE_URL = os.getenv("RETRIEVAL_SERVICE_URL", "http://retrieval-service:8003")

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

@app.post("/chat")
async def chat(
    request: ChatRequest,
    x_user_id: str = Header(None),
    x_tenant_id: str = Header(None)
):
    try:
        # 0. Input Guardrails
        if Guardrails.detect_prompt_injection(request.message):
            raise HTTPException(status_code=400, detail="Security Violation: Prompt Injection Detected")
        
        message = Guardrails.scrub_pii(request.message)
        
        session_id = request.session_id or str(uuid.uuid4())
        
        # 1. Retrieval Step
        async with httpx.AsyncClient() as client:
            retrieval_resp = await client.post(
                f"{RETRIEVAL_SERVICE_URL}/query",
                json={"query": message, "tenant_id": x_tenant_id}
            )
            context = retrieval_resp.json().get("results", [])
        
        # 2. Agent Step
        async with httpx.AsyncClient() as client:
            agent_resp = await client.post(
                f"{AGENT_SERVICE_URL}/process",
                json={
                    "message": message,
                    "context": context,
                    "session_id": session_id,
                    "user_id": x_user_id,
                    "tenant_id": x_tenant_id
                }
            )
            agent_data = agent_resp.json()
        
        response = Guardrails.scrub_pii(agent_data.get("response", ""))
        
        return {
            "session_id": session_id,
            "response": response,
            "sources": [r["metadata"] for r in context]
        }
    except Exception as e:
        print(f"Error in Orchestrator: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
