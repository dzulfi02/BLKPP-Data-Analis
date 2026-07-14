import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import numpy as np

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Forecast Harga Ayam Nasional",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================
# GLOBAL STYLE
# ==========================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    :root{
        --ink:#31333F;
        --ink-soft:#6c6f7a;
        --paper:#FFFFFF;
        --card:#FFFFFF;
        --line:#E6E6E6;
        --forest:#F0F2F6;
        --forest-dark:#E1E4EA;
        --gold:#FF4B4B;
        --gold-soft:#FFE8E8;
        --good:#21C354;
    }

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        color: var(--ink);
    }

    .stApp{
        background: var(--paper);
    }

    /* Hide default Streamlit chrome for a cleaner look */
    #MainMenu, footer {visibility: hidden;}
    header[data-testid="stHeader"]{ background: transparent; }

    .block-container{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* ---------- HERO ---------- */
    .hero{
        background: linear-gradient(120deg, var(--forest) 0%, var(--forest-dark) 100%);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 2rem 2.4rem;
        color: var(--ink);
        margin-bottom: 1.6rem;
    }
    .hero-eyebrow{
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.72rem;
        color: var(--gold);
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .hero-title{
        font-size: 2.1rem;
        font-weight: 600;
        margin: 0 0 0.35rem 0;
        line-height: 1.15;
        color: var(--ink);
    }
    .hero-sub{
        font-size: 0.95rem;
        color: var(--ink-soft);
        max-width: 640px;
    }
    .hero-author{
        display:inline-flex;
        align-items:center;
        gap:0.5rem;
        background: #FFFFFF;
        border: 1px solid var(--line);
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        font-size: 0.8rem;
        margin-top: 1rem;
        color: var(--ink);
    }

    /* ---------- SECTION LABEL ---------- */
    .section-label{
        font-size:1.3rem;
        font-weight:600;
        color: var(--ink);
        margin: 1.6rem 0 0.8rem 0;
        display:flex;
        align-items:center;
        gap:0.5rem;
    }

    /* ---------- STAT CARDS ---------- */
    .stat-card{
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        height: 100%;
    }
    .stat-label{
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--ink-soft);
        margin-bottom: 0.35rem;
    }
    .stat-value{
        font-size: 1.55rem;
        font-weight: 600;
        color: var(--ink);
    }

    /* ---------- GENERIC CARD ---------- */
    .card{
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
    }

    /* ---------- MODEL BADGE ---------- */
    .model-badge{
        display:inline-flex;
        align-items:center;
        gap:0.5rem;
        background: rgba(33,196,84,0.1);
        border: 1px solid rgba(33,196,84,0.35);
        color: var(--good);
        font-weight:600;
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        font-size: 0.88rem;
        margin-bottom: 0.9rem;
    }

    /* Streamlit metric override */
    div[data-testid="stMetric"]{
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
    }
    div[data-testid="stMetricLabel"]{
        color: var(--ink-soft);
    }
    div[data-testid="stMetricValue"]{
        color: var(--ink);
    }

    /* Expander */
    div[data-testid="stExpander"]{
        border: 1px solid var(--line);
        border-radius: 14px;
        background: var(--card);
    }

    /* Footer */
    .app-footer{
        margin-top: 2rem;
        padding-top: 1.2rem;
        border-top: 1px solid var(--line);
        font-size: 0.82rem;
        color: var(--ink-soft);
        display:flex;
        justify-content:space-between;
        flex-wrap: wrap;
        gap: 0.6rem;
    }
    .app-footer b{ color: var(--ink); }

    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================
# DATA LOADING
# ==========================

import os
import glob

DATA_FILENAME = "data_harga_ayam.xlsx"

def find_data_file():
    """Cari file dataset di beberapa lokasi umum relatif terhadap app.py,
    lalu fallback ke pencarian rekursif di seluruh folder proyek."""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    candidate_paths = [
        os.path.join(base_dir, DATA_FILENAME),
        os.path.join(base_dir, "Dataset", DATA_FILENAME),
        os.path.join(base_dir, "dataset", DATA_FILENAME),
        os.path.join(base_dir, "data", DATA_FILENAME),
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return path

    # Fallback: cari rekursif (case-insensitive) di seluruh folder proyek
    for path in glob.glob(os.path.join(base_dir, "**", "*.xlsx"), recursive=True):
        if os.path.basename(path).lower() == DATA_FILENAME.lower():
            return path

    return None


@st.cache_data
def load_data(path):
    df = pd.read_excel(path)
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="%d/ %m/ %Y")
    df["Harga"] = (df["Harga"].astype(str).str.replace(",", "").replace("-", pd.NA).astype(float))
    df.rename(columns={"Harga": "Harga (Rp)"}, inplace=True)
    df["Harga (Rp)"] = df["Harga (Rp)"].astype(int)
    df = df.sort_values("Tanggal").set_index("Tanggal").asfreq("B")
    df["Harga (Rp)"] = df["Harga (Rp)"].interpolate()
    return df


data_path = find_data_file()

if data_path is None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    semua_file = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            semua_file.append(os.path.relpath(os.path.join(root, f), base_dir))

    st.error(
        f"❌ File **{DATA_FILENAME}** tidak ditemukan di dalam repo/folder project.\n\n"
        "Pastikan file dataset sudah di-*push* ke GitHub dan namanya persis sama "
        "(huruf besar/kecil ikut diperiksa)."
    )
    with st.expander("📁 Lihat daftar file yang terdeteksi di folder project"):
        st.write(semua_file if semua_file else "Tidak ada file yang terbaca.")
    st.stop()

df = load_data(data_path)

# ==========================
# HERO HEADER
# ==========================

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">Dashboard Forecasting &middot; Komoditas Pangan</div>
        <div class="hero-title">🐔 Forecast Harga Ayam Nasional</div>
        <div class="hero-sub">
            Prediksi harga daging ayam segar tingkat nasional menggunakan model
            Holt-Winters Exponential Smoothing, disusun dari data historis harian
            Pusat Informasi Harga Pangan Strategis (PIHPS) Nasional.
        </div>
        <div class="hero-author">👩‍💻 Dibuat oleh <b>&nbsp;Dzulfi Khoiriyah Azzahra</b></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================
# DATASET
# ==========================

with st.expander("📂 Lihat Dataset"):
    st.dataframe(df.reset_index(), use_container_width=True)
    st.caption("Sumber data: PIHPS Nasional (Pusat Informasi Harga Pangan Strategis) — Komoditas Daging Ayam Segar.")

# ==========================
# RINGKASAN DATASET
# ==========================

st.markdown('<div class="section-label">📊 Ringkasan Dataset</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
stats = [
    ("Jumlah Data", f"{len(df):,}"),
    ("Harga Minimum", f"Rp {df['Harga (Rp)'].min():,.0f}"),
    ("Harga Maksimum", f"Rp {df['Harga (Rp)'].max():,.0f}"),
    ("Rata-rata", f"Rp {df['Harga (Rp)'].mean():,.0f}"),
]
for col, (label, value) in zip([c1, c2, c3, c4], stats):
    col.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    f"📅 Periode data: **{df.index.min().strftime('%d-%m-%Y')}** "
    f"sampai **{df.index.max().strftime('%d-%m-%Y')}**"
)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.markdown("### ⚙️ Pengaturan Forecast")
st.sidebar.markdown(
    "Pilih jumlah hari yang ingin diprediksi menggunakan model **Holt-Winters**."
)
st.sidebar.markdown("---")

horizon = st.sidebar.selectbox("Forecast Horizon (hari)", [7, 14, 30], index=2)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **🏆 Model Terbaik**

    ✅ Holt-Winters Exponential Smoothing

    MAPE : **3.97%**
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **ℹ️ Tentang Aplikasi**

    Sumber data: PIHPS Nasional
    Komoditas: Daging Ayam Segar

    **Author:** Dzulfi Khoiriyah Azzahra
    """
)

# ==========================
# MODELING
# ==========================

train_size = int(len(df) * 0.8)
train = df.iloc[:train_size]
test = df.iloc[train_size:]

model = ExponentialSmoothing(train["Harga (Rp)"], trend="add", seasonal="add", seasonal_periods=7)
fit = model.fit()
pred_test = fit.forecast(len(test))
pred_test.index = test.index

# Metrik evaluasi Holt-Winters sesuai hasil pada notebook evaluasi model
mae = 1589.870638
rmse = 1851.212818
mape = 3.974525

final_model = ExponentialSmoothing(df["Harga (Rp)"], trend="add", seasonal="add", seasonal_periods=7).fit()
forecast = final_model.forecast(horizon)
future = pd.date_range(df.index[-1] + pd.offsets.BDay(1), periods=horizon, freq="B")

# ==========================
# MODEL TERBAIK
# ==========================

st.markdown('<div class="section-label">🏆 Model Terbaik</div>', unsafe_allow_html=True)
st.markdown('<span class="model-badge">✅ Holt-Winters Exponential Smoothing</span>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("MAE", f"{mae:.2f}")
c2.metric("RMSE", f"{rmse:.2f}")
c3.metric("MAPE", f"{mape:.2f}%")

# ==========================
# GRAFIK HISTORIS
# ==========================

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df["Harga (Rp)"], mode="lines", name="Historis",
                          line=dict(color="#31333F", width=1.6)))
fig.add_trace(go.Scatter(x=future, y=forecast, mode="lines+markers", name="Forecast",
                          line=dict(color="#FF4B4B", width=2, dash="dash")))
fig.update_layout(
    title="Forecast Harga Daging Ayam",
    xaxis_title="Tanggal",
    yaxis_title="Harga (Rp)",
    template="plotly_white",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Poppins, sans-serif", color="#31333F"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.markdown('<div class="section-label">📈 Grafik Historis &amp; Forecast</div>', unsafe_allow_html=True)
with st.expander("Lihat Grafik Historis Penuh", expanded=False):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================
# GRAFIK ZOOM
# ==========================

history_zoom = df.iloc[-120:]

fig_zoom = go.Figure()
fig_zoom.add_trace(go.Scatter(x=history_zoom.index, y=history_zoom["Harga (Rp)"], mode="lines",
                               name="Historis", line=dict(color="#31333F", width=2)))
fig_zoom.add_trace(go.Scatter(x=future, y=forecast, mode="lines+markers", name="Forecast",
                               line=dict(color="#FF4B4B", width=2.4, dash="dash")))
fig_zoom.update_layout(
    title="Forecast 120 Hari Terakhir",
    xaxis_title="Tanggal",
    yaxis_title="Harga (Rp)",
    hovermode="x unified",
    template="plotly_white",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Poppins, sans-serif", color="#31333F"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.plotly_chart(fig_zoom, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==========================
# HASIL FORECAST
# ==========================

forecast_df = pd.DataFrame({"Tanggal": future, "Prediksi Harga": forecast.round().astype(int)})

st.markdown('<div class="section-label">📋 Hasil Forecast</div>', unsafe_allow_html=True)
st.dataframe(forecast_df, use_container_width=True)

csv = forecast_df.to_csv(index=False).encode()
st.download_button("⬇️ Download CSV", csv, "forecast_harga_ayam.csv", "text/csv")

# ==========================
# INSIGHT
# ==========================

# ==========================
# INSIGHT
# ==========================

harga_awal = forecast.iloc[0]
harga_akhir = forecast.iloc[-1]
harga_tertinggi = forecast.max()
harga_terendah = forecast.min()
tgl_tertinggi = future[forecast.values.argmax()].strftime("%d-%m-%Y")
tgl_terendah = future[forecast.values.argmin()].strftime("%d-%m-%Y")
pct_change = (harga_akhir - harga_awal) / harga_awal * 100
rata_historis = df["Harga (Rp)"].mean()
selisih_vs_historis = (forecast.mean() - rata_historis) / rata_historis * 100

if pct_change > 1:
    arah_trend = f"cenderung <b>naik sekitar {pct_change:.2f}%</b> dari awal ke akhir periode forecast"
    saran = "distributor dan pedagang disarankan menyiapkan stok lebih awal untuk mengantisipasi kenaikan harga"
elif pct_change < -1:
    arah_trend = f"cenderung <b>turun sekitar {abs(pct_change):.2f}%</b> dari awal ke akhir periode forecast"
    saran = "konsumen dapat memanfaatkan momen ini untuk membeli dalam jumlah lebih banyak, sementara pedagang perlu mewaspadai penurunan margin"
else:
    arah_trend = "relatif <b>stabil</b> selama periode forecast, tanpa pergerakan signifikan"
    saran = "harga diperkirakan tidak berfluktuasi tajam sehingga kondisi pasar dapat dianggap normal"

bandingan = (
    f"berada <b>{selisih_vs_historis:.2f}% di atas</b> rata-rata historis"
    if selisih_vs_historis > 0
    else f"berada <b>{abs(selisih_vs_historis):.2f}% di bawah</b> rata-rata historis"
)

st.markdown('<div class="section-label">💡 Insight</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="card">
        Berdasarkan hasil forecast {horizon} hari ke depan:
        <ul>
            <li>Harga diperkirakan {arah_trend}.</li>
            <li>Titik harga tertinggi diprediksi terjadi pada <b>{tgl_tertinggi}</b> sebesar
                <b>Rp {harga_tertinggi:,.0f}</b>, sedangkan titik terendah pada <b>{tgl_terendah}</b>
                sebesar <b>Rp {harga_terendah:,.0f}</b>.</li>
            <li>Rata-rata harga hasil prediksi {bandingan} sepanjang data historis
                (Rp {rata_historis:,.0f}).</li>
        </ul>
        Dengan tren tersebut, {saran}.
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================
# FOOTER
# ==========================

st.markdown(
    """
    <div class="app-footer">
        <div>📚 Sumber data: <b>PIHPS Nasional</b> (Pusat Informasi Harga Pangan Strategis) — Komoditas Daging Ayam Segar</div>
        <div>👩‍💻 Dibuat oleh <b>Dzulfi Khoiriyah Azzahra</b></div>
    </div>
    """,
    unsafe_allow_html=True,
)
