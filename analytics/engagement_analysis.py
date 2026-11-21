
import pandas as pd


def analyze_engagement(df):

    # 1. Overall engagement summary
    print("\nCUSTOMER ENGAGEMENT ANALYSIS")

    print("\nOverall statistics:")

    print(
        df[
            [
                "total_usage_events",
                "active_days",
                "total_tickets"
            ]
        ].describe().to_string()
    )

    # 2. Monthly engagement
    monthly_engagement = df.groupby(
        "billing_period"
    ).agg(
        total_customers=("customer_id", "nunique"),
        total_usage_events=("total_usage_events", "sum"),
        average_usage_events=("total_usage_events", "mean"),
        total_active_days=("active_days", "sum"),
        total_tickets=("total_tickets", "sum")
    ).reset_index()

    print("\nMONTHLY ENGAGEMENT")

    print(monthly_engagement.to_string(index=False))

    # 3. Customer engagement levels
    customer_engagement = df.groupby(
        "customer_id"
    ).agg(
        total_usage_events=("total_usage_events", "sum"),
        total_active_days=("active_days", "sum"),
        total_tickets=("total_tickets", "sum"),
        total_cancellations=("cancellation_count", "sum")
    ).reset_index()

    customer_engagement["engagement_level"] = pd.cut(
        customer_engagement["total_usage_events"],
        bins=[-1, 0, 5, float("inf")],
        labels=["Inactive", "Low", "High"]
    )

    print("\nCUSTOMER ENGAGEMENT LEVELS")

    print(
        customer_engagement["engagement_level"]
        .value_counts()
        .to_string()
    )

    # 4. Save monthly engagement
    monthly_engagement.to_csv(
        "data/monthly_engagement.csv",
        index=False
    )

    # 5. Save customer engagement
    customer_engagement.to_csv(
        "data/customer_engagement.csv",
        index=False
    )

    print("\nEngagement analysis files saved successfully!")

    return monthly_engagement, customer_engagement


if __name__ == "__main__":

    # Load saved customer-period dataset
    df = pd.read_csv("data/customer_period.csv")

    monthly_engagement, customer_engagement = (
        analyze_engagement(df)
    )

    print("\nCUSTOMER ENGAGEMENT DATASET")
    print("Monthly dataset shape:", monthly_engagement.shape)
    print("Customer dataset shape:", customer_engagement.shape)
