# =========================================================
# IMPORT LIBRARY
# =========================================================
import io
# io digunakan untuk membaca dan menulis data berbentuk byte,
# terutama saat upload file Excel dan export file (CSV / Excel)

import pandas as pd
# pandas digunakan sebagai library utama untuk pengolahan data
# seperti cleaning, grouping, agregasi, dan manipulasi DataFrame

import numpy as np
# numpy digunakan untuk perhitungan numerik,
# seperti persentase, proporsi, dan operasi matematika sederhana

import streamlit as st
# streamlit adalah framework utama untuk membuat dashboard web interaktif

import plotly.graph_objects as go

import plotly.express as px
# plotly.express digunakan untuk membuat grafik interaktif
# seperti bar chart, line chart, pie chart, heatmap, dan treemap

from pathlib import Path

# =========================================================
# PAGE CONFIG
# Mengatur tampilan dasar halaman dashboard
# =========================================================
st.set_page_config(
    page_title="Dashboard Lapas Cirebon",   # Judul halaman pada browser
    page_icon="🛡️",                        # Ikon tab browser
    layout="wide",                          # Layout lebar agar grafik tidak sempit
    initial_sidebar_state="expanded",       # Sidebar langsung terbuka saat load
)


# =========================================================
# STYLING (CUSTOM CSS)
# Digunakan untuk meningkatkan estetika dan keterbacaan UI
# Tanpa mempengaruhi proses pengolahan data
# =========================================================
st.markdown(
    """
    <style>
    :root{
        --primary:#2563eb;
        --secondary:#0ea5e9;
        --success:#22c55e;
        --warning:#f59e0b;
        --danger:#ef4444;
        --text:#0f172a;
        --card:#ffffff;
        --border: rgba(15,23,42,.08);
        --shadow: 0 12px 30px rgba(15,23,42,.08);
    }

    /* ===== FIX: TEKS DI SELECTBOX / MULTISELECT BIAR KELIHATAN ===== */

/* teks value & placeholder pada selectbox */
div[data-baseweb="select"] *{
  color: #0f172a !important;  /* teks gelap */
}

/* area box select-nya (kalau mau tetap terang) */
div[data-baseweb="select"] > div{
  background: rgba(255,255,255,.92) !important;
  border: 1px solid rgba(15,23,42,.18) !important;
}

/* placeholder (mis. "Semua") kadang dianggap placeholder */
div[data-baseweb="select"] [data-testid="stMarkdownContainer"]{
  color: #0f172a !important;
}

/* icon panah dropdown */
div[data-baseweb="select"] svg{
  fill: #0f172a !important;
}

/* dropdown menu */
div[role="listbox"]{
  background: rgba(255,255,255,.98) !important;
  border: 1px solid rgba(15,23,42,.18) !important;
}

/* item option di dropdown */
div[role="option"]{
  color: #0f172a !important;
}
    /* ===== SECTION HEADER (KPI) ===== */
.section-head{
  position: relative;
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:16px;

  padding: 16px 18px;
  border-radius: 16px;

  background: linear-gradient(135deg,
    rgba(255,255,255,.08) 0%,
    rgba(255,255,255,.05) 50%,
    rgba(0,0,0,.08) 100%
  );

  border: 1px solid rgba(255,255,255,.12);
  box-shadow: 0 14px 34px rgba(0,0,0,.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  overflow:hidden;
}

/* glow halus biar hidup */
.section-head::before{
  content:"";
  position:absolute;
  inset:-2px;
  background:
    radial-gradient(520px 200px at 18% 15%,
      rgba(56,189,248,.18), transparent 60%),
    radial-gradient(520px 220px at 88% 35%,
      rgba(236,72,153,.12), transparent 62%);
  pointer-events:none;
}

.section-left{display:flex; gap:12px; align-items:flex-start;}
.section-icon{
  width:44px; height:44px;
  border-radius:14px;
  display:flex; align-items:center; justify-content:center;
  background: rgba(255,255,255,.10);
  border: 1px solid rgba(255,255,255,.16);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.12);
  font-size:20px;
}

.section-title{
  font-size: 30px;
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -0.3px;
  text-shadow: 0 2px 12px rgba(0,0,0,.35);
  margin-top: 2px;
}

.section-title .kpi-tag{
  font-size: 18px;
  font-weight: 800;
  opacity:.9;
}

.section-sub{
  margin-top: 6px;
  font-size: 13px;
  color: rgba(255,255,255,.70) !important;
}

/* underline gradient tipis */
.section-underline{
  margin-top: 10px;
  height: 2px;
  width: 220px;
  border-radius: 99px;
  background: linear-gradient(90deg,
    rgba(56,189,248,.95),
    rgba(34,197,94,.65),
    rgba(236,72,153,.75),
    transparent
  );
  opacity:.85;
}

.section-right{display:flex; align-items:center; gap:10px; margin-top:2px;}
.section-pill{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.14);
  box-shadow: 0 10px 22px rgba(0,0,0,.22);
  font-size: 13px;
  color: rgba(255,255,255,.88) !important;
  white-space: nowrap;
}
.section-pill .dot{
  width:9px;height:9px;border-radius:999px;
  background:#22c55e;
  box-shadow: 0 0 0 4px rgba(34,197,94,.18), 0 0 18px rgba(34,197,94,.35);
}

    /* ============================
       BACKGROUND PALING BELAKANG
       ============================ */
 /* ===== COLD GREY PREMIUM ===== */
    html, body{
    height: 100%;
    background:
        linear-gradient(
        135deg,
        #384c59 0%,
        #132d3d 100%
        ) !important;
    background-attachment: fixed !important;
    }

[data-testid="stAppViewContainer"],
.stApp,
.main,
.block-container{
  background: transparent !important;
}

    /* Streamlit layers dibuat transparan agar background body kelihatan */
    [data-testid="stAppViewContainer"],
    .stApp,
    .main,
    .block-container{
      background: transparent !important;
      color: var(--text);
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"]{
      background: transparent !important;
    }

    /* Container spacing */
    .block-container{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

/* ===== TEXT TERANG GLOBAL ===== */
html, body, .stApp {
  color: #f8fafc !important;   /* hampir putih */
}

/* Semua heading */
h1, h2, h3, h4, h5, h6 {
  color: #ffffff !important;
}

/* Label dan teks biasa */
label, p, span, div {
  color: rgba(255,255,255,0.92) !important;
}

/* KPI section title */
.kpi-title {
  color: rgba(255,255,255,0.85) !important;
}

/* Subtitle */
.subtitle {
  color: rgba(255,255,255,0.75) !important;
}

/* Tabs */
button[role="tab"] {
  color: rgba(255,255,255,0.85) !important;
}

/* Axis chart */
.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text {
  fill: rgba(255,255,255,0.85) !important;
}

    /* Hilangkan elemen default */
    #MainMenu, footer, header{visibility:hidden;}

    /* ============================
       GLASS / CARD CONTAINER
       ============================ */
    .glass{
        background: rgba(255,255,255,.72);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        box-shadow: var(--shadow);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }

    /* Header / topbar */
    .topbar{
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white;
        border-radius: 18px;
        padding: 22px 26px;
        box-shadow: 0 12px 30px rgba(37,99,235,.35);
    }
    .topbar, .topbar *{ color:#fff !important; }

    /* ============================
       KPI CARDS (BALIKIN YANG ILANG)
       ============================ */
    .cards{
        display:grid;
        grid-template-columns:repeat(4,1fr);
        gap:16px;
    }

    .card{
        border-radius:18px;
        padding:18px;
        color:white !important;
        box-shadow:0 12px 28px rgba(0,0,0,.15);
        border: 1px solid rgba(255,255,255,.18);
    }

    .card .icon{
        font-size:16px;
        width:28px;height:28px;
        border-radius:10px;
        display:flex;
        align-items:center;
        justify-content:center;
        background: rgba(255,255,255,.18);
        border: 1px solid rgba(255,255,255,.18);
        margin-bottom: 10px;
    }

    .card .label{
        font-size:14px;
        font-weight:700;
        opacity:.95;
    }

    .card .value{
        font-size:32px;
        font-weight:900;
        margin-top:8px;
        line-height:1.1;
    }

    .card .note{
        font-size:13px;
        opacity:.92;
        margin-top:10px;
    }

    .card.c1{background:linear-gradient(135deg,#2563eb,#1e40af);}
    .card.c2{background:linear-gradient(135deg,#16a34a,#15803d);}
    .card.c3{background:linear-gradient(135deg,#ec4899,#be185d);}
    .card.c4{background:linear-gradient(135deg,#f59e0b,#b45309);}

    /* Responsive: kalau layar kecil, kartu turun baris */
    @media (max-width: 1100px){
      .cards{ grid-template-columns:repeat(2,1fr); }
    }
    @media (max-width: 640px){
      .cards{ grid-template-columns:1fr; }
    }

    /* Sidebar */
    section[data-testid="stSidebar"]>div{
        background:#ffffff;
        box-shadow:inset -1px 0 0 rgba(0,0,0,.05);
    }

    /* Judul */
    h1,h2,h3{ letter-spacing:-0.3px; }
    /* ===== HERO GLASS + BADGE (HEADER ATAS) ===== */
/* ===== HERO: DARK GLASS (UPGRADED) ===== */
.hero{
  position: relative;
  border-radius: 18px;
  padding: 18px 22px;

  /* base dark glass */
  background: linear-gradient(135deg,
    rgba(15,23,42,.55) 0%,
    rgba(15,23,42,.35) 55%,
    rgba(2,6,23,.25) 100%
  );

  border: 1px solid rgba(255,255,255,.10);
  box-shadow:
    0 18px 45px rgba(0,0,0,.35),
    inset 0 1px 0 rgba(255,255,255,.08);  /* top highlight */

  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  overflow: hidden;
}

/* subtle accent glow (tanpa bikin norak) */
.hero::before{
  content:"";
  position:absolute;
  inset:-2px;
  background:
    radial-gradient(600px 220px at 20% 20%,
      rgba(56,189,248,.18), transparent 60%),
    radial-gradient(520px 240px at 85% 35%,
      rgba(34,197,94,.10), transparent 62%);
  pointer-events:none;
}

/* light sweep line biar lebih “premium” */
.hero::after{
  content:"";
  position:absolute;
  top:0; left:0; right:0;
  height:1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.20), transparent);
  pointer-events:none;
}

.hero, .hero *{ color: rgba(255,255,255,.92) !important; }

/* ===== TYPO: naikkan hierarchy ===== */
.hero h1, .hero h2, .hero h3{
  letter-spacing: .2px;
  text-shadow: 0 2px 10px rgba(0,0,0,.35);
}

.hero p, .hero small{
  color: rgba(255,255,255,.70) !important;
}

/* ===== BADGE: jadi chips modern ===== */
.hero .badge{
  display: inline-flex;
  align-items: center;
  gap: 8px;

  padding: 8px 10px;
  border-radius: 999px;

  background: rgba(255,255,255,.08) !important;
  border: 1px solid rgba(255,255,255,.14) !important;

  box-shadow:
    0 10px 24px rgba(0,0,0,.22),
    inset 0 1px 0 rgba(255,255,255,.10);

  color: rgba(255,255,255,.88) !important;
}

.hero .badge b{
  color: rgba(255,255,255,.92) !important;
  
}
/* =========================
   FIX FILTER SELECTBOX TEXT
   ========================= */

/* Kotak selectbox (control) */
.stSelectbox div[data-baseweb="select"] > div{
  background: rgba(255,255,255,.92) !important;
  border: 1px solid rgba(15,23,42,.18) !important;
}

/* Teks nilai yang terpilih + placeholder di dalam selectbox */
.stSelectbox div[data-baseweb="select"] *{
  color: #0f172a !important;         /* teks gelap */
}

/* Icon dropdown (panah) */
.stSelectbox div[data-baseweb="select"] svg{
  fill: #0f172a !important;
}

/* Popup dropdown menu */
div[role="listbox"]{
  background: rgba(255,255,255,.98) !important;
  border: 1px solid rgba(15,23,42,.18) !important;
}

/* Semua teks di dalam dropdown */
div[role="listbox"] *{
  color: #0f172a !important;
}

/* Hover item dropdown */
div[role="option"]:hover{
  background: rgba(37,99,235,.10) !important;
}

/* =========================
   FIX BUTTON RESET FILTER
   ========================= */
.stButton > button{
  width: 100%;
  border-radius: 12px !important;
  padding: 0.55rem 0.9rem !important;

  background: linear-gradient(90deg, rgba(37,99,235,.95), rgba(14,165,233,.95)) !important;
  color: #ffffff !important;

  border: 1px solid rgba(255,255,255,.18) !important;
  box-shadow: 0 12px 26px rgba(0,0,0,.25) !important;
  font-weight: 800 !important;
}

.stButton > button:hover{
  filter: brightness(1.05);
  transform: translateY(-1px);
}
/* =========================================
   HARD FIX: TEKS OPTION DROPDOWN BASEWEB
   (agar opsi "Februari" dll kelihatan)
   ========================================= */

/* 1) Control select (yang di bar filter) */
.stSelectbox div[data-baseweb="select"] input{
  color:#0f172a !important;
  -webkit-text-fill-color:#0f172a !important; /* penting untuk chrome */
}

.stSelectbox div[data-baseweb="select"] > div{
  background: rgba(255,255,255,.92) !important;
  border: 1px solid rgba(15,23,42,.18) !important;
}

.stSelectbox div[data-baseweb="select"] svg{
  fill:#0f172a !important;
}

/* 2) POPUP dropdown (BaseWeb popover/portal) */
div[data-baseweb="popover"]{
  z-index: 99999 !important; /* biar tidak ketutup elemen lain */
}

/* paksa semua teks di popover jadi gelap */
div[data-baseweb="popover"] *{
  color:#0f172a !important;
}

/* container listbox */
div[data-baseweb="popover"] [role="listbox"]{
  background: rgba(255,255,255,.98) !important;
  border: 1px solid rgba(15,23,42,.18) !important;
}

/* item opsi */
div[data-baseweb="popover"] [role="option"]{
  background: transparent !important;
  color:#0f172a !important;
}

/* hover dan selected biar jelas */
div[data-baseweb="popover"] [role="option"]:hover{
  background: rgba(37,99,235,.10) !important;
}
div[data-baseweb="popover"] [role="option"][aria-selected="true"]{
  background: rgba(37,99,235,.14) !important;
}
/* =========================
   FIX: DOWNLOAD BUTTON (CSV/EXCEL) BIAR KELIHATAN
   ========================= */
div[data-testid="stDownloadButton"] > button{
  width: 100% !important;
  border-radius: 12px !important;
  padding: 0.55rem 0.9rem !important;

  background: linear-gradient(90deg, rgba(37,99,235,.95), rgba(14,165,233,.95)) !important;
  color: #ffffff !important;

  border: 1px solid rgba(255,255,255,.18) !important;
  box-shadow: 0 12px 26px rgba(0,0,0,.25) !important;
  font-weight: 800 !important;
}

/* teks di dalam button */
div[data-testid="stDownloadButton"] > button *{
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
}

/* icon svg */
div[data-testid="stDownloadButton"] > button svg{
  fill: #ffffff !important;
}

div[data-testid="stDownloadButton"] > button:hover{
  filter: brightness(1.05);
  transform: translateY(-1px);
}

    </style>
   """,
    unsafe_allow_html=True
)

# =========================================================
# HELPERS
# Digunakan untuk pengolahan waktu (bulan & tahun)
# =========================================================

# Mapping nama bulan ke angka (untuk konversi datetime)
MONTH_MAP = {
    "JANUARI": 1, "FEBRUARI": 2, "MARET": 3, "APRIL": 4,
    "MEI": 5, "JUNI": 6, "JULI": 7, "AGUSTUS": 8,
    "SEPTEMBER": 9, "OKTOBER": 10, "NOVEMBER": 11, "DESEMBER": 12
}

# Urutan bulan untuk keperluan visualisasi
MONTH_ORDER = list(MONTH_MAP.keys())


def safe_month_to_num(x: str) -> int:
    """
    Mengubah nama bulan (string) menjadi angka.
    Jika bulan kosong atau tidak valid, default ke Januari (1).
    """
    if pd.isna(x):
        return 1
    x = str(x).strip().upper()
    return MONTH_MAP.get(x, 1)

# =========================
# PLOTLY THEME (FIGMA-LIKE)
# =========================
PLOT_CONFIG = {
    "displayModeBar": "hover",
    "displaylogo": False,
    "scrollZoom": True,
    "responsive": True
}

def apply_plot_theme(fig, height=360):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=65, b=25),

        # ✅ jangan 100% transparan (ini kunci biar aman saat fullscreen & download)
        paper_bgcolor="rgba(2, 6, 23, 0.35)",
        plot_bgcolor="rgba(2, 6, 23, 0.15)",

        font=dict(family="Inter, system-ui, Arial", size=14, color="#ffffff"),
        title=dict(font=dict(size=20, color="#ffffff"), x=0.02),

        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(color="rgba(255,255,255,0.88)", size=13),
            bgcolor="rgba(255,255,255,0.06)"
        ),

        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="rgba(15,23,42,0.95)",
            bordercolor="rgba(255,255,255,0.2)",
            font=dict(color="white", size=13)
        ),

        # bonus: modebar dark
        modebar=dict(
            bgcolor="rgba(2,6,23,0.35)",
            color="rgba(255,255,255,0.85)",
            activecolor="#38bdf8"
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.10)",
        tickfont=dict(color="rgba(255,255,255,0.90)", size=12),
        title_font=dict(color="rgba(255,255,255,0.95)", size=13),
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=False,
        tickfont=dict(color="rgba(255,255,255,0.90)", size=12),
        title_font=dict(color="rgba(255,255,255,0.95)", size=13),
        zeroline=False
    )

    return fig
# =========================================================
# LOAD DATA DENGAN CACHE
# Cache digunakan agar file tidak dibaca ulang terus-menerus
# =========================================================
@st.cache_data(show_spinner=False)
def load_data_from_bytes(xlsx_bytes: bytes) -> pd.DataFrame:
    """
    Membaca file Excel dari hasil upload user (dalam bentuk byte)
    """
    return pd.read_excel(io.BytesIO(xlsx_bytes))


@st.cache_data(show_spinner=False)
def load_data_from_path(path: str) -> pd.DataFrame:
    """
    Membaca file Excel dari path default
    """
    return pd.read_excel(path)


# =========================================================
# MEMBENTUK KOLOM DATETIME (PERIODE)
# Digunakan untuk analisis tren berbasis waktu
# =========================================================
def build_datetime(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Normalisasi kolom bulan
    out["bulan"] = out["bulan"].astype(str).str.upper().str.strip()

    # Konversi bulan ke angka
    out["bulan_num"] = out["bulan"].apply(safe_month_to_num)

    # Pastikan kolom tahun bertipe numerik
    out["tahun"] = pd.to_numeric(out["tahun"], errors="coerce")

    # Gabungkan tahun dan bulan menjadi satu kolom datetime
    out["periode"] = pd.to_datetime(
        out["tahun"].fillna(2000).astype(int).astype(str)
        + "-" + out["bulan_num"].astype(int).astype(str)
        + "-01",
        errors="coerce"
    )

    return out


# # =========================================================
# # SIDEBAR – DATA SOURCE & PARAMETER
# # =========================================================
# st.sidebar.markdown("## ⚙️ Pengaturan")

# # Upload file Excel oleh user
# uploaded = st.sidebar.file_uploader(
#     "Upload data (Excel .xlsx)", type=["xlsx"]
# )

# Path default jika user tidak upload file
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_FILE = BASE_DIR / "data" / "data_narapidana_cirebon_clean.xlsx"
@st.cache_data(show_spinner=False)
def load_excel_from_path(path: Path):
    return pd.read_excel(path, engine="openpyxl")

@st.cache_data(show_spinner=False)
def load_excel_from_upload(uploaded_file):
    return pd.read_excel(io.BytesIO(uploaded_file.getvalue()), engine="openpyxl")


# Input kapasitas lapas untuk perhitungan tingkat hunian
capacity = st.sidebar.number_input(
    "Kapasitas Lapas (orang)", min_value=1, value=1200, step=50
)


# =========================================================
# LOAD DATA
# =========================================================
try:
    df_raw = load_excel_from_path(DEFAULT_FILE)

except Exception as e:
    st.error("Data belum bisa dibaca. Pastikan file Excel sesuai format dan kolomnya lengkap.")
    st.write("Path default:", str(DEFAULT_FILE))
    st.write("File ketemu?:", DEFAULT_FILE.exists())
    st.exception(e)
    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================
# Bangun kolom periode (datetime)
df = build_datetime(df_raw)

# Filter khusus wilayah Cirebon jika kolom tersedia
if "nama_kabupaten_kota" in df.columns:
    df["nama_kabupaten_kota"] = (
        df["nama_kabupaten_kota"].astype(str).str.upper().str.strip()
    )
    df = df[df["nama_kabupaten_kota"].str.contains("CIREBON", na=False)]

# Normalisasi kolom kategorikal
df["jenis_kelamin"] = df["jenis_kelamin"].astype(str).str.upper().str.strip()
df["kategori_kejahatan"] = df["kategori_kejahatan"].astype(str).str.strip()

# Pastikan jumlah narapidana bertipe numerik
df["jumlah_narapidana"] = (
    pd.to_numeric(df["jumlah_narapidana"], errors="coerce")
    .fillna(0)
    .astype(int)
)

# Ambil periode terakhir untuk informasi update data
last_period = df["periode"].max()
last_update_str = (
    last_period.strftime("%d %B %Y") if pd.notna(last_period) else "-"
)


# =========================================================
# FILTER STATE
# Digunakan agar filter tidak reset saat interaksi user
# =========================================================
if "filter_gender" not in st.session_state:
    st.session_state.filter_gender = "Semua"
if "filter_crime" not in st.session_state:
    st.session_state.filter_crime = "Semua Kejahatan"
if "filter_year" not in st.session_state:
    st.session_state.filter_year = "Semua"
if "filter_month" not in st.session_state:
    st.session_state.filter_month = "Semua"

# =========================================================
# OPSI FILTER (SELECTBOX OPTIONS)
# Membuat daftar pilihan filter berdasarkan isi data
# =========================================================

# Opsi filter jenis kelamin:
# - "Semua" untuk menampilkan seluruh data
# - Nilai lainnya diambil dari kolom jenis_kelamin (unik, non-null)
gender_opts = ["Semua"] + sorted(
    df["jenis_kelamin"].dropna().unique().tolist()
)

# Opsi filter kategori kejahatan:
# - "Semua Kejahatan" untuk menampilkan seluruh kategori
# - Diambil dari nilai unik kolom kategori_kejahatan
crime_opts = ["Semua Kejahatan"] + sorted(
    df["kategori_kejahatan"].dropna().unique().tolist()
)

# Opsi filter tahun:
# - "Semua" untuk menampilkan seluruh tahun
# - Tahun dikonversi ke integer agar konsisten
year_opts = ["Semua"] + sorted(
    df["tahun"].dropna().astype(int).unique().tolist()
)

# Opsi filter bulan:
# - "Semua" untuk menampilkan seluruh bulan
# - MONTH_ORDER digunakan agar urutan bulan tetap kronologis
month_opts = ["Semua"] + [m.title() for m in MONTH_ORDER]


# =========================================================
# HEADER DASHBOARD
# Menampilkan judul, subjudul, dan info terakhir update data
# =========================================================
st.markdown(f"""
<div class="hero">
  <div style="display:flex;justify-content:space-between;gap:12px;align-items:flex-start;">
    <div>
      <div style="font-size:32px;font-weight:900;letter-spacing:-.3px;">🛡️ Dashboard Lapas Cirebon</div>
      <div style="opacity:.78;margin-top:4px;">Sistem Informasi Data Narapidana · Live Update</div>
      <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
        <span class="badge"><span class="dot"></span>Live Update</span>
        <span class="badge">🗓️ Terakhir diperbarui: <b>{last_update_str}</b></span>
      </div>
    </div>
    <span class="badge">⚡ Monitoring</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

def reset_filters():
    st.session_state["filter_gender"] = "Semua"
    st.session_state["filter_crime"]  = "Semua Kejahatan"
    st.session_state["filter_year"]   = "Semua"
    st.session_state["filter_month"]  = "Semua"

# Layout filter menggunakan kolom
f1, f2, f3, f4, f5 = st.columns([1,2,1,1,1], vertical_alignment="bottom")

# Pastikan default state ada
st.session_state.setdefault("filter_gender", "Semua")
st.session_state.setdefault("filter_crime",  "Semua Kejahatan")
st.session_state.setdefault("filter_year",   "Semua")
st.session_state.setdefault("filter_month",  "Semua")

f1, f2, f3, f4, f5 = st.columns([1,2,1,1,1], vertical_alignment="bottom")

with f1:
    st.selectbox("Jenis Kelamin", gender_opts, key="filter_gender")

with f2:
    st.selectbox("Jenis Kejahatan", crime_opts, key="filter_crime")

with f3:
    st.selectbox("Tahun", year_opts, key="filter_year")

with f4:
    st.selectbox("Bulan", month_opts, key="filter_month")

with f5:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    st.button("Reset Filter", use_container_width=True, on_click=reset_filters)

# =========================================================
# APPLY FILTER
# Menerapkan filter user ke dataset
# =========================================================
df_f = df.copy()

# Filter jenis kelamin
if st.session_state.filter_gender != "Semua":
    df_f = df_f[df_f["jenis_kelamin"] == st.session_state.filter_gender]

# Filter kategori kejahatan
if st.session_state.filter_crime != "Semua Kejahatan":
    df_f = df_f[df_f["kategori_kejahatan"] == st.session_state.filter_crime]

# Filter tahun
if st.session_state.filter_year != "Semua":
    df_f = df_f[df_f["tahun"].astype(int) == int(st.session_state.filter_year)]

# Filter bulan
if st.session_state.filter_month != "Semua":
    df_f = df_f[df_f["bulan"].str.upper() == st.session_state.filter_month.upper()]

# ========================================================
# PERHITUNGAN KPI UTAMA
# =========================================================

# Total narapidana sesuai filter aktif
total_kpi = int(df_f["jumlah_narapidana"].sum()) if len(df_f) else 0

# Agregasi jumlah narapidana per kategori kejahatan
crime_agg_kpi = (
    df_f.groupby("kategori_kejahatan", as_index=False)["jumlah_narapidana"]
       .sum()
       .sort_values("jumlah_narapidana", ascending=False)
)

# Kategori kejahatan dengan jumlah terbanyak
top_crime = crime_agg_kpi.iloc[0]["kategori_kejahatan"] if len(crime_agg_kpi) else "-"

# Agregasi jumlah narapidana per periode (bulan-tahun)
period_agg = (
    df_f.groupby("periode", as_index=False)["jumlah_narapidana"]
       .sum()
       .sort_values("jumlah_narapidana", ascending=False)
)

# Periode dengan jumlah narapidana tertinggi
densest_period = period_agg.iloc[0]["periode"] if len(period_agg) else pd.NaT

# Nama bulan terpadat
densest_month = "-"
if pd.notna(densest_period):
    tmp = df_f[df_f["periode"] == densest_period]
    densest_month = (
        str(tmp.iloc[0]["bulan"]).upper().strip()
        if len(tmp)
        else densest_period.strftime("%B").upper()
    )


# =========================================================
# TAMPILAN KPI RINGKAS

# ===== SECTION KPI =====
st.markdown(
    """
    <div class="section-head">
      <div class="section-left">
        <div class="section-icon">📊</div>
        <div>
          <div class="section-title">
            Ringkasan Utama <span class="kpi-tag">(KPI)</span>
          </div>
          <div class="section-sub">Kondisi terkini berdasarkan periode terakhir</div>
          <div class="section-underline"></div>
        </div>
      </div>

      <div class="section-right">
        <div class="section-pill">
          <span class="dot"></span>
          KPI Summary
        </div>
      </div>
    </div>
    <div style="height:10px"></div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# KPI CARDS (WARNA)
# Menampilkan ringkasan statistik utama secara visual
# =========================================================

# Total narapidana
total = int(df_f["jumlah_narapidana"].sum())

# Jumlah narapidana laki-laki
male = int(
    df_f.loc[
        df_f["jenis_kelamin"].str.contains("LAKI", na=False),
        "jumlah_narapidana"
    ].sum()
)

# ===== KPI berbasis periode terbaru (lebih masuk akal untuk hunian) =====
last_p = df_f["periode"].max() if len(df_f) else pd.NaT
df_last = df_f[df_f["periode"] == last_p] if pd.notna(last_p) else df_f.iloc[0:0]

total = int(df_last["jumlah_narapidana"].sum()) if len(df_last) else 0

male = int(
    df_last.loc[df_last["jenis_kelamin"].str.contains("LAKI", na=False), "jumlah_narapidana"].sum()
) if len(df_last) else 0

female = int(
    df_last.loc[df_last["jenis_kelamin"].str.contains("PEREMPUAN", na=False), "jumlah_narapidana"].sum()
) if len(df_last) else 0

occupancy = (total / capacity) * 100 if capacity else 0.0

# HTML untuk menampilkan kartu KPI berwarna
cards_html = f"""
<div class="cards">
  <div class="card c1">
    <div class="icon">👥</div>
    <div class="label">Total Narapidana</div>
    <div class="value">{total:,}</div>
    <div class="note">Kapasitas: {capacity:,} ({occupancy:.1f}%)</div>
  </div>
  <div class="card c2">
    <div class="icon">♂️</div>
    <div class="label">Laki-laki</div>
    <div class="value">{male:,}</div>
    <div class="note">{(male/total*100 if total else 0):.1f}% dari total</div>
  </div>
  <div class="card c3">
    <div class="icon">♀️</div>
    <div class="label">Perempuan</div>
    <div class="value">{female:,}</div>
    <div class="note">{(female/total*100 if total else 0):.1f}% dari total</div>
  </div>
  <div class="card c4">
    <div class="icon">📈</div>
    <div class="label">Tingkat Hunian</div>
    <div class="value">{occupancy:.1f}%</div>
    <div class="note">Dari kapasitas maksimal</div>
  </div>
</div>
"""

# Render KPI cards ke dashboard
st.markdown(cards_html, unsafe_allow_html=True)

def polish(fig, height=360):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18),
        transition=dict(duration=450, easing="cubic-in-out"),
        hovermode="closest",
        legend_title_text="",
        font=dict(family="Inter, system-ui, sans-serif"),
    )
    return fig
# =========================================================
# TAB UNTUK VISUALISASI
# =========================================================
tab1, tab2, tab3 = st.tabs(
    ["Grafik Utama", "Analisis Lanjutan", "Komposisi"]
)

# =========================================================
# TAB 1: GRAFIK UTAMA (CLEAN & AKADEMIS)
# Semua grafik menggunakan df_f (hasil filter)
# =========================================================
with tab1:
    if df_f.empty:
        st.warning("Tidak ada data untuk kombinasi filter ini. Coba longgarkan filter.")
        st.stop()

    # Flags
    crime_locked = st.session_state.filter_crime != "Semua Kejahatan"
    month_locked = st.session_state.filter_month != "Semua"

    c1, c2 = st.columns(2)

    # =====================================================
    # (A) KIRI ATAS: Struktur / Komposisi
    # - Kalau crime belum dipilih: Top 10 kategori
    # - Kalau crime dipilih: Distribusi bulan untuk crime terpilih
    # =====================================================
    if not crime_locked:
        comp = (
            df_f.groupby("kategori_kejahatan", as_index=False)["jumlah_narapidana"]
                .sum()
                .sort_values("jumlah_narapidana", ascending=False)
        )

        top10 = comp.head(10).copy()
        other_sum = comp.iloc[10:]["jumlah_narapidana"].sum()
        if other_sum > 0:
            top10 = pd.concat(
                [top10, pd.DataFrame([{"kategori_kejahatan": "LAINNYA", "jumlah_narapidana": other_sum}])],
                ignore_index=True
            )

        fig1 = px.bar(
            top10.sort_values("jumlah_narapidana", ascending=True),
            x="jumlah_narapidana",
            y="kategori_kejahatan",
            orientation="h",
            title="Komposisi Kejahatan (Top 10 + Lainnya) — sesuai filter",
            labels={"jumlah_narapidana": "Jumlah", "kategori_kejahatan": ""},
        )
        fig1.update_traces(
            marker_color="#239bf2",
            opacity=0.92,
            hovertemplate="<b>%{y}</b><br>Jumlah: %{x:,}<extra></extra>"
        )
    else:
        by_month = (
            df_f.groupby("bulan", as_index=False)["jumlah_narapidana"]
                .sum()
        )
        by_month["bulan"] = pd.Categorical(
            by_month["bulan"].str.upper(), categories=MONTH_ORDER, ordered=True
        )
        by_month = by_month.sort_values("bulan")

        fig1 = px.bar(
            by_month,
            x="bulan",
            y="jumlah_narapidana",
            title=f"Distribusi Bulan — {st.session_state.filter_crime} (sesuai filter)",
            labels={"bulan": "Bulan", "jumlah_narapidana": "Jumlah"},
        )
        fig1.update_traces(
            marker_color="#239bf2",
            opacity=0.92,
            hovertemplate="<b>%{x}</b><br>Jumlah: %{y:,}<extra></extra>"
        )

    fig1 = apply_plot_theme(fig1, height=360)
    fig1.update_layout(
        # margin=dict(l=20, r=20, t=60, b=20),
        title_font=dict(size=18),
    )

    # =====================================================
    # (B) KANAN ATAS: Distribusi waktu (tidak redundant)
    # - Kalau crime dipilih: tren kumulatif (berbeda makna dari distribusi bulan)
    # - Kalau crime belum dipilih: distribusi bulan total (sesuai filter)
    # =====================================================
    if crime_locked:
        ts = (
            df_f.groupby("periode", as_index=False)["jumlah_narapidana"]
                .sum()
                .sort_values("periode")
        )
        ts["kumulatif"] = ts["jumlah_narapidana"].cumsum()

        fig2 = px.line(
            ts,
            x="periode",
            y="kumulatif",
            markers=True,
            title=f"Tren Kumulatif — {st.session_state.filter_crime} (sesuai filter)",
            labels={"periode": "", "kumulatif": "Total Kumulatif"},
        )
        fig2.update_traces(
            line=dict(width=3),
            hovertemplate="Periode: %{x}<br>Kumulatif: %{y:,}<extra></extra>"
        )
    else:
        # kalau user sudah mengunci bulan, pindah ke distribusi per tahun agar tetap informatif
        if not month_locked:
            agg = (
                df_f.groupby("bulan", as_index=False)["jumlah_narapidana"]
                    .sum()
            )
            agg["bulan"] = pd.Categorical(
                agg["bulan"].str.upper(), categories=MONTH_ORDER, ordered=True
            )
            agg = agg.sort_values("bulan")

            fig2 = px.bar(
                agg,
                x="bulan",
                y="jumlah_narapidana",
                title="Distribusi Jumlah per Bulan — sesuai filter",
                labels={"bulan": "Bulan", "jumlah_narapidana": "Jumlah"},
            )
        else:
            agg = (
                df_f.groupby("tahun", as_index=False)["jumlah_narapidana"]
                    .sum()
                    .sort_values("tahun")
            )
            fig2 = px.bar(
                agg,
                x="tahun",
                y="jumlah_narapidana",
                title=f"Distribusi per Tahun (bulan = {st.session_state.filter_month}) — sesuai filter",
                labels={"tahun": "Tahun", "jumlah_narapidana": "Jumlah"},
            )

        fig2.update_traces(
            marker_color="#00c896",
            opacity=0.92,
            hovertemplate="<b>%{x}</b><br>Jumlah: %{y:,}<extra></extra>"
        )

    fig2 = apply_plot_theme(fig2, height=360)
    fig2.update_layout(
        # margin=dict(l=20, r=20, t=60, b=20),
        title_font=dict(size=18),
    )

    with c1:
        st.plotly_chart(fig1, use_container_width=True, config=PLOT_CONFIG)

    with c2:
        st.plotly_chart(fig2, use_container_width=True, config=PLOT_CONFIG)

    c3, c4 = st.columns(2)

    # =====================================================
    # (C) KIRI BAWAH: Tren (filtered)
    # =====================================================
    trend = (
        df_f.groupby("periode", as_index=False)["jumlah_narapidana"]
            .sum()
            .sort_values("periode")
    )

    fig3 = px.line(
            trend,
            x="periode",
            y="jumlah_narapidana",
            markers=True,
            title="Tren Jumlah Narapidana per Periode — sesuai filter",
            labels={"periode": "", "jumlah_narapidana": "Jumlah"},
        )
        
    fig3.update_traces(
            line=dict(width=3),
            hovertemplate="Periode: %{x}<br>Jumlah: %{y:,}<extra></extra>"
        )
    fig3 = apply_plot_theme(fig3, height=360)
    fig3.update_layout(
            # margin=dict(l=20, r=20, t=60, b=20),
            title_font=dict(size=18),
    )

    # =====================================================
    # (D) KANAN BAWAH: Pola kategori sepanjang waktu
    # - Kalau crime belum dipilih: Area Top 4 kategori (pola per kategori)
    # - Kalau crime dipilih: Area trend single kategori (lebih clean)
    # =====================================================
    if not crime_locked:
        top4 = (
            df_f.groupby("kategori_kejahatan")["jumlah_narapidana"]
                .sum()
                .sort_values(ascending=False)
                .head(4)
                .index
                .tolist()
        )

        area = (
            df_f[df_f["kategori_kejahatan"].isin(top4)]
                .groupby(["periode", "kategori_kejahatan"], as_index=False)["jumlah_narapidana"]
                .sum()
                .sort_values("periode")
        )

        fig4 = px.area(
            area,
            x="periode",
            y="jumlah_narapidana",
            color="kategori_kejahatan",
            title="Pola Top 4 Kategori (Area) — sesuai filter",
            labels={"periode": "", "jumlah_narapidana": "Jumlah", "kategori_kejahatan": ""},
        )
    else:
        area = (
            df_f.groupby("periode", as_index=False)["jumlah_narapidana"]
                .sum()
                .sort_values("periode")
        )
        fig4 = px.area(
            area,
            x="periode",
            y="jumlah_narapidana",
            title=f"Pola Waktu (Area) — {st.session_state.filter_crime} (sesuai filter)",
            labels={"periode": "", "jumlah_narapidana": "Jumlah"},
        )

    fig4 = apply_plot_theme(fig4, height=360)
    fig4.update_layout(
        # margin=dict(l=20, r=20, t=60, b=20),
        title_font=dict(size=18),
    )

    with c3:
        st.plotly_chart(fig3, use_container_width=True, config=PLOT_CONFIG)

    with c4:
        st.plotly_chart(fig4, use_container_width=True, config=PLOT_CONFIG)


# =========================================================
# TAB 2: ANALISIS LANJUTAN
# Heatmap, perbandingan tahunan, dan tren kumulatif
# =========================================================
with tab2:
    # -----------------------------------------------------
    # HEATMAP: Bulan vs Kategori (Top 15)
    # -----------------------------------------------------

    heat = (
        df_f.groupby(["bulan", "kategori_kejahatan"], as_index=False)["jumlah_narapidana"]
            .sum()
    )
    heat["bulan"] = pd.Categorical(
        heat["bulan"].str.upper(), categories=MONTH_ORDER, ordered=True
    )

    top15 = (
        df_f.groupby("kategori_kejahatan")["jumlah_narapidana"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
            .index
    )
    heat = heat[heat["kategori_kejahatan"].isin(top15)]

    heat_pivot = heat.pivot_table(
        index="kategori_kejahatan",
        columns="bulan",
        values="jumlah_narapidana",
        aggfunc="sum",
        fill_value=0
    )
    fig_heat = go.Figure(
        data=go.Heatmap(
            z=heat_pivot.values,
            x=list(heat_pivot.columns),
            y=list(heat_pivot.index),
            colorbar=dict(title="Jumlah")
        )
    )
    fig_heat.update_layout(title="Heatmap: Kategori Kejahatan vs Bulan (Top 15)")
    fig_heat = apply_plot_theme(fig_heat, height=420)

    st.plotly_chart(fig_heat, use_container_width=True, config=PLOT_CONFIG)

    
    # -----------------------------------------------------
    # GROUPED BAR: Top 5 Kategori per Tahun
    # -----------------------------------------------------
     
    top5 = (
        df_f.groupby("kategori_kejahatan")["jumlah_narapidana"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .index
    )
    by_year = (
        df_f[df_f["kategori_kejahatan"].isin(top5)]
            .groupby(["tahun", "kategori_kejahatan"], as_index=False)["jumlah_narapidana"]
            .sum()
            .sort_values(["tahun", "jumlah_narapidana"], ascending=[True, False])
    )

    fig_year = px.bar(
    by_year,
    x="tahun",
    y="jumlah_narapidana",
    color="kategori_kejahatan",
    barmode="group",
    title="Perbandingan Top 5 Kategori per Tahun",
    labels={"tahun": "Tahun", "jumlah_narapidana": "Jumlah", "kategori_kejahatan": ""}
    )

    fig_year = apply_plot_theme(fig_year, height=420)
    st.plotly_chart(fig_year, use_container_width=True, config=PLOT_CONFIG)

    # -----------------------------------------------------
    # LINE CHART: Tren Kumulatif
    # -----------------------------------------------------

    cum = (
        df_f.groupby("periode", as_index=False)["jumlah_narapidana"]
            .sum()
            .sort_values("periode")
    )
    cum["kumulatif"] = cum["jumlah_narapidana"].cumsum()

    fig_cum = px.line(
        cum,
        x="periode",
        y="kumulatif",
        markers=True,
        title="Trend Kumulatif Jumlah Narapidana",
        labels={"periode": "", "kumulatif": "Total Kumulatif"}
        )

    fig_cum = apply_plot_theme(fig_cum, height=380)
    st.plotly_chart(fig_cum, use_container_width=True, config=PLOT_CONFIG)

    # =========================
    # =========================
    # YoY Growth Total Narapidana
    # =========================
    yoy = (
        df_f.groupby("tahun", as_index=False)["jumlah_narapidana"].sum()
        .sort_values("tahun")
    )

    yoy["yoy_pct"] = yoy["jumlah_narapidana"].pct_change() * 100
    yoy["yoy_pct"] = yoy["yoy_pct"].fillna(0)

    # Warna dinamis berdasarkan naik/turun
    colors = []
    for val in yoy["yoy_pct"]:
        if val > 0:
            colors.append("#19a0e9")   # biru
        elif val < 0:
            colors.append("#ef4444")   # merah
        else:
            colors.append("#689fff")   # biru

    fig_yoy = go.Figure(
        data=[
            go.Bar(
                x=yoy["tahun"],
                y=yoy["yoy_pct"],
                marker_color=colors
            )
        ]
    )

    fig_yoy.update_layout(
        title="Pertumbuhan Tahunan (YoY) Jumlah Narapidana (%)",
        xaxis_title="Tahun",
        yaxis_title="YoY (%)"
    )

    fig_yoy.update_traces(
        hovertemplate="Tahun: %{x}<br>YoY: %{y:.2f}%<extra></extra>"
    )

    fig_yoy = apply_plot_theme(fig_yoy, height=360)
    st.plotly_chart(fig_yoy, use_container_width=True, config=PLOT_CONFIG)


# TAB 3: KOMPOSISI (COPY-PASTE FULL)
# =========================
# =========================
# TAB 3: KOMPOSISI (SIAP COPAS) — JUDUL DI DALAM KOTAK, TANPA "undefined"
# =========================
with tab3:

    # =========================
    # 1) TREEMAP (FULL WIDTH)
    # =========================
    tree = (
        df_f.groupby("kategori_kejahatan", as_index=False)["jumlah_narapidana"]
        .sum()
        .sort_values("jumlah_narapidana", ascending=False)
    )

    fig_tree = px.treemap(
        tree,
        path=["kategori_kejahatan"],
        values="jumlah_narapidana",
    )

    # (opsional) hover lebih jelas
    fig_tree.update_traces(
        hovertemplate="<b>%{label}</b><br>Jumlah: %{value:,}<extra></extra>"
    )

    # ✅ apply theme dulu
    fig_tree = apply_plot_theme(fig_tree, height=380)

    # ✅ SET TITLE SETELAH THEME (anti "undefined" walau theme menimpa title)
    fig_tree.update_layout(
        title=dict(
            text="Treemap Kategori Kejahatan",
        ),
    )

    st.plotly_chart(fig_tree, use_container_width=True, config=PLOT_CONFIG)

    st.markdown("---")

    # =========================
    # 2) STRUKTUR KATEGORI PER TAHUN (%) (FULL WIDTH, RAPI)
    # =========================
    share_year = (
        df_f.groupby(["tahun", "kategori_kejahatan"], as_index=False)["jumlah_narapidana"]
        .sum()
    )
    share_year["total_tahun"] = share_year.groupby("tahun")["jumlah_narapidana"].transform("sum")
    share_year["proporsi_pct"] = (share_year["jumlah_narapidana"] / share_year["total_tahun"]) * 100

    # ✅ biar legend gak rame: Top 6 + LAINNYA
    topN = (
        df_f.groupby("kategori_kejahatan")["jumlah_narapidana"]
        .sum()
        .sort_values(ascending=False)
        .head(6)
        .index
    )
    share_year["kategori_plot"] = share_year["kategori_kejahatan"].where(
        share_year["kategori_kejahatan"].isin(topN),
        "LAINNYA"
    )

    share_plot = (
        share_year.groupby(["tahun", "kategori_plot"], as_index=False)["proporsi_pct"]
        .sum()
        .sort_values(["tahun", "proporsi_pct"], ascending=[True, False])
    )

    fig_comp = px.bar(
        share_plot,
        x="tahun",
        y="proporsi_pct",
        color="kategori_plot",
        barmode="stack",
        labels={"tahun": "Tahun", "proporsi_pct": "Proporsi (%)", "kategori_plot": ""},
    )

    # ✅ apply theme dulu
    fig_comp = apply_plot_theme(fig_comp, height=420)

    # ✅ SET TITLE SETELAH THEME (anti "undefined") + legend rapi
    fig_comp.update_layout(
        title=dict(
            text="Struktur Kategori per Tahun (%)",
        ),
        margin=dict(t=70, b=95, l=16, r=16),
    )
    fig_comp.update_yaxes(range=[0, 100], ticksuffix="%")

    st.plotly_chart(fig_comp, use_container_width=True, config=PLOT_CONFIG)


# TABEL DATA + EXPORT
# Menyediakan tabel rekap dan opsi unduh CSV/Excel


st.subheader("Data Narapidana (Rekap)", anchor=False)
st.caption(
    "Tabel ini menampilkan rekap jumlah narapidana per kategori kejahatan, "
    "jenis kelamin, dan periode (bulan-tahun)."
)

# Input pencarian kategori
q = st.text_input("Cari kategori kejahatan (opsional)", "")

# Kolom yang ditampilkan
cols = ["kategori_kejahatan", "jenis_kelamin", "jumlah_narapidana", "bulan", "tahun", "periode"]
if "nama_kabupaten_kota" in df_f.columns:
    cols = ["nama_kabupaten_kota"] + cols

table = df_f[cols].copy()

# Terapkan pencarian teks
if q.strip():
    table = table[table["kategori_kejahatan"].str.contains(q, case=False, na=False)]

# Urutkan data
table = table.sort_values(
    ["periode", "kategori_kejahatan", "jenis_kelamin"],
    ascending=[False, True, True]
)

# Tampilkan tabel
st.write(f"Total baris: **{len(table):,}**")
st.dataframe(table.drop(columns=["periode"]), use_container_width=True, height=360)

# ---------------------------------------------------------
# EXPORT DATA
# ---------------------------------------------------------
csv_bytes = table.drop(columns=["periode"]).to_csv(index=False).encode("utf-8")

xlsx_buffer = io.BytesIO()
with pd.ExcelWriter(xlsx_buffer, engine="openpyxl") as writer:
    table.drop(columns=["periode"]).to_excel(
        writer, index=False, sheet_name="filtered"
    )

x1, x2, x3 = st.columns([1.2, 1.2, 6])
with x1:
    st.download_button(
        "⬇️ Export CSV",
        data=csv_bytes,
        file_name="dashboard_lapas_cirebon_filtered.csv",
        mime="text/csv",
        use_container_width=True
    )
with x2:
    st.download_button(
        "⬇️ Export Excel",
        data=xlsx_buffer.getvalue(),
        file_name="dashboard_lapas_cirebon_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# Catatan kaki
st.markdown(
    "<div style='opacity:0.7; font-size:12px; margin-top:12px;'>"
    "Catatan: Semua grafik mengikuti filter (Gender, Kejahatan, Tahun, Bulan). "
    "Tingkat hunian dihitung dari total data (sesuai filter) dibanding kapasitas yang diisi di sidebar."
    "</div>",
    unsafe_allow_html=True
)
