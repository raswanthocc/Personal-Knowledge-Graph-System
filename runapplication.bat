@echo off
echo ========================================================
echo Starting Personal Knowledge Graph System...
echo ========================================================

echo Starting FastAPI Backend on http://localhost:8000 ...
call env\Scripts\activate
start "FastAPI Backend" cmd /k "python main.py"

echo Starting React Frontend on http://localhost:3000 ...
cd frontend
call npm start
