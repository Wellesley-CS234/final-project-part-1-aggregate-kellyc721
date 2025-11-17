import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURATION AND DATA LOADING (Run once) ---

# Set overall app configuration
st.set_page_config(
    page_title="CS 234 Class Project: Wikipedia for Climate Change", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the file paths for the student datasets

DATA_FILES = {f"st{i:02d}_df" : os.path.join('data', f"st{i:02d}_data.csv") 
              for i in range(1, 16)}


@st.cache_data
def load_all_student_data():
    """
    Loads all student CSV files into a dictionary of DataFrames using caching.
    This function ensures data is loaded only once and shared across all pages.
    """
    data_dict = {}
    
    # Check if data directory and files exist
    for key, path in DATA_FILES.items():
        if os.path.exists(path):
            try:
                data_dict[key] = pd.read_csv(path)
            except Exception as e:
                st.error(f"Error loading data from {path}: {e}")
                data_dict[key] = pd.DataFrame()
        else:
            # IMPORTANT: Display a clear warning if data is missing.
            st.warning(f"Data file not found: {path}. Please ensure 'data/' folder exists and run 'generate_data.py'.")
            data_dict[key] = pd.DataFrame()
    return data_dict


# --- 2. HOME PAGE CONTENT ---

st.title("🎓 Welcome to CS234 Wikipedia Project Page! 🎓")
st.markdown("""
### 👋 Overview

This dashboard showcases multiple independent student analyses based on the **Wikipedia DPDP dataset**.

---

### 💡 Inspiration & Data

Many of the analyses were inspired by the excellent article:

> **[Using Wikipedia Pageview Data to Investigate Public Interest in Climate Change at a Global Scale](https://dl.acm.org/doi/10.1145/3614419.3644007)**

We are incredibly grateful to the author, **Florian Meier**, for making the dataset publicly available. Some of our students used this exact data to generate new and exciting insights!

---

### ➡️ Get Started

👈 **Select an analysis from the sidebar to view a student's project!**
""")

# Initialize Session State for Data (This is available to ALL pages)
if 'student_data' not in st.session_state:
    st.session_state['student_data'] = load_all_student_data()