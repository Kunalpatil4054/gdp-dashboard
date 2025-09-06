import streamlit as st
import pandas as pd

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

        agg_dict = {}
        for col in ["Sales", "Profit", "Units Sold"]:
            if col in df.columns:
                agg_dict[col] = "sum"

        if agg_dict:  # only run if we have some numeric columns
            yearly = df.groupby("Year").agg(agg_dict).reset_index()

            if "Sales" in yearly.columns:
                yearly["Sales_YoY_%"] = yearly["Sales"].pct_change() * 100
            if "Profit" in yearly.columns:
                yearly["Profit_YoY_%"] = yearly["Profit"].pct_change() * 100

            st.dataframe(yearly)

            chart_cols = [col for col in ["Sales", "Profit"] if col in yearly.columns]
            if chart_cols:
                st.line_chart(yearly.set_index("Year")[chart_cols])

    # ------------------------------
    # Segment Analysis
    # ------------------------------
    if "Segment" in df.columns:
        st.subheader("📊 Segment Analysis")

        seg = df.groupby("Segment").sum().reset_index()
        st.dataframe(seg)

        numeric_cols = [c for c in ["Sales", "Profit"] if c in seg.columns]
        if numeric_cols:
            st.bar_chart(seg.set_index("Segment")[numeric_cols])

    # ------------------------------
    # Top 10 Products
    # ------------------------------
    if "Product" in df.columns and "Sales" in df.columns:
        st.subheader("🏆 Top 10 Products by Sales")
        top_products = df.groupby("Product")["Sales"].sum().nlargest(10).reset_index()
        st.bar_chart(top_products.set_index("Product"))

    # ------------------------------
    # Country-wise Analysis
    # ------------------------------
    if "Country" in df.columns and "Profit" in df.columns:
        st.subheader("🌍 Top 10 Countries by Profit")
        top_countries = df.groupby("Country")["Profit"].sum().nlargest(10).reset_index()
        st.bar_chart(top_countries.set_index("Country"))

else:
    st.info("👆 Please upload a financial dataset to start.")
