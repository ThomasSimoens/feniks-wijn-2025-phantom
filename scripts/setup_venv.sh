#!/bin/bash
# Setup virtual environment for the project

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/venv"

echo "Setting up virtual environment..."
echo "Project root: $PROJECT_ROOT"
echo "Virtual environment: $VENV_DIR"
echo ""

# Create virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists at $VENV_DIR"
    echo "Skipping creation..."
else
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual environment created"
fi

echo ""
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "✓ Virtual environment activated"

echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install Pillow
echo "✓ Dependencies installed"

echo ""
echo "================================"
echo "Setup complete!"
echo "================================"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate it, run:"
echo "  deactivate"
echo ""
echo "Now you can run the image scripts:"
echo "  python3 scripts/download_images.py"
echo "  python3 scripts/optimize_images.py"
echo ""
