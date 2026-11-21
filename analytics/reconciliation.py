import pandas as pd


def check_customer_reconciliation(data):

    customers = set(data["customers"]["customer_id"].dropna())

    tables = [
        "invoices",
        "usage_events",
        "support_tickets",
        "cancellations"
    ]

    results = []

    for table in tables:

        df = data[table].copy()

        df["customer_id"] = (
            df["customer_id"].astype("string").str.strip().str.upper()
        )

        unmatched = df[
            ~df["customer_id"].isin(customers)
        ]

        results.append({
            "Dataset": table,
            "Total Records": len(df),
            "Matched Records": len(df) - len(unmatched),
            "Unmatched Records": len(unmatched),
            "Unmatched Customer IDs": unmatched["customer_id"].nunique()
        })

    return pd.DataFrame(results)


if __name__ == "__main__":

    from analytics.data_loader import load_all_data
    from analytics.clean_data import clean_all_data

    data = load_all_data()
    data = clean_all_data(data)

    result = check_customer_reconciliation(data)

    print("\nCUSTOMER RECONCILIATION REPORT")
    print(result.to_string(index=False))