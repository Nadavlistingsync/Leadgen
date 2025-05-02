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
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

def load_leads() -> List[Dict]:
    """Load leads from JSON files"""
    leads = []
    if not os.path.exists('data'):
        os.makedirs('data')
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
                    'source': lead.get('source', 'Unknown'),
                    'status': 'Scheduled'
                })
    
    return pd.DataFrame(schedule)

def save_meeting_notes(date: str, time: str, lead_name: str, notes: str):
    """Save meeting notes to a file"""
    if not os.path.exists('data/meeting_notes'):
        os.makedirs('data/meeting_notes')
    
    filename = f"data/meeting_notes/{date}_{time}_{lead_name.replace(' ', '_')}.txt"
    with open(filename, 'w') as f:
        f.write(notes)

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
        
        st.header("Actions")
        if st.button("Refresh Data"):
            st.experimental_rerun()
    
    # Load data
    leads = load_leads()
    if not leads:
        st.warning("No leads found. Please run the scrapers first.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(leads)
    
    # Filter data based on sidebar selections
    if sources:
        df = df[df['source'].isin(sources)]
    
    # Metrics
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", len(df))
    with col2:
        st.metric("Unique Companies", df['company'].nunique())
    with col3:
        contact_rate = len(df[df['email'].notna() | df['phone'].notna()]) / len(df) * 100
        st.metric("Contact Rate", f"{contact_rate:.1f}%")
    with col4:
        st.metric("Lead Sources", df['source'].nunique())
    
    # Charts
    st.subheader("📊 Lead Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        # Source distribution
        source_counts = df['source'].value_counts()
        fig = px.pie(
            values=source_counts.values,
            names=source_counts.index,
            title="Leads by Source",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Company distribution
        company_counts = df['company'].value_counts().head(10)
        fig = px.bar(
            x=company_counts.index,
            y=company_counts.values,
            title="Top 10 Companies",
            color=company_counts.values,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Lead Details
    st.subheader("👥 Lead Details")
    st.dataframe(
        df[['full_name', 'company', 'phone', 'email', 'source', 'address']],
        use_container_width=True
    )
    
    # Meeting Schedule
    st.subheader("📅 Meeting Schedule")
    schedule = create_meeting_schedule(leads)
    
    # Group by date
    for date, group in schedule.groupby('date'):
        st.markdown(f"### {date.strftime('%A, %B %d')}")
        for _, row in group.iterrows():
            with st.expander(f"{row['time']} - {row['lead_name']} ({row['company']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Contact:** {row['phone']} | {row['email']}")
                    st.write(f"**Source:** {row['source']}")
                    st.write(f"**Status:** {row['status']}")
                
                with col2:
                    # Add meeting notes
                    notes = st.text_area("Meeting Notes", key=f"notes_{date}_{row['time']}")
                    if st.button("Save Notes", key=f"save_{date}_{row['time']}"):
                        save_meeting_notes(
                            str(date),
                            row['time'],
                            row['lead_name'],
                            notes
                        )
                        st.success("Notes saved!")

if __name__ == "__main__":
    main() 