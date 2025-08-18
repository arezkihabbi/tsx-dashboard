from ._dictionary import Dictionary, DictionaryType, FieldDescription, EnumTypeEntry
from ._types import RWFDataType, FieldType


def check_websocket_version():
    from ...._tools import version_to_tuple
    import websocket

    min_supt_ver = (1, 5, 1)
    if version_to_tuple(websocket.__version__) < min_supt_ver:
        import warnings

        warnings.warn(
            f"Your version of websocket-client is old for using rd.delivery.dictionary, update to >= {min_supt_ver}"
        )
