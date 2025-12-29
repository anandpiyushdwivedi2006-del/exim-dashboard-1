import streamlit as st
import pandas as pd
import time

st.title("Mineral EXIM Dashboard")
with st.spinner("Loading data..."):
    try:
        time.sleep(2)  # Test first
        st.success("Loaded!")
    except:
        st.error("Data load failed")