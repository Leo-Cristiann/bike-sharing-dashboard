import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import streamlit as st
import numpy as np

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  –  dark editorial theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0D0D0D;
    color: #F0EDE8;
}

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: #141414;
    border-right: 1px solid #2A2A2A;
}
section[data-testid="stSidebar"] * { color: #F0EDE8 !important; }

/* ── main container ── */
.block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }

/* ── page title ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.1;
    background: linear-gradient(90deg, #F5E642 0%, #F0EDE8 60%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: .25rem;
}
.hero-sub {
    font-size: 1rem;
    color: #888;
    margin-bottom: 2rem;
    letter-spacing: .5px;
}

/* ── section heading ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #F5E642;
    letter-spacing: .5px;
    border-left: 4px solid #F5E642;
    padding-left: .6rem;
    margin-bottom: 1rem;
}

/* ── metric cards ── */
.metric-card {
    background: #181818;
    border: 1px solid #2A2A2A;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color .2s;
}
.metric-card:hover { border-color: #F5E642; }
.metric-accent {
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 16px 0 0 16px;
}
.metric-label {
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #777;
    margin-bottom: .35rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #F0EDE8;
    line-height: 1;
}
.metric-delta {
    font-size: .8rem;
    color: #5FD16B;
    margin-top: .3rem;
}

/* ── chart containers ── */
.chart-card {
    background: #181818;
    border: 1px solid #2A2A2A;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* ── insight box ── */
.insight-box {
    background: #1E1E00;
    border: 1px solid #F5E642;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    font-size: .9rem;
    color: #E8E4C0;
    margin-top: .75rem;
}
.insight-box b { color: #F5E642; }

/* ── divider ── */
hr { border-color: #2A2A2A; margin: 2rem 0; }

/* ── streamlit default overrides ── */
div[data-testid="metric-container"] { display: none; }
.stDateInput label, .stSelectbox label { color: #999 !important; font-size: .85rem !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MATPLOTLIB THEME
# ─────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#181818",
    "axes.facecolor":    "#181818",
    "axes.edgecolor":    "#2A2A2A",
    "axes.labelcolor":   "#999",
    "axes.titlecolor":   "#F0EDE8",
    "xtick.color":       "#666",
    "ytick.color":       "#666",
    "grid.color":        "#242424",
    "grid.linewidth":    0.8,
    "text.color":        "#F0EDE8",
    "font.family":       "sans-serif",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.labelsize":    10,
})

YELLOW  = "#F5E642"
TEAL    = "#3ECFCF"
CORAL   = "#FF6B5B"
VIOLET  = "#A78BFA"
GREEN   = "#5FD16B"
PALETTE = [YELLOW, TEAL, CORAL, VIOLET]


# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    day_df  = pd.read_csv("cleaned_bike_day.csv")
    hour_df = pd.read_csv("cleaned_bike_hour.csv")
    day_df["dteday"]  = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
    return day_df, hour_df

day_df, hour_df = load_data()


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚲 Bike Analytics")
    st.markdown("---")

    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()

    st.markdown("#### Filter Periode")
    start_date, end_date = st.date_input(
        "Rentang Tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

    st.markdown("---")
    st.markdown(
        "<div style='color:#555; font-size:.8rem; line-height:1.6'>"
        "Dataset: Capital Bikeshare<br>Kota: Washington D.C.<br>Periode: 2011 – 2012"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<br><div style='color:#444; font-size:.75rem'>© 2024 Proyek Analisis Data</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FILTER DATA
# ─────────────────────────────────────────────
main_day  = day_df[(day_df["dteday"] >= str(start_date))  & (day_df["dteday"] <= str(end_date))]
main_hour = hour_df[(hour_df["dteday"] >= str(start_date)) & (hour_df["dteday"] <= str(end_date))]


# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">Bike Sharing<br>Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Eksplorasi pola penyewaan sepeda · Washington D.C. · 2011–2012</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  KPI CARDS  (HTML rendered)
# ─────────────────────────────────────────────
total_rentals    = main_day["cnt"].sum()
total_registered = main_day["registered"].sum()
total_casual     = main_day["casual"].sum()
avg_daily        = int(main_day["cnt"].mean())
pct_registered   = total_registered / total_rentals * 100 if total_rentals else 0

col1, col2, col3, col4 = st.columns(4)

cards = [
    (col1, "Total Penyewaan",          f"{total_rentals:,}",    YELLOW,  "Semua transaksi"),
    (col2, "Pengguna Registered",      f"{total_registered:,}", TEAL,    f"{pct_registered:.1f}% dari total"),
    (col3, "Pengguna Casual",          f"{total_casual:,}",     CORAL,   f"{100-pct_registered:.1f}% dari total"),
    (col4, "Rata-rata / Hari",         f"{avg_daily:,}",        VIOLET,  "Penyewaan harian"),
]
for col, label, value, accent, delta in cards:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-accent" style="background:{accent}"></div>
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-delta">↗ {delta}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ROW 1 — Tren Harian  +  Distribusi Musim
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">01 · Tren & Musim</div>', unsafe_allow_html=True)

r1col1, r1col2 = st.columns([2, 1])

with r1col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    # rolling average trend line
    trend = main_day.set_index("dteday")["cnt"].rolling(7).mean()
    raw   = main_day.set_index("dteday")["cnt"]

    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.fill_between(raw.index, raw.values, alpha=.12, color=YELLOW)
    ax.plot(raw.index, raw.values, color="#333", linewidth=.8, alpha=.6)
    ax.plot(trend.index, trend.values, color=YELLOW, linewidth=2.2, label="7-day avg")
    ax.set_title("Tren Penyewaan Harian", pad=12)
    ax.set_xlabel("")
    ax.legend(frameon=False, labelcolor=YELLOW, fontsize=9)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with r1col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    season_map   = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin",
                    "Spring": "Semi", "Summer": "Panas", "Fall": "Gugur", "Winter": "Dingin"}
    season_total = main_day.groupby("season")["cnt"].sum()
    labels       = [season_map.get(s, str(s)) for s in season_total.index]
    sizes        = season_total.values
    colors       = [YELLOW, TEAL, CORAL, VIOLET]

    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.0f%%",
        colors=colors, startangle=140,
        wedgeprops=dict(width=0.55, edgecolor="#0D0D0D", linewidth=2),
        textprops={"fontsize": 9, "color": "#AAA"},
    )
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_color("#F0EDE8")
    ax.set_title("Proporsi per Musim", pad=10)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

# insight box
_idx = season_total.idxmax()
season_best = season_map.get(_idx, str(_idx))
st.markdown(f"""
<div class="insight-box">
💡 <b>Insight:</b> Musim <b>{season_best}</b> mencatat penyewaan tertinggi
({season_total.max():,} penyewaan).
Pola ini konsisten dengan cuaca yang mendukung aktivitas luar ruangan.
</div>""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ROW 2 — Casual vs Registered
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">02 · Casual vs Registered</div>', unsafe_allow_html=True)

r2col1, r2col2 = st.columns([1, 1])

with r2col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    uwd = main_day.groupby("workingday")[["casual", "registered"]].mean().reset_index()
    uwd["workingday"] = uwd["workingday"].map({0: "Libur / Akhir Pekan", 1: "Hari Kerja"})
    uwd_m = uwd.melt(id_vars="workingday", var_name="user_type", value_name="avg")

    x     = np.arange(len(uwd["workingday"]))
    width = 0.35
    cas   = uwd_m[uwd_m["user_type"] == "casual"]["avg"].values
    reg   = uwd_m[uwd_m["user_type"] == "registered"]["avg"].values

    fig, ax = plt.subplots(figsize=(6, 4))
    b1 = ax.bar(x - width/2, cas, width, color=CORAL,  label="Casual",     alpha=.9, zorder=3)
    b2 = ax.bar(x + width/2, reg, width, color=TEAL,   label="Registered", alpha=.9, zorder=3)
    ax.bar_label(b1, fmt="%.0f", fontsize=8, color=CORAL,  padding=3)
    ax.bar_label(b2, fmt="%.0f", fontsize=8, color=TEAL,   padding=3)
    ax.set_xticks(x)
    ax.set_xticklabels(uwd["workingday"].values, fontsize=9)
    ax.set_title("Rata-rata Penyewaan: Casual vs Registered", pad=10)
    ax.set_ylabel("Rata-rata / Hari")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", linestyle="--")
    ax.set_axisbelow(True)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with r2col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    # Monthly stacked area
    main_day["month"] = main_day["dteday"].dt.to_period("M").astype(str)
    monthly = main_day.groupby("month")[["casual", "registered"]].sum().tail(18)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.stackplot(
        monthly.index,
        monthly["casual"].values,
        monthly["registered"].values,
        labels=["Casual", "Registered"],
        colors=[CORAL, TEAL],
        alpha=.85,
    )
    ax.set_title("Komposisi Bulanan (Casual vs Registered)", pad=10)
    ax.set_xlabel("")
    ax.set_ylabel("Total Penyewaan")
    ax.tick_params(axis="x", rotation=45, labelsize=7)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.grid(axis="y", linestyle="--")
    ax.set_axisbelow(True)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
💡 <b>Insight:</b> Pengguna <b>Registered</b> mendominasi hari kerja — kemungkinan besar merupakan
komuter rutin. Sebaliknya, pengguna <b>Casual</b> justru lebih aktif saat akhir pekan,
mengindikasikan pola rekreasional.
</div>""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ROW 3 — Kategori Waktu  +  Heatmap Jam
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">03 · Analisis Waktu</div>', unsafe_allow_html=True)

r3col1, r3col2 = st.columns([1, 1.4])

with r3col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    if "time_category" in main_hour.columns:
        order   = ["Pagi", "Siang", "Sore", "Malam"]
        tc_data = main_hour.groupby("time_category")["cnt"].sum().reindex(order).fillna(0)
        colors_tc = [YELLOW, CORAL, TEAL, VIOLET]

        fig, ax = plt.subplots(figsize=(5.5, 4))
        bars = ax.barh(tc_data.index, tc_data.values, color=colors_tc, height=0.55, zorder=3)
        ax.bar_label(bars, fmt="{:,.0f}", fontsize=8.5, padding=5, color="#AAA")
        ax.set_title("Total Penyewaan per Kategori Waktu", pad=10)
        ax.set_xlabel("Total Penyewaan")
        ax.invert_yaxis()
        ax.grid(axis="x", linestyle="--")
        ax.set_axisbelow(True)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Kolom `time_category` tidak ditemukan di dataset jam.")
    st.markdown("</div>", unsafe_allow_html=True)

with r3col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    if "hr" in main_hour.columns:
        pivot = main_hour.pivot_table(
            index="hr", columns="workingday", values="cnt", aggfunc="mean"
        ).rename(columns={0: "Libur/Akhir Pekan", 1: "Hari Kerja"})

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(pivot.index, pivot.get("Hari Kerja",       pd.Series(dtype=float)),
                color=YELLOW, linewidth=2.2, marker="o", markersize=3.5, label="Hari Kerja")
        ax.plot(pivot.index, pivot.get("Libur/Akhir Pekan", pd.Series(dtype=float)),
                color=TEAL,   linewidth=2.2, marker="s", markersize=3.5, label="Libur / Akhir Pekan",
                linestyle="--")
        ax.fill_between(pivot.index,
                        pivot.get("Hari Kerja", 0),
                        pivot.get("Libur/Akhir Pekan", 0),
                        alpha=.08, color=YELLOW)
        ax.set_title("Rata-rata Penyewaan per Jam dalam Sehari", pad=10)
        ax.set_xlabel("Jam")
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.set_xticks(range(0, 24, 2))
        ax.legend(frameon=False, fontsize=9)
        ax.grid(linestyle="--")
        ax.set_axisbelow(True)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Kolom `hr` tidak ditemukan di dataset jam.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
💡 <b>Insight:</b> Pada <b>hari kerja</b> terdapat dua puncak penyewaan (jam 8 pagi & 5–6 sore),
mencerminkan pola <b>commuting</b>. Pada <b>akhir pekan</b>, penyewaan menyebar merata
sepanjang siang hari dengan puncak tunggal sekitar tengah hari.
</div>""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ROW 4 — Cuaca  +  Suhu
# ─────────────────────────────────────────────
if "weathersit" in main_day.columns and "temp" in main_day.columns:
    st.markdown('<div class="section-label">04 · Cuaca & Temperatur</div>', unsafe_allow_html=True)

    r4col1, r4col2 = st.columns([1, 1])

    with r4col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        weather_map = {
            1: "Cerah", 2: "Mendung", 3: "Hujan Ringan", 4: "Hujan Lebat",
            "Clear": "Cerah", "Mist": "Mendung", "Cloudy": "Mendung",
            "Light Snow": "Hujan Ringan", "Light Rain": "Hujan Ringan",
            "Heavy Rain": "Hujan Lebat", "Heavy Snow": "Hujan Lebat",
        }
        wdf = main_day.copy()
        wdf["weather_label"] = wdf["weathersit"].map(weather_map).fillna(wdf["weathersit"].astype(str))
        weather_avg = wdf.groupby("weather_label")["cnt"].mean().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(5.5, 4))
        bars = ax.bar(weather_avg.index, weather_avg.values,
                      color=[YELLOW, TEAL, CORAL, VIOLET][:len(weather_avg)],
                      alpha=.9, zorder=3, width=.55)
        ax.bar_label(bars, fmt="{:,.0f}", fontsize=8.5, padding=3, color="#AAA")
        ax.set_title("Rata-rata Penyewaan Berdasarkan Cuaca", pad=10)
        ax.set_ylabel("Rata-rata / Hari")
        ax.tick_params(axis="x", rotation=15)
        ax.grid(axis="y", linestyle="--")
        ax.set_axisbelow(True)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    with r4col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5.5, 4))
        ax.scatter(
            main_day["temp"] * 41,        # denormalize to °C approx
            main_day["cnt"],
            alpha=.35, s=20,
            c=main_day["cnt"],
            cmap="YlOrRd",
            edgecolors="none",
        )
        # trend line
        z = np.polyfit(main_day["temp"], main_day["cnt"], 1)
        p = np.poly1d(z)
        t_range = np.linspace(main_day["temp"].min(), main_day["temp"].max(), 100)
        ax.plot(t_range * 41, p(t_range), color=YELLOW, linewidth=2, label="Tren")
        ax.set_title("Korelasi Suhu vs Jumlah Penyewaan", pad=10)
        ax.set_xlabel("Suhu (°C approx)")
        ax.set_ylabel("Total Penyewaan")
        ax.legend(frameon=False, fontsize=9)
        ax.grid(linestyle="--")
        ax.set_axisbelow(True)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    💡 <b>Insight:</b> Terdapat korelasi <b>positif</b> antara suhu dan jumlah penyewaan.
    Cuaca cerah meningkatkan penyewaan secara signifikan; hujan lebat menurunkannya drastis.
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 2rem 0 1rem; color:#444; font-size:.8rem; letter-spacing:.5px'>
    © 2024 · Proyek Analisis Data · Bike Sharing Dataset · Washington D.C.
</div>""", unsafe_allow_html=True)