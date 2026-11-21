import pandas as pd
from pathlib import Path

DATA_PATH = Path("data")

datasets = [
    "customers",
    "subscription_plans",
    "invoices",
    "usage_events",
    "support_tickets",
    "cancellations"
]

for name in datasets:

    print("\n" + "=" * 50)
    print(f"DATASET: {name.upper()}")
    print("=" * 50)

    df = pd.read_csv(DATA_PATH / f"{name}.csv")

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nSample Records:")
    print(df.head(5))