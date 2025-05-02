# Lead Generation Dashboard

A Streamlit-based dashboard for managing and visualizing real estate leads.

## Features

- Lead management and visualization
- Meeting scheduling
- Lead source tracking
- Interactive charts and metrics
- Meeting notes management

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/leadgen-ai.git
cd leadgen-ai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the dashboard:
```bash
streamlit run streamlit_app.py
```

## Deployment

### Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Connect your GitHub repository
5. Select the main file path: `streamlit_app.py`
6. Click "Deploy"

### Environment Variables

Create a `.streamlit/secrets.toml` file with any necessary API keys or configuration:

```toml
[api_keys]
# Add your API keys here
```

## Project Structure

```
leadgen-ai/
├── data/                  # Data directory
│   ├── sample_leads.json  # Sample leads data
│   └── meeting_notes/     # Meeting notes storage
├── src/                   # Source code
│   └── dashboard.py       # Dashboard implementation
├── requirements.txt       # Python dependencies
├── streamlit_app.py       # Main entry point
├── setup.sh              # Setup script
├── Procfile              # Heroku deployment config
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 