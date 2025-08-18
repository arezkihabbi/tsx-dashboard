import pandas as pd

region_report_key_by_column = {
    "description": "description",
    "language": "language",
}


def news_online_reports_hierarchy_build_df(raw: dict, **kwargs) -> pd.DataFrame:
    raw_data = raw.get("data", [{}])

    columns = region_report_key_by_column.keys()

    data = []
    index_data = []

    for region in raw_data:
        for report in region.get("reports", [{}]):
            data.append([report.get(key) for key in region_report_key_by_column.values()])
            index_data.append((region["name"], report["reportId"]))

    index = pd.MultiIndex.from_tuples(index_data, names=("Name", "Report ID"))

    return pd.DataFrame(data, index=index, columns=columns)
