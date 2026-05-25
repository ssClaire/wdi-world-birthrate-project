import json

import joblib
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.preprocessing import StandardScaler

from config import MODELS_DIR, REPORTS_DIR
from prepare_data import build_model_table

FEATURES = [
    "fertility_rate", "gdp_per_capita_usd", "log_gdp", "life_expectancy",
    "urban_population_pct", "education_expenditure_pct_gdp", "unemployment_pct",
    "population_growth_pct", "under5_mortality_per1000", "health_index", "urbanization_growth",
]


def train():
    MODELS_DIR.mkdir(exist_ok=True, parents=True)
    REPORTS_DIR.mkdir(exist_ok=True, parents=True)
    table = build_model_table()
    X = table[FEATURES].fillna(table[FEATURES].median())
    y = table["birth_rate"]
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    reg = Ridge(alpha=1.0)
    cv = min(5, len(table))
    metrics = {
        "mae": float(mean_absolute_error(y, cross_val_predict(reg, Xs, y, cv=cv))),
        "r2": float(np.mean(cross_val_score(reg, Xs, y, cv=cv, scoring="r2"))),
    }
    reg.fit(Xs, y)
    kmeans = KMeans(n_clusters=min(4, len(table)), random_state=42, n_init=10)
    table["cluster_id"] = kmeans.fit_predict(Xs[:, :6])
    table["cluster_name"] = table["cluster_id"].map({0: "A", 1: "B", 2: "C", 3: "D"})
    joblib.dump(reg, MODELS_DIR / "regressor.joblib")
    joblib.dump(scaler, MODELS_DIR / "scaler.joblib")
    (MODELS_DIR / "metadata.json").write_text(
        json.dumps({"features": FEATURES, "metrics": metrics}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    table.to_csv(REPORTS_DIR / "years_with_clusters.csv", index=False)
    print(metrics)
    return metrics


if __name__ == "__main__":
    train()
