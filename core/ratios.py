# core/ratios.py
# Calculs de ratios avec fallback quand les champs manquent.

from __future__ import annotations
import numpy as np
import pandas as pd

def _col_like(df: pd.DataFrame, candidates: list[str]) -> str | None:
    if df is None or df.empty:
        return None
    cols = {c.lower(): c for c in df.index.astype(str)}
    for name in candidates:
        for k, orig in cols.items():
            if name.lower() in k:
                return orig
    return None

def ttm_sum(df_q: pd.DataFrame, candidates: list[str]) -> float | None:
    """Somme des 4 derniers trimestres pour une ligne candidate."""
    if df_q is None or df_q.empty:
        return None
    row = _col_like(df_q, candidates)
    if row is None:
        return None
    s = df_q.loc[row].dropna().astype(float).sort_index(axis=0).tail(4)
    if s.empty:
        return None
    return float(s.sum())

def latest_value(df: pd.DataFrame, candidates: list[str]) -> float | None:
    if df is None or df.empty:
        return None
    row = _col_like(df, candidates)
    if row is None:
        return None
    s = df.loc[row].dropna().astype(float).sort_index(axis=0)
    if s.empty:
        return None
    return float(s.iloc[-1])

def safe_div(a: float | None, b: float | None) -> float | None:
    try:
        if a is None or b is None or b == 0:
            return None
        return float(a) / float(b)
    except Exception:
        return None

def compute_core_ratios(price: float | None,
                        info: dict,
                        stmts: dict) -> dict:
    """
    Calcul de quelques ratios clés avec fallback:
    - P/E (trailing)
    - EV/EBITDA (ttm)
    - P/B
    - P/S (ttm)
    - FCF yield (ttm)
    - ROE (ttm)
    - D/E
    - Current ratio
    - Interest coverage (EBIT/IntExp ttm)
    """
    out = {}

    # Prix & market cap
    mcap = info.get("marketCap")
    shares = info.get("sharesOutstanding")

    # Trailing PE (fallback via EPS TTM)
    pe = info.get("trailingPE")
    if pe is None and price is not None and shares:
        net_income_ttm = ttm_sum(stmts.get("income_q"), ["net income", "net income common"])
        eps_ttm = safe_div(net_income_ttm, shares)
        pe = safe_div(price, eps_ttm)
    out["P/E (TTM)"] = pe

    # P/B
    out["P/B"] = info.get("priceToBook")

    # P/S (TTM)
    ps = info.get("priceToSalesTrailing12Months")
    if ps is None and price is not None and shares:
        sales_ttm = ttm_sum(stmts.get("income_q"), ["total revenue", "revenue", "sales"])
        ps = safe_div(price * shares, sales_ttm)
    out["P/S (TTM)"] = ps

    # EV/EBITDA
    ev_ebitda = info.get("enterpriseToEbitda")
    if ev_ebitda is None:
        total_debt = latest_value(stmts.get("bs_a"), ["total debt", "long term debt", "short long term debt"])
        cash = latest_value(stmts.get("bs_a"), ["cash", "cash and cash equivalents"])
        ev = None
        if mcap is not None and total_debt is not None and cash is not None:
            ev = mcap + total_debt - cash
        ebitda_ttm = ttm_sum(stmts.get("income_q"), ["ebitda"])
        ev_ebitda = safe_div(ev, ebitda_ttm)
    out["EV/EBITDA (TTM)"] = ev_ebitda

    # FCF yield (TTM)
    fcf_ttm = None
    cf_q = stmts.get("cf_q")
    if cf_q is not None and not cf_q.empty:
        # Free Cash Flow ~ Operating CF - CapEx
        ocf_ttm = ttm_sum(cf_q, ["total cash from operating activities", "operating cash flow"])
        capex_ttm = ttm_sum(cf_q, ["capital expenditures"])
        if ocf_ttm is not None and capex_ttm is not None:
            fcf_ttm = ocf_ttm - capex_ttm
    fcf_yield = safe_div(fcf_ttm, mcap) if mcap else None
    out["FCF Yield (TTM)"] = fcf_yield

    # ROE (TTM)
    equity = latest_value(stmts.get("bs_a"), ["total stockholder equity", "total shareholders equity"])
    net_income_ttm = ttm_sum(stmts.get("income_q"), ["net income", "net income common"])
    out["ROE (TTM)"] = safe_div(net_income_ttm, equity)

    # D/E
    total_debt = latest_value(stmts.get("bs_a"), ["total debt", "long term debt"])
    out["D/E"] = safe_div(total_debt, equity)

    # Current ratio
    current_assets = latest_value(stmts.get("bs_a"), ["total current assets"])
    current_liab = latest_value(stmts.get("bs_a"), ["total current liabilities"])
    out["Current Ratio"] = safe_div(current_assets, current_liab)

    # Interest coverage (EBIT / Interest expense)
    ebit_ttm = None
    inc_q = stmts.get("income_q")
    if inc_q is not None and not inc_q.empty:
        # EBIT ~ Operating Income
        ebit_ttm = ttm_sum(inc_q, ["ebit", "operating income"])
    int_exp_ttm = ttm_sum(inc_q, ["interest expense", "interest expense non operating"])
    out["Interest Coverage"] = safe_div(ebit_ttm, abs(int_exp_ttm) if int_exp_ttm else None)

    # Dividend yield
    dy = info.get("dividendYield")
    out["Dividend Yield"] = dy

    # Beta (info)
    out["Beta"] = info.get("beta")

    # Nettoyage: arrondis légers
    for k, v in out.items():
        if isinstance(v, (int, float)) and v is not None and np.isfinite(v):
            if "Yield" in k:
                out[k] = float(v)
            elif k in ["P/E (TTM)", "EV/EBITDA (TTM)", "P/B", "P/S (TTM)", "D/E", "Current Ratio", "Interest Coverage"]:
                out[k] = float(v)
            elif k in ["ROE (TTM)"]:
                out[k] = float(v)
    return out


