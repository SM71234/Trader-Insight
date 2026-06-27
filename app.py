import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import io
import re
import base64

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Trader Insight Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --teal:    #2dd4bf;
    --teal-d:  #0891b2;
    --amber:   #fbbf24;
    --red:     #f87171;
    --green:   #34d399;
    --purple:  #a78bfa;
    --bg1:     #080c12;
    --bg2:     #0d1117;
    --bg3:     #161b22;
    --bg4:     #1c2333;
    --border:  #21262d;
    --border2: #30363d;
    --t1:      #e6edf3;
    --t2:      #8b949e;
    --t3:      #484f58;
}

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif !important;
}
.stApp {
    background: var(--bg1) !important;
    color: var(--t1) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    max-width: 1280px !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

/* ──────────────────────────────────────────────
   TOP NAV
────────────────────────────────────────────── */
.topbar {
    background: var(--bg2);
    border-bottom: 1px solid var(--border2);
    padding: 0 28px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -1.5rem 2.5rem -1.5rem;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
}
.topbar-left { display: flex; align-items: center; gap: 20px; }
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    font-weight: 700;
    color: #e6edf3;
    letter-spacing: -0.03em;
    text-decoration: none;
}
.topbar-logo {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #2dd4bf 0%, #0891b2 100%);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    box-shadow: 0 0 16px #2dd4bf44;
    flex-shrink: 0;
}
.topbar-divider { width: 1px; height: 20px; background: var(--border2); }
.topbar-nav { display: flex; align-items: center; gap: 4px; }
.topbar-nav-item {
    font-size: 12px;
    font-weight: 500;
    color: var(--t2);
    padding: 5px 12px;
    border-radius: 7px;
    cursor: default;
    transition: all 0.15s;
}
.topbar-nav-item.active {
    background: var(--bg4);
    color: var(--t1);
    border: 1px solid var(--border2);
}
.topbar-right { display: flex; align-items: center; gap: 12px; }
.topbar-status {
    display: flex; align-items: center; gap: 6px;
    font-size: 11px; font-weight: 600;
    color: var(--green);
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.2);
    padding: 4px 10px;
    border-radius: 100px;
}
.status-dot {
    width: 6px; height: 6px;
    background: var(--green);
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(52,211,153,0.4); }
    50% { opacity: 0.5; box-shadow: 0 0 0 4px rgba(52,211,153,0); }
}
.topbar-badge {
    font-size: 10px; font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg4);
    color: var(--t2);
    border: 1px solid var(--border2);
    padding: 4px 10px;
    border-radius: 100px;
    letter-spacing: 0.04em;
}

/* ──────────────────────────────────────────────
   UPLOAD ZONE
────────────────────────────────────────────── */
.upload-zone {
    background: var(--bg3);
    border: 1.5px dashed var(--border2);
    border-radius: 16px;
    padding: 40px 32px 32px;
    text-align: center;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.upload-zone::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(45,212,191,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.upload-icon {
    font-size: 36px;
    margin-bottom: 12px;
    filter: drop-shadow(0 0 12px rgba(45,212,191,0.3));
}
.upload-title {
    font-size: 17px; font-weight: 700;
    color: var(--t1);
    margin-bottom: 6px;
    letter-spacing: -0.03em;
}
.upload-sub {
    font-size: 12px; color: var(--t2);
    margin-bottom: 0;
    line-height: 1.6;
}
.upload-tags {
    display: flex; justify-content: center; gap: 8px;
    margin-top: 12px; flex-wrap: wrap;
}
.upload-tag {
    font-size: 10px; font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    color: var(--t3);
    background: var(--bg4);
    border: 1px solid var(--border);
    padding: 3px 8px; border-radius: 5px;
    letter-spacing: 0.04em;
}

/* ──────────────────────────────────────────────
   FILE PILL
────────────────────────────────────────────── */
.file-pill {
    background: var(--bg3);
    border: 1px solid rgba(45,212,191,0.3);
    border-radius: 12px;
    padding: 14px 20px;
    margin-bottom: 14px;
    display: flex; align-items: center; gap: 14px;
    box-shadow: 0 0 20px rgba(45,212,191,0.06);
}
.fp-icon { font-size: 24px; flex-shrink: 0; }
.fp-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px; font-weight: 600;
    color: var(--teal);
}
.fp-meta { font-size: 11px; color: var(--t2); margin-top: 2px; }
.fp-badge {
    margin-left: auto; flex-shrink: 0;
    font-size: 10px; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    background: rgba(52,211,153,0.1);
    color: var(--green);
    border: 1px solid rgba(52,211,153,0.25);
    padding: 3px 9px; border-radius: 100px;
    letter-spacing: 0.06em;
}

/* ──────────────────────────────────────────────
   CLIENT STRIP
────────────────────────────────────────────── */
.client-strip {
    background: var(--bg3);
    border: 1px solid var(--border2);
    border-radius: 12px;
    padding: 16px 22px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 32px;
    flex-wrap: wrap;
}
.cp-item { display: flex; flex-direction: column; gap: 3px; }
.cp-label {
    font-size: 9px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--t3);
}
.cp-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px; font-weight: 600; color: var(--t1);
}
.cp-divider { width: 1px; height: 32px; background: var(--border2); }

/* ──────────────────────────────────────────────
   STAT CARDS
────────────────────────────────────────────── */
.stat-card {
    background: var(--bg3);
    border: 1px solid var(--border2);
    border-radius: 14px;
    padding: 20px 22px;
    position: relative; overflow: hidden;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    cursor: default;
}
.stat-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--glow);
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s;
}
.stat-card:hover::before { opacity: 1; }
.stat-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
.stat-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent-grad);
}
.stat-card.c-teal   {
    --accent-grad: linear-gradient(90deg, #2dd4bf 0%, transparent 70%);
    --glow: radial-gradient(ellipse at 0% 0%, rgba(45,212,191,0.06) 0%, transparent 60%);
    --shadow: 0 8px 24px rgba(45,212,191,0.12);
}
.stat-card.c-amber  {
    --accent-grad: linear-gradient(90deg, #fbbf24 0%, transparent 70%);
    --glow: radial-gradient(ellipse at 0% 0%, rgba(251,191,36,0.06) 0%, transparent 60%);
    --shadow: 0 8px 24px rgba(251,191,36,0.12);
}
.stat-card.c-purple {
    --accent-grad: linear-gradient(90deg, #a78bfa 0%, transparent 70%);
    --glow: radial-gradient(ellipse at 0% 0%, rgba(167,139,250,0.06) 0%, transparent 60%);
    --shadow: 0 8px 24px rgba(167,139,250,0.12);
}
.stat-card.c-green  {
    --accent-grad: linear-gradient(90deg, #34d399 0%, transparent 70%);
    --glow: radial-gradient(ellipse at 0% 0%, rgba(52,211,153,0.06) 0%, transparent 60%);
    --shadow: 0 8px 24px rgba(52,211,153,0.12);
}
.stat-card:hover.c-teal   { border-color: rgba(45,212,191,0.35); }
.stat-card:hover.c-amber  { border-color: rgba(251,191,36,0.35); }
.stat-card:hover.c-purple { border-color: rgba(167,139,250,0.35); }
.stat-card:hover.c-green  { border-color: rgba(52,211,153,0.35); }
.sc-icon {
    font-size: 18px;
    margin-bottom: 12px;
    opacity: 0.7;
}
.sc-label {
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--t3); margin-bottom: 6px;
}
.sc-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 26px; font-weight: 800;
    line-height: 1; letter-spacing: -0.04em;
    margin-bottom: 4px;
}
.sc-value.c-teal   { color: #2dd4bf; }
.sc-value.c-amber  { color: #fbbf24; }
.sc-value.c-purple { color: #a78bfa; }
.sc-value.c-green  { color: #34d399; }
.sc-sub { font-size: 11px; color: var(--t3); }

/* ──────────────────────────────────────────────
   PANEL
────────────────────────────────────────────── */
.panel {
    background: var(--bg3);
    border: 1px solid var(--border2);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 22px;
}
.panel-header {
    padding: 18px 22px;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
    background: linear-gradient(180deg, var(--bg4) 0%, var(--bg3) 100%);
}
.panel-title-wrap { display: flex; align-items: center; gap: 10px; }
.panel-title-icon { font-size: 14px; opacity: 0.6; }
.panel-title {
    font-size: 13px; font-weight: 700;
    color: var(--t1); letter-spacing: -0.02em;
}
.panel-badge {
    font-size: 10px; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    background: rgba(45,212,191,0.1);
    color: #2dd4bf;
    border: 1px solid rgba(45,212,191,0.25);
    padding: 3px 9px; border-radius: 100px;
    letter-spacing: 0.04em;
}
.panel-badge.amber {
    background: rgba(251,191,36,0.1);
    color: #fbbf24;
    border-color: rgba(251,191,36,0.25);
}

/* ──────────────────────────────────────────────
   TABLE
────────────────────────────────────────────── */
.table-wrap { overflow-x: auto; }
.styled-table {
    width: 100%; border-collapse: collapse;
    font-size: 13px; min-width: 560px;
}
.styled-table thead th {
    background: var(--bg4);
    color: var(--t3);
    font-size: 9px; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.1em;
    padding: 12px 18px;
    text-align: left;
    border-bottom: 1px solid var(--border2);
    white-space: nowrap;
}
.styled-table thead th.r { text-align: right; }
.styled-table tbody td {
    padding: 12px 18px;
    border-bottom: 1px solid var(--border);
    color: var(--t1);
    vertical-align: middle;
}
.styled-table tbody td.r { text-align: right; }
.styled-table tbody tr:last-child td { border-bottom: none; }
.styled-table tbody tr:hover td { background: rgba(255,255,255,0.02); }
.sym {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px; font-weight: 700;
    color: #2dd4bf !important;
    letter-spacing: 0.02em;
}
.num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px; color: var(--t1);
}
.num-muted {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; color: var(--t2);
}
.rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px;
    background: var(--bg4);
    border: 1px solid var(--border2);
    border-radius: 6px;
    font-size: 10px; font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    color: var(--t3);
}
.rank-badge.gold   { background: rgba(251,191,36,0.15); color: #fbbf24; border-color: rgba(251,191,36,0.3); }
.rank-badge.silver { background: rgba(139,148,158,0.15); color: #8b949e; border-color: rgba(139,148,158,0.3); }
.rank-badge.bronze { background: rgba(251,146,60,0.12); color: #fb923c; border-color: rgba(251,146,60,0.25); }
.pct-wrap {
    display: flex; align-items: center; gap: 10px;
}
.pct-bar-track {
    flex: 1; min-width: 50px; max-width: 80px; height: 4px;
    background: var(--bg1);
    border-radius: 100px; overflow: hidden;
}
.pct-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #2dd4bf, #0891b2);
    border-radius: 100px;
}
.pct-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; color: var(--t2);
    min-width: 46px; text-align: right;
}

/* ──────────────────────────────────────────────
   CHART PANELS
────────────────────────────────────────────── */
.chart-panel {
    background: var(--bg3);
    border: 1px solid var(--border2);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 22px;
    display: flex; flex-direction: column;
}
.chart-panel-header {
    padding: 18px 22px 0 22px;
    display: flex; align-items: flex-start; justify-content: space-between;
}
.chart-title {
    font-size: 13px; font-weight: 700;
    color: var(--t1); letter-spacing: -0.02em;
    margin-bottom: 2px;
}
.chart-sub {
    font-size: 11px; color: var(--t3);
}
.chart-body { padding: 4px 4px 8px 4px; }

/* ──────────────────────────────────────────────
   ERROR
────────────────────────────────────────────── */
.err-box {
    background: rgba(248,113,113,0.08);
    border: 1px solid rgba(248,113,113,0.3);
    color: #f87171;
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 20px;
    font-size: 13px;
    display: flex; gap: 10px; align-items: flex-start;
}

/* ──────────────────────────────────────────────
   FOOTER
────────────────────────────────────────────── */
.footer {
    border-top: 1px solid var(--border);
    background: var(--bg2);
    margin: 3rem -1.5rem -3rem -1.5rem;
    padding: 18px 32px;
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 8px;
}
.footer-l {
    font-size: 12px; color: var(--t3);
    font-family: 'JetBrains Mono', monospace;
}
.footer-l span { color: var(--teal); }
.footer-r { font-size: 12px; color: var(--t3); }

/* ──────────────────────────────────────────────
   STREAMLIT WIDGET OVERRIDES
────────────────────────────────────────────── */
.stFileUploader > div {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
.stFileUploader label { display: none !important; }
div[data-testid="stFileUploader"] section {
    background: rgba(13,17,23,0.6) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stFileUploader"] section:hover {
    border-color: rgba(45,212,191,0.5) !important;
    box-shadow: 0 0 0 3px rgba(45,212,191,0.08) !important;
}
div[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #2dd4bf, #0891b2) !important;
    color: #080c12 !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 12px rgba(45,212,191,0.3) !important;
    transition: all 0.15s !important;
}
div[data-testid="stFileUploader"] button:hover {
    box-shadow: 0 6px 20px rgba(45,212,191,0.45) !important;
}
div[data-testid="stFileUploader"] p,
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploader"] span {
    color: var(--t2) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}

/* Analyze button */
.stButton > button {
    background: linear-gradient(135deg, #2dd4bf 0%, #0891b2 100%) !important;
    color: #080c12 !important;
    border: none !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    padding: 13px 28px !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 16px rgba(45,212,191,0.3) !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 28px rgba(45,212,191,0.5) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 10px rgba(45,212,191,0.25) !important;
}

.stSpinner > div { border-top-color: #2dd4bf !important; }
div[data-testid="stAlert"] {
    background: rgba(248,113,113,0.08) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    color: #f87171 !important;
    border-radius: 12px !important;
}

/* column gap */
div[data-testid="column"] { padding: 0 8px !important; }
div[data-testid="column"]:first-child { padding-left: 0 !important; }
div[data-testid="column"]:last-child  { padding-right: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─── CONSTANTS ───────────────────────────────────────────────────────────────
PALETTE = [
    '#2dd4bf','#fbbf24','#a78bfa','#34d399','#f87171',
    '#60a5fa','#fb923c','#e879f9','#4ade80','#38bdf8',
    '#facc15','#c084fc','#86efac','#f472b6','#7dd3fc',
    '#fda4af','#67e8f9','#bbf7d0','#ddd6fe','#fed7aa',
]

BASE_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, system-ui, sans-serif', color='#8b949e', size=12),
    margin=dict(l=12, r=12, t=12, b=12),
    hoverlabel=dict(
        bgcolor='#1c2333',
        bordercolor='#30363d',
        font=dict(family='Inter', color='#e6edf3', size=12),
    ),
)

def hex_to_rgba(hex_color, alpha=0.85):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f'rgba({r},{g},{b},{alpha})'

def normalize_symbol(sym):
    s = str(sym).strip().upper()
    return re.sub(r'\.[A-Z]{1,3}$', '', s, flags=re.IGNORECASE).upper()


# ─── FILE PROCESSING ─────────────────────────────────────────────────────────
def extract_client_info(df_raw):
    client_id = name = None
    for _, row in df_raw.iterrows():
        row_text = " ".join([str(x) for x in row.values if pd.notna(x)])
        m = re.search(r'Account:\s*(\d{5,})', row_text)
        if m: client_id = m.group(1)
        nm = re.search(r'Name:\s*([A-Za-z][A-Za-z\s]{1,40})', row_text)
        if nm: name = nm.group(1).strip()
    return name, client_id

def process_file(file_bytes):
    try:
        stream1 = io.BytesIO(file_bytes)
        df_raw = pd.read_excel(stream1, header=None)
        name, client_id = extract_client_info(df_raw)

        header_row = None
        for i, row in df_raw.iterrows():
            row_str = row.astype(str).str.lower()
            if row_str.str.contains("symbol").any() and row_str.str.contains("volume").any():
                header_row = i; break

        if header_row is None:
            return None, None, None, "Positions table not found — ensure the file has 'Symbol' and 'Volume' columns."

        stream2 = io.BytesIO(file_bytes)
        df = pd.read_excel(stream2, header=header_row)
        df.columns = [str(c).strip().lower() for c in df.columns]

        missing = [c for c in ['symbol','volume','position'] if c not in df.columns]
        if missing:
            return None, None, None, f"Missing columns: {', '.join(missing)}"

        df['volume'] = pd.to_numeric(
            df['volume'].astype(str).str.replace(',','.', regex=False).str.strip(),
            errors='coerce'
        )
        df = df.dropna(subset=['symbol','volume','position'])
        df = df[~df['symbol'].astype(str).str.contains("balance|credit", case=False, na=False)]

        # Normalize symbols (strip broker suffix)
        df['symbol'] = df['symbol'].apply(normalize_symbol)

        grouped = df.groupby('symbol').agg(
            volume=('volume','sum'),
            trades=('position','nunique')
        )
        grouped['avg'] = grouped['volume'] / grouped['trades']
        grouped = grouped.round(2).sort_values('volume', ascending=False)

        total_volume = grouped['volume'].sum()
        total_trades = int(df['position'].nunique())

        table_rows = []
        for sym, row in grouped.iterrows():
            pct = round(float(row['volume'])/float(total_volume)*100, 2) if total_volume else 0
            table_rows.append({
                "symbol":  str(sym),
                "volume":  round(float(row['volume']), 2),
                "trades":  int(row['trades']),
                "avg":     round(float(row['avg']), 2),
                "percent": round(pct, 2),
            })

        meta = {
            "total_volume": round(float(total_volume), 2),
            "total_trades": total_trades,
            "top_symbol":   str(grouped.index[0]) if not grouped.empty else "-",
            "avg_trade":    round(float(total_volume)/total_trades, 2) if total_trades else 0,
            "name":         name,
            "client_id":    client_id,
            "symbols":      [str(s) for s in grouped.index],
            "volumes":      [float(v) for v in grouped['volume']],
            "trades_list":  [int(t) for t in grouped['trades']],
        }
        return table_rows, meta, df, None

    except Exception as e:
        return None, None, None, str(e)


# ─── EXPORTS ─────────────────────────────────────────────────────────────────
def make_csv(table_rows):
    lines = ["Symbol,Total Lots,Positions,Avg Lot,% Share"]
    for r in table_rows:
        lines.append(f"{r['symbol']},{r['volume']},{r['trades']},{r['avg']},{r['percent']}%")
    return "\n".join(lines).encode()

def make_excel(table_rows):
    df_out = pd.DataFrame([
        [r['symbol'], r['volume'], r['trades'], r['avg'], f"{r['percent']}%"]
        for r in table_rows
    ], columns=["Symbol","Total Lots","Positions","Avg Lot","% Share"])
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df_out.to_excel(writer, index=False, sheet_name="Volume Insight")
    return buf.getvalue()


# ─── TABLE HTML ──────────────────────────────────────────────────────────────
def render_table(table_rows):
    max_pct = max(r['percent'] for r in table_rows) if table_rows else 1
    rows_html = ""
    for i, r in enumerate(table_rows):
        bar_w = int(r['percent'] / max_pct * 100)
        if i == 0:   rank_cls = "gold"
        elif i == 1: rank_cls = "silver"
        elif i == 2: rank_cls = "bronze"
        else:        rank_cls = ""
        rows_html += f"""<tr>
            <td><span class="rank-badge {rank_cls}">{i+1}</span></td>
            <td class="sym">{r['symbol']}</td>
            <td class="num r">{r['volume']:,.2f}</td>
            <td class="num-muted r">{r['trades']}</td>
            <td class="num-muted r">{r['avg']:,.2f}</td>
            <td>
                <div class="pct-wrap">
                    <div class="pct-bar-track">
                        <div class="pct-bar-fill" style="width:{bar_w}%"></div>
                    </div>
                    <span class="pct-num">{r['percent']}%</span>
                </div>
            </td>
        </tr>"""
    return f"""<div class="table-wrap"><table class="styled-table">
        <thead><tr>
            <th style="width:36px">#</th>
            <th>Symbol</th>
            <th class="r">Total Lots</th>
            <th class="r">Positions</th>
            <th class="r">Avg Lot</th>
            <th style="min-width:160px">% Share</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table></div>"""


# ════════════════════════════════════════════════════════════
#  RENDER
# ════════════════════════════════════════════════════════════

# ── TOP NAV ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <a class="topbar-brand" href="#">
            <div class="topbar-logo">📈</div>
            TraderInsight
        </a>
        <div class="topbar-divider"></div>
        <div class="topbar-nav">
            <span class="topbar-nav-item active">Volume Analyzer</span>
            <span class="topbar-nav-item">History</span>
            <span class="topbar-nav-item">Settings</span>
        </div>
    </div>
    <div class="topbar-right">
        <div class="topbar-status"><div class="status-dot"></div>LIVE</div>
        <span class="topbar-badge">v2.1.0</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── UPLOAD ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="upload-zone">
    <div class="upload-icon">📂</div>
    <div class="upload-title">Drop your broker statement</div>
    <div class="upload-sub">
        MT4 / MT5 export files supported &nbsp;·&nbsp;
        Suffix variants auto-merged (XAUUSD.a + XAUUSD.d → XAUUSD)
    </div>
    <div class="upload-tags">
        <span class="upload-tag">XLSX</span>
        <span class="upload-tag">XLS</span>
        <span class="upload-tag">UP TO 200MB</span>
        <span class="upload-tag">MT4</span>
        <span class="upload-tag">MT5</span>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload broker statement",
    type=["xlsx", "xls"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    size_kb = round(uploaded_file.size / 1024, 1)
    size_str = f"{size_kb} KB" if size_kb < 1000 else f"{size_kb/1024:.1f} MB"
    st.markdown(f"""
    <div class="file-pill">
        <div class="fp-icon">📊</div>
        <div>
            <div class="fp-name">{uploaded_file.name}</div>
            <div class="fp-meta">{size_str} &nbsp;·&nbsp; Excel workbook</div>
        </div>
        <span class="fp-badge">READY</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚡  Analyze Statement"):
        file_bytes = uploaded_file.read()
        with st.spinner("Parsing broker statement…"):
            table_rows, meta, df_raw, err = process_file(file_bytes)
        if err:
            st.markdown(f'<div class="err-box">⚠️ <strong>Parse error:</strong> {err}</div>',
                        unsafe_allow_html=True)
        else:
            st.session_state['result'] = (table_rows, meta, file_bytes)


# ── RESULTS ───────────────────────────────────────────────────────────────────
if 'result' in st.session_state:
    table_rows, meta, file_bytes = st.session_state['result']

    # ── Client strip ──
    if meta.get('name') or meta.get('client_id'):
        parts = ""
        if meta.get('name'):
            parts += f'<div class="cp-item"><div class="cp-label">Trader</div><div class="cp-value">{meta["name"]}</div></div>'
        if meta.get('name') and meta.get('client_id'):
            parts += '<div class="cp-divider"></div>'
        if meta.get('client_id'):
            parts += f'<div class="cp-item"><div class="cp-label">Account</div><div class="cp-value">#{meta["client_id"]}</div></div>'
        parts += '<div class="cp-divider"></div>'
        parts += f'<div class="cp-item"><div class="cp-label">Symbols</div><div class="cp-value">{len(meta["symbols"])}</div></div>'
        parts += '<div class="cp-divider"></div>'
        parts += f'<div class="cp-item"><div class="cp-label">Total Lots</div><div class="cp-value">{meta["total_volume"]:,.2f}</div></div>'
        st.markdown(f'<div class="client-strip">{parts}</div>', unsafe_allow_html=True)

    # ── Stat cards ──
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "📊", "Total Volume",     f"{meta['total_volume']:,.2f}", "lots traded across all symbols",   "c-teal"),
        (c2, "🔢", "Positions",        f"{meta['total_trades']}",      "unique open/closed positions",      "c-amber"),
        (c3, "🏆", "Top Symbol",       meta['top_symbol'],             "highest volume instrument",         "c-purple"),
        (c4, "⚡", "Avg Lot / Trade",  f"{meta['avg_trade']:,.2f}",   "average lot size per position",     "c-green"),
    ]
    for col, icon, label, value, sub, color in cards:
        with col:
            st.markdown(f"""
            <div class="stat-card {color}">
                <div class="sc-icon">{icon}</div>
                <div class="sc-label">{label}</div>
                <div class="sc-value {color}">{value}</div>
                <div class="sc-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Table panel ──
    n_sym = len(table_rows)
    st.markdown(f"""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title-wrap">
                <span class="panel-title-icon">📋</span>
                <span class="panel-title">Volume Breakdown by Symbol</span>
            </div>
            <span class="panel-badge">{n_sym} instruments</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(render_table(table_rows), unsafe_allow_html=True)

    # ── Buttons (inside iframe so clipboard API works) ──
    csv_data   = make_csv(table_rows)
    excel_data = make_excel(table_rows)
    csv_b64    = base64.b64encode(csv_data).decode()
    excel_b64  = base64.b64encode(excel_data).decode()

    copy_lines = ["Symbol\tTotal Lots\tPositions\tAvg Lot\t% Share"]
    for r in table_rows:
        copy_lines.append(f"{r['symbol']}\t{r['volume']}\t{r['trades']}\t{r['avg']}\t{r['percent']}%")
    copy_text_js = (
        "\n".join(copy_lines)
        .replace('\\','\\\\').replace('`','\\`').replace('$','\\$').replace('\r','')
    )

    components.html(f"""<!DOCTYPE html><html><head>
    <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:transparent;font-family:'Inter',system-ui,sans-serif}}
    .row{{
        display:flex;gap:8px;flex-wrap:wrap;
        padding:14px 18px 16px;
        background:linear-gradient(180deg,transparent,rgba(0,0,0,0.08));
        border-top:1px solid #21262d;
    }}
    .btn{{
        display:inline-flex;align-items:center;gap:7px;
        padding:9px 18px;border-radius:9px;
        font-size:12px;font-weight:700;cursor:pointer;
        text-decoration:none;transition:all 0.18s;
        border:1.5px solid transparent;
        font-family:'Inter',system-ui,sans-serif;
        line-height:1;letter-spacing:0.01em;
        white-space:nowrap;
    }}
    .btn-copy{{
        background:#1c2333;color:#c9d1d9;border-color:#30363d;
    }}
    .btn-copy:hover{{
        background:rgba(45,212,191,0.1);border-color:#2dd4bf;color:#2dd4bf;
        box-shadow:0 0 16px rgba(45,212,191,0.15);
    }}
    .btn-copy.done{{
        background:rgba(52,211,153,0.12);border-color:rgba(52,211,153,0.4);
        color:#34d399;
    }}
    .btn-csv{{
        background:#1c2333;color:#c9d1d9;border-color:#30363d;
    }}
    .btn-csv:hover{{
        background:rgba(96,165,250,0.1);border-color:#60a5fa;color:#60a5fa;
        box-shadow:0 0 16px rgba(96,165,250,0.12);
    }}
    .btn-xl{{
        background:rgba(251,191,36,0.08);color:#fbbf24;
        border-color:rgba(251,191,36,0.25);
    }}
    .btn-xl:hover{{
        background:rgba(251,191,36,0.15);border-color:#fbbf24;
        box-shadow:0 0 16px rgba(251,191,36,0.15);
    }}
    .toast{{
        display:none;align-items:center;gap:6px;
        font-size:12px;font-weight:600;color:#34d399;
        padding:9px 14px;
        background:rgba(52,211,153,0.1);
        border:1.5px solid rgba(52,211,153,0.3);
        border-radius:9px;
    }}
    </style></head><body>
    <div class="row">
        <button class="btn btn-copy" id="cb" onclick="doCopy()">📋 Copy Table</button>
        <a class="btn btn-csv"
           href="data:text/csv;base64,{csv_b64}"
           download="trading_data.csv">⬇ Download CSV</a>
        <a class="btn btn-xl"
           href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_b64}"
           download="volume_insight.xlsx">📊 Download Excel</a>
        <span class="toast" id="toast">✓ Copied to clipboard</span>
    </div>
    <script>
    function doCopy(){{
        var text=`{copy_text_js}`;
        var btn=document.getElementById('cb');
        function ok(){{
            btn.textContent='✓ Copied!';btn.classList.add('done');
            var t=document.getElementById('toast');t.style.display='inline-flex';
            setTimeout(function(){{btn.textContent='📋 Copy Table';btn.classList.remove('done');t.style.display='none';}},2500);
        }}
        if(navigator.clipboard&&window.isSecureContext){{
            navigator.clipboard.writeText(text).then(ok).catch(function(){{fb(text,ok);}});
        }}else{{fb(text,ok);}}
    }}
    function fb(text,cb){{
        var ta=document.createElement('textarea');
        ta.value=text;ta.style.cssText='position:fixed;top:-999px;opacity:0;';
        document.body.appendChild(ta);ta.focus();ta.select();
        try{{if(document.execCommand('copy'))cb();}}catch(e){{}}
        document.body.removeChild(ta);
    }}
    </script></body></html>""", height=60)

    st.markdown("</div>", unsafe_allow_html=True)  # close .panel

    # ── CHARTS ───────────────────────────────────────────────────────────────
    labels  = meta['symbols']
    volumes = meta['volumes']
    trades  = meta['trades_list']
    n       = len(labels)
    colors  = [PALETTE[i % len(PALETTE)] for i in range(n)]
    bar_colors  = [hex_to_rgba(c, 0.78) for c in colors]
    pie_colors  = [hex_to_rgba(c, 0.88) for c in colors]

    col_bar, col_pie = st.columns([1, 1], gap="large")

    # ── Bar chart ──────────────────────────────────────────────────────────
    with col_bar:
        st.markdown("""
        <div class="chart-panel">
            <div class="chart-panel-header">
                <div>
                    <div class="chart-title">Lot Volume by Symbol</div>
                    <div class="chart-sub">Total lots traded per instrument</div>
                </div>
                <span class="panel-badge">bar</span>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)

        bar_fig = go.Figure()
        bar_fig.add_trace(go.Bar(
            x=labels, y=volumes,
            marker=dict(
                color=bar_colors,
                line=dict(color=colors, width=1.5),
                cornerradius=4,
            ),
            hovertemplate='<b>%{x}</b><br>%{y:,.2f} lots<extra></extra>',
        ))
        bar_layout = {
            **BASE_LAYOUT,
            'height': 320,
            'margin': dict(l=12, r=12, t=8, b=8),
            'bargap': 0.28,
            'showlegend': False,
            'xaxis': dict(
                gridcolor='#1c2333',
                tickfont=dict(size=10, color='#8b949e'),
                linecolor='#21262d',
                tickangle=-35 if n > 7 else 0,
                showgrid=False,
            ),
            'yaxis': dict(
                gridcolor='#1c2333',
                tickfont=dict(size=10, color='#8b949e'),
                linecolor='#21262d',
                showgrid=True,
                zeroline=False,
            ),
        }
        bar_fig.update_layout(**bar_layout)
        st.plotly_chart(bar_fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Donut chart ─────────────────────────────────────────────────────────
    with col_pie:
        st.markdown("""
        <div class="chart-panel">
            <div class="chart-panel-header">
                <div>
                    <div class="chart-title">Volume Distribution</div>
                    <div class="chart-sub">% share of total lots per symbol</div>
                </div>
                <span class="panel-badge">donut</span>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)

        # For the donut: show only top symbols in legend, use a wider figure
        pie_fig = go.Figure()
        pie_fig.add_trace(go.Pie(
            labels=labels,
            values=volumes,
            hole=0.60,
            marker=dict(
                colors=pie_colors,
                line=dict(color='#080c12', width=2.5),
            ),
            textinfo='percent',
            textposition='outside',
            textfont=dict(size=10, color='#8b949e', family='JetBrains Mono'),
            hovertemplate='<b>%{label}</b><br>%{value:,.2f} lots<br>%{percent:.1%}<extra></extra>',
            sort=True,
            direction='clockwise',
            pull=[0.03 if i == 0 else 0 for i in range(n)],
            automargin=True,
        ))
        pie_layout = {
            **BASE_LAYOUT,
            'height': 320,
            'margin': dict(l=20, r=20, t=8, b=8),
            'showlegend': True,
            'legend': dict(
                font=dict(size=10, color='#8b949e', family='Inter'),
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(0,0,0,0)',
                orientation='v',
                x=1.02, y=0.5,
                xanchor='left', yanchor='middle',
                itemwidth=30,
                traceorder='normal',
            ),
        }
        pie_fig.update_layout(**pie_layout)
        st.plotly_chart(pie_fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Scatter (only when data is varied enough) ───────────────────────────
    if len(labels) > 1:
        st.markdown("""
        <div class="chart-panel">
            <div class="chart-panel-header">
                <div>
                    <div class="chart-title">Trades vs Volume — Positioning Map</div>
                    <div class="chart-sub">Bubble size = relative volume · Hover for details</div>
                </div>
                <span class="panel-badge amber">bubble</span>
            </div>
            <div class="chart-body">
        """, unsafe_allow_html=True)

        max_v = max(volumes) or 1
        bubble_sizes = [max(12, min(52, v / max_v * 52)) for v in volumes]

        sc_fig = go.Figure()
        sc_fig.add_trace(go.Scatter(
            x=trades, y=volumes,
            mode='markers+text',
            text=labels,
            textposition='top center',
            textfont=dict(size=9, color='#8b949e', family='JetBrains Mono'),
            marker=dict(
                size=bubble_sizes,
                color=bar_colors,
                line=dict(color=colors, width=1.5),
                opacity=0.85,
                sizemode='diameter',
            ),
            hovertemplate='<b>%{text}</b><br>Trades: %{x}<br>Volume: %{y:,.2f} lots<extra></extra>',
        ))
        sc_layout = {
            **BASE_LAYOUT,
            'height': 340,
            'margin': dict(l=50, r=20, t=12, b=50),
            'showlegend': False,
            'xaxis': dict(
                title=dict(text='Number of Trades', font=dict(size=11, color='#484f58')),
                gridcolor='#1c2333',
                tickfont=dict(size=10, color='#8b949e'),
                linecolor='#21262d',
                zeroline=False,
            ),
            'yaxis': dict(
                title=dict(text='Total Volume (Lots)', font=dict(size=11, color='#484f58')),
                gridcolor='#1c2333',
                tickfont=dict(size=10, color='#8b949e'),
                linecolor='#21262d',
                zeroline=False,
            ),
        }
        sc_fig.update_layout(**sc_layout)
        st.plotly_chart(sc_fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div></div>", unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-l">TraderInsight &nbsp;·&nbsp; <span>v2.1.0</span></div>
    <div class="footer-r">MT4 / MT5 analyzer &nbsp;·&nbsp; Symbol suffix auto-merge enabled</div>
</div>
""", unsafe_allow_html=True)
