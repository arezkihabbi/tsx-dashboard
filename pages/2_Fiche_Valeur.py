# pages/2_Fiche_Valeur.py — Actions du TSX (recherche par nom ou ticker, KPI, rendements vs ^GSPTSE, états financiers)

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import unicodedata
import yfinance as yf

# =========================
# 1) Config Streamlit (doit être la 1ère commande)
# =========================
st.set_page_config(page_title="Actions du TSX", page_icon="📄", layout="wide")

# Cacher la navigation multipage native (on garde seulement notre menu)
st.markdown("""
<style>
section[data-testid="stSidebar"] nav[aria-label="Pages"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] div[role="navigation"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# 2) Sidebar custom + logo
# =========================
with st.sidebar:
    st.image("assets/logo.png", use_container_width=True)
    st.markdown("---")
    st.page_link("app.py",                  label="Acceuil",           icon="🏠")
    st.page_link("pages/1_Screener.py",     label="Screener",      icon="🔎")
    st.page_link("pages/2_Fiche_Valeur.py", label="Action du tsx",  icon="📄")
    st.page_link("pages/3_Comparateur.py",  label="Comparateur",   icon="🆚")
    st.page_link("pages/4_News.py",         label="News",          icon="📰")
    st.markdown("---")

# =========================
# 3) Imports projet
# =========================
from core import data_source as ds
from core.charts import price_chart  # graphe de prix (titre seul)
try:
    from core.ratios import compute_core_ratios
except Exception:
    compute_core_ratios = None


# =========================
# 4) Helpers communs (formatage & états financiers)
# =========================
def _normalize_ticker(t: str) -> str:
    if not t:
        return t
    t = t.strip().upper()
    if t.startswith("^"):
        return t
    return t if t.endswith(".TO") else t + ".TO"

def _coerce_df(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame) or df.empty:
        return pd.DataFrame()
    # Colonnes -> datetime si possible, tri décroissant (plus récent à gauche)
    new_cols = []
    for c in df.columns:
        try:
            new_cols.append(pd.to_datetime(c))
        except Exception:
            new_cols.append(c)
    df.columns = new_cols
    try:
        df = df.reindex(sorted(df.columns, reverse=True), axis=1)
    except Exception:
        pass
    # Numériser quand possible
    return df.apply(pd.to_numeric, errors="ignore")

def _ttm_from_quarterly(qdf: pd.DataFrame) -> pd.Series | None:
    """TTM = somme des 4 derniers trimestres (colonne la plus récente à gauche)."""
    if not isinstance(qdf, pd.DataFrame) or qdf.empty or qdf.shape[1] < 4:
        return None
    last4 = qdf.iloc[:, :4]  # colonnes déjà triées décroissant
    try:
        ttm = pd.to_numeric(last4).sum(axis=1)
        ttm.name = "TTM"
        return ttm
    except Exception:
        return None

def _fmt_thousands(df: pd.DataFrame) -> pd.DataFrame:
    """Formate avec séparateurs de milliers (style Yahoo)."""
    if not isinstance(df, pd.DataFrame) or df.empty:
        return df
    out = df.copy()
    for c in out.columns:
        try:
            out[c] = pd.to_numeric(out[c], errors="coerce").map(
                lambda x: f"{int(x):,}" if pd.notna(x) else ""
            )
        except Exception:
            pass
    return out

def _fetch_statements_direct(ticker: str) -> dict:
    """
    Récupération directe via yfinance (>=0.2.x).
    Ajoute TTM à Income & Cash Flow. Colonnes triées plus récent -> plus ancien.
    """
    sym = _normalize_ticker(ticker)
    tkr = yf.Ticker(sym)

    # Nouveaux getters, fallback auto si indispo (via attributs historiques)
    def _get(what: str, freq: str) -> pd.DataFrame:
        try:
            if what == "income":
                df = tkr.get_income_stmt(freq=freq)
            elif what == "balance":
                df = tkr.get_balance_sheet(freq=freq)
            elif what == "cashflow":
                df = tkr.get_cashflow(freq=freq)
            else:
                df = pd.DataFrame()
        except Exception:
            attr = {
                ("income", "annual"): "income_stmt",
                ("income", "quarterly"): "quarterly_income_stmt",
                ("balance", "annual"): "balance_sheet",
                ("balance", "quarterly"): "quarterly_balance_sheet",
                ("cashflow", "annual"): "cashflow",
                ("cashflow", "quarterly"): "quarterly_cashflow",
            }[(what, freq)]
            df = getattr(tkr, attr, pd.DataFrame())
        return _coerce_df(df)

    income_a = _get("income", "annual")
    income_q = _get("income", "quarterly")
    bs_a     = _get("balance", "annual")
    bs_q     = _get("balance", "quarterly")
    cf_a     = _get("cashflow", "annual")
    cf_q     = _get("cashflow", "quarterly")

    # TTM en 1ère colonne pour Income & Cash Flow
    ttm_inc = _ttm_from_quarterly(income_q)
    if ttm_inc is not None:
        income_a = income_a.copy()
        income_a.insert(0, "TTM", ttm_inc)

    ttm_cf = _ttm_from_quarterly(cf_q)
    if ttm_cf is not None:
        cf_a = cf_a.copy()
        cf_a.insert(0, "TTM", ttm_cf)

    for df in (income_a, income_q, bs_a, bs_q, cf_a, cf_q):
        if not df.empty:
            df.index.name = "Breakdown"

    return {
        "income_a": income_a,
        "income_q": income_q,
        "bs_a": bs_a,
        "bs_q": bs_q,
        "cf_a": cf_a,
        "cf_q": cf_q,
    }

def returns_chart(prices: pd.DataFrame, ticker: str, title_suffix: str = ""):
    """Rendements cumulés (%) du ticker vs ^GSPTSE (base 0 % à la 1ère date commune)."""
    need_cols = [ticker, "^GSPTSE"]
    if not set(need_cols).issubset(prices.columns):
        return None
    df = prices[need_cols].sort_index().ffill().dropna(how="any")
    if df.shape[0] < 2:
        return None
    ret = (df / df.iloc[0] - 1.0) * 100.0
    ret.index.name = "Date"
    long = ret.reset_index().melt(id_vars="Date", var_name="Série", value_name="Rendement (%)")
    titre = f"Rendement cumulé — {ticker} vs ^GSPTSE (base 0 %)"
    if title_suffix:
        titre += f" — {title_suffix}"
    fig = px.line(long, x="Date", y="Rendement (%)", color="Série", title=titre)
    fig.update_yaxes(ticksuffix=" %")
    return fig

def render_kpi_block(ticker: str, prices: pd.DataFrame, info: dict) -> dict:
    """Header + KPIs (Dernier, 1m, YTD, 1y) en vert/rouge."""
    title = info.get("longName") or info.get("shortName") or ticker
    st.subheader(title)
    meta = []
    if info.get("sector"):   meta.append(f"Secteur: **{info['sector']}**")
    if info.get("industry"): meta.append(f"Industrie: **{info['industry']}**")
    if meta:
        st.caption(" • ".join(meta))

    def _ret_days(series: pd.Series, n: int):
        s = series.dropna()
        if len(s) <= n:
            return None
        return float(s.iloc[-1] / s.iloc[-n-1] - 1.0)

    def _ret_ytd(series: pd.Series):
        s = series.dropna()
        if s.empty:
            return None
        start = pd.Timestamp(pd.Timestamp.today().year, 1, 1)
        s = s[s.index >= start]
        if len(s) < 2:
            return None
        return float(s.iloc[-1] / s.iloc[0] - 1.0)

    def _fmt_pct(val):
        if val is None:
            return "—", ""
        cls = "pos" if val >= 0 else "neg"
        return f"{val*100:.2f} %", cls

    s = prices[ticker].dropna() if (not prices.empty and ticker in prices.columns) else pd.Series(dtype=float)
    last_px = float(s.iloc[-1]) if not s.empty else None
    r_1m  = _ret_days(s, 21)
    r_1y  = _ret_days(s, 252)
    r_ytd = _ret_ytd(s)
    currency = info.get("currency") or ""

    st.markdown("""
    <style>
      .kpi .lbl{ color:rgba(255,255,255,0.75); font-size:13px; margin-bottom:4px; }
      .kpi .num{ font-size:34px; font-weight:700; line-height:1.1; }
      .kpi .pct{ font-size:32px; font-weight:700; line-height:1.1; }
      .kpi .pct.pos{ color:#16a34a; } .kpi .pct.neg{ color:#dc2626; }
      .kpi-divider{ border-top:1px solid rgba(255,255,255,.15); margin:16px 0; }
    </style>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="kpi"><div class="lbl">Dernier prix (ajusté)</div>'
            f'<div class="num">{(f"{last_px:.2f} {currency}" if last_px is not None else "N/D")}</div></div>',
            unsafe_allow_html=True
        )
    with c2:
        v, cls = _fmt_pct(r_1m); st.markdown(f'<div class="kpi"><div class="lbl">1 mois</div><div class="pct {cls}">{v}</div></div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        v, cls = _fmt_pct(r_ytd); st.markdown(f'<div class="kpi"><div class="lbl">YTD</div><div class="pct {cls}">{v}</div></div>', unsafe_allow_html=True)
    with c4:
        v, cls = _fmt_pct(r_1y);  st.markdown(f'<div class="kpi"><div class="lbl">1 an</div><div class="pct {cls}">{v}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="kpi-divider"></div>', unsafe_allow_html=True)
    return {"last_px": last_px, "ret_1m": r_1m, "ret_ytd": r_ytd, "ret_1y": r_1y}


# =========================
# 5) Recherche par NOM OU TICKER (Yahoo Search)
# =========================
def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

@st.cache_data(show_spinner=False, ttl=60*60)
def _symbol_exists(sym: str) -> bool:
    try:
        df = yf.Ticker(sym).history(period="5d")
        return not df.empty
    except Exception:
        return False

@st.cache_data(show_spinner=False, ttl=60*60)
def _yahoo_search(query: str, region: str = "CA", lang: str = "fr-CA", count: int = 50) -> list[dict]:
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {
        "q": query,
        "lang": lang,
        "region": region,
        "quotesCount": count,
        "newsCount": 0,
        "enableFuzzyQuery": True,
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=6)
        r.raise_for_status()
        data = r.json() or {}
        quotes = data.get("quotes", []) or []
    except Exception:
        return []

    def _is_tsx(q: dict) -> bool:
        exch = (q.get("exchange") or "").upper()
        disp = (q.get("exchDisp") or "").upper()
        return any(s in exch or s in disp for s in ("TORONTO", "TSX", "TSXV", "TSX VENTURE"))

    tsx, other = [], []
    for q in quotes:
        sym = (q.get("symbol") or "").upper()
        name = q.get("shortname") or q.get("longname") or q.get("name") or sym
        row = {"symbol": sym, "name": name, "exchDisp": q.get("exchDisp") or "", "score": q.get("score", 0)}
        (tsx if _is_tsx(q) else other).append(row)

    tsx.sort(key=lambda x: x.get("score", 0), reverse=True)

    if not tsx:
        converted = []
        for q in other:
            sym = q["symbol"]
            if sym.startswith("^") or sym.endswith(".TO"):
                continue
            candidate = sym + ".TO"
            if _symbol_exists(candidate):
                converted.append({**q, "symbol": candidate, "exchDisp": "Toronto"})
        converted.sort(key=lambda x: x.get("score", 0), reverse=True)
        tsx = converted

    seen, uniq = set(), []
    for h in tsx:
        if h["symbol"] not in seen:
            seen.add(h["symbol"])
            uniq.append(h)
    return uniq

def _resolve_query_to_ticker(user_query: str) -> tuple[str, list[dict]]:
    """Résout une recherche (nom ou ticker) en symbole TSX; retourne (ticker, hits)."""
    if not user_query:
        return "", []
    q_raw = user_query.strip()
    q = _strip_accents(q_raw).upper()

    # Si l'utilisateur tape déjà un ticker
    if (len(q) <= 5 and q.isalpha()) or q.endswith(".TO") or q.startswith("^"):
        return (_normalize_ticker(q), [])

    # Sinon: recherche par nom
    hits = _yahoo_search(q)
    if not hits:
        candidate = _normalize_ticker(q)
        return (candidate if _symbol_exists(candidate) else ""), []

    if len(hits) == 1:
        return hits[0]["symbol"], hits
    return "", hits


# =========================
# 6) UI & données
# =========================
st.title("📄 Actions du TSX ")

# Valeur par défaut: query param ?ticker= ; sinon RY.TO
qp = st.query_params.get("ticker", ["RY.TO"])
default_q = qp[0] if isinstance(qp, list) else qp

search_text = st.text_input(
    "Rechercher un titre (nom ou ticker TSX)",
    value=(default_q or "RY.TO")
)

resolved_ticker, hits = _resolve_query_to_ticker(search_text)

# Si plusieurs correspondances: on laisse choisir
if hits and not resolved_ticker:
    options = [f"{h['symbol']} — {h['name']} ({h['exchDisp']})" for h in hits]
    choice = st.selectbox("Plusieurs correspondances trouvées :", options, index=0)
    idx = options.index(choice)
    ticker = hits[idx]["symbol"]
else:
    ticker = resolved_ticker or _normalize_ticker(default_q)

# Contrôles de graphes
col_cfg1, col_cfg2, _ = st.columns([1, 1, 2])
with col_cfg1:
    horizon = st.selectbox("Période", ["YTD", "1 an", "3 ans", "5 ans", "Max"], index=4)
with col_cfg2:
    echelle_log = st.toggle("Échelle log (prix)", value=False)

period_map = {"YTD": "1y", "1 an": "1y", "3 ans": "3y", "5 ans": "5y", "Max": "max"}

# Bouton News
colH, colBtn = st.columns([5,1])
with colBtn:
    if st.button("📰 News"):
        try:
            st.query_params["ticker"] = ticker
        except Exception:
            pass
        st.switch_page("pages/4_News.py")

# Données de prix/profil
prices = ds.get_prices([ticker, "^GSPTSE"], period=period_map[horizon], interval="1d").sort_index()
info   = ds.get_profile(ticker)

# Si YTD, tronquer au 1er janvier
if horizon == "YTD" and not prices.empty:
    start = pd.Timestamp(pd.Timestamp.today().year, 1, 1)
    prices = prices.loc[prices.index >= start]

# =========================
# 7) Graphes + KPI
# =========================
colA, colB = st.columns([2, 1])

with colA:
    # Prix
    if not prices.empty and ticker in prices.columns:
        fig_price = price_chart(prices[[ticker]].dropna(), f"Prix ajusté — {ticker} ({horizon})")
        if echelle_log:
            fig_price.update_yaxes(type="log")
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.warning(f"Prix indisponibles pour {ticker}. Vérifie le symbole (ex. RY.TO).")

    # Rendements cumulés vs ^GSPTSE
    if {ticker, "^GSPTSE"}.issubset(prices.columns):
        fig_ret = returns_chart(prices, ticker, title_suffix=horizon)
        if fig_ret is not None:
            st.plotly_chart(fig_ret, use_container_width=True)
        else:
            st.info("Pas assez de données pour calculer les rendements comparés.")
    else:
        st.info("Le benchmark ^GSPTSE n'est pas disponible.")

with colB:
    kpi = render_kpi_block(ticker, prices, info)

    st.write("**Ratios principaux**")
    if compute_core_ratios and kpi["last_px"] is not None:
        stmts_rat = ds.get_statements(ticker)
        ratios = compute_core_ratios(price=kpi["last_px"], info=info, stmts=stmts_rat)
        if isinstance(ratios, dict) and ratios:
            st.dataframe(pd.DataFrame.from_dict(ratios, orient="index", columns=["Valeur"]),
                         use_container_width=True)
        else:
            st.caption("Ratios indisponibles.")
    else:
        st.caption("Ratios indisponibles (module ou prix manquant).")

st.divider()

# =========================
# 8) États financiers (robustes)
# =========================
st.subheader("📑 États financiers (aperçu)")
st.caption("TTM calculé à partir des 4 derniers trimestres lorsqu’ils sont disponibles.")

# 1) Essayer les états via ton module
stm = ds.get_statements(ticker) or {}

# 2) Si annuels vides, fallback direct yfinance (nouveaux getters)
need = ["income_a", "bs_a", "cf_a"]
if not any(isinstance(stm.get(k), pd.DataFrame) and not stm.get(k).empty for k in need):
    stm = _fetch_statements_direct(ticker)

def show_or_info(df: pd.DataFrame, title: str) -> bool:
    if isinstance(df, pd.DataFrame) and not df.empty:
        st.dataframe(_fmt_thousands(df), use_container_width=True)
        return True
    st.info(f"{title} indisponible en annuel sur Yahoo pour {ticker}.")
    return False

tab1, tab2, tab3 = st.tabs(["Compte de résultat (annuel)", "Bilan (annuel)", "Flux de trésorerie (annuel)"])

with tab1:
    inc_a = stm.get("income_a")
    if not show_or_info(inc_a, "Compte de résultat (annuel)"):
        inc_q = stm.get("income_q")
        ttm = _ttm_from_quarterly(_coerce_df(inc_q))
        if ttm is not None:
            st.caption("Remplacement : TTM calculé depuis les 4 derniers trimestres")
            st.dataframe(_fmt_thousands(ttm.to_frame("TTM")), use_container_width=True)

with tab2:
    bs_a = stm.get("bs_a")
    if not show_or_info(bs_a, "Bilan (annuel)"):
        bs_q = stm.get("bs_q")
        bs_q = _coerce_df(bs_q)
        if isinstance(bs_q, pd.DataFrame) and not bs_q.empty:
            st.caption("Remplacement : dernier bilan trimestriel disponible")
            last_col = bs_q.columns[0]
            st.dataframe(_fmt_thousands(bs_q[[last_col]].rename(columns={last_col: "Dernier trimestre"})),
                         use_container_width=True)

with tab3:
    cf_a = stm.get("cf_a")
    if not show_or_info(cf_a, "Flux de trésorerie (annuel)"):
        cf_q = stm.get("cf_q")
        ttm = _ttm_from_quarterly(_coerce_df(cf_q))
        if ttm is not None:
            st.caption("Remplacement : TTM calculé depuis les 4 derniers trimestres")
            st.dataframe(_fmt_thousands(ttm.to_frame("TTM")), use_container_width=True)

            
