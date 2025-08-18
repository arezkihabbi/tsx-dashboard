from typing import List, Dict

from dateutil.parser import parse

from ._context import RDPMixin
from ._cust_inst_context import CustInstContext


class CustInstRDPContext(RDPMixin, CustInstContext):
    @staticmethod
    def get_headers(headers: dict) -> List[str]:
        return [item["name"].lower() if item["name"] == "DATE" else item["name"] for item in headers]

    def _parse_list_to_data(self, raw: list, field_to_idx: dict) -> List[List[dict]]:
        data = []

        for raw_item in raw:
            if not raw_item:
                continue

            ric = raw_item["universe"]["ric"]
            headers = self.get_headers(raw_item["headers"])

            for raw_item_data in raw_item["data"]:
                template = {"instrument": ric}

                for header, raw_data in zip(headers, raw_item_data):
                    try:
                        parse(raw_data, fuzzy=False)
                        raw_data = f"{raw_data} 00:00:00"
                        template.update({header: raw_data})
                    except (ValueError, TypeError):
                        template.update({header: raw_data})

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
            template = {"instrument": ric}

            for header, raw_data in zip(headers, raw_data_item):
                try:
                    parse(raw_data, fuzzy=False)
                    raw_data = f"{raw_data} 00:00:00"
                    template.update({header: raw_data})
                except (ValueError, TypeError):
                    template.update({header: raw_data})

            item = []
            for field in field_to_idx:
                item.insert(field_to_idx[field], template.get(field))

            data.append(item)

        return data

    def prepare_data(self, raw, fields) -> list:
        field_to_idx = {"instrument": 0, "date": 1}
        field_to_idx.update({field: fields.index(field) + 2 for field in fields})

        if isinstance(raw, dict):
            return self._parse_dict_to_data(raw, field_to_idx)

        elif isinstance(raw, list):
            return self._parse_list_to_data(raw, field_to_idx)

    @staticmethod
    def prepare_headers(raw) -> List[Dict[str, str]]:
        headers = [
            {"name": "instrument", "title": "Instrument"},
            {"name": "date", "title": "Date"},
        ]

        for item in raw:
            headers.append({"name": item, "title": item})

        return headers
