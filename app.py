import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.markdown("""
<style>
    /* Main Container - MLC Dark Gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0c0c1a 0%, #1a1a2e 50%, #16213e 100%);
        backdrop-filter: blur(10px);
    }
    
    /* Content Padding & Glass Effect */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        background: rgba(30, 31, 43, 0.4);
        border-radius: 20px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 45px rgba(0,0,0,0.3);
    }
    
    /* Metric Cards - Neon Glow */
    .stMetric {
        background: linear-gradient(145deg, rgba(59,130,246,0.2), rgba(16,185,129,0.2));
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(59,130,246,0.3);
        box-shadow: 0 10px 30px rgba(59,130,246,0.1);
    }
    
    /* DataFrame - Modern Table */
    .stDataFrame {
        background: rgba(30,31,43,0.8);
        border-radius: 12px;
        border: 1px solid rgba(59,130,246,0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Charts - Glass Cards */
    .stPlotlyChart {
        background: rgba(30,31,43,0.6);
        border-radius: 16px;
        border: 1px solid rgba(16,185,129,0.3);
        padding: 1rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    /* Title Animation */
    h1, h2, h3 {
        background: linear-gradient(45deg, #3b82f6, #10b981, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        0% { filter: drop-shadow(0 0 5px #3b82f6); }
        100% { filter: drop-shadow(0 0 20px #10b981); }
    }
    
    /* Button Hover Effects */
    .stButton > button {
        background: linear-gradient(45deg, #3b82f6, #1e40af);
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(59,130,246,0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(59,130,246,0.5);
    }
</style>""", unsafe_allow_html=True)
st.set_page_config(page_title="Mineral EXIM Dashboard by TECH MINERS", layout="wide")
st.title("🪨 IN Mineral Import-Export & Dependency Dashboard")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    if 'Year' in df.columns:
        df['Year'] = df['Year'].astype(str).str.split('-').str[0].astype(int)
    df['Import_value(in cr.)'] = df['Import_value(in cr.)'].astype(str).str.replace(',', '').astype(float)
    df['Export_value(in cr.)'] = df['Export_value(in cr.)'].astype(str).str.replace(',', '').astype(float)
    df['dependency'] = df['Import_value(in cr.)'] / df['Export_value(in cr.)']
    df['export_dependency'] = df['Export_value(in cr.)'] / df['Import_value(in cr.)']
    return df.sort_values('Year').reset_index(drop=True)

minerals = {
    "Lithium Battery": "lithium_exim.csv",
    "Lithium Oxide": "lithium_oxide_exim.csv",
    "Copper": "copper_exim.csv",
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
    
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=years, y=imp, name='Import Actual value(in cr.)', line=dict(color='blue')))
    fig_forecast.add_trace(go.Scatter(x=years, y=exp, name='Export Actual value (in cr.)', line=dict(color='orange')))
    fig_forecast.add_trace(go.Scatter(x=future_years, y=imp_forecast, name='Import Forecast value (in cr.)', line=dict(color='blue', dash='dash')))
    fig_forecast.add_trace(go.Scatter(x=future_years, y=exp_forecast, name='Export Forecast value (in cr.)', line=dict(color='orange', dash='dash')))
    fig_forecast.update_layout(title="ARIMA-Style Forecast", xaxis_title="Year", yaxis_title="₹ Cr")
    st.plotly_chart(fig_forecast, use_container_width=True)

st.subheader("🔮 Forecast Table")
forecast_df = pd.DataFrame({
    'Year': list(years) + future_years,
    'Import Actual': list(imp) + [None]*3,
    'Export Actual': list(exp) + [None]*3,
    'Import Forecast': [None]*len(years) + imp_forecast,
    'Export Forecast': [None]*len(years) + exp_forecast
})
st.dataframe(forecast_df)

# ✅ DEPENDENCY GRAPH (Your tech.py version)
st.subheader("⚖️ Dependency Analysis")
fig_dependency = go.Figure()
fig_dependency.add_trace(go.Scatter(x=df['Year'], y=df['dependency'], 
                                   mode='lines+markers', name='Import Dependency (Imp/Exp)', 
                                   line=dict(color='blue', width=3), marker=dict(size=8)))
fig_dependency.add_trace(go.Scatter(x=df['Year'], y=df['export_dependency'], 
                                   mode='lines+markers', name='Export Dependency (Exp/Imp)', 
                                   line=dict(color='green', width=3), marker=dict(size=8)))
fig_dependency.update_layout(
    title=f"{choice} Import & Export Dependency Ratios",
    xaxis_title="Year", 
    yaxis_title="Dependency Ratio",
    template="plotly_white",
    height=400
)
st.plotly_chart(fig_dependency, use_container_width=True)

st.caption("NIT Agartala | TECH MINERS | Real EXIM Data ")




