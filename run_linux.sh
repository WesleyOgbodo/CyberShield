#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python" ]; then
  echo "Virtual environment not found. Run ./setup_linux.sh first."
  exit 1
fi

if [ ! -f ".env" ]; then
  echo ".env not found. Run ./setup_linux.sh and configure it first."
  exit 1
fi

.venv/bin/python app.py
