import streamlit as st
import pandas as pd
import time

st.title("Mineral EXIM Dashboard")
with st.spinner("loading data..."):
try:
time.sleep(2)
st.success("loaded!")
except:
st.error("Data load failed")