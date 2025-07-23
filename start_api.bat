@echo off
cd /d C:\ApiPagosWEB

REM Lanza uvicorn usando el python de tu env
"C:\Users\Administrador.ML30-SVR\miniconda3\envs\api-espacio-clientes\python.exe" -m uvicorn api.api:app --host 0.0.0.0 --port 8000 >> C:\ApiPagosWEB\api.log 2>&1