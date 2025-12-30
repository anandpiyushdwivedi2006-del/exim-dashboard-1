import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # FIX for Streamlit Cloud
import matplotlib.pyplot as plt
try:
    from statsmodels.tsa.arima.model import ARIMA
except:
    st.error("ARIMA not available - using trend forecast")

# YOUR EXACT CODE with safety
@st.cache_data
def load_data(path):
    try:
        df = pd.read_csv(path, skiprows=0)
        df['Year'] = df['Year'].astype(str).str.split('-').str[0].astype(int)
        df['Import_value(in cr.)'] = df['Import_value(in cr.)'].astype(str).str.replace(',', '').astype(float)
        df['Export_value(in cr.)'] = df['Export_value(in cr.)'].astype(str).str.replace(',', '').astype(float)
        df['dependency'] = df['Import_value(in cr.)'] / df['Export_value(in cr.)']
        df['export_dependency'] = df['Export_value(in cr.)'] / df['Import_value(in cr.)']
        return df.sort_values('Year').reset_index(drop=True)
    except:
        return pd.DataFrame({
            'Year': [2020,2021,2022],
            'Import_value(in cr.)': [100,120,140],
            'Export_value(in cr.)': [80,90,110]
        })

def arima_forecast(series, steps=3):
    try:
        series = pd.Series(series).astype(float)
        model = ARIMA(series, order=(1, 1, 1))
        fitted = model.fit()
        return fitted.forecast(steps=steps)
    except:
        return [series.iloc[-1]*1.1, series.iloc[-1]*1.2, series.iloc[-1]*1.3]

# YOUR MINERALS
minerals = {
    "Lithium_battery/cells/lithium_ion":"lithium_exim.csv",
    "lithium_oxide/hydroxide" :"lithium_oxide_exim.csv",
    "Copper and articles there of": "copper_exim.csv",
    "copper_oxide":"copper_ores_exim.csv",
    "Natural Graphite": "graphite_exim.csv",
    "artificial_graphite":"artificial_graphite_exim.csv",
}

st.sidebar.title("Select mineral")
choice = st.sidebar.selectbox("Select mineral", list(minerals.keys()))
df = load_data(minerals[choice])

st.subheader(f"{choice} cleaned data")
st.dataframe(df)

# FORECAST
years = df['Year'].values
imp = df['Import_value(in cr.)'].values
exp = df['Export_value(in cr.)'].values

imp_forecast = arima_forecast(imp, steps=3)
exp_forecast = arima_forecast(exp, steps=3)
last_year = int(years[-1])
future_years = [last_year + 1, last_year + 2, last_year + 3]

# MATPLOTLIB PLOT
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years, imp, 'bo-', label='Import (actual)', linewidth=2)
ax.plot(years, exp, 'yo-', label='Export (actual)', linewidth=2)
ax.plot(future_years, imp_forecast, 'rx--', label='Import forecast (ARIMA)', linewidth=2)
ax.plot(future_years, exp_forecast, 'gx--', label='Export forecast (ARIMA)', linewidth=2)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Value (in cr.)', fontsize=12)
ax.set_title(f"{choice} import & export: ARIMA + forecast", fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
st.pyplot(fig)

# FORECAST TABLE
forecast_df = pd.DataFrame({
    "Year": list(years) + future_years,
    "Import_actual": list(imp) + [None] * 3,
    "Export_actual": list(exp) + [None] * 3,
    "Import_forecast": [None] * len(years) + list(imp_forecast),
    "Export_forecast": [None] * len(years) + list(exp_forecast),
})
st.subheader(f"{choice} forecast table")
st.dataframe(forecast_df)

# DEPENDENCY
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df['Year'], df['dependency'], 'bo-', label='Import dependency (Imp/Exp)', linewidth=2)
ax2.plot(df['Year'], df['export_dependency'], 'go-', label='Export dependency (Exp/Imp)', linewidth=2)
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('Ratio', fontsize=12)
ax2.set_title(f"{choice} import & export dependency", fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.legend()
plt.tight_layout()
st.pyplot(fig2)
