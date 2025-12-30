import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Mineral EXIM Dashboard", layout="wide")
st.title("🪨 IN Mineral Import-Export & Dependency Dashboard")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, skiprows=0)
    df['Year'] = df['Year'].astype(str).str.split('-').str[0].astype(int)
    df['Import_value(in cr.)'] = df['Import_value(in cr.)'].astype(str).str.replace(',', '').astype(float)
    df['Export_value(in cr.)'] = df['Export_value(in cr.)'].astype(str).str.replace(',', '').astype(float)
    df['dependency'] = df['Import_value(in cr.)'] / df['Export_value(in cr.)']
    df['export_dependency'] = df['Export_value(in cr.)'] / df['Import_value(in cr.)']
    return df.sort_values('Year').reset_index(drop=True)

# YOUR FILENAMES [file:176]
minerals = {
    "Lithium_battery/cells/lithium_ion": "lithium_exim.csv",
    "lithium_oxide/hydroxide": "lithium_oxide_exim.csv",
    "Copper and articles there of": "copper_exim.csv",
    "copper_oxide": "copper_ores_exim.csv",
    "Natural Graphite": "graphite_exim.csv",
    "artificial_graphite": "artificial_graphite_exim.csv",
}

choice = st.sidebar.selectbox("Select mineral", list(minerals.keys()))
df = load_data(minerals[choice])

st.subheader(f"{choice} cleaned data")
st.dataframe(df)

# SIMPLIFIED FORECAST (no ARIMA - instant load)
years = df['Year'].values
imp = df['Import_value(in cr.)'].values
exp = df['Export_value(in cr.)'].values

# Simple trend forecast
future_years = [int(years[-1])+1, int(years[-1])+2, int(years[-1])+3]
imp_trend = [imp[-1]*1.1, imp[-1]*1.2, imp[-1]*1.3]
exp_trend = [exp[-1]*1.05, exp[-1]*1.1, exp[-1]*1.15]

# PLOTLY CHART (replaces matplotlib)
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=imp, mode='lines+markers', name='Import (actual)', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=years, y=exp, mode='lines+markers', name='Export (actual)', line=dict(color='orange')))
fig.add_trace(go.Scatter(x=future_years, y=imp_trend, mode='lines+markers', name='Import forecast', line=dict(color='red', dash='dash')))
fig.add_trace(go.Scatter(x=future_years, y=exp_trend, mode='lines+markers', name='Export forecast', line=dict(color='green', dash='dash')))
fig.update_layout(title=f"{choice} import & export forecast", xaxis_title="Year", yaxis_title="Value (in cr.)")
st.plotly_chart(fig, use_container_width=True)

# FORECAST TABLE
forecast_df = pd.DataFrame({
    "Year": list(years) + future_years,
    "Import_actual": list(imp) + [None] * 3,
    "Export_actual": list(exp) + [None] * 3,
    "Import_forecast": [None] * len(years) + imp_trend,
    "Export_forecast": [None] * len(years) + exp_trend,
})
st.subheader(f"{choice} forecast table")
st.dataframe(forecast_df)

# DEPENDENCY CHART
fig2 = px.line(df, x='Year', y=['dependency', 'export_dependency'], 
               title=f"{choice} dependency ratios")
st.plotly_chart(fig2, use_container_width=True)

