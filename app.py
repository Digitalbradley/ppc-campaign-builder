import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_role_files():
   try:
       # Load all role CSV files
       roles = {
           'General Targeting': None,  # Will handle this case separately
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

def get_general_targeting_data(role_data):
   # Combine data from all roles for general targeting
   all_pain_points = set()
   all_value_props = set()
   
   for role_df in role_data.values():
       if role_df is not None:  # Skip the None value for General Targeting
           # Get pain points
           pain_point_cols = [col for col in role_df.columns if 'Pain_Point_' in col]
           all_pain_points.update(role_df[pain_point_cols].values.flatten())
           
           # Get value props
           value_prop_cols = [col for col in role_df.columns if 'Value_Prop_' in col]
           all_value_props.update(role_df[value_prop_cols].values.flatten())
   
   # Remove any nan values
   all_pain_points = {p for p in all_pain_points if isinstance(p, str)}
   all_value_props = {v for v in all_value_props if isinstance(v, str)}
   
   return list(all_pain_points), list(all_value_props)

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
       
       # Build Type
       build_type = st.radio(
           "What would you like to create?",
           ["Generate Ads Only", "Complete Campaign Structure"]
       )
       
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
   
   # Get appropriate data based on targeting selection
   if selected_role == 'General Targeting':
       pain_points_list, value_props_list = get_general_targeting_data(role_data)
   else:
       role_df = role_data[selected_role]
       pain_point_cols = [col for col in role_df.columns if 'Pain_Point_' in col]
       value_prop_cols = [col for col in role_df.columns if 'Value_Prop_' in col]
       pain_points_list = role_df[pain_point_cols].values.flatten()
       value_props_list = role_df[value_prop_cols].values.flatten()
       
   # Display relevant content based on selections
   st.header("Message Focus")
   
   # Pain Points Selection
   selected_pain_points = st.multiselect(
       "Select Key Pain Points to Address",
       [p for p in pain_points_list if isinstance(p, str)]
   )
   
   # Value Props Selection
   selected_value_props = st.multiselect(
       "Select Value Propositions",
       [v for v in value_props_list if isinstance(v, str)]
   )
   
   # Generate button
   if st.button("Generate Campaign"):
       st.subheader("Generated Content")
       
       # Adjust messaging based on in-market selection
       tone = "bottom-funnel" if is_in_market else "awareness"
       
       if build_type == "Generate Ads Only":
           st.subheader("Ad Variations")
           
           # Create columns for ad preview
           col1, col2 = st.columns(2)
           
           with col1:
               st.markdown("**Headlines**")
               for i, pain in enumerate(selected_pain_points[:3], 1):
                   st.write(f"Headline {i}: Solve {pain}")
               
           with col2:
               st.markdown("**Descriptions**")
               for i, prop in enumerate(selected_value_props[:2], 1):
                   st.write(f"Description {i}: {prop}")
           
           # Add download button for ads
           st.download_button(
               label="Download Ad Variations",
               data="ad variations here",
               file_name="ad_variations.csv",
               mime="text/csv"
           )
           
       else:
           st.subheader("Campaign Structure")
           if selected_role == 'General Targeting':
               st.write("Generating general campaign with broad appeal")
           else:
               st.write(f"Generating {tone} messaging for {selected_role}")
               
           st.write("Campaign Goals:", campaign_goals)
           
           # Show selected content
           if selected_pain_points:
               st.write("Selected Pain Points:", selected_pain_points)
           if selected_value_props:
               st.write("Selected Value Props:", selected_value_props)
               
           # Add download button for full campaign
           st.download_button(
               label="Download Campaign",
               data="campaign structure here",
               file_name="campaign_structure.csv",
               mime="text/csv"
           )

if __name__ == '__main__':
   main()
