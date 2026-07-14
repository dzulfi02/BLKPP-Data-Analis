# 🐔 Forecasting Harga Daging Ayam Nasional Menggunakan Time Series

Proyek ini bertujuan untuk memprediksi harga daging ayam nasional menggunakan metode **Time Series Forecasting**. Beberapa model forecasting dibandingkan untuk memperoleh model dengan performa terbaik berdasarkan metrik evaluasi **MAE**, **RMSE**, dan **MAPE**. Hasil terbaik kemudian diimplementasikan dalam sebuah aplikasi interaktif menggunakan **Streamlit**.

link demo : []

---

## 📌 Latar Belakang

Harga daging ayam merupakan salah satu komoditas pangan strategis di Indonesia yang mengalami fluktuasi akibat berbagai faktor, seperti permintaan pasar, musim, distribusi, dan kondisi ekonomi. Prediksi harga pada periode mendatang dapat membantu pelaku usaha maupun masyarakat dalam melakukan perencanaan.

---

## 🎯 Tujuan

- Melakukan analisis data harga daging ayam nasional.
- Membandingkan beberapa metode forecasting time series.
- Memilih model terbaik berdasarkan nilai evaluasi.
- Membangun aplikasi forecasting berbasis Streamlit.

---

## 📂 Dataset

- **Nama Dataset** : Harga Daging Ayam Nasional
- **Sumber Data** : Panel Harga Pangan Nasional – Badan Pangan Nasional (National Food Agency)
- **Periode Data** : Juli 2022 – Juli 2026

Dataset berisi data harga harian daging ayam yang digunakan sebagai data historis untuk proses forecasting.

---

## 🛠️ Teknologi yang Digunakan

- Python
- Pandas
- NumPy
- Statsmodels
- Prophet
- Matplotlib
- Plotly
- Streamlit
- Scikit-Learn

---

## 📈 Metode Forecasting

Model yang dibandingkan pada penelitian ini yaitu:

- ARIMA
- SARIMA
- Holt-Winters Exponential Smoothing
- Prophet

---

## 📊 Hasil Evaluasi

| Model | MAE | RMSE | MAPE (%) |
|--------|-------:|-------:|-------:|
| ARIMA | 2409.26 | 3044.95 | 5.86 |
| SARIMA | 2409.26 | 3044.95 | 5.86 |
| Prophet | 1666.01 | 1993.54 | 4.26 |
| **Holt-Winters** | **1589.87** | **1851.21** | **3.97** |

### 🏆 Model Terbaik

Model **Holt-Winters Exponential Smoothing** dipilih sebagai model terbaik karena memiliki nilai **MAE**, **RMSE**, dan **MAPE** paling rendah dibandingkan model lainnya.

---

## 📷 Dashboard Streamlit

Dashboard menyediakan beberapa fitur utama, yaitu:

- Menampilkan ringkasan dataset
- Menampilkan model terbaik
- Visualisasi data historis
- Visualisasi hasil forecasting
- Pemilihan horizon forecasting (7, 14, dan 30 hari)
- Perbandingan performa model
- Download hasil forecasting dalam format CSV

---

## 📁 Struktur Project

```text
Forecasting-Time-Series/
│
├── app.py
├── Holt-Winter.py
├── requirements.txt
├── README.md
├── dataset/
│   └── harga_ayam.csv
│
└── images/
    └── dashboard.png
```

---

## ▶️ Menjalankan Project

Clone repository

```bash
git clone https://github.com/dzulfi02/BLKPP-Data-Analis.git
```

Masuk ke folder project

```bash
cd BLKPP-Data-Analis/Forecasting-Time-Series
```

Install dependency

```bash
pip install -r requirements.txt
```

Jalankan Streamlit

```bash
streamlit run app.py
```

---

## 📌 Hasil Forecast

Aplikasi memungkinkan pengguna memilih horizon prediksi:

- 7 Hari
- 14 Hari
- 30 Hari

Kemudian aplikasi akan menampilkan:

- Grafik historis
- Grafik forecasting
- Nilai prediksi
- Tabel hasil forecasting

---

## 📚 Metrik Evaluasi

Model dievaluasi menggunakan:

- **MAE (Mean Absolute Error)**
- **RMSE (Root Mean Squared Error)**
- **MAPE (Mean Absolute Percentage Error)**

Semakin kecil nilai ketiga metrik tersebut, semakin baik performa model.

---

## 👤 Author

**Dzulfi Khoiriyah Azzahra**

- GitHub : https://github.com/dzulfi02
- LinkedIn : www.linkedin.com/in/dzulfi-khoiriyah-azzahra
