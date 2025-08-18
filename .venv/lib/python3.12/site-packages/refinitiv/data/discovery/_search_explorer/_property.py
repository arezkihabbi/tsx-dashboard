from dataclasses import dataclass
from typing import Union, Dict

import pandas as pd

from ._buckets_data import BucketsData, get_counts_labels_filters
from ._navigator import Navigator
from ..._errors import RDError
from ...content import search
from ...delivery._data._response import Response


def to_bool(value: str) -> Union[bool, None]:
    if value == "True":
        return True
    if value == "False":
        return False
    return pd.NA


def create_properties(
    df: pd.DataFrame,
    request_arguments: dict,
    search_response: Response,
    metadata_response: Response,
) -> Dict[str, "Property"]:
    properties = {}

    for data in df.values.tolist():
        name = data[0]
        properties[name] = Property(
            name=name,
            value=data[1],
            type=data[2],
            searchable=to_bool(data[3]),
            sortable=to_bool(data[4]),
            navigable=to_bool(data[5]),
            groupable=to_bool(data[6]),
            exact=to_bool(data[7]),
            symbol=to_bool(data[8]),
            request_arguments=request_arguments,
            _search_response=search_response,
            _metadata_response=metadata_response,
        )

    return properties


@dataclass
class Property:
    """Property object that has data and metadata for specific property."""

    name: str
    value: str
    type: str
    searchable: Union[bool, str]
    sortable: Union[bool, str]
    navigable: Union[bool, str]
    groupable: Union[bool, str]
    exact: Union[bool, str]
    symbol: Union[bool, str]
    request_arguments: dict
    _search_response: Response
    _metadata_response: Response

    def get_possible_values(self) -> Navigator:
        """
        Retrieves the navigator data

        Returns
        -------
            Navigator object

        Examples
        --------
        >>> from refinitiv.data.discovery._search_explorer import SearchPropertyExplorer
        >>> explorer = SearchPropertyExplorer()
        >>> santander_bonds = explorer.get_properties_for(
        ...    view=search.Views.GOV_CORP_INSTRUMENTS,
        ...    query="santander bonds",
        ...    filter="IsPerpetualSecurity ne true and IsActive eq true and not(AssetStatus in ('MAT' 'DC'))",
        ... )
        >>> rcs_issuer_country = santander_bonds.properties["RCSIssuerCountry"].get_possible_values()
        """
        raw_navigators = self._search_response.data.raw.get("Navigators", {})
        if self.name not in raw_navigators:
            definition = search.Definition(
                view=self.request_arguments["view"],
                query=self.request_arguments["query"],
                filter=self.request_arguments["filter"],
                top=1,
                select="_debugall",
                order_by=self.request_arguments["order_by"],
                navigators=self.name,
            )
            response = definition.get_data()
            raw_navigators = response.data.raw.get("Navigators")
            if not raw_navigators:
                error = RDError(-1, f"Possible values could not be reached, {self.name} property is not navigable.")
                error.response = response
                raise error

        navigator_name, navigator_data = next(iter(raw_navigators.items()))
        counts, labels, filters = get_counts_labels_filters(navigator_data["Buckets"])
        data = {navigator_name: labels, "Count": counts}

        if filters:
            data["Filter"] = filters

        return Navigator(df=pd.DataFrame(data), navigator=BucketsData(name=navigator_name, value=labels, count=counts))
