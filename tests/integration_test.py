import httpx
import pytest
import asyncio

BASE_URL = "http://localhost:3000"

@pytest.mark.asyncio
async def test_auth_and_chat_flow():
    async with httpx.AsyncClient() as client:
        # 1. Register (Optional, assuming seed data exists or creating new)
        reg_resp = await client.post(f"{BASE_URL}/auth/register", json={
            "email": "test@goindigo.in",
            "password": "password123",
            "role": "operator",
            "tenant_id": "00000000-0000-0000-0000-000000000000" # Use seed ID if known
        })
        # Note: Might fail if already exists, so we just proceed to login
        
        # 2. Login
        login_resp = await client.post(f"{BASE_URL}/auth/login", json={
            "email": "test@goindigo.in",
            "password": "password123"
        })
        assert login_resp.status_code == 200
        token = login_resp.json()["token"]
        
        # 3. Chat
        chat_resp = await client.post(
            f"{BASE_URL}/ai/chat",
            json={"message": "What is the SOP for baggage delay?"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert chat_resp.status_code == 200
        assert "response" in chat_resp.json()
        print("Integration Test Passed: Auth + Chat Flow")

if __name__ == "__main__":
    asyncio.run(test_auth_and_chat_flow())
