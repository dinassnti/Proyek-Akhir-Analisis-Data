import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Konfigurasi halaman
st.set_page_config(page_title="E-Commerce Analysis Dashboard", layout="wide")

# 1. Load Data dengan Jalur Dinamis
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "main_data.csv")

# Membaca data
main_df = pd.read_csv(file_path)
main_df['order_purchase_timestamp'] = pd.to_datetime(main_df['order_purchase_timestamp'])

# --- SIDEBAR ---
with st.sidebar:
    st.title("E-Commerce Dashboard")
    
    # Input rentang tanggal dengan penanganan error
    try:
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=main_df["order_purchase_timestamp"].min(),
            max_value=main_df["order_purchase_timestamp"].max(),
            value=[main_df["order_purchase_timestamp"].min(), main_df["order_purchase_timestamp"].max()]
        )
    except ValueError:
        st.error("Silakan pilih rentang tanggal (Tanggal Mulai & Tanggal Akhir).")
        st.stop() 

# --- PROSES FILTERING ---
# Hasil filter disimpan di 'main_df_filtered'
main_df_filtered = main_df[
    (main_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
    (main_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

# --- HEADER ---
st.header('E-Commerce Performance Dashboard :sparkles:')

# --- PERTANYAAN 1: TREN PENDAPATAN ---
st.subheader("1. Monthly Revenue Trend")
# PERBAIKAN: Gunakan main_df_filtered agar filter berfungsi
monthly_revenue = main_df_filtered.resample(rule='ME', on='order_purchase_timestamp').total_revenue.sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_revenue["order_purchase_timestamp"], monthly_revenue["total_revenue"], marker='o', linewidth=2, color="#2E86C1")
ax.set_title("Total Revenue per Month (2017-2018)", fontsize=15)
ax.set_xlabel(None)
ax.set_ylabel("Revenue (BRL)")
st.pyplot(fig)
plt.close(fig)

# --- PERTANYAAN 2: ANALISIS RFM ---
st.subheader("2. Best Customer Based on RFM Parameters")

# PERBAIKAN: Gunakan main_df_filtered
snapshot_date = main_df_filtered['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

rfm_df = main_df_filtered.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'nunique',
    'total_revenue': 'sum'
}).reset_index()

rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']

col1, col2, col3 = st.columns(3)

with col1:
    fig, ax = plt.subplots(figsize=(10, 8))
    top_recency = rfm_df.sort_values(by="recency", ascending=True).head(5)
    # PERBAIKAN: Tambahkan hue dan legend=False untuk atasi warning
    sns.barplot(y="recency", x="customer_id", data=top_recency, hue="customer_id", palette="Blues", ax=ax, legend=False)
    ax.set_title("By Recency (days)", fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_xticks([]) 
    st.pyplot(fig)
    plt.close(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 8))
    top_frequency = rfm_df.sort_values(by="frequency", ascending=False).head(5)
    sns.barplot(y="frequency", x="customer_id", data=top_frequency, hue="customer_id", palette="Blues", ax=ax, legend=False)
    ax.set_title("By Frequency", fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_xticks([])
    st.pyplot(fig)
    plt.close(fig)

with col3:
    fig, ax = plt.subplots(figsize=(10, 8))
    top_monetary = rfm_df.sort_values(by="monetary", ascending=False).head(5)
    sns.barplot(y="monetary", x="customer_id", data=top_monetary, hue="customer_id", palette="Blues", ax=ax, legend=False)
    ax.set_title("By Monetary", fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_xticks([])
    st.pyplot(fig)
    plt.close(fig)

# --- PERTANYAAN 3: DISTRIBUSI GEOSPASIAL ---
st.subheader("3. Customer Distribution by State")
# PERBAIKAN: Gunakan main_df_filtered
state_df = main_df_filtered.groupby("customer_state").customer_unique_id.nunique().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
# PERBAIKAN: Tambahkan hue dan legend=False
sns.barplot(x="customer_unique_id", y="customer_state", data=state_df.head(10), hue="customer_state", palette="viridis", ax=ax, legend=False)
ax.set_title("Top 10 States with Most Customers", fontsize=15)
ax.set_xlabel("Number of Customers")
ax.set_ylabel(None)
st.pyplot(fig)
plt.close(fig)

st.caption('Copyright (c) Dina Surya Susanti 2026')
