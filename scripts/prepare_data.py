import numpy as np
import pandas as pd

from config import ALL_CODES, DATA_CSV, FEATURE_CODES, REPORTS_DIR, TARGET_CODE


def year_cols(columns):
    cols = []
    for c in columns:
        if " [YR" in c and c[:4].isdigit():
            cols.append(c)
    return cols


def load_world_raw(path=None):
    path = path or DATA_CSV
    df = pd.read_csv(path, low_memory=False)
    return df[df["Country Code"] == "WLD"].copy()


def melt_world(df):
    years = year_cols(df.columns)
    long = df.melt(
        id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
        value_vars=years,
        var_name="year_col",
        value_name="value",
    )
    long["year"] = long["year_col"].str.slice(0, 4).astype(int)
    long = long.drop(columns=["year_col"])
    long["value"] = pd.to_numeric(long["value"].replace("..", np.nan), errors="coerce")
    return long


def build_model_table():
    raw = load_world_raw()
    long = melt_world(raw)
    long = long[long["Series Code"].isin(ALL_CODES)]
    table = long.pivot_table(index="year", columns="Series Code", values="value", aggfunc="mean").reset_index()
    table = table.rename(columns={TARGET_CODE: "birth_rate", **FEATURE_CODES})
    table["log_gdp"] = np.log1p(table["gdp_per_capita_usd"].fillna(0).clip(lower=0))
    table["health_index"] = table["life_expectancy"] - table["under5_mortality_per1000"] / 10
    table["urbanization_growth"] = table["urban_population_pct"] * (1 + table["population_growth_pct"].fillna(0) / 100)
    return table.dropna(subset=["birth_rate"]).sort_values("year").reset_index(drop=True)


if __name__ == "__main__":
    REPORTS_DIR.mkdir(exist_ok=True, parents=True)
    table = build_model_table()
    table.to_csv(REPORTS_DIR / "world_model_table.csv", index=False)
    print(len(table), "years")
