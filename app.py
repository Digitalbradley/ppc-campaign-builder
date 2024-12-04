import streamlit as st
import pandas as pd
from anthropic import Anthropic
import os

# Initialize Anthropic client
anthropic = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"], base_url=None)

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

stages = {
    'welcome': {
        'message': "Hi! Let's create your Help Desk software campaign. What would you like to create - ads only or full campaign structure?",
        'options': ["Ads Only", "Full Campaign"],
        'next': 'target_role'
    },
    'target_role': {
        'message': "Who are we targeting? Select a role or create a general campaign.",
        'options': [
            "General Campaign",
            "Chief Customer Officer",
            "VP Customer Support", 
            "Senior Director Support",
            "Director Customer Operations",
            "Head Customer Support",
            "Senior Support Manager",
            "Customer Support Manager",
            "Support Team Lead",
            "Technical Support Director",
            "Customer Service Director"
        ],
        'next': 'market_intent'
    },
    'market_intent': {
        'message': """Would you like to target in-market audiences?

In-Market Targeting:
✓ Users actively researching Help Desk solutions
✓ Higher purchase intent
✓ Higher CPCs but better conversion rates

Broader Targeting:
✓ Awareness campaigns
✓ Lower CPCs for testing
✓ Reach competitor audiences
✓ Build brand recognition""",
        'options': ["Yes - Target In-Market Audiences", "No - Broader Targeting"],
        'next': 'campaign_goals'
    },
    'campaign_goals': {
        'message': "What are your main campaign goals? (e.g., increase free trial signups, demo requests)",
        'next': 'generate'
    },
    'generate': {
        'message': "Here's what we'll create based on your selections:",
        'is_final': True
    }
}

def generate_ads_preview(role, is_in_market, goals):
    """Generate ad preview based on role data and AI"""
    # Load role data
    role_df = load_role_data(role)
    
    if role_df is not None:
        # Generate content using Anthropic
        ad_content = generate_ad_content(role_df, is_in_market, goals)
        
        st.subheader("Ad Preview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Headlines (15)**")
            # Parse and display headlines from AI response
            headlines = ad_content.split("Headlines:")[1].split("Descriptions:")[0].strip().split("\n")
            for i, headline in enumerate(headlines[:15], 1):
                st.text(f"{i}. {headline}")
            
        with col2:
            st.markdown("**Descriptions (4)**")
            # Parse and display descriptions from AI response
            descriptions = ad_content.split("Descriptions:")[1].strip().split("\n")
            for i, desc in enumerate(descriptions[:4], 1):
                st.text(f"{i}. {desc}")

def generate_campaign_preview(role, is_in_market, goals):
    """Generate campaign structure preview"""
    st.subheader("Campaign Structure")
    
    # Ad Groups Section
    st.markdown("**Ad Groups**")
    num_groups = st.number_input("Number of Ad Groups", 1, 10, 1)
    
    for i in range(num_groups):
        with st.expander(f"Ad Group {i+1}"):
            st.text_input("Ad Group Name", key=f"ag_name_{i}")
            st.text_area("Keywords (one per line)", key=f"keywords_{i}")

def main():
    st.title("PPC Campaign Builder")

    with st.sidebar:
        if st.button("Start Over"):
            st.session_state.stage = 'welcome'
            st.session_state.responses = {}
            st.rerun()
    
    current_stage = stages[st.session_state.stage]
    
    if st.session_state.stage != 'welcome':
        col1, col2 = st.columns([1,6])
        with col1:
            if st.button("Back"):
                stages_list = list(stages.keys())
                current_index = stages_list.index(st.session_state.stage)
                previous_stage = stages_list[current_index - 1]
                st.session_state.stage = previous_stage
                st.rerun()
    
    with st.chat_message("assistant"):
        st.write(current_stage['message'])
        
        if current_stage.get('is_final'):
            campaign_type = st.session_state.responses['welcome']
            if campaign_type == "Ads Only":
                st.write("Generating ads based on:")
                st.write(f"- Role: {st.session_state.responses['target_role']}")
                st.write(f"- Audience: {st.session_state.responses['market_intent']}")
                st.write(f"- Goals: {st.session_state.responses['campaign_goals']}")
                
                if st.button("Generate Ads"):
                    generate_ads_preview(
                        st.session_state.responses['target_role'],
                        "Yes" in st.session_state.responses['market_intent'],
                        st.session_state.responses['campaign_goals']
                    )
            else:
                st.write("Generating campaign structure based on:")
                st.write(f"- Role: {st.session_state.responses['target_role']}")
                st.write(f"- Audience: {st.session_state.responses['market_intent']}")
                st.write(f"- Goals: {st.session_state.responses['campaign_goals']}")
                
                if st.button("Generate Campaign"):
                    generate_campaign_preview(
                        st.session_state.responses['target_role'],
                        "Yes" in st.session_state.responses['market_intent'],
                        st.session_state.responses['campaign_goals']
                    )
        
        elif 'options' in current_stage:
            response = st.selectbox("Select:", current_stage['options'], key=f"select_{st.session_state.stage}")
            if st.button("Continue", key=f"continue_{st.session_state.stage}"):
                st.session_state.responses[st.session_state.stage] = response
                st.session_state.stage = current_stage['next']
                st.rerun()
        else:
            response = st.text_input("Your response:", key=f"input_{st.session_state.stage}")
            if st.button("Continue", key=f"continue_{st.session_state.stage}"):
                st.session_state.responses[st.session_state.stage] = response
                st.session_state.stage = current_stage['next']
                st.rerun()

    if st.session_state.responses:
        st.sidebar.write("Your selections:")
        for stage, response in st.session_state.responses.items():
            st.sidebar.write(f"{stage}: {response}")

if __name__ == '__main__':
    main()
