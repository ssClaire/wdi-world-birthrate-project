from pathlib import Path

import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
API = "http://127.0.0.1:8000"

st.title("Прогноз рождаемости World")
api = st.sidebar.text_input("API", API)

fertility = st.number_input("fertility_rate", value=2.4)
gdp = st.number_input("gdp_per_capita_usd", value=11000.0)
life = st.number_input("life_expectancy", value=73.0)
urban = st.number_input("urban_population_pct", value=57.0)

if st.button("predict"):
    r = requests.post(
        f"{api.rstrip('/')}/predict",
        json={
            "fertility_rate": fertility,
            "gdp_per_capita_usd": gdp,
            "life_expectancy": life,
            "urban_population_pct": urban,
        },
    )
    st.write(r.json())

csv_path = ROOT / "reports" / "years_with_clusters.csv"
if csv_path.exists():
    df = pd.read_csv(csv_path)
    st.line_chart(df.set_index("year")[["birth_rate", "fertility_rate"]])
    st.dataframe(df)
