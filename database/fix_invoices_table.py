from sqlalchemy import text
from database.connection import engine

with engine.begin() as connection:
    connection.execute(text("""
        ALTER TABLE invoices
        DROP CONSTRAINT IF EXISTS invoices_pkey;
    """))

    connection.execute(text("""
        ALTER TABLE invoices
        ADD COLUMN id SERIAL PRIMARY KEY;
    """))

print("Invoices table updated successfully!")