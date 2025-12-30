
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🪨 IN Mineral Import-Export & Dependency Dashboard")
st.markdown("---")

# EXACT data from your screenshot [file:125]
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

# Sidebar selector (matches screenshot)
st.sidebar.title("Minerals")
mineral = st.sidebar.selectbox("Select Mineral", ["Lithium", "Copper", "Graphite"])

# Show tables side-by-side
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"📊 {mineral} Data")
    if mineral == "Lithium":
        st.dataframe(lithium_data)
    elif mineral == "Copper":
        st.dataframe(copper_data)
    else:
        st.dataframe(pd.DataFrame({"Graphite_Import": [30,40,50], "Graphite_Export": [20,25,30]}))

with col2:
    st.subheader("📈 ARIMA Forecast")
    forecast_data = pd.DataFrame({'Actual': [50,70,90], 'Forecast': [95,105,115]})
    fig = px.line(forecast_data, title="Import Trends")
    st.plotly_chart(fig, use_container_width=True)
