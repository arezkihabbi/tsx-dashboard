from typing import List, Union, Dict

from ._context import UDFMixin
from ._cust_inst_context import CustInstContext


class CustInstUDFContext(UDFMixin, CustInstContext):
    def get_headers(self, headers: dict) -> List[str]:
        return [item["name"].capitalize() if item["name"] == "DATE" else item["name"] for item in headers]

    def _parse_list_to_data(self, raw: list, field_to_idx: dict) -> List[List[dict]]:
        data = []

        for raw_item in raw:
            if not raw_item:
                continue

            ric = raw_item["universe"]["ric"]
            headers = self.get_headers(raw_item["headers"])

            for raw_item_data in raw_item["data"]:
                template = {"Instrument": ric}
                template.update({header: data for header, data in zip(headers, raw_item_data)})
                item = []
                for field in field_to_idx:
                    item.insert(field_to_idx[field], template.get(field))

                data.append(item)

        return data

    def _parse_dict_to_data(self, raw: dict, field_to_idx: dict) -> List[List[dict]]:
        data = []

        ric = raw["universe"]["ric"]
        headers = self.get_headers(raw["headers"])

        for raw_data_item in raw["data"]:
            template = {"Instrument": ric}
            template.update({header: data for header, data in zip(headers, raw_data_item)})
            item = []
            for field in field_to_idx:
                item.insert(field_to_idx[field], template.get(field))

            data.append(item)

        return data

    def prepare_data(self, raw, fields) -> List[List[dict]]:
        field_to_idx = {"Instrument": 0, "Date": 1}
        field_to_idx.update({item: fields.index(item) + 2 for item in fields})

        if isinstance(raw, dict):
            return self._parse_dict_to_data(raw, field_to_idx)

        elif isinstance(raw, list):
            return self._parse_list_to_data(raw, field_to_idx)

    @staticmethod
    def prepare_headers(raw: Union[list, dict]) -> List[List[Dict]]:
        headers = [{"displayName": "Instrument"}, {"displayName": "Date"}]

        for item in raw:
            headers.append({"displayName": item, "field": item})

        return [headers]
