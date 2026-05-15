from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
import redis
import json
from upstash_redis import Redis as UpstashRedis
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI(title="Agent Service")

# Redis Configuration (Support both TCP and REST)
UPSTASH_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

if UPSTASH_REST_URL and UPSTASH_REST_TOKEN:
    # Use Upstash REST client
    redis_client = UpstashRedis(url=UPSTASH_REST_URL, token=UPSTASH_REST_TOKEN)
    print("Using Upstash REST Redis client")
else:
    # Fallback to standard TCP client
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD"),
        ssl=os.getenv("REDIS_USE_TLS", "false").lower() == "true",
        decode_responses=True
    )
    print("Using Standard TCP Redis client")

# Load LLM
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
)

class AgentRequest(BaseModel):
    message: str
    context: list
    session_id: str
    user_id: str
    tenant_id: str

@app.post("/process")
async def process_agent_task(request: AgentRequest):
    try:
        # Prepare system message with context
        context_str = "\n".join([f"- {c['metadata'].get('source')}: {c['metadata'].get('chunk_id')}" for c in request.context])
        
        system_prompt = f"""You are the IndiGo Enterprise AI Operations Copilot. 
        Your goal is to assist staff with operational queries using the provided context.
        
        Tenant ID: {request.tenant_id}
        User ID: {request.user_id}
        
        Context from documents:
        {context_str}
        
        Answer based ONLY on the context provided if possible. If not in context, state you don't have that specific information but try to be helpful based on general aviation knowledge if appropriate.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=request.message)
        ]
        
        response = llm.invoke(messages)
        
        return {"response": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
