from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd

DB_USER = "postgres"
DB_PASSWORD = quote_plus("admin@123")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "analytics"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df = pd.read_csv("data/events.csv")

# ✅ FIX: Convert to datetime
df["event_date"] = pd.to_datetime(df["event_date"])

df.to_sql("events", engine, if_exists="replace", index=False)

print("✅ Data loaded into PostgreSQL with correct date format!")