
import pandas as pd


def analyze_churn_risk():

    print("\nCUSTOMER CHURN RISK ANALYSIS")

    # Load analysis datasets
    engagement_df = pd.read_csv("data/customer_engagement.csv")
    support_df = pd.read_csv("data/customer_support.csv")
    cancellation_df = pd.read_csv("data/customer_cancellations.csv")

    # Select required columns
    engagement_df = engagement_df[
        [
            "customer_id",
            "total_usage_events",
            "total_active_days",
            "engagement_level"
        ]
    ]

    support_df = support_df[
        [
            "customer_id",
            "total_tickets",
            "resolved_tickets",
            "unresolved_tickets"
        ]
    ]

    # Combine customer datasets
    customer_df = engagement_df.merge(
        support_df,
        on="customer_id",
        how="left"
    )

    customer_df = customer_df.merge(
        cancellation_df,
        on="customer_id",
        how="left"
    )

    customer_df = customer_df.fillna({
        "total_tickets": 0,
        "resolved_tickets": 0,
        "unresolved_tickets": 0,
        "total_cancellations": 0
    })

    # Calculate exploratory risk score
    customer_df["risk_score"] = 0

    # Low engagement adds risk points
    customer_df.loc[
        customer_df["engagement_level"] == "Low",
        "risk_score"
    ] += 2

    customer_df.loc[
        customer_df["engagement_level"] == "Inactive",
        "risk_score"
    ] += 3

    # Unresolved support tickets add risk points
    customer_df.loc[
        customer_df["unresolved_tickets"] == 1,
        "risk_score"
    ] += 1

    customer_df.loc[
        customer_df["unresolved_tickets"] >= 2,
        "risk_score"
    ] += 2

    # High support ticket volume adds one point
    customer_df.loc[
        customer_df["total_tickets"] >= 4,
        "risk_score"
    ] += 1

    # Assign risk categories
    customer_df["risk_level"] = pd.cut(
        customer_df["risk_score"],
        bins=[-1, 1, 3, float("inf")],
        labels=["Low Risk", "Medium Risk", "High Risk"]
    )

    # Risk distribution
    risk_distribution = (
        customer_df["risk_level"]
        .value_counts()
        .reindex(["High Risk", "Medium Risk", "Low Risk"], fill_value=0)
        .reset_index()
    )

    risk_distribution.columns = [
        "risk_level",
        "number_of_customers"
    ]

    print("\nCUSTOMER RISK DISTRIBUTION")
    print(risk_distribution.to_string(index=False))

    # High-risk customers
    high_risk_customers = customer_df[
        customer_df["risk_level"] == "High Risk"
    ].sort_values(
        "risk_score",
        ascending=False
    )

    print("\nHIGH-RISK CUSTOMERS")
    print(high_risk_customers.to_string(index=False))

    # Save results
    customer_df.to_csv(
        "data/customer_churn_risk.csv",
        index=False
    )

    risk_distribution.to_csv(
        "data/churn_risk_distribution.csv",
        index=False
    )

    print("\nChurn risk analysis files saved successfully!")

    return customer_df, risk_distribution


if __name__ == "__main__":

    customer_df, risk_distribution = analyze_churn_risk()

    print("\nCHURN RISK DATASETS")
    print("Customer dataset shape:", customer_df.shape)
    print("Risk distribution shape:", risk_distribution.shape)
