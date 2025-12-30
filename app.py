import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA

st.title("IN Mineral Import-Export & Dependency Dashboard")
st.markdown("---")

# Your data tables (from screenshot)
lithium_data = pd.DataFrame({
    'Row': [1,2,3],
    'Lithium_Import': [50,70,90],
    'Lithium_Export': [10,15,25],
    'Battery_cell_Import': [200,250,300],
    'Battery_cell_Export': [50,75,100]
})

copper_data = pd.DataFrame({
    'Row': [1,2,3],
    'Copper_Import': [100,120,140],
    'Copper_Export': [80,90,110],
    'Wire_Import': [150,170,190],
    'Wire_Export': [120,135,150]
})

# Sidebar mineral selector
mineral = st.sidebar.selectbox("Select Mineral", ["Lithium", "Copper", "Graphite"])

# Display tables
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"{mineral} Data")
    if mineral == "Lithium":
        st.dataframe(lithium_data)
    else:
        st.dataframe(copper_data)

# ARIMA Forecast chart (from screenshot)
with col2:
    st.subheader("ARIMA Forecast")
    st.line_chart({'Import': [50,70,90], 'Forecast': [95,105,115]})

st.markdown("---")
