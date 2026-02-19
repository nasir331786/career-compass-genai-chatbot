#!/usr/bin/env bash
# scripts/run_local.sh
# Local development startup script for Career Compass.

set -e

export PYTHONUNBUFFERED=1

# Load environment variables from .env if present
if [ -f ".env" ]; then
  echo "[INFO] Loading environment from .env ..."
  export $(grep -v '^#' .env | xargs)
fi

# Create logs directory
mkdir -p logs

echo "[INFO] Starting Career Compass on http://localhost:8501 ..."
streamlit run app/main.py \
  --server.port 8501 \
  --server.address localhost \
  --server.headless false
