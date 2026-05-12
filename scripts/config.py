import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = Path(os.environ.get("DATA_CSV", ROOT / "data" / "wdi_world_slice.csv"))
MODELS_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"

TARGET_CODE = "SP.DYN.CBRT.IN"
FEATURE_CODES = {
    "SP.DYN.TFRT.IN": "fertility_rate",
    "NY.GDP.PCAP.CD": "gdp_per_capita_usd",
    "SP.DYN.LE00.IN": "life_expectancy",
    "SP.URB.TOTL.IN.ZS": "urban_population_pct",
    "SE.XPD.TOTL.GD.ZS": "education_expenditure_pct_gdp",
    "SL.UEM.TOTL.ZS": "unemployment_pct",
    "SP.POP.GROW": "population_growth_pct",
    "SH.DYN.MORT": "under5_mortality_per1000",
}
ALL_CODES = [TARGET_CODE] + list(FEATURE_CODES.keys())

PG = {
    "host": os.environ.get("PG_HOST", "localhost"),
    "port": int(os.environ.get("PG_PORT", "5432")),
    "user": os.environ.get("PG_USER", "postgres"),
    "password": os.environ.get("PG_PASSWORD", "postgres"),
    "dbname": os.environ.get("PG_DB", "wdi_birthrate"),
}
