#!/bin/bash

# Installation script for Modern Socratic Method CLI
echo "Installing Modern Socratic Method CLI..."

# Check for Python 3.8+
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "Error: Python 3.8 or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

# Create virtual environment (optional)
read -p "Create a virtual environment? (y/n): " CREATE_VENV
if [[ $CREATE_VENV == "y" || $CREATE_VENV == "Y" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Virtual environment created and activated."
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install the package
echo "Installing Modern Socratic Method CLI..."
pip install -e .

# Make scripts executable
chmod +x src/socratic_cli.py
chmod +x run_example.sh

# Run tests
echo "Running tests..."
python -m unittest discover -s tests

echo ""
echo "Installation complete! You can now use the Modern Socratic Method CLI:"
echo "  - Run directly: python src/socratic_cli.py"
echo "  - Run example: ./run_example.sh"
echo "  - Run with command: socratic"
echo ""

if [[ $CREATE_VENV == "y" || $CREATE_VENV == "Y" ]]; then
    echo "Note: To use the CLI in the future, first activate the virtual environment:"
    echo "  source .venv/bin/activate"
fi