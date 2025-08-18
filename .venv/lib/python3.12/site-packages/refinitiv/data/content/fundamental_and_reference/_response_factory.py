from typing import TYPE_CHECKING

from ._content_validator import NO_ROW_HEADERS_COUNT_MESSAGE
from .._content_response_factory import ContentResponseFactory
from .._df_build_type import DFBuildType
from ...delivery._data._response_factory import TypeResponse

if TYPE_CHECKING:
    from ...delivery._data._data_provider import ParsedData

error_message_by_code = {
    "default": "{error_message} Requested universes: {universes}. Requested fields: {fields}",
    412: "Unable to resolve all requested identifiers in {universes}.",
    218: "Unable to resolve all requested fields in {fields}. The formula must "
    "contain at least one field or function.",
}


class DataGridResponseFactory(ContentResponseFactory):
    def create_fail(self, parsed_data: "ParsedData", universe=None, fields=None, **kwargs):
        error_code = parsed_data.first_error_code
        if error_code not in error_message_by_code.keys():
            parsed_data.error_messages = error_message_by_code["default"].format(
                error_message=parsed_data.first_error_message,
                fields=fields,
                universes=universe,
            )
        else:
            parsed_data.error_messages = error_message_by_code[error_code].format(fields=fields, universes=universe)

        return super().create_fail(parsed_data, **kwargs)


class DataGridRDPResponseFactory(DataGridResponseFactory):
    def create_success(self, parsed_data: "ParsedData", **kwargs):
        inst = super().create_success(parsed_data, **kwargs)
        descriptions = self.get_raw(parsed_data).get("messages", {}).get("descriptions", [])
        for descr in descriptions:
            code = descr.get("code")
            if code in {416, 413}:
                inst.errors.append((code, descr.get("description")))

        return inst


class DataGridUDFResponseFactory(DataGridResponseFactory):
    def get_raw(self, parsed_data: "ParsedData"):
        return parsed_data.content_data.get("responses", [{}])[0]

    def create_success(self, parsed_data: "ParsedData", **kwargs):
        inst = super().create_success(parsed_data, **kwargs)
        error = self.get_raw(parsed_data).get("error", [])
        for err in error:
            code = err.get("code")
            if code == 416:
                inst.errors.append((code, err.get("message")))

        return inst

    def create_response(self, is_success: bool, parsed_data: "ParsedData", **kwargs) -> TypeResponse:
        if parsed_data.error_messages == [NO_ROW_HEADERS_COUNT_MESSAGE]:
            is_success = True
            kwargs["__dfbuild_type__"] = DFBuildType.EMPTY
        return super().create_response(is_success, parsed_data, **kwargs)
