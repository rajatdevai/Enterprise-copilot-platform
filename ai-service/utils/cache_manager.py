import redis
import json
import hashlib
from typing import Optional, Any
import os

class CacheManager:
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        except Exception as e:
            print(f"Redis Connection Error: {e}")
            self.redis_client = None

    def _generate_key(self, query: str, context: Optional[str] = "") -> str:
        """
        Creates a unique hash for the query+context pair.
        """
        combined = f"{query}:{context}"
        return hashlib.md5(combined.encode()).hexdigest()

    def get_cached_response(self, query: str, context: Optional[str] = "") -> Optional[str]:
        if not self.redis_client: return None
        key = self._generate_key(query, context)
        return self.redis_client.get(f"cache:response:{key}")

    def set_cached_response(self, query: str, response: str, context: Optional[str] = "", ttl: int = 3600):
        if not self.redis_client: return
        key = self._generate_key(query, context)
        self.redis_client.setex(f"cache:response:{key}", ttl, response)

    def cache_session_history(self, session_id: str, history: list):
        if not self.redis_client: return
        self.redis_client.setex(f"session:history:{session_id}", 1800, json.dumps(history)) # 30 min session

cache_manager = CacheManager()
