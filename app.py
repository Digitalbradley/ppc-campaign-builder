import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_and_transform_knowledge_base():
    try:
        # Load CSV files
        roles_df = pd.read_csv('roles_mapping.csv')
        features_df = pd.read_csv('features_base.csv')
        audience_df = pd.read_csv('audience_targeting.csv')
        
        # Filter for Help Desk only
        roles_df = roles_df[roles_df['Category_Name'] == 'Help Desk']
        features_df = features_df[features_df['Category_Name'] == 'Help Desk']
        audience_df = audience_df[audience_df['Category_Name'] == 'Help Desk']
        
        # Get unique seniority levels for Help Desk
        seniority_cols = [col for col in roles_df.columns if 'Seniority_Level_' in col]
        seniority_levels = pd.Series(roles_df[seniority_cols].values.ravel()).dropna().unique()
        
        # Get unique departments for Help Desk
        dept_cols = [col for col in roles_df.columns if 'Department_' in col]
        departments = pd.Series(roles_df[dept_cols].values.ravel()).dropna().unique()
        
        # Get pain points for Help Desk
        pain_point_cols = [col for col in features_df.columns if 'Pain_Point_' in col]
        pain_points = pd.Series(features_df[pain_point_cols].values.ravel()).dropna().unique()
        
        # Get value propositions for Help Desk
        value_prop_cols = [col for col in features_df.columns if 'Value Prop_' in col]
        value_props = pd.Series(features_df[value_prop_cols].values.ravel()).dropna().unique()
        
        # Get business outcomes for Help Desk
        outcome_cols = [col for col in features_df.columns if 'Business Outcomes_' in col]
        outcomes = pd.Series(features_df[outcome_cols].values.ravel()).dropna().unique()
        
        return seniority_levels, departments, pain_points, value_props, outcomes, roles_df, features_df, audience_df
    
    except Exception as e:
        st.error(f"Error loading knowledge base: {e}")
        return None, None, None, None, None, None, None, None

def main():
    # Load transformed knowledge base data
    seniority_levels, departments, pain_points, value_props, outcomes, roles_df, features_df, audience_df = load_and_transform_knowledge_base()
    
    st.title("PPC Campaign Builder")
    
    # Sidebar for input selections
    with st.sidebar:
        st.header("Campaign Settings")
        
        # Product Selection
        product = st.selectbox(
            "Select Product",
            ["Help Desk"]
        )
        
        # Build Type
        build_type = st.radio(
            "What would you like to create?",
            ["Generate Ads Only", "Complete Campaign Structure"]
        )

    # Main content area
    st.header("Target Audience Settings")
    
    # Role Selection using actual data
    role_level = st.selectbox(
        "Select Seniority Level",
        seniority_levels
    )
    
    # Department Focus using actual data
    department = st.selectbox(
        "Select Department",
        departments
    )
    
    # Pain Points using actual data
    st.header("Message Focus")
    selected_pain_points = st.multiselect(
        "Select Key Pain Points to Address",
        pain_points
    )
    
    # Value Props using actual data
    selected_value_props = st.multiselect(
        "Select Value Propositions",
        value_props
    )
    
    # Desired Outcomes using actual data
    selected_outcomes = st.multiselect(
        "Select Target Outcomes",
        outcomes
    )
    
    # Generate button
    if st.button("Generate Campaign"):
        if build_type == "Generate Ads Only":
            st.subheader("Generated Ad Variations")
            # Add ad generation logic here
            st.write("Ad variations will appear here")
        else:
            st.subheader("Campaign Structure")
            # Add campaign structure generation logic here
            st.write("Campaign structure will appear here")
        
        # Add download button for CSV
        st.download_button(
            label="Download Campaign",
            data="campaign data here",
            file_name="campaign_structure.csv",
            mime="text/csv"
        )

if __name__ == '__main__':
    main()
