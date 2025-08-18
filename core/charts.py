# core/charts.py
import pandas as pd
import plotly.express as px

def price_chart(prices: pd.Series | pd.DataFrame, title: str = ""):
    """Courbe de prix (ajusté). Accepte une série (un ticker) ou un DF multi-tickers."""
    if isinstance(prices, pd.Series):
        df = prices.rename("price").reset_index()
        fig = px.line(df, x=df.columns[0], y="price", title=title)
    else:
        df = prices.reset_index().melt(id_vars=prices.index.name or "Date", var_name="Ticker", value_name="Price")
        fig = px.line(df, x=df.columns[0], y="Price", color="Ticker", title=title)
    fig.update_layout(margin=dict(l=10,r=10,b=10,t=40), height=380)
    return fig

def normalized_return_chart(prices: pd.DataFrame, title: str = "Rendement normalisé"):
    """Indexe chaque série à 100 au départ."""
    base = prices.ffill().dropna().copy()
    base = base / base.iloc[0] * 100.0
    df = base.reset_index().melt(id_vars=base.index.name or "Date", var_name="Ticker", value_name="Index (100=Départ)")
    fig = px.line(df, x=df.columns[0], y="Index (100=Départ)", color="Ticker", title=title)
    fig.update_layout(margin=dict(l=10,r=10,b=10,t=40), height=420)
    return fig
