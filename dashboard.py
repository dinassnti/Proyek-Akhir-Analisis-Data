import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt
from babel.numbers import format_currency


# Konfigurasi Page
st.set_page_config(page_title="E-Commerce Analysis Dashboard", layout="wide")

# Load data yang sudah dibersihkan
df = pd.read_csv("dashboard/main_data.csv")
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['total_revenue'] = df['price'] + df['freight_value']

# Sidebar Filter
with st.sidebar:
    st.title("E-Commerce Dashboard")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=df['order_purchase_timestamp'].min(),
        max_value=df['order_purchase_timestamp'].max(),
        value=[df['order_purchase_timestamp'].min(), df['order_purchase_timestamp'].max()]
    )

main_df = df[(df["order_purchase_timestamp"] >= str(start_date)) & 
            (df["order_purchase_timestamp"] <= str(end_date))]

# Header Utama
st.header('E-Commerce Performance Dashboard :sparkles:')

# --- PERTANYAAN 1: TREN PENDAPATAN ---
st.subheader("1. Monthly Revenue Trend")
monthly_revenue = main_df.resample(rule='M', on='order_purchase_timestamp').total_revenue.sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_revenue["order_purchase_timestamp"], monthly_revenue["total_revenue"], marker='o', linewidth=2, color="#2E86C1")
ax.set_xlabel(None)
ax.set_ylabel("Revenue (BRL)")
st.pyplot(fig)

# --- PERTANYAAN 2: RFM ANALYSIS ---
st.subheader("2. Best Customer Based on RFM Parameters")
now = main_df['order_purchase_timestamp'].max() + dt.timedelta(days=1)
rfm_df = main_df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (now - x.max()).days,
    'order_id': 'nunique',
    'total_revenue': 'sum'
}).reset_index()
rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']

col1, col2, col3 = st.columns(3)
with col1:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), color="#2E86C1")
    ax.set_title("Recency (days)", fontsize=15)
    ax.set_xticks([])
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), color="#2E86C1")
    ax.set_title("Frequency", fontsize=15)
    ax.set_xticks([])
    st.pyplot(fig)
with col3:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), color="#2E86C1")
    ax.set_title("Monetary", fontsize=15)
    ax.set_xticks([])
    st.pyplot(fig)

# --- PERTANYAAN 3: GEOSPATIAL ---
st.subheader("3. Customer Distribution by State")
state_df = main_df.groupby("customer_state").customer_id.nunique().sort_values(ascending=False).reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="customer_id", y="customer_state", data=state_df.head(10), palette="viridis")
ax.set_xlabel("Number of Customers")
ax.set_ylabel("State")
st.pyplot(fig)

st.caption('Copyright (c) Dina Surya Susanti 2026')