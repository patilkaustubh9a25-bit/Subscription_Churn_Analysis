from analytics.data_loader import load_all_data
from analytics.clean_data import clean_all_data

# Load original data from PostgreSQL
data = load_all_data()

# Clean the data in memory
cleaned_data = clean_all_data(data)

print("\n========== CLEANING RESULTS ==========")

for name, df in cleaned_data.items():
    print(f"{name}: {df.shape}")

print("\nCustomers duplicate IDs:",
      cleaned_data["customers"]["customer_id"].duplicated().sum())

print("Invoices duplicate IDs:",
      cleaned_data["invoices"]["invoice_id"].duplicated().sum())

print("\nCleaning completed successfully!")
print("\nBILLING PERIOD CHECK")

print(
    cleaned_data["invoices"]["billing_period"]
    .value_counts(dropna=False)
)

print(
    "\nInvalid billing periods:",
    cleaned_data["invoices"]["billing_period"].isna().sum()
)