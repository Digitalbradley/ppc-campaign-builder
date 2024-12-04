import streamlit as st
import pandas as pd

if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.responses = {}

@st.cache_data
def load_role_data(role):
    if role == "General Campaign":
        return pd.DataFrame({
            'Pain_Point_1': ['High support costs'],
            'Value_Prop_1': ['Reduce operational costs'],
            'Feature_1': ['Automation tools'],
            'Benefit_1': ['30% cost reduction']
        })
    try:
        filename = role.lower().replace(" ", "-") + ".csv"
        role_df = pd.read_csv(filename)
        return role_df
    except Exception as e:
        st.error(f"Error loading role data: {e}")
        return None

def generate_ads_preview(role, is_in_market, goals):
    st.subheader("Ad Preview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Headlines (15)**")
        st.text("1. Example Headline 1")
        st.text("2. Example Headline 2")
        st.text("3. Example Headline 3")
    
    with col2:
        st.markdown("**Descriptions (4)**")
        st.text("1. Example Description 1")
        st.text("2. Example Description 2")

def generate_ads_preview(role, is_in_market, goals):
    role_df = load_role_data(role)
    if role_df is not None:
        st.subheader("Ad Preview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Headlines based on role data:**")
            pain_points = [col for col in role_df.columns if 'Pain_Point_' in col]
            value_props = [col for col in role_df.columns if 'Value_Prop_' in col]
            
            # Generate headlines using pain points and value props
            for i, (pain, value) in enumerate(zip(role_df[pain_points].iloc[0], 
                                                role_df[value_props].iloc[0]), 1):
                if pd.notna(pain) and pd.notna(value):
                    st.text(f"{i}. Solve {pain} with {value}")
        
        with col2:
            st.markdown("**Descriptions based on role data:**")
            features = [col for col in role_df.columns if 'Feature_' in col]
            benefits = [col for col in role_df.columns if 'Benefit_' in col]
            
            for i, (feature, benefit) in enumerate(zip(role_df[features].iloc[0], 
                                                     role_df[benefits].iloc[0]), 1):
                if pd.notna(feature) and pd.notna(benefit):
                    st.text(f"{i}. {feature} delivers {benefit}")

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
