@echo off
CALL C:\ApiPagosWEB\.venv\Scripts\activate.bat
uvicorn api.api:app --host 0.0.0.0 --port 8000