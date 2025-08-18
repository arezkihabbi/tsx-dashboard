import copy
import re
from typing import Tuple, List, Union

from pandas import DataFrame, NA

from ._relationship_type import RelationshipType
from ._stakeholder_data import Customer, Supplier, StakeholderData
from ..._tools import convert_df_columns_to_datetime_re
from ...content import fundamental_and_reference, symbol_conversion
from ...delivery._data._response import Response

data_class_by_relationship_type = {
    RelationshipType.CUSTOMER: Customer,
    RelationshipType.SUPPLIER: Supplier,
}

FIELDS = (
    "TR.SCRelationship",
    "TR.SCRelationship.ScorgIDOut",
    "TR.SCRelationshipConfidenceScore",
    "TR.SCRelationshipFreshnessScore",
    "TR.SCRelationshipUpdateDate",
)
FIELD_TO_UPDATE = (
    "TR.IsPublic",
    "TR.CommonName",
    "TR.HeadquartersCountry",
    "TR.TRBCIndustry",
    "TR.CreditRatioImpliedRating",
    "TR.PCSmartRatiosImpliedRating",
)
TO_SYMBOL_TYPES = [
    symbol_conversion.SymbolTypes.RIC,
    symbol_conversion.SymbolTypes.ISIN,
    symbol_conversion.SymbolTypes.CUSIP,
    symbol_conversion.SymbolTypes.SEDOL,
]

STAKEHOLDERS_DATE_PATTERN = re.compile(r".*Date")


def get_fundamental_data(instrument: Union[list, tuple], fields=None) -> Response:
    if fields is None:
        fields = FIELDS
    response = fundamental_and_reference.Definition(universe=instrument, fields=fields).get_data()
    return response


def get_symbol_conversion_data(ric_list: Union[list, tuple]) -> Response:
    response = symbol_conversion.Definition(
        symbols=ric_list,
        from_symbol_type=symbol_conversion.SymbolTypes.OA_PERM_ID,
        to_symbol_types=TO_SYMBOL_TYPES,
    ).get_data()
    return response


def get_df_column(fund_data_column: list, symbol_data: dict):
    column = copy.copy(fund_data_column)
    current_symbol_data = symbol_data.get(column[3], {})
    column = (
        column[:5]
        + [
            # current_symbol_data.get("DocumentTitle", "").split(",")[0],
            current_symbol_data.get("RIC"),
            current_symbol_data.get("IssueISIN"),
            current_symbol_data.get("CUSIP"),
            current_symbol_data.get("SEDOL"),
        ]
        + column[5:]
    )
    if column[1] in (None, ""):
        column[1] = NA
    return column


def get_columns(first_fund_response: "Response", second_fund_response: "Response"):
    fund_headers = copy.copy(first_fund_response.data.raw["headers"][0])
    fund_headers.insert(1, second_fund_response.data.raw["headers"][0][1])
    fund_headers.insert(4, second_fund_response.data.raw["headers"][0][2])
    fund_headers.extend(second_fund_response.data.raw["headers"][0][3:])

    columns = [i["displayName"] for i in fund_headers]
    columns = columns[:5] + ["RIC", "IssueISIN", "CUSIP", "SEDOL"] + columns[5:]
    return columns


def update_fund_data(fund_data: Union[list, tuple], fund_response: "Response"):
    fundamental_org_data = {i[0]: i[1:] for i in fund_response.data.raw["data"]}
    for i, v in enumerate(fund_data):
        data_for_update = fundamental_org_data.get(v[2], [None] * 6)
        v.insert(1, data_for_update[0])
        v.insert(4, data_for_update[1])
        v.extend(data_for_update[2:])


def fetch_data(
    instrument: Union[str, list], relationship_type: RelationshipType
) -> Tuple[List[StakeholderData], DataFrame]:
    first_fund_response = get_fundamental_data(instrument)
    fund_data = tuple(
        filter(lambda elem: elem[1] == relationship_type.value, first_fund_response.data.raw.get("data", []))
    )
    # fund_data -> (['VOD.L', 'Supplier', '4295858439', 0.2648416, 1, '2013-06-04'], ...)
    ric_list = tuple(map(lambda elem: elem[2], fund_data))
    # ric_list -> ["5000051106", ...]

    second_fund_response = get_fundamental_data(ric_list, fields=FIELD_TO_UPDATE)
    update_fund_data(fund_data, second_fund_response)
    # fund_data -> [['VOD.L', True, 'Supplier', '4295858439', 0.2648416, 1, '2013-06-04', 'Australia', 'Real Estate Rental, Development & Operations', 'BBB+', ''], ...]

    symbol_response = get_symbol_conversion_data(ric_list)
    symbol_data = symbol_response.data.raw.get("Matches")
    # symbol_data -> {"5000051106": {"DocumentTitle": "Indian", "RIC": "IOTL.NS"}, ...}

    data_for_df = []
    stakeholders = []
    for stakeholder_data in fund_data:
        stakeholder = data_class_by_relationship_type[relationship_type].from_list(stakeholder_data)

        stakeholder_symbol_data = symbol_data.get(stakeholder.related_organization_id)
        if stakeholder_symbol_data:
            stakeholder.update(stakeholder_symbol_data)

        stakeholders.append(stakeholder)

        data_for_df.append(get_df_column(stakeholder_data, symbol_data))

    columns = get_columns(first_fund_response, second_fund_response)
    df = DataFrame(data_for_df, columns=columns).convert_dtypes()
    df = convert_df_columns_to_datetime_re(df, STAKEHOLDERS_DATE_PATTERN)
    return stakeholders, df
