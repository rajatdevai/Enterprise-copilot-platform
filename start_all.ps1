# Start All Services for Enterprise AI Platform
Write-Host "🚀 Starting all Enterprise AI Microservices..." -ForegroundColor Cyan

# Backend Node Services
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd gateway-service; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd auth-service; npm run dev"

# AI Python Services
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd ai-orchestrator; python main.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd agent-service; python main.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd embedding-service; python main.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd retrieval-service; python main.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd document-service; python main.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd streaming-service; python main.py"

# Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "✅ All services triggered. Check individual terminals for logs." -ForegroundColor Green
Write-Host "Run 'python infra/health_monitor.py' in 10 seconds to verify." -ForegroundColor Yellow
