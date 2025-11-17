import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px

# The actual page content is executed here by Streamlit
st.title("🌎 Climate Articles in Spanish Language Analysis")
st.markdown("---")

# Retrieve shared data from the Home page's session state
if 'student_data' not in st.session_state or st.session_state['student_data']['st08_df'].empty:
    st.warning("Data not loaded. Please ensure the main Home Page ran successfully and the data files exist.")
else:

    df = st.session_state['student_data']['st08_df']
        
        # --- Student Introductory Section ---
    st.header("1. Introduction and Project Goal")
    st.markdown("""
            ⚙️**Data Description:** \n
            This dataset contains results from **2020-04-22 to 2020-09-14** 
            for the top 25 contries where wikipedia articles about climate change in spanish where accessed, 
            in comparison to all other languages from those respective countries. Data was extracted from
            DPDP Wikepedia files. Languages where matched by key matching the first two characters of wiki site names, and labeled as spanish
            or other languages for filtering. Then data was grouped by country and aggregated by language. Results are measure by views.
                    
            ❓**Question:**  What is the relation of **spanish articles** accessed in comparison to other languages in each country?
                    
            🖱️**Interaction:** The selection box below has the following options:\n
                    
                    (Hover over both data frames to see more detailed values of results)

                    ➡️ Language comparisons : Allows you to see the data set of spansih and Other language comparisons \n
                    ➡️ Spanish views in top 25 Countries : Allows you to see the data set of only the spanish views in the top 25 countries
    """)
    
st.markdown("---")
st.header("2. Data figures")

options=["Language Comparisons","Spanish Views in Top 25 Countries"]
selection=st.selectbox("Select a data frame",options)
    
#import and order data
data=pd.read_csv("data/st08_data.csv")
data=data.sort_values(by=['Country','views'], ascending=False)
data=data.drop('Unnamed: 0', axis=1)
#Get SD+- to order from higuest to lowest
stdv_df=data.groupby('Country')['views'].std().reset_index().rename(columns={'views':'std_views'})
sorted=stdv_df.sort_values(by='std_views',ascending=False)['Country'].tolist()

data2=data[data['language_type']=='spanish']
sorted2=data2.sort_values(by='views (log)',ascending=False)['Country'].tolist()


if selection == options[0]:
#Making plot
    st.subheader(options[0])
    #plt.figure(figsize=(20,6))

    figure= px.bar(data, x='Country',y='views (log)',color='language_type',hover_data=['views'],category_orders={"Country": sorted})
    figure.update_layout(barmode='group',xaxis_tickangle=90, height=600, width=1000)
    st.plotly_chart(figure)

    st.markdown("---")
    st.subheader("3. Data Snippet")

    st.write(data[:5])

elif selection== options[1]:
    st.subheader(options[1])

    figure= px.bar(data2, x='Country',y='views (log)',color='Country',hover_data=['views'],category_orders={"Country": sorted2})
    figure.update_layout(xaxis_tickangle=90, height=600, width=1000)

    st.plotly_chart(figure)

    st.markdown("---")
    st.subheader("3. Data Snippet")
    st.write(data2[:5])


