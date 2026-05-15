import os
from openai import AsyncOpenAI
from typing import List, Optional, Dict, AsyncGenerator
from config import config

class OpenAIEngine:
    def __init__(self):
        # API key should be in environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = "gpt-4o" # default to flagship multimodal model

    async def generate_stream(
        self, 
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> AsyncGenerator[str, None]:
        """
        Generates a stream of responses from OpenAI.
        """
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error in AI stream: {str(e)}"

    async def summarize(self, messages: List[Dict]) -> str:
        """
        Summarizes a conversation fragment using a cost-effective model.
        """
        if not messages:
            return ""
            
        summary_prompt = "Summarize the following conversation fragment concisely, focusing on key facts and user intent. Keep the summary under 150 words."
        
        # Prepare content for summarization
        conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini", # Use mini for efficiency
                messages=[
                    {"role": "system", "content": summary_prompt},
                    {"role": "user", "content": conversation_text}
                ],
                temperature=0.3,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Summarization error: {e}")
            return "History summarized."
