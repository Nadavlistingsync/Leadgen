import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List
import calendar

# Page configuration
st.set_page_config(
    page_title="Lead Generation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

def load_leads() -> List[Dict]:
    """Load leads from JSON files"""
    leads = []
    for file in os.listdir('data'):
        if file.endswith('.json'):
            with open(f'data/{file}', 'r') as f:
                leads.extend(json.load(f))
    return leads

def create_meeting_schedule(leads: List[Dict]) -> pd.DataFrame:
    """Create a meeting schedule from leads"""
    schedule = []
    current_time = datetime.now()
    
    for lead in leads:
        # Schedule meetings for next 7 days
        for day in range(7):
            meeting_time = current_time + timedelta(days=day)
            if meeting_time.weekday() < 5:  # Only weekdays
                schedule.append({
                    'date': meeting_time.date(),
                    'time': f"{9 + day % 8}:00",  # 9 AM to 5 PM
                    'lead_name': lead.get('full_name', 'Unknown'),
                    'company': lead.get('company', 'Unknown'),
                    'phone': lead.get('phone', ''),
                    'email': lead.get('email', ''),
                    'source': lead.get('source', 'Unknown')
                })
    
    return pd.DataFrame(schedule)

def main():
    st.title("📊 Lead Generation Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.header("Filters")
        sources = st.multiselect(
            "Select Lead Sources",
            ["Yellow Pages", "Public Records", "Professional Directories"],
            default=["Yellow Pages", "Public Records", "Professional Directories"]
        )
        
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now(), datetime.now() + timedelta(days=7))
        )
    
    # Load data
    leads = load_leads()
    if not leads:
        st.warning("No leads found. Please run the scrapers first.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(leads)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", len(df))
    with col2:
        st.metric("Unique Companies", df['company'].nunique())
    with col3:
        st.metric("Contact Rate", f"{len(df[df['email'].notna() | df['phone'].notna()]) / len(df) * 100:.1f}%")
    with col4:
        st.metric("Lead Sources", df['source'].nunique())
    
    # Charts
    st.subheader("Lead Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        # Source distribution
        source_counts = df['source'].value_counts()
        fig = px.pie(
            values=source_counts.values,
            names=source_counts.index,
            title="Leads by Source"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Company distribution
        company_counts = df['company'].value_counts().head(10)
        fig = px.bar(
            x=company_counts.index,
            y=company_counts.values,
            title="Top 10 Companies"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Meeting Schedule
    st.subheader("Meeting Schedule")
    schedule = create_meeting_schedule(leads)
    
    # Group by date
    for date, group in schedule.groupby('date'):
        st.markdown(f"### {date.strftime('%A, %B %d')}")
        for _, row in group.iterrows():
            with st.expander(f"{row['time']} - {row['lead_name']} ({row['company']})"):
                st.write(f"**Contact:** {row['phone']} | {row['email']}")
                st.write(f"**Source:** {row['source']}")
                
                # Add meeting notes
                notes = st.text_area("Meeting Notes", key=f"notes_{date}_{row['time']}")
                if st.button("Save Notes", key=f"save_{date}_{row['time']}"):
                    # Save notes to a file or database
                    st.success("Notes saved!")

if __name__ == "__main__":
    main() 