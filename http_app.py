# streamlit_app_direct.py
import streamlit as st
from urllib.parse import parse_qs

# Get request example
query_params = st.query_params.to_dict()
if 'name' in query_params:
    st.write(f"Hello, {query_params}!")

# Post request example
if 'POST' in query_params:
    st.write("POST Request detected!")
    if 'data' in st.query_params:
        st.write(f"Data: {query_params}")

st.write("Send a GET request with ?name=yourname or a POST request with ?POST&data=yourdata in the URL")
