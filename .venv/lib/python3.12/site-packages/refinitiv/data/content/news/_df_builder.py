import pandas as pd


def concat_news_dfs(_, responses, limit: int, **__):
    df = None
    dfs = [response.data.df for response in responses]
    all_dfs_is_none = all(a is None for a in dfs)
    if not all_dfs_is_none:
        df = pd.concat(dfs)
    return df[:limit] if limit else df
