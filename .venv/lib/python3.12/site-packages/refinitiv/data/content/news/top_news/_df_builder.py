import pandas as pd
from numpy import datetime64

from ...._tools import get_from_path, convert_dtypes

headline_data_key_by_column = {
    "headline": "text",
    "snippet": "snippet",
    "storyId": "storyId",
    "imageId": "image.id",
}


def news_top_build_df(raw: dict, **kwargs):
    raw_data = raw.get("data", [{}])

    # data
    columns = headline_data_key_by_column.keys()
    data = [
        [get_from_path(headline_data, path) for path in headline_data_key_by_column.values()]
        for headline_data in raw_data
    ]

    # index
    index_data = [datetime64(headline_data.get("versionCreated")) for headline_data in raw_data]
    index = pd.Index(index_data, name="versionCreated")
    df = pd.DataFrame(data, columns=columns, index=index)
    return convert_dtypes(df)
