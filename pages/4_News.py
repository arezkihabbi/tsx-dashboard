# pages/4_News.py — Actualités (Yahoo Finance, FR & Canada priorisés)

from __future__ import annotations

import re
import html
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

import streamlit as st


# =========================
# 1) Config Streamlit
# =========================
st.set_page_config(page_title="Actualités", page_icon="📰", layout="wide")

# Cacher la nav multipage native
st.markdown("""
<style>
section[data-testid="stSidebar"] nav[aria-label="Pages"] { display:none !important; }
[data-testid="stSidebarNav"] { display:none !important; }
section[data-testid="stSidebar"] div[role="navigation"] { display:none !important; }
</style>
""", unsafe_allow_html=True)


# =========================
# 2) Sidebar custom + logo
# =========================
with st.sidebar:
    try:
        st.image("assets/logo.png")
    except Exception:
        pass
    st.markdown("---")
    st.page_link("app.py",                  label="Accueil",      icon="🏠")
    st.page_link("pages/1_Screener.py",     label="Screener",     icon="🔎")
    st.page_link("pages/2_Fiche_Valeur.py", label="Actions TSX",  icon="📈")
    st.page_link("pages/3_Comparateur.py",  label="Comparateur",  icon="🆚")
    st.page_link("pages/4_News.py",         label="Actualités",   icon="🖼️")
    st.markdown("---")


# =========================
# 3) Flux & helpers
# =========================

# Flux FR (prioritaires) puis EN (fallback)
YF_RSS_FR = [
    "https://fr.finance.yahoo.com/actualites/rssindex",
    "https://fr.finance.yahoo.com/news/rssindex",
]
YF_RSS_EN = [
    "https://ca.finance.yahoo.com/news/rssindex",     # Canada (EN)
    "https://finance.yahoo.com/news/rssindex",        # Global (EN)
]

# Styles cartes compactes
st.markdown("""
<style>
.news-row { padding:12px 0; border-bottom:1px solid rgba(255,255,255,.08); }
.news-title a { color:#9dd1ff; text-decoration:none; font-weight:600; }
.news-title a:hover { text-decoration:underline; }
.news-meta { color:rgba(255,255,255,.55); font-size:12px; }
.thumb-box { width:78px; height:78px; background:rgba(255,255,255,.06);
             border-radius:10px; display:flex; align-items:center; justify-content:center; overflow:hidden; }
.thumb-box img { object-fit:cover; width:78px; height:78px; }
</style>
""", unsafe_allow_html=True)


def _strip_html(s: str) -> str:
    s = re.sub(r"<br\s*/?>", "\n", s or "", flags=re.I)
    s = re.sub(r"<.*?>", "", s or "")
    return html.unescape(s).strip()


def _human_time(dt: datetime | None) -> str:
    if not dt:
        return ""
    now = datetime.now(timezone.utc)
    diff = (now - dt).total_seconds()
    if diff < 60:
        return "à l’instant"
    if diff < 3600:
        m = int(diff // 60);  return f"il y a {m} minute{'s' if m>1 else ''}"
    if diff < 86400:
        h = int(diff // 3600); return f"il y a {h} heure{'s' if h>1 else ''}"
    d = int(diff // 86400);   return f"il y a {d} jour{'s' if d>1 else ''}"


def _parse_pubdate(text: str | None) -> datetime | None:
    if not text:
        return None
    # RFC 2822
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(text).astimezone(timezone.utc)
    except Exception:
        pass
    # ISO
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def _find_thumb(item: ET.Element) -> str | None:
    for tag in ("{http://search.yahoo.com/mrss/}content", "{http://search.yahoo.com/mrss/}thumbnail"):
        for n in item.findall(tag):
            url = n.attrib.get("url")
            if url:
                return url
    enc = item.find("enclosure")
    if enc is not None:
        url = enc.attrib.get("url")
        if url:
            return url
    return None


@st.cache_data(ttl=600, show_spinner=False)
def fetch_rss(url: str) -> list[dict]:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=10) as resp:
            data = resp.read()
    except (URLError, HTTPError):
        return []

    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return []

    out: list[dict] = []
    items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
    for it in items:
        title = _strip_html((it.findtext("title") or it.findtext("{http://www.w3.org/2005/Atom}title") or "").strip())
        link = (it.findtext("link") or it.findtext("{http://www.w3.org/2005/Atom}link") or "").strip()
        if not link:
            lk = it.find("{http://www.w3.org/2005/Atom}link")
            if lk is not None:
                link = lk.attrib.get("href", "").strip()
        desc = it.findtext("description") or it.findtext("{http://www.w3.org/2005/Atom}summary") or ""
        summary = _strip_html(desc)
        pub = it.findtext("pubDate") or it.findtext("{http://www.w3.org/2005/Atom}updated") or ""
        published = _parse_pubdate(pub)
        img = _find_thumb(it)

        try:
            dom = urlparse(link).netloc
            source = dom.replace("www.", "")
        except Exception:
            source = "finance.yahoo.com"

        if title and link:
            out.append({
                "title": title,
                "link": link,
                "summary": summary,
                "image": img,
                "published": published,
                "source": source,
            })
    return out


# --------- Priorisation FR & Canada (plus agressive) ---------

FR_HINTS = {
    " le ", " la ", " les ", " des ", " aux ", " du ", " de ",
    " bourse", " action", " obligations", " dividende", "rendement",
    " économie", " croissance", " inflation", " récession",
    " québec", " montréal", " toronto", " ottawa", " vancouver", " calgary",
    " dollar canadien", " cad ", " tsx", " gsp",  # (gsp pour ^GSPTSE)
}

CA_HINTS = {
    " canada", " canadien", " canadienne", " toronto", " ottawa", " québec",
    " vancouver", " alberta", " ontario", " saskatchewan", " manitoba",
    " tsx", ".to", " cad ", " banque du canada", " boc", " gsp",
    " royal bank of canada", " rbc", " td bank", " scotiabank", " bmo", " cibc",
    " enbridge", " suncor", " canadian natural", " cnq", " shopify",
    " bell", " bce", " rogers", " telus", " bombardier", " air canada",
}

def _is_french_like(text: str) -> bool:
    """Heuristique simple pour repérer du FR (mots-outils + accents)."""
    t = " " + (text or "").lower() + " "
    score = 0
    if any(k in t for k in FR_HINTS): score += 1
    if re.search(r"[éèêàùç]", t):     score += 1
    return score >= 1

def _is_canada_focused(title: str, source: str, link: str) -> bool:
    t = " " + (title or "").lower() + " "
    if any(k in t for k in CA_HINTS): return True
    if source.endswith(".ca"):        return True
    if "ca.finance.yahoo.com" in source: return True
    if ".to" in t:                    return True
    return False

def _score_item(item: dict) -> int:
    title = (item.get("title") or "") + " " + (item.get("summary") or "")
    source = (item.get("source") or "").lower()
    link   = (item.get("link") or "").lower()

    score = 0
    # Français très favorisé
    if "fr.finance.yahoo.com" in source or source.startswith("fr."):
        score += 50
    if _is_french_like(title):
        score += 25

    # Canada très favorisé
    if _is_canada_focused(title, source, link):
        score += 40

    # Bonus date (les plus récents un peu remontés dans les égalités)
    if item.get("published"):
        score += 1
    return score


def aggregate_news(limit: int = 40) -> list[dict]:
    """FR d'abord, EN ensuite. Puis on sépare en PRÉFÉRÉS (FR/Canada) et AUTRES."""
    raw: list[dict] = []
    seen: set[str] = set()

    def _add(items: list[dict]):
        for it in items:
            lk = it.get("link")
            if not lk or lk in seen:
                continue
            seen.add(lk)
            raw.append(it)
            if len(raw) >= limit * 3:   # on prend large, on filtrera après
                break

    # 1) FR
    for url in YF_RSS_FR:
        _add(fetch_rss(url))
        if len(raw) >= limit * 2:
            break

    # 2) EN (Canada & Global)
    if len(raw) < limit * 2:
        for url in YF_RSS_EN:
            _add(fetch_rss(url))
            if len(raw) >= limit * 3:
                break

    # 3) Séparation préférés vs autres
    preferred, others = [], []
    for it in raw:
        score = _score_item(it)
        if score >= 50:  # seuil agressif FR/Canada
            preferred.append((score, it))
        else:
            others.append((score, it))

    # 4) Tri (score desc puis date desc)
    def _sort_key(x):
        it = x[1]
        dt = it.get("published") or datetime.min.replace(tzinfo=timezone.utc)
        return (x[0], dt)

    preferred.sort(key=_sort_key, reverse=True)
    others.sort(key=_sort_key, reverse=True)

    ordered = [it for _, it in preferred] + [it for _, it in others]
    return ordered[:limit]


def render_card(item: dict):
    with st.container():
        st.markdown('<div class="news-row">', unsafe_allow_html=True)
        col_img, col_txt = st.columns([1, 11])

        with col_img:
            if item.get("image"):
                st.markdown(
                    f'<div class="thumb-box"><img src="{item["image"]}" alt=""></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown('<div class="thumb-box">—</div>', unsafe_allow_html=True)

        with col_txt:
            title = item.get("title", "Sans titre")
            link = item.get("link", "#")
            pub = _human_time(item.get("published"))
            src = item.get("source", "finance.yahoo.com")

            st.markdown(f'<div class="news-title"><a href="{link}" target="_blank">{title}</a></div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="news-meta">{src} • {pub}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 4) UI
# =========================
st.title("📰 Actualités")

col_btn, _ = st.columns([1, 8])
with col_btn:
    if st.button("🔄 Actualiser le flux"):
        fetch_rss.clear()  # vide le cache
        st.experimental_rerun()

feed = aggregate_news(limit=40)

if not feed:
    st.info("Aucune actualité n’a été récupérée pour le moment.")
else:
    for it in feed:
        render_card(it)
        