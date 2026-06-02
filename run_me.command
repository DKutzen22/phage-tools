#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "Project directory: $PROJECT_DIR"
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed or not on PATH."
  echo "Install Python 3 first, then run this again."
  read -p "Press Enter to close..."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
  echo "Installing/checking dependencies from requirements.txt..."
  python -m pip install -r requirements.txt
else
  echo "No requirements.txt found. Skipping dependency install."
fi

echo
read -p "Enter accession(s) or query: " USER_QUERY
read -p "Enter output directory path: " OUTPUT_DIR
read -p "Enter NCBI email (optional): " NCBI_EMAIL
read -p "Enter NCBI API key (optional): " NCBI_API_KEY

echo
echo "Running script..."
python genbank_scraper.py \
  --query "$USER_QUERY" \
  --output "$OUTPUT_DIR" \
  --email "$NCBI_EMAIL" \
  --api-key "$NCBI_API_KEY"

echo
echo "Finished."
read -p "Press Enter to close..."