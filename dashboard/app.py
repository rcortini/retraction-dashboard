import requests
import streamlit as st
import pandas as pd

API_URL = "http://api:8000"

st.set_page_config(
    page_title="Retraction Dashboard",
    layout="wide"
)

## TITLE
st.title("Retraction Dashboard yeah")

## OVERVIEW STATISTICS
@st.cache_data(ttl=10)
def fetch_overview():
    r = requests.get(f'{API_URL}/metrics/total-publications', timeout=5)
    r.raise_for_status()
    return r.json()

# initialize the containers for the overview statistics
col1, col2 = st.columns(2)

col1.metric("Total publications", fetch_overview()['total_publications'])