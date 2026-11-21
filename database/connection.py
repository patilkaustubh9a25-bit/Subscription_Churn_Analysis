import os
import streamlit as st

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = st.secrets.get("DATABASE_URL")

DATABASE_URL = DATABASE_URL.replace(
    "postgresql://",
    "postgresql+psycopg2://",
    1
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT version();")
            )
            print("Connected to Neon PostgreSQL!")
            print(result.fetchone()[0])
            return True

    except Exception as e:
        print("Database connection failed:", e)
        return False