import streamlit as st
import pandas as pd

def main():
    st.title("PPC Campaign Builder")
    
    # Product Selection
    product = st.selectbox(
        "Select Product",
        ["Help Desk"]
    )
    
    # Role Selection
    roles = st.multiselect(
        "Select Target Roles",
        ["Director", "VP", "C-Level", "Manager"]
    )
    
    # Campaign Type
    build_type = st.radio(
        "What would you like to create?",
        ["Generate Ads Only", "Complete Campaign Structure"]
    )

if __name__ == '__main__':
    main()