import streamlit as st
import pandas as pd

# Initialize session state
if 'stage' not in st.session_state:
   st.session_state.stage = 'welcome'
   st.session_state.responses = {}

# Wizard stages definition
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
   """Generate ad preview based on selections"""
   st.subheader("Ad Preview")
   
   col1, col2 = st.columns(2)
   with col1:
       st.markdown("**Headlines (15)**")
       st.text("1. Transform Your Help Desk Today")
       st.text("2. Streamline Customer Support")
       st.text("3. Free Trial Available")
       
   with col2:
       st.markdown("**Descriptions (4)**")
       st.text("1. Efficient support solution for...")
       st.text("2. Scale your support operations...")

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

   # Sidebar with reset button
   with st.sidebar:
       if st.button("Start Over"):
           st.session_state.stage = 'welcome'
           st.session_state.responses = {}
           st.rerun()
   
   current_stage = stages[st.session_state.stage]
   
   # Back button
   if st.session_state.stage != 'welcome':
       col1, col2 = st.columns([1,6])
       with col1:
           if st.button("Back"):
               stages_list = list(stages.keys())
               current_index = stages_list.index(st.session_state.stage)
               previous_stage = stages_list[current_index - 1]
               st.session_state.stage = previous_stage
               st.rerun()
   
   # Main content
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

   # Display selections in sidebar
   if st.session_state.responses:
       st.sidebar.write("Your selections:")
       for stage, response in st.session_state.responses.items():
           st.sidebar.write(f"{stage}: {response}")

if __name__ == '__main__':
   main()
