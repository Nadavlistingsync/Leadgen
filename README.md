# Lead Generation AI

A comprehensive lead generation system that combines web scraping, API integration, and data analysis to identify and manage real estate leads.

## Features

- **Web Scraping**: Automatically collect leads from various sources
- **API Integration**: Access data from multiple real estate APIs
- **Dashboard**: Visualize and manage leads with an interactive dashboard
- **Meeting Scheduler**: Automatically schedule meetings with leads
- **Data Analysis**: Analyze lead quality and conversion rates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/leadgen-ai.git
cd leadgen-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

## Usage

1. Run the scrapers:
```bash
python src/run_scrapers.py
```

2. Start the dashboard:
```bash
python src/run_dashboard.py
```

## Project Structure

```
leadgen-ai/
├── src/
│   ├── scraper/
│   │   ├── base_scraper.py
│   │   ├── public_records_scraper.py
│   │   └── professional_directory_scraper.py
│   ├── utils/
│   │   ├── api_client.py
│   │   └── data_processor.py
│   ├── config/
│   │   └── settings.py
│   ├── dashboard.py
│   ├── run_scrapers.py
│   └── run_dashboard.py
├── data/
├── requirements.txt
├── .env.example
└── README.md
```

## API Keys Required

- ATTOM Data API
- Google Maps API
- SchoolDigger API
- ClimateCheck API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 