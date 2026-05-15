import httpx
import asyncio
import time
from datetime import datetime

SERVICES = {
    "Gateway Service": "http://localhost:3000/health",
    "Auth Service": "http://localhost:3001/health",
    "AI Orchestrator": "http://localhost:8001/health",
    "Agent Service": "http://localhost:8002/health",
    "Retrieval Service": "http://localhost:8003/health",
    "Embedding Service": "http://localhost:8004/health",
    "Document Service": "http://localhost:8005/health",
    "Streaming Service": "http://localhost:8006/health"
}

async def check_health():
    print(f"\n--- Health Check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, url in SERVICES.items():
            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    print(f"✅ {name:20} : UP ({resp.json().get('status', 'OK')})")
                else:
                    print(f"❌ {name:20} : DOWN (Status {resp.status_code})")
            except Exception as e:
                print(f"❌ {name:20} : UNREACHABLE")

async def main():
    print("Starting Enterprise AI Platform Health Monitor...")
    print("Note: Ensure services are running via docker-compose.")
    while True:
        await check_health()
        await asyncio.sleep(30) # Check every 30 seconds

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitor stopped.")
