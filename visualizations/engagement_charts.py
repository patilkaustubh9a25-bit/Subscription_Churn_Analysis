
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_engagement_charts():

    sns.set_theme(style="whitegrid")

    # Load engagement datasets
    monthly_df = pd.read_csv("data/monthly_engagement.csv")
    customer_df = pd.read_csv("data/customer_engagement.csv")

    # 1. Customer Engagement Distribution
    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=customer_df,
        x="engagement_level",
        hue="engagement_level",
        palette="viridis",
        legend=False
    )

    plt.title("Customer Engagement Distribution")
    plt.xlabel("Engagement Level")
    plt.ylabel("Number of Customers")
    plt.tight_layout()

    plt.savefig("visualizations/engagement_distribution.png")
    plt.close()

    # 2. Monthly Usage Activity
    plt.figure(figsize=(12, 5))

    sns.lineplot(
        data=monthly_df,
        x="billing_period",
        y="total_usage_events",
        marker="o"
    )

    plt.title("Monthly Usage Activity")
    plt.xlabel("Billing Period")
    plt.ylabel("Total Usage Events")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("visualizations/monthly_usage.png")
    plt.close()

    # 3. Monthly Active Days
    plt.figure(figsize=(12, 5))

    sns.lineplot(
        data=monthly_df,
        x="billing_period",
        y="total_active_days",
        marker="o",
        color="green"
    )

    plt.title("Monthly Active Days")
    plt.xlabel("Billing Period")
    plt.ylabel("Total Active Days")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("visualizations/monthly_active_days.png")
    plt.close()

    print("Engagement charts created successfully!")


if __name__ == "__main__":
    create_engagement_charts()
