# pages/3_Comparateur.py — Comparateur (rendements cumulés vs ^GSPTSE + menu custom + logo)

import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# =========================
# 1) Config Streamlit (doit être 1ère commande)
# =========================
st.set_page_config(page_title="Comparateur", page_icon="🆚", layout="wide")
# Masquer le menu par défaut de Streamlit
st.markdown("""
<style>
/* Cache le menu multipage natif */
section[data-testid="stSidebar"] nav[aria-label="Pages"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] nav { display: none !important; }
</style>
""", unsafe_allow_html=True)


# =========================
# 2) Sidebar custom + logo + liens
# =========================
with st.sidebar:
    st.image("assets/logo.png", use_column_width=True)
    st.markdown("---")
    st.page_link("app.py",                  label="Accueil",       icon="🏠")
    st.page_link("pages/1_Screener.py",     label="Screener",      icon="🔍")
    st.page_link("pages/2_Fiche_Valeur.py", label="Actions TSX",   icon="📈")
    st.page_link("pages/3_Comparateur.py",  label="Comparateur",   icon="🆚")
    st.page_link("pages/4_News.py",         label="Actualités",    icon="📰")
    st.markdown("---")

# =========================
# 3) Utilitaires
# =========================
def _normalize_tsx(t: str) -> str:
    """Renvoie un ticker normalisé: ajoute .TO si nécessaire (sauf indice commençant par ^)."""
    if not t:
        return t
    t = t.strip().upper()
    if t.startswith("^"):
        return t
    return t if t.endswith(".TO") else f"{t}.TO"

@st.cache_data(ttl=3600, show_spinner=False)
def load_prices(tickers: list[str], period: str, interval: str = "1d") -> pd.DataFrame:
    """Télécharge les prix ajustés (yfinance). Retourne un DataFrame avec colonnes = tickers."""
    # yfinance gère mieux un seul appel groupé
    tickers = list(dict.fromkeys([t for t in tickers if t]))  # unique + garde l'ordre
    if not tickers:
        return pd.DataFrame()
    df = yf.download(
        tickers=" ".join(tickers),
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
        threads=True,
        group_by="ticker",
    )
    # Normaliser en tableau simple colonnes=tickers (cas 1 ou n tickers)
    if len(tickers) == 1:
        out = df["Close"].to_frame(tickers[0])
    else:
        out = pd.concat({t: df[t]["Close"] for t in tickers if t in df.columns.levels[0]}, axis=1)
    out = out.sort_index().ffill().dropna(how="all")
    return out

def to_cumulative_base100(df: pd.DataFrame) -> pd.DataFrame:
    """Transforme les prix en rendement cumulé base 100 (première date = 100)."""
    df = df.dropna(how="all")
    if df.empty:
        return df
    return df / df.iloc[0] * 100.0

def to_cumulative_pct(df: pd.DataFrame) -> pd.DataFrame:
    """Transforme les prix en rendement cumulé en % (première date = 0%)."""
    df = df.dropna(how="all")
    if df.empty:
        return df
    return (df / df.iloc[0] - 1.0) * 100.0

def melt_for_plot(df: pd.DataFrame, value_name: str) -> pd.DataFrame:
    df = df.copy()
    df.index.name = "Date"
    return df.reset_index().melt(id_vars="Date", var_name="Ticker", value_name=value_name)

# =========================
# 4) UI
# =========================
st.title("🆚 Comparateur de titres")

tickers_raw = st.text_input(
    "Entrez jusqu'à 5 tickers séparés par des virgules (ex. RY.TO, ENB.TO, SHOP.TO)",
    value="RY.TO, ENB.TO, SHOP.TO",
)
tickers = [ _normalize_tsx(t) for t in tickers_raw.split(",") if t.strip() ]

col_opt1, col_opt2, col_opt3 = st.columns([1, 1, 1])
with col_opt1:
    # Périodes courantes yfinance
    periode = st.selectbox("Période", ["YTD", "1 an", "3 ans", "5 ans", "10 ans", "Max"], index=5)
with col_opt2:
    incl_bench = st.checkbox("Comparer à l'indice ^GSPTSE", value=True)
with col_opt3:
    mode = st.radio("Normalisation", ["Base 100", "En % (base 0)"], horizontal=True)

period_map = {
    "YTD": "ytd",   # géré plus bas (on tronque au 1er janv.)
    "1 an": "1y",
    "3 ans": "3y",
    "5 ans": "5y",
    "10 ans": "10y",
    "Max": "max",
}

if incl_bench and "^GSPTSE" not in tickers:
    tickers = tickers + ["^GSPTSE"]

# =========================
# 5) Données & graphiques
# =========================
if len(tickers) == 0:
    st.info("Ajoute au moins un ticker TSX (ex. **RY.TO**) pour lancer la comparaison.")
    st.stop()

# Charge les prix
period_for_dl = "1y" if periode == "YTD" else period_map[periode]
prices = load_prices(tickers, period_for_dl, interval="1d")

# YTD = on tronque au 1er janvier de l'année courante
if periode == "YTD" and not prices.empty:
    start = pd.Timestamp(pd.Timestamp.today().year, 1, 1)
    prices = prices.loc[prices.index >= start]

if prices.empty or prices.shape[1] == 0:
    st.warning("Impossible de charger les prix. Vérifie les tickers saisis.")
    st.stop()

# Choix de la normalisation
if mode == "Base 100":
    series = to_cumulative_base100(prices)
    y_label = "Rendement normalisé (base 100)"
else:
    series = to_cumulative_pct(prices)
    y_label = "Rendement cumulé (%)"

# Line chart interactif
data_long = melt_for_plot(series, y_label)
titre = f"Comparaison des rendements — {periode}"
fig = px.line(data_long, x="Date", y=y_label, color="Ticker", title=titre)
if mode != "Base 100":
    fig.update_yaxes(ticksuffix=" %")
st.plotly_chart(fig, use_container_width=True)

# =========================
# 6) Petit tableau récap (dernier point)
# =========================
with st.expander("Détails (dernier point de la série)"):
    last_row = series.dropna(how="all").iloc[-1].to_frame("Dernier point").sort_index()
    st.dataframe(last_row, use_container_width=True)
