import pandas as pd


def clean_customers(df):
    df = df.copy()

    df["customer_id"] = df["customer_id"].str.strip().str.upper()
    df["email"] = df["email"].str.strip().str.lower()

    df = df.drop_duplicates(subset=["customer_id"], keep="first")

    df["signup_date"] = pd.to_datetime(
        df["signup_date"], errors="coerce"
    )

    return df


def clean_invoices(df):
    df = df.copy()

    df["customer_id"] = df["customer_id"].str.strip().str.upper()
    df["payment_status"] = (
        df["payment_status"].str.strip().str.lower()
    )

    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"], errors="coerce"
    )
    df["billing_period"] = pd.to_datetime(
    df["billing_period"],
    format="mixed",
    errors="coerce"
    ).dt.strftime("%Y-%m")

    df = df.drop_duplicates(subset=["invoice_id"], keep="first")

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Mark negative amounts as invalid
    df.loc[df["amount"] < 0, "amount"] = pd.NA

    return df


def clean_usage(df):
    df = df.copy()

    df["customer_id"] = df["customer_id"].str.strip().str.upper()

    df["event_date"] = pd.to_datetime(
        df["event_date"], errors="coerce"
    )

    return df


def clean_tickets(df):
    df = df.copy()

    df["customer_id"] = df["customer_id"].str.strip().str.upper()

    df["created_at"] = pd.to_datetime(
        df["created_at"], errors="coerce"
    )

    df["resolved_at"] = pd.to_datetime(
        df["resolved_at"], errors="coerce"
    )

    return df


def clean_cancellations(df):
    df = df.copy()

    df["customer_id"] = df["customer_id"].str.strip().str.upper()

    df["cancellation_date"] = pd.to_datetime(
        df["cancellation_date"], errors="coerce"
    )

    return df


def clean_all_data(data):

    data["customers"] = clean_customers(data["customers"])
    data["invoices"] = clean_invoices(data["invoices"])
    data["usage_events"] = clean_usage(data["usage_events"])
    data["support_tickets"] = clean_tickets(data["support_tickets"])
    data["cancellations"] = clean_cancellations(data["cancellations"])

    return data