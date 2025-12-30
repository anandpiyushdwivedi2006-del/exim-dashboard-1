
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(page_title="Mineral EXIM Dashboard", layout="wide")
st.title("IN Mineral Import-Export & Dependency Dashboard")

@st.cache_data
def load_data(path):
    # change skiprows if your file has 2 header lines
    df = pd.read_csv(path, skiprows=0)

    # Year like "2017-2018" → take "2017" then int
    df['Year'] = (
        df['Year'].astype(str).str.split('-').str[0].astype(int)
    )

    # use exact column names from your CSV
    df['Import_value(in cr.)'] = (
        df['Import_value(in cr.)'].astype(str).str.replace(',', '')
    ).astype(float)

    df['Export_value(in cr.)'] = (
        df['Export_value(in cr.)'].astype(str).str.replace(',', '')
    ).astype(float)

    # dependency metrics
    df['dependency'] = df['Import_value(in cr.)'] / df['Export_value(in cr.)']
    df['export_dependency'] = df['Export_value(in cr.)'] / df['Import_value(in cr.)']
    df=df.sort_values('Year').reset_index(drop=True)

    return df


def arima_forecast(series, steps=3):
    series = pd.Series(series).astype(float)
    model = ARIMA(series, order=(1, 1, 1))
    fitted = model.fit()
    forecast = fitted.forecast(steps=steps)
    return forecast


# -------- paths to your CSVs (put correct filenames here) --------
minerals = {
    "Lithium_battery/cells/lithium_ion":"lithium_exim.csv",
     "lithium_oxide/hydroxide" :"lithium_oxide_exim.csv",
    "Copper and articles there of": "copper_exim1.csv",
    "copper_oxide":"copper_ores_exim.csv",
    " Natural Graphite": "graphite_exim.csv",
    "artificial_graphite":"artificial_graphite_exim.csv",
}

choice = st.sidebar.selectbox("Select mineral", list(minerals.keys()))
df = load_data(minerals[choice])

st.subheader(f"{choice} cleaned data")
st.dataframe(df)

# -------- history + ARIMA + forecast table --------
years = df['Year'].values
imp = df['Import_value(in cr.)'].values
exp = df['Export_value(in cr.)'].values

# 3‑year ARIMA forecast
imp_forecast = arima_forecast(imp, steps=3)
exp_forecast = arima_forecast(exp, steps=3)

last_year = int(years[-1])
future_years = [last_year + 1, last_year + 2, last_year + 3]

# plot actual + forecast
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(years, imp, 'bo-', label='Import (actual)')
ax.plot(years, exp, 'yo-', label='Export (actual)')
ax.plot(future_years, imp_forecast, 'rx--', label='Import forecast (ARIMA)')
ax.plot(future_years, exp_forecast, 'gx--', label='Export forecast (ARIMA)')
ax.set_xlabel('Year')
ax.set_ylabel('Value (in cr.)')
ax.set_title(f"{choice} import & export: ARIMA + forecast")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# forecast table
forecast_df = pd.DataFrame({
    "Year": list(years) + future_years,
    "Import_actual": list(imp) + [None] * len(future_years),
    "Export_actual": list(exp) + [None] * len(future_years),
    "Import_forecast": [None] * len(years) + list(imp_forecast),
    "Export_forecast": [None] * len(years) + list(exp_forecast),
})

st.subheader(f"{choice} forecast table")
st.dataframe(forecast_df)
# ---------- Dependency plots ----------
fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.plot(df['Year'], df['dependency'], marker='o',
         label='Import dependency (Imp/Exp)')
ax2.plot(df['Year'], df['export_dependency'], marker='s',
         label='Export dependency (Exp/Imp)')
ax2.set_xlabel('Year')
ax2.set_ylabel('Ratio')
ax2.set_title(f"{choice} import & export dependency")
ax2.grid(True)
ax2.legend()
st.pyplot(fig2)


