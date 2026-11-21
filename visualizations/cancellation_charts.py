
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_cancellation_charts():

    sns.set_theme(style="whitegrid")

    monthly_df = pd.read_csv("data/monthly_cancellations.csv")
    customer_df = pd.read_csv("data/customer_cancellations.csv")

    # 1. Monthly Cancellation Trends
    plt.figure(figsize=(12, 5))

    sns.lineplot(
        data=monthly_df,
        x="billing_period",
        y="total_cancellations",
        marker="o"
    )

    plt.title("Monthly Cancellation Trends")
    plt.xlabel("Billing Period")
    plt.ylabel("Total Cancellations")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("visualizations/monthly_cancellations.png")
    plt.close()

    # 2. Customer Cancellation Distribution
    cancellation_counts = (
        customer_df["total_cancellations"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    cancellation_counts.columns = [
        "Cancellation Count",
        "Number of Customers"
    ]

    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=cancellation_counts,
        x="Cancellation Count",
        y="Number of Customers",
        hue="Cancellation Count",
        palette="viridis",
        legend=False
    )

    plt.title("Customer Cancellation Distribution")
    plt.xlabel("Number of Cancellations")
    plt.ylabel("Number of Customers")
    plt.tight_layout()

    plt.savefig("visualizations/cancellation_distribution.png")
    plt.close()

    # 3. Customers With vs Without Cancellations
    customer_status = pd.DataFrame({
        "Status": ["With Cancellations", "Without Cancellations"],
        "Customers": [
            (customer_df["total_cancellations"] > 0).sum(),
            (customer_df["total_cancellations"] == 0).sum()
        ]
    })

    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=customer_status,
        x="Status",
        y="Customers",
        hue="Status",
        palette="viridis",
        legend=False
    )

    plt.title("Customers With vs Without Cancellations")
    plt.xlabel("Customer Status")
    plt.ylabel("Number of Customers")
    plt.tight_layout()

    plt.savefig("visualizations/cancellation_status.png")
    plt.close()

    print("Cancellation charts created successfully!")

if __name__ == "__main__":
    create_cancellation_charts()