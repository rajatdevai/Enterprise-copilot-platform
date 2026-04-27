import json
import google.generativeai as genai
from enum import Enum
from typing import Optional, Dict
from config import config

class Intent(str, Enum):
    KNOWLEDGE_RETRIEVAL = "KNOWLEDGE_RETRIEVAL" # Company RAG
    GENERAL_REASONING = "GENERAL_REASONING"   # General LLM
    DOCUMENT_ANALYSIS = "DOCUMENT_ANALYSIS"   # Temporary uploaded doc
    SENSITIVE_ACTION = "SENSITIVE_ACTION"     # Human-in-loop
    INVALID = "INVALID"

from openai import AsyncOpenAI
import os

class IntentRouter:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key)
        # Using gpt-4o-mini for fast, cost-effective routing
        self.model = "gpt-4o-mini"


    async def route(self, query: str, context_metadata: Dict = {}) -> Intent:
        """
        Uses semantic analysis to determine the user's intent.
        """
        prompt = f"""
        Analyze the following user query for an Enterprise AI Copilot system.
        Classify the query into one of these categories:
        
        1. KNOWLEDGE_RETRIEVAL: Query is about company policies, internal documents, procedures, or domain-specific knowledge stored in the organization's database.
        2. GENERAL_REASONING: Query is a general question, coding problem, creative task, or explanation that doesn't rely on company-specific data.
        3. SENSITIVE_ACTION: User wants to perform an action that requires authorization, approval, or modification of sensitive data (e.g., salary changes, system configuration).
        4. DOCUMENT_ANALYSIS: User is asking about a specific file they have just uploaded (indicated by context).
        
        Query: "{query}"
        Context: {json.dumps(context_metadata)}
        
        Return ONLY a JSON object with the "intent" key.
        Example: {{"intent": "KNOWLEDGE_RETRIEVAL"}}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            
            response_text = response.choices[0].message.content
            data = json.loads(response_text)
            intent_str = data.get("intent", "GENERAL_REASONING")
            return Intent(intent_str)
        except Exception as e:
            print(f"Error in Semantic Router: {e}")
            return Intent.GENERAL_REASONING

