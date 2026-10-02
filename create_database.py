import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("vendor_data.csv")

# Create SQLite database
conn = sqlite3.connect("vendor_data.db")

# Save CSV data into database
df.to_sql("vendor_data", conn, if_exists="replace", index=False)

print("Database created successfully!")
print("Table 'vendor_data' created successfully!")

conn.close()