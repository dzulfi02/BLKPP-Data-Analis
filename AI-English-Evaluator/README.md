# 📚 AI English Evaluator

Dashboard berbasis **Streamlit** untuk mengevaluasi kemampuan Bahasa Inggris (Writing & Speaking) menggunakan **Artificial Intelligence (LLM)**.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-green)

Link Demo: [https://itjvq95ck2nce2mefy5qlb.streamlit.app/]
---

## ✨ Fitur

| Fitur | Deskripsi |
|---|---|
| ✍️ **Writing Evaluation** | Analisis grammar, vocabulary, skor, dan saran perbaikan dari tulisan Bahasa Inggris. |
| 🎤 **Speaking Evaluation** | Upload audio `.wav`, otomatis ditranskripsi lalu dievaluasi seperti Writing. |
| 📜 **History** | Rekam jejak seluruh hasil evaluasi lengkap dengan ringkasan & filter tipe. |
| 📊 **Export / Download CSV** | Unduh riwayat evaluasi dalam format CSV. |
| 🎨 **UI Modern** | Tampilan dashboard dengan hero banner, kartu fitur, dan badge skor berwarna. |

---

## 🧠 Teknologi

- **Frontend / Dashboard:** [Streamlit](https://streamlit.io/)
- **AI Provider:** OpenRouter
- **LLM Model:** Google Gemini 2.5 Flash
- **Database:** SQLite (lihat `database.py`)
- **Bahasa:** Python 3.9+

---

## 📁 Struktur Proyek

```
.
├── app.py            # Entry point dashboard Streamlit
├── writing.py         # Logika evaluasi Writing (panggil LLM)
├── speaking.py        # Logika evaluasi Speaking (transkripsi + evaluasi)
├── database.py         # Setup database, simpan & ambil history, export CSV
├── audio/              # Folder penyimpanan sementara file audio upload
└── README.md
```

---

## ⚙️ Instalasi

1. **Clone / siapkan folder proyek**

   ```bash
   git clone <repo-url>
   cd ai-english-evaluator
   ```

2. **Buat virtual environment (opsional tapi disarankan)**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install streamlit pandas
   ```

   > Sesuaikan juga dependency tambahan yang dipakai di `writing.py`, `speaking.py`, dan `database.py` (misalnya SDK OpenRouter, library speech-to-text, dsb).

4. **Siapkan API Key**

   Jika `writing.py` / `speaking.py` memerlukan API key OpenRouter, buat file `.env` atau `secrets.toml` sesuai implementasi masing-masing, contoh:

   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

5. **Buat folder audio (jika belum ada)**

   ```bash
   mkdir audio
   ```

---

## ▶️ Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser pada `http://localhost:8501`.

---

## 🖥️ Cara Pakai

1. **Home** — Lihat ringkasan fitur dan info provider/model AI yang digunakan.
2. **Writing Evaluation** — Tempel tulisan Bahasa Inggris → klik **🚀 Evaluate** → lihat skor, feedback grammar, vocabulary, dan saran perbaikan.
3. **Speaking Evaluation** — Upload file audio `.wav` → klik **🎤 Evaluate Speaking** → lihat transcript dan hasil evaluasi.
4. **History** — Lihat seluruh riwayat evaluasi, filter berdasarkan tipe, lalu export/download sebagai CSV.

---

## 📊 Tentang Skor

Setiap evaluasi menghasilkan **Overall Score (0–100)** dengan indikator warna:

- 🟢 **80–100** → Sangat baik
- 🟡 **60–79** → Cukup baik
- 🔴 **< 60** → Perlu banyak perbaikan

---

## 👩‍💻 Author

**Dzulfi Khoiriyah Azzahra**
Developer & Author aplikasi ini.

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan pembelajaran/pengembangan pribadi. Silakan sesuaikan lisensi (MIT, dsb) sesuai kebutuhanmu.
