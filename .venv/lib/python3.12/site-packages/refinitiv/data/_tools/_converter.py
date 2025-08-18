from typing import List, Any, Union
from collections.abc import Iterable

from ._lazy_loader import load as lazy_load

np = lazy_load("numpy")
pd = lazy_load("pandas")


def try_copy_to_list(obj: Any) -> Union[List[Any], Any]:
    if isinstance(obj, (list, tuple, set, dict)) and not isinstance(obj, str):
        return list(obj)

    return obj


class Copier:
    @staticmethod
    def get_list(obj: Any) -> Union[List[Any], Any]:
        if isinstance(obj, Iterable) and not isinstance(obj, str):
            return list(obj)

        return [obj]


def convert_dict_to_df(data, columns) -> "pd.DataFrame":
    if data:
        df = pd.DataFrame(np.array(data), columns=columns)
        if not df.empty:
            df.fillna(pd.NA, inplace=True)
            df = df.convert_dtypes()
    else:
        df = pd.DataFrame([], columns=columns)
    return df


def convert_content_data_to_df(content_data: dict, use_field_names_in_headers: bool = True):
    if "headers" not in content_data or "data" not in content_data:
        return pd.DataFrame()

    if use_field_names_in_headers:
        key = "name"
    else:
        key = "title"

    headers_names = [header[key] for header in content_data["headers"]]
    return convert_dict_to_df(content_data["data"], headers_names)
