import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Vendor Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# File Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent

CSV_FILE = BASE_DIR / "vendor_data.csv"
DB_FILE = BASE_DIR / "vendor_data.db"

# -----------------------------
# Load CSV
# -----------------------------

if not CSV_FILE.exists():
    st.error("vendor_data.csv was not found.")
    st.stop()

df = pd.read_csv(CSV_FILE)

# -----------------------------
# Check Columns
# -----------------------------

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
        "Missing columns: "
        + ", ".join(missing_columns)
    )

    st.write("Columns available in CSV:")
    st.write(list(df.columns))

    st.stop()

# -----------------------------
# Convert Numeric Columns
# -----------------------------

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

# -----------------------------
# Create SQLite Database
# -----------------------------

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

    st.warning(f"Database error: {e}")

# -----------------------------
# Dashboard Title
# -----------------------------

st.title("📊 Vendor Performance Dashboard")

st.write(
    "Analysis of vendor orders, purchases, quantities and defects."
)

st.divider()

# -----------------------------
# KPI Section
# -----------------------------

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

# -----------------------------
# Vendor Performance
# -----------------------------

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

# -----------------------------
# Purchase Chart
# -----------------------------

st.subheader("Purchase Amount by Vendor")

st.bar_chart(
    summary["Purchase_Amount"]
)

# -----------------------------
# Orders Chart
# -----------------------------

st.subheader("Orders by Vendor")

st.bar_chart(
    summary["Orders"]
)

# -----------------------------
# Quantity Chart
# -----------------------------

st.subheader("Quantity by Vendor")

st.bar_chart(
    summary["Quantity"]
)

# -----------------------------
# Defects Chart
# -----------------------------

st.subheader("Defects by Vendor")

st.bar_chart(
    summary["Defects"]
)

# -----------------------------
# Raw Data
# -----------------------------

st.divider()

st.header("Raw Vendor Data")

st.dataframe(
    df,
    use_container_width=True
)

# -----------------------------
# Download CSV
# -----------------------------

st.download_button(
    label="Download Vendor Data",
    data=df.to_csv(index=False),
    file_name="vendor_data.csv",
    mime="text/csv"
)