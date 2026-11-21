
from analytics.data_loader import load_all_data
from analytics.clean_data import clean_all_data
from analytics.customer_period import build_customer_period


# Load and clean source data
data = load_all_data()
data = clean_all_data(data)

# Build customer-period dataset
customer_period = build_customer_period(data)

# Save dataset
customer_period.to_csv(
    "data/customer_period.csv",
    index=False
)

print("\nCustomer-period dataset saved successfully!")
print("Records:", len(customer_period))
print("Columns:", len(customer_period.columns))

# Verify saved CSV
import pandas as pd

saved_data = pd.read_csv("data/customer_period.csv")

print("\nSAVED CSV VERIFICATION")
print("Shape:", saved_data.shape)
print("Duplicate keys:", saved_data.duplicated(
    ["customer_id", "billing_period"]
).sum())
print("Missing customer IDs:", saved_data["customer_id"].isna().sum())
