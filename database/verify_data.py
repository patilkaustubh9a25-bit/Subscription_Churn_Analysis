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

with engine.connect() as connection:

    for table in tables:
        result = connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        )

        count = result.scalar()

        print(f"{table}: {count} records")