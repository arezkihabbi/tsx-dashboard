# app.py — Accueil / Tableau de bord (menu custom + logo en haut)
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo   # <-- pour les % identiques à Yahoo (fuseau Toronto)

# 1) Config Streamlit
st.set_page_config(page_title="UQAR • TSX Dashboard", page_icon="📈", layout="wide")

# 2) Styles (cache la nav native + look des cartes)
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] nav[aria-label="Pages"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    section[data-testid="stSidebar"] div[role="navigation"] { display: none !important; }

    .chip-row{display:flex;gap:8px;margin-top:12px}
    .chip{font-size:12px;padding:6px 10px;border-radius:999px;border:1px solid rgba(148,163,184,.25);background:rgba(14,18,24,.25);color:#d1d7e0}
    .chip.neg{background:rgba(239,68,68,.12);border-color:#ef4444;color:#ffb3b3}
    .chip.pos{background:rgba(34,197,94,.12);border-color:#22c55e;color:#b5f3c8}

    .idx-card{
      position:relative;border-radius:18px;padding:18px 18px 20px 18px;
      background: linear-gradient(135deg, rgba(34,41,59,.55), rgba(15,23,42,.55));
      border:1px solid rgba(148,163,184,.18);height:150px;
    }
    .idx-title{font-size:13px;letter-spacing:.2px;opacity:.7;margin-bottom:6px}
    .idx-last{font-size:36px;font-weight:700;letter-spacing:.5px;margin-top:10px}
    .idx-badges{position:absolute;left:18px;bottom:16px}
    </style>
    """,
    unsafe_allow_html=True,
)

# 3) Sidebar personnalisée
with st.sidebar:
    st.image("logo.png", use_column_width=True)
    st.page_link("app.py",                  label="Accueil",       icon="🏠")
    st.page_link("pages/1_Screener.py",     label="Screener",      icon="🔎")
    st.page_link("pages/2_Fiche_Valeur.py", label="Action du tsx", icon="📰")
    st.page_link("pages/3_Comparateur.py",  label="Comparateur",   icon="🆚")
    st.page_link("pages/4_News.py",         label="News",          icon="📰")
    st.markdown("---")

# ========= Chargement CSV TSX60 (liste externe) =========
@st.cache_data(ttl=1800, show_spinner=False)
def load_tsx60_universe_csv(path: str | Path = "data/tsx60_universe.csv") -> pd.DataFrame | None:
    p = Path(path)
    if not p.exists():
        return None
    try:
        # Encodage tolérant au BOM + auto-détection séparateur
        df = pd.read_csv(p, encoding="utf-8-sig", sep=None, engine="python")
        # Normaliser noms colonnes
        norm = {c: c.strip().lower().replace(" ", "") for c in df.columns}
        df.rename(columns=norm, inplace=True)
        if "secteur" in df.columns and "sector" not in df.columns:
            df.rename(columns={"secteur": "sector"}, inplace=True)
        if not {"ticker", "sector"}.issubset(df.columns):
            return None
        # Nettoyage
        df["ticker"] = df["ticker"].astype(str).str.strip().str.upper()
        df["sector"] = df["sector"].astype(str).str.strip()
        if "name" in df.columns:
            df["name"] = df["name"].astype(str).str.strip()
        # Sécurité : ne garder que .TO
        df = df[df["ticker"].str.endswith(".TO", na=False)]
        df = df.drop_duplicates(subset=["ticker"]).reset_index(drop=True)
        return df
    except Exception:
        return None

# ========= Helpers Yahoo pour les indices / macro =========
@st.cache_data(ttl=60, show_spinner=False)
def get_index_snapshot(ticker: str) -> dict | None:
    try:
        hist = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=False)
        if hist is None or hist.empty: return None
        close = hist["Close"].dropna()
        last = float(close.iloc[-1])
        d1 = None
        if close.size >= 2:
            prev = float(close.iloc[-2])
            if prev > 0: d1 = (last / prev - 1.0) * 100.0
        jan1 = pd.Timestamp(datetime.today().year, 1, 1, tz=close.index.tz)
        ytd_slice = close[close.index >= jan1]
        ytd = None
        if not ytd_slice.empty:
            base = float(ytd_slice.iloc[0])
            if base > 0: ytd = (last / base - 1.0) * 100.0
        return {"last": last, "d1": d1, "ytd": ytd}
    except Exception:
        return None

def fmt_pct(x: float | None) -> tuple[str, str]:
    if x is None or not np.isfinite(x): return "—", ""
    s = f"{x:.2f}%".replace(".", ",")
    css = "pos" if x >= 0 else "neg"
    return s, css

def render_index_card(title: str, ticker: str, data: dict | None):
    with st.container(border=False):
        if not data:
            st.info("Indice indisponible pour l’instant.")
            return
        last = data.get("last"); d1 = data.get("d1"); ytd = data.get("ytd")
        d1_txt, d1_cls = fmt_pct(d1); ytd_txt, ytd_cls = fmt_pct(ytd)
        last_fmt = f"{last:,.0f}".replace(",", " ")
        st.markdown(
            f"""
            <div class="idx-card">
              <div class="idx-title">{title} <span style="opacity:.6">({ticker})</span></div>
              <div class="idx-last">{last_fmt}</div>
              <div class="idx-badges chip-row">
                 <span class="chip {d1_cls}">1 j&nbsp;{d1_txt}</span>
                 <span class="chip {ytd_cls}">YTD&nbsp;{ytd_txt}</span>
              </div>
            </div>
            """, unsafe_allow_html=True,
        )

# ========= Fonctions macro mini‑cartes =========
@st.cache_data(ttl=120, show_spinner=False)
def macro_pair_last_and_returns(ticker: str) -> tuple[float|None,float|None,float|None]:
    try:
        hist = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True, progress=False)
        if hist is None or hist.empty: return None, None, None
        c = hist["Close"].dropna()
        last = float(c.iloc[-1])
        d1 = (last / float(c.iloc[-2]) - 1.0) * 100.0 if len(c) >= 2 else None
        jan1 = pd.Timestamp(datetime.today().year, 1, 1, tz=c.index.tz)
        ytd_slice = c[c.index >= jan1]
        ytd = (last / float(ytd_slice.iloc[0]) - 1.0) * 100.0 if not ytd_slice.empty else None
        return last, d1, ytd
    except Exception:
        return None, None, None

def small_metric_card(title: str, tk: str):
    last, d1, ytd = macro_pair_last_and_returns(tk)
    d1_txt, d1_cls = fmt_pct(d1)
    ytd_txt, ytd_cls = fmt_pct(ytd)
    if last is None:
        st.info(f"{title} indisponible.")
        return
    st.markdown(
        f"""
        <div class="idx-card" style="height:120px">
          <div class="idx-title">{title} <span style="opacity:.6">({tk})</span></div>
          <div class="idx-last" style="font-size:28px">{last:.4f}</div>
          <div class="idx-badges chip-row">
            <span class="chip {d1_cls}">1 j {d1_txt}</span>
            <span class="chip {ytd_cls}">YTD {ytd_txt}</span>
          </div>
        </div>
        """, unsafe_allow_html=True
    )

# ========= Contenu =========
st.title("Tableau de bord — Marché TSX")

# Barre de recherche → ouvre la fiche valeur
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        q = st.text_input("Rechercher une fiche valeur (ex. RY.TO, SHOP.TO)", "")
    with col2:
        if st.button("Ouvrir la fiche valeur"):
            if q:
                try:
                    st.query_params["ticker"] = q.strip().upper()
                except Exception:
                    pass
                st.switch_page("pages/2_Fiche_Valeur.py")

st.divider()

# ========== Section indices ==========
st.subheader("📊 Indices boursiers")
c1, c2, c3 = st.columns(3, gap="large")
with c1:
    render_index_card("Composite S&P/TSX", "^GSPTSE", get_index_snapshot("^GSPTSE"))
with c2:
    render_index_card("S&P/TSX 60", "TX60.TS", get_index_snapshot("TX60.TS"))
with c3:
    render_index_card("S&P 500", "^GSPC", get_index_snapshot("^GSPC"))

st.divider()

# ========== Indicateurs macro ==========
# ====== Indicateurs macro — correctif de mise en page (affichage uniquement) ======
st.subheader("📉 Indicateurs macro")

# 1) CSS d'ajustement, appliqué uniquement à un wrapper .macro
st.markdown(
    """
    <style>
      /* Limiter la hauteur et éviter les remontées de badges */
      .macro .idx-card{height:140px; overflow:hidden;}
      /* Prix un peu plus petit pour éviter le chevauchement */
      .macro .idx-last{font-size:28px; font-weight:800; line-height:1.05; margin:4px 0 8px;}
      /* Les badges ne sont plus positionnés en absolu -> suivent le flux */
      .macro .idx-badges{position:static; margin-top:4px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# 2) Rendu : on réutilise **tes** fonctions existantes (ne rien changer côté data)
#    Le wrapper .macro assure que le CSS ne s'applique qu'ici.
mc1, mc2, mc3, mc4 = st.columns(4, gap="large")
with mc1:
    st.markdown('<div class="macro">', unsafe_allow_html=True)
    small_metric_card("CAD / USD", "CADUSD=X")
    st.markdown('</div>', unsafe_allow_html=True)

with mc2:
    st.markdown('<div class="macro">', unsafe_allow_html=True)
    small_metric_card("CAD / EUR", "CADEUR=X")
    st.markdown('</div>', unsafe_allow_html=True)

with mc3:
    st.markdown('<div class="macro">', unsafe_allow_html=True)
    small_metric_card("Pétrole WTI", "CL=F")
    st.markdown('</div>', unsafe_allow_html=True)

with mc4:
    st.markdown('<div class="macro">', unsafe_allow_html=True)
    small_metric_card("Or (Gold)", "GC=F")
    st.markdown('</div>', unsafe_allow_html=True)
# ===================================================================================
