import streamlit as st
from PIL import Image
import base64
import os
import re
import json
import io
import sqlite3
import calendar
import pandas as pd
from datetime import datetime, date

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
    .stApp {
        background: linear-gradient(180deg, #f7f9fc 0%, #eef1f7 100%);
    }
    #MainMenu, footer {visibility: hidden;}

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

    .status-pill-valid {
        display: inline-block;
        background: #1c7a41;
        color: white;
        padding: 6px 18px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
    }
    .status-pill-invalid {
        display: inline-block;
        background: #c0392b;
        color: white;
        padding: 6px 18px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
    }

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
# Kolom wajib minimal: ID, Nama, Nomor Dokumen, Jenis Dokumen, Tanggal Upload,
# Status Validasi. Kolom tambahan disimpan agar detail hasil OCR tetap lengkap.
# Sesuai workflow project: hanya data dengan status VALID yang disimpan ke DB.

def init_database():

    conn = sqlite3.connect("ktp_database.db")
    cursor = conn.cursor()

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
        golongan_darah TEXT,
        alamat TEXT,
        rt TEXT,
        rw TEXT,
        kelurahan TEXT,
        kecamatan TEXT,
        agama TEXT,
        status_perkawinan TEXT,
        pekerjaan TEXT,
        kewarganegaraan TEXT,
        berlaku_hingga TEXT
    )
    """)

    conn.commit()

    # Migrasi otomatis: jika tabel dibuat oleh versi aplikasi sebelumnya
    # (skema lama tanpa sebagian kolom), tambahkan kolom yang belum ada
    # tanpa menghapus data yang sudah tersimpan.
    required_columns = {
        "nama": "TEXT",
        "nomor_dokumen": "TEXT",
        "jenis_dokumen": "TEXT",
        "tanggal_upload": "TIMESTAMP",
        "status_validasi": "TEXT",
        "tempat_tgl_lahir": "TEXT",
        "jenis_kelamin": "TEXT",
        "golongan_darah": "TEXT",
        "alamat": "TEXT",
        "rt": "TEXT",
        "rw": "TEXT",
        "kelurahan": "TEXT",
        "kecamatan": "TEXT",
        "agama": "TEXT",
        "status_perkawinan": "TEXT",
        "pekerjaan": "TEXT",
        "kewarganegaraan": "TEXT",
        "berlaku_hingga": "TEXT",
    }

    cursor.execute("PRAGMA table_info(ktp_data)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    for col_name, col_type in required_columns.items():
        if col_name not in existing_columns:
            cursor.execute(f"ALTER TABLE ktp_data ADD COLUMN {col_name} {col_type}")

    conn.commit()
    conn.close()


def save_database(data, jenis_dokumen, status_validasi):

    conn = sqlite3.connect("ktp_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ktp_data
    (nama, nomor_dokumen, jenis_dokumen, status_validasi,
     tempat_tgl_lahir, jenis_kelamin, golongan_darah, alamat,
     rt, rw, kelurahan, kecamatan, agama, status_perkawinan,
     pekerjaan, kewarganegaraan, berlaku_hingga)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
        data.get("nama", ""),
        data.get("nik", ""),
        jenis_dokumen,
        status_validasi,
        data.get("tempat_tgl_lahir", ""),
        data.get("jenis_kelamin", ""),
        data.get("golongan_darah", ""),
        data.get("alamat", ""),
        data.get("rt", ""),
        data.get("rw", ""),
        data.get("kelurahan", ""),
        data.get("kecamatan", ""),
        data.get("agama", ""),
        data.get("status_perkawinan", ""),
        data.get("pekerjaan", ""),
        data.get("kewarganegaraan", ""),
        data.get("berlaku_hingga", "")
    ))

    conn.commit()
    conn.close()


def read_database():

    conn = sqlite3.connect("ktp_database.db")

    df = pd.read_sql_query("""
        SELECT id, nama, nomor_dokumen, jenis_dokumen, tanggal_upload,
               status_validasi, tempat_tgl_lahir, jenis_kelamin,
               golongan_darah, alamat, rt, rw, kelurahan, kecamatan,
               agama, status_perkawinan, pekerjaan, kewarganegaraan,
               berlaku_hingga
        FROM ktp_data
        ORDER BY id DESC
    """, conn)

    conn.close()

    return df


init_database()



# =====================================
# IMAGE ENCODE
# =====================================

def encode_image(image_file):

    image = Image.open(image_file)
    image.thumbnail((1200, 1200))

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")



# =====================================
# CLEAN JSON RESPONSE
# =====================================

def clean_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text.strip())



# =====================================
# AI CLASSIFICATION (AI Vision)
# =====================================

def classify_document(base64_image):

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
Apakah gambar ini merupakan KTP Indonesia?

Jawab hanya JSON:

{
"is_ktp": true,
"confidence": 0.0
}

atau

{
"is_ktp": false,
"confidence": 0.0
}

Jangan memberikan penjelasan.
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    return clean_json(response.choices[0].message.content)



# =====================================
# AI OCR EXTRACTION (AI Vision, tanpa Regex)
# =====================================

def extract_ocr(base64_image):

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
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
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    return clean_json(response.choices[0].message.content)



# =====================================
# BUSINESS RULE VALIDATION (Python, tanpa AI)
# =====================================
# Struktur NIK KTP Indonesia (16 digit): PPRRSSDDMMYYXXXX
#   PP-RR-SS = kode wilayah (provinsi-kab/kota-kecamatan)
#   DD-MM-YY = tanggal lahir (DD+40 untuk perempuan)
#   XXXX     = nomor urut

def _parse_date_ddmmyyyy(text):
    """Ambil objek date pertama berformat DD-MM-YYYY / DD/MM/YYYY dari sebuah teks."""
    if not text:
        return None
    match = re.search(r"(\d{2})[-/](\d{2})[-/](\d{4})", text)
    if not match:
        return None
    day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
    try:
        return date(year, month, day)
    except ValueError:
        return None


def validate_ktp(data):
    """
    Menjalankan Business Rule Validation terhadap hasil OCR KTP.
    Mengembalikan list of dict: {rule, is_valid, message}
    """

    results = []
    nik = str(data.get("nik", "")).strip()

    # 1. Panjang NIK harus 16 digit
    nik_length_valid = len(nik) == 16
    results.append({
        "rule": "Panjang NIK (16 digit)",
        "is_valid": nik_length_valid,
        "message": "NIK terdiri dari 16 digit" if nik_length_valid
                    else f"NIK tidak valid — panjang {len(nik)} digit, seharusnya 16 digit"
    })

    # 2. NIK hanya boleh berisi angka
    nik_numeric_valid = nik.isdigit()
    results.append({
        "rule": "NIK Hanya Angka",
        "is_valid": nik_numeric_valid,
        "message": "NIK hanya berisi angka" if nik_numeric_valid
                    else "NIK tidak valid — mengandung karakter selain angka"
    })

    # Ekstraksi tanggal lahir & jenis kelamin dari struktur NIK
    nik_birthdate = None
    nik_gender = None
    nik_date_valid = False

    if nik_numeric_valid and nik_length_valid:
        raw_day = int(nik[6:8])
        month = int(nik[8:10])
        year_yy = int(nik[10:12])

        nik_gender = "PEREMPUAN" if raw_day > 40 else "LAKI-LAKI"
        day = raw_day - 40 if raw_day > 40 else raw_day

        current_yy = datetime.now().year % 100
        year_full = 2000 + year_yy if year_yy <= current_yy else 1900 + year_yy

        try:
            max_day = calendar.monthrange(year_full, month)[1] if 1 <= month <= 12 else 0
            if 1 <= day <= max_day and 1 <= month <= 12:
                nik_birthdate = date(year_full, month, day)
                nik_date_valid = True
        except ValueError:
            nik_date_valid = False

    # 3. Validasi tanggal lahir dari NIK
    results.append({
        "rule": "Tanggal Lahir dari NIK",
        "is_valid": nik_date_valid,
        "message": f"Tanggal lahir sesuai struktur NIK: {nik_birthdate.strftime('%d-%m-%Y')}" if nik_date_valid
                    else "Tanggal lahir tidak valid berdasarkan struktur NIK"
    })

    # 4. Validasi jenis kelamin berdasarkan NIK
    jenis_kelamin_ocr = str(data.get("jenis_kelamin", "")).strip().upper()
    gender_match = False
    if nik_gender and jenis_kelamin_ocr:
        is_female_ocr = any(k in jenis_kelamin_ocr for k in ["PEREMPUAN", "WANITA", "P"]) and \
                         not any(k in jenis_kelamin_ocr for k in ["LAKI"])
        is_male_ocr = any(k in jenis_kelamin_ocr for k in ["LAKI", "PRIA"])
        if nik_gender == "PEREMPUAN" and is_female_ocr:
            gender_match = True
        elif nik_gender == "LAKI-LAKI" and is_male_ocr:
            gender_match = True

    results.append({
        "rule": "Jenis Kelamin sesuai NIK",
        "is_valid": gender_match,
        "message": f"Jenis kelamin ({jenis_kelamin_ocr or '-'}) sesuai dengan NIK ({nik_gender or '-'})" if gender_match
                    else f"Jenis kelamin tidak sesuai dengan NIK (harusnya {nik_gender or '-'}, hasil OCR: {jenis_kelamin_ocr or '-'})"
    })

    # 5. Validasi format tanggal pada field tempat_tgl_lahir
    ocr_birthdate = _parse_date_ddmmyyyy(data.get("tempat_tgl_lahir", ""))
    format_tanggal_valid = ocr_birthdate is not None
    results.append({
        "rule": "Format Tanggal Lahir",
        "is_valid": format_tanggal_valid,
        "message": f"Format tanggal valid: {ocr_birthdate.strftime('%d-%m-%Y')}" if format_tanggal_valid
                    else "Format tanggal lahir tidak dikenali (harus DD-MM-YYYY)"
    })

    # 5b. Kecocokan tanggal lahir NIK vs field tempat_tgl_lahir
    birthdate_match = bool(nik_date_valid and format_tanggal_valid and nik_birthdate == ocr_birthdate)
    results.append({
        "rule": "Kecocokan Tanggal Lahir & NIK",
        "is_valid": birthdate_match,
        "message": "Tanggal lahir pada NIK cocok dengan data OCR" if birthdate_match
                    else "Tanggal lahir pada NIK tidak cocok dengan data OCR"
    })

    # 6. Validasi status berlaku (berlaku_hingga)
    berlaku_hingga = str(data.get("berlaku_hingga", "")).strip().upper()
    if not berlaku_hingga:
        berlaku_valid = False
        berlaku_msg = "Kolom berlaku hingga tidak terbaca"
    elif "SEUMUR HIDUP" in berlaku_hingga:
        berlaku_valid = True
        berlaku_msg = "Berlaku seumur hidup"
    else:
        expiry = _parse_date_ddmmyyyy(berlaku_hingga)
        if expiry is None:
            berlaku_valid = False
            berlaku_msg = "Format tanggal berlaku hingga tidak dikenali"
        elif expiry < date.today():
            berlaku_valid = False
            berlaku_msg = f"KTP sudah kedaluwarsa sejak {expiry.strftime('%d-%m-%Y')}"
        else:
            berlaku_valid = True
            berlaku_msg = f"Masih berlaku hingga {expiry.strftime('%d-%m-%Y')}"

    results.append({
        "rule": "Status Berlaku",
        "is_valid": berlaku_valid,
        "message": berlaku_msg
    })

    return results


def overall_status(validation_results):
    """VALID hanya jika seluruh rule lolos, selebihnya INVALID."""
    return "VALID" if all(r["is_valid"] for r in validation_results) else "INVALID"


def render_validation_table(validation_results):
    df_val = pd.DataFrame([
        {
            "Rule": r["rule"],
            "Status": "VALID" if r["is_valid"] else "INVALID",
            "Keterangan": r["message"]
        }
        for r in validation_results
    ])

    def highlight_status(val):
        if val == "VALID":
            return "background-color:#e5f7ec;color:#1c7a41;font-weight:600;"
        return "background-color:#fdecea;color:#c0392b;font-weight:600;"

    st.dataframe(
        df_val.style.map(highlight_status, subset=["Status"]),
        use_container_width=True,
        hide_index=True
    )



# =====================================
# HERO HEADER
# =====================================

st.markdown("""
<div class="hero-box">
    <p class="hero-title">🪪 AI KTP OCR Dashboard</p>
    <p class="hero-subtitle">AI Document Classification &amp; OCR — klasifikasi, ekstraksi, dan validasi data KTP Indonesia secara otomatis menggunakan AI Vision (GPT-4o-mini via OpenRouter).</p>
</div>
""", unsafe_allow_html=True)


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.markdown("### 🪪 AI KTP OCR")
    st.caption("AI Document Classification & OCR")
    st.markdown("---")

    menu = st.radio(
        "Menu",
        ["🏠 Home", "📤 Upload Image", "🗄️ Database History"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Workflow:**")
    st.markdown(
        "1. Upload Image\n"
        "2. AI Classification\n"
        "3. OCR Extraction\n"
        "4. Validation Rule\n"
        "5. Save Database (jika VALID)"
    )
    st.markdown("---")
    st.caption("Model: `openai/gpt-4o-mini`\nvia OpenRouter")


# =====================================
# HOME PAGE
# =====================================

if menu == "🏠 Home":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("👋 Tentang Aplikasi")
    st.markdown("""
**AI KTP OCR Dashboard** adalah implementasi *AI Document Classification & OCR*
menggunakan OpenRouter. Aplikasi ini membantu mengklasifikasikan dan mengekstrak
data dari gambar KTP (Kartu Tanda Penduduk) Indonesia secara otomatis, lalu
memvalidasi hasilnya menggunakan **Business Rule** sebelum disimpan ke database.

Alur kerja aplikasi:

1. **Upload Image** — pengguna mengunggah gambar dokumen.
2. **AI Classification** — AI menganalisis apakah gambar merupakan KTP atau bukan.
3. **OCR Extraction** — jika terdeteksi KTP, AI mengekstrak seluruh informasi ke format JSON.
4. **Validation Rule** — data hasil OCR divalidasi menggunakan aturan bisnis (business rules) di Python.
5. **Save Database** — jika seluruh validasi **VALID**, data disimpan ke database. Jika **INVALID**, aplikasi menampilkan pesan error dan data tidak disimpan.
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
| **Kemampuan** | AI Vision (image understanding) + text generation |
| **Fungsi 1** | Klasifikasi dokumen (KTP / Bukan KTP) |
| **Fungsi 2** | OCR — ekstraksi field data KTP ke format JSON |
| **Validasi** | Business rule berbasis Python (bukan AI/regex OCR) |
""")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🗂️ Struktur Data Tersimpan")
        st.markdown("""
Dokumen dengan status validasi **VALID** disimpan ke database dengan kolom:

- **ID** — nomor urut data
- **Nama** — nama pemilik dokumen
- **Nomor Dokumen** — NIK
- **Jenis Dokumen** — jenis dokumen terdeteksi (KTP)
- **Tanggal Upload** — waktu data disimpan
- **Status Validasi** — VALID
""")
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================
# UPLOAD IMAGE PAGE
# =====================================

elif menu == "📤 Upload Image":

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📤 Upload Image")

        uploaded_file = st.file_uploader(
            "Upload gambar dokumen (jpg, jpeg, png)",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Preview Dokumen", use_container_width=True)
            process_clicked = st.button("🚀 Proses Dokumen", use_container_width=True)
        else:
            st.info("Silakan upload gambar dokumen terlebih dahulu untuk memulai proses.")
            process_clicked = False

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if uploaded_file and process_clicked:

            base64_image = encode_image(uploaded_file)

            # ---------- CLASSIFICATION ----------
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("📌 Classification")

            with st.spinner("Melakukan klasifikasi dokumen..."):
                classification = classify_document(base64_image)

            confidence = float(classification.get("confidence", 0))
            is_ktp = bool(classification.get("is_ktp"))

            prediction_label = "KTP" if is_ktp else "Bukan KTP"
            if is_ktp:
                st.success(f"✅ Prediction: **{prediction_label}**")
            else:
                st.error(f"❌ Prediction: **{prediction_label}**")

            st.progress(min(max(confidence, 0.0), 1.0), text=f"Tingkat keyakinan: {confidence*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

            if not is_ktp:
                st.warning("⛔ Proses dihentikan — gambar bukan dokumen target (KTP), OCR tidak dijalankan.")

            if is_ktp:

                # ---------- OCR RESULT ----------
                with st.spinner("Melakukan OCR terhadap dokumen..."):
                    data = extract_ocr(base64_image)

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📄 OCR Result")

                df = pd.DataFrame(data.items(), columns=["Field", "Value"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # ---------- VALIDATION RESULT ----------
                validation_results = validate_ktp(data)
                status_validasi = overall_status(validation_results)

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("✅ Validation Result")

                render_validation_table(validation_results)

                pill_class = "status-pill-valid" if status_validasi == "VALID" else "status-pill-invalid"
                st.markdown(
                    f'<br><span class="{pill_class}">Status Akhir: {status_validasi}</span>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

                # ---------- SAVE / ERROR ----------
                if status_validasi == "VALID":
                    save_database(data, jenis_dokumen="KTP", status_validasi=status_validasi)
                    st.success("💾 Data VALID — berhasil disimpan ke database")

                    csv = df.to_csv(index=False)
                    st.download_button(
                        "⬇️ Export CSV",
                        csv,
                        "hasil_ktp.csv",
                        "text/csv",
                        use_container_width=True
                    )
                else:
                    failed_rules = [r["message"] for r in validation_results if not r["is_valid"]]
                    st.error(
                        "❌ Data **INVALID** — tidak disimpan ke database. Rincian error:\n\n"
                        + "\n".join(f"- {msg}" for msg in failed_rules)
                    )

        elif not uploaded_file:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("📌 Hasil akan tampil di sini")
            st.caption("Upload gambar dokumen di panel kiri, lalu klik **Proses Dokumen** untuk melihat hasil Classification, OCR Result, dan Validation Result.")
            st.markdown('</div>', unsafe_allow_html=True)


# =====================================
# DATABASE HISTORY PAGE
# =====================================

else:

    try:
        df_database = read_database()
    except Exception as e:
        st.error(f"⚠️ Gagal membaca database: {e}")
        st.info("Coba hapus file `ktp_database.db` lama lalu jalankan ulang aplikasi jika masalah berlanjut.")
        st.stop()

    total_records = len(df_database)
    valid_count = int((df_database["status_validasi"] == "VALID").sum()) if total_records else 0
    invalid_count = total_records - valid_count if total_records else 0
    last_entry = df_database["tanggal_upload"].iloc[0] if total_records else "-"

    m1, m2, m3, m4 = st.columns(4)
    for col, value, label in zip(
        [m1, m2, m3, m4],
        [total_records, valid_count, invalid_count, last_entry],
        ["Total Data Tersimpan", "Status VALID", "Status INVALID", "Upload Terakhir"]
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
    st.subheader("🗄️ Database History")
    st.caption("Menampilkan seluruh hasil OCR yang telah tersimpan (status VALID).")

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
        st.info("Belum ada data KTP yang tersimpan. Upload dan proses dokumen terlebih dahulu di menu **Upload Image**.")

    st.markdown('</div>', unsafe_allow_html=True)
