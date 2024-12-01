import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_role_files():
   try:
       # Load all role CSV files
       roles = {
           'Chief Customer Officer': pd.read_csv('chief-customer-officer.csv'),
           'VP Customer Support': pd.read_csv('vp-customer-support.csv'),
           'Senior Director Support': pd.read_csv('senior-director-support.csv'),
           'Director Customer Operations': pd.read_csv('director-customer-operations.csv'),
           'Head Customer Support': pd.read_csv('head-customer-support.csv'),
           'Senior Support Manager': pd.read_csv('senior-support-manager.csv'),
           'Customer Support Manager': pd.read_csv('customer-support-manager.csv'),
           'Support Team Lead': pd.read_csv('support-team-lead.csv'),
           'Technical Support Director': pd.read_csv('technical-support-director.csv'),
           'Customer Service Director': pd.read_csv('customer-service-director.csv')
       }
       return roles
   except Exception as e:
       st.error(f"Error loading role files: {e}")
       return None

def main():
   st.title("PPC Campaign Builder")
   
   # Load role data
   role_data = load_role_files()
   
   if role_data is None:
       st.error("Failed to load role data")
       return
   
   # Sidebar for main settings
   with st.sidebar:
       st.header("Campaign Settings")
       
       # Role Selection
       selected_role = st.selectbox(
           "Select Role",
           list(role_data.keys())
       )
       
       # In-Market Checkbox
       is_in_market = st.checkbox(
           "In-Market Audience",
           help="Check for bottom-funnel messaging focused on immediate solutions"
       )
   
   # Main content area
   st.header("Campaign Goals")
   
   # Campaign Goals Text Input
   campaign_goals = st.text_area(
       "Describe your campaign goals",
       placeholder="Example: Looking to increase free trial signups by targeting directors and VPs with a focus on team efficiency and cost savings"
   )
   
   # Get data for selected role
   role_df = role_data[selected_role]
   
   # Display relevant content based on selections
   st.header("Message Focus")
   
   # Pain Points Selection
   pain_points = [col for col in role_df.columns if 'Pain_Point_' in col]
   selected_pain_points = st.multiselect(
       "Select Key Pain Points to Address",
       role_df[pain_points].values.flatten()
   )
   
   # Value Props Selection
   value_props = [col for col in role_df.columns if 'Value_Prop_' in col]
   selected_value_props = st.multiselect(
       "Select Value Propositions",
       role_df[value_props].values.flatten()
   )
   
   # Generate button
   if st.button("Generate Campaign"):
       st.subheader("Generated Content")
       
       # Adjust messaging based on in-market selection
       tone = "bottom-funnel" if is_in_market else "awareness"
       
       st.write(f"Generating {tone} messaging for {selected_role}")
       st.write("Campaign Goals:", campaign_goals)
       
       # Show selected content
       if selected_pain_points:
           st.write("Selected Pain Points:", selected_pain_points)
       if selected_value_props:
           st.write("Selected Value Props:", selected_value_props)
           
       # Add download button for CSV
       st.download_button(
           label="Download Campaign",
           data="campaign data here",
           file_name="campaign_structure.csv",
           mime="text/csv"
       )

if __name__ == '__main__':
   main()
