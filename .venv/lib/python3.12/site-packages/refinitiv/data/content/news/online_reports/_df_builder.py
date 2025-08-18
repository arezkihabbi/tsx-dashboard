import pandas as pd
from numpy import datetime64

from ...._tools import get_from_path, convert_dtypes


def get_images_ids(headline_data):
    images_data = get_from_path(headline_data, "newsItem/itemMeta/link/0/remoteContent", "/")
    if not images_data:
        return ""
    return "\n".join((i.get("_residref", "") for i in images_data))


def news_online_reports_build_df(raw: dict, **kwargs):
    raw_data = raw.get("data", [{}])

    # data
    columns = ["firstParagraph", "ImageId", "title"]
    data = [
        [
            get_from_path(headline_data, "newsItem/firstParagraph", "/"),
            get_images_ids(headline_data),
            get_from_path(headline_data, "newsItem/itemMeta/title/0/$", "/"),
        ]
        for headline_data in raw_data
    ]

    # index
    index_data = [
        datetime64(get_from_path(headline_data, "newsItem/itemMeta/versionCreated/$", "/"))
        for headline_data in raw_data
    ]
    index = pd.Index(index_data, name="versionCreated")
    df = pd.DataFrame(data, columns=columns, index=index)
    return convert_dtypes(df)
