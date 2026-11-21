
import numpy as np
import pandas as pd
import random
from pathlib import Path

random.seed(42)
np.random.seed(42)

OUTPUT = Path("data")
OUTPUT.mkdir(exist_ok=True)

# 1. Customers
n = 500

customers = pd.DataFrame({
    "customer_id": [f"C{i:04d}" for i in range(1, n + 1)],
    "name": [f"Customer {i}" for i in range(1, n + 1)],
    "email": [f"customer{i}@example.com" for i in range(1, n + 1)],
    "signup_date": pd.to_datetime(
        np.random.choice(pd.date_range("2024-01-01", "2026-06-30"), n)
    ),
    "country": np.random.choice(
        ["India", "USA", "UK", "Canada", "Australia"], n
    )
})

# Missing values and duplicate customer
customers.loc[10:19, "email"] = np.nan
customers = pd.concat([customers, customers.iloc[[5]]], ignore_index=True)

# 2. Subscription plans
plans = pd.DataFrame({
    "plan_id": ["P01", "P02", "P03", "P04"],
    "plan_name": ["Basic", "Standard", "Premium", "Enterprise"],
    "monthly_price": [199, 399, 699, 999],
    "billing_cycle": ["Monthly", "Monthly", "Yearly", "Monthly"]
})

# 3. Invoices
invoice_rows = []

for i in range(1, 1201):
    customer_id = f"C{random.randint(1, n):04d}"

    # Introduce inconsistent customer IDs
    if i % 50 == 0:
        customer_id = customer_id.lower()

    invoice_rows.append({
        "invoice_id": f"INV{i:05d}",
        "customer_id": customer_id,
        "plan_id": random.choice(plans["plan_id"]),
        "invoice_date": pd.Timestamp("2025-01-01")
            + pd.Timedelta(days=random.randint(0, 650)),
        "billing_period": random.choice([
            "2025-01", "2025-02", "2025-03",
            "2025-04", "Jan-2025", "2025/05"
        ]),
        "amount": random.choice([199, 399, 699, 999, -199, None]),
        "payment_status": random.choice([
            "Paid", "Unpaid", "Pending", "paid", "Failed", None
        ])
    })

invoices = pd.DataFrame(invoice_rows)

# Duplicate invoices
invoices = pd.concat(
    [invoices, invoices.iloc[:10]],
    ignore_index=True
)

# 4. Usage events
usage_rows = []

for i in range(1, 3001):
    usage_rows.append({
        "event_id": f"E{i:05d}",
        "customer_id": f"C{random.randint(1, n):04d}",
        "event_date": pd.Timestamp("2025-01-01")
            + pd.Timedelta(days=random.randint(0, 650)),
        "event_type": random.choice([
            "Login", "Search", "Download", "Upload", "Purchase"
        ])
    })

usage = pd.DataFrame(usage_rows)

# 5. Support tickets
ticket_rows = []

for i in range(1, 401):
    created = pd.Timestamp("2025-01-01") + pd.Timedelta(
        days=random.randint(0, 650)
    )

    resolved = created + pd.Timedelta(
        days=random.randint(1, 15)
    )

    ticket_rows.append({
        "ticket_id": f"T{i:05d}",
        "customer_id": f"C{random.randint(1, n):04d}",
        "created_at": created,
        "resolved_at": resolved if i % 5 != 0 else None,
        "status": random.choice(["Open", "Resolved", "Closed"]),
        "issue_type": random.choice([
            "Billing", "Technical", "Account", "Payment"
        ])
    })

tickets = pd.DataFrame(ticket_rows)

# 6. Cancellations
cancellation_rows = []

for i in range(1, 101):
    cancellation_rows.append({
        "cancellation_id": f"CAN{i:04d}",
        "customer_id": f"C{random.randint(1, n):04d}",
        "cancellation_date": pd.Timestamp("2025-01-01")
            + pd.Timedelta(days=random.randint(0, 650)),
        "cancellation_reason": random.choice([
            "High Price", "Poor Service", "Not Needed",
            "Technical Issues", None
        ])
    })

cancellations = pd.DataFrame(cancellation_rows)

# Save all datasets
datasets = {
    "customers": customers,
    "subscription_plans": plans,
    "invoices": invoices,
    "usage_events": usage,
    "support_tickets": tickets,
    "cancellations": cancellations
}

for name, df in datasets.items():
    df.to_csv(OUTPUT / f"{name}.csv", index=False)
    print(f"{name}.csv created: {df.shape}")

print("\nAll six datasets generated successfully!")
