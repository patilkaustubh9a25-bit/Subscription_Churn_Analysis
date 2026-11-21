
import pandas as pd


def analyze_cancellations(df):

    print("\nCANCELLATION ANALYSIS")

    # 1. Overall cancellation statistics
    total_cancellations = df["cancellation_count"].sum()

    print("\nOVERALL CANCELLATION SUMMARY")
    print("Total cancellations:", total_cancellations)

    # 2. Monthly cancellation analysis
    monthly_cancellations = df.groupby(
        "billing_period"
    ).agg(
        total_cancellations=("cancellation_count", "sum"),
        total_customers=("customer_id", "nunique")
    ).reset_index()

    print("\nMONTHLY CANCELLATION ANALYSIS")
    print(monthly_cancellations.to_string(index=False))

    # 3. Customer-level cancellation analysis
    customer_cancellations = df.groupby(
        "customer_id"
    ).agg(
        total_cancellations=("cancellation_count", "sum")
    ).reset_index()

    cancelled_customers = customer_cancellations[
        customer_cancellations["total_cancellations"] > 0
    ]

    print("\nCUSTOMER CANCELLATION SUMMARY")
    print("Total customers:", len(customer_cancellations))
    print("Customers with cancellations:", len(cancelled_customers))
    print(
        "Customers without cancellations:",
        len(customer_cancellations) - len(cancelled_customers)
    )

    # 4. Cancellation distribution
    cancellation_distribution = (
        customer_cancellations["total_cancellations"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    cancellation_distribution.columns = [
        "cancellation_count",
        "number_of_customers"
    ]

    print("\nCANCELLATION DISTRIBUTION")
    print(cancellation_distribution.to_string(index=False))

    # 5. Save analysis files
    monthly_cancellations.to_csv(
        "data/monthly_cancellations.csv",
        index=False
    )

    customer_cancellations.to_csv(
        "data/customer_cancellations.csv",
        index=False
    )

    cancellation_distribution.to_csv(
        "data/cancellation_distribution.csv",
        index=False
    )

    print("\nCancellation analysis files saved successfully!")

    return (
        monthly_cancellations,
        customer_cancellations,
        cancellation_distribution
    )


if __name__ == "__main__":

    df = pd.read_csv("data/customer_period.csv")

    (
        monthly_cancellations,
        customer_cancellations,
        cancellation_distribution
    ) = analyze_cancellations(df)

    print("\nCANCELLATION ANALYSIS DATASETS")
    print("Monthly dataset shape:", monthly_cancellations.shape)
    print("Customer dataset shape:", customer_cancellations.shape)
    print("Distribution dataset shape:", cancellation_distribution.shape)
