from sqlalchemy import text
from database.connection import engine

with engine.begin() as connection:
    connection.execute(text("""
        ALTER TABLE customers
        DROP CONSTRAINT IF EXISTS customers_pkey;
    """))

    connection.execute(text("""
        ALTER TABLE customers
        ADD COLUMN id SERIAL PRIMARY KEY;
    """))

print("Customers table updated successfully!")