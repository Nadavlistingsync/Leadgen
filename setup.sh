#!/bin/bash

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p data/meeting_notes
mkdir -p data/leads
mkdir -p config

# Set up Streamlit configuration
echo "Setting up Streamlit configuration..."
mkdir -p .streamlit
touch .streamlit/secrets.toml

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

echo "Setup complete! You can now run the dashboard with:"
echo "streamlit run streamlit_app.py" 