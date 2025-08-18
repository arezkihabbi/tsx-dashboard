import warnings
from dataclasses import dataclass
from typing import Dict, Iterable, List, TYPE_CHECKING

import pandas as pd

from .._content_data import Data
from .._content_data_provider import ContentDataProvider
from .._content_response_factory import ContentResponseFactory
from .._error_parser import ErrorParser
from ..._tools import convert_df_columns_to_datetime, convert_dtypes
from ...delivery._data._data_provider import RequestFactory
from ...delivery.endpoint_request import RequestMethod

if TYPE_CHECKING:
    from ...delivery._data._data_provider import ParsedData


# --------------------------------------------------------------------------------------
#   Response
# --------------------------------------------------------------------------------------


def _get_unique_keys(list_of_dict: Iterable[Dict]) -> list:
    keys = []
    unique_keys = set()

    for item in list_of_dict:
        unique_keys.update(item)
        if len(keys) < len(item):
            keys = list(item.keys())

    diff_set = unique_keys - set(keys)
    if diff_set:
        keys += diff_set

    return keys


def discovery_search_build_df(raw: dict, **kwargs) -> pd.DataFrame:
    if "Hits" not in raw:
        return pd.DataFrame()

    hits = raw["Hits"]
    keys = _get_unique_keys(hits)
    hit_dataframe = {key: [item.get(key) for item in hits] for key in keys}

    if hit_dataframe:
        df = pd.DataFrame(hit_dataframe)
        convert_df_columns_to_datetime(df, entry="Date", utc=True, delete_tz=True)
        df = convert_dtypes(df)
        return df

    return pd.DataFrame()


def discovery_lookup_build_df(raw: dict, **kwargs) -> pd.DataFrame:
    if "Matches" not in raw:
        return pd.DataFrame()

    match_df = {}
    matches = raw["Matches"]
    matches_list_of_dict = list(matches.values())
    property_names = _get_unique_keys(matches_list_of_dict)

    for match_name, match_value_dict in matches.items():
        for property_name in property_names:
            match_property_df_dict = match_df.setdefault(property_name, {})

            get_name = match_value_dict.get(property_name)
            match_property_df_dict[match_name] = get_name

    if not match_df:
        return pd.DataFrame()

    df = pd.DataFrame(match_df)
    df = convert_dtypes(df)
    return df


#   response data keyword
_ResponsePropertiesName = "Properties"
_ResponseTypeName = "Type"

#       flags
_ResponseFlagNames = [
    _ResponseTypeName,
    # flags
    "Searchable",
    "Sortable",
    "Navigable",
    "Groupable",
    "Exact",
    "Symbol",
]


def _extend_tuple_with_last_element(input_tuple, num_expected_tuple_elements):
    """do extend the input tuple by duplicate last element value to be the
    expected number of tuple elements"""
    num_input_tuple_elements = len(input_tuple)
    return input_tuple + input_tuple[num_input_tuple_elements - 1 :] * (
        num_expected_tuple_elements - num_input_tuple_elements
    )


def _convert_property_attributes(
    property_attribute_to_property_dict_dict,
    property_name,
    ancestor_property_name_type,
    property_attribute_dict,
):
    """convert each property into a dictionary of property attribute
    to property dictionary"""
    #   depth of this property
    this_property_depth = 1

    #   determine this attribute name tuple
    attribute_name_type = ancestor_property_name_type[:] + (property_name,)

    #   check the attribute type is nested or not?
    property_attribute_type = property_attribute_dict[_ResponseTypeName]
    if property_attribute_type == "Nested":
        #   this property is a nested type, recursive convert this property attribute
        #   extract properties of this nested type
        this_properties_of_nested_type = property_attribute_dict[_ResponsePropertiesName]

        #   loop over all nested attributes and convert it
        for (
            nested_property_name,
            nested_property_attribute_dict,
        ) in this_properties_of_nested_type.items():
            #   call convert recusivly for nested type
            _convert_property_attributes(
                property_attribute_to_property_dict_dict,
                nested_property_name,
                attribute_name_type,
                nested_property_attribute_dict,
            )

        #   increase property depth by one
        this_property_depth += 1

    #   convert the attribute flags of this property attributes
    #       loop over all possible attributes and convert it
    for property_attribute_name in _ResponseFlagNames:
        #   add properties of properties to dict of dict
        #       fill with None if the properties doesn't exist
        property_dict = property_attribute_to_property_dict_dict.setdefault(property_attribute_name, {})
        property_dict[attribute_name_type] = property_attribute_dict.get(property_attribute_name, False)

    return this_property_depth


def discovery_metadata_build_df(raw: dict, **kwargs) -> pd.DataFrame:
    """parse the metadata response from dict of dict to be a dict of dict tuple"""
    if _ResponsePropertiesName not in raw:
        return pd.DataFrame()

    property_attribute_to_property_dict_dict = {}
    property_name_to_depth_dict = {}

    properties = raw[_ResponsePropertiesName]

    # loop over view metadata and convert it to dict of dict tuple
    for property_name, property_attribute_dict in properties.items():
        # do convert each property attributes into dict of dict
        this_property_depth = _convert_property_attributes(
            property_attribute_to_property_dict_dict,
            property_name,
            (),
            property_attribute_dict,
        )

        # store each property depth as dict
        property_name_to_depth_dict[property_name] = this_property_depth

    ######################################################
    # convert response to be a dataframe format
    # warning OPTIMIZE_ME :: THIS CAN BE OPTIMIZE

    #   determine the maximum depth on nested property
    max_property_depth = max(property_name_to_depth_dict.values())

    # loop over all the propertyAttributeToPropertyDictDict
    # and convert to a dataframe format
    data = {}
    for (
        property_attribute_name,
        property_dict,
    ) in property_attribute_to_property_dict_dict.items():
        for property_key, property_value in property_dict.items():
            #   construct the property attribute for this property
            dataframe_property_dict = data.setdefault(property_attribute_name, {})

            #   construct the key of dataframe property
            dataframe_property_key = _extend_tuple_with_last_element(property_key, max_property_depth)
            dataframe_property_dict[dataframe_property_key] = property_value

    if len(data) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df = convert_dtypes(df)
    return df


class Bucket:
    def __init__(self, data):
        self._data = data
        self._subnavigator = None

    @property
    def label(self):
        return self._data["Label"]

    @property
    def navigator(self):
        if not self._subnavigator:
            for name, value in self._data.items():
                if isinstance(self._data[name], dict):
                    buckets_objects = [Bucket(bucket) for bucket in self._data[name]["Buckets"]]
                    self._subnavigator = Navigator(buckets_objects, name)
        return self._subnavigator

    @property
    def count(self):
        return self._data["Count"]

    def __getitem__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise KeyError(f"'{name}' property does not exist.")


@dataclass
class HitsItem:
    BusinessEntity: str
    DocumentTitle: str
    PermID: str
    PI: str
    RIC: str


@dataclass
class Navigator:
    buckets: List
    name: str


@dataclass
class SearchData(Data):
    _navigators: Dict[str, Navigator] = None
    _hits: List[HitsItem] = None
    _total: int = None

    @property
    def total(self):
        if not self._total:
            self._total = self.raw.get("Total")
        return self._total

    @property
    def hits(self):
        if not self._hits:
            self._hits = [
                HitsItem(
                    item.get("BusinessEntity"),
                    item.get("DocumentTitle"),
                    item.get("PermID"),
                    item.get("PI"),
                    item.get("RIC"),
                )
                for item in self.raw.get("Hits", [])
            ]
        return self._hits

    @property
    def navigators(self):
        if not self._navigators:
            self._navigators = {
                name: Navigator([Bucket(bucket) for bucket in buckets["Buckets"]], name)
                for name, buckets in self.raw.get("Navigators", {}).items()
            }

        return self._navigators


class SearchResponseFactory(ContentResponseFactory):
    def create_success(self, parsed_data: "ParsedData", **kwargs):
        inst = super().create_success(parsed_data, **kwargs)
        skipped = parsed_data.content_data.get("Skipped", 0)
        total = parsed_data.content_data.get("Total", 0)
        hits = len(parsed_data.content_data.get("Hits", []))
        query = kwargs.get("query", "")
        if total > hits + skipped == 10000:
            warnings.warn(
                f"Search result for {query} not full.\n"
                f"Result is maxed at 10000 while the total is {total} rows.\n"
                f"Requested - {hits}, skipped - {skipped} rows."
            )

        inst.total = total
        return inst


# --------------------------------------------------------------------------------------
#   Request
# --------------------------------------------------------------------------------------


class BaseSearchRequestFactory(RequestFactory):
    defn_params_by_body_params = {}

    def get_body_parameters(self, *_, **kwargs) -> dict:
        return {
            self.defn_params_by_body_params[param_name]: param_value
            for param_name, param_value in kwargs.items()
            if param_name in self.defn_params_by_body_params and param_value is not None
        }

    def get_request_method(self, **kwargs) -> RequestMethod:
        return RequestMethod.POST


class SearchRequestFactory(BaseSearchRequestFactory):
    defn_params_by_body_params = {
        "boost": "Boost",
        "features": "Features",
        "filter": "Filter",
        "group_by": "GroupBy",
        "group_count": "GroupCount",
        "navigators": "Navigators",
        "order_by": "OrderBy",
        "query": "Query",
        "scope": "Scope",
        "select": "Select",
        "skip": "Skip",
        "terms": "Terms",
        "top": "Top",
        "view": "View",
    }


class LookupRequestFactory(BaseSearchRequestFactory):
    defn_params_by_body_params = {
        "boost": "Boost",
        "filter": "Filter",
        "scope": "Scope",
        "select": "Select",
        "terms": "Terms",
        "view": "View",
    }


class MetadataRequestFactory(RequestFactory):
    def get_query_parameters(self, *, view, **_):
        return view

    def add_query_parameters(self, url, query_parameters) -> str:
        return f"{url}/{query_parameters}"


# --------------------------------------------------------------------------------------
#   Data provider
# --------------------------------------------------------------------------------------


search_data_provider = ContentDataProvider(
    request=SearchRequestFactory(),
    response=SearchResponseFactory(data_class=SearchData),
    parser=ErrorParser(),
)

lookup_data_provider = ContentDataProvider(
    request=LookupRequestFactory(),
    parser=ErrorParser(),
)

metadata_data_provider = ContentDataProvider(
    request=MetadataRequestFactory(),
    parser=ErrorParser(),
)
