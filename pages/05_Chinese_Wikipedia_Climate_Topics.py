import streamlit as st
import pandas as pd

# The actual page content is executed here by Streamlit
st.title("Chinese Wikipedia: Top 10 Climate Related Topics")
st.markdown("---")

# Retrieve shared data from the Home page's session state
if 'student_data' not in st.session_state or st.session_state['student_data']['st05_df'].empty:
    st.warning("Data not loaded. Please ensure the main Home Page ran successfully and the data files exist.")
else:
    df = st.session_state['student_data']['st05_df']

    # --- Student Introductory Section ---
    st.header("1. Introduction")
    st.markdown("""
        **Data Description:** This dataset contains **Chinese Wikipedia Pageviews** for the top 10 climate related topics during a small period in 2021.
        
        **Question:** What were the climate change topics from 2021-11-27 to 2022-04-21 that were the most important to Chinese Wikipedia users?
        
        **Interaction:** Use the selection box below to choose a specific climate topic and view its number of views.
    """)
    st.markdown("---")
    
    # --- Analysis Controls ---
    col_control, col_spacer = st.columns([1, 3])
    with col_control:
        # 1. Change the selectbox prompt and use the 'author' column for options
        topic_filter = st.selectbox(
            "Select Topic to Analyze:", 
            df['author'].unique()
        )

    # 2. Filter data for the selected 'author' (topic)
    topic_df = df[df['author'] == topic_filter]

    # --- Analysis Content ---
    if topic_df.empty:
        st.info(f"No data found for the topic '{topic_filter}' in the dataset to analyze.")
    else:
        # 3. Update the subheader to reflect the topic
        st.subheader(f"2. Pageview Metrics for the Topic: {topic_filter.replace('_', ' ')}")
        
        col1, col2 = st.columns(2)
        
        # Total Views Metric
        with col1:
            # Calculate and display the total views for the selected topic
            total_views = topic_df['Views'].sum()
            st.metric(
                label="Total Views Analyzed", 
                value=f"{total_views:,.0f}"
            )
            
            # Display the full row data for the selected topic (useful for single-row data)
            st.dataframe(topic_df, use_container_width=True)
            
        # Views Bar Chart (if the data has multiple rows per author/topic, e.g., daily views)
        with col2:
            # Since your example data has only one row per QID/Author, 
            # this chart will simply show the single value. 
            # If your full dataset has multiple dates/rows per author, this would show the distribution.
            
            # We can rename the 'author' column index for a cleaner chart label
            views_data = topic_df.set_index('author')['Views']
            
            st.metric(
                label="Views Count (Individual Entry)",
                value=f"{views_data.iloc[0]:,.0f}" if not views_data.empty else "N/A"
            )
            
            st.bar_chart(views_data)