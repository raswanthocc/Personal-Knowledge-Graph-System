@echo off
echo ========================================================
echo Setting up Personal Knowledge Graph System Environment...
echo ========================================================

echo [1/4] Setting up Python virtual environment...
python -m venv env
call env\Scripts\activate

echo [2/4] Installing backend dependencies...
pip install -r requirements.txt

echo [3/4] Applying database migrations (Alembic)...
alembic upgrade head

echo [3.5/4] Seeding initial test data into SQLite database...
sqlite3 knowledge_graph.db < seed_data.sql

echo [4/4] Setting up React frontend...
cd frontend
call npm install
cd ..

echo ========================================================
echo Setup complete.
echo Run 'runapplication.bat' to start the application.
echo ========================================================
