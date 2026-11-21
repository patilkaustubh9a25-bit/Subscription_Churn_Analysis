
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_churn_risk_charts():

    sns.set_theme(style="whitegrid")

    customer_df = pd.read_csv("data/customer_churn_risk.csv")
    distribution_df = pd.read_csv("data/churn_risk_distribution.csv")

    # 1. Churn Risk Distribution
    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=distribution_df,
        x="risk_level",
        y="number_of_customers",
        hue="risk_level",
        palette="viridis",
        legend=False
    )

    plt.title("Customer Churn Risk Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Customers")
    plt.tight_layout()

    plt.savefig("visualizations/churn_risk_distribution.png")
    plt.close()

    # 2. Risk Score Distribution
    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=customer_df,
        x="risk_score",
        hue="risk_score",
        palette="viridis",
        legend=False
    )

    plt.title("Customer Risk Score Distribution")
    plt.xlabel("Risk Score")
    plt.ylabel("Number of Customers")
    plt.tight_layout()

    plt.savefig("visualizations/risk_score_distribution.png")
    plt.close()

    # 3. High-Risk Customer Comparison
    high_risk = customer_df[
        customer_df["risk_level"] == "High Risk"
    ].sort_values(
        "risk_score",
        ascending=False
    )

    plt.figure(figsize=(9, 5))

    sns.barplot(
        data=high_risk,
        x="customer_id",
        y="risk_score",
        hue="customer_id",
        palette="viridis",
        legend=False
    )

    plt.title("High-Risk Customer Scores")
    plt.xlabel("Customer ID")
    plt.ylabel("Risk Score")
    plt.tight_layout()

    plt.savefig("visualizations/high_risk_customers.png")
    plt.close()

    print("Churn risk charts created successfully!")


if __name__ == "__main__":
    create_churn_risk_charts()
