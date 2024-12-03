import streamlit as st
import pandas as pd

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.responses = {}
    st.session_state.view = 'wizard'  # Add view state

# Keep existing stages dictionary
stages = {
    # ... (keep existing stages)
}

def wizard_view():
    # Current wizard code goes here (most of the existing main function)
    st.title("PPC Campaign Builder - Wizard")
    # ... (rest of existing wizard code)

def dashboard_view():
    st.title("PPC Campaign Builder - Dashboard")
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Campaign Settings", "Ad Creation", "Preview"])
    
    with tab1:
        st.subheader("Campaign Settings")
        campaign_type = st.radio(
            "What would you like to create?",
            ["Ads Only", "Full Campaign"]
        )
        
        role = st.selectbox(
            "Target Role",
            ["General Campaign", "Chief Customer Officer", "VP Customer Support", 
             "Senior Director Support", "Director Customer Operations", "Head Customer Support",
             "Senior Support Manager", "Customer Support Manager", "Support Team Lead",
             "Technical Support Director", "Customer Service Director"]
        )
        
        in_market = st.checkbox("Target In-Market Audiences", 
                              help="Users actively researching Help Desk solutions")
        
        goals = st.text_area("Campaign Goals",
                           placeholder="e.g., increase free trial signups, demo requests")
    
    with tab2:
        st.subheader("Ad Creation")
        if campaign_type == "Full Campaign":
            num_adgroups = st.number_input("Number of Ad Groups", min_value=1, value=1)
            for i in range(int(num_adgroups)):
                st.text_input(f"Ad Group {i+1} Name")
                st.text_area(f"Keywords for Ad Group {i+1}", 
                           placeholder="One keyword per line")
        
        num_ads = st.number_input("Number of Ads", min_value=1, max_value=3, value=1)
        st.info("Each ad will include 15 headlines and 4 descriptions")
    
    with tab3:
        st.subheader("Preview & Generate")
        if st.button("Generate"):
            if campaign_type == "Ads Only":
                st.write("Generating ads based on:")
                st.write(f"- Role: {role}")
                st.write(f"- Audience: {'In-Market' if in_market else 'Broader Targeting'}")
                st.write(f"- Goals: {goals}")
            else:
                st.write("Generating campaign structure based on:")
                st.write(f"- Role: {role}")
                st.write(f"- Audience: {'In-Market' if in_market else 'Broader Targeting'}")
                st.write(f"- Goals: {goals}")
                st.write("- Ad Groups: [will show ad group details]")

def main():
    # Add view selector in sidebar
    with st.sidebar:
        st.title("PPC Campaign Builder")
        view = st.radio("Select View", ["Wizard", "Dashboard"])
        st.session_state.view = view.lower()
        
        if st.button("Start Over"):
            st.session_state.stage = 'welcome'
            st.session_state.responses = {}
            st.rerun()
    
    # Show selected view
    if st.session_state.view == 'wizard':
        wizard_view()
    else:
        dashboard_view()

if __name__ == '__main__':
    main()
