import pandas as pd
from sqlalchemy import text
from database.connection import engine


def load_table(table_name):
    query = text(f"SELECT * FROM {table_name}")

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    return df


def load_all_data():

    tables = [
        "customers",
        "subscription_plans",
        "invoices",
        "usage_events",
        "support_tickets",
        "cancellations"
    ]

    data = {}

    for table in tables:
        data[table] = load_table(table)
        print(f"{table}: {data[table].shape}")

    return data


if __name__ == "__main__":
    load_all_data()