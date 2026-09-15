#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

command -v python3 >/dev/null 2>&1 || { echo "Python 3.11+ is required."; exit 1; }

if [ ! -x ".venv/bin/python" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env from .env.example. Configure your MySQL credentials before starting."
fi

echo "Setup complete. Create the database with database/schema.sql, then run ./run_linux.sh"
