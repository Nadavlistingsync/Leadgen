from typing import Dict, List
import openai
from config.settings import API_SETTINGS
import json
from datetime import datetime, timedelta

class MessageGenerator:
    def __init__(self):
        openai.api_key = API_SETTINGS['openai_api_key']
        self.model = API_SETTINGS['openai_model']
        self.max_tokens = API_SETTINGS['max_tokens']

    def generate_messages(self, lead: Dict) -> Dict:
        """Generate all messages for a lead"""
        context = self._create_context(lead)
        
        messages = {
            'email_subject': self._generate_email_subject(context),
            'email_body': self._generate_email_body(context),
            'linkedin_message': self._generate_linkedin_message(context),
            'sms_message': self._generate_sms_message(context),
            'follow_ups': self._generate_follow_ups(context)
        }
        
        return messages

    def _create_context(self, lead: Dict) -> str:
        """Create context for message generation"""
        context = f"""
        Lead Information:
        - Name: {lead.get('full_name', 'N/A')}
        - Company: {lead.get('company', 'N/A')}
        - Location: {lead.get('location', 'N/A')}
        - Website: {lead.get('website', 'N/A')}
        - LinkedIn: {lead.get('linkedin', 'N/A')}
        
        Target Industry: Real Estate
        Location: {lead.get('location', 'N/A')}
        """
        return context

    def _generate_email_subject(self, context: str) -> str:
        """Generate email subject line"""
        prompt = f"""
        Based on the following lead information, generate a compelling email subject line.
        The subject should be personalized, attention-grabbing, and relevant to real estate.
        
        {context}
        
        Subject line (max 10 words):
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message.content.strip()

    def _generate_email_body(self, context: str) -> str:
        """Generate email body"""
        prompt = f"""
        Based on the following lead information, generate a personalized cold email.
        The email should be professional, concise, and focused on value proposition.
        
        {context}
        
        Email template:
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens * 2
        )
        
        return response.choices[0].message.content.strip()

    def _generate_linkedin_message(self, context: str) -> str:
        """Generate LinkedIn connection message"""
        prompt = f"""
        Based on the following lead information, generate a personalized LinkedIn connection request message.
        The message should be brief, professional, and focused on mutual value.
        
        {context}
        
        LinkedIn message (max 300 characters):
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message.content.strip()

    def _generate_sms_message(self, context: str) -> str:
        """Generate SMS message"""
        prompt = f"""
        Based on the following lead information, generate a brief SMS message.
        The message should be casual, friendly, and include a clear call-to-action.
        
        {context}
        
        SMS message (max 160 characters):
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message.content.strip()

    def _generate_follow_ups(self, context: str) -> List[Dict]:
        """Generate follow-up messages"""
        follow_ups = []
        days = [1, 3, 7, 14, 30]  # Days after initial contact
        
        for day in days:
            prompt = f"""
            Based on the following lead information, generate a follow-up message for day {day}.
            The message should reference previous contact and provide additional value.
            
            {context}
            
            Follow-up message for day {day}:
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens
            )
            
            follow_ups.append({
                'day': day,
                'message': response.choices[0].message.content.strip(),
                'scheduled_date': (datetime.now() + timedelta(days=day)).isoformat()
            })
        
        return follow_ups 