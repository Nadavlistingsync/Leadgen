from typing import Dict, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config.settings import EMAIL_SETTINGS, SMS_SETTINGS, LINKEDIN_SETTINGS
from datetime import datetime
import json

class OutreachManager:
    def __init__(self):
        self.email_settings = EMAIL_SETTINGS
        self.sms_settings = SMS_SETTINGS
        self.linkedin_settings = LINKEDIN_SETTINGS
        self.driver = None
        self.setup_linkedin()

    def setup_linkedin(self):
        """Setup Selenium for LinkedIn automation"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    def send_email(self, lead: Dict, message: Dict) -> bool:
        """Send email to lead"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_settings['sender_email']
            msg['To'] = lead.get('email', '')
            msg['Subject'] = message['email_subject']

            body = message['email_body']
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_settings['sender_email'], self.email_settings['sender_password'])
            server.send_message(msg)
            server.quit()

            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_sms(self, lead: Dict, message: Dict) -> bool:
        """Send SMS to lead"""
        try:
            if self.sms_settings['provider'] == 'twilio':
                client = Client(
                    self.sms_settings['twilio_account_sid'],
                    self.sms_settings['twilio_auth_token']
                )
                message = client.messages.create(
                    body=message['sms_message'],
                    from_=self.sms_settings['twilio_phone_number'],
                    to=lead.get('phone', '')
                )
                return True
            elif self.sms_settings['provider'] == 'telnyx':
                # Implement Telnyx API call
                pass
            return False
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return False

    def send_linkedin_message(self, lead: Dict, message: Dict) -> bool:
        """Send LinkedIn connection request and message"""
        try:
            # Login to LinkedIn
            self.driver.get('https://www.linkedin.com/login')
            self.driver.find_element(By.ID, 'username').send_keys(self.linkedin_settings['username'])
            self.driver.find_element(By.ID, 'password').send_keys(self.linkedin_settings['password'])
            self.driver.find_element(By.CSS_SELECTOR, '.login__form_action_container button').click()

            # Navigate to profile
            self.driver.get(lead.get('linkedin', ''))
            time.sleep(2)

            # Click connect button
            connect_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.pv-s-profile-actions--connect'))
            )
            connect_button.click()

            # Add note
            add_note_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.artdeco-button--secondary'))
            )
            add_note_button.click()

            # Enter message
            message_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'custom-message'))
            )
            message_box.send_keys(message['linkedin_message'])

            # Send connection request
            send_button = self.driver.find_element(By.CSS_SELECTOR, '.artdeco-button--primary')
            send_button.click()

            return True
        except Exception as e:
            print(f"Error sending LinkedIn message: {str(e)}")
            return False

    def schedule_follow_up(self, lead: Dict, follow_ups: List[Dict]):
        """Schedule follow-up messages"""
        try:
            # Load existing follow-ups
            try:
                with open('src/data/follow_ups.json', 'r') as f:
                    scheduled_follow_ups = json.load(f)
            except FileNotFoundError:
                scheduled_follow_ups = []

            # Add new follow-ups
            for follow_up in follow_ups:
                scheduled_follow_ups.append({
                    'lead_id': lead.get('id', ''),
                    'lead_name': lead.get('full_name', ''),
                    'lead_email': lead.get('email', ''),
                    'lead_phone': lead.get('phone', ''),
                    'lead_linkedin': lead.get('linkedin', ''),
                    'day': follow_up['day'],
                    'message': follow_up['message'],
                    'scheduled_date': follow_up['scheduled_date'],
                    'status': 'scheduled'
                })

            # Save updated follow-ups
            with open('src/data/follow_ups.json', 'w') as f:
                json.dump(scheduled_follow_ups, f, indent=4)

            return True
        except Exception as e:
            print(f"Error scheduling follow-ups: {str(e)}")
            return False

    def process_lead(self, lead: Dict, messages: Dict) -> Dict:
        """Process a lead with all outreach methods"""
        results = {
            'email_sent': False,
            'sms_sent': False,
            'linkedin_sent': False,
            'follow_ups_scheduled': False
        }

        if lead.get('email'):
            results['email_sent'] = self.send_email(lead, messages)
        
        if lead.get('phone'):
            results['sms_sent'] = self.send_sms(lead, messages)
        
        if lead.get('linkedin'):
            results['linkedin_sent'] = self.send_linkedin_message(lead, messages)
        
        results['follow_ups_scheduled'] = self.schedule_follow_up(lead, messages['follow_ups'])

        return results

    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()

    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup() 