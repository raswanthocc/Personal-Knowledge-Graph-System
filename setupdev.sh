#!/usr/bin/env bash
set -e

echo "========================================================"
echo "Setting up Personal Knowledge Graph System Environment..."
echo "========================================================"

echo "[1/4] Setting up Python virtual environment..."
python3 -m venv env
source env/bin/activate

echo "[2/4] Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[3/4] Applying database migrations (Alembic)..."
alembic upgrade head

echo "[3.5/4] Seeding initial test data into SQLite database..."
if [ -f seed_data.sql ]; then
    sqlite3 knowledge_graph.db < seed_data.sql
fi

echo "[4/4] Setting up React frontend..."
cd frontend
npm install
cd ..

echo "========================================================"
echo "Setup complete."
echo "Run './runapplication.sh' to start the application."
echo "========================================================"
