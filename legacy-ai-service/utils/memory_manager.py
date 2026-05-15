import tiktoken
from typing import List, Dict

class MemoryManager:
    def __init__(self, model_name: str = "gpt-4"):
        self.encoder = tiktoken.encoding_for_model(model_name)
        self.max_context_tokens = 4000 # Configurable limit for history

    def get_token_count(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def trim_history(self, history: List[Dict], max_tokens: int = None) -> List[Dict]:
        """
        Implements a sliding window. Keeps the most recent messages that fit 
        within the token budget.
        """
        limit = max_tokens or self.max_context_tokens
        current_tokens = 0
        trimmed_history = []
        
        # Iterate backwards through history (most recent first)
        for message in reversed(history):
            content = message.get("content", "")
            tokens = self.get_token_count(content)
            
            if current_tokens + tokens > limit:
                break
            
            trimmed_history.insert(0, message)
            current_tokens += tokens
            
        return trimmed_history

    def should_compact(self, history: List[Dict], threshold: int = 10) -> bool:
        """
        Determines if the history has enough messages to warrant compaction.
        Threshold is the number of messages.
        """
        return len(history) > threshold

    def prepare_compact_chunks(self, history: List[Dict], keep_recent: int = 4) -> tuple[List[Dict], List[Dict]]:
        """
        Splits history into old messages (to be summarized) and 
        recent messages (to be kept as is).
        """
        if len(history) <= keep_recent:
            return [], history
            
        old_messages = history[:-keep_recent]
        recent_messages = history[-keep_recent:]
        return old_messages, recent_messages

    def format_for_openai(self, history: List[Dict], system_prompt: str) -> List[Dict]:
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        return messages
