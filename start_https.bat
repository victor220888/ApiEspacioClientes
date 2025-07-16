@echo off
CALL C:\ApiPagosWEB\.venv\Scripts\activate.bat
uvicorn api.api:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips="192.198.13.202, 192.168.3.21"
