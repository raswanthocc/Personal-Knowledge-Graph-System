#!/usr/bin/env bash

echo "========================================================"
echo "Starting Personal Knowledge Graph System..."
echo "========================================================"

source env/bin/activate

echo "Starting FastAPI Backend on http://localhost:8000 ..."
python main.py &
BACKEND_PID=$!

echo "Starting React Frontend on http://localhost:3000 ..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT INT TERM

wait
