from typing import Callable, List, TYPE_CHECKING

import pandas as pd

from ..._tools import convert_dtypes, convert_str_to_timestamp

if TYPE_CHECKING:
    from .headlines._data import Headline


def tz_replacer(s: str) -> str:
    if isinstance(s, str):
        if s.endswith("Z"):
            s = s[:-1]
        elif s.endswith("-0000"):
            s = s[:-5]
        if s.endswith(".000"):
            s = s[:-4]
    return s


def news_build_df(raw: dict, **kwargs) -> pd.DataFrame:
    columns = ["headline", "storyId", "sourceCode"]
    if isinstance(raw, list):
        content_data = []

        for i in raw:
            content_data.extend(i["data"])

    else:
        content_data = raw["data"]

    index = [
        convert_str_to_timestamp(tz_replacer(headline["newsItem"]["itemMeta"]["versionCreated"]["$"]))
        for headline in content_data
    ]

    data = []

    for headline_data in content_data:
        news_item = headline_data.get("newsItem", dict())
        item_meta = news_item.get("itemMeta", {})
        info_sources = news_item["contentMeta"]["infoSource"]
        info_source = next(
            (item["_qcode"] for item in info_sources if item["_role"] == "sRole:source"),
            None,
        )
        data.append(
            [
                item_meta["title"][0]["$"],
                headline_data["storyId"],
                info_source,
            ]
        )
    if data:
        df = pd.DataFrame(
            data=data,
            index=index,
            columns=columns,
        )
        df = convert_dtypes(df)

    else:
        df = pd.DataFrame([], columns=columns)
    df.index.name = "versionCreated"
    return df


def _get_headline_from_story(story: dict) -> str:
    news_item = story.get("newsItem", dict())
    content_meta = news_item.get("contentMeta", dict())
    headline = content_meta.get("headline", [dict()])
    return headline[0].get("$")


def get_headlines(
    raw: dict,
    build_headline: Callable[[dict], "Headline"],
    limit: int,
) -> List["Headline"]:
    headlines = []

    if isinstance(raw, list):
        data = []
        for i in raw:
            data.extend(i.get("data", i.get("headlines", [])))

    else:
        data = raw.get("data", raw.get("headlines", []))

    for datum in data:
        headline = build_headline(datum)
        headlines.append(headline)

    headlines = headlines[:limit]
    return headlines
