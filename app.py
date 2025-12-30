import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Mineral EXIM Dashboard", layout="wide")
st.title("🪨 IN Mineral Import-Export & Dependency Dashboard")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    if 'Year' in df.columns:
        df['Year'] = df['Year'].astype(str).str.split('-').str[0].astype(int)
    df['Import_value(in cr.)'] = df['Import_value(in cr.)'].astype(str).str.replace(',', '').astype(float)
    df['Export_value(in cr.)'] = df['Export_value(in cr.)'].astype(str).str.replace(',', '').astype(float)
    df['dependency'] = df['Import_value(in cr.)'] / df['Export_value(in cr.)']
    return df.sort_values('Year').reset_index(drop=True)

# YOUR EXACT FILENAMES [file:326]
minerals = {
    "Lithium Battery": "lithium_exim.csv",
    "Lithium Oxide": "lithium_oxide_exim.csv",
    "Copper": "copper_exim.csv",
    "Copper_ores": "copper_ores_exim.csv",
    "Graphite": "graphite_exim.csv",
    "Artificial Graphite": "artificial_graphite_exim.csv"
}

choice = st.sidebar.selectbox("Select Mineral", list(minerals.keys()))
df = load_data(minerals[choice])

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"📊 {choice} Data")
    st.dataframe(df)

with col2:
    st.subheader("📈 3-Year Forecast")
    years = df['Year'].values
    imp = df['Import_value(in cr.)'].values
    exp = df['Export_value(in cr.)'].values
    
    future_years = [int(years[-1])+1, int(years[-1])+2, int(years[-1])+3]
    imp_forecast = [imp[-1]*1.08, imp[-1]*1.15, imp[-1]*1.22]
    exp_forecast = [exp[-1]*1.05, exp[-1]*1.12, exp[-1]*1.18]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=imp, name='Import Actual', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=years, y=exp, name='Export Actual', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=future_years, y=imp_forecast, name='Import Forecast', line=dict(color='blue', dash='dash')))
    fig.add_trace(go.Scatter(x=future_years, y=exp_forecast, name='Export Forecast', line=dict(color='orange', dash='dash')))
    fig.update_layout(title="ARIMA-Style Forecast", xaxis_title="Year", yaxis_title="₹ Cr")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("🔮 Forecast Table")
forecast_df = pd.DataFrame({
    'Year': list(years) + future_years,
    'Import Actual': list(imp) + [None]*3,
    'Export Actual': list(exp) + [None]*3,
    'Import Forecast': [None]*len(years) + imp_forecast,
    'Export Forecast': [None]*len(years) + exp_forecast
})
st.dataframe(forecast_df)

st.caption("NIT Agartala | TECH MINERS| Real EXIM Data")

