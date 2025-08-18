from typing import List, Dict

from ._adc_context import ADCContext
from ._context import UDFMixin
from ..._tools import cached_property


class ADCUDFContext(UDFMixin, ADCContext):
    @staticmethod
    def prepare_headers(raw: dict, fields: list) -> List[List[Dict[str, str]]]:
        field_to_idx = {field.upper(): fields.index(field) + 2 for field in fields}
        headers = [{"displayName": "Instrument"}, {"displayName": "Date"}]

        for header in raw["headers"][0]:
            if len(header) > 1:
                field_upper = header["field"].upper()

                if field_upper not in field_to_idx:
                    continue

                headers.insert(field_to_idx[field_upper], header)
                field_to_idx.pop(field_upper)

        for field, index in field_to_idx.items():
            headers.insert(index, {"displayName": field, "field": field})

        return [headers]

    def get_fields(self, headers, user_fields) -> List[str]:
        return [header["name"] for header in headers if header["name"] != "Instrument"]

    @cached_property
    def headers_names(self) -> List[str]:
        """
        Examples
        -------
        >>> raw_headers_ = [
        ...     [
        ...         {'displayName': 'Instrument'},
        ...         {'displayName': 'Currency', 'field': 'TR.REVENUEMEAN.currency'},
        ...         {'displayName': 'Date', 'field': 'TR.REVENUEMEAN.DATE'}
        ...     ]
        ... ]
        >>> headers_names_ = ['Instrument', 'TR.REVENUEMEAN.currency', 'TR.REVENUEMEAN.DATE']
        """
        raw_headers = self.raw.get("headers", [{}])[0]
        headers_names = []
        key = "field" if self.use_field_names_in_headers else "displayName"
        for raw_header in raw_headers:
            header_name = raw_header.get(key)
            if not header_name:
                header_name = raw_header.get("displayName")
            headers_names.append(header_name)
        return headers_names
