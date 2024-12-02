import streamlit as st
import pandas as pd

if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.responses = {}

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
        'message': "What are your main campaign goals?",
        'next': 'generate'
    },
    'generate': {
        'message': "Great! Let's generate your campaign.",
        'next': 'complete'
    }
}

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
        
        if 'options' in current_stage:
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
