import pandas as pd
from sqlalchemy import text
from database.connection import engine

tables = [
    "customers",
    "subscription_plans",
    "invoices",
    "usage_events",
    "support_tickets",
    "cancellations"
]

for table in tables:
    df = pd.read_csv(f"data/{table}.csv")

    df.to_sql(
        name=table,
        con=engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"{table}: {len(df)} records inserted")

print("\nAll datasets loaded into PostgreSQL!")