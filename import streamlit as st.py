import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# =========================================================
# 1. PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Vendor Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# 2. FIND CSV FILE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "vendor_data.csv"
DB_FILE = BASE_DIR / "vendor_data.db"

# Check CSV exists
if not CSV_FILE.exists():
    st.error(f"CSV file not found: {CSV_FILE}")
    st.stop()

# =========================================================
# 3. LOAD DATA
# =========================================================

try:
    df = pd.read_csv(CSV_FILE)
except Exception as e:
    st.error(f"Error reading CSV file: {e}")
    st.stop()

# =========================================================
# 4. CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "Vendor",
    "Order_ID",
    "Purchase_Amount",
    "Quantity",
    "Defects"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "Missing columns in vendor_data.csv: "
        + ", ".join(missing_columns)
    )
    st.write("Columns found in your CSV:")
    st.write(list(df.columns))
    st.stop()

# =========================================================
# 5. CONVERT NUMERIC COLUMNS
# =========================================================

df["Purchase_Amount"] = pd.to_numeric(
    df["Purchase_Amount"],
    errors="coerce"
).fillna(0)

df["Quantity"] = pd.to_numeric(
    df["Quantity"],
    errors="coerce"
).fillna(0)

df["Defects"] = pd.to_numeric(
    df["Defects"],
    errors="coerce"
).fillna(0)

# =========================================================
# 6. CREATE SQLITE DATABASE
# =========================================================

try:
    conn = sqlite3.connect(DB_FILE)

    df.to_sql(
        "vendor_data",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

except Exception as e:
    st.warning(f"Database could not be created: {e}")

# =========================================================
# 7. TITLE
# =========================================================

st.title("📊 Vendor Performance Dashboard")

st.write(
    "Analysis of vendor orders, purchases, quantities and defects."
)

st.divider()

# =========================================================
# 8. KPI SECTION
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Orders",
        len(df)
    )

with col2:
    st.metric(
        "Total Purchase Amount",
        f"₹{df['Purchase_Amount'].sum():,.2f}"
    )

with col3:
    st.metric(
        "Total Quantity",
        f"{df['Quantity'].sum():,.0f}"
    )

with col4:
    st.metric(
        "Total Defects",
        f"{df['Defects'].sum():,.0f}"
    )

st.divider()

# =========================================================
# 9. VENDOR PERFORMANCE
# =========================================================

st.header("Vendor Performance")

summary = df.groupby("Vendor").agg(
    Orders=("Order_ID", "count"),
    Purchase_Amount=("Purchase_Amount", "sum"),
    Quantity=("Quantity", "sum"),
    Defects=("Defects", "sum")
)

st.dataframe(
    summary,
    use_container_width=True
)

# =========================================================
# 10. PURCHASE AMOUNT CHART
# =========================================================

st.subheader("Purchase Amount by Vendor")

st.bar_chart(
    summary["Purchase_Amount"]
)

# =========================================================
# 11. ORDERS CHART
# =========================================================

st.subheader("Orders by Vendor")

st.bar_chart(
    summary["Orders"]
)

# =========================================================
# 12. QUANTITY CHART
# =========================================================

st.subheader("Quantity by Vendor")

st.bar_chart(
    summary["Quantity"]
)

# =========================================================
# 13. DEFECTS CHART
# =========================================================

st.subheader("Defects by Vendor")

st.bar_chart(
    summary["Defects"]
)

# =========================================================
# 14. RAW DATA
# =========================================================

st.divider()

st.header("Vendor Data")

st.dataframe(
    df,
    use_container_width=True
)

# =========================================================
# 15. DOWNLOAD DATA
# =========================================================

csv_download = df.to_csv(index=False)

st.download_button(
    label="Download Vendor Data",
    data=csv_download,
    file_name="vendor_data.csv",
    mime="text/csv"
)

# =========================================================
# END
# ====