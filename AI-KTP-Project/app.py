import streamlit as st
from PIL import Image
import base64
import os
import json
import io
import sqlite3
import pandas as pd
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path


# =====================================
# LOAD ENVIRONMENT
# =====================================

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("⚠️ OPENROUTER_API_KEY tidak ditemukan. Tambahkan file .env dengan variabel OPENROUTER_API_KEY.")
    st.stop()


client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


# =====================================
# PAGE CONFIG (harus dipanggil sebelum elemen lain)
# =====================================

st.set_page_config(
    page_title="AI KTP OCR",
    page_icon="🪪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================
# CUSTOM STYLING
# =====================================

st.markdown("""
<style>
    /* Global */
    .stApp {
        background: linear-gradient(180deg, #f7f9fc 0%, #eef1f7 100%);
    }
    #MainMenu, footer {visibility: hidden;}

    /* Hero header */
    .hero-box {
        background: linear-gradient(120deg, #1f2a56 0%, #3453a3 55%, #4f7cd6 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.6rem;
        box-shadow: 0 12px 28px rgba(31, 42, 86, 0.25);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.85;
        margin-top: 0.4rem;
        font-weight: 400;
    }

    /* Section card */
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        box-shadow: 0 4px 16px rgba(31, 42, 86, 0.07);
        border: 1px solid rgba(31, 42, 86, 0.06);
        margin-bottom: 1.2rem;
    }

    .badge-ok {
        display: inline-block;
        background: #e5f7ec;
        color: #1c7a41;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 3px 4px 3px 0;
    }
    .badge-bad {
        display: inline-block;
        background: #fdecea;
        color: #c0392b;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 3px 4px 3px 0;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        text-align: center;
        box-shadow: 0 4px 14px rgba(31, 42, 86, 0.07);
        border: 1px solid rgba(31, 42, 86, 0.06);
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #1f2a56;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.4rem;
        border: none;
        background: linear-gradient(120deg, #2c5cc5, #4f7cd6);
        color: white;
        transition: 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(44, 92, 197, 0.35);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: #1f2a56;
    }
    section[data-testid="stSidebar"] * {
        color: #f0f2fa !important;
    }

    div[data-testid="stFileUploader"] {
        border: 2px dashed #4f7cd6;
        border-radius: 14px;
        padding: 0.6rem;
        background: #f5f8ff;
    }
</style>
""", unsafe_allow_html=True)


# =====================================
# DATABASE
# =====================================

def init_database():

    conn = sqlite3.connect(
        "ktp_database.db"
    )

    cursor = conn.cursor()


    # Kolom wajib minimal: ID, Nama, Nomor Dokumen, Jenis Dokumen,
    # Tanggal Upload, Status Validasi. Kolom tambahan (tempat_tgl_lahir,
    # jenis_kelamin, alamat, agama, pekerjaan) disimpan agar detail hasil
    # OCR tetap lengkap dan bisa ditelusuri.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ktp_data (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        nomor_dokumen TEXT,
        jenis_dokumen TEXT,
        tanggal_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status_validasi TEXT,
        tempat_tgl_lahir TEXT,
        jenis_kelamin TEXT,
        alamat TEXT,
        agama TEXT,
        pekerjaan TEXT

    )
    """)


    conn.commit()
    conn.close()



def save_database(data, jenis_dokumen, status_validasi):

    conn = sqlite3.connect(
        "ktp_database.db"
    )

    cursor = conn.cursor()


    cursor.execute("""

    INSERT INTO ktp_data
    (
    nama,
    nomor_dokumen,
    jenis_dokumen,
    status_validasi,
    tempat_tgl_lahir,
    jenis_kelamin,
    alamat,
    agama,
    pekerjaan
    )

    VALUES (?,?,?,?,?,?,?,?,?)

    """,

    (

    data.get("nama",""),
    data.get("nik",""),
    jenis_dokumen,
    status_validasi,
    data.get("tempat_tgl_lahir",""),
    data.get("jenis_kelamin",""),
    data.get("alamat",""),
    data.get("agama",""),
    data.get("pekerjaan","")

    ))


    conn.commit()
    conn.close()



def read_database():

    conn = sqlite3.connect(
        "ktp_database.db"
    )


    df = pd.read_sql_query(

        """
        SELECT
            id,
            nama,
            nomor_dokumen,
            jenis_dokumen,
            tanggal_upload,
            status_validasi,
            tempat_tgl_lahir,
            jenis_kelamin,
            alamat,
            agama,
            pekerjaan
        FROM ktp_data
        ORDER BY id DESC
        """,

        conn

    )


    conn.close()

    return df



init_database()



# =====================================
# IMAGE ENCODE
# =====================================

def encode_image(image_file):

    image = Image.open(image_file)

    image.thumbnail(
        (1200,1200)
    )

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="JPEG"
    )


    return base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")



# =====================================
# CLEAN JSON RESPONSE
# =====================================

def clean_json(text):

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    return json.loads(
        text.strip()
    )



# =====================================
# AI CLASSIFICATION
# =====================================

def classify_document(base64_image):


    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[

            {

            "role":"user",

            "content":[


                {

                "type":"text",

                "text":"""

Apakah gambar ini merupakan KTP Indonesia?

Jawab hanya JSON:

{
"is_ktp": true,
"confidence":0.0
}

atau

{
"is_ktp": false,
"confidence":0.0
}

Jangan memberikan penjelasan.

"""

                },


                {

                "type":"image_url",

                "image_url":{

                    "url":
                    f"data:image/jpeg;base64,{base64_image}"

                }

                }

            ]

            }

        ]

    )


    return clean_json(
        response.choices[0].message.content
    )



# =====================================
# AI OCR
# =====================================

def extract_ocr(base64_image):


    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[

            {

            "role":"user",

            "content":[


            {

            "type":"text",

            "text":"""

Anda adalah AI OCR KTP Indonesia.

Ekstrak semua informasi KTP.

Jawab hanya JSON.

Jika tidak terbaca isi "".

Format:

{
"nik":"",
"nama":"",
"tempat_tgl_lahir":"",
"jenis_kelamin":"",
"golongan_darah":"",
"alamat":"",
"rt":"",
"rw":"",
"kelurahan":"",
"kecamatan":"",
"agama":"",
"status_perkawinan":"",
"pekerjaan":"",
"kewarganegaraan":"",
"berlaku_hingga":""
}

"""

            },


            {

            "type":"image_url",

            "image_url":{

                "url":
                f"data:image/jpeg;base64,{base64_image}"

            }

            }

            ]

            }

        ]

    )


    return clean_json(
        response.choices[0].message.content
    )



# =====================================
# VALIDATION
# =====================================

def validate_data(data):
    """Mengembalikan list tuple (label, is_valid) agar mudah dirender sebagai badge."""

    result = []

    if len(data.get("nik", "")) == 16:
        result.append(("NIK valid", True))
    else:
        result.append(("NIK tidak valid", False))

    if data.get("nama"):
        result.append(("Nama terbaca", True))
    else:
        result.append(("Nama tidak terbaca", False))

    if data.get("alamat"):
        result.append(("Alamat terbaca", True))
    else:
        result.append(("Alamat tidak terbaca", False))

    return result


def render_badges(validation_results):
    html = ""
    for label, is_valid in validation_results:
        css_class = "badge-ok" if is_valid else "badge-bad"
        icon = "✅" if is_valid else "❌"
        html += f'<span class="{css_class}">{icon} {label}</span>'
    st.markdown(html, unsafe_allow_html=True)


def overall_status(validation_results):
    """Status validasi ringkas untuk disimpan ke kolom database."""
    return "Valid" if all(is_valid for _, is_valid in validation_results) else "Tidak Valid"



# =====================================
# HERO HEADER
# =====================================

st.markdown("""
<div class="hero-box">
    <p class="hero-title">🪪 AI KTP OCR Dashboard</p>
    <p class="hero-subtitle">Klasifikasi &amp; ekstraksi data KTP Indonesia secara otomatis menggunakan AI Vision — didukung GPT-4o-mini via OpenRouter.</p>
</div>
""", unsafe_allow_html=True)


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.markdown("### 🪪 AI KTP OCR")
    st.caption("Dashboard klasifikasi & ekstraksi KTP")
    st.markdown("---")

    menu = st.radio(
        "Menu",
        ["🏠 Home", "📤 Upload KTP", "🗄️ Database"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Alur proses:**")
    st.markdown(
        "1. Upload gambar KTP\n"
        "2. AI mengklasifikasi dokumen\n"
        "3. AI melakukan OCR\n"
        "4. Data divalidasi & disimpan"
    )
    st.markdown("---")
    st.caption(f"Model: `openai/gpt-4o-mini`\nvia OpenRouter")


# =====================================
# HOME PAGE
# =====================================

if menu == "🏠 Home":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("👋 Tentang Aplikasi")
    st.markdown("""
**AI KTP OCR Dashboard** adalah aplikasi berbasis AI Vision untuk membantu
mengklasifikasikan dan mengekstrak data dari gambar KTP (Kartu Tanda Penduduk)
Indonesia secara otomatis. Cukup upload foto KTP, aplikasi akan:

1. **Mengklasifikasikan** apakah gambar tersebut benar merupakan KTP Indonesia.
2. **Melakukan OCR** untuk mengekstrak data seperti NIK, nama, alamat, dan informasi lainnya.
3. **Memvalidasi** kelengkapan & format data hasil OCR.
4. **Menyimpan** hasilnya secara otomatis ke dalam database.
""")
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🤖 Informasi Model AI")
        st.markdown("""
| Komponen | Detail |
|---|---|
| **Model** | `openai/gpt-4o-mini` |
| **Provider** | OpenRouter |
| **Kemampuan** | Vision (image understanding) + text generation |
| **Fungsi 1** | Klasifikasi dokumen (KTP / bukan KTP) |
| **Fungsi 2** | OCR — ekstraksi field data KTP ke format JSON |
""")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🗂️ Struktur Data Tersimpan")
        st.markdown("""
Setiap dokumen yang berhasil diproses disimpan ke database dengan kolom:

- **ID** — nomor urut data
- **Nama** — nama pemilik dokumen
- **Nomor Dokumen** — NIK
- **Jenis Dokumen** — jenis dokumen yang terdeteksi (KTP)
- **Tanggal Upload** — waktu data disimpan
- **Status Validasi** — Valid / Tidak Valid
""")
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================
# UPLOAD PAGE
# =====================================

elif menu == "📤 Upload KTP":

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📤 Upload Gambar KTP")

        uploaded_file = st.file_uploader(
            "Seret & lepas atau pilih gambar KTP (jpg, jpeg, png)",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Preview KTP", use_container_width=True)
            process_clicked = st.button("🚀 Proses Dokumen", use_container_width=True)
        else:
            st.info("Silakan upload gambar KTP terlebih dahulu untuk memulai proses.")
            process_clicked = False

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if uploaded_file and process_clicked:

            base64_image = encode_image(uploaded_file)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("📌 Hasil Klasifikasi")

            with st.spinner("Melakukan klasifikasi dokumen..."):
                classification = classify_document(base64_image)

            confidence = float(classification.get("confidence", 0))

            if classification.get("is_ktp"):
                st.success("✅ Dokumen terdeteksi sebagai **KTP Indonesia**")
                st.progress(min(max(confidence, 0.0), 1.0), text=f"Tingkat keyakinan: {confidence*100:.1f}%")
            else:
                st.error("❌ Dokumen **bukan** KTP Indonesia")
                st.progress(min(max(confidence, 0.0), 1.0), text=f"Tingkat keyakinan: {confidence*100:.1f}%")

            st.markdown('</div>', unsafe_allow_html=True)

            if classification.get("is_ktp"):

                with st.spinner("Melakukan OCR terhadap KTP..."):
                    data = extract_ocr(base64_image)

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📄 Hasil OCR")

                df = pd.DataFrame(
                    data.items(),
                    columns=["Field", "Value"]
                )

                st.dataframe(df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

                validation_results = validate_data(data)
                status_validasi = overall_status(validation_results)

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("🔍 Validasi Data")
                render_badges(validation_results)
                st.markdown(
                    f'<span class="{"badge-ok" if status_validasi == "Valid" else "badge-bad"}">'
                    f'Status Validasi: {status_validasi}</span>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

                save_database(data, jenis_dokumen="KTP", status_validasi=status_validasi)
                st.success("💾 Data berhasil disimpan ke database")

                csv = df.to_csv(index=False)
                st.download_button(
                    "⬇️ Export CSV",
                    csv,
                    "hasil_ktp.csv",
                    "text/csv",
                    use_container_width=True
                )
        elif not uploaded_file:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("📌 Hasil akan tampil di sini")
            st.caption("Upload gambar KTP di panel kiri, lalu klik **Proses Dokumen** untuk melihat hasil klasifikasi, OCR, dan validasi.")
            st.markdown('</div>', unsafe_allow_html=True)


# =====================================
# DATABASE PAGE
# =====================================

else:

    df_database = read_database()

    total_records = len(df_database)
    valid_count = int((df_database["status_validasi"] == "Valid").sum()) if total_records else 0
    invalid_count = total_records - valid_count if total_records else 0
    last_entry = df_database["tanggal_upload"].iloc[0] if total_records else "-"

    m1, m2, m3, m4 = st.columns(4)
    for col, value, label in zip(
        [m1, m2, m3, m4],
        [total_records, valid_count, invalid_count, last_entry],
        ["Total Data Tersimpan", "Status Valid", "Status Tidak Valid", "Upload Terakhir"]
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🗄️ Database KTP")

    if total_records:
        search = st.text_input("🔎 Cari berdasarkan nama atau nomor dokumen", "")
        if search:
            mask = (
                df_database["nama"].astype(str).str.contains(search, case=False, na=False)
                | df_database["nomor_dokumen"].astype(str).str.contains(search, case=False, na=False)
            )
            df_display = df_database[mask]
        else:
            df_display = df_database

        st.dataframe(df_display, use_container_width=True, hide_index=True)

        csv_all = df_database.to_csv(index=False)
        st.download_button(
            "⬇️ Export Semua Data (CSV)",
            csv_all,
            "database_ktp.csv",
            "text/csv"
        )
    else:
        st.info("Belum ada data KTP yang tersimpan. Upload dan proses KTP terlebih dahulu di menu **Upload KTP**.")

    st.markdown('</div>', unsafe_allow_html=True)
