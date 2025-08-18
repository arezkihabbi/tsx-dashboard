from dataclasses import dataclass
from itertools import zip_longest
from typing import Any, TYPE_CHECKING

import pandas as pd
from pandas import DataFrame

from ..._content_data import Data as ContentData
from ..._content_data_provider import ContentDataProvider
from ..._content_response_factory import ContentResponseFactory
from ..._error_parser import ErrorParser
from ...._tools import (
    ArgsParser,
    fields_arg_parser,
    merge_dict_to_dict,
    convert_df_columns_to_datetime_by_idx,
    convert_dtypes,
)
from ....delivery._data._data_provider import ContentValidator, RequestFactory, ValidatorContainer
from ....delivery.endpoint_request import RequestMethod

if TYPE_CHECKING:
    from ....delivery._data._data_provider import ParsedData


# --------------------------------------------------------------------------------------
#   Content data validator
# --------------------------------------------------------------------------------------


class ContractsContentValidator(ContentValidator):
    @classmethod
    def any_valid_content_data(cls, data: "ParsedData") -> bool:
        content_data = data.content_data
        headers = content_data.get("headers", [])
        datas = content_data.get("data", [])
        err_codes = []
        err_msgs = []

        for header, *data_items in zip(headers, *datas):
            header_name = header["name"]

            if "ErrorCode" == header_name:
                err_codes = data_items

            elif "ErrorMessage" == header_name:
                err_msgs = data_items

        counter = len(datas) or 1  # because datas can be empty list
        if err_codes or err_msgs:
            for err_code, err_msg in zip_longest(err_codes, err_msgs, fillvalue=None):
                if err_code or err_msg:
                    counter -= 1
                    data.error_codes.append(err_code)
                    data.error_messages.append(err_msg)

        if counter == 0:
            return False

        return True

    def __init__(self) -> None:
        super().__init__()
        self.validators.append(self.any_valid_content_data)


# ---------------------------------------------------------------------------
#   Content data
# ---------------------------------------------------------------------------


def convert_data_items_to_datetime(df: pd.DataFrame, headers: dict) -> pd.DataFrame:
    columns_indexes = [index for index, header in enumerate(headers) if header.get("type", "") in ["DateTime", "Date"]]

    df = convert_df_columns_to_datetime_by_idx(df, columns_indexes, utc=True, delete_tz=True)
    return df


def financial_contracts_build_df(raw: dict, **kwargs) -> pd.DataFrame:
    """
    Convert "data" from raw response bond to dataframe format
    """
    data = raw.get("data")
    headers = raw.get("headers")
    if data:
        columns = [header["name"] for header in headers]
        df = DataFrame(data, columns=columns)
        df = convert_data_items_to_datetime(df, headers)
        df = convert_dtypes(df)
    else:
        df = DataFrame()
    return df


@dataclass
class Data(ContentData):
    """
    This class is designed for storing and managing the response instrument data
    """

    _analytics_headers: Any = None
    _analytics_data: Any = None
    _analytics_market_data: Any = None
    _analytics_statuses: Any = None

    def __post_init__(self):
        if self.raw:
            #   get headers
            self._analytics_headers = self.raw.get("headers")
            #   get data
            self._analytics_data = self.raw.get("data")
            #   get marketData
            self._analytics_market_data = self.raw.get("marketData")
            #   get statuses
            self._analytics_statuses = self.raw.get("statuses")

    @property
    def analytics_headers(self):
        return self._analytics_headers

    @property
    def analytics_data(self):
        return self._analytics_data

    @property
    def analytics_market_data(self):
        return self._analytics_market_data

    @property
    def analytics_statuses(self):
        return self._analytics_statuses

    @property
    def marketdata_df(self):
        """
        Convert "marketData" from raw response bond to dataframe format
        """
        return None


# ---------------------------------------------------------------------------
#   Request factory
# ---------------------------------------------------------------------------


class ContractsRequestFactory(RequestFactory):
    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if not extended_params:
            return body_parameters

        if kwargs.get("__plural__") is True:
            body_parameters.update(extended_params)
            return body_parameters

        universes = body_parameters.get("universe", [{}])
        universes[0] = merge_dict_to_dict(universes[0], extended_params)
        return body_parameters

    def get_request_method(self, *, method=None, **kwargs):
        return method or RequestMethod.POST

    def get_body_parameters(
        self,
        *args,
        universe=None,
        definition=None,
        fields=None,
        outputs=None,
        pricing_parameters=None,
        **kwargs,
    ):
        plural = kwargs.get("__plural__")
        if plural is True:
            input_universe = universe
        else:
            input_universe = [definition]

        universe = []
        for item in input_universe:
            item_defn = item
            item_pricing_parameters = not plural and pricing_parameters
            item_extended_params = None

            if hasattr(item, "_kwargs"):
                kwargs = getattr(item, "_kwargs")
                item_defn = kwargs.get("definition")
                item_pricing_parameters = kwargs.get("pricing_parameters")
                item_extended_params = kwargs.get("extended_params")

            inst_defn_dict = item_defn.get_dict()

            if item_extended_params:
                inst_defn_dict.update(item_extended_params)

            data = {
                "instrumentType": item_defn.get_instrument_type(),
                "instrumentDefinition": inst_defn_dict,
            }

            if item_pricing_parameters:
                data["pricingParameters"] = item_pricing_parameters.get_dict()

            universe.append(data)

        body_parameters = {"universe": universe}

        if fields:
            fields = fields_arg_parser.get_list(fields)
            body_parameters["fields"] = fields

        if pricing_parameters and plural is True:
            body_parameters["pricingParameters"] = pricing_parameters.get_dict()

        return body_parameters


def get_data(definition, pricing_parameters=None):
    fields = None
    extended_params = None

    if hasattr(definition, "_kwargs"):
        kwargs = getattr(definition, "_kwargs")
        definition = kwargs.get("definition")
        fields = kwargs.get("fields")
        pricing_parameters = kwargs.get("pricing_parameters")
        extended_params = kwargs.get("extended_params")

    definition_dict = definition.get_dict()

    if extended_params:
        definition_dict.update(extended_params)

    data = {
        "instrumentType": definition.get_instrument_type(),
        "instrumentDefinition": definition_dict,
    }

    if fields:
        fields = fields_arg_parser.get_list(fields)
        data["fields"] = fields

    if pricing_parameters:
        data["pricingParameters"] = pricing_parameters.get_dict()

    return data


def process_bond_instrument_code(code: Any) -> str:
    if code is None or isinstance(code, str):
        return code
    else:
        raise ValueError(f"Invalid type of instrument_code, string is expected. type: {type(code)} is given")


bond_instrument_code_arg_parser = ArgsParser(process_bond_instrument_code)

# ---------------------------------------------------------------------------
#   Data provider
# ---------------------------------------------------------------------------

contracts_data_provider = ContentDataProvider(
    request=ContractsRequestFactory(),
    response=ContentResponseFactory(data_class=Data),
    validator=ValidatorContainer(content_validator=ContractsContentValidator()),
    parser=ErrorParser(),
)
