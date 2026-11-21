from sqlalchemy import text
from database.connection import engine


def create_tables():

    queries = [

        """
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            customer_id VARCHAR(50),
            name VARCHAR(100),
            email VARCHAR(150),
            signup_date DATE,
            country VARCHAR(50)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS subscription_plans (
            plan_id VARCHAR(50) PRIMARY KEY,
            plan_name VARCHAR(100),
            monthly_price NUMERIC(10,2),
            billing_cycle VARCHAR(30)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS invoices (
            id SERIAL PRIMARY KEY,
            invoice_id VARCHAR(50),
            customer_id VARCHAR(50),
            plan_id VARCHAR(50),
            invoice_date DATE,
            billing_period VARCHAR(30),
            amount NUMERIC(10,2),
            payment_status VARCHAR(30)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS usage_events (
            event_id VARCHAR(50) PRIMARY KEY,
            customer_id VARCHAR(50),
            event_date TIMESTAMP,
            event_type VARCHAR(100)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS support_tickets (
            ticket_id VARCHAR(50) PRIMARY KEY,
            customer_id VARCHAR(50),
            created_at TIMESTAMP,
            resolved_at TIMESTAMP,
            status VARCHAR(30),
            issue_type VARCHAR(100)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS cancellations (
            cancellation_id VARCHAR(50) PRIMARY KEY,
            customer_id VARCHAR(50),
            cancellation_date DATE,
            cancellation_reason VARCHAR(200)
        );
        """
    ]

    with engine.begin() as connection:
        for query in queries:
            connection.execute(text(query))

    print("All six database tables created successfully!")


if __name__ == "__main__":
    create_tables()