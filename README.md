# AI-Powered Lead Generation System

An automated system for scraping, analyzing, and reaching out to potential leads.

## Features

- Web scraping of lead information from multiple sources
- Data storage in Google Sheets
- AI-powered personalized outreach messages
- Automated follow-up system
- Dashboard for lead tracking
- Multi-channel outreach (Email, LinkedIn, SMS)

## Project Structure

```
leadgen-ai/
├── config/
│   └── settings.py
├── src/
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── base_scraper.py
│   │   ├── realtor_scraper.py
│   │   └── yelp_scraper.py
│   ├── data/
│   │   └── leads.json
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your settings in `config/settings.py`
4. Run the scraper: `python src/main.py`

## Configuration

Create a `.env` file with the following variables:
```
GOOGLE_SHEETS_CREDENTIALS=path/to/credentials.json
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Configure your target audience in `config/settings.py`
2. Run the scraper to collect leads
3. Review and approve leads in the dashboard
4. System will automatically send personalized outreach
5. Track responses and follow-ups in the dashboard

## License

MIT License 