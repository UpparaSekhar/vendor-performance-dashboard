import pandas as pd

# Load the vendor data
df = pd.read_csv("vendor_data.csv")

print("VENDOR DATA")
print(df)

print("\nTOTAL ORDERS:")
print(len(df))

print("\nTOTAL PURCHASE AMOUNT:")
print(df["Purchase_Amount"].sum())

print("\nVENDOR PERFORMANCE:")

summary = df.groupby("Vendor").agg(
    Orders=("Order_ID", "count"),
    Purchase_Amount=("Purchase_Amount", "sum"),
    Quantity=("Quantity", "sum"),
    Defects=("Defects", "sum")
)

print(summary)