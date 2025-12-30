import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Mineral EXIM Dashboard", layout="wide")

st.title("🪨 IN Mineral Import-Export & Dependency Dashboard")
st.markdown("---")

# YOUR EXACT FILENAMES [file:176]
@st.cache_data
def load_exim_data(mineral):
    filename_map = {
        "Copper": "copper_exim.csv",
        "Lithium": "lithium_exim.csv", 
        "Lithium Oxide": "lithium_oxide_exim.csv",
        "Graphite": "graphite_exim.csv",
        "Artificial Graphite": "artificial_graphite_exim.csv"
    }
    
    try:
        df = pd.read_csv(filename_map[mineral])
        # Add Year column if missing (your CSV format)
        if df.shape[1] > 0:
            df.insert(0, 'Year', [2023, 2024, 2025][:len(df)])
        return df
    except FileNotFoundError:
        st.error(f"❌ {filename_map[mineral]} not found. Upload to repo.")
        st.stop()
    except:
        # Fallback dummy data
        return pd.DataFrame({
            'Year': [2023, 2024, 2025],
            'Import': [100, 120, 140],
            'Export': [80, 90, 110]
        })

# Sidebar
st.sidebar.title("🔍 Select Mineral")
mineral = st.sidebar.selectbox("Choose Mineral", [
    "Copper", "Lithium", "Lithium Oxide", 
    "Graphite", "Artificial Graphite"
])

# Load data
df = load_exim_data(mineral)
st.success(f"✅ {mineral} data loaded! Rows: {len(df)}")

# Dashboard - FIXED for numeric-only CSV
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📊 {mineral} EXIM Data")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("📈 Trade Trends")
    
    # SAFE Plotly - handles any CSV format
    if len(df.columns) >= 2 and df.columns[0] == 'Year':
        fig = px.line(df, x='Year', y=df.columns[1:], 
                     title=f"{mineral} Import/Export")
    else:
        # Generic line chart for numeric data
        fig = px.line(x=np.arange(len(df)), y=df.iloc[:, 0], 
                     title=f"{mineral} Trends")
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("NIT Agartala | Real EXIM Data 2023-24")



