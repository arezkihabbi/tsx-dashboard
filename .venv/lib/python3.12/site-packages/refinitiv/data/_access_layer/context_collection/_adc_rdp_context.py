from typing import List, Dict

from ._adc_context import ADCContext
from ._context import RDPMixin
from ..._tools import cached_property


class ADCRDPContext(RDPMixin, ADCContext):
    @staticmethod
    def prepare_headers(raw: dict, fields: list) -> List[Dict[str, str]]:
        field_to_idx = {field.casefold(): fields.index(field) + 2 for field in fields}

        headers = [
            {"name": "instrument", "title": "Instrument"},
            {"name": "date", "title": "Date"},
        ]

        for header in raw["headers"]:
            field = f"{header['name']}.{header['title']}".casefold()
            header_name = header["name"].casefold()

            if header_name in field_to_idx and field not in field_to_idx:
                headers.insert(field_to_idx[header_name], header)
                field_to_idx.pop(header_name)

            if field in field_to_idx:
                headers.insert(field_to_idx[field], header)
                field_to_idx.pop(field)

        for field, index in field_to_idx.items():
            headers.insert(index, {"name": field.upper(), "title": field.upper()})

        return headers

    def get_fields(self, headers, user_fields) -> List[str]:
        fields = []
        user_fields = [field.casefold() for field in user_fields]

        for header in headers:
            header_name = header["name"]
            header_title = header["title"]
            field = f"{header_name}.{header_title}".casefold()

            if header_name.casefold() == "instrument":
                continue

            elif field in user_fields:
                fields.append(f"{header_name}.{header_title}")

            else:
                fields.append(header_name)

        return fields

    @cached_property
    def headers_names(self) -> List[str]:
        return [
            header.get("name" if self.use_field_names_in_headers else "title") for header in self.raw.get("headers", [])
        ]
