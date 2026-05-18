from config import ALL_CODES, DATA_CSV, ROOT
from prepare_data import load_world_raw

OUT = ROOT / "data" / "wdi_world_slice.csv"


if __name__ == "__main__":
    raw = load_world_raw()
    raw[raw["Series Code"].isin(ALL_CODES)].to_csv(OUT, index=False)
    print("saved", OUT)
