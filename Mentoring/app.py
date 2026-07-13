import streamlit as st
import joblib
from pathlib import Path

# ===========================
# Load Model
# ===========================
BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "model" / "logistic_regression.pkl")
vectorizer = joblib.load(BASE_DIR / "model" / "tfidf_vectorizer.pkl")

# ===========================
# Konfigurasi Halaman
# ===========================
st.set_page_config(
    page_title="Sentiment Analysis MBG",
    page_icon="💬",
    layout="centered"
)

# ===========================
# Header
# ===========================
st.title("💬 Analisis Sentimen Program Makan Bergizi Gratis")

st.markdown("""
Aplikasi ini digunakan untuk **menganalisis sentimen masyarakat terhadap Program Makan Bergizi Gratis (MBG)** berdasarkan komentar dari **YouTube**.

Model yang digunakan adalah **Logistic Regression** dengan ekstraksi fitur **TF-IDF** untuk mengklasifikasikan komentar ke dalam tiga kategori sentimen, yaitu **Positive**, **Neutral**, dan **Negative**.
""")

st.divider()

# ===========================
# Informasi Dataset
# ===========================
st.subheader("📁 Informasi Dataset")

col1, col2 = st.columns(2)

with col1:
    st.info("""
**📊 Dataset**
- Jumlah Data : 6.000 komentar
- Sumber Data : Komentar YouTube
- Jumlah Video : 2 video
""")

with col2:
    st.info("""
**🏷️ Label Sentimen**
- Positive
- Neutral
- Negative
""")

st.markdown("### 🎥 Video yang Dianalisis")

st.markdown("""
**1. TAK ADA MAKAN SIANG GRATIS: Kelindan Kepentingan di Balik Program MBG**  
**Channel:** Watchdoc Documentary

**2. Kroni Prabowo dalam Proyek Makan Bergizi Gratis (MBG): Bocor Alus Politik**  
**Channel:** Tempodotco
""")

st.divider()
# ===========================
# Contoh Input
# ===========================
st.subheader("💬 Contoh Komentar")

st.markdown("""
**😊 Positif**
> Program ini sangat membantu masyarakat dan layak diteruskan.

**😐 Netral**
> Program makan bergizi gratis mulai diterapkan di beberapa daerah.

**😠 Negatif**
> Program ini hanya menghabiskan anggaran negara.
""")

st.divider()

# ===========================
# Input User
# ===========================
st.subheader("✍ Masukkan Komentar")

text = st.text_area(
    "Komentar",
    placeholder="Contoh: Program ini sangat membantu masyarakat..."
)

# ===========================
# Prediksi
# ===========================
if st.button("🔍 Prediksi Sentimen"):

    if text.strip() == "":
        st.warning("⚠ Masukkan komentar terlebih dahulu.")
    else:

        vector = vectorizer.transform([text])

        prediction = model.predict(vector)[0]
        confidence = model.predict_proba(vector).max() * 100

        st.subheader("🎯 Hasil Prediksi")

        if prediction == "Positive":
            st.success(f"😊 **Sentimen : {prediction}**")

        elif prediction == "Negative":
            st.error(f"😠 **Sentimen : {prediction}**")

        else:
            st.info(f"😐 **Sentimen : {prediction}**")

        st.write(f"**Confidence Score : {confidence:.2f}%**")

st.divider()

# ===========================
# Informasi Model
# ===========================
st.subheader("📈 Informasi Model")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Model", "Logistic Regression")

with col2:
    st.metric("Fitur", "TF-IDF")

with col3:
    st.metric("Akurasi", "69%")

st.caption("""
Model dikembangkan menggunakan algoritma **Logistic Regression** dengan representasi fitur **TF-IDF** untuk melakukan klasifikasi sentimen terhadap komentar YouTube mengenai Program Makan Bergizi Gratis.
""")

st.divider()

# ===========================
# Footer
# ===========================
st.caption(
    """
**Dibuat oleh:** Dzulfi Khoiriyah Azzahra

**Dataset:** Komentar YouTube Program Makan Bergizi Gratis

© 2026
"""
)
