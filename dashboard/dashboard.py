import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Konfigurasi halaman
st.set_page_config(page_title="E-Commerce Analysis Dashboard", layout="wide")

# 1. Load Data dengan Jalur Dinamis
# Mendapatkan jalur direktori tempat file dashboard.py ini berada
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "main_data.csv")

# Membaca data
main_df = pd.read_csv(file_path)
main_df['order_purchase_timestamp'] = pd.to_datetime(main_df['order_purchase_timestamp'])

# --- SIDEBAR ---
with st.sidebar:
    st.title("E-Commerce Dashboard")
    
     # Input rentang tanggal dengan penanganan error sesuai saran Reviewer
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
monthly_revenue = main_df.resample(rule='ME', on='order_purchase_timestamp').total_revenue.sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_revenue["order_purchase_timestamp"], monthly_revenue["total_revenue"], marker='o', linewidth=2, color="#2E86C1")
ax.set_xlabel(None)
ax.set_ylabel("Revenue (BRL)")
st.pyplot(fig)

# --- PERTANYAAN 2: ANALISIS RFM ---
st.subheader("2. Best Customer Based on RFM Parameters")

# 1. Menentukan tanggal referensi terbaru
# Kita tambahkan 1 hari agar pelanggan yang belanja di hari terakhir tidak memiliki recency 0 (yang membuat grafik kosong)
snapshot_date = main_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

# 2. Menghitung RFM
rfm_df = main_df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days, # Recency
    'order_id': 'nunique', # Frequency
    'total_revenue': 'sum' # Monetary
}).reset_index()

rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']

# 3. Menampilkan Visualisasi
col1, col2, col3 = st.columns(3)

with col1:
    fig, ax = plt.subplots(figsize=(10, 8))
    # Recency: Semakin kecil semakin baik, jadi kita ambil 5 terkecil
    top_recency = rfm_df.sort_values(by="recency", ascending=True).head(5)
    sns.barplot(y="recency", x="customer_id", data=top_recency, palette="Blues", ax=ax)
    ax.set_title("Recency (days)", fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel("Customer ID", fontsize=15)
    ax.set_xticks([]) # Menyembunyikan ID agar tidak berantakan
    st.pyplot(fig)
    plt.close(fig) # Membersihkan memori agar tidak bentrok

with col2:
    fig, ax = plt.subplots(figsize=(10, 8))
    # Frequency: Semakin besar semakin baik
    top_frequency = rfm_df.sort_values(by="frequency", ascending=False).head(5)
    sns.barplot(y="frequency", x="customer_id", data=top_frequency, palette="Blues", ax=ax)
    ax.set_title("Frequency", fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel("Customer ID", fontsize=15)
    ax.set_xticks([])
    st.pyplot(fig)
    plt.close(fig)

with col3:
    fig, ax = plt.subplots(figsize=(10, 8))
    # Monetary: Semakin besar semakin baik
    top_monetary = rfm_df.sort_values(by="monetary", ascending=False).head(5)
    sns.barplot(y="monetary", x="customer_id", data=top_monetary, palette="Blues", ax=ax)
    ax.set_title("Monetary", fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel("Customer ID", fontsize=15)
    ax.set_xticks([])
    st.pyplot(fig)
    plt.close(fig)

# --- PERTANYAAN 3: DISTRIBUSI GEOSPASIAL ---
st.subheader("3. Customer Distribution by State")
state_df = main_df.groupby("customer_state").customer_unique_id.nunique().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="customer_unique_id", y="customer_state", data=state_df.head(10), palette="viridis")
ax.set_xlabel("Number of Customers")
ax.set_ylabel("State")
st.pyplot(fig)

st.caption('Copyright (c) Dina Surya Susantni 2026')
