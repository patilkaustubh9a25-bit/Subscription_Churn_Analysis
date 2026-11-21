
import pandas as pd

from analytics.data_loader import load_all_data
from analytics.clean_data import clean_all_data


def build_customer_period(data):

    invoices = data["invoices"].copy()
    usage = data["usage_events"].copy()
    tickets = data["support_tickets"].copy()
    cancellations = data["cancellations"].copy()

    # 1. Invoice aggregation
    invoice_summary = invoices.groupby(
        ["customer_id", "billing_period"]
    ).agg(
        invoice_count=("invoice_id", "count"),
        total_billed=("amount", lambda x: x.sum(min_count=1)),
        average_invoice_amount=("amount", "mean"),
        paid_invoices=("payment_status",
                       lambda x: (x == "paid").sum()),
        unpaid_invoices=("payment_status",
                         lambda x: (x == "unpaid").sum()),
        pending_invoices=("payment_status",
                          lambda x: (x == "pending").sum())
    ).reset_index()

    # 2. Usage aggregation
    usage["billing_period"] = (
        usage["event_date"].dt.strftime("%Y-%m")
    )

    usage_summary = usage.groupby(
        ["customer_id", "billing_period"]
    ).agg(
        total_usage_events=("event_id", "count"),
        active_days=("event_date",
                     lambda x: x.dt.date.nunique())
    ).reset_index()

    # 3. Support ticket aggregation
    tickets["billing_period"] = (
        tickets["created_at"].dt.strftime("%Y-%m")
    )

    tickets_summary = tickets.groupby(
        ["customer_id", "billing_period"]
    ).agg(
        total_tickets=("ticket_id", "count"),
        resolved_tickets=("resolved_at",
                          lambda x: x.notna().sum())
    ).reset_index()

    # 4. Cancellation aggregation
    cancellations["billing_period"] = (
        cancellations["cancellation_date"].dt.strftime("%Y-%m")
    )

    cancellation_summary = cancellations.groupby(
        ["customer_id", "billing_period"]
    ).agg(
        cancellation_count=("cancellation_id", "count")
    ).reset_index()

    # 5. Create combined customer-period keys
    customer_period_keys = pd.concat(
        [
            invoice_summary[["customer_id", "billing_period"]],
            usage_summary[["customer_id", "billing_period"]],
            tickets_summary[["customer_id", "billing_period"]],
            cancellation_summary[["customer_id", "billing_period"]]
        ],
        ignore_index=True
    ).drop_duplicates()

    # 6. Merge all summaries
    customer_period = customer_period_keys.merge(
        invoice_summary,
        on=["customer_id", "billing_period"],
        how="left"
    )

    customer_period = customer_period.merge(
        usage_summary,
        on=["customer_id", "billing_period"],
        how="left"
    )

    customer_period = customer_period.merge(
        tickets_summary,
        on=["customer_id", "billing_period"],
        how="left"
    )

    customer_period = customer_period.merge(
        cancellation_summary,
        on=["customer_id", "billing_period"],
        how="left"
    )

    # 7. Fill missing activity counts with zero
    count_columns = [
        "invoice_count",
        "paid_invoices",
        "unpaid_invoices",
        "pending_invoices",
        "total_usage_events",
        "active_days",
        "total_tickets",
        "resolved_tickets",
        "cancellation_count"
    ]

    customer_period[count_columns] = (
        customer_period[count_columns].fillna(0)
    )

    # 8. Add customer information
    customer_period = customer_period.merge(
        data["customers"][["customer_id", "name", "country"]],
        on="customer_id",
        how="left"
    )

    # 9. Sort records
    customer_period = customer_period.sort_values(
        ["customer_id", "billing_period"]
    ).reset_index(drop=True)

    # 10. Invoice amount quality checks
    print("\nINVOICE AMOUNT QUALITY CHECK")

    print(
        "Missing invoice amounts:",
        invoices["amount"].isna().sum()
    )

    print(
        "Customer-period groups with missing average:",
        invoice_summary["average_invoice_amount"].isna().sum()
    )

    print(
        "Total billed missing:",
        customer_period["total_billed"].isna().sum()
    )

    # 11. Customer-period quality checks
    print("\nCUSTOMER-PERIOD QUALITY CHECK")

    print("Total customer-period records:", len(customer_period))

    print(
        "Duplicate customer-period keys:",
        customer_period.duplicated(
            ["customer_id", "billing_period"]
        ).sum()
    )

    print(
        "Missing customer IDs:",
        customer_period["customer_id"].isna().sum()
    )

    return customer_period


if __name__ == "__main__":

    # Load and clean data
    data = load_all_data()
    data = clean_all_data(data)

    # Build customer-period dataset
    result = build_customer_period(data)

    # 12. Analyze records without invoices
    invoice_free = result[result["invoice_count"] == 0]

    print("\nCUSTOMER-PERIOD RECORDS WITHOUT INVOICES")

    print("Count:", len(invoice_free))

    print("\nActivity statistics:")

    activity_columns = [
        "total_usage_events",
        "total_tickets",
        "cancellation_count"
    ]

    print(
        invoice_free[activity_columns]
        .describe()
        .to_string()
    )

    print("\nSample records without invoices:")

    print(
        invoice_free.head(5).to_string(index=False)
    )

    # 13. Final customer-period dataset
    print("\nCUSTOMER-PERIOD DATASET")

    print("Shape:", result.shape)

    print("\nSample records:")

    print(result.head(10).to_string(index=False))

    print("\nMissing values:")

    print(result.isnull().sum().to_string())





