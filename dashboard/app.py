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