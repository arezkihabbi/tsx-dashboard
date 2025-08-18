# core/data_source.py — version SANS fallback local
from __future__ import annotations
import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st

# ------------------------------------------------------------------
# Constantes / cache
# ------------------------------------------------------------------
WIKI_TSX_COMPOSITE = "https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index"

TTL_PRICE_S = 6 * 3600      # prix: 6h
TTL_FUND_S  = 24 * 3600     # fondamentaux: 24h
TTL_META_S  = 24 * 3600     # métadonnées (secteur, etc.)

# ------------------------------------------------------------------
# Utils
# ------------------------------------------------------------------
def _normalize_ticker(t: str) -> str:
    t = t.strip().upper()
    if not t.endswith(".TO") and t not in ["^GSPTSE", "^GSPC", "^GSPTSX"]:
        t = t + ".TO"
    return t

# ------------------------------------------------------------------
# Univers TSX (depuis Wikipedia UNIQUEMENT)
# ------------------------------------------------------------------
@st.cache_data(ttl=TTL_META_S, show_spinner=False)
def get_tsx_universe(limit: int | None = 230) -> pd.DataFrame:
    """
    Récupère la liste des constituants du S&P/TSX Composite depuis Wikipedia.
    AUCUN fallback local : si échec, retourne un DF vide (colonnes standard).
    """
    cols = ["symbol", "name", "sector", "industry"]
    try:
        tables = pd.read_html(WIKI_TSX_COMPOSITE)
        df = None
        for t in tables:
            c = [str(c).lower() for c in t.columns]
            if any("symbol" in x or "ticker" in x for x in c):
                df = t.copy()
                break
        if df is None:
            return pd.DataFrame(columns=cols)

        # Normalisation des colonnes
        rename_map = {}
        for c in df.columns:
            lc = str(c).lower()
            if "symbol" in lc or "ticker" in lc:
                rename_map[c] = "symbol"
            elif "company" in lc or "name" in lc:
                rename_map[c] = "name"
            elif "sector" in lc:
                rename_map[c] = "sector"
            elif "industry" in lc or "sub" in lc:
                rename_map[c] = "industry"
        df = df.rename(columns=rename_map)

        if "symbol" not in df.columns:
            return pd.DataFrame(columns=cols)

        df["symbol"] = df["symbol"].astype(str).str.strip()
        df["symbol"] = df["symbol"].apply(
            lambda s: s if s.endswith(".TO") or s.startswith("^") else s + ".TO"
        )
        for c in ["name", "sector", "industry"]:
            if c not in df.columns:
                df[c] = np.nan
        df = (
            df[cols]
            .dropna(subset=["symbol"])
            .drop_duplicates(subset=["symbol"])
            .reset_index(drop=True)
        )
        if limit:
            df = df.head(limit)
        return df

    except Exception:
        # Aucun fallback : renvoyer DF vide avec schéma correct
        return pd.DataFrame(columns=cols)

# ------------------------------------------------------------------
# Prix
# ------------------------------------------------------------------
@st.cache_data(ttl=TTL_PRICE_S, show_spinner=False)
def get_prices(tickers: list[str], period: str = "max", interval: str = "1d") -> pd.DataFrame:
    """
    Télécharge les prix ajustés (auto_adjust=True) pour une liste de tickers.
    Retourne un DataFrame: index=dates, colonnes=tickers (Close ajusté).
    """
    if not tickers:
        return pd.DataFrame()
    tickers = list(dict.fromkeys([_normalize_ticker(t) for t in tickers]))
    data = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        auto_adjust=True,
        group_by="ticker",
        threads=True,
        progress=False,
    )
    if isinstance(data.columns, pd.MultiIndex):
        close = {}
        for t in tickers:
            if (t, "Close") in data.columns:
                close[t] = data[(t, "Close")]
            elif "Close" in data.columns:
                close[t] = data["Close"]
        df = pd.DataFrame(close)
    else:
        # cas 1 seul ticker
        try:
            df = data["Close"].to_frame(name=tickers[0])
        except Exception:
            df = pd.DataFrame()
    return df.dropna(how="all")

@st.cache_data(ttl=TTL_PRICE_S, show_spinner=False)
def get_index_block() -> dict:
    """Infos rapides sur l’indice S&P/TSX (^GSPTSE) : last, %1D, %YTD."""
    idx = "^GSPTSE"
    px = get_prices([idx], period="ytd", interval="1d")
    last = float(px[idx].dropna().iloc[-1]) if not px.empty and idx in px.columns else np.nan
    p1 = px[idx].dropna() if not px.empty and idx in px.columns else pd.Series(dtype=float)
    d1  = (p1.iloc[-1]/p1.iloc[-2]-1.0)*100 if len(p1)>=2 else np.nan
    ytd = (p1.iloc[-1]/p1.iloc[0]-1.0)*100  if len(p1)>=1 else np.nan
    return {"last": last, "d1": d1, "ytd": ytd}

@st.cache_data(ttl=TTL_PRICE_S, show_spinner=False)
def get_advancers_decliners(tickers: list[str]) -> tuple[int, int]:
    """Nombre de hausses/baisse sur 1 jour."""
    px = get_prices(tickers, period="5d", interval="1d")
    if px.empty:
        return 0, 0
    last = px.ffill().iloc[-2:]
    if len(last) < 2:
        return 0, 0
    ret = last.iloc[-1] / last.iloc[-2] - 1.0
    adv = int((ret > 0).sum())
    dec = int((ret < 0).sum())
    return adv, dec

@st.cache_data(ttl=TTL_PRICE_S, show_spinner=False)
def get_top_movers(tickers: list[str], top_n: int = 5) -> pd.DataFrame:
    """Top gagnants/perdants 1D."""
    px = get_prices(tickers, period="5d", interval="1d")
    if px.empty:
        return pd.DataFrame(columns=["ticker","ret_1d"])
    last = px.ffill().iloc[-2:]
    if len(last) < 2:
        return pd.DataFrame(columns=["ticker","ret_1d"])
    ret = (last.iloc[-1] / last.iloc[-2] - 1.0).sort_values(ascending=False)
    best = ret.head(top_n)
    worst = ret.tail(top_n)
    out = pd.concat([best, worst]).to_frame("ret_1d").reset_index().rename(columns={"index":"ticker"})
    return out

# ------------------------------------------------------------------
# Métadonnées / profils
# ------------------------------------------------------------------
@st.cache_data(ttl=TTL_META_S, show_spinner=False)
def get_profile(ticker: str) -> dict:
    """Métadonnées (secteur, industry, etc.) via yfinance.get_info()."""
    t = yf.Ticker(_normalize_ticker(ticker))
    try:
        info = t.get_info()  # moderne (remplace .info legacy)
    except Exception:
        info = {}
    wanted = {k: info.get(k) for k in [
        "longName","shortName","sector","industry","longBusinessSummary","website",
        "marketCap","sharesOutstanding","trailingPE","forwardPE","priceToBook",
        "enterpriseToEbitda","dividendYield","beta","currency"
    ]}
    return wanted

# ------------------------------------------------------------------
# États financiers
# ------------------------------------------------------------------
@st.cache_data(ttl=TTL_FUND_S, show_spinner=False)
def get_statements(ticker: str) -> dict:
    """États financiers annuels et trimestriels (si dispo)."""
    t = yf.Ticker(_normalize_ticker(ticker))
    out = {}
    try:
        out["income_q"] = t.get_income_stmt(freq="quarterly")
        out["income_a"] = t.get_income_stmt(freq="annual")
    except Exception:
        out["income_q"] = pd.DataFrame()
        out["income_a"] = pd.DataFrame()
    try:
        out["bs_q"] = t.get_balance_sheet(freq="quarterly")
        out["bs_a"] = t.get_balance_sheet(freq="annual")
    except Exception:
        out["bs_q"] = pd.DataFrame()
        out["bs_a"] = pd.DataFrame()
    try:
        out["cf_q"] = t.get_cashflow(freq="quarterly")
        out["cf_a"] = t.get_cashflow(freq="annual")
    except Exception:
        out["cf_q"] = pd.DataFrame()
        out["cf_a"] = pd.DataFrame()
    return out

# ------------------------------------------------------------------
# News
# ------------------------------------------------------------------
@st.cache_data(ttl=TTL_PRICE_S, show_spinner=False)
def get_news(ticker: str) -> list[dict]:
    t = yf.Ticker(_normalize_ticker(ticker))
    try:
        return t.get_news() or []
    except Exception:
        return []
    
    # --- Recherche Yahoo: nom -> tickers TSX -------------------------------------
import requests

@st.cache_data(ttl=3600)
def search_tsx_symbols(query: str, max_results: int = 10) -> list[dict]:
    """
    Retourne une liste de correspondances {'symbol','name','type'} pour le TSX,
    en se basant sur l'autocomplétion Yahoo Finance.
    """
    if not query or not query.strip():
        return []

    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {
        "q": query.strip(),
        "lang": "fr-CA",
        "region": "CA",
        "quotesCount": max_results,
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=8)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return []

    out = []
    for q in data.get("quotes", []):
        sym = q.get("symbol", "")
        exch = q.get("exchange", "")
        # On garde uniquement TSX / Toronto
        if sym.endswith(".TO") or exch in ("TSX", "TOR"):
            out.append({
                "symbol": sym,
                "name": q.get("shortname") or q.get("longname") or q.get("name") or "",
                "type": q.get("quoteType") or "",
            })
    return out

    