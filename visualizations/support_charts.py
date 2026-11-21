
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_support_charts():

    sns.set_theme(style="whitegrid")

    monthly_df = pd.read_csv("data/monthly_support.csv")
    customer_df = pd.read_csv("data/customer_support.csv")

    # 1. Monthly Support Ticket Volume
    plt.figure(figsize=(12, 5))

    sns.lineplot(
        data=monthly_df,
        x="billing_period",
        y="total_tickets",
        marker="o"
    )

    plt.title("Monthly Support Ticket Volume")
    plt.xlabel("Billing Period")
    plt.ylabel("Total Tickets")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("visualizations/monthly_support_tickets.png")
    plt.close()

    # 2. Resolved vs Unresolved Tickets
    ticket_summary = pd.DataFrame({
        "Status": ["Resolved", "Unresolved"],
        "Tickets": [
            monthly_df["resolved_tickets"].sum(),
            monthly_df["unresolved_tickets"].sum()
        ]
    })

    plt.figure(figsize=(7, 5))

    sns.barplot(
        data=ticket_summary,
        x="Status",
        y="Tickets",
        hue="Status",
        palette="viridis",
        legend=False
    )

    plt.title("Resolved vs Unresolved Support Tickets")
    plt.xlabel("Ticket Status")
    plt.ylabel("Number of Tickets")
    plt.tight_layout()

    plt.savefig("visualizations/ticket_resolution.png")
    plt.close()

    # 3. Top 10 Customers by Support Tickets
    top_customers = customer_df.sort_values(
        "total_tickets",
        ascending=False
    ).head(10)

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=top_customers,
        x="total_tickets",
        y="customer_id",
        hue="customer_id",
        palette="viridis",
        legend=False
    )

    plt.title("Top 10 Customers by Support Tickets")
    plt.xlabel("Total Support Tickets")
    plt.ylabel("Customer ID")
    plt.tight_layout()

    plt.savefig("visualizations/top_support_customers.png")
    plt.close()

    print("Support charts created successfully!")

if __name__ == "__main__":
    create_support_charts()