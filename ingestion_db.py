
import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine("sqlite:///vendorinventory.db")



def ingest_db(csv_path, table_name, engine):
    """Read a CSV in chunks and ingest it into the database."""

    first_chunk = True

    for chunk in pd.read_csv(csv_path, chunksize=10000):
        chunk.to_sql(
            table_name,
            con=engine,
            if_exists="replace" if first_chunk else "append",
            index=False,
            chunksize=1000
        )
        first_chunk = False


def load_raw_data():
    """Load CSV files as chunks and ingest them into the database."""

    start = time.time()

    for file in sorted(os.listdir("data")):
        if file.endswith(".csv"):
            logging.info(f"Ingesting {file} in db")

            csv_path = os.path.join("data", file)
            table_name = os.path.splitext(file)[0]

            ingest_db(csv_path, table_name, engine)

    end = time.time()
    total_time = (end - start) / 60

    logging.info(
        "==" * 50 + " Ingestion complete " + "==" * 50
    )
    logging.info(f"Total Time Taken: {total_time} minutes")


if __name__ == "__main__":
    load_raw_data()
