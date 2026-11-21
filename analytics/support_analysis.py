
import pandas as pd


def analyze_support(df):

    print("\nSUPPORT TICKET ANALYSIS")

    # 1. Overall support statistics
    total_tickets = df["total_tickets"].sum()
    resolved_tickets = df["resolved_tickets"].sum()

    unresolved_tickets = total_tickets - resolved_tickets

    resolution_rate = (
        resolved_tickets / total_tickets * 100
        if total_tickets > 0 else 0
    )

    print("\nOVERALL SUPPORT SUMMARY")

    print("Total tickets:", total_tickets)
    print("Resolved tickets:", resolved_tickets)
    print("Unresolved tickets:", unresolved_tickets)
    print("Resolution rate:", round(resolution_rate, 2), "%")

    # 2. Monthly support analysis
    monthly_support = df.groupby(
        "billing_period"
    ).agg(
        total_tickets=("total_tickets", "sum"),
        resolved_tickets=("resolved_tickets", "sum")
    ).reset_index()

    monthly_support["unresolved_tickets"] = (
        monthly_support["total_tickets"]
        - monthly_support["resolved_tickets"]
    )

    monthly_support["resolution_rate"] = (
        monthly_support["resolved_tickets"]
        .div(monthly_support["total_tickets"].replace(0, pd.NA))
        .mul(100)
        .fillna(0)
        .round(2)
    )

    print("\nMONTHLY SUPPORT ANALYSIS")

    print(monthly_support.to_string(index=False))

    # 3. Customer-level support analysis
    customer_support = df.groupby(
        "customer_id"
    ).agg(
        total_tickets=("total_tickets", "sum"),
        resolved_tickets=("resolved_tickets", "sum")
    ).reset_index()

    customer_support["unresolved_tickets"] = (
        customer_support["total_tickets"]
        - customer_support["resolved_tickets"]
    )

    customer_support = customer_support.sort_values(
        "total_tickets",
        ascending=False
    )

    print("\nTOP 10 CUSTOMERS BY SUPPORT TICKETS")

    print(customer_support.head(10).to_string(index=False))

    # 4. Save analysis results
    monthly_support.to_csv(
        "data/monthly_support.csv",
        index=False
    )

    customer_support.to_csv(
        "data/customer_support.csv",
        index=False
    )

    print("\nSupport analysis files saved successfully!")

    return monthly_support, customer_support


if __name__ == "__main__":

    df = pd.read_csv("data/customer_period.csv")

    monthly_support, customer_support = analyze_support(df)

    print("\nSUPPORT ANALYSIS DATASETS")

    print("Monthly support shape:", monthly_support.shape)
    print("Customer support shape:", customer_support.shape)
