import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

MODELS = ROOT / "models"
reg = joblib.load(MODELS / "regressor.joblib")
scaler = joblib.load(MODELS / "scaler.joblib")
meta = json.loads((MODELS / "metadata.json").read_text(encoding="utf-8"))

app = FastAPI()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/predict")
def predict(data: dict):
    row = {
        "fertility_rate": float(data.get("fertility_rate", 2.4)),
        "gdp_per_capita_usd": float(data.get("gdp_per_capita_usd", 11000)),
        "life_expectancy": float(data.get("life_expectancy", 73)),
        "urban_population_pct": float(data.get("urban_population_pct", 57)),
        "education_expenditure_pct_gdp": float(data.get("education_expenditure_pct_gdp", 4.2)),
        "unemployment_pct": float(data.get("unemployment_pct", 6)),
        "population_growth_pct": float(data.get("population_growth_pct", 1)),
        "under5_mortality_per1000": float(data.get("under5_mortality_per1000", 38)),
    }
    row["log_gdp"] = float(np.log1p(max(row["gdp_per_capita_usd"], 0)))
    row["health_index"] = row["life_expectancy"] - row["under5_mortality_per1000"] / 10
    row["urbanization_growth"] = row["urban_population_pct"] * (1 + row["population_growth_pct"] / 100)
    X = pd.DataFrame([row])[meta["features"]]
    birth = float(reg.predict(scaler.transform(X))[0])
    return {"birth_rate": round(birth, 2), "metrics": meta["metrics"]}
