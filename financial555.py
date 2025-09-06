import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Financial Dashboard", layout="wide")

# ------------------------------
# File Uploader
# ------------------------------
st.title("📊 Shriram Finance Dashboard")

uploaded_file = st.file_uploader("Upload Financial Data (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Preview of Data")
    st.dataframe(df.head())

    # ------------------------------
    # KPIs
    # ------------------------------
    st.subheader("Key Performance Indicators (KPIs)")

    kpi_cols = st.columns(4)

    if "Sales" in df.columns:
        total_sales = df["Sales"].sum()
        kpi_cols[0].metric("Total Sales", f"{total_sales:,.0f}")

    if "Profit" in df.columns:
        total_profit = df["Profit"].sum()
        kpi_cols[1].metric("Total Profit", f"{total_profit:,.0f}")

    if "Units Sold" in df.columns:
        total_units = df["Units Sold"].sum()
        kpi_cols[2].metric("Total Units", f"{total_units:,.0f}")

    if {"Sales", "Profit"}.issubset(df.columns):
        gross_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
        kpi_cols[3].metric("Gross Margin %", f"{gross_margin:.2f}%")

    # ------------------------------
    # Yearly Trends
    # ------------------------------
    if "Year" in df.columns:
        st.subheader("📈 Yearly Trends")
        yearly = df.groupby("Year").agg({
            "Sales": "sum",
            "Profit": "sum",
            "Units Sold": "sum"
        }).reset_index()

        yearly["Sales_YoY_%"] = yearly["Sales"].pct_change() * 100
        yearly["Profit_YoY_%"] = yearly["Profit"].pct_change() * 100

        st.dataframe(yearly)

        st.line_chart(yearly.set_index("Year")[["Sales", "Profit"]])

    # ------------------------------
    # Segment Analysis
    # ------------------------------
    if "Segment" in df.columns:
        st.subheader("📊 Segment Analysis")
        seg = df.groupby("Segment").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        seg["Gross_Margin_%"] = (seg["Profit"] / seg["Sales"]) * 100

        st.dataframe(seg)

        st.bar_chart(seg.set_index("Segment")[["Sales", "Profit"]])
        st.line_chart(seg.set_index("Segment")[["Gross_Margin_%"]])

    # ------------------------------
    # Top 10 Products
    # ------------------------------
    if "Product" in df.columns:
        st.subheader("🏆 Top 10 Products by Sales")
        top_products = df.groupby("Product")["Sales"].sum().nlargest(10).reset_index()
        st.bar_chart(top_products.set_index("Product"))

    # ------------------------------
    # Country-wise Analysis
    # ------------------------------
    if "Country" in df.columns:
        st.subheader("🌍 Top 10 Countries by Profit")
        top_countries = df.groupby("Country")["Profit"].sum().nlargest(10).reset_index()
        st.bar_chart(top_countries.set_index("Country"))

else:
    st.info("👆 Please upload a financial dataset to start.")
