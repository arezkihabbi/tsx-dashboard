import numpy as np
import pandas as pd

from ._buckets_data import get_counts_labels_filters


def build_navigators_df(raw: dict) -> pd.DataFrame:
    if "Navigators" in raw:
        data_by_nav_name = {}
        buckets_counts = []
        for navigator_name, navigator_data in raw["Navigators"].items():
            for buckets in navigator_data.values():
                counts, labels, filters = get_counts_labels_filters(buckets)
                data = {navigator_name: labels, "Count": counts}

                if filters:
                    data["Filter"] = filters

                data_by_nav_name[navigator_name] = data
                buckets_counts.append(counts)

        dfs = [pd.DataFrame(bucket_data) for bucket_data in data_by_nav_name.values()]

        if len(dfs) == 1:
            df = dfs[0]

        elif not any(buckets_counts):
            df = pd.DataFrame([], columns=[*data_by_nav_name.keys(), "Label", "Count"])

        elif all(item == buckets_counts[0] for item in buckets_counts):
            df = pd.merge(*dfs, on="Count", how="outer")

        else:
            df = pd.concat(dfs)
            df = df.sort_values("Count", ascending=False)

        df.replace({np.nan: pd.NA}, inplace=True)
        return df

    else:
        return pd.DataFrame()


def build_metadata_df(metadata_properties: dict, search_df: pd.DataFrame) -> pd.DataFrame:
    data = []
    for prop_name in metadata_properties:
        if prop_name in search_df["Property"].values:
            metadata_properties[prop_name]["Property"] = prop_name
            data.append(metadata_properties[prop_name])

    df = pd.DataFrame(data)
    df.set_index("Property", inplace=True)
    df.replace(np.nan, False, inplace=True)
    return df


def build_search_df(raw: dict, total: int) -> pd.DataFrame:
    data = []

    if total > 0:
        unique_prop_names = []
        for property_name, value in raw["Hits"][0]["raw_source"].items():
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                for node in value:
                    for nested_property, nested_value in node.items():
                        nested_prop_name = f"{property_name}.{nested_property}"
                        if nested_prop_name in unique_prop_names:
                            continue

                        data.append([nested_prop_name, nested_value])
                        unique_prop_names.append(nested_prop_name)

            else:
                if property_name in unique_prop_names:
                    continue

                data.append([property_name, value])
                unique_prop_names.append(property_name)

    return pd.DataFrame(data, columns=["Property", "Example Value"])


def merge_metadata_df_and_search_df(metadata_df: pd.DataFrame, search_df: pd.DataFrame) -> pd.DataFrame:
    if metadata_df.index.nlevels > 1:
        metadata_df.index.set_names(["Property", "Nested"], inplace=True)
        metadata_df.reset_index(inplace=True)
        metadata_df.loc[(metadata_df.Property == metadata_df.Nested), "Nested"] = ""
        df = search_df.join(metadata_df.set_index(["Property"]), on=["Property"])
        df.drop("Nested", inplace=True, axis=1)
    else:
        metadata_df.index.set_names(["Property"], inplace=True)
        metadata_df.reset_index(inplace=True)
        df = search_df.join(metadata_df.set_index(["Property"]), on="Property")
    df.replace({np.nan: pd.NA}, inplace=True)
    df = df.astype("str")
    return df
