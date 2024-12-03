import streamlit as st
import pandas as pd
from anthropic import Anthropic
import os

# Initialize Anthropic client
anthropic = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.responses = {}

# Load role data function
@st.cache_data
def load_role_data(role):
    try:
        filename = role.lower().replace(" ", "-") + ".csv"
        role_df = pd.read_csv(filename)
        return role_df
    except Exception as e:
        st.error(f"Error loading role data: {e}")
        return None

def generate_ad_content(role_data, is_in_market, goals):
    prompt = f"""
    Create PPC ad content based on:
    Role: {role_data['Job_Title']}
    Pain Points: {role_data['Pain_Points']}
    Value Props: {role_data['Value_Props']}
    Goals: {goals}
    Audience: {'In-Market' if is_in_market else 'Awareness'}
    
    Generate:
    - 15 headlines (30 characters max)
    - 4 descriptions (90 characters max)
    """
    
    message = anthropic.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content

[Rest of your existing stages dictionary and code...]
