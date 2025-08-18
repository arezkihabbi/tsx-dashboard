from typing import List

import pandas as pd


def bulk_build_df(raw: dict, column_by_field: dict, columns: List[str], **kwargs) -> pd.DataFrame:
    fields = [column_by_field.get(column, column) for i, (column, *_) in enumerate(columns)]
    df = pd.DataFrame(raw, columns=fields)
    if not df.empty:
        df = df.convert_dtypes()

    return df
