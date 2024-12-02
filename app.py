import streamlit as st
import pandas as pd

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.responses = {}

# Define conversation flow
stages = {
    'welcome': {
        'message': "Hi! Let's create your Help Desk software campaign. What would you like to create - ads only or full campaign structure?",
        'options': ["Ads Only", "Full Campaign"],
        'next': 'target_role'
    },
    'target_role': {
        'message': "Who are we targeting? Select a role or create a general campaign.",
        'options': ["General Campaign", "Chief Customer Officer", "VP Customer Support"],
        'next': 'market_intent'
    },
    'market_intent': {
        'message': "Are you targeting users actively looking for Help Desk solutions?",
        'options': ["Yes", "No"],
        'next': 'campaign_goals'
    },
    'campaign_goals': {
        'message': "What are your main campaign goals?",
        'next': 'generate'
    }
}

def main():
    st.title("PPC Campaign Builder")
    
    current_stage = stages[st.session_state.stage]
    
    with st.chat_message("assistant"):
        st.write(current_stage['message'])
        
        if 'options' in current_stage:
            response = st.selectbox("Select:", current_stage['options'])
            if st.button("Continue"):
                st.session_state.responses[st.session_state.stage] = response
                st.session_state.stage = current_stage['next']
        else:
            response = st.text_input("Your response:")
            if st.button("Continue"):
                st.session_state.responses[st.session_state.stage] = response
                st.session_state.stage = current_stage['next']

if __name__ == '__main__':
    main()
