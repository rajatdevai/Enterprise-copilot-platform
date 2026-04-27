from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional, List
import json
import asyncio
from router.intent_router import IntentRouter, Intent
from llm.openai_engine import OpenAIEngine
from rag.retriever import RAGRetriever
from utils.memory_manager import MemoryManager
from config import config

app = FastAPI(title="Enterprise AI Copilot - Scalable AI Service")

intent_router = IntentRouter()
llm_engine = OpenAIEngine()
rag_retriever = RAGRetriever()
memory_manager = MemoryManager()

# Security: System Prompts defined here to maintain internal control
SYSTEM_PROMPTS = {
    "GENERAL": "You are a helpful Enterprise AI assistant. You provide general intelligence and reasoning.",
    "RAG": "You are an Enterprise AI assistant with access to company internal documents. Use the provided context to answer the user's question accurately. If the information is not in the context, say you don't know.",
    "FILES": "You are analyzing documents uploaded by the user. Be precise and thorough."
}

from utils.pii_scrubber import pii_scrubber
from utils.cache_manager import cache_manager

@app.post("/chat/stream")
async def chat_stream(
    query: str = Form(...),
    history_json: str = Form("[]"),
    files: Optional[List[UploadFile]] = File(None)
):
    # 1. PII Scrubbing (Privacy first)
    scrubbed_query = pii_scrubber.scrub(query)
    history = json.loads(history_json)
    has_files = files is not None and len(files) > 0

    # 2. Caching Layer (Performance)
    # Check cache for non-file general queries
    if not has_files:
        cached = cache_manager.get_cached_response(scrubbed_query)
        if cached:
            return StreamingResponse(
                iter([f"data: {json.dumps({'content': cached, 'source': 'Cache'})}\n\n", "data: [DONE]\n\n"]),
                media_type="text/event-stream"
            )

    # 3. Intent Routing
    intent = await intent_router.route(scrubbed_query, context_metadata={"has_files": has_files})

    
    # 2. Context Isolation & Security
    context = ""
    system_prompt = SYSTEM_PROMPTS["GENERAL"]
    
    if intent == Intent.KNOWLEDGE_RETRIEVAL:
        context = await rag_retriever.retrieve(query)
        system_prompt = SYSTEM_PROMPTS["RAG"]
    elif intent == Intent.DOCUMENT_ANALYSIS or has_files:
        system_prompt = SYSTEM_PROMPTS["FILES"]

    # 3. Memory Optimization (Sliding Window)
    optimized_history = memory_manager.trim_history(history)
    
    # Construct Messages
    messages = [{"role": "system", "content": system_prompt}]
    if context:
        messages.append({"role": "system", "content": f"COMPANY CONTEXT: {context}"})
    
    messages.extend(optimized_history)
    messages.append({"role": "user", "content": scrubbed_query})


    # 4. SSE Streaming Generator
    async def event_generator():
        try:
            async for chunk in llm_engine.generate_stream(messages):
                # SSE format: data: <chunk>\n\n
                yield f"data: {json.dumps({'content': chunk, 'intent': intent})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    # High concurrency settings
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)
