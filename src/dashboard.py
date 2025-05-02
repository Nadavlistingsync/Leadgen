import streamlit as st
import pandas as pd
from datetime import datetime
import json
import plotly.express as px
from utils.sheets_manager import SheetsManager
import os

def load_leads():
    """Load leads from Google Sheets"""
    sheets_manager = SheetsManager()
    return sheets_manager.get_all_leads()

def load_follow_ups():
    """Load scheduled follow-ups"""
    try:
        with open('src/data/follow_ups.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    st.set_page_config(page_title="Lead Generation Dashboard", layout="wide")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Leads", "Outreach", "Follow-ups"])
    
    # Load data
    leads = load_leads()
    follow_ups = load_follow_ups()
    
    if page == "Overview":
        st.title("Lead Generation Dashboard")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Leads", len(leads))
        with col2:
            new_leads = len([l for l in leads if l.get('Status') == 'New'])
            st.metric("New Leads", new_leads)
        with col3:
            contacted = len([l for l in leads if l.get('Status') == 'Contacted'])
            st.metric("Contacted", contacted)
        with col4:
            converted = len([l for l in leads if l.get('Status') == 'Converted'])
            st.metric("Converted", converted)
        
        # Charts
        st.subheader("Lead Status Distribution")
        status_counts = pd.DataFrame(leads)['Status'].value_counts()
        fig1 = px.pie(values=status_counts.values, names=status_counts.index)
        st.plotly_chart(fig1)
        
        st.subheader("Lead Source Distribution")
        source_counts = pd.DataFrame(leads)['Source'].value_counts()
        fig2 = px.bar(x=source_counts.index, y=source_counts.values)
        st.plotly_chart(fig2)
    
    elif page == "Leads":
        st.title("Leads Management")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect("Filter by Status", 
                                         options=pd.DataFrame(leads)['Status'].unique(),
                                         default=pd.DataFrame(leads)['Status'].unique())
        with col2:
            source_filter = st.multiselect("Filter by Source",
                                         options=pd.DataFrame(leads)['Source'].unique(),
                                         default=pd.DataFrame(leads)['Source'].unique())
        
        # Filtered leads table
        filtered_leads = [l for l in leads 
                         if l.get('Status') in status_filter 
                         and l.get('Source') in source_filter]
        
        st.dataframe(pd.DataFrame(filtered_leads))
    
    elif page == "Outreach":
        st.title("Outreach Management")
        
        # Outreach metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            emails_sent = len([l for l in leads if l.get('Email Sent') == 'Yes'])
            st.metric("Emails Sent", emails_sent)
        with col2:
            linkedin_sent = len([l for l in leads if l.get('LinkedIn Sent') == 'Yes'])
            st.metric("LinkedIn Messages", linkedin_sent)
        with col3:
            sms_sent = len([l for l in leads if l.get('SMS Sent') == 'Yes'])
            st.metric("SMS Sent", sms_sent)
        
        # Response rate
        st.subheader("Response Rate")
        responses = [l for l in leads if l.get('Response')]
        response_rate = len(responses) / len(leads) * 100 if leads else 0
        st.metric("Overall Response Rate", f"{response_rate:.1f}%")
    
    elif page == "Follow-ups":
        st.title("Follow-up Management")
        
        # Upcoming follow-ups
        st.subheader("Upcoming Follow-ups")
        upcoming = [f for f in follow_ups 
                   if datetime.fromisoformat(f['scheduled_date']) > datetime.now()]
        
        if upcoming:
            df = pd.DataFrame(upcoming)
            df['scheduled_date'] = pd.to_datetime(df['scheduled_date'])
            st.dataframe(df[['lead_name', 'day', 'scheduled_date', 'status']])
        else:
            st.info("No upcoming follow-ups")
        
        # Follow-up history
        st.subheader("Follow-up History")
        completed = [f for f in follow_ups 
                    if datetime.fromisoformat(f['scheduled_date']) <= datetime.now()]
        
        if completed:
            df = pd.DataFrame(completed)
            df['scheduled_date'] = pd.to_datetime(df['scheduled_date'])
            st.dataframe(df[['lead_name', 'day', 'scheduled_date', 'status']])
        else:
            st.info("No completed follow-ups")

if __name__ == "__main__":
    main() 