import pandas as pd


def concat_ownership_dfs(_, responses, **__):
    df = None
    dfs = [response.data.df for response in responses]
    all_dfs_is_none = all(a is None for a in dfs)
    if not all_dfs_is_none:
        df = pd.concat(dfs)
    if df is not None:
        df = df.reset_index(drop=True)
    return df
