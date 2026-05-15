from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
import json
import asyncio
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI(title="Streaming Service")

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    streaming=True
)

@app.post("/stream")
async def stream_chat(request: Request):
    data = await request.json()
    message = data.get("message")
    context = data.get("context", [])
    
    async def event_generator():
        try:
            # Simplified streaming logic
            context_str = str(context)
            system_prompt = f"You are a helpful assistant. Context: {context_str}"
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            
            async for chunk in llm.astream(messages):
                if chunk.content:
                    yield f"data: {json.dumps({'token': chunk.content})}\n\n"
            
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/health")
async def health():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
