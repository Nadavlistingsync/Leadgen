#!/bin/bash

# Create necessary directories
mkdir -p ~/.streamlit/
mkdir -p data/
mkdir -p data/meeting_notes/

# Create Streamlit credentials
echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml

# Create Streamlit config
echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
[browser]\n\
gatherUsageStats = false\n\
[theme]\n\
primaryColor = '#FF4B4B'\n\
backgroundColor = '#FFFFFF'\n\
secondaryBackgroundColor = '#F0F2F6'\n\
textColor = '#262730'\n\
font = 'sans serif'\n\
" > ~/.streamlit/config.toml

# Install requirements
pip install -r requirements.txt 