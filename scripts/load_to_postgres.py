import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import PG
from prepare_data import build_model_table


def load_tables():
    conn = psycopg2.connect(host=PG["host"], port=PG["port"], user=PG["user"], password=PG["password"], dbname="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (PG["dbname"],))
    if not cur.fetchone():
        cur.execute(f'CREATE DATABASE "{PG["dbname"]}"')
    cur.close()
    conn.close()

    table = build_model_table()
    conn = psycopg2.connect(**PG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS world_features (
            year INT PRIMARY KEY,
            birth_rate DOUBLE PRECISION,
            fertility_rate DOUBLE PRECISION,
            gdp_per_capita_usd DOUBLE PRECISION
        )
    """)
    cur.execute("TRUNCATE world_features")
    for _, row in table.iterrows():
        cur.execute(
            "INSERT INTO world_features (year, birth_rate, fertility_rate, gdp_per_capita_usd) VALUES (%s, %s, %s, %s)",
            (int(row["year"]), float(row["birth_rate"]), float(row["fertility_rate"]), float(row["gdp_per_capita_usd"])),
        )
    conn.commit()
    cur.close()
    conn.close()
    print("loaded", len(table), "rows")


if __name__ == "__main__":
    load_tables()
