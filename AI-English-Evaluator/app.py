import streamlit as st
import pandas as pd
from datetime import datetime

from writing import evaluate_writing
from database import (
    create_database,
    save_result,
    get_history,
    export_history
)
from speaking import evaluate_speaking

# =====================================
# Konfigurasi Halaman
# =====================================
st.set_page_config(
    page_title="AI English Evaluator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Membuat database jika belum ada
create_database()

# =====================================
# Global CSS (biar tampilan lebih rapi & konsisten)
# =====================================
st.markdown("""
<style>
    /* Sembunyikan branding default Streamlit yang mengganggu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Font & spacing umum */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(49, 51, 63, 0.1);
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 0.95rem;
    }

    /* ===== Hero banner (Home) ===== */
    .hero-banner {
        background: linear-gradient(135deg, #6a5cff 0%, #8f6bff 45%, #b06bff 100%);
        border-radius: 20px;
        padding: 2.4rem 2.2rem;
        color: #ffffff;
        margin-bottom: 1.6rem;
        box-shadow: 0 12px 30px rgba(106, 92, 255, 0.28);
    }
    .hero-banner h1 {
        color: #ffffff;
        font-size: 2.1rem;
        margin-bottom: 0.4rem;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.9);
        font-size: 1.02rem;
        margin-bottom: 0;
    }
    .hero-pill {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 999px;
        padding: 0.25rem 0.9rem;
        font-size: 0.8rem;
        margin-bottom: 0.9rem;
        backdrop-filter: blur(4px);
    }

    /* Non-home page hero (lebih ringkas) */
    .page-hero {
        background: linear-gradient(120deg, #6a5cff10, #b06bff10);
        border: 1px solid rgba(106, 92, 255, 0.15);
        border-radius: 16px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1.6rem;
    }
    .page-hero h1 { margin-bottom: 0.15rem; font-size: 1.7rem; }
    .page-hero p { color: rgba(49, 51, 63, 0.65); margin-bottom: 0; }

    /* Card umum */
    .app-card {
        background: var(--background-color, #ffffff);
        border: 1px solid rgba(49, 51, 63, 0.12);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }

    /* Feature card di Home */
    .feature-card {
        border: 1px solid rgba(49, 51, 63, 0.12);
        border-radius: 14px;
        padding: 1.3rem 1.1rem;
        text-align: center;
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(106, 92, 255, 0.15);
    }
    .feature-card h4 { margin-bottom: 0.3rem; }
    .feature-card p { color: rgba(49, 51, 63, 0.65); font-size: 0.9rem; margin: 0; }

    /* Badge skor */
    .score-badge {
        display: inline-block;
        padding: 0.35rem 1rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .score-high   { background: #d4f4dd; color: #157347; }
    .score-mid    { background: #fff3cd; color: #997404; }
    .score-low    { background: #f8d7da; color: #b02a37; }

    /* Judul halaman */
    .page-title { margin-bottom: 0.2rem; }
    .page-subtitle { color: rgba(49, 51, 63, 0.6); margin-bottom: 1.5rem; }

    /* Author card di sidebar */
    .author-card {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        background: linear-gradient(135deg, #6a5cff12, #b06bff12);
        border: 1px solid rgba(106, 92, 255, 0.2);
        border-radius: 14px;
        padding: 0.7rem 0.9rem;
        margin-top: 0.5rem;
    }
    .author-avatar {
        width: 38px;
        height: 38px;
        min-width: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6a5cff, #b06bff);
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .author-name { font-weight: 600; font-size: 0.85rem; line-height: 1.2; margin: 0; }
    .author-role { font-size: 0.72rem; color: rgba(49, 51, 63, 0.6); margin: 0; }

    /* Footer credit di bawah tiap halaman */
    .app-footer {
        text-align: center;
        color: rgba(49, 51, 63, 0.45);
        font-size: 0.8rem;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(49, 51, 63, 0.08);
    }

    hr { margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)


def score_class(score: float) -> str:
    """Tentukan kelas warna badge berdasarkan skor."""
    if score >= 80:
        return "score-high"
    if score >= 60:
        return "score-mid"
    return "score-low"


def render_score_badge(score: float):
    st.markdown(
        f'<span class="score-badge {score_class(score)}">⭐ {score}/100</span>',
        unsafe_allow_html=True
    )


def render_footer():
    st.markdown(
        '<div class="app-footer">📚 AI English Evaluator &nbsp;•&nbsp; '
        'Dibuat dengan ❤️ oleh <b>Dzulfi Khoiriyah Azzahra</b></div>',
        unsafe_allow_html=True
    )


def render_feedback_section(result: dict):
    """Tampilkan hasil evaluasi (grammar, vocabulary, suggestion) secara rapi."""
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### 📝 Grammar")
            st.write(result["grammar"])

    with col2:
        with st.container(border=True):
            st.markdown("#### 📖 Vocabulary")
            st.write(result["vocabulary"])

    with st.container(border=True):
        st.markdown("#### 💡 Improvement Suggestion")
        st.write(result["suggestion"])


# =====================================
# Sidebar
# =====================================
with st.sidebar:
    st.markdown("## 📚 AI English Evaluator")
    st.caption("Evaluasi Writing & Speaking berbasis AI")
    st.divider()

    menu = st.radio(
        "Pilih Menu",
        [
            "🏠 Home",
            "✍️ Writing Evaluation",
            "🎤 Speaking Evaluation",
            "📜 History"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.caption("⚙️ Provider: **OpenRouter**")
    st.caption("🤖 Model: **Google Gemini 2.5 Flash**")

    st.markdown(
        """
        <div class="author-card">
            <div class="author-avatar">DKA</div>
            <div>
                <p class="author-name">Dzulfi Khoiriyah Azzahra</p>
                <p class="author-role">Developer & Author</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================
# Home
# =====================================
if menu == "🏠 Home":

    st.markdown(
        """
        <div class="hero-banner">
            <span class="hero-pill">✨ Powered by Google Gemini 2.5 Flash</span>
            <h1>📚 AI English Evaluator</h1>
            <p>Evaluasi kemampuan Bahasa Inggris kamu secara instan menggunakan Artificial Intelligence (LLM) —
            mulai dari Writing sampai Speaking, semua dalam satu dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✨ Fitur Utama")

    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("✍️", "Writing Evaluation", "Analisis grammar, vocabulary, dan saran perbaikan tulisan."),
        ("🎤", "Speaking Evaluation", "Transkripsi otomatis + evaluasi kemampuan berbicara."),
        ("📜", "History", "Rekam jejak seluruh hasil evaluasi kamu."),
        ("📊", "Export CSV", "Unduh riwayat evaluasi untuk dianalisis lebih lanjut."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div style="font-size:1.8rem;">{icon}</div>
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("")
    with st.container(border=True):
        colA, colB, colC = st.columns(3)
        colA.markdown("**🧠 AI Provider**")
        colA.write("OpenRouter")
        colB.markdown("**⚡ LLM Model**")
        colB.write("Google Gemini 2.5 Flash")
        colC.markdown("**👩‍💻 Author**")
        colC.write("Dzulfi Khoiriyah Azzahra")

    render_footer()

# =====================================
# Writing Evaluation
# =====================================
elif menu == "✍️ Writing Evaluation":

    st.markdown(
        """
        <div class="page-hero">
            <h1>✍️ Writing Evaluation</h1>
            <p>Tempel tulisan Bahasa Inggris kamu, lalu klik Evaluate untuk mendapatkan feedback dari AI.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    text = st.text_area(
        "Masukkan tulisan Bahasa Inggris",
        height=220,
        placeholder="Example: My name is John. I like playing football every weekend..."
    )
    st.caption(f"{len(text.strip().split()) if text.strip() else 0} kata")

    evaluate_clicked = st.button("🚀 Evaluate", type="primary", use_container_width=False)

    if evaluate_clicked:

        if text.strip() == "":
            st.warning("⚠️ Silakan masukkan tulisan terlebih dahulu.")

        else:
            with st.spinner("🤖 AI sedang mengevaluasi tulisan..."):
                result = evaluate_writing(text)

            st.success("✅ Evaluasi selesai!")
            st.markdown("### 📊 Evaluation Result")
            render_score_badge(result["overall_score"])
            st.markdown("")

            render_feedback_section(result)

            save_result(
                input_text=text,
                evaluation_type="Writing",
                overall_score=result["overall_score"],
                result=str(result)
            )

    render_footer()

# =====================================
# Speaking Evaluation
# =====================================
elif menu == "🎤 Speaking Evaluation":

    st.markdown(
        """
        <div class="page-hero">
            <h1>🎤 Speaking Evaluation</h1>
            <p>Upload rekaman audio (.wav) kamu, AI akan mentranskripsi dan mengevaluasinya.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Audio (.wav)",
        type=["wav"]
    )

    if uploaded_file is not None:

        st.audio(uploaded_file)

        with open("audio/temp.wav", "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("🎤 Evaluate Speaking", type="primary"):

            with st.spinner("🎧 Menganalisis audio..."):
                result = evaluate_speaking("audio/temp.wav")

            st.success("✅ Evaluasi selesai!")

            with st.container(border=True):
                st.markdown("#### 📝 Transcript")
                st.write(result["transcript"])

            st.markdown("### 📊 Evaluation Result")
            render_score_badge(result["overall_score"])
            st.markdown("")

            render_feedback_section(result)

            save_result(
                input_text=result["transcript"],
                evaluation_type="Speaking",
                overall_score=result["overall_score"],
                result=str(result)
            )
    else:
        st.info("⬆️ Silakan upload file audio (.wav) terlebih dahulu.")

    render_footer()

# =====================================
# History
# =====================================
elif menu == "📜 History":

    st.markdown(
        """
        <div class="page-hero">
            <h1>📜 History</h1>
            <p>Riwayat seluruh hasil evaluasi kamu, lengkap dengan ringkasan dan filter.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    history = get_history()

    if history:

        df = pd.DataFrame(
            history,
            columns=["ID", "Evaluation Type", "Overall Score", "Created At"]
        )

        # Ubah kolom Overall Score menjadi angka
        df["Overall Score"] = pd.to_numeric(df["Overall Score"], errors="coerce")

        # --- Ringkasan singkat ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Evaluasi", len(df))
        m2.metric("Rata-rata Skor", f"{df['Overall Score'].mean():.1f}/100")
        m3.metric(
            "Terakhir Dievaluasi",
            df["Created At"].max() if "Created At" in df else "-"
        )

        st.markdown("")

        # --- Filter ---
        f1, f2 = st.columns([1, 3])
        with f1:
            type_filter = st.selectbox(
                "Filter Tipe",
                ["Semua"] + sorted(df["Evaluation Type"].unique().tolist())
            )

        filtered_df = df if type_filter == "Semua" else df[df["Evaluation Type"] == type_filter]

        # --- Tabel ---
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Overall Score": st.column_config.ProgressColumn(
                    "Overall Score",
                    min_value=0,
                    max_value=100,
                    format="%d/100"
                )
            }
        )

        # --- Export ---
        st.markdown("")
        exp_col1, exp_col2 = st.columns([1, 4])
        with exp_col1:
            if st.button("📊 Export CSV"):
                try:
                    export_history()
                    st.success("✅ Data berhasil diexport.")
                except Exception as e:
                    st.error(f"Gagal export: {e}")
        with exp_col2:
            st.download_button(
                "⬇️ Download sebagai CSV",
                data=filtered_df.to_csv(index=False).encode("utf-8"),
                file_name=f"evaluation_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    else:
        st.info("📭 Belum ada data evaluasi.")

    render_footer()