import streamlit as st
import pandas as pd
import plotly.express as px

st.title("QiQi: East Asia Climate Views") 
st.markdown("---")

    # --- Introduction Section ---
st.header("1. Introduction and Project Goal")
st.markdown("""
        **Data Description:** This dataset contains **wikipedia pageview data on climate topics** for three East Asian countries in July 2018, 
        including date, country, and views.

        **Question:** Which **East Asian country** care the most about climate topics using pageviews data in **July 2018**?

        **Interaction:** Use the selection box below to choose a specific country and view its pageviews on climate change topics on July 2018.
    """)
st.markdown("---")

# Load the CSV into session_state if not already loaded
if 'student_data' not in st.session_state:
    st.session_state['student_data'] = {}

if 'st06_df' not in st.session_state['student_data']:
    df = pd.read_csv("data/st06_data.csv")
    st.session_state['student_data']['st06_df'] = df

st.write("Here's a snippet of the data")
st.write("First, I prepared the data by collect data for July 2018, then web scrape the articles from the web.")
st.write("Second, I clean the data to only include East Asia countries and match the QIDs from the article to the climate topics.")
st.write("Lastly, I combine the finalized cleaned dataset")

st06_df = st.session_state['student_data']['st06_df']
st.dataframe(st06_df.head())
    
    # --- Country Selection ---
c_filter = st.selectbox(
        "Select Country to Analyze (East Asia Countries Only):", 
        st06_df['country'].unique()
    )
    
    # Filter data for the selected country
c_df = st06_df[st06_df['country'] == c_filter]

if c_df.empty:
    st.info(f"No data found for the country '{c_filter}' in the dataset to analyze.")
else:
    st.subheader(f"2. Pageviews for {c_filter}")

        # --- Count Table ---
    st.markdown("**Count Table by Country:**")
    count_table = c_df['country'].value_counts().to_frame().rename(columns={'country': 'Count'})
    st.dataframe(count_table, use_container_width=True)

        # --- Daily Views Chart ---
    st.markdown("**Daily Views Chart:**")
    daily = c_df.groupby('Date', as_index=False)['views'].sum()
    fig = px.bar(
        daily,
        x='Date',
        y='views',
        title=f'Total Views per Date for {c_filter}',
        labels={'Date': 'Date', 'views': 'Total Views'},
        color='views',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Views',
        xaxis_tickangle=-45,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

import os
file_path = 'data/st06_data.csv'  # Replace with your CSV file path
file_size = os.path.getsize(file_path)
print(f"The size of {file_path} is {file_size} bytes.")