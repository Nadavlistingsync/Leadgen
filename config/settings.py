import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Scraping settings
SCRAPING_SETTINGS = {
    'max_pages_per_source': 5,
    'delay_between_requests': (1, 3),  # Random delay range in seconds
    'user_agent_rotation': True,
    'save_progress_interval': 1,  # Save after each page
}

# Target settings
TARGET_SETTINGS = {
    'location': "New York, NY",
    'industry': "real estate",
    'min_company_size': 1,
    'max_company_size': 1000,
}

# Data storage settings
STORAGE_SETTINGS = {
    'google_sheets_credentials': os.getenv('GOOGLE_SHEETS_CREDENTIALS'),
    'google_sheet_id': os.getenv('GOOGLE_SHEET_ID'),
    'local_storage_path': 'src/data',
}

# API settings
API_SETTINGS = {
    'openai_api_key': os.getenv('OPENAI_API_KEY'),
    'openai_model': 'gpt-3.5-turbo',
    'max_tokens': 150,
}

# Email settings
EMAIL_SETTINGS = {
    'sender_email': os.getenv('SENDER_EMAIL'),
    'sender_name': os.getenv('SENDER_NAME'),
    'email_template_path': 'templates/email',
}

# LinkedIn settings
LINKEDIN_SETTINGS = {
    'username': os.getenv('LINKEDIN_USERNAME'),
    'password': os.getenv('LINKEDIN_PASSWORD'),
    'message_template_path': 'templates/linkedin',
}

# SMS settings
SMS_SETTINGS = {
    'provider': 'twilio',  # or 'telnyx'
    'twilio_account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
    'twilio_auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
    'twilio_phone_number': os.getenv('TWILIO_PHONE_NUMBER'),
    'telnyx_api_key': os.getenv('TELNYX_API_KEY'),
    'telnyx_phone_number': os.getenv('TELNYX_PHONE_NUMBER'),
}

# Follow-up settings
FOLLOW_UP_SETTINGS = {
    'max_follow_ups': 5,
    'follow_up_days': [1, 3, 7, 14, 30],  # Days after initial contact
    'auto_reply_enabled': True,
    'calendly_link': os.getenv('CALENDLY_LINK'),
} 