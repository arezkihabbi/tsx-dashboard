from ..._base_enum import StrEnum
from typing import TYPE_CHECKING, Tuple

from ..._content_type import ContentType
from ..._core.session.tools import is_platform_session
from ..._tools import make_enum_arg_parser, ArgsParser, validate_bool_value

if TYPE_CHECKING:
    from ..._core.session import Session


class DataGridType(StrEnum):
    UDF = "udf"
    RDP = "rdp"


data_grid_types_arg_parser = make_enum_arg_parser(DataGridType)
use_field_names_in_headers_arg_parser = ArgsParser(validate_bool_value)

data_grid_type_value_by_content_type = {
    DataGridType.UDF: ContentType.DATA_GRID_UDF,
    DataGridType.RDP: ContentType.DATA_GRID_RDP,
}

content_type_by_data_grid_type = {
    ContentType.DATA_GRID_UDF: DataGridType.UDF,
    ContentType.DATA_GRID_RDP: DataGridType.RDP,
}


def get_data_grid_type(content_type: ContentType) -> DataGridType:
    data_grid_type = content_type_by_data_grid_type.get(content_type)

    if not data_grid_type:
        raise ValueError(f"There is no DataGridType for content_type:{content_type}")

    return data_grid_type


def get_content_type(session: "Session") -> ContentType:
    from ...delivery._data._data_provider_factory import get_api_config

    config = get_api_config(ContentType.DATA_GRID_RDP, session.config)
    name_platform = config.setdefault("underlying-platform", DataGridType.RDP)
    name_platform = data_grid_types_arg_parser.get_str(name_platform)
    content_type = data_grid_type_value_by_content_type.get(name_platform)
    return content_type


def determine_content_type_and_flag(session: "Session") -> Tuple["ContentType", bool]:
    content_type = get_content_type(session)
    changed = False

    if is_platform_session(session) and content_type == ContentType.DATA_GRID_UDF:
        content_type = ContentType.DATA_GRID_RDP
        changed = True

    return content_type, changed


def get_data_grid_type_by_session(session: "Session") -> DataGridType:
    content_type, _ = determine_content_type_and_flag(session)
    return get_data_grid_type(content_type)
