import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore
import datetime

st.title("Climate Change Article Wikipedia Pageviews (2017–2022)")
st.subheader("RQ: How has engagement with climate change topics changed under different political parties in India, the US, and Brazil over a 5-year period?")

st.write("""This project uses weekly Wikipedia pageview data for climate-change–related
Wikidata topics. The data was originally from the Wikimedia DPDP dataset, then filtered by country, cleaned, 
and saved into the a file for this interactive visualization.
""")

@st.cache_data
def load_data():
    df = pd.read_csv("data/st15_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["pageviews"] = pd.to_numeric(df["pageviews"])
    return df

df = load_data()

# ---- Sidebar Inputs ----
st.sidebar.title("Select a Country for Analysis")

analysis_options = {
    "India": "India",
    "United States of America": "United States of America",
    "Brazil": "Brazil"
}

# The radio buttons control which analysis is shown on the main page
country = st.sidebar.radio(
    "Choose a country view:",
    list(analysis_options.keys()),
    format_func=lambda x: analysis_options[x] # Display the friendly name in the sidebar
)



start_date = st.sidebar.date_input("Start date", datetime.date(2017,1,1))
end_date = st.sidebar.date_input("End date", datetime.date(2023,2,5))

# creating variable out of the datetime that was put in the side bar option like in the plt.axvspan
start_date2 = pd.to_datetime(start_date)
end_date2= pd.to_datetime(end_date)

#filter for date range and country from original figure code
filter = ((df["country"] == country) &(df["date"] >= pd.to_datetime(start_date)) &(df["date"] <= pd.to_datetime(end_date)))
country_df = df[filter]

# timeseries 
timeseries = (country_df.groupby("date")["pageviews"].sum().reset_index())

timeseries["pageviews_zscore"] = zscore(timeseries["pageviews"])

#plot
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(timeseries["date"],timeseries["pageviews_zscore"])



#from notebook code
ax.axhline(y=0, color='black', linestyle='--') 
ax.set_xlabel("Year")
ax.set_ylabel("Pageviews (Z-score)")




# shading by political party
if country == "India":
    ax.set_title("Z-Score of CC Wikipedia Pageviews in India (2017-22)")
    ax.axvspan(start_date2, datetime.datetime(2019,5,30), color="orange", alpha=0.2, label="Modi (Term 1)")
    ax.axvspan(datetime.datetime(2019,5,30), end_date2, color="red", alpha=0.2, label="Modi (Term 2)")

elif country == "United States of America":
    ax.set_title("Z-Score of CC Wikipedia Pageviews in USA (2017-22)")
    ax.axvspan(start_date2, datetime.datetime(2021,1,20), color="red", alpha=0.2, label="Trump (Republican)")
    ax.axvspan(datetime.datetime(2021,1,20), end_date2, color="blue", alpha=0.2, label="Biden (Democrat)")

elif country == "Brazil":
    ax.set_title("Z-Score of CC Wikipedia Pageviews in Brazil (2017-22)")
    ax.axvspan(start_date2, datetime.datetime(2019,1,1), color="gold", alpha=0.2, label="Temer (Center-right)")
    ax.axvspan(datetime.datetime(2019,1,1), datetime.datetime(2023,1,1), color="red", alpha=0.2, label="Bolsonaro (Far-right)")
    ax.axvspan(datetime.datetime(2023,1,1), end_date2, color="green", alpha=0.3, label="Lula (Left-wing)")

ax.legend()

st.pyplot(fig)


