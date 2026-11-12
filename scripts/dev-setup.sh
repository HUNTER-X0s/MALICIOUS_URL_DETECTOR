#!/usr/bin/env bash
# URLSentinel Local Development Setup (POSIX)
set -euo pipefail

echo "========================================="
echo "  URLSentinel Secure Development Setup   "
echo "========================================="

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment in .venv..."
    python3 -m venv .venv
fi

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "[OK] Generated .env from .env.example"
fi

echo "Installing backend dependencies in .venv..."
.venv/bin/pip install -r services/api/requirements.txt

echo "Setup complete! Run pytest with: .venv/bin/pytest services/api/tests"

