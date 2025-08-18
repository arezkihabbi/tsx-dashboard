# pages/1_Screener.py — Screener TSX (menu custom + logo en haut)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1) Config : doit être la 1ère commande Streamlit
st.set_page_config(page_title="Screener", page_icon="🔎", layout="wide")

# 2) Cacher la navigation multipage native
st.markdown("""
<style>
section[data-testid="stSidebar"] nav[aria-label="Pages"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] div[role="navigation"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# 3) Sidebar personnalisée : logo en HAUT puis liens
with st.sidebar:
    st.image("assets/logo.png", use_column_width=True)
    st.markdown("---")
    st.page_link("app.py",                  label="Acceuil",           icon="🏠")
    st.page_link("pages/1_Screener.py",     label="Screener",      icon="🔎")
    st.page_link("pages/2_Fiche_Valeur.py", label="Action du tsx",  icon="📄")
    st.page_link("pages/3_Comparateur.py",  label="Comparateur",   icon="🆚")
    st.page_link("pages/4_News.py",         label="News",          icon="📰")
    st.markdown("---")

# -------------------------------------------------------------------
# Contenu : screener
# -------------------------------------------------------------------
from core import data_source as ds

st.title("🔎 Screener TSX")

# --- Chargement de l’univers TSX
univ = ds.get_tsx_universe(limit=230)  # composite complet si possible
if univ.empty or "symbol" not in univ.columns:
    st.warning("Univers TSX indisponible pour le moment.")
    st.stop()

# Colonnes attendues : symbol, longName, sector, industry (certaines peuvent manquer)
univ = univ.copy()
for c in ["longName", "sector", "industry"]:
    if c not in univ.columns:
        univ[c] = None

# --- Filtres
c1, c2, c3 = st.columns([2,2,2])
with c1:
    sectors = sorted([s for s in univ["sector"].dropna().unique()])
    sel_sectors = st.multiselect("Secteurs", sectors, default=sectors[:min(6, len(sectors))])
with c2:
    search = st.text_input("Recherche (ticker / nom contient)", "")
with c3:
    max_tickers = st.slider("Nombre max de titres à charger", 20, 200, 120, step=10)

# Appliquer filtres basiques (sans prix)
df = univ.copy()
if sel_sectors:
    df = df[df["sector"].isin(sel_sectors)]
if search:
    s = search.lower()
    df = df[df["symbol"].str.lower().str.contains(s) | df["longName"].fillna("").str.lower().str.contains(s)]

if df.empty:
    st.info("Aucun titre ne correspond aux filtres.")
    st.stop()

# Limiter le nombre pour éviter des chargements trop lourds
df = df.head(max_tickers)
tickers = df["symbol"].tolist()

# --- Prix & rendements
with st.spinner("Chargement des prix Yahoo…"):
    prices = ds.get_prices(tickers, period="max", interval="1d")  # max pour YTD robuste; on tronque ensuite
if prices.empty:
    st.warning("Impossible de récupérer les prix pour ces tickers.")
    st.stop()

prices = prices.sort_index().ffill()

def ytd_return(series: pd.Series) -> float | None:
    if series.empty:
        return None
    start_year = pd.Timestamp(datetime(datetime.now().year, 1, 1))
    s = series[series.index >= start_year].dropna()
    if len(s) < 2:
        return None
    return float(s.iloc[-1] / s.iloc[0] - 1.0)

def pct_window(series: pd.Series, n: int) -> float | None:
    s = series.dropna()
    if len(s) <= n:
        return None
    return float(s.iloc[-1] / s.iloc[-n-1] - 1.0)

# Fenêtre 1 an pour les rendements “1Y”, et le reste par pas de jours
RET_1D = 1
RET_1W = 5
RET_1M = 21
RET_3M = 63
RET_6M = 126
RET_1Y = 252

rows = []
for t in prices.columns:
    s = prices[t]
    rows.append({
        "Ticker": t,
        "Nom": df.loc[df["symbol"] == t, "longName"].values[0] if (df["symbol"] == t).any() else None,
        "Secteur": df.loc[df["symbol"] == t, "sector"].values[0] if (df["symbol"] == t).any() else None,
        "% 1j":   pct_window(s, RET_1D),
        "% 1 sem": pct_window(s, RET_1W),
        "% 1 mois": pct_window(s, RET_1M),
        "% 3 mois": pct_window(s, RET_3M),
        "% 6 mois": pct_window(s, RET_6M),
        "% 1 an":  pct_window(s, RET_1Y),
        "% YTD":  ytd_return(s),
        "Dernier prix": float(s.dropna().iloc[-1]) if not s.dropna().empty else None,
    })

res = pd.DataFrame(rows)

# Mise en forme %
for col in ["% 1j","% 1 sem","% 1 mois","% 3 mois","% 6 mois","% 1 an","% YTD"]:
    res[col] = (pd.to_numeric(res[col], errors="coerce") * 100).round(2)

# Tri & options d’affichage
cA, cB, cC = st.columns([2,2,2])
with cA:
    sort_col = st.selectbox("Trier par", ["% 1 an","% YTD","% 6 mois","% 3 mois","% 1 mois","% 1 sem","% 1j","Ticker"])
with cB:
    ascending = st.checkbox("Tri ascendant", value=False)
with cC:
    show_rows = st.slider("Lignes visibles", 10, min(200, len(res)), min(50, len(res)))

res_sorted = res.sort_values(sort_col, ascending=ascending).head(show_rows)

st.dataframe(res_sorted, use_container_width=True, hide_index=True)

# Export CSV
csv = res.to_csv(index=False).encode("utf-8")
st.download_button("Exporter tout le screener (CSV)", data=csv, file_name="tsx_screener.csv", mime="text/csv")
