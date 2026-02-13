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
    --bg:#f1f5f9;
    --card:#ffffff;
    --text:#0f172a;
}

/* Background (lebih kompatibel di hosting & mobile) */
html, body, .stApp, [data-testid="stAppViewContainer"]{
    background: linear-gradient(180deg, #f8fbff 0%, #e6efff 100%) !important; /* cerah tapi jelas */
}

/* Biar konten utama gak nimpain background */
[data-testid="stAppViewContainer"] > .main{
    background: transparent !important;
}

/* Card: jangan terlalu transparan biar gak "samar" */
:root{
    --card: rgba(255,255,255,0.98);
}

/* Mobile: matiin blur (ini yang sering bikin kabut di HP) */
@media (max-width: 768px){
    .glass{
        backdrop-filter: none !important;
    }
}


/* Container */
.block-container{
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

/* Hilangkan elemen default */
#MainMenu, footer, header{visibility:hidden;}

/* Card */
.glass{
    background: var(--card);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,.08);
}

/* Header */
.topbar{
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    color: white;
    border-radius: 18px;
    padding: 22px 26px;
    box-shadow: 0 12px 30px rgba(37,99,235,.35);
}

/* KPI Cards */
.cards{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:16px;
}

.card{
    border-radius:18px;
    padding:18px;
    color:white;
    box-shadow:0 12px 28px rgba(0,0,0,.15);
}

.card .value{
    font-size:32px;
    font-weight:800;
}

.card.c1{background:linear-gradient(135deg,#2563eb,#1e40af);}
.card.c2{background:linear-gradient(135deg,#16a34a,#15803d);}
.card.c3{background:linear-gradient(135deg,#ec4899,#be185d);}
.card.c4{background:linear-gradient(135deg,#f59e0b,#b45309);}

/* Sidebar */
section[data-testid="stSidebar"]>div{
    background:#ffffff;
    box-shadow:inset -1px 0 0 rgba(0,0,0,.05);
}

/* Judul */
h1,h2,h3{
    letter-spacing:-0.3px;
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


# =========================================================
# SIDEBAR – DATA SOURCE & PARAMETER
# =========================================================
st.sidebar.markdown("## ⚙️ Pengaturan")
st.sidebar.caption(
    "Gunakan file Excel yang kamu kirim, atau upload ulang jika ingin update data."
)

# Upload file Excel oleh user
uploaded = st.sidebar.file_uploader(
    "Upload data (Excel .xlsx)", type=["xlsx"]
)

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
    if uploaded is not None:
        df_raw = load_excel_from_upload(uploaded)
    else:
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
st.title("🛡️ Dashboard Lapas Cirebon")
st.caption("Sistem Informasi Data Narapidana · Live Update")
st.info(f"🗓️ Terakhir diperbarui: {last_update_str}")
st.divider()


# Layout filter menggunakan kolom
f1, f2, f3, f4, f5 = st.columns([2, 3, 2, 2, 2])

with f1:
    # Filter berdasarkan jenis kelamin
    st.session_state.filter_gender = st.selectbox(
        "Jenis Kelamin",
        gender_opts,
        index=gender_opts.index(st.session_state.filter_gender)
    )

with f2:
    # Filter berdasarkan kategori kejahatan
    st.session_state.filter_crime = st.selectbox(
        "Jenis Kejahatan",
        crime_opts,
        index=crime_opts.index(st.session_state.filter_crime)
    )

with f3:
    # Filter berdasarkan tahun
    st.session_state.filter_year = st.selectbox(
        "Tahun",
        year_opts,
        index=year_opts.index(st.session_state.filter_year)
    )

with f4:
    # Filter berdasarkan bulan
    st.session_state.filter_month = st.selectbox(
        "Bulan",
        month_opts,
        index=month_opts.index(st.session_state.filter_month)
    )

with f5:
    # Tombol untuk mengembalikan seluruh filter ke kondisi awal
    if st.button("Reset Filter", use_container_width=True):
        st.session_state.filter_gender = "Semua"
        st.session_state.filter_crime = "Semua Kejahatan"
        st.session_state.filter_year = "Semua"
        st.session_state.filter_month = "Semua"
        st.rerun()


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


# =========================================================
# INFORMASI DASHBOARD + KPI RINGKAS
# =========================================================

st.markdown("## Dashboard Visualisasi Data Narapidana Cirebon",)
st.markdown(
    "Dashboard ini menyajikan visualisasi data narapidana berdasarkan kategori kejahatan, "
    "waktu, dan karakteristik lainnya untuk mendukung pengambilan keputusan berbasis data.",
)
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
st.subheader("📊 Ringkasan Utama (KPI)")
st.caption("Kondisi terkini berdasarkan periode terakhir")
st.divider()
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown("<div style='opacity:0.9; font-size:13px;'>Total Narapidana</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:40px; font-weight:900; line-height:1.05;'>{total_kpi:,}</div>",
        unsafe_allow_html=True
    )

with k2:
    st.markdown("<div style='opacity:0.9; font-size:13px;'>Kategori Terbanyak</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:34px; font-weight:900; line-height:1.05; text-transform:uppercase;'>"
        f"{top_crime}</div>",
        unsafe_allow_html=True
    )

with k3:
    st.markdown("<div style='opacity:0.9; font-size:13px;'>Bulan Terpadat</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:34px; font-weight:900; line-height:1.05; text-transform:uppercase;'>"
        f"{densest_month}</div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


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

# Jumlah narapidana perempuan
female = int(
    df_f.loc[
        df_f["jenis_kelamin"].str.contains("PEREMPUAN", na=False),
        "jumlah_narapidana"
    ].sum()
)

# Tingkat hunian lapas (%)
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

# =========================================================
# TAB UNTUK VISUALISASI
# =========================================================
tab1, tab2, tab3 = st.tabs(
    ["Grafik Utama", "Analisis Lanjutan", "Komposisi"]
)

# =========================================================
# TAB 1: GRAFIK UTAMA
# Menampilkan visualisasi inti: distribusi, komposisi, dan tren
# =========================================================
with tab1:
    # Membagi area menjadi dua kolom
    c1, c2 = st.columns(2)

    # -----------------------------------------------------
    # BAR CHART: Top 10 Kategori Kejahatan
    # -----------------------------------------------------
    crime_agg = (
        df_f.groupby("kategori_kejahatan", as_index=False)["jumlah_narapidana"]
            .sum()
            .sort_values("jumlah_narapidana", ascending=False)
    )
    crime_top = crime_agg.head(10)

    fig_bar = px.bar(
        crime_top.sort_values("jumlah_narapidana", ascending=True),
        x="jumlah_narapidana",
        y="kategori_kejahatan",
        orientation="h",
        title="Distribusi Jenis Kejahatan (Top 10)",
        labels={"jumlah_narapidana": "Jumlah", "kategori_kejahatan": ""},
    )
    fig_bar.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18),
    )

    # -----------------------------------------------------
    # PIE CHART: Distribusi Jenis Kelamin
    # -----------------------------------------------------
    gender_agg = pd.DataFrame(
        {"Jenis Kelamin": ["Laki-laki", "Perempuan"], "Jumlah": [male, female]}
    )
    fig_pie = px.pie(
        gender_agg,
        names="Jenis Kelamin",
        values="Jumlah",
        title="Distribusi Jenis Kelamin",
        hole=0.55
    )
    fig_pie.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18),
        legend_title_text="",
    )

    # Render grafik
    with c1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # LINE CHART: Tren Penghuni per Bulan (by Gender)
    # -----------------------------------------------------
    c3, c4 = st.columns(2)

    trend = (
        df_f.groupby(["periode", "jenis_kelamin"], as_index=False)["jumlah_narapidana"]
            .sum()
            .sort_values("periode")
    )
    fig_line = px.line(
        trend,
        x="periode",
        y="jumlah_narapidana",
        color="jenis_kelamin",
        markers=True,
        title="Trend Penghuni Lapas (per Bulan)",
        labels={"periode": "", "jumlah_narapidana": "Jumlah", "jenis_kelamin": ""}
    )
    fig_line.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18),
    )

    # -----------------------------------------------------
    # AREA CHART: Top 4 Kategori Sepanjang Waktu
    # -----------------------------------------------------
    top_cats = crime_agg.head(4)["kategori_kejahatan"].tolist()
    area = (
        df_f[df_f["kategori_kejahatan"].isin(top_cats)]
            .groupby(["periode", "kategori_kejahatan"], as_index=False)["jumlah_narapidana"]
            .sum()
            .sort_values("periode")
    )
    fig_area = px.area(
        area,
        x="periode",
        y="jumlah_narapidana",
        color="kategori_kejahatan",
        title="Kategori Pidana (Top 4) - Area",
        labels={"periode": "", "jumlah_narapidana": "Jumlah", "kategori_kejahatan": ""}
    )
    fig_area.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18),
    )

    with c3:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.plotly_chart(fig_area, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 2: ANALISIS LANJUTAN
# Heatmap, perbandingan tahunan, dan tren kumulatif
# =========================================================
with tab2:
    # -----------------------------------------------------
    # HEATMAP: Bulan vs Kategori (Top 15)
    # -----------------------------------------------------
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

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

    fig_heat = px.imshow(
        heat_pivot,
        title="Heatmap: Kategori Kejahatan vs Bulan (Top 15)",
        labels=dict(x="Bulan", y="Kategori", color="Jumlah"),
        aspect="auto"
    )
    fig_heat.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18)
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # GROUPED BAR: Top 5 Kategori per Tahun
    # -----------------------------------------------------
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

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
    fig_year.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18)
    )
    st.plotly_chart(fig_year, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # LINE CHART: Tren Kumulatif
    # -----------------------------------------------------
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

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
    fig_cum.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18)
    )
    st.plotly_chart(fig_cum, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 3: KOMPOSISI
# Treemap dan 100% stacked bar
# =========================================================
with tab3:
    c5, c6 = st.columns(2)

    # -----------------------------------------------------
    # TREEMAP: Kategori -> Jenis Kelamin (Top 12)
    # -----------------------------------------------------
    with c5:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)

        tree = (
            df_f.groupby(["kategori_kejahatan", "jenis_kelamin"], as_index=False)["jumlah_narapidana"]
                .sum()
        )
        top12 = (
            df_f.groupby("kategori_kejahatan")["jumlah_narapidana"]
                .sum()
                .sort_values(ascending=False)
                .head(12)
                .index
        )
        tree = tree[tree["kategori_kejahatan"].isin(top12)]

        fig_tree = px.treemap(
            tree,
            path=["kategori_kejahatan", "jenis_kelamin"],
            values="jumlah_narapidana",
            title="Treemap: Kategori → Jenis Kelamin"
        )
        fig_tree.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=18)
        )
        st.plotly_chart(fig_tree, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # 100% STACKED BAR: Proporsi Gender per Kategori (Top 10)
    # -----------------------------------------------------
    with c6:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)

        top10 = (
            df_f.groupby("kategori_kejahatan")["jumlah_narapidana"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .index
        )

        gshare = (
            df_f[df_f["kategori_kejahatan"].isin(top10)]
                .groupby(["kategori_kejahatan", "jenis_kelamin"], as_index=False)["jumlah_narapidana"]
                .sum()
        )

        # Hitung total per kategori untuk mendapatkan proporsi
        gtotal = (
            gshare.groupby("kategori_kejahatan", as_index=False)["jumlah_narapidana"]
                .sum()
                .rename(columns={"jumlah_narapidana": "total"})
        )
        gshare = gshare.merge(gtotal, on="kategori_kejahatan", how="left")
        gshare["proporsi"] = np.where(
            gshare["total"] > 0,
            (gshare["jumlah_narapidana"] / gshare["total"]) * 100,
            0
        )

        fig_stack = px.bar(
            gshare,
            x="proporsi",
            y="kategori_kejahatan",
            color="jenis_kelamin",
            orientation="h",
            barmode="stack",
            title="Proporsi Gender per Kategori (Top 10) - 100%",
            labels={"proporsi": "Proporsi (%)", "kategori_kejahatan": "", "jenis_kelamin": ""}
        )
        fig_stack.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=18)
        )
        st.plotly_chart(fig_stack, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)


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
