# 📊 Analisis Sentimen Komentar YouTube Menggunakan IndoBERT dan Machine Learning

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis sentimen masyarakat terhadap **Program Makan Bergizi Gratis (MBG)** berdasarkan komentar yang diperoleh dari platform YouTube.

Analisis dilakukan menggunakan model **IndoBERT** untuk proses pelabelan sentimen, kemudian dibandingkan performa beberapa algoritma Machine Learning untuk melakukan klasifikasi sentimen.

---

## 🎯 Tujuan

- Mengumpulkan komentar dari video YouTube yang membahas Program Makan Bergizi Gratis (MBG).
- Melakukan preprocessing terhadap data teks.
- Memberikan label sentimen menggunakan model IndoBERT.
- Melakukan analisis eksploratif terhadap hasil sentimen.
- Membangun model klasifikasi sentimen menggunakan Machine Learning.
- Melakukan deployment model menggunakan Streamlit.

---

## 📂 Dataset

Sumber data diperoleh dari komentar YouTube menggunakan library:

- youtube-comment-downloader

Jumlah data yang digunakan sekitar **6.000 komentar**.

---

## 🔄 Alur Pengerjaan

```
Scraping Data
      │
      ▼
Data Understanding (EDA)
      │
      ▼
Data Preprocessing
      │
      ▼
Pelabelan Sentimen (IndoBERT)
      │
      ▼
Exploratory Data Analysis (EDA)
      │
      ▼
Feature Engineering (TF-IDF)
      │
      ▼
Machine Learning
      │
      ├── Naive Bayes
      └── Logistic Regression
      │
      ▼
Evaluasi Model
      │
      ▼
Deployment Streamlit
```

---

## 🧹 Tahapan Preprocessing

Tahapan preprocessing yang dilakukan meliputi:

- Case Folding
- Cleaning Text
- Remove URL
- Remove Mention
- Remove Hashtag
- Remove Emoji
- Remove Number
- Remove Punctuation
- Tokenization
- Normalisasi Kata Slang
- Stopword Removal
- Stemming Bahasa Indonesia menggunakan Sastrawi

---

## 🤖 Pelabelan Sentimen

Pelabelan sentimen dilakukan menggunakan model **IndoBERT** sehingga setiap komentar memiliki tiga kategori sentimen, yaitu:

- 😊 Positive
- 😐 Neutral
- 😠 Negative

---

## ⚙️ Feature Engineering

Representasi teks dilakukan menggunakan:

- TF-IDF Vectorizer

---

## 🧠 Algoritma Machine Learning

Model yang digunakan pada penelitian ini adalah:

- Multinomial Naive Bayes
- Logistic Regression

---

## 📈 Evaluasi Model

Evaluasi dilakukan menggunakan beberapa metrik berikut:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

### Hasil Evaluasi

| Model | Accuracy |
|--------|----------|
| Logistic Regression | **0.69** |
| Naive Bayes | 0.66 |

Berdasarkan hasil evaluasi tersebut, **Logistic Regression** dipilih sebagai model terbaik dan digunakan pada tahap deployment.

---

## 🛠️ Teknologi yang Digunakan

- Python
- Google Colab
- Pandas
- NumPy
- Scikit-Learn
- Transformers
- IndoBERT
- Sastrawi
- Matplotlib
- WordCloud
- Streamlit

---

## 📁 Struktur Folder

```
Mentoring
│
├── Dataset
│      └── youtube_comment.csv
│
├── Model
│      ├── logistic_regression.pkl
│      └── tfidf.pkl
│
├── Notebook
│      └── Project_Sentiment_Mentoring.ipynb
│
├── app.py
├── requirements.txt
└── README.md
```

---


## 👨‍💻 Author

**Dzulfi Khoiriyah Azzahra**
