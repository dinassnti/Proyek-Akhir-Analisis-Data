# E-Commerce Data Analysis Dashboard ✨

## Dashboard Preview
Dashboard ini memberikan visualisasi data terkait performa penjualan e-commerce di Brazil, segmentasi pelanggan menggunakan analisis RFM, serta distribusi geografis pelanggan.

## Struktur Proyek
- `/dashboard`: Berisi file utama dashboard (`dashboard.py`) dan dataset yang telah dibersihkan (`main_data.csv`).
- `/data`: Berisi dataset mentah (opsional).
- `Proyek_Analisis_Data.ipynb`: File analisis data lengkap mulai dari Wrangling hingga Exploratory Data Analysis (EDA).
- `requirements.txt`: Daftar library Python yang dibutuhkan.

## Cara Menjalankan Secara Lokal
### 1. Persiapan Environment
Pastikan kamu sudah menginstal Python. Sangat disarankan menggunakan virtual environment.
```bash
conda create --name main-ds python=3.13
conda activate main-ds
pip install -r requirements.txt