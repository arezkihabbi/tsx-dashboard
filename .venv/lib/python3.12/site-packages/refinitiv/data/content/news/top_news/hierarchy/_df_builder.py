import pandas as pd
from ....._tools import convert_str_to_timestamp


page_key_by_column = {
    "revisionId": "revisionId",
    "revisionDate": "revisionDate",
    "topNewsId": "topNewsId",
}


def news_top_hierarchy_build_df(raw: dict, **kwargs) -> pd.DataFrame:
    raw_data = raw.get("data", [{}])

    # data
    columns = page_key_by_column.keys()
    data = [
        [
            convert_str_to_timestamp(page.get(key)) if key == "revisionDate" else page.get(key)
            for key in page_key_by_column.values()
        ]
        for category in raw_data
        for page in category.get("pages", [{}])
    ]
    # index
    index_data = [(category["name"], page["name"]) for category in raw_data for page in category["pages"]]
    index = pd.MultiIndex.from_tuples(index_data, names=("Category", "Subcategory"))

    return pd.DataFrame(data, index=index, columns=columns)
