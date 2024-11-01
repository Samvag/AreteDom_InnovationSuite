import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import graphviz as graphviz
from datetime import datetime, timedelta

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = {
        "Win Growth Strategy": {},
        "Production Health Check": pd.DataFrame(),
        "Innovation Analyzer": {},
        "Design Thinking": {}
    }

# App Title
st.title("Unified Application for Innovation, Strategy, and Health Check")

# Sidebar Navigation
st.sidebar.title("Navigate")
selected_step = st.sidebar.radio("Select Step", [
    "Win Growth Strategy",
    "Production Health Check",
    "Innovation Analyzer",
    "Design Thinking",
    "Overview"
])

# Step 1: Win Growth Strategy Tool
if selected_step == "Win Growth Strategy":
    st.header("Win Growth Strategy Tool")
    st.write("Define OKRs and Strategic Mapping.")

    # Select section for OKRs
    levels = ["Corporate", "Business Unit", "Plant"]
    selected_section = st.selectbox("Select Level", levels)

    # Editable OKRs Section
    def display_okrs():
        st.subheader(f"OKRs for {selected_section}")
        num_okrs = st.number_input(f"Number of OKRs for {selected_section}", min_value=1, max_value=10, value=3)
        okrs = []
        for i in range(num_okrs):
            objective = st.text_input(f"Objective {i+1}:", value=f"Enter Objective {i+1}")
            key_result = st.text_input(f"Key Result {i+1}:", value=f"Enter Key Result {i+1}")
            progress = st.slider(f"Progress for Objective {i+1}", 0, 100, 50)
            okrs.append({"Objective": objective, "Key Result": key_result, "Progress": progress})

        okrs_df = pd.DataFrame(okrs)
        st.write("Current OKRs:")
        st.dataframe(okrs_df)

        # Save button
        if st.button("Save OKRs"):
            st.session_state.data["Win Growth Strategy"][selected_section] = okrs_df
            st.success(f"OKRs for {selected_section} saved successfully!")

    # Display OKRs
    display_okrs()

# Step 2: Production Health Check
elif selected_step == "Production Health Check":
    st.header("Production Health Check")
    st.write("Track production metrics and health status.")

    # Define metrics data
    default_metrics_data = {
        'Metric': ['Production Output', 'Production Costs', 'Raw Material Turnover', 'Production Waste (kg)', 'Energy Consumption (kWh)'],
        'Target': [10000, 50000, 1000, 50, 2000],
        'Actual': [9500, 52000, 1100, 60, 2100]
    }
    df = pd.DataFrame(default_metrics_data)

    # Editable Targets and Actuals
    st.write("Edit Target Metrics and Update Actuals")
    for index, row in df.iterrows():
        target_value = st.number_input(f"Set Target for {row['Metric']}", value=row['Target'], key=f"target_{index}")
        actual_value = st.slider(f"Actual {row['Metric']}", 0, 20000, int(row['Actual']), step=100, key=f"actual_{index}")
        df.at[index, 'Target'] = target_value
        df.at[index, 'Actual'] = actual_value

    st.dataframe(df)
    
    # Save button
    if st.button("Save Production Health Data"):
        st.session_state.data["Production Health Check"] = df
        st.success("Production Health Check data saved successfully!")

# Step 3: Innovation Analyzer
elif selected_step == "Innovation Analyzer":
    st.header("Innovation Analyzer")
    st.write("Evaluate and analyze innovation opportunities.")

    # Sidebar tool selector
    innovation_ideas = [f"Innovation {i}" for i in range(1, 13)]
    selected_innovation = st.selectbox("Select Innovation Idea", innovation_ideas)
    
    # Initialize innovation data
    if selected_innovation not in st.session_state.data["Innovation Analyzer"]:
        st.session_state.data["Innovation Analyzer"][selected_innovation] = {
            'Innovation Title': '',
            'Innovation Description': '',
            'Market Share Before': 0.0,
            'Market Share After': 0.0,
            'Sales Before': 0.0,
            'Sales After': 0.0,
            'Gross Profit Before': 0.0,
            'Gross Profit After': 0.0,
            'Net Profit Before': 0.0,
            'Net Profit After': 0.0
        }

    # Input fields for innovation analysis
    data = st.session_state.data["Innovation Analyzer"][selected_innovation]
    data['Innovation Title'] = st.text_input("Innovation Title", value=data['Innovation Title'])
    data['Innovation Description'] = st.text_area("Innovation Description", value=data['Innovation Description'])
    data['Market Share Before'] = st.number_input("Market Share Before (%)", value=data['Market Share Before'])
    data['Market Share After'] = st.number_input("Market Share After (%)", value=data['Market Share After'])
    data['Sales Before'] = st.number_input("Sales Before Innovation", value=data['Sales Before'])
    data['Sales After'] = st.number_input("Sales After Innovation", value=data['Sales After'])
    data['Gross Profit Before'] = st.number_input("Gross Profit Before Innovation", value=data['Gross Profit Before'])
    data['Gross Profit After'] = st.number_input("Gross Profit After Innovation", value=data['Gross Profit After'])
    data['Net Profit Before'] = st.number_input("Net Profit Before Innovation", value=data['Net Profit Before'])
    data['Net Profit After'] = st.number_input("Net Profit After Innovation", value=data['Net Profit After'])

    # Save button for innovation
    if st.button("Save Innovation Data"):
        st.session_state.data["Innovation Analyzer"][selected_innovation] = data
        st.success("Innovation data saved successfully!")

# Step 4: Design Thinking Tool
elif selected_step == "Design Thinking":
    st.header("Design Thinking Tool")
    st.write("Utilize design thinking methodology to refine ideas.")

    steps = ["Challenge Identification", "Ideation", "Converging", "Prototyping", "Iterating"]
    status_options = ["Not Started", "In Progress", "Completed"]
    
    # Select or add a challenge
    if 'challenges' not in st.session_state:
        st.session_state.challenges = []

    # Add new challenge
    if st.button("Add New Challenge"):
        title = st.text_input("Challenge Title")
        team = st.text_input("Team Name")
        description = st.text_area("Challenge Description")
        
        if title and team and description:
            challenge = {
                'title': title,
                'team': team,
                'description': description,
                'progress': {step: {'status': 'Not Started', 'description': ''} for step in steps}
            }
            st.session_state.challenges.append(challenge)
            st.success("Challenge added successfully!")
        else:
            st.warning("Please fill in all fields.")

    # Display and update challenges
    if st.session_state.challenges:
        selected_challenge = st.selectbox("Select Challenge", st.session_state.challenges, format_func=lambda x: x['title'])
        st.subheader(f"Challenge: {selected_challenge['title']} (Team: {selected_challenge['team']})")
        st.write(f"Description: {selected_challenge['description']}")

        for step in steps:
            st.write(f"### {step}")
            status = st.selectbox(f"Status for {step}", status_options, index=status_options.index(selected_challenge['progress'][step]['status']))
            description = st.text_area(f"Description for {step}", value=selected_challenge['progress'][step]['description'])
            
            if st.button(f"Save {step} Progress"):
                selected_challenge['progress'][step]['status'] = status
                selected_challenge['progress'][step]['description'] = description
                st.success(f"Progress for {step} saved successfully!")

# Overview Section
elif selected_step == "Overview":
    st.header("Project Overview")
    
    # Display all data from each tool
    for tool, data in st.session_state.data.items():
        st.subheader(tool)
        
        if tool == "Win Growth Strategy":
            for level, df in data.items():
                st.write(f"Level: {level}")
                st.dataframe(df)
        
        elif tool == "Production Health Check":
            st.dataframe(data)
        
        elif tool == "Innovation Analyzer":
            for innovation, details in data.items():
                st.write(f"Innovation: {innovation}")
                st.write(details)
        
        elif tool == "Design Thinking":
            if st.session_state.challenges:
                for challenge in st.session_state.challenges:
                    st.write(f"Challenge: {challenge['title']}")
                    st.write(f"Team: {challenge['team']}")
                    for step, progress in challenge['progress'].items():
                        st.write(f"{step}: {progress['status']}")
                        st.write(f"Description: {progress['description']}")

# Download options for each data type
st.sidebar.subheader("Download Data")
if not st.session_state.data["Production Health Check"].empty:
    csv_data = st.session_state.data["Production Health Check"].to_csv(index=False)
    st.sidebar.download_button("Download Production Data", data=csv_data, file_name="production_data.csv", mime="text/csv")

# Save and run this as `unified_app.py`. Push it to GitHub and deploy on Streamlit for full functionality.
