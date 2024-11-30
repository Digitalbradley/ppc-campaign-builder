import streamlit as st
import pandas as pd

@st.cache_data
def load_and_transform_knowledge_base():
    try:
        # Load CSV files
        roles_df = pd.read_csv('roles_mapping.csv')
        features_df = pd.read_csv('features_base.csv')
        audience_df = pd.read_csv('audience_targeting.csv')
        
        # Get unique seniority levels
        seniority_cols = [col for col in roles_df.columns if 'Seniority_Level_' in col]
        seniority_levels = roles_df[seniority_cols].values.flatten().unique()
        seniority_levels = [x for x in seniority_levels if str(x) != 'nan']
        
        # Get unique departments
        dept_cols = [col for col in roles_df.columns if 'Department_' in col]
        departments = roles_df[dept_cols].values.flatten().unique()
        departments = [x for x in departments if str(x) != 'nan']
        
        # Get pain points
        pain_point_cols = [col for col in features_df.columns if 'Pain_Point_' in col]
        pain_points = features_df[pain_point_cols].values.flatten().unique()
        pain_points = [x for x in pain_points if str(x) != 'nan']
        
        # Get value propositions
        value_prop_cols = [col for col in features_df.columns if 'Value Prop_' in col]
        value_props = features_df[value_prop_cols].values.flatten().unique()
        value_props = [x for x in value_props if str(x) != 'nan']
        
        # Get business outcomes
        outcome_cols = [col for col in features_df.columns if 'Business Outcomes_' in col]
        outcomes = features_df[outcome_cols].values.flatten().unique()
        outcomes = [x for x in outcomes if str(x) != 'nan']
        
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
