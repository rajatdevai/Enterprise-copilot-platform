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
