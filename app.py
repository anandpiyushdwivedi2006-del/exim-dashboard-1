import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mineral EXIM Dashboard", layout="wide")

st.title("🪨 IN Mineral Import-Export & Dependency Dashboard")
st.markdown("---")

# EXACT YOUR FILENAMES [file:176]
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
        return df
    except:
        st.error(f"❌ {filename_map[mineral]} not found")
        st.stop()

# Sidebar with YOUR exact files
st.sidebar.title("🔍 Select Mineral")
mineral = st.sidebar.selectbox("Choose Mineral", [
    "Copper", 
    "Lithium", 
    "Lithium Oxide", 
    "Graphite", 
    "Artificial Graphite"
])

# Load data
df = load_exim_data(mineral)
st.success(f"✅ {mineral} EXIM data loaded from {mineral.lower()}_exim.csv!")

# Dashboard layout (matches screenshot [file:125])
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📊 {mineral} EXIM Data")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("📈 Trade Trends")
    if len(df.columns) >= 2:
        # Auto-detect import/export columns
        fig = px.line(df, x=df.columns[0], y=df.columns[1:], 
                     title=f"{mineral} Import/Export Trends")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(df)

st.markdown("---")
st.caption("NIT Agartala Engineering Project | Real EXIM Data 2023-24")


